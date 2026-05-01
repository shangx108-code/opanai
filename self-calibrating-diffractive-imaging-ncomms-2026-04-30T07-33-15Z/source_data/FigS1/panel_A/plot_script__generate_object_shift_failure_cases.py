#!/usr/bin/env python3
"""Generate representative phase-only failure cases under object-family shift."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw

from optics_propagation import PropagationConfig
from run_baseline_phase_only_megadiverse_train_dual_heldout_thickstats import (
    PhaseOnlyConfig,
    build_features,
    build_targets,
    fit_ridge_regression,
    make_aberration_cases,
    make_heldout_objects,
    make_megadiverse_training_objects,
    make_phase_basis,
    make_psf,
    normalize_to_uint8,
    optimize_phase_coeffs,
    phase_masks_from_coeffs,
    predict_ridge,
    downsample,
    fft_convolve,
    psnr,
    wiener_deconvolution,
)


OBJECT_LABELS = {
    "heldout_object_family_object_00": "diag_x",
    "heldout_object_family_object_01": "triangle",
    "heldout_object_family_object_02": "checker_blocks",
    "heldout_object_family_object_03": "crescent",
}

FAILURE_REASON = {
    "heldout_object_family_object_00": "thin diagonal crossings concentrate oblique high-frequency content that is weakened by the 12x12 low-resolution frontend",
    "heldout_object_family_object_02": "periodic block structure creates alias-prone repeated edges and boundary leakage under object-family shift",
    "heldout_object_family_object_03": "curved asymmetric boundaries and hollow subtraction yield mixed low-contrast edge errors after the learned optical encoding",
}


def rich_build_split_samples(
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
    rng = np.random.default_rng(config.seed + (0 if object_split == "train" else 1000))
    samples: list[dict[str, object]] = []
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
        for object_index, (obj_native, obj_lowres) in enumerate(zip(objects, lowres_objects)):
            blurred = fft_convolve(obj_native, psf)
            noisy = np.clip(blurred + rng.normal(0.0, config.noise_sigma, blurred.shape), 0.0, 1.0)
            fixed_restore = wiener_deconvolution(noisy, nominal_psf, config.nominal_wiener_k)
            fixed_lowres = downsample(fixed_restore, config.lowres_size)
            samples.append(
                {
                    "split": object_split,
                    "case_id": case_id,
                    "object_id": f"{object_split}_object_{object_index:02d}",
                    "gt_lowres": obj_lowres,
                    "noisy_lowres": downsample(noisy, config.lowres_size),
                    "fixed_lowres": fixed_lowres,
                    "reference_lowres": reference_lowres,
                    "psf_lowres": reference_lowres,
                    "fixed_psnr_lowres": psnr(obj_lowres, fixed_lowres),
                    "defocus": coeffs["defocus"],
                    "astig_x": coeffs["astig_x"],
                    "coma_x": coeffs["coma_x"],
                }
            )
    return samples


def upscale(arr: np.ndarray, scale: int = 10) -> Image.Image:
    return normalize_to_uint8(arr).resize((arr.shape[1] * scale, arr.shape[0] * scale), Image.Resampling.NEAREST)


def build_panel(rows: list[dict[str, object]], output_path: Path) -> None:
    labels = ["ground_truth", "aberrated", "fixed", "phase_only", "|fixed err|", "|phase err|", "ref_psf"]
    scale = 10
    tile = rows[0]["gt_lowres"].shape[0] * scale
    margin = 12
    row_label_width = 180
    header_height = 28
    width = row_label_width + len(labels) * (tile + margin) + margin
    height = margin + header_height + len(rows) * (tile + 44 + margin)
    canvas = Image.new("L", (width, height), color=255)
    draw = ImageDraw.Draw(canvas)

    for col_index, label in enumerate(labels):
        x = row_label_width + margin + col_index * (tile + margin)
        draw.text((x, margin), label, fill=0)

    for row_index, row in enumerate(rows):
        y = margin + header_height + row_index * (tile + 44 + margin)
        draw.text((margin, y + 8), row["row_label"], fill=0)
        images = [
            row["gt_lowres"],
            row["noisy_lowres"],
            row["fixed_lowres"],
            row["phase_lowres"],
            np.abs(row["fixed_lowres"] - row["gt_lowres"]),
            np.abs(row["phase_lowres"] - row["gt_lowres"]),
            row["psf_lowres"],
        ]
        for col_index, arr in enumerate(images):
            x = row_label_width + margin + col_index * (tile + margin)
            canvas.paste(upscale(arr, scale), (x, y))
        draw.text(
            (margin, y + tile + 16),
            f"gain={row['psnr_gain_over_fixed_lowres']:.3f} dB | fixed={row['fixed_psnr_lowres']:.3f} | phase={row['phase_psnr_lowres']:.3f}",
            fill=0,
        )
    canvas.save(output_path)


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    results_dir = project_root / "results" / "failure_cases"
    results_dir.mkdir(parents=True, exist_ok=True)

    detail_path = project_root / "results" / "unified_comparison" / "unified_comparison_detail.csv"
    detail_df = pd.read_csv(detail_path)
    phase_df = detail_df[
        (detail_df["method"] == "phase_only_stack")
        & (detail_df["ledger"] == "new_family_heldout_object_family")
    ].copy()

    selected_rows = []
    for object_id in [
        "heldout_object_family_object_00",
        "heldout_object_family_object_02",
        "heldout_object_family_object_03",
    ]:
        selected_rows.append(
            phase_df.loc[phase_df["object_id"] == object_id]
            .sort_values("psnr_gain_over_fixed_lowres")
            .iloc[0]
        )
    selected_df = pd.DataFrame(selected_rows).reset_index(drop=True)

    by_seed_predictions: dict[int, dict[tuple[int, str], np.ndarray]] = {}
    by_seed_samples: dict[int, dict[tuple[int, str], dict[str, object]]] = {}

    for seed in sorted(selected_df["seed"].unique()):
        config = PhaseOnlyConfig(seed=int(seed))
        train_objects = make_megadiverse_training_objects(config.image_size)
        heldout_objects = make_heldout_objects(config.image_size)
        train_cases = make_aberration_cases(config.train_case_count, config.seed)
        heldout_cases = make_aberration_cases(config.heldout_case_count, config.seed + 500)

        train_samples = rich_build_split_samples(train_objects, "train", train_cases, config)
        heldout_samples = rich_build_split_samples(heldout_objects, "heldout_object_family", heldout_cases, config)

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
        predictions = predict_ridge(build_features(heldout_samples, masks, propagation), weights)

        by_seed_predictions[int(seed)] = {}
        by_seed_samples[int(seed)] = {}
        for index, sample in enumerate(heldout_samples):
            key = (int(sample["case_id"]), str(sample["object_id"]))
            by_seed_predictions[int(seed)][key] = predictions[index].reshape(config.lowres_size, config.lowres_size)
            by_seed_samples[int(seed)][key] = sample

    panel_rows = []
    output_rows = []
    for _, selected in selected_df.iterrows():
        seed = int(selected["seed"])
        case_id = int(selected["case_id"])
        object_id = str(selected["object_id"])
        key = (case_id, object_id)
        sample = by_seed_samples[seed][key]
        phase_pred = by_seed_predictions[seed][key]
        phase_psnr = psnr(sample["gt_lowres"], phase_pred)

        object_label = OBJECT_LABELS[object_id]
        output_rows.append(
            {
                "seed": seed,
                "case_id": case_id,
                "object_id": object_id,
                "object_label": object_label,
                "defocus": float(sample["defocus"]),
                "astig_x": float(sample["astig_x"]),
                "coma_x": float(sample["coma_x"]),
                "fixed_psnr_lowres": float(sample["fixed_psnr_lowres"]),
                "phase_psnr_lowres": float(phase_psnr),
                "psnr_gain_over_fixed_lowres": float(phase_psnr - sample["fixed_psnr_lowres"]),
                "failure_reason": FAILURE_REASON[object_id],
            }
        )
        panel_rows.append(
            {
                "row_label": f"{object_label} | seed {seed} | case {case_id}",
                "gt_lowres": sample["gt_lowres"],
                "noisy_lowres": sample["noisy_lowres"],
                "fixed_lowres": sample["fixed_lowres"],
                "phase_lowres": phase_pred,
                "psf_lowres": sample["psf_lowres"],
                "fixed_psnr_lowres": float(sample["fixed_psnr_lowres"]),
                "phase_psnr_lowres": float(phase_psnr),
                "psnr_gain_over_fixed_lowres": float(phase_psnr - sample["fixed_psnr_lowres"]),
            }
        )

    failure_csv = results_dir / "object_shift_failure_cases.csv"
    failure_md = results_dir / "object_shift_failure_cases.md"
    failure_png = results_dir / "object_shift_failure_cases_panel.png"
    failure_json = results_dir / "object_shift_failure_cases_summary.json"

    pd.DataFrame(output_rows).to_csv(failure_csv, index=False)
    build_panel(panel_rows, failure_png)

    md_lines = [
        "# Supplementary Failure Cases Under Object-Family Shift",
        "",
        "This package documents representative cases in which the current phase-only stack falls below the fixed baseline under `new_family_heldout_object_family`.",
        "",
        "## Main pattern",
        "",
        "- `diag_x` is the most consistently negative held-out object family.",
        "- `checker_blocks` is near the decision boundary but contains clear negative cases.",
        "- `crescent` shows mixed behavior with a negative tail.",
        "- `triangle` is comparatively stable and positive, so the failures are structure-dependent rather than uniformly distributed across the held-out ledger.",
        "",
        "## Representative cases",
        "",
    ]
    for row in output_rows:
        md_lines.extend(
            [
                f"### {row['object_label']}",
                f"- seed: `{row['seed']}`",
                f"- case_id: `{row['case_id']}`",
                f"- aberration coefficients: defocus `{row['defocus']:.4f}`, astig_x `{row['astig_x']:.4f}`, coma_x `{row['coma_x']:.4f}`",
                f"- fixed low-resolution PSNR: `{row['fixed_psnr_lowres']:.3f} dB`",
                f"- phase-only low-resolution PSNR: `{row['phase_psnr_lowres']:.3f} dB`",
                f"- phase-only gain over fixed: `{row['psnr_gain_over_fixed_lowres']:.3f} dB`",
                f"- interpretation: {row['failure_reason']}",
                "",
            ]
        )
    md_lines.extend(
        [
            "## Figure usage note",
            "",
            "The panel image is intended as a supplementary figure candidate showing ground truth, aberrated input, fixed restoration, phase-only restoration, corresponding error maps, and the reference PSF for representative failure modes.",
            "",
            f"- panel: `{failure_png.relative_to(project_root)}`",
            f"- table: `{failure_csv.relative_to(project_root)}`",
        ]
    )
    failure_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    failure_json.write_text(json.dumps(output_rows, indent=2), encoding="utf-8")

    print(json.dumps({"failure_csv": str(failure_csv), "failure_png": str(failure_png)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
