#!/usr/bin/env python3
"""Run a held-out multi-seed baseline with a 3-layer phase-only frontend."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from optics_propagation import PropagationConfig, frequency_coordinates, propagate_fresnel
from run_baseline_reference_psf import (
    SimulationConfig,
    build_optics_metadata,
    fft_convolve,
    make_objects,
    make_psf,
    normalize_to_uint8,
    psnr,
    ssim_simple,
    wiener_deconvolution,
)


@dataclass
class PhaseOnlyConfig:
    image_size: int = 128
    pupil_size: int = 128
    lowres_size: int = 8
    layer_count: int = 3
    phase_basis_count: int = 6
    seed: int = 0
    train_case_count: int = 48
    heldout_case_count: int = 16
    ridge_lambda: float = 1.0
    search_steps: int = 10
    proposal_scale: float = 0.35
    wavelength: float = 532.0e-9
    sample_spacing: float = 8.0e-6
    propagation_distance: float = 12.0e-3
    noise_sigma: float = 0.01
    nominal_wiener_k: float = 1.0e-3
    guided_wiener_k: float = 5.0e-4
    propagation_model: str = "fresnel"


def confidence_interval_95(values: np.ndarray) -> tuple[float, float]:
    if len(values) < 2:
        return float(values.mean()), 0.0
    std = float(values.std(ddof=1))
    half_width = 1.96 * std / np.sqrt(len(values))
    return float(values.mean()), half_width


def write_sha256_manifest(paths: list[Path], manifest_path: Path) -> None:
    lines = []
    for path in sorted(paths):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        lines.append(f"{digest}  {path.name}")
    manifest_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def downsample(arr: np.ndarray, size: int) -> np.ndarray:
    image = normalize_to_uint8(arr)
    resized = image.resize((size, size), Image.Resampling.BICUBIC)
    return np.asarray(resized, dtype=np.float64) / 255.0


def make_phase_basis(size: int, count: int) -> np.ndarray:
    axis = np.linspace(-1.0, 1.0, size, endpoint=False)
    xx, yy = np.meshgrid(axis, axis)
    basis = [
        np.sin(np.pi * xx),
        np.sin(np.pi * yy),
        np.cos(np.pi * xx),
        np.cos(np.pi * yy),
        np.sin(np.pi * (xx + yy)),
        np.sin(np.pi * (xx - yy)),
    ]
    return np.asarray(basis[:count], dtype=np.float64)


def phase_masks_from_coeffs(coeffs: np.ndarray, basis: np.ndarray) -> np.ndarray:
    masks = []
    for layer_coeffs in coeffs:
        phase = np.tensordot(layer_coeffs, basis, axes=(0, 0))
        masks.append(np.exp(1j * np.pi * np.tanh(phase)))
    return np.asarray(masks)


def propagate_phase_frontend(
    noisy_lowres: np.ndarray,
    reference_lowres: np.ndarray,
    masks: np.ndarray,
    propagation: PropagationConfig,
) -> list[np.ndarray]:
    amplitude = np.sqrt(np.clip(0.85 * noisy_lowres + 0.15 * reference_lowres, 0.0, 1.0) + 1.0e-8)
    field = amplitude.astype(np.complex128)
    outputs: list[np.ndarray] = []
    for mask in masks:
        field = propagate_fresnel(field * mask, propagation)
        intensity = np.abs(field) ** 2
        intensity = intensity / (intensity.max() + 1.0e-8)
        outputs.append(intensity)
    return outputs


def make_aberration_cases(case_count: int, seed: int) -> list[dict[str, float]]:
    rng = np.random.default_rng(seed)
    cases = []
    for _ in range(case_count):
        cases.append(
            {
                "defocus": float(rng.uniform(-1.5, 1.5)),
                "astig_x": float(rng.uniform(-1.0, 1.0)),
                "coma_x": float(rng.uniform(-0.8, 0.8)),
            }
        )
    return cases


def build_split_samples(
    objects: list[np.ndarray],
    object_split: str,
    cases: list[dict[str, float]],
    config: PhaseOnlyConfig,
) -> list[dict[str, object]]:
    lowres_objects = [downsample(obj, config.lowres_size) for obj in objects]
    nominal_psf = make_psf(
        config.pupil_size,
        {
            "defocus": 0.0,
            "astig_x": 0.0,
            "coma_x": 0.0,
            "_sample_spacing": config.sample_spacing,
            "_wavelength": config.wavelength,
            "_propagation_distance": config.propagation_distance,
            "_propagation_model": config.propagation_model,
        },
    )

    samples: list[dict[str, object]] = []
    rng = np.random.default_rng(config.seed + (0 if object_split == "train" else 1000))
    for case_id, coeffs in enumerate(cases):
        psf = make_psf(
            config.pupil_size,
            {
                **coeffs,
                "_sample_spacing": config.sample_spacing,
                "_wavelength": config.wavelength,
                "_propagation_distance": config.propagation_distance,
                "_propagation_model": config.propagation_model,
            },
        )
        reference_lowres = downsample(psf, config.lowres_size)
        for object_id, (obj_native, obj_lowres) in enumerate(zip(objects, lowres_objects)):
            blurred = fft_convolve(obj_native, psf)
            noisy = np.clip(blurred + rng.normal(0.0, config.noise_sigma, blurred.shape), 0.0, 1.0)
            fixed_restore = wiener_deconvolution(noisy, nominal_psf, config.nominal_wiener_k)
            guided_restore = wiener_deconvolution(noisy, psf, config.guided_wiener_k)
            noisy_lowres = downsample(noisy, config.lowres_size)
            fixed_lowres = downsample(fixed_restore, config.lowres_size)
            guided_lowres = downsample(guided_restore, config.lowres_size)
            samples.append(
                {
                    "split": object_split,
                    "case_id": case_id,
                    "object_id": f"{object_split}_object_{object_id:02d}",
                    "defocus": coeffs["defocus"],
                    "astig_x": coeffs["astig_x"],
                    "coma_x": coeffs["coma_x"],
                    "gt_lowres": obj_lowres,
                    "noisy_lowres": noisy_lowres,
                    "reference_lowres": reference_lowres,
                    "fixed_psnr_lowres": psnr(obj_lowres, fixed_lowres),
                    "guided_psnr_lowres": psnr(obj_lowres, guided_lowres),
                    "fixed_ssim_lowres": ssim_simple(obj_lowres, fixed_lowres),
                    "guided_ssim_lowres": ssim_simple(obj_lowres, guided_lowres),
                }
            )
    return samples


def build_features(samples: list[dict[str, object]], masks: np.ndarray, propagation: PropagationConfig) -> np.ndarray:
    rows = []
    for sample in samples:
        outputs = propagate_phase_frontend(
            sample["noisy_lowres"], sample["reference_lowres"], masks, propagation
        )
        feature_blocks = [
            sample["noisy_lowres"].reshape(-1),
            sample["reference_lowres"].reshape(-1),
            *(out.reshape(-1) for out in outputs),
        ]
        rows.append(np.concatenate(feature_blocks))
    return np.asarray(rows)


def build_targets(samples: list[dict[str, object]]) -> np.ndarray:
    return np.asarray([sample["gt_lowres"].reshape(-1) for sample in samples])


def fit_ridge_regression(x_train: np.ndarray, y_train: np.ndarray, ridge_lambda: float) -> np.ndarray:
    x_aug = np.concatenate([x_train, np.ones((x_train.shape[0], 1))], axis=1)
    xtx = x_aug.T @ x_aug
    regularizer = ridge_lambda * np.eye(xtx.shape[0])
    regularizer[-1, -1] = 0.0
    xty = x_aug.T @ y_train
    return np.linalg.solve(xtx + regularizer, xty)


def predict_ridge(x: np.ndarray, weights: np.ndarray) -> np.ndarray:
    x_aug = np.concatenate([x, np.ones((x.shape[0], 1))], axis=1)
    prediction = x_aug @ weights
    return np.clip(prediction, 0.0, 1.0)


def evaluate_training_objective(
    coeffs: np.ndarray,
    basis: np.ndarray,
    train_samples: list[dict[str, object]],
    propagation: PropagationConfig,
    ridge_lambda: float,
) -> tuple[float, np.ndarray]:
    masks = phase_masks_from_coeffs(coeffs, basis)
    x_train = build_features(train_samples, masks, propagation)
    y_train = build_targets(train_samples)
    weights = fit_ridge_regression(x_train, y_train, ridge_lambda)
    prediction = predict_ridge(x_train, weights)
    mse = float(np.mean((prediction - y_train) ** 2))
    return mse, weights


def optimize_phase_coeffs(
    config: PhaseOnlyConfig,
    basis: np.ndarray,
    train_samples: list[dict[str, object]],
    propagation: PropagationConfig,
) -> np.ndarray:
    rng = np.random.default_rng(config.seed)
    coeffs = rng.normal(0.0, 0.15, size=(config.layer_count, config.phase_basis_count))
    best_loss, _ = evaluate_training_objective(coeffs, basis, train_samples, propagation, config.ridge_lambda)
    step = config.proposal_scale
    for _ in range(config.search_steps):
        direction = rng.normal(0.0, 1.0, size=coeffs.shape)
        candidate_plus = coeffs + step * direction
        candidate_minus = coeffs - step * direction
        loss_plus, _ = evaluate_training_objective(
            candidate_plus, basis, train_samples, propagation, config.ridge_lambda
        )
        loss_minus, _ = evaluate_training_objective(
            candidate_minus, basis, train_samples, propagation, config.ridge_lambda
        )
        if loss_plus < best_loss or loss_minus < best_loss:
            if loss_plus <= loss_minus:
                coeffs = candidate_plus
                best_loss = loss_plus
            else:
                coeffs = candidate_minus
                best_loss = loss_minus
        step *= 0.85
    return coeffs


def run_seed(config: PhaseOnlyConfig) -> tuple[pd.DataFrame, dict[str, float]]:
    train_objects = make_objects(config.image_size)
    train_cases = make_aberration_cases(config.train_case_count, config.seed)
    heldout_cases = make_aberration_cases(config.heldout_case_count, config.seed + 500)

    train_samples = build_split_samples(train_objects, "train", train_cases, config)
    heldout_samples = build_split_samples(train_objects, "heldout", heldout_cases, config)

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
    weights = fit_ridge_regression(x_train, y_train, config.ridge_lambda)

    x_test = build_features(heldout_samples, masks, propagation)
    y_test = build_targets(heldout_samples)
    prediction = predict_ridge(x_test, weights)

    rows = []
    for idx, sample in enumerate(heldout_samples):
        pred = prediction[idx].reshape(config.lowres_size, config.lowres_size)
        phase_psnr = psnr(sample["gt_lowres"], pred)
        phase_ssim = ssim_simple(sample["gt_lowres"], pred)
        rows.append(
            {
                "seed": config.seed,
                "case_id": sample["case_id"],
                "object_id": sample["object_id"],
                "split": sample["split"],
                "defocus": sample["defocus"],
                "astig_x": sample["astig_x"],
                "coma_x": sample["coma_x"],
                "fixed_psnr_lowres": sample["fixed_psnr_lowres"],
                "guided_psnr_lowres": sample["guided_psnr_lowres"],
                "phaseonly_psnr_lowres": phase_psnr,
                "fixed_ssim_lowres": sample["fixed_ssim_lowres"],
                "guided_ssim_lowres": sample["guided_ssim_lowres"],
                "phaseonly_ssim_lowres": phase_ssim,
                "phaseonly_psnr_gain_over_fixed_lowres": phase_psnr - sample["fixed_psnr_lowres"],
                "phaseonly_psnr_gap_to_guided_lowres": sample["guided_psnr_lowres"] - phase_psnr,
                "phaseonly_ssim_gain_over_fixed_lowres": phase_ssim - sample["fixed_ssim_lowres"],
            }
        )

    df = pd.DataFrame(rows)
    fx, fy = frequency_coordinates(propagation)
    summary = {
        "seed": config.seed,
        "layer_count": config.layer_count,
        "phase_basis_count": config.phase_basis_count,
        "frontend_sample_spacing_m": frontend_spacing,
        "wavelength_m": config.wavelength,
        "propagation_distance_m": config.propagation_distance,
        "fx_min_1_per_m": float(fx.min()),
        "fx_max_1_per_m": float(fx.max()),
        "fy_min_1_per_m": float(fy.min()),
        "fy_max_1_per_m": float(fy.max()),
        "mean_fixed_psnr_lowres": float(df["fixed_psnr_lowres"].mean()),
        "mean_guided_psnr_lowres": float(df["guided_psnr_lowres"].mean()),
        "mean_phaseonly_psnr_lowres": float(df["phaseonly_psnr_lowres"].mean()),
        "mean_phaseonly_psnr_gain_over_fixed_lowres": float(
            df["phaseonly_psnr_gain_over_fixed_lowres"].mean()
        ),
        "mean_phaseonly_psnr_gap_to_guided_lowres": float(
            df["phaseonly_psnr_gap_to_guided_lowres"].mean()
        ),
        "mean_fixed_ssim_lowres": float(df["fixed_ssim_lowres"].mean()),
        "mean_guided_ssim_lowres": float(df["guided_ssim_lowres"].mean()),
        "mean_phaseonly_ssim_lowres": float(df["phaseonly_ssim_lowres"].mean()),
        "mean_phaseonly_ssim_gain_over_fixed_lowres": float(
            df["phaseonly_ssim_gain_over_fixed_lowres"].mean()
        ),
        "phaseonly_better_than_fixed_fraction": float(
            (df["phaseonly_psnr_gain_over_fixed_lowres"] > 0.0).mean()
        ),
    }
    return df, summary


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "results" / "baselines" / "baseline-003-phaseonly-heldout-multiseed"
    out_dir.mkdir(parents=True, exist_ok=True)

    seeds = [0, 1, 2]
    generated_files: list[Path] = []
    per_seed_rows = []

    native_optics = build_optics_metadata(
        SimulationConfig(
            wavelength=532.0e-9,
            sample_spacing=8.0e-6,
            propagation_distance=12.0e-3,
            propagation_model="fresnel",
        )
    )

    for seed in seeds:
        config = PhaseOnlyConfig(seed=seed)
        df, summary = run_seed(config)
        metrics_path = out_dir / f"heldout_metrics_seed{seed}.csv"
        log_path = out_dir / f"run_log_seed_{seed}.txt"
        df.to_csv(metrics_path, index=False)
        log_path.write_text(
            "\n".join(
                [
                    f"seed={seed}",
                    "propagation_model=fresnel",
                    "fresnel_transfer_function=exp(-i*pi*lambda*z*(fx^2+fy^2))",
                    f"layer_count={summary['layer_count']}",
                    f"phase_basis_count={summary['phase_basis_count']}",
                    f"wavelength_m={summary['wavelength_m']}",
                    f"sample_spacing_m_native={native_optics['sample_spacing_m']}",
                    f"sample_spacing_m_frontend={summary['frontend_sample_spacing_m']}",
                    f"propagation_distance_m={summary['propagation_distance_m']}",
                    f"fx_min_1_per_m={summary['fx_min_1_per_m']}",
                    f"fx_max_1_per_m={summary['fx_max_1_per_m']}",
                    f"fy_min_1_per_m={summary['fy_min_1_per_m']}",
                    f"fy_max_1_per_m={summary['fy_max_1_per_m']}",
                    f"heldout_mean_phaseonly_psnr_lowres={summary['mean_phaseonly_psnr_lowres']}",
                    f"heldout_mean_phaseonly_ssim_lowres={summary['mean_phaseonly_ssim_lowres']}",
                    f"heldout_phaseonly_better_than_fixed_fraction={summary['phaseonly_better_than_fixed_fraction']}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        generated_files.extend([metrics_path, log_path])
        per_seed_rows.append(summary)

    per_seed_df = pd.DataFrame(per_seed_rows)
    summary_rows = []
    for metric in [
        "mean_fixed_psnr_lowres",
        "mean_guided_psnr_lowres",
        "mean_phaseonly_psnr_lowres",
        "mean_phaseonly_psnr_gain_over_fixed_lowres",
        "mean_phaseonly_psnr_gap_to_guided_lowres",
        "mean_fixed_ssim_lowres",
        "mean_guided_ssim_lowres",
        "mean_phaseonly_ssim_lowres",
        "mean_phaseonly_ssim_gain_over_fixed_lowres",
        "phaseonly_better_than_fixed_fraction",
    ]:
        values = per_seed_df[metric].to_numpy(dtype=float)
        mean, ci95 = confidence_interval_95(values)
        summary_rows.append(
            {
                "metric": metric,
                "mean": mean,
                "std": float(values.std(ddof=1)),
                "ci95_half_width": ci95,
                "seed_count": len(values),
            }
        )
    summary_path = out_dir / "multiseed_summary.csv"
    pd.DataFrame(summary_rows).to_csv(summary_path, index=False)
    generated_files.append(summary_path)

    manifest_path = out_dir / "sha256_manifest.txt"
    write_sha256_manifest(generated_files, manifest_path)

    print(
        json.dumps(
            {
                "output_dir": str(out_dir),
                "seeds": seeds,
                "layer_count": 3,
                "artifact_count": len(generated_files) + 1,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
