#!/usr/bin/env python3
"""Thick-statistics rerun for mixed synthetic + proxy-natural training."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from run_baseline_phase_only_megadiverse_train_dual_heldout_thickstats import (
    PhaseOnlyConfig,
    build_split_samples,
    confidence_interval_95,
    make_aberration_cases,
)
from run_mixed_train_natural_object_rerun import build_mixed_training_objects
from run_natural_object_evaluation import dataset_dir_name, load_grayscale_objects, load_subset_index, staging_root
from run_real_pipeline import compute_psnr, fit_pipeline, forward_diffractive, model


@dataclass
class ThickstatsConfig:
    seeds: tuple[int, ...] = (0, 1, 2, 3, 4)
    train_case_count: int = 24
    eval_case_count: int = 12


def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def natural_root() -> Path:
    return project_root() / "results" / "natural_objects"


def summarize_group(df: pd.DataFrame) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for dataset_name, dataset_df in df.groupby("dataset_name"):
        per_seed = (
            dataset_df.groupby("seed", as_index=False)
            .agg(
                mean_psnr_gain_over_fixed_lowres=("psnr_gain_over_fixed_lowres", "mean"),
                better_than_fixed_fraction=("psnr_gain_over_fixed_lowres", lambda s: float((s > 0.0).mean())),
                mean_pipeline_psnr_lowres=("pipeline_psnr_lowres", "mean"),
                mean_fixed_psnr_lowres=("fixed_psnr_lowres", "mean"),
                mean_guided_psnr_lowres=("guided_psnr_lowres", "mean"),
            )
        )
        gains = per_seed["mean_psnr_gain_over_fixed_lowres"].to_numpy(dtype=float)
        mean_gain, ci_half = confidence_interval_95(gains)
        rows.append(
            {
                "dataset_name": dataset_name,
                "seed_count": int(len(per_seed)),
                "mean_psnr_gain_over_fixed_lowres": float(mean_gain),
                "ci95_half_width": float(ci_half),
                "std_psnr_gain_over_fixed_lowres": float(gains.std(ddof=1)) if len(gains) > 1 else 0.0,
                "mean_better_than_fixed_fraction": float(per_seed["better_than_fixed_fraction"].mean()),
                "mean_pipeline_psnr_lowres": float(per_seed["mean_pipeline_psnr_lowres"].mean()),
                "mean_fixed_psnr_lowres": float(per_seed["mean_fixed_psnr_lowres"].mean()),
                "mean_guided_psnr_lowres": float(per_seed["mean_guided_psnr_lowres"].mean()),
            }
        )
    return rows


def main() -> int:
    cfg = ThickstatsConfig()
    mixed_train_objects, mix_counts = build_mixed_training_objects()
    all_rows: list[pd.DataFrame] = []
    out_dir = natural_root()
    out_dir.mkdir(parents=True, exist_ok=True)

    for seed in cfg.seeds:
        phase_config = PhaseOnlyConfig(seed=seed, train_case_count=cfg.train_case_count, heldout_case_count=cfg.eval_case_count)
        train_cases = make_aberration_cases(phase_config.train_case_count, phase_config.seed)
        eval_cases = make_aberration_cases(phase_config.heldout_case_count, phase_config.seed + 500)
        train_samples = build_split_samples(mixed_train_objects, "train", train_cases, phase_config)
        state = fit_pipeline(train_samples, config=type("Cfg", (), {"seed": seed, "train_case_count": cfg.train_case_count, "eval_case_count": cfg.eval_case_count})())

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
            metrics_df, _summary = compute_psnr(eval_samples, recon, state)
            metrics_df["dataset_name"] = spec.dataset_name
            metrics_df["dataset_version"] = spec.dataset_version
            metrics_df["seed"] = seed
            metrics_df["training_regime"] = "mixed_synthetic_plus_public_natural_thickstats"
            all_rows.append(metrics_df)

    metrics = pd.concat(all_rows, ignore_index=True)
    summary_rows = summarize_group(metrics)
    metrics_path = out_dir / "mixed_train_natural_object_thickstats_metrics.csv"
    summary_path = out_dir / "mixed_train_natural_object_thickstats_summary.json"
    metrics.to_csv(metrics_path, index=False)
    payload = {
        "status": "completed",
        "config": {
            "seeds": list(cfg.seeds),
            "seed_count": len(cfg.seeds),
            "train_case_count": cfg.train_case_count,
            "eval_case_count": cfg.eval_case_count,
        },
        "training_mix_counts": mix_counts,
        "summary_rows": summary_rows,
        "metrics_csv": str(metrics_path),
        "summary_json": str(summary_path),
    }
    summary_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
