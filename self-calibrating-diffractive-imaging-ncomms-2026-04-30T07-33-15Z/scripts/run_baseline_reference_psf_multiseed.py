#!/usr/bin/env python3
"""Run multi-seed statistics for the reference-guided PSF baseline."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from run_baseline_reference_psf import SimulationConfig, run_reference_baseline


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


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "results" / "baselines" / "baseline-001-reference-psf-multiseed"
    out_dir.mkdir(parents=True, exist_ok=True)

    per_seed_metrics = []
    generated_files: list[Path] = []

    for seed in SEEDS:
        config = SimulationConfig(seed=seed)
        df, summary, _ = run_reference_baseline(config)
        sample_path = out_dir / f"metrics_by_sample_seed_{seed}.csv"
        sample_log = out_dir / f"run_log_seed_{seed}.txt"
        df.to_csv(sample_path, index=False)
        sample_log.write_text(
            "\n".join(
                [
                    f"seed={seed}",
                    f"sample_spacing_m={config.sample_spacing}",
                    f"wavelength_m={config.wavelength}",
                    f"propagation_distance_m={config.propagation_distance}",
                    f"fx_min_1_per_m={summary['optics_metadata']['fx_min_1_per_m']}",
                    f"fx_max_1_per_m={summary['optics_metadata']['fx_max_1_per_m']}",
                    f"fy_min_1_per_m={summary['optics_metadata']['fy_min_1_per_m']}",
                    f"fy_max_1_per_m={summary['optics_metadata']['fy_max_1_per_m']}",
                    f"mean_psnr_gain={summary['mean_psnr_gain']}",
                    f"mean_ssim_gain={summary['mean_ssim_gain']}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        generated_files.extend([sample_path, sample_log])
        per_seed_metrics.append(
            {
                "seed": seed,
                "mean_fixed_psnr": summary["mean_fixed_psnr"],
                "mean_guided_psnr": summary["mean_guided_psnr"],
                "mean_psnr_gain": summary["mean_psnr_gain"],
                "mean_fixed_ssim": summary["mean_fixed_ssim"],
                "mean_guided_ssim": summary["mean_guided_ssim"],
                "mean_ssim_gain": summary["mean_ssim_gain"],
                "guided_better_fraction_psnr": summary["guided_better_fraction_psnr"],
                "guided_better_fraction_ssim": summary["guided_better_fraction_ssim"],
            }
        )

    per_seed_df = pd.DataFrame(per_seed_metrics)
    rows = []
    for metric in [
        "mean_fixed_psnr",
        "mean_guided_psnr",
        "mean_psnr_gain",
        "mean_fixed_ssim",
        "mean_guided_ssim",
        "mean_ssim_gain",
        "guided_better_fraction_psnr",
        "guided_better_fraction_ssim",
    ]:
        values = per_seed_df[metric].to_numpy(dtype=float)
        mean, ci95 = confidence_interval_95(values)
        rows.append(
            {
                "metric": metric,
                "mean": mean,
                "std": float(values.std(ddof=1)),
                "ci95_half_width": ci95,
                "seed_count": len(values),
            }
        )
    summary_df = pd.DataFrame(rows)
    summary_path = out_dir / "multiseed_summary.csv"
    summary_df.to_csv(summary_path, index=False)
    generated_files.append(summary_path)

    manifest_path = out_dir / "sha256_manifest.txt"
    write_sha256_manifest(generated_files, manifest_path)

    print(json.dumps({"seeds": SEEDS, "output_dir": str(out_dir)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
