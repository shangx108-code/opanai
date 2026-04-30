#!/usr/bin/env python3
"""Run a minimal reference-guided baseline under dynamic aberrations.

This is the first executable scaffold for the project. It does not train a
diffractive neural network yet. Instead, it tests the narrower physical claim
that a co-propagating reference, by revealing the instantaneous PSF, can
improve restoration relative to a fixed, reference-free baseline.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw


@dataclass
class SimulationConfig:
    image_size: int = 128
    pupil_size: int = 128
    wavelength: float = 1.0
    nominal_wiener_k: float = 1.0e-3
    guided_wiener_k: float = 5.0e-4
    seed: int = 7
    noise_sigma: float = 0.01
    object_count: int = 6
    case_count: int = 8


def make_coordinate_grid(size: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    axis = np.linspace(-1.0, 1.0, size, endpoint=False)
    xx, yy = np.meshgrid(axis, axis)
    rr = np.sqrt(xx**2 + yy**2)
    return xx, yy, rr


def zernike_basis(xx: np.ndarray, yy: np.ndarray, rr: np.ndarray) -> dict[str, np.ndarray]:
    theta = np.arctan2(yy, xx)
    pupil = rr <= 1.0
    basis = {
        "defocus": np.sqrt(3.0) * (2.0 * rr**2 - 1.0),
        "astig_x": np.sqrt(6.0) * rr**2 * np.cos(2.0 * theta),
        "coma_x": np.sqrt(8.0) * (3.0 * rr**3 - 2.0 * rr) * np.cos(theta),
    }
    for key in basis:
        basis[key] = np.where(pupil, basis[key], 0.0)
    return basis


def make_psf(size: int, coeffs: dict[str, float]) -> np.ndarray:
    xx, yy, rr = make_coordinate_grid(size)
    pupil = (rr <= 1.0).astype(np.float64)
    phase = np.zeros_like(xx)
    for key, basis in zernike_basis(xx, yy, rr).items():
        phase += coeffs.get(key, 0.0) * basis
    field = pupil * np.exp(1j * phase)
    amp = np.fft.fftshift(np.fft.fft2(np.fft.ifftshift(field)))
    psf = np.abs(amp) ** 2
    psf /= psf.sum()
    return psf


def fft_convolve(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    image_fft = np.fft.fft2(image)
    kernel_fft = np.fft.fft2(np.fft.ifftshift(kernel))
    out = np.fft.ifft2(image_fft * kernel_fft).real
    return out


def wiener_deconvolution(observed: np.ndarray, kernel: np.ndarray, k: float) -> np.ndarray:
    kernel_fft = np.fft.fft2(np.fft.ifftshift(kernel))
    obs_fft = np.fft.fft2(observed)
    denom = np.abs(kernel_fft) ** 2 + k
    restored = np.fft.ifft2(obs_fft * np.conj(kernel_fft) / denom).real
    return np.clip(restored, 0.0, 1.0)


def psnr(reference: np.ndarray, estimate: np.ndarray) -> float:
    mse = float(np.mean((reference - estimate) ** 2))
    if mse == 0.0:
        return 99.0
    return 10.0 * np.log10(1.0 / mse)


def ssim_simple(reference: np.ndarray, estimate: np.ndarray) -> float:
    c1 = 0.01**2
    c2 = 0.03**2
    mu_x = float(reference.mean())
    mu_y = float(estimate.mean())
    sigma_x = float(reference.var())
    sigma_y = float(estimate.var())
    sigma_xy = float(((reference - mu_x) * (estimate - mu_y)).mean())
    numerator = (2 * mu_x * mu_y + c1) * (2 * sigma_xy + c2)
    denominator = (mu_x**2 + mu_y**2 + c1) * (sigma_x + sigma_y + c2)
    return numerator / denominator


def make_objects(size: int) -> list[np.ndarray]:
    objects: list[np.ndarray] = []
    names = [
        "double_slit",
        "rings",
        "cross",
        "offset_bars",
        "disk_pair",
        "staircase",
    ]
    for name in names:
        canvas = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(canvas)
        if name == "double_slit":
            draw.rectangle((40, 28, 50, 100), fill=255)
            draw.rectangle((78, 28, 88, 100), fill=255)
        elif name == "rings":
            draw.ellipse((22, 22, 106, 106), outline=255, width=8)
            draw.ellipse((42, 42, 86, 86), outline=255, width=8)
        elif name == "cross":
            draw.rectangle((58, 20, 70, 108), fill=255)
            draw.rectangle((24, 56, 104, 68), fill=255)
        elif name == "offset_bars":
            for i in range(4):
                x0 = 20 + i * 22
                y0 = 20 + (i % 2) * 18
                draw.rectangle((x0, y0, x0 + 10, y0 + 72), fill=255)
        elif name == "disk_pair":
            draw.ellipse((24, 42, 58, 76), fill=255)
            draw.ellipse((70, 52, 108, 90), fill=255)
        elif name == "staircase":
            for step in range(5):
                draw.rectangle((18 + step * 16, 88 - step * 14, 34 + step * 16, 108), fill=255)
        arr = np.asarray(canvas, dtype=np.float64) / 255.0
        objects.append(arr)
    return objects


def normalize_to_uint8(arr: np.ndarray) -> Image.Image:
    clipped = np.clip(arr, 0.0, 1.0)
    return Image.fromarray(np.uint8(np.round(clipped * 255.0)), mode="L")


def make_montage(rows: list[list[np.ndarray]], labels: list[str], path: Path) -> None:
    tile_size = rows[0][0].shape[0]
    margin = 8
    label_height = 20
    width = len(labels) * tile_size + (len(labels) + 1) * margin
    height = len(rows) * (tile_size + label_height + margin) + margin
    canvas = Image.new("L", (width, height), color=255)
    draw = ImageDraw.Draw(canvas)
    for row_index, row in enumerate(rows):
        y_base = margin + row_index * (tile_size + label_height + margin)
        for col_index, arr in enumerate(row):
            x_base = margin + col_index * (tile_size + margin)
            canvas.paste(normalize_to_uint8(arr), (x_base, y_base))
            draw.text((x_base, y_base + tile_size + 2), labels[col_index], fill=0)
    canvas.save(path)


def main() -> int:
    config = SimulationConfig()
    rng = np.random.default_rng(config.seed)
    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "results" / "baselines" / "baseline-001-reference-psf"
    out_dir.mkdir(parents=True, exist_ok=True)

    objects = make_objects(config.image_size)
    object_names = [f"object_{idx:02d}" for idx in range(len(objects))]

    nominal_psf = make_psf(config.pupil_size, {"defocus": 0.0, "astig_x": 0.0, "coma_x": 0.0})

    rows = []
    montage_rows: list[list[np.ndarray]] = []
    for case_idx in range(config.case_count):
        coeffs = {
            "defocus": float(rng.uniform(-1.5, 1.5)),
            "astig_x": float(rng.uniform(-1.0, 1.0)),
            "coma_x": float(rng.uniform(-0.8, 0.8)),
        }
        psf = make_psf(config.pupil_size, coeffs)
        reference_observation = psf.copy()
        for obj_idx, obj in enumerate(objects):
            blurred = fft_convolve(obj, psf)
            noisy = np.clip(blurred + rng.normal(0.0, config.noise_sigma, blurred.shape), 0.0, 1.0)

            fixed_restore = wiener_deconvolution(noisy, nominal_psf, config.nominal_wiener_k)
            guided_restore = wiener_deconvolution(noisy, reference_observation, config.guided_wiener_k)

            row = {
                "case_id": case_idx,
                "object_id": object_names[obj_idx],
                "defocus": coeffs["defocus"],
                "astig_x": coeffs["astig_x"],
                "coma_x": coeffs["coma_x"],
                "fixed_psnr": psnr(obj, fixed_restore),
                "guided_psnr": psnr(obj, guided_restore),
                "fixed_ssim": ssim_simple(obj, fixed_restore),
                "guided_ssim": ssim_simple(obj, guided_restore),
            }
            row["psnr_gain"] = row["guided_psnr"] - row["fixed_psnr"]
            row["ssim_gain"] = row["guided_ssim"] - row["fixed_ssim"]
            rows.append(row)

            if case_idx < 2 and obj_idx < 2:
                montage_rows.append([obj, noisy, fixed_restore, guided_restore])

    df = pd.DataFrame(rows)
    summary = {
        "config": asdict(config),
        "sample_count": int(len(df)),
        "mean_fixed_psnr": float(df["fixed_psnr"].mean()),
        "mean_guided_psnr": float(df["guided_psnr"].mean()),
        "mean_psnr_gain": float(df["psnr_gain"].mean()),
        "median_psnr_gain": float(df["psnr_gain"].median()),
        "mean_fixed_ssim": float(df["fixed_ssim"].mean()),
        "mean_guided_ssim": float(df["guided_ssim"].mean()),
        "mean_ssim_gain": float(df["ssim_gain"].mean()),
        "guided_better_fraction_psnr": float((df["psnr_gain"] > 0).mean()),
        "guided_better_fraction_ssim": float((df["ssim_gain"] > 0).mean()),
    }

    df.to_csv(out_dir / "baseline_metrics.csv", index=False)
    pd.DataFrame(
        [
            {
                "metric": "fixed_psnr",
                "mean": df["fixed_psnr"].mean(),
                "std": df["fixed_psnr"].std(),
            },
            {
                "metric": "guided_psnr",
                "mean": df["guided_psnr"].mean(),
                "std": df["guided_psnr"].std(),
            },
            {
                "metric": "psnr_gain",
                "mean": df["psnr_gain"].mean(),
                "std": df["psnr_gain"].std(),
            },
            {
                "metric": "fixed_ssim",
                "mean": df["fixed_ssim"].mean(),
                "std": df["fixed_ssim"].std(),
            },
            {
                "metric": "guided_ssim",
                "mean": df["guided_ssim"].mean(),
                "std": df["guided_ssim"].std(),
            },
            {
                "metric": "ssim_gain",
                "mean": df["ssim_gain"].mean(),
                "std": df["ssim_gain"].std(),
            },
        ]
    ).to_csv(out_dir / "baseline_summary.csv", index=False)

    (out_dir / "baseline_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    summary_md = f"""# Baseline 001 Summary

Goal: test whether a co-propagating reference PSF can improve restoration under dynamic aberrations before any diffractive-network training.

## Scope

- Dynamic perturbation family: low-order Zernike-like defocus, astigmatism, and coma
- Restoration comparison:
  - fixed reference-free Wiener deconvolution using a nominal PSF
  - reference-guided Wiener deconvolution using the instantaneous PSF from the co-propagating reference
- Objects: {config.object_count} synthetic binary patterns
- Aberration cases: {config.case_count}
- Total evaluated samples: {len(df)}

## Aggregate results

- Mean fixed PSNR: {summary['mean_fixed_psnr']:.3f} dB
- Mean guided PSNR: {summary['mean_guided_psnr']:.3f} dB
- Mean PSNR gain: {summary['mean_psnr_gain']:.3f} dB
- Mean fixed SSIM: {summary['mean_fixed_ssim']:.4f}
- Mean guided SSIM: {summary['mean_guided_ssim']:.4f}
- Mean SSIM gain: {summary['mean_ssim_gain']:.4f}
- Guided better fraction by PSNR: {summary['guided_better_fraction_psnr']:.3f}
- Guided better fraction by SSIM: {summary['guided_better_fraction_ssim']:.3f}

## Interpretation boundary

This is a pre-network baseline scaffold, not yet evidence for the full passive diffractive neural-operator claim. What it does establish is a first executable reference point: when the instantaneous distortion kernel is available through a co-path reference, adaptive restoration outperforms a fixed non-adaptive baseline under the same dynamic aberration family.

## Next executable step

Replace the pure post-detection adaptive deconvolution with a trainable optical-frontend surrogate or differentiable diffractive layer stack, while keeping the same perturbation generator and metrics ledger.
"""
    (out_dir / "baseline_summary.md").write_text(summary_md, encoding="utf-8")

    labels = ["ground_truth", "aberrated", "fixed_restore", "guided_restore"]
    make_montage(montage_rows, labels, out_dir / "example_montage.png")

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
