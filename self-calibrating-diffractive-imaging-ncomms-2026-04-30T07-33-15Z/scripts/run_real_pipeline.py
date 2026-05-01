#!/usr/bin/env python3
"""Unified executable pipeline for the active diffractive-imaging project."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
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
    make_heldout_objects,
    make_megadiverse_training_objects,
    make_objects,
    make_phase_basis,
    optimize_phase_coeffs,
    phase_masks_from_coeffs,
    predict_ridge,
    propagate_phase_frontend,
)
from run_baseline_reference_psf import psnr


@dataclass
class PipelineRunConfig:
    seed: int = 0
    train_case_count: int = 24
    eval_case_count: int = 6
    eval_split: str = "new_family_heldout_object_family"
    output_subdir: str = "pipeline_smoke"


@dataclass
class PipelineState:
    phase_config: PhaseOnlyConfig
    propagation: PropagationConfig
    basis: np.ndarray
    masks: np.ndarray
    weights: np.ndarray


def resolve_project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_dataset(config: PipelineRunConfig) -> dict[str, list[dict[str, object]]]:
    phase_config = PhaseOnlyConfig(
        seed=config.seed,
        train_case_count=config.train_case_count,
        heldout_case_count=config.eval_case_count,
    )
    train_objects = make_megadiverse_training_objects(phase_config.image_size)
    same_family_objects = make_objects(phase_config.image_size)
    new_family_objects = make_heldout_objects(phase_config.image_size)
    train_cases = make_aberration_cases(phase_config.train_case_count, config.seed)
    eval_cases = make_aberration_cases(phase_config.heldout_case_count, config.seed + 500)
    return {
        "train": build_split_samples(train_objects, "train", train_cases, phase_config),
        "same_family_heldout_aberration": build_split_samples(
            same_family_objects,
            "heldout_aberration",
            eval_cases,
            phase_config,
        ),
        "new_family_heldout_object_family": build_split_samples(
            new_family_objects,
            "heldout_object_family",
            eval_cases,
            phase_config,
        ),
    }


def fit_pipeline(train_samples: list[dict[str, object]], config: PipelineRunConfig) -> PipelineState:
    phase_config = PhaseOnlyConfig(
        seed=config.seed,
        train_case_count=config.train_case_count,
        heldout_case_count=config.eval_case_count,
    )
    basis = make_phase_basis(phase_config.lowres_size, phase_config.phase_basis_count)
    frontend_spacing = phase_config.sample_spacing * phase_config.image_size / phase_config.lowres_size
    propagation = PropagationConfig(
        grid_size=phase_config.lowres_size,
        sample_spacing=frontend_spacing,
        wavelength=phase_config.wavelength,
        propagation_distance=phase_config.propagation_distance,
    )
    coeffs = optimize_phase_coeffs(phase_config, basis, train_samples, propagation)
    masks = phase_masks_from_coeffs(coeffs, basis)
    x_train = build_features(train_samples, masks, propagation)
    y_train = build_targets(train_samples)
    weights = fit_ridge_regression(x_train, y_train, phase_config.ridge_lambda)
    return PipelineState(
        phase_config=phase_config,
        propagation=propagation,
        basis=basis,
        masks=masks,
        weights=weights,
    )


def forward_diffractive(
    samples: list[dict[str, object]],
    state: PipelineState,
) -> dict[str, object]:
    feature_rows: list[np.ndarray] = []
    per_sample_planes: list[np.ndarray] = []
    for sample in samples:
        optical_planes = propagate_phase_frontend(
            sample["noisy_lowres"],
            sample["reference_lowres"],
            state.masks,
            state.propagation,
        )
        per_sample_planes.append(np.asarray(optical_planes))
        feature_rows.append(
            np.concatenate(
                [
                    sample["noisy_lowres"].reshape(-1),
                    sample["reference_lowres"].reshape(-1),
                    *(plane.reshape(-1) for plane in optical_planes),
                ]
            )
        )
    return {
        "features": np.asarray(feature_rows, dtype=np.float64),
        "phase_planes": np.asarray(per_sample_planes, dtype=np.float64),
        "sample_count": len(samples),
    }


def model(optical_output: dict[str, object], state: PipelineState) -> np.ndarray:
    return predict_ridge(optical_output["features"], state.weights)


def compute_psnr(
    samples: list[dict[str, object]],
    recon: np.ndarray,
    state: PipelineState,
) -> tuple[pd.DataFrame, dict[str, float]]:
    rows: list[dict[str, object]] = []
    for index, sample in enumerate(samples):
        recon_image = recon[index].reshape(
            state.phase_config.lowres_size,
            state.phase_config.lowres_size,
        )
        recon_psnr = psnr(sample["gt_lowres"], recon_image)
        rows.append(
            {
                "case_id": int(sample["case_id"]),
                "object_id": str(sample["object_id"]),
                "fixed_psnr_lowres": float(sample["fixed_psnr_lowres"]),
                "guided_psnr_lowres": float(sample["guided_psnr_lowres"]),
                "pipeline_psnr_lowres": float(recon_psnr),
                "psnr_gain_over_fixed_lowres": float(recon_psnr - sample["fixed_psnr_lowres"]),
                "psnr_gap_to_guided_lowres": float(sample["guided_psnr_lowres"] - recon_psnr),
            }
        )
    df = pd.DataFrame(rows)
    summary = {
        "sample_count": int(len(df)),
        "mean_fixed_psnr_lowres": float(df["fixed_psnr_lowres"].mean()),
        "mean_guided_psnr_lowres": float(df["guided_psnr_lowres"].mean()),
        "mean_pipeline_psnr_lowres": float(df["pipeline_psnr_lowres"].mean()),
        "mean_psnr_gain_over_fixed_lowres": float(df["psnr_gain_over_fixed_lowres"].mean()),
        "better_than_fixed_fraction": float((df["psnr_gain_over_fixed_lowres"] > 0.0).mean()),
    }
    return df, summary


def run_pipeline(config: PipelineRunConfig) -> dict[str, object]:
    dataset = load_dataset(config)
    train_samples = dataset["train"]
    eval_samples = dataset[config.eval_split]
    state = fit_pipeline(train_samples, config)
    optical_output = forward_diffractive(eval_samples, state)
    recon = model(optical_output, state)
    metrics_df, summary = compute_psnr(eval_samples, recon, state)

    project_root = resolve_project_root()
    output_dir = project_root / "results" / "pipeline" / config.output_subdir
    output_dir.mkdir(parents=True, exist_ok=True)

    metrics_path = output_dir / "pipeline_metrics.csv"
    summary_path = output_dir / "pipeline_summary.json"
    runtime_path = output_dir / "pipeline_runtime.json"

    metrics_df.to_csv(metrics_path, index=False)
    summary_payload = {
        "run_config": asdict(config),
        "phase_config": asdict(state.phase_config),
        "summary": summary,
        "output_files": {
            "metrics_csv": str(metrics_path),
            "summary_json": str(summary_path),
            "runtime_json": str(runtime_path),
        },
    }
    summary_path.write_text(json.dumps(summary_payload, indent=2) + "\n", encoding="utf-8")

    runtime_payload = {
        "train_sample_count": len(train_samples),
        "eval_sample_count": len(eval_samples),
        "feature_shape": list(optical_output["features"].shape),
        "phase_plane_shape": list(optical_output["phase_planes"].shape),
    }
    runtime_path.write_text(json.dumps(runtime_payload, indent=2) + "\n", encoding="utf-8")
    return summary_payload


def main() -> int:
    payload = run_pipeline(PipelineRunConfig())
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
