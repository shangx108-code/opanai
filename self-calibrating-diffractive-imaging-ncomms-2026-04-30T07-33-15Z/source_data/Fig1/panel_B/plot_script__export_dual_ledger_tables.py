from __future__ import annotations

import math
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path("/workspace/memory/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z")
DETAIL_IN = PROJECT_ROOT / "results/unified_comparison/unified_comparison_detail.csv"
TABLES_DIR = PROJECT_ROOT / "results/tables"


def ci95_half_width(std: float, n: int) -> float:
    if n <= 1 or pd.isna(std):
        return float("nan")
    return 1.96 * std / math.sqrt(n)


def main() -> None:
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DETAIL_IN)

    seed_level = (
        df.groupby(["ledger", "method", "seed"], as_index=False)
        .agg(
            mean_psnr_gain=("psnr_gain_over_fixed_lowres", "mean"),
            better_than_fixed_fraction=("better_than_fixed", "mean"),
            n_samples=("psnr_gain_over_fixed_lowres", "size"),
        )
        .sort_values(["ledger", "method", "seed"])
    )
    seed_level.to_csv(TABLES_DIR / "unified_comparison_by_ledger_detail.csv", index=False)

    summary = (
        seed_level.groupby(["ledger", "method"], as_index=False)
        .agg(
            mean_psnr_gain=("mean_psnr_gain", "mean"),
            std_psnr_gain=("mean_psnr_gain", "std"),
            better_than_fixed_fraction=("better_than_fixed_fraction", "mean"),
            n_seeds=("seed", "nunique"),
            n_samples_per_seed=("n_samples", "first"),
        )
        .sort_values(["ledger", "method"])
    )
    summary["ci95_half_width"] = summary.apply(
        lambda row: ci95_half_width(row["std_psnr_gain"], int(row["n_seeds"])), axis=1
    )
    summary["ci_low"] = summary["mean_psnr_gain"] - summary["ci95_half_width"]
    summary["ci_high"] = summary["mean_psnr_gain"] + summary["ci95_half_width"]
    summary["n_samples"] = summary["n_seeds"] * summary["n_samples_per_seed"]

    summary = summary[
        [
            "method",
            "ledger",
            "mean_psnr_gain",
            "std_psnr_gain",
            "ci95_half_width",
            "ci_low",
            "ci_high",
            "better_than_fixed_fraction",
            "n_seeds",
            "n_samples",
            "n_samples_per_seed",
        ]
    ]
    summary.to_csv(TABLES_DIR / "unified_comparison_by_ledger.csv", index=False)
    print("Wrote:")
    print(TABLES_DIR / "unified_comparison_by_ledger.csv")
    print(TABLES_DIR / "unified_comparison_by_ledger_detail.csv")


if __name__ == "__main__":
    main()
