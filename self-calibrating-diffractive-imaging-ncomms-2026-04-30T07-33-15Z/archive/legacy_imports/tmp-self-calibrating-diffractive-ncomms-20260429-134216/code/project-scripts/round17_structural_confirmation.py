from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from round16_structural_modes_scan import (
    CONDITIONS,
    INPUT_PHASE_COUPLING,
    NUM_LAYERS,
    PHASE_MIX,
    REFERENCE_WEIGHT,
    RISK_SAMPLE_NAMES,
    ensure_dirs,
    make_input,
    objective,
    percentile,
    processor_forward,
    psnr,
    mse,
    OUT,
    SIZE,
    TEST_SAMPLES,
    TRAIN_SAMPLES,
    tile_images,
)


WRONGREF_MODE = "sparse_tracker_decoy"
ENCODING_MODE = "occupancy_guarded"
REPEAT_SEEDS = list(range(14))


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    fieldnames = list(rows[0].keys())
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def train_condition(condition: str, seed: int):
    rng = np.random.default_rng(seed)
    masks = rng.uniform(-0.15, 0.15, size=(NUM_LAYERS, SIZE, SIZE))
    best_masks = masks.copy()
    best_loss = objective(best_masks, TRAIN_SAMPLES, condition, WRONGREF_MODE, ENCODING_MODE)
    history = []
    for step in range(18):
        delta = rng.choice([-1.0, 1.0], size=masks.shape)
        ck = 0.32 / ((step + 1) ** 0.22)
        ak = 0.50 / ((step + 2) ** 0.55)
        plus_loss = objective(masks + ck * delta, TRAIN_SAMPLES, condition, WRONGREF_MODE, ENCODING_MODE)
        minus_loss = objective(masks - ck * delta, TRAIN_SAMPLES, condition, WRONGREF_MODE, ENCODING_MODE)
        grad = (plus_loss - minus_loss) / (2.0 * ck) * delta
        masks = np.mod(masks - ak * grad + np.pi, 2.0 * np.pi) - np.pi
        train_loss = objective(masks, TRAIN_SAMPLES, condition, WRONGREF_MODE, ENCODING_MODE)
        if train_loss < best_loss:
            best_loss = train_loss
            best_masks = masks.copy()
        history.append({"step": step + 1, "train_mse": train_loss})
    return best_masks, history


def main() -> None:
    ensure_dirs()
    repeat_rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []
    risk_rows: list[dict[str, object]] = []
    best_preview = None
    best_histories = None
    best_preview_score = -1e9

    for repeat_seed in REPEAT_SEEDS:
        trained = {}
        histories = {}
        risk_bucket: dict[str, dict[str, float]] = {}
        summary_by_condition: dict[str, dict[str, float]] = {}

        for cond_idx, condition in enumerate(CONDITIONS):
            masks, history = train_condition(condition=condition, seed=17100 + repeat_seed * 37 + cond_idx)
            trained[condition] = masks
            histories[condition] = history

        preview_rows = []
        for sample in [s for s in TEST_SAMPLES if s.name in RISK_SAMPLE_NAMES]:
            row = [sample.object_pattern] + [np.zeros_like(sample.object_pattern) for _ in range(4)]
            for col, condition in enumerate(CONDITIONS, start=1):
                amp, phase = make_input(sample, condition, WRONGREF_MODE, ENCODING_MODE)
                row[col] = processor_forward(amp, phase, trained[condition])
            preview_rows.append(row)

        for split_name, samples in [("train", TRAIN_SAMPLES), ("ood", TEST_SAMPLES)]:
            for condition in CONDITIONS:
                scores = []
                mses = []
                for sample in samples:
                    amp, phase = make_input(sample, condition, WRONGREF_MODE, ENCODING_MODE)
                    pred = processor_forward(amp, phase, trained[condition])
                    err = mse(pred, sample.object_pattern)
                    score = psnr(pred, sample.object_pattern)
                    scores.append(score)
                    mses.append(err)
                    detail_rows.append(
                        {
                            "repeat_seed": repeat_seed,
                            "split": split_name,
                            "sample": sample.name,
                            "condition": condition,
                            "wrongref_mode": WRONGREF_MODE,
                            "encoding_mode": ENCODING_MODE,
                            "psnr_db": round(score, 6),
                            "mse": round(err, 8),
                        }
                    )
                    if split_name == "ood" and sample.name in RISK_SAMPLE_NAMES:
                        risk_bucket.setdefault(sample.name, {})[condition] = score
                if split_name == "ood":
                    summary_by_condition[condition] = {
                        "ood_mean_psnr_db": float(np.mean(scores)),
                        "ood_mean_mse": float(np.mean(mses)),
                    }

        risk_margins = []
        for sample_name in sorted(RISK_SAMPLE_NAMES):
            bucket = risk_bucket[sample_name]
            cmw = bucket["common_path"] - bucket["wrong_reference"]
            cmo = bucket["common_path"] - bucket["ordinary"]
            risk_margins.append(cmw)
            risk_rows.append(
                {
                    "repeat_seed": repeat_seed,
                    "sample": sample_name,
                    "wrongref_mode": WRONGREF_MODE,
                    "encoding_mode": ENCODING_MODE,
                    "common_minus_wrongref_db": round(cmw, 6),
                    "common_minus_ordinary_db": round(cmo, 6),
                }
            )

        repeat_row = {
            "repeat_seed": repeat_seed,
            "wrongref_mode": WRONGREF_MODE,
            "encoding_mode": ENCODING_MODE,
            "common_minus_ordinary_db": round(
                summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["ordinary"]["ood_mean_psnr_db"], 6
            ),
            "common_minus_wrongref_db": round(
                summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["wrong_reference"]["ood_mean_psnr_db"], 6
            ),
            "risk_pair_q10_repeat": round(percentile(risk_margins, 0.10), 6),
            "risk_pair_min_repeat": round(min(risk_margins), 6),
            "risk_pair_positive_fraction_repeat": round(sum(v > 0 for v in risk_margins) / len(risk_margins), 6),
        }
        repeat_rows.append(repeat_row)

        preview_score = 2.0 * float(repeat_row["risk_pair_q10_repeat"]) + 0.3 * float(repeat_row["common_minus_ordinary_db"])
        if preview_score > best_preview_score:
            best_preview_score = preview_score
            best_preview = preview_rows
            best_histories = histories

    all_risk_margins = [float(row["common_minus_wrongref_db"]) for row in risk_rows]
    all_cmo = [float(row["common_minus_ordinary_db"]) for row in repeat_rows]
    all_cmw = [float(row["common_minus_wrongref_db"]) for row in repeat_rows]
    summary = {
        "wrongref_mode": WRONGREF_MODE,
        "encoding_mode": ENCODING_MODE,
        "repeat_count": len(REPEAT_SEEDS),
        "fixed_phase_mix": PHASE_MIX,
        "fixed_reference_weight": REFERENCE_WEIGHT,
        "fixed_input_phase_coupling": INPUT_PHASE_COUPLING,
        "risk_pair_q10_db": round(percentile(all_risk_margins, 0.10), 6),
        "risk_pair_min_db": round(min(all_risk_margins), 6),
        "risk_pair_positive_fraction": round(sum(v > 0 for v in all_risk_margins) / len(all_risk_margins), 6),
        "common_minus_ordinary_db_mean": round(float(np.mean(all_cmo)), 6),
        "common_minus_ordinary_db_min": round(float(np.min(all_cmo)), 6),
        "common_minus_wrongref_db_mean": round(float(np.mean(all_cmw)), 6),
        "common_minus_wrongref_db_min": round(float(np.min(all_cmw)), 6),
    }

    repeat_csv = OUT / "round17_structural_confirm_repeat_rows.csv"
    detail_csv = OUT / "round17_structural_confirm_detail.csv"
    risk_csv = OUT / "round17_structural_confirm_risk_rows.csv"
    summary_json = OUT / "round17_structural_confirm_summary.json"
    summary_md = OUT / "round17_structural_confirm_summary.md"
    best_panel_png = OUT / "round17_structural_confirm_best_panel.png"
    best_history_json = OUT / "round17_structural_confirm_best_history.json"

    write_csv(repeat_rows, repeat_csv)
    write_csv(detail_rows, detail_csv)
    write_csv(risk_rows, risk_csv)
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    tile_images(best_preview, ["target", "ordinary", "common", "noncommon", "wrongref"], best_panel_png)
    best_history_json.write_text(json.dumps(best_histories, indent=2), encoding="utf-8")

    lines = [
        "# Round 17 Structural Confirmation",
        "",
        f"- confirmed structure: {WRONGREF_MODE} + {ENCODING_MODE}",
        f"- repeats: {len(REPEAT_SEEDS)}",
        f"- risk-pair q10: {summary['risk_pair_q10_db']:+.3f} dB",
        f"- risk-pair min: {summary['risk_pair_min_db']:+.3f} dB",
        f"- risk-pair positive fraction: {summary['risk_pair_positive_fraction']:.3f}",
        f"- common minus ordinary mean: {summary['common_minus_ordinary_db_mean']:+.3f} dB",
        f"- common minus ordinary min: {summary['common_minus_ordinary_db_min']:+.3f} dB",
        "- interpretation: this round checks whether the first positive q10 survives substantially more repeats without changing the structure.",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
