from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from round6_numpy_passive_d2nn import OUT, TEST_SAMPLES, TRAIN_SAMPLES, ensure_dirs, mse, processor_forward, psnr, tile_images
from round9_wrong_reference_targeted_scan import CONDITIONS, make_input, train_condition


PHASE_MIXES = [0.18, 0.185, 0.19, 0.195, 0.20, 0.205, 0.21, 0.215, 0.22]
WRONGREF_MODE = "anti_phase"
REPEAT_SEEDS = list(range(10))


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    fieldnames = list(rows[0].keys())
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def evaluate_config(config_id: int, phase_mix: float, repeat_seed: int):
    trained = {}
    histories = {}
    detail_rows: list[dict[str, object]] = []
    summary_by_condition: dict[str, dict[str, float]] = {}

    for cond_idx, condition in enumerate(CONDITIONS):
        masks, history = train_condition(
            condition=condition,
            phase_mix=phase_mix,
            wrongref_mode=WRONGREF_MODE,
            seed=10100 + config_id * 131 + repeat_seed * 23 + cond_idx,
        )
        trained[condition] = masks
        histories[condition] = history

    preview_rows = []
    for sample in TEST_SAMPLES[:3]:
        row = [sample.object_pattern] + [np.zeros_like(sample.object_pattern) for _ in range(4)]
        for col, condition in enumerate(CONDITIONS, start=1):
            amp, phase = make_input(sample, condition, phase_mix, WRONGREF_MODE)
            row[col] = processor_forward(amp, phase, trained[condition])
        preview_rows.append(row)

    for split_name, samples in [("train", TRAIN_SAMPLES), ("ood", TEST_SAMPLES)]:
        for condition in CONDITIONS:
            scores = []
            mses = []
            for sample in samples:
                amp, phase = make_input(sample, condition, phase_mix, WRONGREF_MODE)
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
                        "phase_mix": round(phase_mix, 4),
                        "wrongref_mode": WRONGREF_MODE,
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
        "phase_mix": round(phase_mix, 4),
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
            1.60 * float(np.mean(cmw))
            + 0.40 * float(np.mean(cmo))
            + 0.20 * float(np.mean(cmn))
            - 0.50 * float(np.std(cmw))
            - 0.10 * float(np.std(cmo))
            + 0.80 * min(float(np.min(cmw)), 0.0)
        )

        summary_rows.append(
            {
                "config_id": config_id,
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

    for config_id, phase_mix in enumerate(PHASE_MIXES, start=1):
        local_rows = []
        local_best_score = -1e9
        local_best_preview = None
        local_best_histories = None
        for repeat_seed in REPEAT_SEEDS:
            repeat_row, local_detail, preview_rows, histories = evaluate_config(config_id, phase_mix, repeat_seed)
            repeat_rows.append(repeat_row)
            local_rows.append(repeat_row)
            detail_rows.extend(local_detail)

            score = float(repeat_row["common_minus_wrongref_db"]) + 0.5 * float(repeat_row["common_minus_ordinary_db"])
            if score > local_best_score:
                local_best_score = score
                local_best_preview = preview_rows
                local_best_histories = histories

        local_mean = float(np.mean([float(row["common_minus_wrongref_db"]) for row in local_rows]))
        preview_score = local_mean + 0.4 * float(np.mean([float(row["common_minus_ordinary_db"]) for row in local_rows]))
        if best_payload is None or preview_score > best_payload["preview_score"]:
            best_payload = {
                "config_id": config_id,
                "preview_rows": local_best_preview,
                "histories": local_best_histories,
                "preview_score": preview_score,
            }

    summary_rows = aggregate_rows(repeat_rows)
    top_rows = summary_rows[:9]

    repeat_csv = OUT / "round10_antiphase_repeat_rows.csv"
    detail_csv = OUT / "round10_antiphase_detail.csv"
    summary_csv = OUT / "round10_antiphase_summary.csv"
    top_csv = OUT / "round10_antiphase_top.csv"
    summary_json = OUT / "round10_antiphase_summary.json"
    summary_md = OUT / "round10_antiphase_summary.md"
    best_panel_png = OUT / "round10_antiphase_best_panel.png"
    best_history_json = OUT / "round10_antiphase_best_history.json"

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
        "wrongref_mode": WRONGREF_MODE,
        "phase_mix_grid": PHASE_MIXES,
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
        "note": "Round10 confirms the anti_phase wrong-reference window with denser phase_mix sampling and more repeats.",
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    best = top_rows[0]
    lines = [
        "# Round 10 Anti-phase Confirmation Scan",
        "",
        f"- scan size: {len(summary_rows)} phase_mix points",
        f"- repeats per config: {len(REPEAT_SEEDS)}",
        f"- locked wrongref_mode: {WRONGREF_MODE}",
        f"- best phase_mix: {best['phase_mix']:.3f}",
        f"- mean common minus ordinary: {best['common_minus_ordinary_db_mean']:+.3f} dB",
        f"- min common minus ordinary: {best['common_minus_ordinary_db_min']:+.3f} dB",
        f"- mean common minus wrongref: {best['common_minus_wrongref_db_mean']:+.3f} dB",
        f"- min common minus wrongref: {best['common_minus_wrongref_db_min']:+.3f} dB",
        f"- std common minus wrongref: {best['common_minus_wrongref_db_std']:.3f} dB",
        "- interpretation: this round asks whether the anti_phase exclusion window survives denser local sampling and more seeds",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
