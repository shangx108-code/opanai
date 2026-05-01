#!/usr/bin/env python3
"""Second-generation joint-perturbation training and evaluation package.

This script upgrades the first-order robust-mask strategy by injecting linked
phase-noise, misalignment, and wavelength-drift variants into the training
objective itself, then evaluating the trained model on the same linked
fabrication-style tolerance grid used by the earlier scans.
"""

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
    phase_masks_from_coeffs,
    predict_ridge,
)
from run_baseline_reference_psf import psnr
from run_joint_fabrication_tolerance import (
    JointToleranceConfig,
    apply_joint_mask_perturbation,
    build_axis_tolerance_curves,
    build_failure_boundary,
    build_seed_detail,
    build_summary_markdown,
    build_wavelength_shifted_eval_samples,
    shifted_propagation,
    summarize_joint_grid,
    wavelength_shifted_config,
)
from run_mixed_train_natural_object_rerun import build_mixed_training_objects
from run_natural_object_evaluation import (
    dataset_dir_name,
    load_grayscale_objects,
    load_subset_index,
    staging_root,
)


@dataclass(frozen=True)
class JointTrainVariant:
    label: str
    phase_noise_sigma_rad: float
    shift_sigma_px: float
    rotation_sigma_deg: float
    wavelength_drift_fraction: float


@dataclass(frozen=True)
class SecondGenConfig:
    joint_eval: JointToleranceConfig = JointToleranceConfig()
    train_variants: tuple[JointTrainVariant, ...] = (
        JointTrainVariant("clean", 0.0, 0.0, 0.0, 0.0),
        JointTrainVariant("joint_mild", 0.05, 0.25, 0.50, 0.005),
        JointTrainVariant("joint_moderate", 0.10, 0.50, 1.00, 0.010),
    )
    train_search_steps: int = 3


@dataclass(frozen=True)
class TrainingVariantContext:
    variant: JointTrainVariant
    variant_index: int
    samples: list[dict[str, object]]
    propagation: PropagationConfig
    targets: np.ndarray


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def result_root() -> Path:
    return project_root() / "results" / "tolerance_joint_secondgen"


def deterministic_rng(seed: int, variant_index: int) -> np.random.Generator:
    return np.random.default_rng(3000003 * (seed + 1) + 1009 * variant_index)


def secondgen_phase_config(seed: int, base: JointToleranceConfig, search_steps: int) -> PhaseOnlyConfig:
    return PhaseOnlyConfig(
        seed=seed,
        train_case_count=base.train_case_count,
        heldout_case_count=base.eval_case_count,
        search_steps=search_steps,
    )


def build_training_variant_block(
    phase_config: PhaseOnlyConfig,
    base_masks: np.ndarray,
    context: TrainingVariantContext,
) -> tuple[np.ndarray, np.ndarray]:
    rng = deterministic_rng(phase_config.seed, context.variant_index)
    perturbed_masks = apply_joint_mask_perturbation(
        base_masks,
        phase_noise_sigma_rad=context.variant.phase_noise_sigma_rad,
        shift_sigma_px=context.variant.shift_sigma_px,
        rotation_sigma_deg=context.variant.rotation_sigma_deg,
        rng=rng,
    )
    return (
        build_features(context.samples, perturbed_masks, context.propagation),
        context.targets,
    )


def build_joint_training_matrix(
    coeffs: np.ndarray,
    basis: np.ndarray,
    phase_config: PhaseOnlyConfig,
    variant_contexts: tuple[TrainingVariantContext, ...],
) -> tuple[np.ndarray, np.ndarray]:
    base_masks = phase_masks_from_coeffs(coeffs, basis)
    x_blocks = []
    y_blocks = []
    for context in variant_contexts:
        x_block, y_block = build_training_variant_block(
            phase_config,
            base_masks,
            context,
        )
        x_blocks.append(x_block)
        y_blocks.append(y_block)
    return np.concatenate(x_blocks, axis=0), np.concatenate(y_blocks, axis=0)


def secondgen_training_objective(
    coeffs: np.ndarray,
    basis: np.ndarray,
    phase_config: PhaseOnlyConfig,
    variant_contexts: tuple[TrainingVariantContext, ...],
) -> float:
    x_train, y_train = build_joint_training_matrix(
        coeffs,
        basis,
        phase_config,
        variant_contexts,
    )
    weights = fit_ridge_regression(x_train, y_train, phase_config.ridge_lambda)
    pred = predict_ridge(x_train, weights)
    return float(np.mean((pred - y_train) ** 2))


def optimize_phase_coeffs_secondgen(
    phase_config: PhaseOnlyConfig,
    basis: np.ndarray,
    variant_contexts: tuple[TrainingVariantContext, ...],
) -> np.ndarray:
    rng = np.random.default_rng(phase_config.seed)
    coeffs = rng.normal(0.0, 0.12, size=(phase_config.layer_count, phase_config.phase_basis_count))
    best_loss = secondgen_training_objective(
        coeffs,
        basis,
        phase_config,
        variant_contexts,
    )
    step = phase_config.proposal_scale
    for _ in range(phase_config.search_steps):
        direction = rng.normal(0.0, 1.0, size=coeffs.shape)
        for candidate in (coeffs + step * direction, coeffs - step * direction):
            loss = secondgen_training_objective(
                candidate,
                basis,
                phase_config,
                variant_contexts,
            )
            if loss < best_loss:
                coeffs = candidate
                best_loss = loss
        step *= 0.88
    return coeffs


def train_secondgen_phase_model(
    seed: int,
    train_objects: list[np.ndarray],
    train_cases: list[dict[str, float]],
    cfg: SecondGenConfig,
) -> dict[str, object]:
    phase_config = secondgen_phase_config(seed, cfg.joint_eval, cfg.train_search_steps)
    basis = make_phase_basis(phase_config.lowres_size, phase_config.phase_basis_count)
    variant_contexts = []
    for variant_index, variant in enumerate(cfg.train_variants):
        variant_config = wavelength_shifted_config(phase_config, variant.wavelength_drift_fraction)
        samples = build_split_samples(train_objects, "train", train_cases, variant_config)
        variant_contexts.append(
            TrainingVariantContext(
                variant=variant,
                variant_index=variant_index,
                samples=samples,
                propagation=shifted_propagation(phase_config, variant.wavelength_drift_fraction),
                targets=build_targets(samples),
            )
        )
    variant_contexts = tuple(variant_contexts)
    coeffs = optimize_phase_coeffs_secondgen(
        phase_config,
        basis,
        variant_contexts,
    )
    x_train, y_train = build_joint_training_matrix(
        coeffs,
        basis,
        phase_config,
        variant_contexts,
    )
    weights = fit_ridge_regression(x_train, y_train, phase_config.ridge_lambda)
    return {
        "config": phase_config,
        "basis": basis,
        "masks": phase_masks_from_coeffs(coeffs, basis),
        "weights": weights,
    }


def evaluate_secondgen_phase_only_stack(
    eval_samples: list[dict[str, object]],
    *,
    masks: np.ndarray,
    propagation: PropagationConfig,
    weights: np.ndarray,
    lowres_size: int,
) -> pd.DataFrame:
    features = build_features(eval_samples, masks, propagation)
    prediction = predict_ridge(features, weights)
    rows: list[dict[str, object]] = []
    for idx, sample in enumerate(eval_samples):
        pred = prediction[idx].reshape(lowres_size, lowres_size)
        method_psnr = float(psnr(sample["gt_lowres"], pred))
        rows.append(
            {
                "object_id": str(sample["object_id"]),
                "case_id": int(sample["case_id"]),
                "fixed_psnr_lowres": float(sample["fixed_psnr_lowres"]),
                "guided_psnr_lowres": float(sample["guided_psnr_lowres"]),
                "method_psnr_lowres": method_psnr,
                "psnr_gain_over_fixed_lowres": method_psnr - float(sample["fixed_psnr_lowres"]),
            }
        )
    return pd.DataFrame(rows)


def build_boundary_comparison(
    secondgen_summary: pd.DataFrame,
    baseline_path: Path,
    robust_path: Path,
    *,
    failure_threshold_gain_db: float,
) -> pd.DataFrame:
    secondgen_boundary = build_failure_boundary(secondgen_summary, failure_threshold_gain_db)
    baseline = pd.read_csv(baseline_path).rename(
        columns={
            "max_passing_wavelength_drift_fraction": "baseline_max_passing_wavelength_drift_fraction",
            "clean_point_gain_db": "baseline_clean_point_gain_db",
            "clean_point_state": "baseline_clean_point_state",
        }
    )
    robust = pd.read_csv(robust_path).rename(
        columns={
            "max_passing_wavelength_drift_fraction": "robust_max_passing_wavelength_drift_fraction",
            "clean_point_gain_db": "robust_clean_point_gain_db",
            "clean_point_state": "robust_clean_point_state",
        }
    )
    merged = secondgen_boundary.merge(
        baseline[
            [
                "dataset_name",
                "dataset_version",
                "phase_noise_sigma_rad",
                "misalignment_label",
                "shift_sigma_px",
                "rotation_sigma_deg",
                "failure_threshold_gain_db",
                "baseline_max_passing_wavelength_drift_fraction",
                "baseline_clean_point_gain_db",
                "baseline_clean_point_state",
            ]
        ],
        on=[
            "dataset_name",
            "dataset_version",
            "phase_noise_sigma_rad",
            "misalignment_label",
            "shift_sigma_px",
            "rotation_sigma_deg",
            "failure_threshold_gain_db",
        ],
        how="left",
    ).merge(
        robust[
            [
                "dataset_name",
                "dataset_version",
                "phase_noise_sigma_rad",
                "misalignment_label",
                "shift_sigma_px",
                "rotation_sigma_deg",
                "failure_threshold_gain_db",
                "robust_max_passing_wavelength_drift_fraction",
                "robust_clean_point_gain_db",
                "robust_clean_point_state",
            ]
        ],
        on=[
            "dataset_name",
            "dataset_version",
            "phase_noise_sigma_rad",
            "misalignment_label",
            "shift_sigma_px",
            "rotation_sigma_deg",
            "failure_threshold_gain_db",
        ],
        how="left",
    )
    merged["clean_point_gain_delta_vs_unmitigated_db"] = (
        merged["clean_point_gain_db"] - merged["baseline_clean_point_gain_db"]
    )
    merged["clean_point_gain_delta_vs_robustmask_db"] = (
        merged["clean_point_gain_db"] - merged["robust_clean_point_gain_db"]
    )
    return merged


def main() -> int:
    cfg = SecondGenConfig()
    out_dir = result_root()
    out_dir.mkdir(parents=True, exist_ok=True)

    mixed_train_objects, mix_counts = build_mixed_training_objects()
    all_rows: list[pd.DataFrame] = []

    for seed in cfg.joint_eval.seeds:
        train_cases = make_aberration_cases(cfg.joint_eval.train_case_count, seed)
        trained = train_secondgen_phase_model(seed, mixed_train_objects, train_cases, cfg)
        eval_cases = make_aberration_cases(cfg.joint_eval.eval_case_count, seed + 500)

        for spec in load_subset_index():
            objects = [arr for _, arr in load_grayscale_objects(staging_root() / dataset_dir_name(spec))]
            eval_cache = {
                drift: build_wavelength_shifted_eval_samples(objects, eval_cases, trained["config"], drift)
                for drift in cfg.joint_eval.wavelength_drift_fraction_levels
            }
            for phase_noise_sigma_rad in cfg.joint_eval.phase_noise_sigma_rad_levels:
                for misalignment in cfg.joint_eval.misalignment_levels:
                    repeat_count = 1
                    if phase_noise_sigma_rad > 0.0 or misalignment.shift_sigma_px > 0.0 or misalignment.rotation_sigma_deg > 0.0:
                        repeat_count = cfg.joint_eval.monte_carlo_repeats
                    for wavelength_drift_fraction in cfg.joint_eval.wavelength_drift_fraction_levels:
                        propagation = shifted_propagation(trained["config"], wavelength_drift_fraction)
                        eval_samples = eval_cache[wavelength_drift_fraction]
                        for repeat in range(repeat_count):
                            rng = np.random.default_rng(
                                4000003 * (seed + 1)
                                + 10007 * int(round(phase_noise_sigma_rad * 1000))
                                + 101 * int(round(misalignment.shift_sigma_px * 100))
                                + 1009 * int(round(misalignment.rotation_sigma_deg * 100))
                                + 17 * int(round(wavelength_drift_fraction * 10000))
                                + repeat
                            )
                            masks = apply_joint_mask_perturbation(
                                trained["masks"],
                                phase_noise_sigma_rad=phase_noise_sigma_rad,
                                shift_sigma_px=misalignment.shift_sigma_px,
                                rotation_sigma_deg=misalignment.rotation_sigma_deg,
                                rng=rng,
                            )
                            df = evaluate_secondgen_phase_only_stack(
                                eval_samples,
                                masks=masks,
                                propagation=propagation,
                                weights=trained["weights"],
                                lowres_size=trained["config"].lowres_size,
                            )
                            df["seed"] = seed
                            df["repeat"] = repeat
                            df["dataset_name"] = spec.dataset_name
                            df["dataset_version"] = spec.dataset_version
                            df["phase_noise_sigma_rad"] = phase_noise_sigma_rad
                            df["misalignment_label"] = misalignment.label
                            df["shift_sigma_px"] = misalignment.shift_sigma_px
                            df["rotation_sigma_deg"] = misalignment.rotation_sigma_deg
                            df["wavelength_drift_fraction"] = wavelength_drift_fraction
                            all_rows.append(df)

    metrics = pd.concat(all_rows, ignore_index=True)
    seed_detail = build_seed_detail(metrics)
    summary = summarize_joint_grid(seed_detail, cfg.joint_eval.failure_threshold_gain_db)
    boundary = build_failure_boundary(summary, cfg.joint_eval.failure_threshold_gain_db)
    axis_curves = build_axis_tolerance_curves(summary)
    comparison = build_boundary_comparison(
        summary,
        project_root() / "results" / "tolerance_joint" / "failure_boundary.csv",
        project_root() / "results" / "tolerance_joint_robust" / "failure_boundary.csv",
        failure_threshold_gain_db=cfg.joint_eval.failure_threshold_gain_db,
    )

    metrics_path = out_dir / "joint_tolerance_metrics.csv"
    seed_detail_path = out_dir / "joint_tolerance_seed_detail.csv"
    summary_path = out_dir / "joint_tolerance_curve.csv"
    degradation_path = out_dir / "degradation_ci.csv"
    boundary_path = out_dir / "failure_boundary.csv"
    axis_curve_path = out_dir / "axis_tolerance_curves.csv"
    comparison_path = out_dir / "boundary_comparison.csv"
    payload_path = out_dir / "joint_tolerance_summary.json"
    markdown_path = out_dir / "joint_tolerance_summary.md"

    metrics.to_csv(metrics_path, index=False)
    seed_detail.to_csv(seed_detail_path, index=False)
    summary.to_csv(summary_path, index=False)
    summary[
        [
            "dataset_name",
            "dataset_version",
            "phase_noise_sigma_rad",
            "misalignment_label",
            "shift_sigma_px",
            "rotation_sigma_deg",
            "wavelength_drift_fraction",
            "mean_degradation_vs_clean_db",
            "degradation_ci95_half_width",
            "degradation_ci_low",
            "degradation_ci_high",
            "mean_psnr_gain_over_fixed_lowres",
            "gain_ci95_half_width",
            "pass_state",
        ]
    ].to_csv(degradation_path, index=False)
    boundary.to_csv(boundary_path, index=False)
    axis_curves.to_csv(axis_curve_path, index=False)
    comparison.to_csv(comparison_path, index=False)

    payload = {
        "status": "completed",
        "seeds": list(cfg.joint_eval.seeds),
        "train_case_count": cfg.joint_eval.train_case_count,
        "eval_case_count": cfg.joint_eval.eval_case_count,
        "monte_carlo_repeats": cfg.joint_eval.monte_carlo_repeats,
        "train_search_steps": cfg.train_search_steps,
        "train_variants": [
            {
                "label": variant.label,
                "phase_noise_sigma_rad": variant.phase_noise_sigma_rad,
                "shift_sigma_px": variant.shift_sigma_px,
                "rotation_sigma_deg": variant.rotation_sigma_deg,
                "wavelength_drift_fraction": variant.wavelength_drift_fraction,
            }
            for variant in cfg.train_variants
        ],
        "training_mix_counts": mix_counts,
        "failure_threshold_gain_db": cfg.joint_eval.failure_threshold_gain_db,
        "output_files": {
            "joint_tolerance_metrics_csv": str(metrics_path),
            "joint_tolerance_seed_detail_csv": str(seed_detail_path),
            "joint_tolerance_curve_csv": str(summary_path),
            "degradation_ci_csv": str(degradation_path),
            "failure_boundary_csv": str(boundary_path),
            "axis_tolerance_curves_csv": str(axis_curve_path),
            "boundary_comparison_csv": str(comparison_path),
            "summary_md": str(markdown_path),
        },
    }
    payload_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(build_summary_markdown(summary, boundary, cfg.joint_eval), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
