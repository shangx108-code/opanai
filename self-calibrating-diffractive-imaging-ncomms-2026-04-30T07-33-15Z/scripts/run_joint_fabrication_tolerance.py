#!/usr/bin/env python3
"""Joint fabrication-tolerance execution for the active diffractive-imaging project.

This script upgrades the earlier single-factor tolerance package to a linked
three-factor scan over:
1. phase noise on the fabricated phase masks
2. layer-wise lateral/rotational misalignment
3. wavelength drift

The output package is organized around three reviewer-facing deliverables:
- tolerance curves over the executed joint grid
- degradation confidence intervals relative to the clean operating point
- failure-boundary tables using the paper's existing gain-over-fixed criterion
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from optics_propagation import PropagationConfig
from run_baseline_phase_only_megadiverse_train_dual_heldout_thickstats import (
    PhaseOnlyConfig,
    build_features,
    build_split_samples,
    make_aberration_cases,
    predict_ridge,
)
from run_baseline_reference_psf import psnr
from run_mixed_train_natural_object_rerun import build_mixed_training_objects
from run_mixed_train_tolerance import confidence_interval_95, train_models
from run_natural_object_evaluation import (
    dataset_dir_name,
    load_grayscale_objects,
    load_subset_index,
    staging_root,
)


@dataclass(frozen=True)
class MisalignmentLevel:
    label: str
    shift_sigma_px: float
    rotation_sigma_deg: float


@dataclass(frozen=True)
class JointToleranceConfig:
    seeds: tuple[int, ...] = (0, 1, 2)
    train_case_count: int = 24
    eval_case_count: int = 6
    phase_noise_sigma_rad_levels: tuple[float, ...] = (0.0, 0.05, 0.10, 0.20)
    wavelength_drift_fraction_levels: tuple[float, ...] = (0.0, 0.005, 0.010, 0.020)
    misalignment_levels: tuple[MisalignmentLevel, ...] = (
        MisalignmentLevel("clean", 0.0, 0.0),
        MisalignmentLevel("mild", 0.25, 0.50),
        MisalignmentLevel("moderate", 0.50, 1.00),
        MisalignmentLevel("severe", 1.00, 2.00),
    )
    monte_carlo_repeats: int = 4
    failure_threshold_gain_db: float = 0.0


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def result_root() -> Path:
    return project_root() / "results" / "tolerance_joint"


def to_float_image(arr: np.ndarray) -> Image.Image:
    return Image.fromarray(np.asarray(arr, dtype=np.float32), mode="F")


def from_float_image(image: Image.Image) -> np.ndarray:
    return np.asarray(image, dtype=np.float64)


def affine_transform_real(
    arr: np.ndarray,
    *,
    shift_x_px: float,
    shift_y_px: float,
    rotation_deg: float,
    fill_value: float,
) -> np.ndarray:
    image = to_float_image(arr)
    transformed = image.rotate(
        rotation_deg,
        resample=Image.Resampling.BICUBIC,
        translate=(shift_x_px, shift_y_px),
        fillcolor=float(fill_value),
    )
    return from_float_image(transformed)


def transform_complex_mask(
    mask: np.ndarray,
    *,
    shift_x_px: float,
    shift_y_px: float,
    rotation_deg: float,
) -> np.ndarray:
    real = affine_transform_real(
        np.real(mask),
        shift_x_px=shift_x_px,
        shift_y_px=shift_y_px,
        rotation_deg=rotation_deg,
        fill_value=1.0,
    )
    imag = affine_transform_real(
        np.imag(mask),
        shift_x_px=shift_x_px,
        shift_y_px=shift_y_px,
        rotation_deg=rotation_deg,
        fill_value=0.0,
    )
    transformed = real + 1j * imag
    magnitude = np.abs(transformed)
    safe = magnitude > 1.0e-8
    out = np.ones_like(transformed, dtype=np.complex128)
    out[safe] = transformed[safe] / magnitude[safe]
    return out


def apply_joint_mask_perturbation(
    masks: np.ndarray,
    *,
    phase_noise_sigma_rad: float,
    shift_sigma_px: float,
    rotation_sigma_deg: float,
    rng: np.random.Generator,
) -> np.ndarray:
    perturbed = []
    for mask in masks:
        shift_x_px = float(rng.normal(0.0, shift_sigma_px))
        shift_y_px = float(rng.normal(0.0, shift_sigma_px))
        rotation_deg = float(rng.normal(0.0, rotation_sigma_deg))
        transformed = transform_complex_mask(
            mask,
            shift_x_px=shift_x_px,
            shift_y_px=shift_y_px,
            rotation_deg=rotation_deg,
        )
        if phase_noise_sigma_rad > 0.0:
            phase_noise = rng.normal(0.0, phase_noise_sigma_rad, size=mask.shape)
            transformed = transformed * np.exp(1j * phase_noise)
        perturbed.append(transformed)
    return np.asarray(perturbed, dtype=np.complex128)


def wavelength_shifted_config(base_config: PhaseOnlyConfig, drift_fraction: float) -> PhaseOnlyConfig:
    return PhaseOnlyConfig(
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
        wavelength=base_config.wavelength * (1.0 + drift_fraction),
        sample_spacing=base_config.sample_spacing,
        propagation_distance=base_config.propagation_distance,
        noise_sigma=base_config.noise_sigma,
        nominal_wiener_k=base_config.nominal_wiener_k,
        guided_wiener_k=base_config.guided_wiener_k,
        propagation_model=base_config.propagation_model,
    )


def shifted_propagation(base_config: PhaseOnlyConfig, drift_fraction: float) -> PropagationConfig:
    frontend_spacing = base_config.sample_spacing * base_config.image_size / base_config.lowres_size
    return PropagationConfig(
        grid_size=base_config.lowres_size,
        sample_spacing=frontend_spacing,
        wavelength=base_config.wavelength * (1.0 + drift_fraction),
        propagation_distance=base_config.propagation_distance,
    )


def build_wavelength_shifted_eval_samples(
    objects: list[np.ndarray],
    eval_cases: list[dict[str, float]],
    base_config: PhaseOnlyConfig,
    drift_fraction: float,
) -> list[dict[str, object]]:
    return build_split_samples(
        objects,
        "natural_object_eval",
        eval_cases,
        wavelength_shifted_config(base_config, drift_fraction),
    )


def evaluate_phase_only_stack(
    eval_samples: list[dict[str, object]],
    *,
    masks: np.ndarray,
    propagation: PropagationConfig,
    phase_weights: np.ndarray,
    lowres_size: int,
) -> pd.DataFrame:
    features = build_features(eval_samples, masks, propagation)
    prediction = predict_ridge(features, phase_weights)
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


def build_seed_detail(metrics: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        metrics.groupby(
            [
                "dataset_name",
                "dataset_version",
                "phase_noise_sigma_rad",
                "misalignment_label",
                "shift_sigma_px",
                "rotation_sigma_deg",
                "wavelength_drift_fraction",
                "seed",
            ],
            as_index=False,
        )
        .agg(
            repeat_count=("repeat", "nunique"),
            sample_count=("psnr_gain_over_fixed_lowres", "size"),
            mean_psnr_gain_over_fixed_lowres=("psnr_gain_over_fixed_lowres", "mean"),
            mean_method_psnr_lowres=("method_psnr_lowres", "mean"),
            mean_fixed_psnr_lowres=("fixed_psnr_lowres", "mean"),
            mean_guided_psnr_lowres=("guided_psnr_lowres", "mean"),
        )
    )
    clean = grouped.loc[
        (grouped["phase_noise_sigma_rad"] == 0.0)
        & (grouped["shift_sigma_px"] == 0.0)
        & (grouped["rotation_sigma_deg"] == 0.0)
        & (grouped["wavelength_drift_fraction"] == 0.0),
        ["dataset_name", "dataset_version", "seed", "mean_psnr_gain_over_fixed_lowres"],
    ].rename(columns={"mean_psnr_gain_over_fixed_lowres": "clean_mean_psnr_gain_over_fixed_lowres"})
    merged = grouped.merge(clean, on=["dataset_name", "dataset_version", "seed"], how="left")
    merged["degradation_vs_clean_db"] = (
        merged["clean_mean_psnr_gain_over_fixed_lowres"] - merged["mean_psnr_gain_over_fixed_lowres"]
    )
    return merged


def summarize_joint_grid(seed_detail: pd.DataFrame, failure_threshold_gain_db: float) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    grouped = seed_detail.groupby(
        [
            "dataset_name",
            "dataset_version",
            "phase_noise_sigma_rad",
            "misalignment_label",
            "shift_sigma_px",
            "rotation_sigma_deg",
            "wavelength_drift_fraction",
        ]
    )
    for key, group in grouped:
        gains = group["mean_psnr_gain_over_fixed_lowres"].to_numpy(dtype=float)
        degradation = group["degradation_vs_clean_db"].to_numpy(dtype=float)
        mean_gain, gain_ci = confidence_interval_95(gains)
        mean_deg, deg_ci = confidence_interval_95(degradation)
        ci_low = mean_gain - gain_ci
        ci_high = mean_gain + gain_ci
        if ci_low > failure_threshold_gain_db:
            pass_state = "pass"
        elif ci_high <= failure_threshold_gain_db:
            pass_state = "fail"
        else:
            pass_state = "uncertain"
        rows.append(
            {
                "dataset_name": key[0],
                "dataset_version": key[1],
                "phase_noise_sigma_rad": key[2],
                "misalignment_label": key[3],
                "shift_sigma_px": key[4],
                "rotation_sigma_deg": key[5],
                "wavelength_drift_fraction": key[6],
                "seed_count": int(len(group)),
                "repeat_count_per_seed": int(group["repeat_count"].iloc[0]),
                "sample_count_per_seed": int(group["sample_count"].iloc[0]),
                "mean_psnr_gain_over_fixed_lowres": mean_gain,
                "gain_ci95_half_width": gain_ci,
                "gain_ci_low": ci_low,
                "gain_ci_high": ci_high,
                "mean_degradation_vs_clean_db": mean_deg,
                "degradation_ci95_half_width": deg_ci,
                "degradation_ci_low": mean_deg - deg_ci,
                "degradation_ci_high": mean_deg + deg_ci,
                "mean_method_psnr_lowres": float(group["mean_method_psnr_lowres"].mean()),
                "mean_fixed_psnr_lowres": float(group["mean_fixed_psnr_lowres"].mean()),
                "mean_guided_psnr_lowres": float(group["mean_guided_psnr_lowres"].mean()),
                "failure_threshold_gain_db": failure_threshold_gain_db,
                "pass_state": pass_state,
            }
        )
    return pd.DataFrame(rows).sort_values(
        [
            "dataset_name",
            "phase_noise_sigma_rad",
            "shift_sigma_px",
            "rotation_sigma_deg",
            "wavelength_drift_fraction",
        ]
    ).reset_index(drop=True)


def build_failure_boundary(summary: pd.DataFrame, failure_threshold_gain_db: float) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    grouped = summary.groupby(
        ["dataset_name", "dataset_version", "phase_noise_sigma_rad", "misalignment_label", "shift_sigma_px", "rotation_sigma_deg"]
    )
    for key, group in grouped:
        group = group.sort_values("wavelength_drift_fraction").reset_index(drop=True)
        pass_rows = group.loc[group["gain_ci_low"] > failure_threshold_gain_db]
        mean_fail_rows = group.loc[group["mean_psnr_gain_over_fixed_lowres"] <= failure_threshold_gain_db]
        certain_fail_rows = group.loc[group["gain_ci_high"] <= failure_threshold_gain_db]
        rows.append(
            {
                "dataset_name": key[0],
                "dataset_version": key[1],
                "phase_noise_sigma_rad": key[2],
                "misalignment_label": key[3],
                "shift_sigma_px": key[4],
                "rotation_sigma_deg": key[5],
                "max_passing_wavelength_drift_fraction": float(pass_rows["wavelength_drift_fraction"].max()) if not pass_rows.empty else np.nan,
                "first_mean_fail_wavelength_drift_fraction": float(mean_fail_rows["wavelength_drift_fraction"].iloc[0]) if not mean_fail_rows.empty else np.nan,
                "first_certain_fail_wavelength_drift_fraction": float(certain_fail_rows["wavelength_drift_fraction"].iloc[0]) if not certain_fail_rows.empty else np.nan,
                "clean_point_gain_db": float(group.loc[group["wavelength_drift_fraction"] == 0.0, "mean_psnr_gain_over_fixed_lowres"].iloc[0]),
                "clean_point_state": str(group.loc[group["wavelength_drift_fraction"] == 0.0, "pass_state"].iloc[0]),
                "failure_threshold_gain_db": failure_threshold_gain_db,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["dataset_name", "phase_noise_sigma_rad", "shift_sigma_px", "rotation_sigma_deg"]
    ).reset_index(drop=True)


def build_axis_tolerance_curves(summary: pd.DataFrame) -> pd.DataFrame:
    zero_mask = (
        (summary["phase_noise_sigma_rad"] == 0.0)
        & (summary["shift_sigma_px"] == 0.0)
        & (summary["rotation_sigma_deg"] == 0.0)
        & (summary["wavelength_drift_fraction"] == 0.0)
    )
    phase_curve = summary.loc[
        (summary["shift_sigma_px"] == 0.0)
        & (summary["rotation_sigma_deg"] == 0.0)
        & (summary["wavelength_drift_fraction"] == 0.0)
    ].copy()
    phase_curve["curve_family"] = "phase_noise_only"
    phase_curve["curve_level"] = phase_curve["phase_noise_sigma_rad"]

    misalignment_curve = summary.loc[
        (summary["phase_noise_sigma_rad"] == 0.0)
        & (summary["wavelength_drift_fraction"] == 0.0)
    ].copy()
    misalignment_curve["curve_family"] = "misalignment_only"
    misalignment_curve["curve_level"] = misalignment_curve["shift_sigma_px"]

    wavelength_curve = summary.loc[
        (summary["phase_noise_sigma_rad"] == 0.0)
        & (summary["shift_sigma_px"] == 0.0)
        & (summary["rotation_sigma_deg"] == 0.0)
    ].copy()
    wavelength_curve["curve_family"] = "wavelength_drift_only"
    wavelength_curve["curve_level"] = wavelength_curve["wavelength_drift_fraction"]

    clean_curve = summary.loc[zero_mask].copy()
    clean_curve["curve_family"] = "clean_point"
    clean_curve["curve_level"] = 0.0

    cols = [
        "dataset_name",
        "dataset_version",
        "curve_family",
        "curve_level",
        "phase_noise_sigma_rad",
        "misalignment_label",
        "shift_sigma_px",
        "rotation_sigma_deg",
        "wavelength_drift_fraction",
        "mean_psnr_gain_over_fixed_lowres",
        "gain_ci95_half_width",
        "mean_degradation_vs_clean_db",
        "degradation_ci95_half_width",
        "pass_state",
    ]
    return pd.concat([clean_curve, phase_curve, misalignment_curve, wavelength_curve], ignore_index=True)[cols]


def build_summary_markdown(summary: pd.DataFrame, boundary: pd.DataFrame, cfg: JointToleranceConfig) -> str:
    lines = [
        "# Joint Fabrication-Tolerance Summary",
        "",
        "Executed linked scan over phase noise, layer misalignment, and wavelength drift.",
        "",
        "## Executed grid",
        "",
        f"- Seeds: `{', '.join(str(seed) for seed in cfg.seeds)}`",
        f"- Monte Carlo repeats per noisy operating point: `{cfg.monte_carlo_repeats}`",
        f"- Phase-noise levels (rad RMS): `{', '.join(f'{level:.3f}' for level in cfg.phase_noise_sigma_rad_levels)}`",
        f"- Wavelength-drift levels (fraction): `{', '.join(f'{level:.3f}' for level in cfg.wavelength_drift_fraction_levels)}`",
        "- Misalignment levels:",
    ]
    for level in cfg.misalignment_levels:
        lines.append(
            f"  - `{level.label}`: shift sigma `{level.shift_sigma_px:.2f} px`, rotation sigma `{level.rotation_sigma_deg:.2f} deg`"
        )
    lines.extend(["", "## Failure-boundary snapshot", ""])
    for dataset_name in sorted(boundary["dataset_name"].unique()):
        dataset_rows = boundary.loc[boundary["dataset_name"] == dataset_name].copy()
        clean_rows = dataset_rows.loc[
            (dataset_rows["phase_noise_sigma_rad"] == 0.0)
            & (dataset_rows["shift_sigma_px"] == 0.0)
            & (dataset_rows["rotation_sigma_deg"] == 0.0)
        ]
        lines.append(f"- `{dataset_name}`:")
        if clean_rows.empty:
            lines.append("  - No clean boundary row found.")
            continue
        row = clean_rows.iloc[0]
        lines.append(
            "  - "
            + f"clean-point state `{row['clean_point_state']}`, first mean-fail drift "
            + (f"`{row['first_mean_fail_wavelength_drift_fraction']:.3f}`" if pd.notna(row["first_mean_fail_wavelength_drift_fraction"]) else "`not reached`")
        )
    lines.extend(["", "## Files", ""])
    lines.extend(
        [
            "- `joint_tolerance_curve.csv`: joint-grid tolerance curve with gain CI and degradation CI",
            "- `degradation_ci.csv`: degradation-focused view of the same grid",
            "- `failure_boundary.csv`: wavelength-drift failure boundary conditioned on phase noise and misalignment",
            "- `axis_tolerance_curves.csv`: one-factor slices for quick plotting",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    cfg = JointToleranceConfig()
    out_dir = result_root()
    out_dir.mkdir(parents=True, exist_ok=True)

    mixed_train_objects, mix_counts = build_mixed_training_objects()
    all_rows: list[pd.DataFrame] = []

    for seed in cfg.seeds:
        phase_config = PhaseOnlyConfig(
            seed=seed,
            train_case_count=cfg.train_case_count,
            heldout_case_count=cfg.eval_case_count,
        )
        train_cases = make_aberration_cases(cfg.train_case_count, seed)
        train_samples = build_split_samples(mixed_train_objects, "train", train_cases, phase_config)
        trained = train_models(seed, train_samples)
        eval_cases = make_aberration_cases(cfg.eval_case_count, seed + 500)

        for spec in load_subset_index():
            objects = [arr for _, arr in load_grayscale_objects(staging_root() / dataset_dir_name(spec))]
            eval_cache = {
                drift: build_wavelength_shifted_eval_samples(objects, eval_cases, trained["config"], drift)
                for drift in cfg.wavelength_drift_fraction_levels
            }

            for phase_noise_sigma_rad in cfg.phase_noise_sigma_rad_levels:
                for misalignment in cfg.misalignment_levels:
                    repeat_count = 1
                    if phase_noise_sigma_rad > 0.0 or misalignment.shift_sigma_px > 0.0 or misalignment.rotation_sigma_deg > 0.0:
                        repeat_count = cfg.monte_carlo_repeats
                    for wavelength_drift_fraction in cfg.wavelength_drift_fraction_levels:
                        propagation = shifted_propagation(trained["config"], wavelength_drift_fraction)
                        eval_samples = eval_cache[wavelength_drift_fraction]
                        for repeat in range(repeat_count):
                            rng = np.random.default_rng(
                                1000003 * (seed + 1)
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
                            df = evaluate_phase_only_stack(
                                eval_samples,
                                masks=masks,
                                propagation=propagation,
                                phase_weights=trained["phase_weights"],
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
    summary = summarize_joint_grid(seed_detail, cfg.failure_threshold_gain_db)
    boundary = build_failure_boundary(summary, cfg.failure_threshold_gain_db)
    axis_curves = build_axis_tolerance_curves(summary)

    metrics_path = out_dir / "joint_tolerance_metrics.csv"
    seed_detail_path = out_dir / "joint_tolerance_seed_detail.csv"
    summary_path = out_dir / "joint_tolerance_curve.csv"
    degradation_path = out_dir / "degradation_ci.csv"
    boundary_path = out_dir / "failure_boundary.csv"
    axis_curve_path = out_dir / "axis_tolerance_curves.csv"
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

    payload = {
        "status": "completed",
        "seeds": list(cfg.seeds),
        "train_case_count": cfg.train_case_count,
        "eval_case_count": cfg.eval_case_count,
        "monte_carlo_repeats": cfg.monte_carlo_repeats,
        "training_mix_counts": mix_counts,
        "failure_threshold_gain_db": cfg.failure_threshold_gain_db,
        "output_files": {
            "joint_tolerance_metrics_csv": str(metrics_path),
            "joint_tolerance_seed_detail_csv": str(seed_detail_path),
            "joint_tolerance_curve_csv": str(summary_path),
            "degradation_ci_csv": str(degradation_path),
            "failure_boundary_csv": str(boundary_path),
            "axis_tolerance_curves_csv": str(axis_curve_path),
            "summary_md": str(markdown_path),
        },
    }
    payload_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(build_summary_markdown(summary, boundary, cfg), encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
