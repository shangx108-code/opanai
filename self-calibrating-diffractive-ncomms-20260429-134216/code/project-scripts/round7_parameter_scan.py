from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from round6_numpy_passive_d2nn import (
    LOG,
    OUT,
    SIZE,
    TEST_SAMPLES,
    TRAIN_SAMPLES,
    ensure_dirs,
    make_input as make_input_round6,
    mse,
    normalize,
    processor_forward,
    psnr,
    tile_images,
)


REFERENCE_WEIGHTS = [0.20, 0.40, 0.65, 0.90, 1.10]
PHASE_MIXES = [0.15, 0.35, 0.55]
LAYER_COUNTS = [1, 2, 3]
TRAIN_STEPS = 16
CONDITIONS = ["ordinary", "common_path", "noncommon_path", "wrong_reference"]


def make_input(sample, condition: str, reference_weight: float, phase_mix: float):
    amp, phase = make_input_round6(sample, condition)
    object_amp = sample.object_pattern
    object_phase = phase - 0.35 * (phase - (phase_from_amp(amp) if False else 0))
    # Rebuild from round6's convention while varying only the pilot-related weights.
    if condition == "ordinary":
        return object_amp, phase_from_coeffs(sample.coeffs)
    object_phase = phase_from_coeffs(sample.coeffs)
    if condition == "common_path":
        ref_phase = object_phase
    elif condition == "noncommon_path":
        ref_phase = phase_from_coeffs(sample.coeffs[::-1] * np.array([1.1, -0.9, 1.0, -1.0]))
    else:
        ref_phase = object_phase
    ref_only_amp = np.clip((amp - object_amp) / 0.65, 0.0, 1.0)
    new_amp = np.clip(object_amp + reference_weight * ref_only_amp, 0.0, 1.7)
    new_phase = object_phase + phase_mix * ref_phase
    return new_amp, new_phase


def phase_from_coeffs(coeffs: np.ndarray) -> np.ndarray:
    from round6_numpy_passive_d2nn import BASIS

    phase = np.zeros((SIZE, SIZE), dtype=np.float64)
    for c, b in zip(coeffs, BASIS):
        phase += c * b
    return phase


def objective(masks: np.ndarray, samples, condition: str, reference_weight: float, phase_mix: float) -> float:
    losses = []
    for sample in samples:
        amp, phase = make_input(sample, condition, reference_weight, phase_mix)
        pred = processor_forward(amp, phase, masks)
        losses.append(mse(pred, sample.object_pattern))
    return float(np.mean(losses))


def train_condition(condition: str, num_layers: int, reference_weight: float, phase_mix: float, seed: int):
    rng = np.random.default_rng(seed)
    masks = rng.uniform(-0.15, 0.15, size=(num_layers, SIZE, SIZE))
    history = []
    best_masks = masks.copy()
    best_loss = objective(best_masks, TRAIN_SAMPLES, condition, reference_weight, phase_mix)
    for step in range(TRAIN_STEPS):
        delta = rng.choice([-1.0, 1.0], size=masks.shape)
        ck = 0.32 / ((step + 1) ** 0.22)
        ak = 0.50 / ((step + 2) ** 0.55)
        plus_loss = objective(masks + ck * delta, TRAIN_SAMPLES, condition, reference_weight, phase_mix)
        minus_loss = objective(masks - ck * delta, TRAIN_SAMPLES, condition, reference_weight, phase_mix)
        grad = (plus_loss - minus_loss) / (2.0 * ck) * delta
        masks = np.mod(masks - ak * grad + np.pi, 2.0 * np.pi) - np.pi
        train_loss = objective(masks, TRAIN_SAMPLES, condition, reference_weight, phase_mix)
        if train_loss < best_loss:
            best_loss = train_loss
            best_masks = masks.copy()
        history.append({"step": step + 1, "train_mse": train_loss})
    return best_masks, history


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    fieldnames = list(rows[0].keys())
    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def render_heatmap(scan_rows: list[dict[str, object]], target: Path) -> None:
    from PIL import Image, ImageDraw

    best_phase = max({float(row["phase_mix"]) for row in scan_rows})
    filtered = [row for row in scan_rows if float(row["phase_mix"]) == best_phase]
    cell_w, cell_h = 96, 36
    width = cell_w * (len(REFERENCE_WEIGHTS) + 1)
    height = cell_h * (len(LAYER_COUNTS) + 2)
    image = Image.new("RGB", (width, height), (248, 248, 248))
    draw = ImageDraw.Draw(image)
    draw.text((6, 6), f"Round7 heatmap (phase_mix={best_phase:.2f})", fill=(10, 10, 10))
    for c, rw in enumerate(REFERENCE_WEIGHTS):
        draw.text(((c + 1) * cell_w + 8, cell_h), f"w={rw:.2f}", fill=(20, 20, 20))
    for r, nl in enumerate(LAYER_COUNTS):
        draw.text((8, (r + 2) * cell_h + 8), f"L={nl}", fill=(20, 20, 20))
        for c, rw in enumerate(REFERENCE_WEIGHTS):
            row = next(item for item in filtered if int(item["num_layers"]) == nl and abs(float(item["reference_weight"]) - rw) < 1e-9)
            val = float(row["common_minus_ordinary_db"])
            red = 220 if val < 0 else int(max(0, 220 - min(160, val * 180)))
            green = 220 if val > 0 else int(max(0, 220 - min(160, -val * 120)))
            fill = (red, green, 190)
            x0 = (c + 1) * cell_w
            y0 = (r + 2) * cell_h
            draw.rectangle((x0 + 2, y0 + 2, x0 + cell_w - 2, y0 + cell_h - 2), fill=fill, outline=(120, 120, 120))
            draw.text((x0 + 8, y0 + 10), f"{val:+.2f} dB", fill=(15, 15, 15))
    image.save(target)


def main() -> None:
    ensure_dirs()
    detailed_rows: list[dict[str, object]] = []
    scan_rows: list[dict[str, object]] = []
    best_payload: dict[str, object] | None = None
    best_score = -1e9

    config_index = 0
    for num_layers in LAYER_COUNTS:
        for reference_weight in REFERENCE_WEIGHTS:
            for phase_mix in PHASE_MIXES:
                config_index += 1
                trained = {}
                histories = {}
                for cond_idx, condition in enumerate(CONDITIONS):
                    masks, history = train_condition(
                        condition=condition,
                        num_layers=num_layers,
                        reference_weight=reference_weight,
                        phase_mix=phase_mix,
                        seed=7000 + config_index * 17 + cond_idx,
                    )
                    trained[condition] = masks
                    histories[condition] = history

                summary_by_condition = {}
                preview_rows = []
                for sample in TEST_SAMPLES[:3]:
                    row = [sample.object_pattern] + [np.zeros_like(sample.object_pattern) for _ in range(4)]
                    for col, condition in enumerate(CONDITIONS, start=1):
                        amp, phase = make_input(sample, condition, reference_weight, phase_mix)
                        pred = processor_forward(amp, phase, trained[condition])
                        row[col] = pred
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
                                    "config_id": config_index,
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

                common_minus_ordinary = summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["ordinary"]["ood_mean_psnr_db"]
                common_minus_noncommon = summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["noncommon_path"]["ood_mean_psnr_db"]
                common_minus_wrongref = summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["wrong_reference"]["ood_mean_psnr_db"]
                scan_row = {
                    "config_id": config_index,
                    "num_layers": num_layers,
                    "reference_weight": reference_weight,
                    "phase_mix": phase_mix,
                    "ordinary_ood_mean_psnr_db": round(summary_by_condition["ordinary"]["ood_mean_psnr_db"], 6),
                    "common_ood_mean_psnr_db": round(summary_by_condition["common_path"]["ood_mean_psnr_db"], 6),
                    "noncommon_ood_mean_psnr_db": round(summary_by_condition["noncommon_path"]["ood_mean_psnr_db"], 6),
                    "wrongref_ood_mean_psnr_db": round(summary_by_condition["wrong_reference"]["ood_mean_psnr_db"], 6),
                    "common_minus_ordinary_db": round(common_minus_ordinary, 6),
                    "common_minus_noncommon_db": round(common_minus_noncommon, 6),
                    "common_minus_wrongref_db": round(common_minus_wrongref, 6),
                }
                scan_rows.append(scan_row)

                ranking_score = common_minus_ordinary + 0.35 * common_minus_noncommon + 0.15 * common_minus_wrongref
                if ranking_score > best_score:
                    best_score = ranking_score
                    best_payload = {
                        "config_id": config_index,
                        "scan_row": scan_row,
                        "preview_rows": preview_rows,
                        "histories": histories,
                    }

    scan_rows_sorted = sorted(scan_rows, key=lambda row: row["common_minus_ordinary_db"], reverse=True)
    top_rows = scan_rows_sorted[:10]

    detailed_csv = OUT / "round7_parameter_scan_detail.csv"
    summary_csv = OUT / "round7_parameter_scan_summary.csv"
    top_csv = OUT / "round7_parameter_scan_top10.csv"
    summary_json = OUT / "round7_parameter_scan_summary.json"
    summary_md = OUT / "round7_parameter_scan_summary.md"
    heatmap_png = OUT / "round7_parameter_scan_heatmap.png"
    best_panel_png = OUT / "round7_best_config_panel.png"
    best_history_json = OUT / "round7_best_config_training_history.json"

    write_csv(detailed_rows, detailed_csv)
    write_csv(scan_rows_sorted, summary_csv)
    write_csv(top_rows, top_csv)
    render_heatmap(scan_rows, heatmap_png)
    tile_images(best_payload["preview_rows"], ["target", "ordinary", "common", "noncommon", "wrongref"], best_panel_png)
    best_history_json.write_text(json.dumps(best_payload["histories"], indent=2), encoding="utf-8")

    payload = {
        "status": "ok",
        "scan_size": len(scan_rows),
        "search_space": {
            "num_layers": LAYER_COUNTS,
            "reference_weight": REFERENCE_WEIGHTS,
            "phase_mix": PHASE_MIXES,
            "train_steps": TRAIN_STEPS,
        },
        "best_config": best_payload["scan_row"],
        "top10": top_rows,
        "artifacts": {
            "detail_csv": str(detailed_csv),
            "summary_csv": str(summary_csv),
            "top10_csv": str(top_csv),
            "summary_json": str(summary_json),
            "summary_md": str(summary_md),
            "heatmap_png": str(heatmap_png),
            "best_panel_png": str(best_panel_png),
            "best_history_json": str(best_history_json),
        },
        "note": "Round7 is a full parameter scan over lightweight numpy-based passive D2NN settings for reproducible data completion.",
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Round 7 Parameter Scan",
        "",
        f"- scan size: {len(scan_rows)} configurations",
        f"- best config id: {best_payload['scan_row']['config_id']}",
        f"- best num_layers: {best_payload['scan_row']['num_layers']}",
        f"- best reference_weight: {best_payload['scan_row']['reference_weight']:.2f}",
        f"- best phase_mix: {best_payload['scan_row']['phase_mix']:.2f}",
        f"- best ordinary OOD mean PSNR: {best_payload['scan_row']['ordinary_ood_mean_psnr_db']:.3f} dB",
        f"- best common-path OOD mean PSNR: {best_payload['scan_row']['common_ood_mean_psnr_db']:.3f} dB",
        f"- best common minus ordinary: {best_payload['scan_row']['common_minus_ordinary_db']:+.3f} dB",
        f"- best common minus noncommon: {best_payload['scan_row']['common_minus_noncommon_db']:+.3f} dB",
        f"- best common minus wrongref: {best_payload['scan_row']['common_minus_wrongref_db']:+.3f} dB",
        "- interpretation: full scan completed; use the top table and heatmap before deciding whether Figure 5 has a credible positive direction",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
