#!/usr/bin/env python3
"""First executable tolerance package on the mixed-train public-natural regime."""

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
from run_real_pipeline import forward_diffractive
from run_unified_comparison_ci import build_spectral_features


@dataclass
class ToleranceConfig:
    seeds: tuple[int, ...] = (0, 1, 2)
    train_case_count: int = 24
    eval_case_count: int = 6


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def tolerance_root() -> Path:
    return project_root() / "results" / "tolerance"


def confidence_interval_95(values: np.ndarray) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    if len(values) == 0:
        return 0.0, 0.0
    if len(values) == 1:
        return float(values[0]), 0.0
    std = values.std(ddof=1)
    return float(values.mean()), float(1.96 * std / np.sqrt(len(values)))


def shift_array(arr: np.ndarray, shift_x: int, shift_y: int) -> np.ndarray:
    shifted = np.roll(arr, shift=(shift_y, shift_x), axis=(0, 1))
    if shift_y > 0:
        shifted[:shift_y, :] = 0.0
    elif shift_y < 0:
        shifted[shift_y:, :] = 0.0
    if shift_x > 0:
        shifted[:, :shift_x] = 0.0
    elif shift_x < 0:
        shifted[:, shift_x:] = 0.0
    return shifted


def apply_common_tolerance(
    samples: list[dict[str, object]],
    *,
    misregistration_px: float = 0.0,
    reference_noise_sigma: float = 0.0,
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    int_shift = int(round(misregistration_px))
    rng = np.random.default_rng(100 + int_shift + int(reference_noise_sigma * 1000))
    for sample in samples:
        copied = dict(sample)
        ref = np.asarray(sample["reference_lowres"], dtype=np.float64).copy()
        if int_shift != 0:
            ref = shift_array(ref, int_shift, int_shift)
        if reference_noise_sigma > 0.0:
            ref = np.clip(ref + rng.normal(0.0, reference_noise_sigma, ref.shape), 0.0, 1.0)
        copied["reference_lowres"] = ref
        out.append(copied)
    return out


def quantize_masks(masks: np.ndarray, bits: int | None) -> np.ndarray:
    if bits is None:
        return masks.copy()
    phase = np.angle(masks)
    levels = 2**bits
    quantized = np.round((phase + np.pi) / (2 * np.pi) * (levels - 1)) / (levels - 1)
    quantized_phase = quantized * 2 * np.pi - np.pi
    return np.exp(1j * quantized_phase)


def shift_masks(masks: np.ndarray, pixels: int) -> np.ndarray:
    if pixels == 0:
        return masks.copy()
    shifted = []
    for mask in masks:
        shifted_mask = np.roll(mask, shift=(pixels, pixels), axis=(0, 1))
        if pixels > 0:
            shifted_mask[:pixels, :] = 1.0 + 0.0j
            shifted_mask[:, :pixels] = 1.0 + 0.0j
        shifted.append(shifted_mask)
    return np.asarray(shifted)


def train_models(seed: int, train_samples: list[dict[str, object]]) -> dict[str, object]:
    config = PhaseOnlyConfig(seed=seed, train_case_count=24, heldout_case_count=6)
    basis = make_phase_basis(config.lowres_size, config.phase_basis_count)
    frontend_spacing = config.sample_spacing * config.image_size / config.lowres_size
    propagation = PropagationConfig(
        grid_size=config.lowres_size,
        sample_spacing=frontend_spacing,
        wavelength=config.wavelength,
        propagation_distance=config.propagation_distance,
    )
    coeffs = optimize_phase_coeffs(config, basis, train_samples, propagation)
    masks = phase_masks_from_coeffs(coeffs, basis)
    x_train = build_features(train_samples, masks, propagation)
    y_train = build_targets(train_samples)
    phase_weights = fit_ridge_regression(x_train, y_train, config.ridge_lambda)

    ridge_train = np.asarray(
        [
            np.concatenate([sample["noisy_lowres"].reshape(-1), sample["reference_lowres"].reshape(-1)])
            for sample in train_samples
        ],
        dtype=np.float64,
    )
    surrogate_weights = fit_ridge_regression(ridge_train, y_train, config.ridge_lambda)

    spectral_train = build_spectral_features(train_samples, spectral_crop_size=6)
    spectral_weights = fit_ridge_regression(spectral_train, y_train, config.ridge_lambda)

    return {
        "config": config,
        "propagation": propagation,
        "masks": masks,
        "phase_weights": phase_weights,
        "surrogate_weights": surrogate_weights,
        "spectral_weights": spectral_weights,
    }


def evaluate_methods(
    eval_samples: list[dict[str, object]],
    trained: dict[str, object],
    *,
    quant_bits: int | None = None,
    mask_shift_px: int = 0,
    include_surrogate: bool = True,
    include_reference: bool = True,
    include_spectral: bool = True,
) -> pd.DataFrame:
    config: PhaseOnlyConfig = trained["config"]
    masks = shift_masks(quantize_masks(trained["masks"], quant_bits), mask_shift_px)
    phase_features = build_features(eval_samples, masks, trained["propagation"])
    phase_pred = predict_ridge(phase_features, trained["phase_weights"])

    surrogate_x = np.asarray(
        [
            np.concatenate([sample["noisy_lowres"].reshape(-1), sample["reference_lowres"].reshape(-1)])
            for sample in eval_samples
        ],
        dtype=np.float64,
    )
    surrogate_pred = predict_ridge(surrogate_x, trained["surrogate_weights"])
    spectral_x = build_spectral_features(eval_samples, spectral_crop_size=6)
    spectral_pred = predict_ridge(spectral_x, trained["spectral_weights"])

    rows: list[dict[str, object]] = []
    method_predictions = {"phase_only_stack": phase_pred}
    if include_surrogate:
        method_predictions["trainable_surrogate_ridge"] = surrogate_pred
    if include_spectral:
        method_predictions["spectral_frontend"] = spectral_pred
    for method_name, pred_array in method_predictions.items():
        for idx, sample in enumerate(eval_samples):
            pred = pred_array[idx].reshape(config.lowres_size, config.lowres_size)
            rows.append(
                {
                    "method": method_name,
                    "object_id": str(sample["object_id"]),
                    "fixed_psnr_lowres": float(sample["fixed_psnr_lowres"]),
                    "guided_psnr_lowres": float(sample["guided_psnr_lowres"]),
                    "method_psnr_lowres": float(psnr(sample["gt_lowres"], pred)),
                }
            )
    if include_reference:
        for sample in eval_samples:
            rows.append(
                {
                    "method": "reference_psf_deconvolution",
                    "object_id": str(sample["object_id"]),
                    "fixed_psnr_lowres": float(sample["fixed_psnr_lowres"]),
                    "guided_psnr_lowres": float(sample["guided_psnr_lowres"]),
                    "method_psnr_lowres": float(sample["guided_psnr_lowres"]),
                }
            )
    df = pd.DataFrame(rows)
    df["psnr_gain_over_fixed_lowres"] = df["method_psnr_lowres"] - df["fixed_psnr_lowres"]
    return df


def build_propagation_perturbed_eval_samples(
    objects: list[np.ndarray],
    eval_cases: list[dict[str, float]],
    base_config: PhaseOnlyConfig,
    distance_fraction: float,
) -> list[dict[str, object]]:
    perturbed = PhaseOnlyConfig(
        image_size=base_config.image_size,
        pupil_size=base_config.pupil_size,
        lowres_size=base_config.lowres_size,
        layer_count=base_config.layer_count,
        phase_basis_count=base_config.phase_basis_count,
        seed=base_config.seed,
        train_case_count=base_config.train_case_count,
        heldout_case_count=base_config.heldout_case_count,
        ridge_lambda=base_config.ridge_lambda,
        search_steps=base_config.search_steps,
        proposal_scale=base_config.proposal_scale,
        wavelength=base_config.wavelength,
        sample_spacing=base_config.sample_spacing,
        propagation_distance=base_config.propagation_distance * (1.0 + distance_fraction),
        noise_sigma=base_config.noise_sigma,
        nominal_wiener_k=base_config.nominal_wiener_k,
        guided_wiener_k=base_config.guided_wiener_k,
        propagation_model=base_config.propagation_model,
    )
    return build_split_samples(objects, "natural_object_eval", eval_cases, perturbed)


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby(["perturbation_family", "level", "dataset_name", "method"], as_index=False)
        .agg(
            mean_psnr_gain_over_fixed_lowres=("psnr_gain_over_fixed_lowres", "mean"),
            better_than_fixed_fraction=("psnr_gain_over_fixed_lowres", lambda s: float((s > 0.0).mean())),
        )
    )


def build_tolerance_detail(metrics: pd.DataFrame) -> pd.DataFrame:
    return (
        metrics.groupby(
            ["perturbation_family", "level", "dataset_name", "dataset_version", "method", "seed"],
            as_index=False,
        )
        .agg(
            sample_count=("psnr_gain_over_fixed_lowres", "size"),
            mean_psnr_gain_over_fixed_lowres=("psnr_gain_over_fixed_lowres", "mean"),
            std_psnr_gain_over_fixed_lowres=("psnr_gain_over_fixed_lowres", lambda s: float(s.std(ddof=1)) if len(s) > 1 else 0.0),
            better_than_fixed_fraction=("psnr_gain_over_fixed_lowres", lambda s: float((s > 0.0).mean())),
            mean_method_psnr_lowres=("method_psnr_lowres", "mean"),
            mean_fixed_psnr_lowres=("fixed_psnr_lowres", "mean"),
            mean_guided_psnr_lowres=("guided_psnr_lowres", "mean"),
        )
    )


def build_tolerance_summary(detail: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    grouped = detail.groupby(["perturbation_family", "level", "dataset_name", "dataset_version", "method"])
    for key, group in grouped:
        gains = group["mean_psnr_gain_over_fixed_lowres"].to_numpy(dtype=float)
        mean_gain, ci95 = confidence_interval_95(gains)
        rows.append(
            {
                "perturbation_family": key[0],
                "level": key[1],
                "dataset_name": key[2],
                "dataset_version": key[3],
                "method": key[4],
                "seed_count": int(len(group)),
                "sample_count_per_seed": int(group["sample_count"].iloc[0]),
                "mean_psnr_gain_over_fixed_lowres": mean_gain,
                "std_psnr_gain_over_fixed_lowres": float(gains.std(ddof=1)) if len(gains) > 1 else 0.0,
                "ci95_half_width": ci95,
                "ci_low": mean_gain - ci95,
                "ci_high": mean_gain + ci95,
                "mean_better_than_fixed_fraction": float(group["better_than_fixed_fraction"].mean()),
                "mean_method_psnr_lowres": float(group["mean_method_psnr_lowres"].mean()),
                "mean_fixed_psnr_lowres": float(group["mean_fixed_psnr_lowres"].mean()),
                "mean_guided_psnr_lowres": float(group["mean_guided_psnr_lowres"].mean()),
            }
        )
    return pd.DataFrame(rows)


def build_tolerance_plot_manifest(summary: pd.DataFrame, detail_path: Path, summary_path: Path) -> pd.DataFrame:
    family_order = [
        "reference_channel_misregistration",
        "reference_channel_intensity_noise",
        "propagation_distance_error",
        "phase_mask_quantization",
        "phase_mask_lateral_shift",
    ]
    fairness_class = {
        "reference_channel_misregistration": "common_input",
        "reference_channel_intensity_noise": "common_input",
        "propagation_distance_error": "common_input",
        "phase_mask_quantization": "phase_mask_only",
        "phase_mask_lateral_shift": "phase_mask_only",
    }
    rows: list[dict[str, object]] = []
    for family in family_order:
        family_df = summary.loc[summary["perturbation_family"] == family]
        if family_df.empty:
            continue
        methods = sorted(family_df["method"].unique().tolist())
        datasets = sorted(family_df["dataset_name"].unique().tolist())
        rows.append(
            {
                "panel_id": family,
                "perturbation_family": family,
                "fairness_class": fairness_class[family],
                "summary_file": str(summary_path),
                "detail_file": str(detail_path),
                "x_column": "level",
                "y_column": "mean_psnr_gain_over_fixed_lowres",
                "ci_column": "ci95_half_width",
                "methods": "|".join(methods),
                "datasets": "|".join(datasets),
            }
        )
    return pd.DataFrame(rows)


def build_hardware_tolerance_metrics(summary: pd.DataFrame, out_dir: Path) -> pd.DataFrame:
    hardware_df = summary.copy()
    hardware_df["model_variant"] = "standard_phase_only_training"
    hardware_df["evidence_scope"] = np.where(
        hardware_df["perturbation_family"].isin(
            [
                "reference_channel_misregistration",
                "reference_channel_intensity_noise",
                "propagation_distance_error",
            ]
        ),
        "common_input_public_natural_tolerance",
        "phase_mask_engineering_public_natural_tolerance",
    )

    robust_metrics_path = out_dir / "robust_mask_tolerance_metrics.csv"
    if robust_metrics_path.exists():
        robust = pd.read_csv(robust_metrics_path)
        robust_detail = (
            robust.groupby(
                ["perturbation_family", "level", "dataset_name", "dataset_version", "seed"],
                as_index=False,
            )
            .agg(
                sample_count=("psnr_gain_over_fixed_lowres", "size"),
                mean_psnr_gain_over_fixed_lowres=("psnr_gain_over_fixed_lowres", "mean"),
                better_than_fixed_fraction=("psnr_gain_over_fixed_lowres", lambda s: float((s > 0.0).mean())),
                mean_method_psnr_lowres=("robust_method_psnr_lowres", "mean"),
                mean_fixed_psnr_lowres=("fixed_psnr_lowres", "mean"),
            )
        )
        robust_rows: list[dict[str, object]] = []
        grouped = robust_detail.groupby(["perturbation_family", "level", "dataset_name", "dataset_version"])
        for key, group in grouped:
            gains = group["mean_psnr_gain_over_fixed_lowres"].to_numpy(dtype=float)
            mean_gain, ci95 = confidence_interval_95(gains)
            robust_rows.append(
                {
                    "perturbation_family": key[0],
                    "level": key[1],
                    "dataset_name": key[2],
                    "dataset_version": key[3],
                    "method": "robust_phase_only_stack",
                    "seed_count": int(len(group)),
                    "sample_count_per_seed": int(group["sample_count"].iloc[0]),
                    "mean_psnr_gain_over_fixed_lowres": mean_gain,
                    "std_psnr_gain_over_fixed_lowres": float(gains.std(ddof=1)) if len(gains) > 1 else 0.0,
                    "ci95_half_width": ci95,
                    "ci_low": mean_gain - ci95,
                    "ci_high": mean_gain + ci95,
                    "mean_better_than_fixed_fraction": float(group["better_than_fixed_fraction"].mean()),
                    "mean_method_psnr_lowres": float(group["mean_method_psnr_lowres"].mean()),
                    "mean_fixed_psnr_lowres": float(group["mean_fixed_psnr_lowres"].mean()),
                    "mean_guided_psnr_lowres": np.nan,
                    "model_variant": "robust_mask_training",
                    "evidence_scope": "phase_mask_engineering_public_natural_tolerance",
                }
            )
        if robust_rows:
            hardware_df = pd.concat([hardware_df, pd.DataFrame(robust_rows)], ignore_index=True)

    return hardware_df


def write_tolerance_exports(metrics: pd.DataFrame, out_dir: Path) -> dict[str, str]:
    detail = build_tolerance_detail(metrics)
    summary = build_tolerance_summary(detail)
    detail_path = out_dir / "tolerance_curve_detail.csv"
    summary_path = out_dir / "tolerance_curve_summary.csv"
    plot_manifest_path = out_dir / "tolerance_plot_manifest.csv"
    hardware_metrics_path = out_dir / "hardware_tolerance_metrics.csv"

    detail.to_csv(detail_path, index=False)
    summary.to_csv(summary_path, index=False)
    build_tolerance_plot_manifest(summary, detail_path, summary_path).to_csv(plot_manifest_path, index=False)
    build_hardware_tolerance_metrics(summary, out_dir).to_csv(hardware_metrics_path, index=False)

    return {
        "tolerance_curve_detail_csv": str(detail_path),
        "tolerance_curve_summary_csv": str(summary_path),
        "tolerance_plot_manifest_csv": str(plot_manifest_path),
        "hardware_tolerance_metrics_csv": str(hardware_metrics_path),
    }


def main() -> int:
    cfg = ToleranceConfig()
    mixed_train_objects, mix_counts = build_mixed_training_objects()
    all_rows: list[pd.DataFrame] = []

    common_tolerances = [
        ("reference_channel_misregistration", 0.0, {"misregistration_px": 0.0, "reference_noise_sigma": 0.0}),
        ("reference_channel_misregistration", 1.0, {"misregistration_px": 1.0, "reference_noise_sigma": 0.0}),
        ("reference_channel_intensity_noise", 0.01, {"misregistration_px": 0.0, "reference_noise_sigma": 0.01}),
        ("reference_channel_intensity_noise", 0.02, {"misregistration_px": 0.0, "reference_noise_sigma": 0.02}),
    ]
    propagation_distance_tolerances = [
        ("propagation_distance_error", -0.05),
        ("propagation_distance_error", 0.0),
        ("propagation_distance_error", 0.05),
    ]
    phase_only_engineering = [
        ("phase_mask_quantization", 3, {"quant_bits": 3, "mask_shift_px": 0}),
        ("phase_mask_quantization", 4, {"quant_bits": 4, "mask_shift_px": 0}),
        ("phase_mask_lateral_shift", 1, {"quant_bits": None, "mask_shift_px": 1}),
        ("phase_mask_lateral_shift", 2, {"quant_bits": None, "mask_shift_px": 2}),
    ]

    for seed in cfg.seeds:
        phase_config = PhaseOnlyConfig(seed=seed, train_case_count=cfg.train_case_count, heldout_case_count=cfg.eval_case_count)
        train_cases = make_aberration_cases(cfg.train_case_count, seed)
        train_samples = build_split_samples(mixed_train_objects, "train", train_cases, phase_config)
        trained = train_models(seed, train_samples)
        eval_cases = make_aberration_cases(cfg.eval_case_count, seed + 500)

        for spec in load_subset_index():
            objects = [arr for _, arr in load_grayscale_objects(staging_root() / dataset_dir_name(spec))]
            eval_samples_base = build_split_samples(objects, "natural_object_eval", eval_cases, phase_config)

            for perturbation_family, level, kwargs in common_tolerances:
                perturbed_samples = apply_common_tolerance(eval_samples_base, **kwargs)
                df = evaluate_methods(perturbed_samples, trained)
                df["seed"] = seed
                df["dataset_name"] = spec.dataset_name
                df["dataset_version"] = spec.dataset_version
                df["perturbation_family"] = perturbation_family
                df["level"] = level
                df["training_regime"] = "mixed_train_tolerance"
                all_rows.append(df)

            for perturbation_family, level in propagation_distance_tolerances:
                eval_samples_prop = build_propagation_perturbed_eval_samples(objects, eval_cases, phase_config, level)
                df = evaluate_methods(
                    eval_samples_prop,
                    trained,
                    include_surrogate=False,
                    include_reference=True,
                    include_spectral=True,
                )
                df["seed"] = seed
                df["dataset_name"] = spec.dataset_name
                df["dataset_version"] = spec.dataset_version
                df["perturbation_family"] = perturbation_family
                df["level"] = level
                df["training_regime"] = "mixed_train_tolerance"
                all_rows.append(df)

            for perturbation_family, level, kwargs in phase_only_engineering:
                df = evaluate_methods(eval_samples_base, trained, **kwargs)
                df = df.loc[df["method"] == "phase_only_stack"].reset_index(drop=True)
                df["seed"] = seed
                df["dataset_name"] = spec.dataset_name
                df["dataset_version"] = spec.dataset_version
                df["perturbation_family"] = perturbation_family
                df["level"] = level
                df["training_regime"] = "mixed_train_tolerance"
                all_rows.append(df)

    metrics = pd.concat(all_rows, ignore_index=True)
    summary_df = summarize(metrics)
    out_dir = tolerance_root()
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = out_dir / "mixed_train_tolerance_metrics.csv"
    summary_path = out_dir / "mixed_train_tolerance_summary.json"
    metrics.to_csv(metrics_path, index=False)
    export_paths = write_tolerance_exports(metrics, out_dir)
    payload = {
        "status": "completed",
        "config": {
            "seeds": list(cfg.seeds),
            "train_case_count": cfg.train_case_count,
            "eval_case_count": cfg.eval_case_count,
        },
        "training_mix_counts": mix_counts,
        "summary_rows": summary_df.to_dict(orient="records"),
        "metrics_csv": str(metrics_path),
        "summary_json": str(summary_path),
        **export_paths,
    }
    summary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
