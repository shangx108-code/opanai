#!/usr/bin/env python3
"""Robust-mask mitigation training and baseline comparison in the project long-term space."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from optics_propagation import PropagationConfig
from run_baseline_phase_only_megadiverse_train_dual_heldout_thickstats import (
    PhaseOnlyConfig,
    build_features,
    build_split_samples,
    build_targets,
    fit_ridge_regression,
    make_aberration_cases,
    make_phase_basis,
    optimize_phase_coeffs,
    phase_masks_from_coeffs,
    predict_ridge,
)
from run_baseline_reference_psf import psnr
from run_mixed_train_natural_object_rerun import build_mixed_training_objects
from run_natural_object_evaluation import dataset_dir_name, load_grayscale_objects, load_subset_index, staging_root
from run_mixed_train_tolerance import quantize_masks, shift_masks


@dataclass
class RobustMaskConfig:
    seeds: tuple[int, ...] = (0, 1, 2)
    train_case_count: int = 24
    eval_case_count: int = 6
    spectral_crop_size: int = 6
    robust_variants: tuple[tuple[int | None, int], ...] = (
        (None, 0),
        (4, 0),
        (3, 0),
        (None, 1),
    )


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def tolerance_root() -> Path:
    return project_root() / "results" / "tolerance"


def build_variant_features(
    samples: list[dict[str, object]],
    masks: np.ndarray,
    propagation: PropagationConfig,
    variants: tuple[tuple[int | None, int], ...],
) -> np.ndarray:
    blocks = []
    for quant_bits, shift_px in variants:
        variant_masks = shift_masks(quantize_masks(masks, quant_bits), shift_px)
        blocks.append(build_features(samples, variant_masks, propagation))
    return np.concatenate(blocks, axis=0)


def robust_training_objective(
    coeffs: np.ndarray,
    basis: np.ndarray,
    train_samples: list[dict[str, object]],
    propagation: PropagationConfig,
    ridge_lambda: float,
    variants: tuple[tuple[int | None, int], ...],
) -> float:
    masks = phase_masks_from_coeffs(coeffs, basis)
    x_train = build_variant_features(train_samples, masks, propagation, variants)
    y_train = np.concatenate([build_targets(train_samples) for _ in variants], axis=0)
    weights = fit_ridge_regression(x_train, y_train, ridge_lambda)
    pred = predict_ridge(x_train, weights)
    return float(np.mean((pred - y_train) ** 2))


def optimize_phase_coeffs_robust(
    config: PhaseOnlyConfig,
    basis: np.ndarray,
    train_samples: list[dict[str, object]],
    propagation: PropagationConfig,
    variants: tuple[tuple[int | None, int], ...],
) -> np.ndarray:
    rng = np.random.default_rng(config.seed)
    coeffs = rng.normal(0.0, 0.12, size=(config.layer_count, config.phase_basis_count))
    best_loss = robust_training_objective(coeffs, basis, train_samples, propagation, config.ridge_lambda, variants)
    step = config.proposal_scale
    for _ in range(config.search_steps):
        direction = rng.normal(0.0, 1.0, size=coeffs.shape)
        for candidate in (coeffs + step * direction, coeffs - step * direction):
            loss = robust_training_objective(candidate, basis, train_samples, propagation, config.ridge_lambda, variants)
            if loss < best_loss:
                coeffs = candidate
                best_loss = loss
        step *= 0.88
    return coeffs


def train_robust_phase_model(
    seed: int,
    train_samples: list[dict[str, object]],
    cfg: RobustMaskConfig,
) -> dict[str, object]:
    phase_config = PhaseOnlyConfig(seed=seed, train_case_count=cfg.train_case_count, heldout_case_count=cfg.eval_case_count)
    basis = make_phase_basis(phase_config.lowres_size, phase_config.phase_basis_count)
    frontend_spacing = phase_config.sample_spacing * phase_config.image_size / phase_config.lowres_size
    propagation = PropagationConfig(
        grid_size=phase_config.lowres_size,
        sample_spacing=frontend_spacing,
        wavelength=phase_config.wavelength,
        propagation_distance=phase_config.propagation_distance,
    )
    coeffs = optimize_phase_coeffs_robust(phase_config, basis, train_samples, propagation, cfg.robust_variants)
    masks = phase_masks_from_coeffs(coeffs, basis)
    x_train = build_variant_features(train_samples, masks, propagation, cfg.robust_variants)
    y_train = np.concatenate([build_targets(train_samples) for _ in cfg.robust_variants], axis=0)
    weights = fit_ridge_regression(x_train, y_train, phase_config.ridge_lambda)
    return {
        "config": phase_config,
        "propagation": propagation,
        "masks": masks,
        "weights": weights,
    }


def evaluate_robust_phase_only(
    eval_samples: list[dict[str, object]],
    trained: dict[str, object],
    *,
    quant_bits: int | None,
    shift_px: int,
) -> pd.DataFrame:
    config: PhaseOnlyConfig = trained["config"]
    masks = shift_masks(quantize_masks(trained["masks"], quant_bits), shift_px)
    x_eval = build_features(eval_samples, masks, trained["propagation"])
    pred = predict_ridge(x_eval, trained["weights"])
    rows = []
    for idx, sample in enumerate(eval_samples):
        recon = pred[idx].reshape(config.lowres_size, config.lowres_size)
        rows.append(
            {
                "object_id": str(sample["object_id"]),
                "fixed_psnr_lowres": float(sample["fixed_psnr_lowres"]),
                "robust_method_psnr_lowres": float(psnr(sample["gt_lowres"], recon)),
            }
        )
    df = pd.DataFrame(rows)
    df["psnr_gain_over_fixed_lowres"] = df["robust_method_psnr_lowres"] - df["fixed_psnr_lowres"]
    return df


def main() -> int:
    cfg = RobustMaskConfig()
    mixed_train_objects, mix_counts = build_mixed_training_objects()
    tolerance_summary = json.loads((tolerance_root() / "mixed_train_tolerance_summary.json").read_text(encoding="utf-8"))
    baseline_rows = pd.DataFrame(tolerance_summary["summary_rows"])
    baseline_rows = baseline_rows.loc[baseline_rows["method"] == "phase_only_stack"].reset_index(drop=True)

    perturbations = [
        ("clean_reference", 0.0, None, 0),
        ("phase_mask_quantization", 3.0, 3, 0),
        ("phase_mask_quantization", 4.0, 4, 0),
        ("phase_mask_lateral_shift", 1.0, None, 1),
        ("phase_mask_lateral_shift", 2.0, None, 2),
    ]

    all_rows: list[pd.DataFrame] = []
    for seed in cfg.seeds:
        phase_config = PhaseOnlyConfig(seed=seed, train_case_count=cfg.train_case_count, heldout_case_count=cfg.eval_case_count)
        train_cases = make_aberration_cases(cfg.train_case_count, seed)
        eval_cases = make_aberration_cases(cfg.eval_case_count, seed + 500)
        train_samples = build_split_samples(mixed_train_objects, "train", train_cases, phase_config)
        trained = train_robust_phase_model(seed, train_samples, cfg)

        for spec in load_subset_index():
            objects = [arr for _, arr in load_grayscale_objects(staging_root() / dataset_dir_name(spec))]
            eval_samples = build_split_samples(objects, "natural_object_eval", eval_cases, phase_config)
            for index, (name, _) in enumerate(load_grayscale_objects(staging_root() / dataset_dir_name(spec))):
                for case_id in range(cfg.eval_case_count):
                    sample_index = case_id * len(objects) + index
                    eval_samples[sample_index]["object_id"] = f"{spec.dataset_name}:{name}"
            for family, level, quant_bits, shift_px in perturbations:
                df = evaluate_robust_phase_only(eval_samples, trained, quant_bits=quant_bits, shift_px=shift_px)
                df["seed"] = seed
                df["dataset_name"] = spec.dataset_name
                df["dataset_version"] = spec.dataset_version
                df["perturbation_family"] = family
                df["level"] = level
                df["training_regime"] = "robust_mask_mixed_train"
                all_rows.append(df)

    metrics = pd.concat(all_rows, ignore_index=True)
    robust_summary = (
        metrics.groupby(["perturbation_family", "level", "dataset_name"], as_index=False)
        .agg(
            robust_mean_psnr_gain_over_fixed_lowres=("psnr_gain_over_fixed_lowres", "mean"),
            robust_better_than_fixed_fraction=("psnr_gain_over_fixed_lowres", lambda s: float((s > 0.0).mean())),
        )
    )

    compare = robust_summary.merge(
        baseline_rows[["perturbation_family", "level", "dataset_name", "mean_psnr_gain_over_fixed_lowres", "better_than_fixed_fraction"]],
        on=["perturbation_family", "level", "dataset_name"],
        how="left",
    )
    compare = compare.rename(
        columns={
            "mean_psnr_gain_over_fixed_lowres": "baseline_mean_psnr_gain_over_fixed_lowres",
            "better_than_fixed_fraction": "baseline_better_than_fixed_fraction",
        }
    )
    compare["gain_delta_vs_baseline"] = (
        compare["robust_mean_psnr_gain_over_fixed_lowres"] - compare["baseline_mean_psnr_gain_over_fixed_lowres"]
    )

    # Clean reference row has no exact baseline counterpart in the tolerance summary; fill from propagation-distance 0.
    clean_mask = compare["perturbation_family"] == "clean_reference"
    for idx in compare.index[clean_mask]:
        dataset_name = compare.at[idx, "dataset_name"]
        baseline_row = baseline_rows[
            (baseline_rows["perturbation_family"] == "propagation_distance_error")
            & (baseline_rows["level"] == 0.0)
            & (baseline_rows["dataset_name"] == dataset_name)
        ].iloc[0]
        compare.at[idx, "baseline_mean_psnr_gain_over_fixed_lowres"] = baseline_row["mean_psnr_gain_over_fixed_lowres"]
        compare.at[idx, "baseline_better_than_fixed_fraction"] = baseline_row["better_than_fixed_fraction"]
        compare.at[idx, "gain_delta_vs_baseline"] = (
            compare.at[idx, "robust_mean_psnr_gain_over_fixed_lowres"] - baseline_row["mean_psnr_gain_over_fixed_lowres"]
        )

    out_dir = tolerance_root()
    metrics_path = out_dir / "robust_mask_tolerance_metrics.csv"
    summary_path = out_dir / "robust_mask_tolerance_compare.json"
    compare_csv_path = out_dir / "robust_mask_tolerance_compare.csv"
    metrics.to_csv(metrics_path, index=False)
    compare.to_csv(compare_csv_path, index=False)
    payload = {
        "status": "completed",
        "config": {
            "seeds": list(cfg.seeds),
            "train_case_count": cfg.train_case_count,
            "eval_case_count": cfg.eval_case_count,
            "robust_variants": [[q if q is not None else "inf", s] for q, s in cfg.robust_variants],
        },
        "training_mix_counts": mix_counts,
        "comparison_rows": compare.to_dict(orient="records"),
        "metrics_csv": str(metrics_path),
        "compare_csv": str(compare_csv_path),
        "summary_json": str(summary_path),
    }
    summary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
