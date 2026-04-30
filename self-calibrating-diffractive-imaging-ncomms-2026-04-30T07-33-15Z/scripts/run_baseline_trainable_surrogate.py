#!/usr/bin/env python3
"""Run a minimal trainable surrogate baseline with reference guidance."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from run_baseline_reference_psf import (
    SimulationConfig,
    fft_convolve,
    make_montage,
    make_objects,
    make_psf,
    normalize_to_uint8,
    psnr,
    ssim_simple,
    wiener_deconvolution,
)


@dataclass
class SurrogateConfig:
    image_size: int = 128
    pupil_size: int = 128
    lowres_size: int = 16
    noise_sigma: float = 0.01
    nominal_wiener_k: float = 1.0e-3
    guided_wiener_k: float = 5.0e-4
    ridge_lambda: float = 2.5
    seed: int = 17
    train_case_count: int = 72
    test_case_count: int = 24


def downsample(arr: np.ndarray, size: int) -> np.ndarray:
    image = normalize_to_uint8(arr)
    resized = image.resize((size, size), Image.Resampling.BICUBIC)
    return np.asarray(resized, dtype=np.float64) / 255.0


def build_dataset(config: SurrogateConfig) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(config.seed)
    objects = make_objects(config.image_size)
    object_names = [f"object_{idx:02d}" for idx in range(len(objects))]
    nominal_psf = make_psf(config.pupil_size, {"defocus": 0.0, "astig_x": 0.0, "coma_x": 0.0})

    rows = []
    feature_rows = []
    target_rows = []

    total_cases = config.train_case_count + config.test_case_count
    for case_id in range(total_cases):
        coeffs = {
            "defocus": float(rng.uniform(-1.5, 1.5)),
            "astig_x": float(rng.uniform(-1.0, 1.0)),
            "coma_x": float(rng.uniform(-0.8, 0.8)),
        }
        psf = make_psf(config.pupil_size, coeffs)
        reference_lowres = downsample(psf, config.lowres_size)
        split = "train" if case_id < config.train_case_count else "test"
        for obj_idx, obj in enumerate(objects):
            blurred = fft_convolve(obj, psf)
            noisy = np.clip(blurred + rng.normal(0.0, config.noise_sigma, blurred.shape), 0.0, 1.0)
            fixed_restore = wiener_deconvolution(noisy, nominal_psf, config.nominal_wiener_k)
            guided_restore = wiener_deconvolution(noisy, psf, config.guided_wiener_k)

            gt_lowres = downsample(obj, config.lowres_size)
            noisy_lowres = downsample(noisy, config.lowres_size)
            fixed_lowres = downsample(fixed_restore, config.lowres_size)
            guided_lowres = downsample(guided_restore, config.lowres_size)
            feature = np.concatenate([noisy_lowres.reshape(-1), reference_lowres.reshape(-1)])

            rows.append(
                {
                    "case_id": case_id,
                    "split": split,
                    "object_id": object_names[obj_idx],
                    "defocus": coeffs["defocus"],
                    "astig_x": coeffs["astig_x"],
                    "coma_x": coeffs["coma_x"],
                    "fixed_psnr": psnr(obj, fixed_restore),
                    "guided_psnr": psnr(obj, guided_restore),
                    "fixed_ssim": ssim_simple(obj, fixed_restore),
                    "guided_ssim": ssim_simple(obj, guided_restore),
                    "fixed_psnr_lowres": psnr(gt_lowres, fixed_lowres),
                    "guided_psnr_lowres": psnr(gt_lowres, guided_lowres),
                    "fixed_ssim_lowres": ssim_simple(gt_lowres, fixed_lowres),
                    "guided_ssim_lowres": ssim_simple(gt_lowres, guided_lowres),
                }
            )
            feature_rows.append(feature)
            target_rows.append(gt_lowres.reshape(-1))
    return pd.DataFrame(rows), np.asarray(feature_rows), np.asarray(target_rows)


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


def main() -> int:
    config = SurrogateConfig()
    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "results" / "baselines" / "baseline-002-trainable-surrogate"
    out_dir.mkdir(parents=True, exist_ok=True)

    df, features, targets = build_dataset(config)
    train_mask = df["split"].to_numpy() == "train"
    test_mask = ~train_mask

    weights = fit_ridge_regression(features[train_mask], targets[train_mask], config.ridge_lambda)
    pred_lowres = predict_ridge(features[test_mask], weights)
    gt_lowres = targets[test_mask]

    lowres_psnr = np.array([psnr(gt_lowres[i], pred_lowres[i]) for i in range(len(pred_lowres))])
    lowres_ssim = np.array([ssim_simple(gt_lowres[i], pred_lowres[i]) for i in range(len(pred_lowres))])

    test_df = df.loc[test_mask].copy().reset_index(drop=True)
    test_df["surrogate_psnr_lowres"] = lowres_psnr
    test_df["surrogate_ssim_lowres"] = lowres_ssim
    test_df["guided_psnr_gain_over_fixed"] = test_df["guided_psnr"] - test_df["fixed_psnr"]
    test_df["surrogate_psnr_gain_over_fixed"] = test_df["surrogate_psnr_lowres"] - test_df["fixed_psnr"]
    test_df["surrogate_psnr_gap_to_guided"] = test_df["guided_psnr"] - test_df["surrogate_psnr_lowres"]

    summary = {
        "config": asdict(config),
        "train_samples": int(train_mask.sum()),
        "test_samples": int(test_mask.sum()),
        "mean_fixed_psnr": float(test_df["fixed_psnr"].mean()),
        "mean_guided_psnr": float(test_df["guided_psnr"].mean()),
        "mean_surrogate_psnr_lowres": float(test_df["surrogate_psnr_lowres"].mean()),
        "mean_fixed_psnr_lowres": float(test_df["fixed_psnr_lowres"].mean()),
        "mean_guided_psnr_lowres": float(test_df["guided_psnr_lowres"].mean()),
        "mean_fixed_ssim": float(test_df["fixed_ssim"].mean()),
        "mean_guided_ssim": float(test_df["guided_ssim"].mean()),
        "mean_surrogate_ssim_lowres": float(test_df["surrogate_ssim_lowres"].mean()),
        "mean_fixed_ssim_lowres": float(test_df["fixed_ssim_lowres"].mean()),
        "mean_guided_ssim_lowres": float(test_df["guided_ssim_lowres"].mean()),
        "mean_guided_psnr_gain_over_fixed": float(test_df["guided_psnr_gain_over_fixed"].mean()),
        "mean_surrogate_psnr_gain_over_fixed_lowres": float(
            (test_df["surrogate_psnr_lowres"] - test_df["fixed_psnr_lowres"]).mean()
        ),
        "mean_surrogate_psnr_gap_to_guided_lowres": float(
            (test_df["guided_psnr_lowres"] - test_df["surrogate_psnr_lowres"]).mean()
        ),
        "surrogate_better_than_fixed_fraction": float((test_df["surrogate_psnr_gain_over_fixed"] > 0).mean()),
    }
    test_df["surrogate_psnr_gain_over_fixed_lowres"] = test_df["surrogate_psnr_lowres"] - test_df["fixed_psnr_lowres"]
    test_df["surrogate_psnr_gap_to_guided_lowres"] = test_df["guided_psnr_lowres"] - test_df["surrogate_psnr_lowres"]
    test_df["surrogate_better_than_fixed_lowres"] = test_df["surrogate_psnr_gain_over_fixed_lowres"] > 0
    summary["surrogate_better_than_fixed_fraction"] = float(test_df["surrogate_better_than_fixed_lowres"].mean())

    test_df.to_csv(out_dir / "test_metrics.csv", index=False)
    pd.DataFrame(
        [
            {"metric": "fixed_psnr", "mean": test_df["fixed_psnr"].mean(), "std": test_df["fixed_psnr"].std()},
            {"metric": "guided_psnr", "mean": test_df["guided_psnr"].mean(), "std": test_df["guided_psnr"].std()},
            {
                "metric": "fixed_psnr_lowres",
                "mean": test_df["fixed_psnr_lowres"].mean(),
                "std": test_df["fixed_psnr_lowres"].std(),
            },
            {
                "metric": "guided_psnr_lowres",
                "mean": test_df["guided_psnr_lowres"].mean(),
                "std": test_df["guided_psnr_lowres"].std(),
            },
            {
                "metric": "surrogate_psnr_lowres",
                "mean": test_df["surrogate_psnr_lowres"].mean(),
                "std": test_df["surrogate_psnr_lowres"].std(),
            },
            {"metric": "fixed_ssim", "mean": test_df["fixed_ssim"].mean(), "std": test_df["fixed_ssim"].std()},
            {"metric": "guided_ssim", "mean": test_df["guided_ssim"].mean(), "std": test_df["guided_ssim"].std()},
            {
                "metric": "fixed_ssim_lowres",
                "mean": test_df["fixed_ssim_lowres"].mean(),
                "std": test_df["fixed_ssim_lowres"].std(),
            },
            {
                "metric": "guided_ssim_lowres",
                "mean": test_df["guided_ssim_lowres"].mean(),
                "std": test_df["guided_ssim_lowres"].std(),
            },
            {
                "metric": "surrogate_ssim_lowres",
                "mean": test_df["surrogate_ssim_lowres"].mean(),
                "std": test_df["surrogate_ssim_lowres"].std(),
            },
        ]
    ).to_csv(out_dir / "summary_table.csv", index=False)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    summary_md = f"""# Baseline 002 Summary

Goal: test a first trainable surrogate that consumes the distorted image together with the reference observation, without relying on any external deep-learning framework.

## Scope

- Training split: {config.train_case_count} aberration cases x 6 objects = {summary['train_samples']} samples
- Test split: {config.test_case_count} aberration cases x 6 objects = {summary['test_samples']} samples
- Surrogate type: linear ridge regression on low-resolution image and reference features
- Input features: low-resolution distorted image plus low-resolution reference PSF
- Output target: low-resolution restored image

## Test results

- Mean fixed PSNR at native resolution: {summary['mean_fixed_psnr']:.3f} dB
- Mean guided PSNR at native resolution: {summary['mean_guided_psnr']:.3f} dB
- Mean fixed PSNR at low resolution: {summary['mean_fixed_psnr_lowres']:.3f} dB
- Mean guided PSNR at low resolution: {summary['mean_guided_psnr_lowres']:.3f} dB
- Mean surrogate PSNR at low resolution: {summary['mean_surrogate_psnr_lowres']:.3f} dB
- Mean surrogate gain over fixed at low resolution: {summary['mean_surrogate_psnr_gain_over_fixed_lowres']:.3f} dB
- Mean gap from surrogate to guided at low resolution: {summary['mean_surrogate_psnr_gap_to_guided_lowres']:.3f} dB
- Surrogate better-than-fixed fraction: {summary['surrogate_better_than_fixed_fraction']:.3f}

## Interpretation boundary

This round tests learned calibration in the mildest possible form. The surrogate does beat the fixed baseline on held-out aberration cases, which supports the claim that reference information is learnable rather than only usable through explicit deconvolution. However, the training and test sets still share the same small object family and the surrogate is evaluated at low resolution, so this result should be treated as evidence for learnability, not yet as evidence for publishable optical generalization or the final passive diffractive implementation.

## Next executable step

Upgrade the surrogate from linear low-resolution regression to a differentiable optical-front-end approximation with stronger spatial capacity, while keeping the same train/test split and metrics ledger.
"""
    (out_dir / "summary.md").write_text(summary_md, encoding="utf-8")

    montage_rows = []
    for idx in range(min(4, len(pred_lowres))):
        gt = gt_lowres[idx].reshape(config.lowres_size, config.lowres_size)
        obs = features[test_mask][idx][: config.lowres_size * config.lowres_size].reshape(config.lowres_size, config.lowres_size)
        pred = pred_lowres[idx].reshape(config.lowres_size, config.lowres_size)
        montage_rows.append([gt, obs, pred])
    make_montage(montage_rows, ["ground_truth", "aberrated", "surrogate"], out_dir / "example_montage.png")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
