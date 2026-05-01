#!/usr/bin/env python3
"""Robust-mask version of the linked fabrication-tolerance scan."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from run_baseline_phase_only_megadiverse_train_dual_heldout_thickstats import (
    PhaseOnlyConfig,
    build_features,
    build_split_samples,
    make_aberration_cases,
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
)
from run_mixed_train_natural_object_rerun import build_mixed_training_objects
from run_natural_object_evaluation import (
    dataset_dir_name,
    load_grayscale_objects,
    load_subset_index,
    staging_root,
)
from run_robust_mask_tolerance_compare import train_robust_phase_model


@dataclass(frozen=True)
class RobustTrainShim:
    train_case_count: int
    eval_case_count: int
    robust_variants: tuple[tuple[int | None, int], ...] = (
        (None, 0),
        (4, 0),
        (3, 0),
        (None, 1),
    )


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def result_root() -> Path:
    return project_root() / "results" / "tolerance_joint_robust"


def evaluate_robust_phase_only_stack(
    eval_samples: list[dict[str, object]],
    *,
    masks: np.ndarray,
    propagation,
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


def build_boundary_expansion(
    robust_summary: pd.DataFrame,
    baseline_boundary_path: Path,
    *,
    failure_threshold_gain_db: float,
) -> pd.DataFrame:
    baseline = pd.read_csv(baseline_boundary_path)
    baseline = baseline.rename(
        columns={
            "max_passing_wavelength_drift_fraction": "baseline_max_passing_wavelength_drift_fraction",
            "first_mean_fail_wavelength_drift_fraction": "baseline_first_mean_fail_wavelength_drift_fraction",
            "first_certain_fail_wavelength_drift_fraction": "baseline_first_certain_fail_wavelength_drift_fraction",
            "clean_point_gain_db": "baseline_clean_point_gain_db",
            "clean_point_state": "baseline_clean_point_state",
        }
    )
    robust_boundary = build_failure_boundary(robust_summary, failure_threshold_gain_db)
    merged = robust_boundary.merge(
        baseline,
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
    merged["clean_point_gain_delta_db"] = (
        merged["clean_point_gain_db"] - merged["baseline_clean_point_gain_db"]
    )
    return merged


def main() -> int:
    joint_cfg = JointToleranceConfig()
    out_dir = result_root()
    out_dir.mkdir(parents=True, exist_ok=True)

    mixed_train_objects, mix_counts = build_mixed_training_objects()
    all_rows: list[pd.DataFrame] = []

    for seed in joint_cfg.seeds:
        phase_config = PhaseOnlyConfig(
            seed=seed,
            train_case_count=joint_cfg.train_case_count,
            heldout_case_count=joint_cfg.eval_case_count,
        )
        train_cases = make_aberration_cases(joint_cfg.train_case_count, seed)
        train_samples = build_split_samples(mixed_train_objects, "train", train_cases, phase_config)
        trained = train_robust_phase_model(
            seed,
            train_samples,
            RobustTrainShim(
                train_case_count=joint_cfg.train_case_count,
                eval_case_count=joint_cfg.eval_case_count,
            ),
        )
        eval_cases = make_aberration_cases(joint_cfg.eval_case_count, seed + 500)

        for spec in load_subset_index():
            objects = [arr for _, arr in load_grayscale_objects(staging_root() / dataset_dir_name(spec))]
            eval_cache = {
                drift: build_wavelength_shifted_eval_samples(objects, eval_cases, trained["config"], drift)
                for drift in joint_cfg.wavelength_drift_fraction_levels
            }

            for phase_noise_sigma_rad in joint_cfg.phase_noise_sigma_rad_levels:
                for misalignment in joint_cfg.misalignment_levels:
                    repeat_count = 1
                    if phase_noise_sigma_rad > 0.0 or misalignment.shift_sigma_px > 0.0 or misalignment.rotation_sigma_deg > 0.0:
                        repeat_count = joint_cfg.monte_carlo_repeats
                    for wavelength_drift_fraction in joint_cfg.wavelength_drift_fraction_levels:
                        propagation = shifted_propagation(trained["config"], wavelength_drift_fraction)
                        eval_samples = eval_cache[wavelength_drift_fraction]
                        for repeat in range(repeat_count):
                            rng = np.random.default_rng(
                                2000003 * (seed + 1)
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
                            df = evaluate_robust_phase_only_stack(
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
    summary = summarize_joint_grid(seed_detail, joint_cfg.failure_threshold_gain_db)
    boundary = build_failure_boundary(summary, joint_cfg.failure_threshold_gain_db)
    axis_curves = build_axis_tolerance_curves(summary)
    boundary_expansion = build_boundary_expansion(
        summary,
        project_root() / "results" / "tolerance_joint" / "failure_boundary.csv",
        failure_threshold_gain_db=joint_cfg.failure_threshold_gain_db,
    )

    metrics_path = out_dir / "joint_tolerance_metrics.csv"
    seed_detail_path = out_dir / "joint_tolerance_seed_detail.csv"
    summary_path = out_dir / "joint_tolerance_curve.csv"
    degradation_path = out_dir / "degradation_ci.csv"
    boundary_path = out_dir / "failure_boundary.csv"
    axis_curve_path = out_dir / "axis_tolerance_curves.csv"
    expansion_path = out_dir / "boundary_expansion_vs_unmitigated.csv"
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
    boundary_expansion.to_csv(expansion_path, index=False)

    payload = {
        "status": "completed",
        "seeds": list(joint_cfg.seeds),
        "train_case_count": joint_cfg.train_case_count,
        "eval_case_count": joint_cfg.eval_case_count,
        "monte_carlo_repeats": joint_cfg.monte_carlo_repeats,
        "training_mix_counts": mix_counts,
        "failure_threshold_gain_db": joint_cfg.failure_threshold_gain_db,
        "output_files": {
            "joint_tolerance_metrics_csv": str(metrics_path),
            "joint_tolerance_seed_detail_csv": str(seed_detail_path),
            "joint_tolerance_curve_csv": str(summary_path),
            "degradation_ci_csv": str(degradation_path),
            "failure_boundary_csv": str(boundary_path),
            "axis_tolerance_curves_csv": str(axis_curve_path),
            "boundary_expansion_vs_unmitigated_csv": str(expansion_path),
            "summary_md": str(markdown_path),
        },
    }
    payload_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(build_summary_markdown(summary, boundary, joint_cfg), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
