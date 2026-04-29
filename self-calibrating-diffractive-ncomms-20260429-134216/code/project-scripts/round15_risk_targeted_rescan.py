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
    processor_forward,
    psnr,
    tile_images,
)
from round7_parameter_scan import phase_from_coeffs
from wrong_reference_designs_v2 import wrong_reference_v2


NUM_LAYERS = 1
PHASE_MIXES = [0.16, 0.17, 0.18, 0.19]
REFERENCE_WEIGHTS = [0.14, 0.16, 0.18, 0.20]
INPUT_PHASE_COUPLINGS = [0.90, 1.00, 1.10]
REPEAT_SEEDS = list(range(8))
CONDITIONS = ["ordinary", "common_path", "noncommon_path", "wrong_reference"]
RISK_SAMPLE_NAMES = {"frame", "two_spots"}
WRONGREF_MODE = "anti_phase_plus_decoy"


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    fieldnames = list(rows[0].keys())
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def make_input(sample, condition: str, reference_weight: float, phase_mix: float, input_phase_coupling: float):
    object_amp = sample.object_pattern
    object_phase = phase_from_coeffs(sample.coeffs)

    if condition == "ordinary":
        return object_amp, input_phase_coupling * object_phase

    if condition == "common_path":
        ref_amp = GOOD_REFERENCE
        ref_phase = object_phase
    elif condition == "noncommon_path":
        ref_amp = GOOD_REFERENCE
        ref_phase = phase_from_coeffs(sample.coeffs[::-1] * np.array([1.1, -0.9, 1.0, -1.0]))
    elif condition == "wrong_reference":
        ref_amp, ref_phase = wrong_reference_v2(sample, WRONGREF_MODE)
    else:
        raise ValueError(condition)

    new_amp = np.clip(object_amp + reference_weight * ref_amp, 0.0, 1.7)
    new_phase = input_phase_coupling * object_phase + phase_mix * ref_phase
    return new_amp, new_phase


def objective(masks: np.ndarray, samples, condition: str, reference_weight: float, phase_mix: float, input_phase_coupling: float) -> float:
    losses = []
    for sample in samples:
        amp, phase = make_input(sample, condition, reference_weight, phase_mix, input_phase_coupling)
        pred = processor_forward(amp, phase, masks)
        losses.append(mse(pred, sample.object_pattern))
    return float(np.mean(losses))


def train_condition(condition: str, reference_weight: float, phase_mix: float, input_phase_coupling: float, seed: int):
    rng = np.random.default_rng(seed)
    masks = rng.uniform(-0.15, 0.15, size=(NUM_LAYERS, SIZE, SIZE))
    best_masks = masks.copy()
    best_loss = objective(best_masks, TRAIN_SAMPLES, condition, reference_weight, phase_mix, input_phase_coupling)
    history = []
    for step in range(18):
        delta = rng.choice([-1.0, 1.0], size=masks.shape)
        ck = 0.32 / ((step + 1) ** 0.22)
        ak = 0.50 / ((step + 2) ** 0.55)
        plus_loss = objective(masks + ck * delta, TRAIN_SAMPLES, condition, reference_weight, phase_mix, input_phase_coupling)
        minus_loss = objective(masks - ck * delta, TRAIN_SAMPLES, condition, reference_weight, phase_mix, input_phase_coupling)
        grad = (plus_loss - minus_loss) / (2.0 * ck) * delta
        masks = np.mod(masks - ak * grad + np.pi, 2.0 * np.pi) - np.pi
        train_loss = objective(masks, TRAIN_SAMPLES, condition, reference_weight, phase_mix, input_phase_coupling)
        if train_loss < best_loss:
            best_loss = train_loss
            best_masks = masks.copy()
        history.append({"step": step + 1, "train_mse": train_loss})
    return best_masks, history


def evaluate_config(config_id: int, reference_weight: float, phase_mix: float, input_phase_coupling: float, repeat_seed: int):
    trained = {}
    histories = {}
    detail_rows: list[dict[str, object]] = []
    risk_pair_margins: list[float] = []
    summary_by_condition: dict[str, dict[str, float]] = {}

    for cond_idx, condition in enumerate(CONDITIONS):
        masks, history = train_condition(
            condition=condition,
            reference_weight=reference_weight,
            phase_mix=phase_mix,
            input_phase_coupling=input_phase_coupling,
            seed=15100 + config_id * 97 + repeat_seed * 31 + cond_idx,
        )
        trained[condition] = masks
        histories[condition] = history

    preview_rows = []
    for sample in [sample for sample in TEST_SAMPLES if sample.name in RISK_SAMPLE_NAMES]:
        row = [sample.object_pattern] + [np.zeros_like(sample.object_pattern) for _ in range(4)]
        for col, condition in enumerate(CONDITIONS, start=1):
            amp, phase = make_input(sample, condition, reference_weight, phase_mix, input_phase_coupling)
            row[col] = processor_forward(amp, phase, trained[condition])
        preview_rows.append(row)

    risk_rows_by_sample: dict[str, dict[str, float]] = {}
    for split_name, samples in [("train", TRAIN_SAMPLES), ("ood", TEST_SAMPLES)]:
        for condition in CONDITIONS:
            scores = []
            mses = []
            for sample in samples:
                amp, phase = make_input(sample, condition, reference_weight, phase_mix, input_phase_coupling)
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
                        "num_layers": NUM_LAYERS,
                        "reference_weight": round(reference_weight, 4),
                        "phase_mix": round(phase_mix, 4),
                        "input_phase_coupling": round(input_phase_coupling, 4),
                        "wrongref_mode": WRONGREF_MODE,
                        "psnr_db": round(score, 6),
                        "mse": round(err, 8),
                    }
                )
                if split_name == "ood" and sample.name in RISK_SAMPLE_NAMES:
                    risk_rows_by_sample.setdefault(sample.name, {})[condition] = score
            if split_name == "ood":
                summary_by_condition[condition] = {
                    "ood_mean_psnr_db": float(np.mean(scores)),
                    "ood_mean_mse": float(np.mean(mses)),
                    "train_final_mse": float(histories[condition][-1]["train_mse"]),
                }

    risk_sample_rows = []
    for sample_name in sorted(RISK_SAMPLE_NAMES):
        bucket = risk_rows_by_sample[sample_name]
        cmw = float(bucket["common_path"] - bucket["wrong_reference"])
        cmo = float(bucket["common_path"] - bucket["ordinary"])
        risk_pair_margins.append(cmw)
        risk_sample_rows.append(
            {
                "config_id": config_id,
                "repeat_seed": repeat_seed,
                "sample": sample_name,
                "reference_weight": round(reference_weight, 4),
                "phase_mix": round(phase_mix, 4),
                "input_phase_coupling": round(input_phase_coupling, 4),
                "common_minus_wrongref_db": round(cmw, 6),
                "common_minus_ordinary_db": round(cmo, 6),
            }
        )

    repeat_row = {
        "config_id": config_id,
        "repeat_seed": repeat_seed,
        "num_layers": NUM_LAYERS,
        "reference_weight": round(reference_weight, 4),
        "phase_mix": round(phase_mix, 4),
        "input_phase_coupling": round(input_phase_coupling, 4),
        "wrongref_mode": WRONGREF_MODE,
        "ordinary_ood_mean_psnr_db": round(summary_by_condition["ordinary"]["ood_mean_psnr_db"], 6),
        "common_ood_mean_psnr_db": round(summary_by_condition["common_path"]["ood_mean_psnr_db"], 6),
        "noncommon_ood_mean_psnr_db": round(summary_by_condition["noncommon_path"]["ood_mean_psnr_db"], 6),
        "wrongref_ood_mean_psnr_db": round(summary_by_condition["wrong_reference"]["ood_mean_psnr_db"], 6),
        "common_minus_ordinary_db": round(
            summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["ordinary"]["ood_mean_psnr_db"], 6
        ),
        "common_minus_noncommon_db": round(
            summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["noncommon_path"]["ood_mean_psnr_db"], 6
        ),
        "common_minus_wrongref_db": round(
            summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["wrong_reference"]["ood_mean_psnr_db"], 6
        ),
        "risk_pair_q10_db_repeat": round(percentile(risk_pair_margins, 0.10), 6),
        "risk_pair_min_db_repeat": round(min(risk_pair_margins), 6),
        "risk_pair_positive_fraction_repeat": round(sum(value > 0 for value in risk_pair_margins) / len(risk_pair_margins), 6),
    }
    return repeat_row, detail_rows, risk_sample_rows, preview_rows, histories


def aggregate_rows(repeat_rows: list[dict[str, object]], risk_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped_repeats: dict[int, list[dict[str, object]]] = {}
    for row in repeat_rows:
        grouped_repeats.setdefault(int(row["config_id"]), []).append(row)

    grouped_risk: dict[int, list[dict[str, object]]] = {}
    for row in risk_rows:
        grouped_risk.setdefault(int(row["config_id"]), []).append(row)

    summary_rows = []
    for config_id, bucket in grouped_repeats.items():
        base = bucket[0]
        risk_bucket = grouped_risk[config_id]

        def vals(rows: list[dict[str, object]], key: str) -> np.ndarray:
            return np.array([float(row[key]) for row in rows], dtype=float)

        cmo = vals(bucket, "common_minus_ordinary_db")
        cmw = vals(bucket, "common_minus_wrongref_db")
        risk_cmw = vals(risk_bucket, "common_minus_wrongref_db")

        risk_q10 = float(percentile(risk_cmw.tolist(), 0.10))
        risk_positive_fraction = float(np.mean(risk_cmw > 0))
        risk_min = float(np.min(risk_cmw))
        ranking_score = (
            2.50 * risk_q10
            + 0.80 * risk_positive_fraction
            + 0.40 * float(np.mean(cmo))
            + 0.20 * float(np.mean(cmw))
            + 1.20 * min(risk_min, 0.0)
        )

        summary_rows.append(
            {
                "config_id": config_id,
                "num_layers": int(base["num_layers"]),
                "reference_weight": float(base["reference_weight"]),
                "phase_mix": float(base["phase_mix"]),
                "input_phase_coupling": float(base["input_phase_coupling"]),
                "wrongref_mode": str(base["wrongref_mode"]),
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
    risk_sample_rows: list[dict[str, object]] = []
    best_payload = None
    config_id = 0

    for phase_mix in PHASE_MIXES:
        for reference_weight in REFERENCE_WEIGHTS:
            for input_phase_coupling in INPUT_PHASE_COUPLINGS:
                config_id += 1
                local_repeat_rows = []
                local_risk_rows = []
                local_best_preview = None
                local_best_histories = None
                local_best_score = -1e9
                for repeat_seed in REPEAT_SEEDS:
                    repeat_row, local_detail, local_risk, preview_rows, histories = evaluate_config(
                        config_id=config_id,
                        reference_weight=reference_weight,
                        phase_mix=phase_mix,
                        input_phase_coupling=input_phase_coupling,
                        repeat_seed=repeat_seed,
                    )
                    repeat_rows.append(repeat_row)
                    detail_rows.extend(local_detail)
                    risk_sample_rows.extend(local_risk)
                    local_repeat_rows.append(repeat_row)
                    local_risk_rows.extend(local_risk)
                    repeat_score = 1.8 * float(repeat_row["risk_pair_q10_db_repeat"]) + 0.4 * float(repeat_row["common_minus_ordinary_db"])
                    if repeat_score > local_best_score:
                        local_best_score = repeat_score
                        local_best_preview = preview_rows
                        local_best_histories = histories

                local_q10 = percentile([float(row["common_minus_wrongref_db"]) for row in local_risk_rows], 0.10)
                preview_score = 1.8 * local_q10 + 0.4 * float(np.mean([float(row["common_minus_ordinary_db"]) for row in local_repeat_rows]))
                if best_payload is None or preview_score > best_payload["preview_score"]:
                    best_payload = {
                        "config_id": config_id,
                        "preview_rows": local_best_preview,
                        "histories": local_best_histories,
                        "preview_score": preview_score,
                    }

    summary_rows = aggregate_rows(repeat_rows, risk_sample_rows)
    top_rows = summary_rows[:10]

    repeat_csv = OUT / "round15_risk_rescan_repeat_rows.csv"
    detail_csv = OUT / "round15_risk_rescan_detail.csv"
    risk_csv = OUT / "round15_risk_rescan_risk_rows.csv"
    summary_csv = OUT / "round15_risk_rescan_summary.csv"
    top_csv = OUT / "round15_risk_rescan_top.csv"
    summary_json = OUT / "round15_risk_rescan_summary.json"
    summary_md = OUT / "round15_risk_rescan_summary.md"
    best_panel_png = OUT / "round15_risk_rescan_best_panel.png"
    best_history_json = OUT / "round15_risk_rescan_best_history.json"

    write_csv(repeat_rows, repeat_csv)
    write_csv(detail_rows, detail_csv)
    write_csv(risk_sample_rows, risk_csv)
    write_csv(summary_rows, summary_csv)
    write_csv(top_rows, top_csv)
    tile_images(best_payload["preview_rows"], ["target", "ordinary", "common", "noncommon", "wrongref"], best_panel_png)
    best_history_json.write_text(json.dumps(best_payload["histories"], indent=2), encoding="utf-8")

    payload = {
        "status": "ok",
        "scan_size": len(summary_rows),
        "repeat_count_per_config": len(REPEAT_SEEDS),
        "target_samples": sorted(RISK_SAMPLE_NAMES),
        "search_space": {
            "phase_mix": PHASE_MIXES,
            "reference_weight": REFERENCE_WEIGHTS,
            "input_phase_coupling": INPUT_PHASE_COUPLINGS,
            "wrongref_mode": WRONGREF_MODE,
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
        "note": "Round15 targets only frame and two_spots for q10 >= 0, while keeping the processor family fixed to anti_phase_plus_decoy.",
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    best = top_rows[0]
    lines = [
        "# Round 15 Risk-sample Targeted Re-scan",
        "",
        f"- scan size: {len(summary_rows)} focused configurations",
        f"- repeats per config: {len(REPEAT_SEEDS)}",
        f"- target samples: {', '.join(sorted(RISK_SAMPLE_NAMES))}",
        f"- fixed wrongref_mode: {WRONGREF_MODE}",
        f"- best phase_mix: {best['phase_mix']:.3f}",
        f"- best reference_weight: {best['reference_weight']:.3f}",
        f"- best input_phase_coupling: {best['input_phase_coupling']:.3f}",
        f"- best risk-pair q10: {best['risk_pair_q10_db']:+.3f} dB",
        f"- best risk-pair min: {best['risk_pair_min_db']:+.3f} dB",
        f"- best risk-pair positive fraction: {best['risk_pair_positive_fraction']:.3f}",
        f"- configs with q10 >= 0: {sum(float(row['risk_pair_q10_db']) >= 0.0 for row in summary_rows)}",
        "- interpretation: this round asks whether tuning phase_mix, reference_weight, and input-phase coupling can remove the remaining negative tail on frame/two_spots.",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
