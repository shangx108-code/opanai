from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from round6_numpy_passive_d2nn import (
    GOOD_REFERENCE,
    OUT,
    SIZE,
    TEST_SAMPLES,
    TRAIN_SAMPLES,
    ensure_dirs,
    mse,
    normalize,
    processor_forward,
    psnr,
    tile_images,
)
from round7_parameter_scan import phase_from_coeffs
from wrong_reference_designs_v3 import WRONG_REFERENCE_V3_MODES, edge_map, sparse_map, wrong_reference_v3


NUM_LAYERS = 1
REFERENCE_WEIGHT = 0.16
PHASE_MIX = 0.16
INPUT_PHASE_COUPLING = 0.90
REPEAT_SEEDS = list(range(6))
CONDITIONS = ["ordinary", "common_path", "noncommon_path", "wrong_reference"]
RISK_SAMPLE_NAMES = {"frame", "two_spots"}
ENCODING_MODES = ["baseline", "edge_guarded", "occupancy_guarded", "hybrid_guarded"]


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    pos = (len(ordered) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return ordered[lo]
    w = pos - lo
    return ordered[lo] * (1.0 - w) + ordered[hi] * w


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    fieldnames = list(rows[0].keys())
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def smooth_map(pattern: np.ndarray) -> np.ndarray:
    acc = pattern.copy()
    acc += np.roll(pattern, 1, axis=0)
    acc += np.roll(pattern, -1, axis=0)
    acc += np.roll(pattern, 1, axis=1)
    acc += np.roll(pattern, -1, axis=1)
    return normalize(acc / 5.0)


def encoding_gate(pattern: np.ndarray, mode: str) -> np.ndarray:
    if mode == "baseline":
        return np.ones_like(pattern)
    if mode == "edge_guarded":
        return np.clip(1.0 - 0.75 * edge_map(pattern), 0.20, 1.0)
    if mode == "occupancy_guarded":
        return np.clip(0.20 + 0.80 * smooth_map(pattern), 0.20, 1.0)
    if mode == "hybrid_guarded":
        edges = edge_map(pattern)
        occ = smooth_map(pattern)
        sparse = sparse_map(pattern)
        return np.clip(0.15 + 0.45 * occ + 0.30 * sparse + 0.25 * (1.0 - edges), 0.15, 1.0)
    raise ValueError(mode)


def make_input(sample, condition: str, wrongref_mode: str, encoding_mode: str):
    object_amp = sample.object_pattern
    object_phase = phase_from_coeffs(sample.coeffs)
    gate = encoding_gate(object_amp, encoding_mode)

    if condition == "ordinary":
        return object_amp, INPUT_PHASE_COUPLING * object_phase

    if condition == "common_path":
        ref_amp = GOOD_REFERENCE
        ref_phase = object_phase
    elif condition == "noncommon_path":
        ref_amp = GOOD_REFERENCE
        ref_phase = phase_from_coeffs(sample.coeffs[::-1] * np.array([1.1, -0.9, 1.0, -1.0]))
    elif condition == "wrong_reference":
        ref_amp, ref_phase = wrong_reference_v3(sample, wrongref_mode)
    else:
        raise ValueError(condition)

    encoded_ref_amp = gate * ref_amp
    encoded_ref_phase = gate * ref_phase
    new_amp = np.clip(object_amp + REFERENCE_WEIGHT * encoded_ref_amp, 0.0, 1.7)
    new_phase = INPUT_PHASE_COUPLING * object_phase + PHASE_MIX * encoded_ref_phase
    return new_amp, new_phase


def objective(masks: np.ndarray, samples, condition: str, wrongref_mode: str, encoding_mode: str) -> float:
    losses = []
    for sample in samples:
        amp, phase = make_input(sample, condition, wrongref_mode, encoding_mode)
        pred = processor_forward(amp, phase, masks)
        losses.append(mse(pred, sample.object_pattern))
    return float(np.mean(losses))


def train_condition(condition: str, wrongref_mode: str, encoding_mode: str, seed: int):
    rng = np.random.default_rng(seed)
    masks = rng.uniform(-0.15, 0.15, size=(NUM_LAYERS, SIZE, SIZE))
    best_masks = masks.copy()
    best_loss = objective(best_masks, TRAIN_SAMPLES, condition, wrongref_mode, encoding_mode)
    history = []
    for step in range(18):
        delta = rng.choice([-1.0, 1.0], size=masks.shape)
        ck = 0.32 / ((step + 1) ** 0.22)
        ak = 0.50 / ((step + 2) ** 0.55)
        plus_loss = objective(masks + ck * delta, TRAIN_SAMPLES, condition, wrongref_mode, encoding_mode)
        minus_loss = objective(masks - ck * delta, TRAIN_SAMPLES, condition, wrongref_mode, encoding_mode)
        grad = (plus_loss - minus_loss) / (2.0 * ck) * delta
        masks = np.mod(masks - ak * grad + np.pi, 2.0 * np.pi) - np.pi
        train_loss = objective(masks, TRAIN_SAMPLES, condition, wrongref_mode, encoding_mode)
        if train_loss < best_loss:
            best_loss = train_loss
            best_masks = masks.copy()
        history.append({"step": step + 1, "train_mse": train_loss})
    return best_masks, history


def evaluate_config(config_id: int, wrongref_mode: str, encoding_mode: str, repeat_seed: int):
    trained = {}
    histories = {}
    detail_rows: list[dict[str, object]] = []
    risk_rows: list[dict[str, object]] = []
    summary_by_condition: dict[str, dict[str, float]] = {}

    for cond_idx, condition in enumerate(CONDITIONS):
        masks, history = train_condition(
            condition=condition,
            wrongref_mode=wrongref_mode,
            encoding_mode=encoding_mode,
            seed=16100 + config_id * 83 + repeat_seed * 29 + cond_idx,
        )
        trained[condition] = masks
        histories[condition] = history

    preview_rows = []
    for sample in [s for s in TEST_SAMPLES if s.name in RISK_SAMPLE_NAMES]:
        row = [sample.object_pattern] + [np.zeros_like(sample.object_pattern) for _ in range(4)]
        for col, condition in enumerate(CONDITIONS, start=1):
            amp, phase = make_input(sample, condition, wrongref_mode, encoding_mode)
            row[col] = processor_forward(amp, phase, trained[condition])
        preview_rows.append(row)

    risk_bucket: dict[str, dict[str, float]] = {}
    for split_name, samples in [("train", TRAIN_SAMPLES), ("ood", TEST_SAMPLES)]:
        for condition in CONDITIONS:
            scores = []
            mses = []
            for sample in samples:
                amp, phase = make_input(sample, condition, wrongref_mode, encoding_mode)
                pred = processor_forward(amp, phase, trained[condition])
                err = mse(pred, sample.object_pattern)
                score = psnr(pred, sample.object_pattern)
                scores.append(score)
                mses.append(err)
                detail_rows.append(
                    {
                        "config_id": config_id,
                        "repeat_seed": repeat_seed,
                        "split": split_name,
                        "sample": sample.name,
                        "condition": condition,
                        "wrongref_mode": wrongref_mode,
                        "encoding_mode": encoding_mode,
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
                "config_id": config_id,
                "repeat_seed": repeat_seed,
                "sample": sample_name,
                "wrongref_mode": wrongref_mode,
                "encoding_mode": encoding_mode,
                "common_minus_wrongref_db": round(cmw, 6),
                "common_minus_ordinary_db": round(cmo, 6),
            }
        )

    repeat_row = {
        "config_id": config_id,
        "repeat_seed": repeat_seed,
        "wrongref_mode": wrongref_mode,
        "encoding_mode": encoding_mode,
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
    return repeat_row, detail_rows, risk_rows, preview_rows, histories


def aggregate_rows(repeat_rows: list[dict[str, object]], risk_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped_repeats: dict[int, list[dict[str, object]]] = {}
    for row in repeat_rows:
        grouped_repeats.setdefault(int(row["config_id"]), []).append(row)

    grouped_risk: dict[int, list[dict[str, object]]] = {}
    for row in risk_rows:
        grouped_risk.setdefault(int(row["config_id"]), []).append(row)

    summary_rows = []
    for config_id, bucket in grouped_repeats.items():
        risk_bucket = grouped_risk[config_id]
        base = bucket[0]

        cmo = np.array([float(row["common_minus_ordinary_db"]) for row in bucket], dtype=float)
        cmw = np.array([float(row["common_minus_wrongref_db"]) for row in bucket], dtype=float)
        risk_cmw = np.array([float(row["common_minus_wrongref_db"]) for row in risk_bucket], dtype=float)
        risk_q10 = float(percentile(risk_cmw.tolist(), 0.10))
        risk_min = float(np.min(risk_cmw))
        risk_positive_fraction = float(np.mean(risk_cmw > 0))

        ranking_score = 2.8 * risk_q10 + 0.9 * risk_positive_fraction + 0.4 * float(np.mean(cmo)) + 0.2 * float(np.mean(cmw))
        summary_rows.append(
            {
                "config_id": config_id,
                "wrongref_mode": str(base["wrongref_mode"]),
                "encoding_mode": str(base["encoding_mode"]),
                "repeat_count": len(bucket),
                "risk_pair_q10_db": round(risk_q10, 6),
                "risk_pair_min_db": round(risk_min, 6),
                "risk_pair_positive_fraction": round(risk_positive_fraction, 6),
                "common_minus_ordinary_db_mean": round(float(np.mean(cmo)), 6),
                "common_minus_ordinary_db_min": round(float(np.min(cmo)), 6),
                "common_minus_wrongref_db_mean": round(float(np.mean(cmw)), 6),
                "common_minus_wrongref_db_min": round(float(np.min(cmw)), 6),
                "ranking_score": round(ranking_score, 6),
            }
        )
    return sorted(summary_rows, key=lambda row: row["ranking_score"], reverse=True)


def main() -> None:
    ensure_dirs()
    repeat_rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []
    risk_rows: list[dict[str, object]] = []
    best_payload = None
    config_id = 0

    for wrongref_mode in WRONG_REFERENCE_V3_MODES:
        for encoding_mode in ENCODING_MODES:
            config_id += 1
            local_repeat_rows = []
            local_risk_rows = []
            local_best_preview = None
            local_best_histories = None
            local_best_score = -1e9
            for repeat_seed in REPEAT_SEEDS:
                repeat_row, local_detail, local_risk, preview_rows, histories = evaluate_config(
                    config_id=config_id,
                    wrongref_mode=wrongref_mode,
                    encoding_mode=encoding_mode,
                    repeat_seed=repeat_seed,
                )
                repeat_rows.append(repeat_row)
                detail_rows.extend(local_detail)
                risk_rows.extend(local_risk)
                local_repeat_rows.append(repeat_row)
                local_risk_rows.extend(local_risk)
                repeat_score = 2.0 * float(repeat_row["risk_pair_q10_repeat"]) + 0.3 * float(repeat_row["common_minus_ordinary_db"])
                if repeat_score > local_best_score:
                    local_best_score = repeat_score
                    local_best_preview = preview_rows
                    local_best_histories = histories

            local_q10 = percentile([float(row["common_minus_wrongref_db"]) for row in local_risk_rows], 0.10)
            local_cmo = float(np.mean([float(row["common_minus_ordinary_db"]) for row in local_repeat_rows]))
            preview_score = 2.0 * local_q10 + 0.3 * local_cmo
            if best_payload is None or preview_score > best_payload["preview_score"]:
                best_payload = {
                    "config_id": config_id,
                    "preview_rows": local_best_preview,
                    "histories": local_best_histories,
                    "preview_score": preview_score,
                }

    summary_rows = aggregate_rows(repeat_rows, risk_rows)
    top_rows = summary_rows[:10]

    repeat_csv = OUT / "round16_structural_scan_repeat_rows.csv"
    detail_csv = OUT / "round16_structural_scan_detail.csv"
    risk_csv = OUT / "round16_structural_scan_risk_rows.csv"
    summary_csv = OUT / "round16_structural_scan_summary.csv"
    top_csv = OUT / "round16_structural_scan_top.csv"
    summary_json = OUT / "round16_structural_scan_summary.json"
    summary_md = OUT / "round16_structural_scan_summary.md"
    best_panel_png = OUT / "round16_structural_scan_best_panel.png"
    best_history_json = OUT / "round16_structural_scan_best_history.json"

    write_csv(repeat_rows, repeat_csv)
    write_csv(detail_rows, detail_csv)
    write_csv(risk_rows, risk_csv)
    write_csv(summary_rows, summary_csv)
    write_csv(top_rows, top_csv)
    tile_images(best_payload["preview_rows"], ["target", "ordinary", "common", "noncommon", "wrongref"], best_panel_png)
    best_history_json.write_text(json.dumps(best_payload["histories"], indent=2), encoding="utf-8")

    payload = {
        "status": "ok",
        "scan_size": len(summary_rows),
        "repeat_count_per_config": len(REPEAT_SEEDS),
        "fixed_settings": {
            "phase_mix": PHASE_MIX,
            "reference_weight": REFERENCE_WEIGHT,
            "input_phase_coupling": INPUT_PHASE_COUPLING,
            "target_samples": sorted(RISK_SAMPLE_NAMES),
        },
        "best_config": top_rows[0],
        "configs_meeting_q10_target": [row for row in summary_rows if float(row["risk_pair_q10_db"]) >= 0.0],
        "top": top_rows,
        "artifacts": {
            "repeat_csv": str(repeat_csv),
            "detail_csv": str(detail_csv),
            "risk_csv": str(risk_csv),
            "summary_csv": str(summary_csv),
            "top_csv": str(top_csv),
            "summary_json": str(summary_json),
            "summary_md": str(summary_md),
            "best_panel_png": str(best_panel_png),
            "best_history_json": str(best_history_json),
        },
        "note": "Round16 replaces continuous micro-tuning with structural wrong-reference and input-encoding variants.",
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    best = top_rows[0]
    lines = [
        "# Round 16 Structural Mode Scan",
        "",
        f"- scan size: {len(summary_rows)} structural combinations",
        f"- repeats per config: {len(REPEAT_SEEDS)}",
        f"- fixed phase_mix/reference_weight/input_phase_coupling: {PHASE_MIX:.2f} / {REFERENCE_WEIGHT:.2f} / {INPUT_PHASE_COUPLING:.2f}",
        f"- best wrongref_mode: {best['wrongref_mode']}",
        f"- best encoding_mode: {best['encoding_mode']}",
        f"- best risk-pair q10: {best['risk_pair_q10_db']:+.3f} dB",
        f"- best risk-pair min: {best['risk_pair_min_db']:+.3f} dB",
        f"- best risk-pair positive fraction: {best['risk_pair_positive_fraction']:.3f}",
        f"- configs with q10 >= 0: {sum(float(row['risk_pair_q10_db']) >= 0.0 for row in summary_rows)}",
        "- interpretation: this round asks whether structural changes outperform continuous micro-tuning on the frame/two_spots tail.",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
