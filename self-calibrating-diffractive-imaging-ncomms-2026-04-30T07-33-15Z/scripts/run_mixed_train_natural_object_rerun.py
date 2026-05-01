#!/usr/bin/env python3
"""Rerun natural-object evaluation with mixed synthetic + proxy-natural training objects."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from run_baseline_phase_only_megadiverse_train_dual_heldout_thickstats import (
    PhaseOnlyConfig,
    build_split_samples,
    make_aberration_cases,
    make_megadiverse_training_objects,
)
from run_natural_object_evaluation import (
    dataset_dir_name,
    load_subset_index,
    load_grayscale_objects,
    staging_root,
)
from run_real_pipeline import compute_psnr, fit_pipeline, forward_diffractive, model


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def natural_root() -> Path:
    return project_root() / "results" / "natural_objects"


def build_mixed_training_objects() -> tuple[list[np.ndarray], dict[str, int]]:
    phase_config = PhaseOnlyConfig()
    synthetic_objects = make_megadiverse_training_objects(phase_config.image_size)
    proxy_objects: list[np.ndarray] = []
    per_dataset_counts: dict[str, int] = {}
    for spec in load_subset_index():
        directory = staging_root() / dataset_dir_name(spec)
        proxy_rows = load_grayscale_objects(directory)
        per_dataset_counts[spec.dataset_name] = len(proxy_rows)
        proxy_objects.extend(arr for _, arr in proxy_rows)
    counts = {
        "synthetic_training_objects": len(synthetic_objects),
        "public_natural_training_objects": len(proxy_objects),
    }
    counts.update({f"public_{k}": v for k, v in per_dataset_counts.items()})
    return synthetic_objects + proxy_objects, counts


def run_mixed_train_rerun() -> dict[str, object]:
    phase_config = PhaseOnlyConfig(seed=0, train_case_count=24, heldout_case_count=6)
    mixed_train_objects, counts = build_mixed_training_objects()
    train_cases = make_aberration_cases(phase_config.train_case_count, phase_config.seed)
    eval_cases = make_aberration_cases(phase_config.heldout_case_count, phase_config.seed + 500)
    train_samples = build_split_samples(mixed_train_objects, "train", train_cases, phase_config)
    state = fit_pipeline(train_samples, config=type("Cfg", (), {"seed": 0, "train_case_count": 24, "eval_case_count": 6})())

    all_rows: list[pd.DataFrame] = []
    summary_rows: list[dict[str, object]] = []
    for spec in load_subset_index():
        directory = staging_root() / dataset_dir_name(spec)
        objects_with_names = load_grayscale_objects(directory)
        object_arrays = [arr for _, arr in objects_with_names]
        eval_samples = build_split_samples(object_arrays, "natural_object_eval", eval_cases, phase_config)
        for index, (name, _) in enumerate(objects_with_names):
            for case_id in range(phase_config.heldout_case_count):
                sample_index = case_id * len(objects_with_names) + index
                eval_samples[sample_index]["object_id"] = f"{spec.dataset_name}:{name}"
        optical_output = forward_diffractive(eval_samples, state)
        recon = model(optical_output, state)
        metrics_df, summary = compute_psnr(eval_samples, recon, state)
        metrics_df["dataset_name"] = spec.dataset_name
        metrics_df["dataset_version"] = spec.dataset_version
        metrics_df["training_regime"] = "mixed_synthetic_plus_public_natural"
        all_rows.append(metrics_df)
        summary_rows.append(
            {
                "dataset_name": spec.dataset_name,
                "dataset_version": spec.dataset_version,
                "image_count": len(objects_with_names),
                "training_regime": "mixed_synthetic_plus_public_natural",
                **summary,
            }
        )

    out_dir = natural_root()
    metrics_path = out_dir / "mixed_train_natural_object_metrics.csv"
    summary_path = out_dir / "mixed_train_natural_object_summary.json"
    metrics = pd.concat(all_rows, ignore_index=True)
    metrics.to_csv(metrics_path, index=False)
    payload = {
        "status": "completed",
        "training_mix_counts": counts,
        "summary_rows": summary_rows,
        "metrics_csv": str(metrics_path),
        "summary_json": str(summary_path),
    }
    summary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    payload = run_mixed_train_rerun()
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
