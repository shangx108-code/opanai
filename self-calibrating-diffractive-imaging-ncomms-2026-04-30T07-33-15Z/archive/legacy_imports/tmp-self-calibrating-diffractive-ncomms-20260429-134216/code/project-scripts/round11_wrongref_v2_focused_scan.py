from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from round6_numpy_passive_d2nn import GOOD_REFERENCE, OUT, SIZE, TEST_SAMPLES, TRAIN_SAMPLES, ensure_dirs, mse, processor_forward, psnr, tile_images
from round7_parameter_scan import phase_from_coeffs
from wrong_reference_designs_v2 import WRONG_REFERENCE_V2_MODES, wrong_reference_v2


NUM_LAYERS = 1
REFERENCE_WEIGHT = 0.16
PHASE_MIXES = [0.14, 0.15, 0.16, 0.17, 0.18]
REPEAT_SEEDS = list(range(8))
CONDITIONS = ["ordinary", "common_path", "noncommon_path", "wrong_reference"]
WRONGREF_V2_MODES = [mode for mode in WRONG_REFERENCE_V2_MODES if mode in {"anti_phase_plus_decoy", "task_matched_decoy"}]


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    fieldnames = list(rows[0].keys())
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def make_input(sample, condition: str, phase_mix: float, wrongref_mode: str):
    object_amp = sample.object_pattern
    object_phase = phase_from_coeffs(sample.coeffs)
    if condition == "ordinary":
        return object_amp, object_phase

    if condition == "common_path":
        ref_amp = GOOD_REFERENCE
        ref_phase = object_phase
    elif condition == "noncommon_path":
        ref_amp = GOOD_REFERENCE
        ref_phase = phase_from_coeffs(sample.coeffs[::-1] * np.array([1.1, -0.9, 1.0, -1.0]))
    elif condition == "wrong_reference":
        ref_amp, ref_phase = wrong_reference_v2(sample, wrongref_mode)
    else:
        raise ValueError(condition)

    new_amp = np.clip(object_amp + REFERENCE_WEIGHT * ref_amp, 0.0, 1.7)
    new_phase = object_phase + phase_mix * ref_phase
    return new_amp, new_phase


def objective(masks: np.ndarray, samples, condition: str, phase_mix: float, wrongref_mode: str) -> float:
    losses = []
    for sample in samples:
        amp, phase = make_input(sample, condition, phase_mix, wrongref_mode)
        pred = processor_forward(amp, phase, masks)
        losses.append(mse(pred, sample.object_pattern))
    return float(np.mean(losses))


def train_condition(condition: str, phase_mix: float, wrongref_mode: str, seed: int):
    rng = np.random.default_rng(seed)
    masks = rng.uniform(-0.15, 0.15, size=(NUM_LAYERS, SIZE, SIZE))
    best_masks = masks.copy()
    best_loss = objective(best_masks, TRAIN_SAMPLES, condition, phase_mix, wrongref_mode)
    history = []
    for step in range(18):
        delta = rng.choice([-1.0, 1.0], size=masks.shape)
        ck = 0.32 / ((step + 1) ** 0.22)
        ak = 0.50 / ((step + 2) ** 0.55)
        plus_loss = objective(masks + ck * delta, TRAIN_SAMPLES, condition, phase_mix, wrongref_mode)
        minus_loss = objective(masks - ck * delta, TRAIN_SAMPLES, condition, phase_mix, wrongref_mode)
        grad = (plus_loss - minus_loss) / (2.0 * ck) * delta
        masks = np.mod(masks - ak * grad + np.pi, 2.0 * np.pi) - np.pi
        train_loss = objective(masks, TRAIN_SAMPLES, condition, phase_mix, wrongref_mode)
        if train_loss < best_loss:
            best_loss = train_loss
            best_masks = masks.copy()
        history.append({"step": step + 1, "train_mse": train_loss})
    return best_masks, history
def evaluate_config(config_id: int, phase_mix: float, wrongref_mode: str, repeat_seed: int):
    trained = {}
    histories = {}
    detail_rows: list[dict[str, object]] = []
    summary_by_condition: dict[str, dict[str, float]] = {}

    for cond_idx, condition in enumerate(CONDITIONS):
        masks, history = train_condition(
            condition=condition,
            phase_mix=phase_mix,
            wrongref_mode=wrongref_mode,
            seed=11100 + config_id * 97 + repeat_seed * 29 + cond_idx,
        )
        trained[condition] = masks
        histories[condition] = history

    preview_rows = []
    for sample in TEST_SAMPLES[:3]:
        row = [sample.object_pattern] + [np.zeros_like(sample.object_pattern) for _ in range(4)]
        for col, condition in enumerate(CONDITIONS, start=1):
            amp, phase = make_input(sample, condition, phase_mix, wrongref_mode)
            row[col] = processor_forward(amp, phase, trained[condition])
        preview_rows.append(row)

    for split_name, samples in [("train", TRAIN_SAMPLES), ("ood", TEST_SAMPLES)]:
        for condition in CONDITIONS:
            scores = []
            mses = []
            for sample in samples:
                amp, phase = make_input(sample, condition, phase_mix, wrongref_mode)
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
                        "reference_weight": REFERENCE_WEIGHT,
                        "phase_mix": round(phase_mix, 4),
                        "wrongref_mode": wrongref_mode,
                        "psnr_db": round(score, 6),
                        "mse": round(err, 8),
                    }
                )
            if split_name == "ood":
                summary_by_condition[condition] = {
                    "ood_mean_psnr_db": float(np.mean(scores)),
                    "ood_mean_mse": float(np.mean(mses)),
                    "train_final_mse": float(histories[condition][-1]["train_mse"]),
                }

    repeat_row = {
        "config_id": config_id,
        "repeat_seed": repeat_seed,
        "num_layers": NUM_LAYERS,
        "reference_weight": REFERENCE_WEIGHT,
        "phase_mix": round(phase_mix, 4),
        "wrongref_mode": wrongref_mode,
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
    }
    return repeat_row, detail_rows, preview_rows, histories


def aggregate_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[int, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(int(row["config_id"]), []).append(row)

    summary_rows = []
    for config_id, bucket in grouped.items():
        base = bucket[0]

        def vals(key: str) -> np.ndarray:
            return np.array([float(row[key]) for row in bucket], dtype=float)

        cmo = vals("common_minus_ordinary_db")
        cmn = vals("common_minus_noncommon_db")
        cmw = vals("common_minus_wrongref_db")

        ranking_score = (
            1.80 * float(np.mean(cmw))
            + 0.45 * float(np.mean(cmo))
            + 0.15 * float(np.mean(cmn))
            - 0.55 * float(np.std(cmw))
            - 0.10 * float(np.std(cmo))
            + 1.00 * min(float(np.min(cmw)), 0.0)
        )

        summary_rows.append(
            {
                "config_id": config_id,
                "num_layers": int(base["num_layers"]),
                "reference_weight": float(base["reference_weight"]),
                "phase_mix": float(base["phase_mix"]),
                "wrongref_mode": str(base["wrongref_mode"]),
                "repeat_count": len(bucket),
                "common_minus_ordinary_db_mean": round(float(np.mean(cmo)), 6),
                "common_minus_ordinary_db_min": round(float(np.min(cmo)), 6),
                "common_minus_ordinary_db_std": round(float(np.std(cmo)), 6),
                "common_minus_noncommon_db_mean": round(float(np.mean(cmn)), 6),
                "common_minus_wrongref_db_mean": round(float(np.mean(cmw)), 6),
                "common_minus_wrongref_db_min": round(float(np.min(cmw)), 6),
                "common_minus_wrongref_db_std": round(float(np.std(cmw)), 6),
                "ranking_score": round(ranking_score, 6),
            }
        )
    return sorted(summary_rows, key=lambda row: row["ranking_score"], reverse=True)


def main() -> None:
    ensure_dirs()
    repeat_rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []
    best_payload = None
    config_id = 0

    for wrongref_mode in WRONGREF_V2_MODES:
        for phase_mix in PHASE_MIXES:
            config_id += 1
            local_rows = []
            local_best_preview = None
            local_best_histories = None
            local_best_score = -1e9
            for repeat_seed in REPEAT_SEEDS:
                repeat_row, local_detail, preview_rows, histories = evaluate_config(
                    config_id=config_id,
                    phase_mix=phase_mix,
                    wrongref_mode=wrongref_mode,
                    repeat_seed=repeat_seed,
                )
                repeat_rows.append(repeat_row)
                local_rows.append(repeat_row)
                detail_rows.extend(local_detail)
                score = 1.2 * float(repeat_row["common_minus_wrongref_db"]) + 0.4 * float(repeat_row["common_minus_ordinary_db"])
                if score > local_best_score:
                    local_best_score = score
                    local_best_preview = preview_rows
                    local_best_histories = histories

            preview_score = (
                1.2 * float(np.mean([float(row["common_minus_wrongref_db"]) for row in local_rows]))
                + 0.4 * float(np.mean([float(row["common_minus_ordinary_db"]) for row in local_rows]))
            )
            if best_payload is None or preview_score > best_payload["preview_score"]:
                best_payload = {
                    "config_id": config_id,
                    "preview_rows": local_best_preview,
                    "histories": local_best_histories,
                    "preview_score": preview_score,
                }

    summary_rows = aggregate_rows(repeat_rows)
    top_rows = summary_rows[:10]

    repeat_csv = OUT / "round11_wrongref_v2_repeat_rows.csv"
    detail_csv = OUT / "round11_wrongref_v2_detail.csv"
    summary_csv = OUT / "round11_wrongref_v2_summary.csv"
    top_csv = OUT / "round11_wrongref_v2_top.csv"
    summary_json = OUT / "round11_wrongref_v2_summary.json"
    summary_md = OUT / "round11_wrongref_v2_summary.md"
    best_panel_png = OUT / "round11_wrongref_v2_best_panel.png"
    best_history_json = OUT / "round11_wrongref_v2_best_history.json"

    write_csv(repeat_rows, repeat_csv)
    write_csv(detail_rows, detail_csv)
    write_csv(summary_rows, summary_csv)
    write_csv(top_rows, top_csv)
    tile_images(best_payload["preview_rows"], ["target", "ordinary", "common", "noncommon", "wrongref"], best_panel_png)
    best_history_json.write_text(json.dumps(best_payload["histories"], indent=2), encoding="utf-8")

    payload = {
        "status": "ok",
        "scan_size": len(summary_rows),
        "repeat_count_per_config": len(REPEAT_SEEDS),
        "fixed_window": {
            "num_layers": NUM_LAYERS,
            "reference_weight": REFERENCE_WEIGHT,
            "phase_mix_grid": PHASE_MIXES,
        },
        "wrongref_v2_modes": WRONGREF_V2_MODES,
        "best_config": top_rows[0],
        "top": top_rows,
        "artifacts": {
            "repeat_csv": str(repeat_csv),
            "detail_csv": str(detail_csv),
            "summary_csv": str(summary_csv),
            "top_csv": str(top_csv),
            "summary_json": str(summary_json),
            "summary_md": str(summary_md),
            "best_panel_png": str(best_panel_png),
            "best_history_json": str(best_history_json),
        },
        "note": "Round11 fixes the ordinary-positive window and tests only two wrong-reference v2 candidates.",
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    best = top_rows[0]
    lines = [
        "# Round 11 Wrong-reference v2 Focused Scan",
        "",
        f"- scan size: {len(summary_rows)} focused configurations",
        f"- repeats per config: {len(REPEAT_SEEDS)}",
        f"- fixed num_layers: {NUM_LAYERS}",
        f"- fixed reference_weight: {REFERENCE_WEIGHT:.2f}",
        f"- phase_mix grid: {', '.join(f'{value:.2f}' for value in PHASE_MIXES)}",
        f"- tested wrongref_v2 modes: {', '.join(WRONGREF_V2_MODES)}",
        f"- best wrongref_v2 mode: {best['wrongref_mode']}",
        f"- best phase_mix: {best['phase_mix']:.3f}",
        f"- mean common minus ordinary: {best['common_minus_ordinary_db_mean']:+.3f} dB",
        f"- min common minus ordinary: {best['common_minus_ordinary_db_min']:+.3f} dB",
        f"- mean common minus wrongref: {best['common_minus_wrongref_db_mean']:+.3f} dB",
        f"- min common minus wrongref: {best['common_minus_wrongref_db_min']:+.3f} dB",
        f"- std common minus wrongref: {best['common_minus_wrongref_db_std']:.3f} dB",
        "- interpretation: this round only tests whether the two strongest wrong-reference v2 decoys can preserve a positive common-minus-wrongref gap inside the current ordinary-positive window",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
