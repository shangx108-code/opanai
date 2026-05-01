#!/usr/bin/env python3
"""Run a parameter-matched digital-only surrogate on the frozen dual-heldout ledgers."""

from __future__ import annotations

import csv
import json
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from run_baseline_reference_psf import psnr
from run_baseline_phase_only_megadiverse_train_dual_heldout_thickstats import (
    PhaseOnlyConfig,
    build_split_samples,
    confidence_interval_95,
    fit_ridge_regression,
    make_aberration_cases,
    make_heldout_objects,
    make_megadiverse_training_objects,
    make_objects,
    predict_ridge,
)


SEEDS = list(range(10))
LEDGER_NAMES = (
    "same_family_heldout_aberration",
    "new_family_heldout_object_family",
)
METHOD_NAME = "parameter_matched_digital_surrogate"
DERIVED_CHANNEL_NAMES = (
    "noisy_lowres",
    "reference_lowres",
    "difference",
    "sum",
    "product",
    "noisy_square",
    "reference_square",
)


def parameter_matched_feature_vector(sample: dict[str, object]) -> np.ndarray:
    noisy = np.asarray(sample["noisy_lowres"], dtype=np.float64)
    reference = np.asarray(sample["reference_lowres"], dtype=np.float64)
    channels = [
        noisy,
        reference,
        noisy - reference,
        0.5 * (noisy + reference),
        noisy * reference,
        noisy * noisy,
        reference * reference,
    ]
    return np.concatenate([channel.reshape(-1) for channel in channels], axis=0)


def build_parameter_matched_features(samples: list[dict[str, object]]) -> np.ndarray:
    return np.asarray([parameter_matched_feature_vector(sample) for sample in samples], dtype=np.float64)


def build_ledgers(config: PhaseOnlyConfig, seed: int) -> tuple[list[dict[str, object]], dict[str, list[dict[str, object]]]]:
    train_objects = make_megadiverse_training_objects(config.image_size)
    same_family_eval_objects = make_objects(config.image_size)
    new_family_eval_objects = make_heldout_objects(config.image_size)
    train_cases = make_aberration_cases(config.train_case_count, seed)
    heldout_cases = make_aberration_cases(config.heldout_case_count, seed + 500)

    train_samples = build_split_samples(train_objects, "train", train_cases, config)
    same_family_samples = build_split_samples(same_family_eval_objects, "heldout_aberration", heldout_cases, config)
    new_family_samples = build_split_samples(new_family_eval_objects, "heldout_object_family", heldout_cases, config)

    for sample in train_samples:
        sample["seed"] = seed
        sample["ledger"] = "train"
    for sample in same_family_samples:
        sample["seed"] = seed
        sample["ledger"] = "same_family_heldout_aberration"
    for sample in new_family_samples:
        sample["seed"] = seed
        sample["ledger"] = "new_family_heldout_object_family"

    return train_samples, {
        "same_family_heldout_aberration": same_family_samples,
        "new_family_heldout_object_family": new_family_samples,
    }


def evaluate_prediction_method(
    samples: list[dict[str, object]],
    prediction: np.ndarray,
    lowres_size: int,
) -> pd.DataFrame:
    rows = []
    for index, sample in enumerate(samples):
        pred = prediction[index].reshape(lowres_size, lowres_size)
        method_psnr = psnr(sample["gt_lowres"], pred)
        rows.append(
            {
                "method": METHOD_NAME,
                "seed": int(sample["seed"]),
                "ledger": str(sample["ledger"]),
                "case_id": int(sample["case_id"]),
                "object_id": str(sample["object_id"]),
                "fixed_psnr_lowres": float(sample["fixed_psnr_lowres"]),
                "method_psnr_lowres": float(method_psnr),
                "psnr_gain_over_fixed_lowres": float(method_psnr - sample["fixed_psnr_lowres"]),
                "better_than_fixed": bool(method_psnr > sample["fixed_psnr_lowres"]),
            }
        )
    return pd.DataFrame(rows)


def summarize_per_seed(detail_df: pd.DataFrame) -> pd.DataFrame:
    return (
        detail_df.groupby(["method", "seed", "ledger"], as_index=False)
        .agg(
            mean_psnr_gain=("psnr_gain_over_fixed_lowres", "mean"),
            better_than_fixed_fraction=("better_than_fixed", "mean"),
            n_samples=("object_id", "count"),
        )
        .sort_values(["seed", "ledger"])
        .reset_index(drop=True)
    )


def summarize_by_ledger(detail_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    grouped = detail_df.groupby(["ledger", "seed"], as_index=False).agg(
        mean_psnr_gain=("psnr_gain_over_fixed_lowres", "mean"),
        better_than_fixed_fraction=("better_than_fixed", "mean"),
        n_samples=("object_id", "count"),
    )
    for ledger_name in LEDGER_NAMES:
        ledger_df = grouped.loc[grouped["ledger"] == ledger_name].reset_index(drop=True)
        gains = ledger_df["mean_psnr_gain"].to_numpy(dtype=float)
        mean_gain, half_width = confidence_interval_95(gains)
        rows.append(
            {
                "method": METHOD_NAME,
                "ledger": ledger_name,
                "mean_psnr_gain": mean_gain,
                "std_psnr_gain": float(gains.std(ddof=1)) if len(gains) > 1 else 0.0,
                "ci_low": mean_gain - half_width,
                "ci_high": mean_gain + half_width,
                "better_than_fixed_fraction": float(ledger_df["better_than_fixed_fraction"].mean()),
                "n_seeds": int(len(ledger_df)),
                "n_samples": int(ledger_df["n_samples"].sum()),
                "samples_per_seed": int(ledger_df["n_samples"].iloc[0]) if len(ledger_df) else 0,
            }
        )
    return pd.DataFrame(rows)


def summarize_overall(ledger_summary: pd.DataFrame) -> dict[str, float | int | list[str]]:
    gains = ledger_summary["mean_psnr_gain"].to_numpy(dtype=float)
    mean_gain, half_width = confidence_interval_95(gains)
    return {
        "method": METHOD_NAME,
        "mean_psnr_gain_across_ledgers": float(gains.mean()),
        "mean_psnr_gain_across_ledgers_with_ci_center": mean_gain,
        "mean_psnr_gain_ci_low": mean_gain - half_width,
        "mean_psnr_gain_ci_high": mean_gain + half_width,
        "mean_better_than_fixed_fraction": float(ledger_summary["better_than_fixed_fraction"].mean()),
        "digital_trainable_parameters": int((7 * 12 * 12) * (12 * 12) + (12 * 12)),
        "optical_trainable_parameters": 0,
        "derived_channels": list(DERIVED_CHANNEL_NAMES),
    }


def ledger_summary_markdown(ledger_summary_df: pd.DataFrame) -> str:
    header = "| Method | Ledger | Mean PSNR gain | Std PSNR gain | CI low | CI high | Better-than-fixed fraction | n seeds | n samples |"
    divider = "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |"
    rows = [header, divider]
    for row in ledger_summary_df.itertuples(index=False):
        rows.append(
            "| "
            + " | ".join(
                [
                    str(row.method),
                    str(row.ledger),
                    f"{row.mean_psnr_gain:.6f}",
                    f"{row.std_psnr_gain:.6f}",
                    f"{row.ci_low:.6f}",
                    f"{row.ci_high:.6f}",
                    f"{row.better_than_fixed_fraction:.6f}",
                    str(int(row.n_seeds)),
                    str(int(row.n_samples)),
                ]
            )
            + " |"
        )
    return "\n".join(rows)


def run_seed(seed: int) -> pd.DataFrame:
    config = PhaseOnlyConfig(seed=seed)
    train_samples, ledgers = build_ledgers(config, seed)
    x_train = build_parameter_matched_features(train_samples)
    y_train = np.asarray([sample["gt_lowres"].reshape(-1) for sample in train_samples], dtype=np.float64)
    weights = fit_ridge_regression(x_train, y_train, config.ridge_lambda)

    detail_frames = []
    for ledger_name in LEDGER_NAMES:
        ledger_samples = ledgers[ledger_name]
        prediction = predict_ridge(build_parameter_matched_features(ledger_samples), weights)
        detail_frames.append(evaluate_prediction_method(ledger_samples, prediction, config.lowres_size))
    return pd.concat(detail_frames, ignore_index=True)


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    out_dir = project_root / "results" / "baselines" / "baseline-010-parameter-matched-digital-surrogate"
    out_dir.mkdir(parents=True, exist_ok=True)

    with ProcessPoolExecutor(max_workers=min(5, len(SEEDS))) as executor:
        detail_frames = list(executor.map(run_seed, SEEDS))

    detail_df = pd.concat(detail_frames, ignore_index=True)
    per_seed_df = summarize_per_seed(detail_df)
    ledger_summary_df = summarize_by_ledger(detail_df)
    overall_summary = summarize_overall(ledger_summary_df)

    detail_df.to_csv(out_dir / "detail_metrics.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    per_seed_df.to_csv(out_dir / "per_seed_summary.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    ledger_summary_df.to_csv(out_dir / "ledger_summary.csv", index=False, quoting=csv.QUOTE_MINIMAL)
    (out_dir / "summary.json").write_text(
        json.dumps(
            {
                "seeds": SEEDS,
                "method": METHOD_NAME,
                "parameter_budget_match_target": "phase_only_stack digital ridge stage",
                "overall_summary": overall_summary,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    (out_dir / "summary.md").write_text(
        "\n".join(
            [
                "# Baseline 010 Parameter-Matched Digital Surrogate",
                "",
                "Goal: provide a digital-only comparator with the same trainable digital parameter count used by the downstream ridge stage of `phase_only_stack`.",
                "",
                "## Design",
                "",
                "- Same training object family and same two held-out ledgers as the unified benchmark",
                "- Same low-resolution target grid: `12 x 12`",
                "- Zero optical trainable parameters",
                f"- Digital trainable parameters: `{overall_summary['digital_trainable_parameters']}`",
                f"- Derived channels: `{', '.join(DERIVED_CHANNEL_NAMES)}`",
                "",
                "## Mean PSNR gain over fixed baseline by ledger",
                "",
                ledger_summary_markdown(ledger_summary_df),
                "",
                "## Interpretation boundary",
                "",
                "This comparator is intentionally simple: it expands the distorted and reference channels into a fixed seven-channel image-domain feature bank and trains only the final linear readout. It tests whether the phase-only result can be explained by downstream digital capacity alone after parameter matching.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print(json.dumps({"output_dir": str(out_dir), "method": METHOD_NAME}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
