#!/usr/bin/env python3
"""Thicker statistics rerun for the fixed dual-heldout megadiverse phase-only setup."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

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
    lowres_size: int = 12
    layer_count: int = 5
    phase_basis_count: int = 10
    seed: int = 0
    train_case_count: int = 96
    heldout_case_count: int = 24
    ridge_lambda: float = 0.75
    search_steps: int = 14
    proposal_scale: float = 0.28
    wavelength: float = 532.0e-9
    sample_spacing: float = 8.0e-6
    propagation_distance: float = 12.0e-3
    noise_sigma: float = 0.01
    nominal_wiener_k: float = 1.0e-3
    guided_wiener_k: float = 5.0e-4
    propagation_model: str = "fresnel"


SEEDS = [0, 1, 2, 3, 4]


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


def make_heldout_objects(size: int) -> list[np.ndarray]:
    names = ["diag_x", "triangle", "checker_blocks", "crescent"]
    objects: list[np.ndarray] = []
    for name in names:
        canvas = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(canvas)
        if name == "diag_x":
            draw.line((20, 20, 108, 108), fill=255, width=12)
            draw.line((108, 20, 20, 108), fill=255, width=12)
        elif name == "triangle":
            draw.polygon([(64, 18), (22, 102), (106, 102)], fill=255)
        elif name == "checker_blocks":
            block = 18
            for ix in range(4):
                for iy in range(4):
                    if (ix + iy) % 2 == 0:
                        x0 = 24 + ix * block
                        y0 = 24 + iy * block
                        draw.rectangle((x0, y0, x0 + block - 4, y0 + block - 4), fill=255)
        elif name == "crescent":
            draw.ellipse((24, 24, 104, 104), fill=255)
            draw.ellipse((46, 24, 110, 96), fill=0)
        objects.append(np.asarray(canvas, dtype=np.float64) / 255.0)
    return objects


def make_megadiverse_training_objects(size: int) -> list[np.ndarray]:
    objects = list(make_objects(size))
    names = [
        "diamond","t_shape","frame","chevron","triple_dots","ladder","offcenter_ring","fork",
        "plus_disk","zigzag","two_boxes","hourglass","arch","bracket_pair","shifted_cross","quad_disks",
        "tilted_bar_pair","triangle_ring","donut_bar","staggered_blocks","y_shape","split_circle","notched_frame",
        "spiral_stub","offset_triplet","l_shape","u_shape","kite","double_chevron","windowpane",
        "bowtie","crosshair","pyramid_steps","three_rings","asymmetric_u","leaning_t","offset_frame",
        "hook_pair","barbell","trident","capsule_pair","double_window","offset_diamond","parallel_slashes"
    ]
    for name in names:
        canvas = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(canvas)
        if name == "diamond":
            draw.polygon([(64, 18), (104, 64), (64, 110), (24, 64)], fill=255)
        elif name == "t_shape":
            draw.rectangle((24, 22, 104, 42), fill=255); draw.rectangle((54, 22, 74, 106), fill=255)
        elif name == "frame":
            draw.rectangle((22, 22, 106, 106), outline=255, width=10)
        elif name == "chevron":
            draw.line((26, 40, 64, 84), fill=255, width=12); draw.line((64, 84, 102, 40), fill=255, width=12)
            draw.line((26, 76, 64, 112), fill=255, width=12); draw.line((64, 112, 102, 76), fill=255, width=12)
        elif name == "triple_dots":
            for x in [18, 52, 86]: draw.ellipse((x, 46, x + 24, 70), fill=255)
        elif name == "ladder":
            draw.rectangle((28, 20, 38, 108), fill=255); draw.rectangle((90, 20, 100, 108), fill=255)
            for y in [30, 48, 66, 84]: draw.rectangle((38, y, 90, y + 8), fill=255)
        elif name == "offcenter_ring":
            draw.ellipse((18, 28, 94, 104), outline=255, width=10); draw.ellipse((44, 44, 68, 68), fill=255)
        elif name == "fork":
            draw.rectangle((56, 24, 72, 108), fill=255); draw.rectangle((36, 20, 50, 54), fill=255); draw.rectangle((78, 20, 92, 54), fill=255)
        elif name == "plus_disk":
            draw.ellipse((34, 34, 94, 94), fill=255); draw.rectangle((56, 18, 72, 110), fill=255); draw.rectangle((18, 56, 110, 72), fill=255)
        elif name == "zigzag":
            draw.line([(20, 34), (48, 62), (34, 76), (62, 104), (90, 76), (76, 62), (104, 34)], fill=255, width=12)
        elif name == "two_boxes":
            draw.rectangle((22, 32, 54, 96), outline=255, width=8); draw.rectangle((74, 32, 106, 96), outline=255, width=8)
        elif name == "hourglass":
            draw.polygon([(28, 26), (54, 26), (76, 60), (98, 26), (100, 28), (76, 64), (100, 100), (98, 102), (76, 68), (54, 102), (28, 102), (52, 64)], fill=255)
        elif name == "arch":
            draw.arc((18, 20, 110, 108), start=180, end=360, fill=255, width=12); draw.rectangle((24, 62, 38, 108), fill=255); draw.rectangle((90, 62, 104, 108), fill=255)
        elif name == "bracket_pair":
            draw.rectangle((22, 24, 34, 106), fill=255); draw.rectangle((22, 24, 60, 36), fill=255); draw.rectangle((22, 94, 60, 106), fill=255)
            draw.rectangle((94, 24, 106, 106), fill=255); draw.rectangle((68, 24, 106, 36), fill=255); draw.rectangle((68, 94, 106, 106), fill=255)
        elif name == "shifted_cross":
            draw.rectangle((48, 14, 62, 104), fill=255); draw.rectangle((18, 50, 98, 64), fill=255); draw.rectangle((74, 34, 90, 116), fill=255)
        elif name == "quad_disks":
            for x0, y0 in [(20, 20), (72, 20), (20, 72), (72, 72)]: draw.ellipse((x0, y0, x0 + 28, y0 + 28), fill=255)
        elif name == "tilted_bar_pair":
            draw.polygon([(26, 92), (38, 84), (86, 24), (74, 16)], fill=255); draw.polygon([(54, 108), (66, 100), (112, 42), (100, 34)], fill=255)
        elif name == "triangle_ring":
            draw.polygon([(64, 18), (20, 102), (108, 102)], outline=255, width=10)
        elif name == "donut_bar":
            draw.ellipse((24, 24, 104, 104), outline=255, width=12); draw.rectangle((56, 16, 72, 112), fill=255)
        elif name == "staggered_blocks":
            for x, y in [(18, 28), (42, 52), (66, 28), (90, 52)]: draw.rectangle((x, y, x + 18, y + 34), fill=255)
        elif name == "y_shape":
            draw.line((64, 56, 64, 108), fill=255, width=12); draw.line((64, 56, 34, 24), fill=255, width=12); draw.line((64, 56, 94, 24), fill=255, width=12)
        elif name == "split_circle":
            draw.ellipse((24, 24, 104, 104), fill=255); draw.rectangle((60, 18, 68, 110), fill=0)
        elif name == "notched_frame":
            draw.rectangle((18, 18, 110, 110), outline=255, width=10); draw.rectangle((52, 18, 76, 42), fill=0)
        elif name == "spiral_stub":
            draw.arc((24, 24, 104, 104), start=20, end=320, fill=255, width=12); draw.line((72, 62, 92, 62), fill=255, width=12)
        elif name == "offset_triplet":
            draw.rectangle((18, 24, 36, 104), fill=255); draw.rectangle((54, 16, 72, 96), fill=255); draw.rectangle((90, 30, 108, 110), fill=255)
        elif name == "l_shape":
            draw.rectangle((24, 20, 42, 108), fill=255); draw.rectangle((24, 90, 96, 108), fill=255)
        elif name == "u_shape":
            draw.rectangle((22, 20, 40, 108), fill=255); draw.rectangle((88, 20, 106, 108), fill=255); draw.rectangle((22, 90, 106, 108), fill=255)
        elif name == "kite":
            draw.polygon([(64, 12), (96, 60), (64, 116), (32, 60)], fill=255)
        elif name == "double_chevron":
            draw.line((18, 34, 52, 64), fill=255, width=10); draw.line((52, 64, 18, 94), fill=255, width=10)
            draw.line((76, 34, 110, 64), fill=255, width=10); draw.line((110, 64, 76, 94), fill=255, width=10)
        elif name == "windowpane":
            draw.rectangle((24, 24, 104, 104), outline=255, width=10); draw.rectangle((60, 24, 68, 104), fill=255); draw.rectangle((24, 60, 104, 68), fill=255)
        elif name == "bowtie":
            draw.polygon([(22, 24), (62, 62), (22, 100), (42, 100), (74, 68), (106, 100), (106, 24), (74, 56), (42, 24)], fill=255)
        elif name == "crosshair":
            draw.rectangle((58, 16, 70, 112), fill=255); draw.rectangle((16, 58, 112, 70), fill=255); draw.ellipse((44, 44, 84, 84), outline=0, width=10)
        elif name == "pyramid_steps":
            for x0, y0, x1, y1 in [(18,90,110,108),(28,72,100,90),(38,54,90,72),(48,36,80,54)]: draw.rectangle((x0,y0,x1,y1), fill=255)
        elif name == "three_rings":
            for box in [(14,14,54,54),(44,44,84,84),(74,74,114,114)]: draw.ellipse(box, outline=255, width=8)
        elif name == "asymmetric_u":
            draw.rectangle((20, 20, 34, 108), fill=255); draw.rectangle((80, 36, 98, 108), fill=255); draw.rectangle((20, 92, 98, 108), fill=255)
        elif name == "leaning_t":
            draw.polygon([(24,24),(102,18),(104,34),(26,40)], fill=255); draw.polygon([(52,24),(68,22),(82,108),(66,110)], fill=255)
        elif name == "offset_frame":
            draw.rectangle((18,18,100,100), outline=255, width=10); draw.rectangle((42,42,110,110), outline=255, width=10)
        elif name == "hook_pair":
            draw.rectangle((22,20,38,92), fill=255); draw.rectangle((22,76,74,92), fill=255); draw.rectangle((90,36,106,108), fill=255); draw.rectangle((54,36,106,52), fill=255)
        elif name == "barbell":
            draw.ellipse((18,42,50,74), fill=255); draw.ellipse((78,42,110,74), fill=255); draw.rectangle((42,52,86,64), fill=255)
        elif name == "trident":
            for x in [34,62,90]: draw.rectangle((x,20,x+12,62), fill=255)
            draw.rectangle((58,62,70,108), fill=255)
        elif name == "capsule_pair":
            draw.rounded_rectangle((18,30,54,98), radius=18, fill=255); draw.rounded_rectangle((74,30,110,98), radius=18, fill=255)
        elif name == "double_window":
            draw.rectangle((18,18,110,110), outline=255, width=10); draw.rectangle((46,18,58,110), fill=255); draw.rectangle((70,18,82,110), fill=255)
        elif name == "offset_diamond":
            draw.polygon([(52,14),(88,54),(52,94),(16,54)], fill=255); draw.polygon([(78,34),(112,68),(78,102),(44,68)], fill=255)
        elif name == "parallel_slashes":
            for shift in [0, 28, 56]: draw.polygon([(18+shift,96),(30+shift,88),(78+shift,24),(66+shift,16)], fill=255)
        objects.append(np.asarray(canvas, dtype=np.float64) / 255.0)
    return objects


def make_phase_basis(size: int, count: int) -> np.ndarray:
    axis = np.linspace(-1.0, 1.0, size, endpoint=False)
    xx, yy = np.meshgrid(axis, axis)
    basis = [
        np.sin(np.pi * xx), np.sin(np.pi * yy), np.cos(np.pi * xx), np.cos(np.pi * yy),
        np.sin(np.pi * (xx + yy)), np.sin(np.pi * (xx - yy)),
        np.cos(2.0 * np.pi * xx), np.cos(2.0 * np.pi * yy),
        np.sin(2.0 * np.pi * (xx + yy)), np.sin(2.0 * np.pi * (xx - yy)),
    ]
    return np.asarray(basis[:count], dtype=np.float64)


def phase_masks_from_coeffs(coeffs: np.ndarray, basis: np.ndarray) -> np.ndarray:
    return np.asarray([np.exp(1j * np.pi * np.tanh(np.tensordot(layer_coeffs, basis, axes=(0, 0)))) for layer_coeffs in coeffs])


def propagate_phase_frontend(noisy_lowres: np.ndarray, reference_lowres: np.ndarray, masks: np.ndarray, propagation: PropagationConfig) -> list[np.ndarray]:
    amplitude = np.sqrt(np.clip(0.8 * noisy_lowres + 0.2 * reference_lowres, 0.0, 1.0) + 1.0e-8)
    field = amplitude.astype(np.complex128)
    outputs = []
    for mask in masks:
        field = propagate_fresnel(field * mask, propagation)
        intensity = np.abs(field) ** 2
        outputs.append(intensity / (intensity.max() + 1.0e-8))
    return outputs


def make_aberration_cases(case_count: int, seed: int) -> list[dict[str, float]]:
    rng = np.random.default_rng(seed)
    return [{"defocus": float(rng.uniform(-1.5, 1.5)), "astig_x": float(rng.uniform(-1.0, 1.0)), "coma_x": float(rng.uniform(-0.8, 0.8))} for _ in range(case_count)]


def build_split_samples(objects: list[np.ndarray], object_split: str, cases: list[dict[str, float]], config: PhaseOnlyConfig) -> list[dict[str, object]]:
    lowres_objects = [downsample(obj, config.lowres_size) for obj in objects]
    nominal_psf = make_psf(config.pupil_size, {"defocus": 0.0, "astig_x": 0.0, "coma_x": 0.0, "_sample_spacing": config.sample_spacing, "_wavelength": config.wavelength, "_propagation_distance": config.propagation_distance, "_propagation_model": config.propagation_model})
    samples = []
    rng = np.random.default_rng(config.seed + (0 if object_split == "train" else 1000))
    for case_id, coeffs in enumerate(cases):
        psf = make_psf(config.pupil_size, {**coeffs, "_sample_spacing": config.sample_spacing, "_wavelength": config.wavelength, "_propagation_distance": config.propagation_distance, "_propagation_model": config.propagation_model})
        reference_lowres = downsample(psf, config.lowres_size)
        for object_id, (obj_native, obj_lowres) in enumerate(zip(objects, lowres_objects)):
            blurred = fft_convolve(obj_native, psf)
            noisy = np.clip(blurred + rng.normal(0.0, config.noise_sigma, blurred.shape), 0.0, 1.0)
            fixed_restore = wiener_deconvolution(noisy, nominal_psf, config.nominal_wiener_k)
            guided_restore = wiener_deconvolution(noisy, psf, config.guided_wiener_k)
            samples.append({
                "split": object_split, "case_id": case_id, "object_id": f"{object_split}_object_{object_id:02d}",
                "defocus": coeffs["defocus"], "astig_x": coeffs["astig_x"], "coma_x": coeffs["coma_x"],
                "gt_lowres": obj_lowres, "noisy_lowres": downsample(noisy, config.lowres_size), "reference_lowres": reference_lowres,
                "fixed_psnr_lowres": psnr(obj_lowres, downsample(fixed_restore, config.lowres_size)),
                "guided_psnr_lowres": psnr(obj_lowres, downsample(guided_restore, config.lowres_size)),
                "fixed_ssim_lowres": ssim_simple(obj_lowres, downsample(fixed_restore, config.lowres_size)),
                "guided_ssim_lowres": ssim_simple(obj_lowres, downsample(guided_restore, config.lowres_size)),
            })
    return samples


def build_features(samples: list[dict[str, object]], masks: np.ndarray, propagation: PropagationConfig) -> np.ndarray:
    rows = []
    for sample in samples:
        outputs = propagate_phase_frontend(sample["noisy_lowres"], sample["reference_lowres"], masks, propagation)
        rows.append(np.concatenate([sample["noisy_lowres"].reshape(-1), sample["reference_lowres"].reshape(-1), *(out.reshape(-1) for out in outputs)]))
    return np.asarray(rows)


def build_targets(samples: list[dict[str, object]]) -> np.ndarray:
    return np.asarray([sample["gt_lowres"].reshape(-1) for sample in samples])


def fit_ridge_regression(x_train: np.ndarray, y_train: np.ndarray, ridge_lambda: float) -> np.ndarray:
    x_aug = np.concatenate([x_train, np.ones((x_train.shape[0], 1))], axis=1)
    xtx = x_aug.T @ x_aug
    regularizer = ridge_lambda * np.eye(xtx.shape[0]); regularizer[-1, -1] = 0.0
    return np.linalg.solve(xtx + regularizer, x_aug.T @ y_train)


def predict_ridge(x: np.ndarray, weights: np.ndarray) -> np.ndarray:
    x_aug = np.concatenate([x, np.ones((x.shape[0], 1))], axis=1)
    return np.clip(x_aug @ weights, 0.0, 1.0)


def evaluate_training_objective(coeffs: np.ndarray, basis: np.ndarray, train_samples: list[dict[str, object]], propagation: PropagationConfig, ridge_lambda: float) -> float:
    masks = phase_masks_from_coeffs(coeffs, basis)
    x_train = build_features(train_samples, masks, propagation)
    y_train = build_targets(train_samples)
    weights = fit_ridge_regression(x_train, y_train, ridge_lambda)
    prediction = predict_ridge(x_train, weights)
    return float(np.mean((prediction - y_train) ** 2))


def optimize_phase_coeffs(config: PhaseOnlyConfig, basis: np.ndarray, train_samples: list[dict[str, object]], propagation: PropagationConfig) -> np.ndarray:
    rng = np.random.default_rng(config.seed)
    coeffs = rng.normal(0.0, 0.12, size=(config.layer_count, config.phase_basis_count))
    best_loss = evaluate_training_objective(coeffs, basis, train_samples, propagation, config.ridge_lambda)
    step = config.proposal_scale
    for _ in range(config.search_steps):
        direction = rng.normal(0.0, 1.0, size=coeffs.shape)
        for candidate in (coeffs + step * direction, coeffs - step * direction):
            loss = evaluate_training_objective(candidate, basis, train_samples, propagation, config.ridge_lambda)
            if loss < best_loss:
                coeffs = candidate
                best_loss = loss
        step *= 0.88
    return coeffs


def evaluate_protocol(samples: list[dict[str, object]], prediction: np.ndarray, config: PhaseOnlyConfig, seed: int, protocol_name: str) -> tuple[pd.DataFrame, dict[str, float]]:
    rows = []
    for idx, sample in enumerate(samples):
        pred = prediction[idx].reshape(config.lowres_size, config.lowres_size)
        phase_psnr = psnr(sample["gt_lowres"], pred)
        phase_ssim = ssim_simple(sample["gt_lowres"], pred)
        rows.append({
            "seed": seed, "protocol": protocol_name, "case_id": sample["case_id"], "object_id": sample["object_id"], "split": sample["split"],
            "defocus": sample["defocus"], "astig_x": sample["astig_x"], "coma_x": sample["coma_x"],
            "fixed_psnr_lowres": sample["fixed_psnr_lowres"], "guided_psnr_lowres": sample["guided_psnr_lowres"], "phaseonly_psnr_lowres": phase_psnr,
            "fixed_ssim_lowres": sample["fixed_ssim_lowres"], "guided_ssim_lowres": sample["guided_ssim_lowres"], "phaseonly_ssim_lowres": phase_ssim,
            "phaseonly_psnr_gain_over_fixed_lowres": phase_psnr - sample["fixed_psnr_lowres"],
            "phaseonly_psnr_gap_to_guided_lowres": sample["guided_psnr_lowres"] - phase_psnr,
            "phaseonly_ssim_gain_over_fixed_lowres": phase_ssim - sample["fixed_ssim_lowres"],
        })
    df = pd.DataFrame(rows)
    summary = {
        "seed": seed, "protocol": protocol_name,
        "mean_fixed_psnr_lowres": float(df["fixed_psnr_lowres"].mean()),
        "mean_guided_psnr_lowres": float(df["guided_psnr_lowres"].mean()),
        "mean_phaseonly_psnr_lowres": float(df["phaseonly_psnr_lowres"].mean()),
        "mean_phaseonly_psnr_gain_over_fixed_lowres": float(df["phaseonly_psnr_gain_over_fixed_lowres"].mean()),
        "mean_phaseonly_psnr_gap_to_guided_lowres": float(df["phaseonly_psnr_gap_to_guided_lowres"].mean()),
        "mean_fixed_ssim_lowres": float(df["fixed_ssim_lowres"].mean()),
        "mean_guided_ssim_lowres": float(df["guided_ssim_lowres"].mean()),
        "mean_phaseonly_ssim_lowres": float(df["phaseonly_ssim_lowres"].mean()),
        "mean_phaseonly_ssim_gain_over_fixed_lowres": float(df["phaseonly_ssim_gain_over_fixed_lowres"].mean()),
        "phaseonly_better_than_fixed_fraction": float((df["phaseonly_psnr_gain_over_fixed_lowres"] > 0.0).mean()),
    }
    return df, summary


def run_seed(config: PhaseOnlyConfig) -> tuple[dict[str, tuple[pd.DataFrame, dict[str, float]]], dict[str, float]]:
    train_objects = make_megadiverse_training_objects(config.image_size)
    object_family_heldout = make_heldout_objects(config.image_size)
    same_family_eval_objects = make_objects(config.image_size)
    train_cases = make_aberration_cases(config.train_case_count, config.seed)
    heldout_cases = make_aberration_cases(config.heldout_case_count, config.seed + 500)

    train_samples = build_split_samples(train_objects, "train", train_cases, config)
    same_family_samples = build_split_samples(same_family_eval_objects, "heldout_aberration", heldout_cases, config)
    new_family_samples = build_split_samples(object_family_heldout, "heldout_object_family", heldout_cases, config)

    basis = make_phase_basis(config.lowres_size, config.phase_basis_count)
    frontend_spacing = config.sample_spacing * config.image_size / config.lowres_size
    propagation = PropagationConfig(grid_size=config.lowres_size, sample_spacing=frontend_spacing, wavelength=config.wavelength, propagation_distance=config.propagation_distance)

    coeffs = optimize_phase_coeffs(config, basis, train_samples, propagation)
    masks = phase_masks_from_coeffs(coeffs, basis)
    x_train = build_features(train_samples, masks, propagation)
    y_train = build_targets(train_samples)
    weights = fit_ridge_regression(x_train, y_train, config.ridge_lambda)

    same_prediction = predict_ridge(build_features(same_family_samples, masks, propagation), weights)
    new_prediction = predict_ridge(build_features(new_family_samples, masks, propagation), weights)

    protocol_outputs = {
        "same_family_heldout_aberration": evaluate_protocol(same_family_samples, same_prediction, config, config.seed, "same_family_heldout_aberration"),
        "new_family_heldout_object_family": evaluate_protocol(new_family_samples, new_prediction, config, config.seed, "new_family_heldout_object_family"),
    }

    fx, fy = frequency_coordinates(propagation)
    shared_metadata = {
        "seed": config.seed, "layer_count": config.layer_count, "phase_basis_count": config.phase_basis_count, "lowres_size": config.lowres_size,
        "training_object_family_count": len(train_objects), "same_family_eval_count": len(same_family_eval_objects), "new_family_eval_count": len(object_family_heldout),
        "heldout_case_count": config.heldout_case_count,
        "wavelength_m": config.wavelength, "sample_spacing_m_native": config.sample_spacing, "sample_spacing_m_frontend": frontend_spacing,
        "propagation_distance_m": config.propagation_distance, "fx_min_1_per_m": float(fx.min()), "fx_max_1_per_m": float(fx.max()), "fy_min_1_per_m": float(fy.min()), "fy_max_1_per_m": float(fy.max()),
    }
    return protocol_outputs, shared_metadata


def write_protocol_log(log_path: Path, shared: dict[str, float], protocol_summary: dict[str, float]) -> None:
    log_path.write_text("\n".join([
        f"seed={shared['seed']}", f"protocol={protocol_summary['protocol']}", "propagation_model=fresnel", "fresnel_transfer_function=exp(-i*pi*lambda*z*(fx^2+fy^2))",
        f"layer_count={shared['layer_count']}", f"phase_basis_count={shared['phase_basis_count']}", f"lowres_size={shared['lowres_size']}",
        f"training_object_family_count={shared['training_object_family_count']}", f"same_family_eval_count={shared['same_family_eval_count']}", f"new_family_eval_count={shared['new_family_eval_count']}",
        f"heldout_case_count={shared['heldout_case_count']}",
        f"wavelength_m={shared['wavelength_m']}", f"sample_spacing_m_native={shared['sample_spacing_m_native']}", f"sample_spacing_m_frontend={shared['sample_spacing_m_frontend']}", f"propagation_distance_m={shared['propagation_distance_m']}",
        f"fx_min_1_per_m={shared['fx_min_1_per_m']}", f"fx_max_1_per_m={shared['fx_max_1_per_m']}", f"fy_min_1_per_m={shared['fy_min_1_per_m']}", f"fy_max_1_per_m={shared['fy_max_1_per_m']}",
        f"mean_phaseonly_psnr_lowres={protocol_summary['mean_phaseonly_psnr_lowres']}", f"mean_phaseonly_ssim_lowres={protocol_summary['mean_phaseonly_ssim_lowres']}", f"phaseonly_psnr_gain_over_fixed_lowres={protocol_summary['mean_phaseonly_psnr_gain_over_fixed_lowres']}", f"phaseonly_better_than_fixed_fraction={protocol_summary['phaseonly_better_than_fixed_fraction']}",
    ]) + "\n", encoding="utf-8")


def write_protocol_summary(summary_path: Path, per_seed_df: pd.DataFrame) -> None:
    rows = []
    for metric in ["mean_fixed_psnr_lowres", "mean_guided_psnr_lowres", "mean_phaseonly_psnr_lowres", "mean_phaseonly_psnr_gain_over_fixed_lowres", "mean_phaseonly_psnr_gap_to_guided_lowres", "mean_fixed_ssim_lowres", "mean_guided_ssim_lowres", "mean_phaseonly_ssim_lowres", "mean_phaseonly_ssim_gain_over_fixed_lowres", "phaseonly_better_than_fixed_fraction"]:
        values = per_seed_df[metric].to_numpy(dtype=float)
        mean, ci95 = confidence_interval_95(values)
        rows.append({"metric": metric, "mean": mean, "std": float(values.std(ddof=1)), "ci95_half_width": ci95, "seed_count": len(values)})
    pd.DataFrame(rows).to_csv(summary_path, index=False)


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "results" / "baselines" / "baseline-009-phaseonly-megadiverse-thickstats"
    out_dir.mkdir(parents=True, exist_ok=True)
    protocol_names = ["same_family_heldout_aberration", "new_family_heldout_object_family"]
    protocol_dirs = {name: out_dir / name for name in protocol_names}
    for path in protocol_dirs.values():
        path.mkdir(parents=True, exist_ok=True)

    build_optics_metadata(SimulationConfig(wavelength=532.0e-9, sample_spacing=8.0e-6, propagation_distance=12.0e-3, propagation_model="fresnel"))
    generated_by_protocol = {name: [] for name in protocol_names}
    per_seed_summaries = {name: [] for name in protocol_names}

    for seed in SEEDS:
        config = PhaseOnlyConfig(seed=seed)
        protocol_outputs, shared = run_seed(config)
        for protocol_name, (df, summary) in protocol_outputs.items():
            protocol_dir = protocol_dirs[protocol_name]
            metrics_path = protocol_dir / f"heldout_metrics_seed{seed}.csv"
            log_path = protocol_dir / f"run_log_seed_{seed}.txt"
            df.to_csv(metrics_path, index=False)
            write_protocol_log(log_path, shared, summary)
            generated_by_protocol[protocol_name].extend([metrics_path, log_path])
            per_seed_summaries[protocol_name].append(summary)

    for protocol_name in protocol_names:
        protocol_dir = protocol_dirs[protocol_name]
        summary_path = protocol_dir / "multiseed_summary.csv"
        write_protocol_summary(summary_path, pd.DataFrame(per_seed_summaries[protocol_name]))
        generated_by_protocol[protocol_name].append(summary_path)
        write_sha256_manifest(generated_by_protocol[protocol_name], protocol_dir / "sha256_manifest.txt")

    print(json.dumps({
        "output_dir": str(out_dir),
        "seeds": SEEDS,
        "protocols": protocol_names,
        "training_object_family_count": 50,
        "layer_count": 5,
        "phase_basis_count": 10,
        "lowres_size": 12,
        "heldout_case_count": 24,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
