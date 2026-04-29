from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from round6_numpy_passive_d2nn import (
    GOOD_REFERENCE,
    OUT,
    SIZE,
    TEST_SAMPLES,
    TRAIN_SAMPLES,
    WRONG_REFERENCE,
    ensure_dirs,
    mse,
    processor_forward,
    psnr,
    tile_images,
)
from round7_parameter_scan import phase_from_coeffs


NUM_LAYERS = 1
REFERENCE_WEIGHT = 0.16
PHASE_MIXES = [0.10, 0.125, 0.15, 0.175, 0.20]
REPEAT_SEEDS = [0, 1, 2, 3]
CONDITIONS = ["ordinary", "common_path", "noncommon_path", "wrong_reference"]
WRONGREF_MODES = [
    "existing_amp_only",
    "permuted_phase",
    "wrong_amp_permuted_phase",
    "anti_phase",
    "orthogonal_phase",
    "strong_mismatch",
]


def wrongref_phase(sample, mode: str) -> np.ndarray:
    coeffs = sample.coeffs
    if mode == "existing_amp_only":
        return phase_from_coeffs(coeffs)
    if mode == "permuted_phase":
        return phase_from_coeffs(coeffs[::-1] * np.array([1.35, -1.10, 1.20, -1.05]))
    if mode == "wrong_amp_permuted_phase":
        return phase_from_coeffs(coeffs[::-1] * np.array([1.50, -1.25, 1.20, -1.20]))
    if mode == "anti_phase":
        return -1.25 * phase_from_coeffs(coeffs)
    if mode == "orthogonal_phase":
        mixed = np.array([coeffs[1], -coeffs[0], -coeffs[3], coeffs[2]])
        return phase_from_coeffs(1.30 * mixed)
    if mode == "strong_mismatch":
        mixed = np.array([coeffs[2], -coeffs[3], coeffs[0], -coeffs[1]])
        return phase_from_coeffs(1.55 * mixed)
    raise ValueError(mode)


def wrongref_amp(mode: str) -> np.ndarray:
    if mode in {"existing_amp_only", "wrong_amp_permuted_phase", "anti_phase", "strong_mismatch"}:
        return WRONG_REFERENCE
    return GOOD_REFERENCE


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
        ref_amp = wrongref_amp(wrongref_mode)
        ref_phase = wrongref_phase(sample, wrongref_mode)
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


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    fieldnames = list(rows[0].keys())
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


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
            seed=9100 + config_id * 83 + repeat_seed * 17 + cond_idx,
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
            1.50 * float(np.mean(cmw))
            + 0.40 * float(np.mean(cmo))
            + 0.20 * float(np.mean(cmn))
            - 0.45 * float(np.std(cmw))
            - 0.10 * float(np.std(cmo))
            + 0.60 * min(float(np.min(cmw)), 0.0)
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


def render_heatmap(summary_rows: list[dict[str, object]], target: Path) -> None:
    cell_w, cell_h = 110, 38
    width = cell_w * (len(PHASE_MIXES) + 1)
    height = cell_h * (len(WRONGREF_MODES) + 2)
    image = Image.new("RGB", (width, height), (247, 247, 247))
    draw = ImageDraw.Draw(image)
    draw.text((6, 6), "Round9 targeted heatmap (metric=common-wrongref mean)", fill=(10, 10, 10))
    for c, pm in enumerate(PHASE_MIXES):
        draw.text(((c + 1) * cell_w + 10, cell_h), f"p={pm:.3f}", fill=(20, 20, 20))
    for r, mode in enumerate(WRONGREF_MODES):
        label = mode.replace("_", " ")
        draw.text((8, (r + 2) * cell_h + 10), label[:16], fill=(20, 20, 20))
        for c, pm in enumerate(PHASE_MIXES):
            row = next(item for item in summary_rows if item["wrongref_mode"] == mode and abs(float(item["phase_mix"]) - pm) < 1e-9)
            val = float(row["common_minus_wrongref_db_mean"])
            red = 220 if val < 0 else int(max(0, 220 - min(170, val * 220)))
            green = 220 if val > 0 else int(max(0, 220 - min(170, -val * 150)))
            x0 = (c + 1) * cell_w
            y0 = (r + 2) * cell_h
            draw.rectangle((x0 + 2, y0 + 2, x0 + cell_w - 2, y0 + cell_h - 2), fill=(red, green, 186), outline=(118, 118, 118))
            draw.text((x0 + 8, y0 + 11), f"{val:+.2f} dB", fill=(15, 15, 15))
    image.save(target)


def main() -> None:
    ensure_dirs()
    repeat_rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []
    config_index = 0
    best_payload = None

    for wrongref_mode in WRONGREF_MODES:
        for phase_mix in PHASE_MIXES:
            config_index += 1
            local_rows = []
            local_best_score = -1e9
            local_best_preview = None
            local_best_histories = None
            for repeat_seed in REPEAT_SEEDS:
                repeat_row, local_detail, preview_rows, histories = evaluate_config(
                    config_id=config_index,
                    phase_mix=phase_mix,
                    wrongref_mode=wrongref_mode,
                    repeat_seed=repeat_seed,
                )
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
                    "config_id": config_index,
                    "preview_rows": local_best_preview,
                    "histories": local_best_histories,
                    "preview_score": preview_score,
                }

    summary_rows = aggregate_rows(repeat_rows)
    top_rows = summary_rows[:10]

    repeat_csv = OUT / "round9_wrongref_target_repeat_rows.csv"
    detail_csv = OUT / "round9_wrongref_target_detail.csv"
    summary_csv = OUT / "round9_wrongref_target_summary.csv"
    top_csv = OUT / "round9_wrongref_target_top10.csv"
    summary_json = OUT / "round9_wrongref_target_summary.json"
    summary_md = OUT / "round9_wrongref_target_summary.md"
    heatmap_png = OUT / "round9_wrongref_target_heatmap.png"
    best_panel_png = OUT / "round9_wrongref_target_best_panel.png"
    best_history_json = OUT / "round9_wrongref_target_best_history.json"

    write_csv(repeat_rows, repeat_csv)
    write_csv(detail_rows, detail_csv)
    write_csv(summary_rows, summary_csv)
    write_csv(top_rows, top_csv)
    render_heatmap(summary_rows, heatmap_png)
    tile_images(best_payload["preview_rows"], ["target", "ordinary", "common", "noncommon", "wrongref"], best_panel_png)
    best_history_json.write_text(json.dumps(best_payload["histories"], indent=2), encoding="utf-8")

    payload = {
        "status": "ok",
        "scan_size": len(summary_rows),
        "repeat_count_per_config": len(REPEAT_SEEDS),
        "fixed_window": {
            "num_layers": NUM_LAYERS,
            "reference_weight": REFERENCE_WEIGHT,
        },
        "search_space": {
            "phase_mix": PHASE_MIXES,
            "wrongref_mode": WRONGREF_MODES,
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
        "note": "Round9 fixes the round8 stable window and only targets wrong-reference construction plus local phase-mix variation.",
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    best = top_rows[0]
    lines = [
        "# Round 9 Wrong-reference Targeted Scan",
        "",
        f"- scan size: {len(summary_rows)} targeted configurations",
        f"- repeats per config: {len(REPEAT_SEEDS)}",
        f"- fixed num_layers: {NUM_LAYERS}",
        f"- fixed reference_weight: {REFERENCE_WEIGHT:.2f}",
        f"- best wrongref_mode: {best['wrongref_mode']}",
        f"- best phase_mix: {best['phase_mix']:.3f}",
        f"- mean common minus ordinary: {best['common_minus_ordinary_db_mean']:+.3f} dB",
        f"- min common minus ordinary: {best['common_minus_ordinary_db_min']:+.3f} dB",
        f"- mean common minus wrongref: {best['common_minus_wrongref_db_mean']:+.3f} dB",
        f"- min common minus wrongref: {best['common_minus_wrongref_db_min']:+.3f} dB",
        f"- std common minus wrongref: {best['common_minus_wrongref_db_std']:.3f} dB",
        "- interpretation: this round isolates whether a more destructive wrong-reference definition can stabilize Figure 5's exclusion test",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
