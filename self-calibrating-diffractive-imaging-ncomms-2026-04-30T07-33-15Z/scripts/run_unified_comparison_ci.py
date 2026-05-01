#!/usr/bin/env python3
"""Run one unified four-method comparison on the frozen dual held-out ledgers."""

from __future__ import annotations

import csv
import json
import os
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np
import pandas as pd

from run_baseline_reference_psf import psnr
from run_baseline_phase_only_megadiverse_train_dual_heldout_thickstats import (
    PhaseOnlyConfig,
    build_features,
    build_split_samples,
    build_targets,
    confidence_interval_95,
    fit_ridge_regression,
    make_aberration_cases,
    make_heldout_objects,
    make_megadiverse_training_objects,
    make_objects,
    make_phase_basis,
    optimize_phase_coeffs,
    phase_masks_from_coeffs,
    predict_ridge,
)
from run_parameter_matched_digital_surrogate import build_parameter_matched_features
from optics_propagation import PropagationConfig


SEEDS = list(range(10))
LEDGER_NAMES = (
    "same_family_heldout_aberration",
    "new_family_heldout_object_family",
)
PHASEONLY_EXISTING_DIR = (
    Path(__file__).resolve().parents[1]
    / "results"
    / "baselines"
    / "baseline-009-phaseonly-megadiverse-thickstats"
)


def spectral_feature_vector(
    noisy_lowres: np.ndarray,
    reference_lowres: np.ndarray,
    spectral_crop_size: int,
) -> np.ndarray:
    def crop_coeffs(arr: np.ndarray) -> np.ndarray:
        shifted = np.fft.fftshift(np.fft.fft2(arr))
        center = shifted.shape[0] // 2
        radius = spectral_crop_size // 2
        patch = shifted[
            center - radius : center - radius + spectral_crop_size,
            center - radius : center - radius + spectral_crop_size,
        ]
        return np.concatenate([patch.real.reshape(-1), patch.imag.reshape(-1)])

    return np.concatenate(
        [
            crop_coeffs(noisy_lowres),
            crop_coeffs(reference_lowres),
        ]
    )


def build_spectral_features(samples: list[dict[str, object]], spectral_crop_size: int) -> np.ndarray:
    rows = []
    for sample in samples:
        rows.append(
            spectral_feature_vector(
                sample["noisy_lowres"],
                sample["reference_lowres"],
                spectral_crop_size,
            )
        )
    return np.asarray(rows, dtype=np.float64)


def evaluate_prediction_method(
    method_name: str,
    samples: list[dict[str, object]],
    prediction: np.ndarray,
    lowres_size: int,
) -> pd.DataFrame:
    rows = []
    for index, sample in enumerate(samples):
        pred = prediction[index].reshape(lowres_size, lowres_size)
        method_psnr = psnr(sample["gt_lowres"], pred)
        rows.append(
            {
                "method": method_name,
                "seed": int(sample["seed"]),
                "ledger": str(sample["ledger"]),
                "case_id": int(sample["case_id"]),
                "object_id": str(sample["object_id"]),
                "fixed_psnr_lowres": float(sample["fixed_psnr_lowres"]),
                "method_psnr_lowres": float(method_psnr),
                "psnr_gain_over_fixed_lowres": float(method_psnr - sample["fixed_psnr_lowres"]),
                "better_than_fixed": bool(method_psnr > sample["fixed_psnr_lowres"]),
            }
        )
    return pd.DataFrame(rows)


def evaluate_reference_method(samples: list[dict[str, object]]) -> pd.DataFrame:
    rows = []
    for sample in samples:
        method_psnr = float(sample["guided_psnr_lowres"])
        rows.append(
            {
                "method": "reference_psf_deconvolution",
                "seed": int(sample["seed"]),
                "ledger": str(sample["ledger"]),
                "case_id": int(sample["case_id"]),
                "object_id": str(sample["object_id"]),
                "fixed_psnr_lowres": float(sample["fixed_psnr_lowres"]),
                "method_psnr_lowres": method_psnr,
                "psnr_gain_over_fixed_lowres": float(method_psnr - sample["fixed_psnr_lowres"]),
                "better_than_fixed": bool(method_psnr > sample["fixed_psnr_lowres"]),
            }
        )
    return pd.DataFrame(rows)


def summarize_method_seed(df: pd.DataFrame) -> pd.DataFrame:
    ledger_summary = (
        df.groupby(["method", "seed", "ledger"], as_index=False)
        .agg(
            mean_psnr_gain=("psnr_gain_over_fixed_lowres", "mean"),
            better_than_fixed_fraction=("better_than_fixed", "mean"),
        )
    )
    return (
        ledger_summary.groupby(["method", "seed"], as_index=False)
        .agg(
            mean_psnr_gain=("mean_psnr_gain", "mean"),
            better_than_fixed_fraction=("better_than_fixed_fraction", "mean"),
        )
    )


def format_ci(mean: float, half_width: float) -> str:
    lower = mean - half_width
    upper = mean + half_width
    return f"[{lower:.6f}, {upper:.6f}]"


def build_final_summary(per_seed_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for method_name in per_seed_summary["method"].unique():
        method_df = per_seed_summary.loc[per_seed_summary["method"] == method_name].reset_index(drop=True)
        gains = method_df["mean_psnr_gain"].to_numpy(dtype=float)
        fractions = method_df["better_than_fixed_fraction"].to_numpy(dtype=float)
        mean_gain, gain_ci_half_width = confidence_interval_95(gains)
        rows.append(
            {
                "method": method_name,
                "mean_psnr_gain": mean_gain,
                "std": float(gains.std(ddof=1)) if len(gains) > 1 else 0.0,
                "95% CI": format_ci(mean_gain, gain_ci_half_width),
                "better_than_fixed_fraction": float(fractions.mean()),
            }
        )
    return pd.DataFrame(rows)


def build_ledgers(config: PhaseOnlyConfig, seed: int) -> tuple[list[dict[str, object]], dict[str, list[dict[str, object]]]]:
    train_objects = make_megadiverse_training_objects(config.image_size)
    same_family_eval_objects = make_objects(config.image_size)
    new_family_eval_objects = make_heldout_objects(config.image_size)
    train_cases = make_aberration_cases(config.train_case_count, seed)
    heldout_cases = make_aberration_cases(config.heldout_case_count, seed + 500)

    train_samples = build_split_samples(train_objects, "train", train_cases, config)
    same_family_samples = build_split_samples(same_family_eval_objects, "heldout_aberration", heldout_cases, config)
    new_family_samples = build_split_samples(new_family_eval_objects, "heldout_object_family", heldout_cases, config)

    for sample in train_samples:
        sample["seed"] = seed
        sample["ledger"] = "train"
    for sample in same_family_samples:
        sample["seed"] = seed
        sample["ledger"] = "same_family_heldout_aberration"
    for sample in new_family_samples:
        sample["seed"] = seed
        sample["ledger"] = "new_family_heldout_object_family"

    return train_samples, {
        "same_family_heldout_aberration": same_family_samples,
        "new_family_heldout_object_family": new_family_samples,
    }


def load_existing_phaseonly_detail(seed: int) -> pd.DataFrame | None:
    detail_frames: list[pd.DataFrame] = []
    for ledger_name in LEDGER_NAMES:
        metrics_path = PHASEONLY_EXISTING_DIR / ledger_name / f"heldout_metrics_seed{seed}.csv"
        if not metrics_path.exists():
            return None
        source_df = pd.read_csv(metrics_path)
        detail_frames.append(
            pd.DataFrame(
                {
                    "method": "phase_only_stack",
                    "seed": seed,
                    "ledger": ledger_name,
                    "case_id": source_df["case_id"].astype(int),
                    "object_id": source_df["object_id"].astype(str),
                    "fixed_psnr_lowres": source_df["fixed_psnr_lowres"].astype(float),
                    "method_psnr_lowres": source_df["phaseonly_psnr_lowres"].astype(float),
                    "psnr_gain_over_fixed_lowres": source_df["phaseonly_psnr_gain_over_fixed_lowres"].astype(float),
                    "better_than_fixed": source_df["phaseonly_psnr_gain_over_fixed_lowres"].astype(float) > 0.0,
                }
            )
        )
    return pd.concat(detail_frames, ignore_index=True)


def run_seed(seed: int) -> tuple[pd.DataFrame, pd.DataFrame]:
    config = PhaseOnlyConfig(seed=seed)
    train_samples, ledgers = build_ledgers(config, seed)
    train_targets = build_targets(train_samples)

    ridge_train_features = np.asarray(
        [
            np.concatenate([sample["noisy_lowres"].reshape(-1), sample["reference_lowres"].reshape(-1)])
            for sample in train_samples
        ],
        dtype=np.float64,
    )
    ridge_weights = fit_ridge_regression(ridge_train_features, train_targets, config.ridge_lambda)

    spectral_crop_size = 6
    spectral_train_features = build_spectral_features(train_samples, spectral_crop_size)
    spectral_weights = fit_ridge_regression(spectral_train_features, train_targets, config.ridge_lambda)
    parameter_matched_train_features = build_parameter_matched_features(train_samples)
    parameter_matched_weights = fit_ridge_regression(
        parameter_matched_train_features,
        train_targets,
        config.ridge_lambda,
    )

    detail_frames: list[pd.DataFrame] = []
    per_seed_frames: list[pd.DataFrame] = []

    phaseonly_detail_df = load_existing_phaseonly_detail(seed)
    if phaseonly_detail_df is None:
        frontend_spacing = config.sample_spacing * config.image_size / config.lowres_size
        propagation = PropagationConfig(
            grid_size=config.lowres_size,
            sample_spacing=frontend_spacing,
            wavelength=config.wavelength,
            propagation_distance=config.propagation_distance,
        )
        basis = make_phase_basis(config.lowres_size, config.phase_basis_count)
        coeffs = optimize_phase_coeffs(config, basis, train_samples, propagation)
        masks = phase_masks_from_coeffs(coeffs, basis)
        phase_train_features = build_features(train_samples, masks, propagation)
        phase_weights = fit_ridge_regression(phase_train_features, train_targets, config.ridge_lambda)
    else:
        propagation = None
        masks = None
        phase_weights = None

    for ledger_name in LEDGER_NAMES:
        ledger_samples = ledgers[ledger_name]
        ridge_prediction = predict_ridge(
            np.asarray(
                [
                    np.concatenate([sample["noisy_lowres"].reshape(-1), sample["reference_lowres"].reshape(-1)])
                    for sample in ledger_samples
                ],
                dtype=np.float64,
            ),
            ridge_weights,
        )
        spectral_prediction = predict_ridge(
            build_spectral_features(ledger_samples, spectral_crop_size),
            spectral_weights,
        )
        parameter_matched_prediction = predict_ridge(
            build_parameter_matched_features(ledger_samples),
            parameter_matched_weights,
        )

        detail_frames.extend(
            [
                evaluate_reference_method(ledger_samples),
                evaluate_prediction_method("trainable_surrogate_ridge", ledger_samples, ridge_prediction, config.lowres_size),
                evaluate_prediction_method("spectral_frontend", ledger_samples, spectral_prediction, config.lowres_size),
                evaluate_prediction_method(
                    "parameter_matched_digital_surrogate",
                    ledger_samples,
                    parameter_matched_prediction,
                    config.lowres_size,
                ),
            ]
        )
        if phaseonly_detail_df is None:
            phase_prediction = predict_ridge(build_features(ledger_samples, masks, propagation), phase_weights)
            detail_frames.append(
                evaluate_prediction_method("phase_only_stack", ledger_samples, phase_prediction, config.lowres_size)
            )

    if phaseonly_detail_df is not None:
        detail_frames.append(phaseonly_detail_df)

    detail_df = pd.concat(detail_frames, ignore_index=True)
    per_seed_df = summarize_method_seed(detail_df)
    return detail_df, per_seed_df


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    results_dir = project_root / "results"
    unified_dir = results_dir / "unified_comparison"
    unified_dir.mkdir(parents=True, exist_ok=True)

    with ProcessPoolExecutor(max_workers=min(5, len(SEEDS))) as executor:
        seed_outputs = list(executor.map(run_seed, SEEDS))

    detail_df = pd.concat([item[0] for item in seed_outputs], ignore_index=True)
    per_seed_df = pd.concat([item[1] for item in seed_outputs], ignore_index=True)
    final_df = build_final_summary(per_seed_df)
    final_df = final_df.sort_values("mean_psnr_gain", ascending=False).reset_index(drop=True)

    detail_path = unified_dir / "unified_comparison_detail.csv"
    per_seed_path = unified_dir / "unified_comparison_per_seed.csv"
    summary_json_path = unified_dir / "unified_comparison_summary.json"
    final_csv_path = results_dir / "unified_comparison_ci.csv"

    detail_df.to_csv(detail_path, index=False)
    per_seed_df.to_csv(per_seed_path, index=False)
    final_df.to_csv(final_csv_path, index=False, quoting=csv.QUOTE_MINIMAL)
    summary_json_path.write_text(
        json.dumps(
            {
                "seeds": SEEDS,
                "seed_count": len(SEEDS),
                "ledgers": list(LEDGER_NAMES),
                "phase_only_config": {
                    "training_object_family_count": 50,
                    "layer_count": 5,
                    "phase_basis_count": 10,
                    "lowres_size": 12,
                    "train_case_count": 96,
                    "heldout_case_count": 24,
                },
                "spectral_frontend_crop_size": 6,
                "output_csv": str(final_csv_path),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(json.dumps({"output_csv": str(final_csv_path), "seed_count": len(SEEDS)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
