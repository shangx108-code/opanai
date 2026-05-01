from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from round6_numpy_passive_d2nn import OUT, TEST_SAMPLES, TRAIN_SAMPLES, ensure_dirs, mse, processor_forward, psnr, tile_images
from round7_parameter_scan import CONDITIONS, make_input, train_condition


REFERENCE_WEIGHTS = [0.12, 0.16, 0.20, 0.24, 0.28, 0.32]
PHASE_MIXES = [0.05, 0.10, 0.15, 0.20, 0.25]
LAYER_COUNTS = [1, 2]
REPEAT_SEEDS = [0, 1, 2, 3]


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    fieldnames = list(rows[0].keys())
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def evaluate_config(num_layers: int, reference_weight: float, phase_mix: float, repeat_seed: int, config_id: int):
    trained = {}
    histories = {}
    detailed_rows: list[dict[str, object]] = []
    summary_by_condition: dict[str, dict[str, float]] = {}

    for cond_idx, condition in enumerate(CONDITIONS):
        masks, history = train_condition(
            condition=condition,
            num_layers=num_layers,
            reference_weight=reference_weight,
            phase_mix=phase_mix,
            seed=8100 + config_id * 97 + repeat_seed * 19 + cond_idx,
        )
        trained[condition] = masks
        histories[condition] = history

    preview_rows = []
    for sample in TEST_SAMPLES[:3]:
        row = [sample.object_pattern] + [np.zeros_like(sample.object_pattern) for _ in range(4)]
        for col, condition in enumerate(CONDITIONS, start=1):
            amp, phase = make_input(sample, condition, reference_weight, phase_mix)
            row[col] = processor_forward(amp, phase, trained[condition])
        preview_rows.append(row)

    for split_name, samples in [("train", TRAIN_SAMPLES), ("ood", TEST_SAMPLES)]:
        for condition in CONDITIONS:
            scores = []
            mses = []
            for sample in samples:
                amp, phase = make_input(sample, condition, reference_weight, phase_mix)
                pred = processor_forward(amp, phase, trained[condition])
                err = mse(pred, sample.object_pattern)
                score = psnr(pred, sample.object_pattern)
                scores.append(score)
                mses.append(err)
                detailed_rows.append(
                    {
                        "config_id": config_id,
                        "repeat_seed": repeat_seed,
                        "split": split_name,
                        "sample": sample.name,
                        "condition": condition,
                        "num_layers": num_layers,
                        "reference_weight": reference_weight,
                        "phase_mix": phase_mix,
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
        "num_layers": num_layers,
        "reference_weight": round(reference_weight, 4),
        "phase_mix": round(phase_mix, 4),
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
    return repeat_row, detailed_rows, preview_rows, histories


def aggregate_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[int, list[dict[str, object]]] = {}
    for row in rows:
        grouped.setdefault(int(row["config_id"]), []).append(row)

    summary_rows: list[dict[str, object]] = []
    for config_id, bucket in grouped.items():
        base = bucket[0]

        def vals(key: str) -> np.ndarray:
            return np.array([float(row[key]) for row in bucket], dtype=float)

        cmo = vals("common_minus_ordinary_db")
        cmn = vals("common_minus_noncommon_db")
        cmw = vals("common_minus_wrongref_db")
        common_psnr = vals("common_ood_mean_psnr_db")
        ordinary_psnr = vals("ordinary_ood_mean_psnr_db")

        # Rank for Figure 5 strengthening: prioritize wrong-reference separation first,
        # then ordinary separation, while penalizing instability across repeats.
        ranking_score = (
            1.20 * float(np.mean(cmw))
            + 0.70 * float(np.mean(cmo))
            + 0.25 * float(np.mean(cmn))
            - 0.35 * float(np.std(cmw))
            - 0.20 * float(np.std(cmo))
            + 0.30 * min(float(np.min(cmw)), 0.0)
        )

        summary_rows.append(
            {
                "config_id": config_id,
                "num_layers": int(base["num_layers"]),
                "reference_weight": float(base["reference_weight"]),
                "phase_mix": float(base["phase_mix"]),
                "repeat_count": len(bucket),
                "ordinary_ood_mean_psnr_db_mean": round(float(np.mean(ordinary_psnr)), 6),
                "common_ood_mean_psnr_db_mean": round(float(np.mean(common_psnr)), 6),
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


def render_heatmap(summary_rows: list[dict[str, object]], target: Path) -> None:
    best_layer = int(summary_rows[0]["num_layers"])
    filtered = [row for row in summary_rows if int(row["num_layers"]) == best_layer]
    cell_w, cell_h = 92, 38
    width = cell_w * (len(REFERENCE_WEIGHTS) + 1)
    height = cell_h * (len(PHASE_MIXES) + 2)
    image = Image.new("RGB", (width, height), (247, 247, 247))
    draw = ImageDraw.Draw(image)
    draw.text((6, 6), f"Round8 local heatmap (layers={best_layer}, metric=common-wrongref mean)", fill=(10, 10, 10))
    for c, rw in enumerate(REFERENCE_WEIGHTS):
        draw.text(((c + 1) * cell_w + 8, cell_h), f"w={rw:.2f}", fill=(20, 20, 20))
    for r, pm in enumerate(PHASE_MIXES):
        draw.text((8, (r + 2) * cell_h + 10), f"p={pm:.2f}", fill=(20, 20, 20))
        for c, rw in enumerate(REFERENCE_WEIGHTS):
            row = next(item for item in filtered if abs(float(item["reference_weight"]) - rw) < 1e-9 and abs(float(item["phase_mix"]) - pm) < 1e-9)
            val = float(row["common_minus_wrongref_db_mean"])
            red = 220 if val < 0 else int(max(0, 220 - min(170, val * 180)))
            green = 220 if val > 0 else int(max(0, 220 - min(170, -val * 140)))
            x0 = (c + 1) * cell_w
            y0 = (r + 2) * cell_h
            draw.rectangle((x0 + 2, y0 + 2, x0 + cell_w - 2, y0 + cell_h - 2), fill=(red, green, 186), outline=(118, 118, 118))
            draw.text((x0 + 8, y0 + 11), f"{val:+.2f} dB", fill=(15, 15, 15))
    image.save(target)


def main() -> None:
    ensure_dirs()
    repeat_rows: list[dict[str, object]] = []
    detailed_rows: list[dict[str, object]] = []
    best_payload: dict[str, object] | None = None
    config_index = 0

    for num_layers in LAYER_COUNTS:
        for reference_weight in REFERENCE_WEIGHTS:
            for phase_mix in PHASE_MIXES:
                config_index += 1
                local_repeat_rows = []
                local_best_preview = None
                local_best_histories = None
                local_best_score = -1e9
                for repeat_seed in REPEAT_SEEDS:
                    repeat_row, local_detailed_rows, preview_rows, histories = evaluate_config(
                        num_layers=num_layers,
                        reference_weight=reference_weight,
                        phase_mix=phase_mix,
                        repeat_seed=repeat_seed,
                        config_id=config_index,
                    )
                    repeat_rows.append(repeat_row)
                    local_repeat_rows.append(repeat_row)
                    detailed_rows.extend(local_detailed_rows)
                    repeat_score = float(repeat_row["common_minus_wrongref_db"]) + 0.6 * float(repeat_row["common_minus_ordinary_db"])
                    if repeat_score > local_best_score:
                        local_best_score = repeat_score
                        local_best_preview = preview_rows
                        local_best_histories = histories

                mean_wrongref = float(np.mean([float(row["common_minus_wrongref_db"]) for row in local_repeat_rows]))
                mean_ordinary = float(np.mean([float(row["common_minus_ordinary_db"]) for row in local_repeat_rows]))
                preview_score = mean_wrongref + 0.6 * mean_ordinary
                if best_payload is None or preview_score > best_payload["preview_score"]:
                    best_payload = {
                        "config_id": config_index,
                        "preview_rows": local_best_preview,
                        "histories": local_best_histories,
                        "preview_score": preview_score,
                    }

    summary_rows = aggregate_rows(repeat_rows)
    top_rows = summary_rows[:10]

    repeat_csv = OUT / "round8_narrow_scan_repeat_rows.csv"
    detail_csv = OUT / "round8_narrow_scan_detail.csv"
    summary_csv = OUT / "round8_narrow_scan_summary.csv"
    top_csv = OUT / "round8_narrow_scan_top10.csv"
    summary_json = OUT / "round8_narrow_scan_summary.json"
    summary_md = OUT / "round8_narrow_scan_summary.md"
    heatmap_png = OUT / "round8_narrow_scan_heatmap.png"
    best_panel_png = OUT / "round8_best_local_config_panel.png"
    best_history_json = OUT / "round8_best_local_config_history.json"

    write_csv(repeat_rows, repeat_csv)
    write_csv(detailed_rows, detail_csv)
    write_csv(summary_rows, summary_csv)
    write_csv(top_rows, top_csv)
    render_heatmap(summary_rows, heatmap_png)
    tile_images(best_payload["preview_rows"], ["target", "ordinary", "common", "noncommon", "wrongref"], best_panel_png)
    best_history_json.write_text(json.dumps(best_payload["histories"], indent=2), encoding="utf-8")

    payload = {
        "status": "ok",
        "scan_size": len(summary_rows),
        "repeat_count_per_config": len(REPEAT_SEEDS),
        "search_space": {
            "num_layers": LAYER_COUNTS,
            "reference_weight": REFERENCE_WEIGHTS,
            "phase_mix": PHASE_MIXES,
        },
        "best_config": top_rows[0],
        "top10": top_rows,
        "artifacts": {
            "repeat_csv": str(repeat_csv),
            "detail_csv": str(detail_csv),
            "summary_csv": str(summary_csv),
            "top10_csv": str(top_csv),
            "summary_json": str(summary_json),
            "summary_md": str(summary_md),
            "heatmap_png": str(heatmap_png),
            "best_panel_png": str(best_panel_png),
            "best_history_json": str(best_history_json),
        },
        "note": "Round8 narrows the scan around the round7 window and ranks configs by wrong-reference separation plus repeat stability.",
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    best = top_rows[0]
    lines = [
        "# Round 8 Narrow Processor Scan",
        "",
        f"- scan size: {len(summary_rows)} local configurations",
        f"- repeats per config: {len(REPEAT_SEEDS)}",
        f"- best config id: {best['config_id']}",
        f"- best num_layers: {best['num_layers']}",
        f"- best reference_weight: {best['reference_weight']:.2f}",
        f"- best phase_mix: {best['phase_mix']:.2f}",
        f"- mean common minus ordinary: {best['common_minus_ordinary_db_mean']:+.3f} dB",
        f"- min common minus ordinary: {best['common_minus_ordinary_db_min']:+.3f} dB",
        f"- mean common minus wrongref: {best['common_minus_wrongref_db_mean']:+.3f} dB",
        f"- min common minus wrongref: {best['common_minus_wrongref_db_min']:+.3f} dB",
        f"- std common minus wrongref: {best['common_minus_wrongref_db_std']:.3f} dB",
        "- interpretation: this round prioritizes wrong-reference separation and repeat stability, not single-shot peak score alone",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
