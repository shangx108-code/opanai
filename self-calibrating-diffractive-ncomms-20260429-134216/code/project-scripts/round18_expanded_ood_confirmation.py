from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from round6_numpy_passive_d2nn import OUT, RADIUS, SIZE, TEST_SAMPLES, Sample, XX, YY, normalize
from round17_structural_confirmation import CONDITIONS, REPEAT_SEEDS, train_condition
from round16_structural_modes_scan import make_input, mse, percentile, processor_forward, psnr, tile_images


EXPANDED_OOD_NAMES = [
    "disk",
    "two_spots",
    "frame",
    "diamond",
    "corner_dots",
    "half_ring",
    "triple_bars",
    "offcenter_disk",
    "zigzag",
]
NEGATIVE_MARGIN_EPS = 0.0


def make_extended_shape(name: str) -> np.ndarray:
    img = np.zeros((SIZE, SIZE), dtype=np.float64)
    if name == "disk":
        img[RADIUS < 0.42] = 1.0
    elif name == "two_spots":
        img[(XX + 0.35) ** 2 + (YY + 0.12) ** 2 < 0.06] = 1.0
        img[(XX - 0.28) ** 2 + (YY - 0.18) ** 2 < 0.05] = 0.9
    elif name == "frame":
        img[4:20, 4:5] = 1.0
        img[4:20, 19:20] = 1.0
        img[4:5, 4:20] = 1.0
        img[19:20, 4:20] = 1.0
        img[9:15, 9:15] = 0.7
    elif name == "diamond":
        img[np.abs(XX) + np.abs(YY) < 0.60] = 1.0
        img[np.abs(XX) + np.abs(YY) < 0.30] = 0.45
    elif name == "corner_dots":
        for cx, cy, radius, amp in [(-0.50, -0.50, 0.032, 1.0), (0.50, -0.50, 0.032, 0.95), (-0.50, 0.50, 0.032, 0.9), (0.50, 0.50, 0.032, 0.85)]:
            img[(XX - cx) ** 2 + (YY - cy) ** 2 < radius] = amp
    elif name == "half_ring":
        img[(RADIUS > 0.32) & (RADIUS < 0.50) & (YY < 0.25)] = 1.0
        img[(RADIUS > 0.32) & (RADIUS < 0.50) & (YY < -0.10) & (np.abs(XX) < 0.35)] = 0.4
    elif name == "triple_bars":
        img[4:20, 5:7] = 1.0
        img[7:17, 11:13] = 0.85
        img[4:20, 17:19] = 0.7
    elif name == "offcenter_disk":
        img[(XX - 0.18) ** 2 + (YY + 0.12) ** 2 < 0.20] = 1.0
        img[(XX + 0.30) ** 2 + (YY - 0.25) ** 2 < 0.025] = 0.55
    elif name == "zigzag":
        for row in range(4, SIZE - 4):
            col = 4 + ((row - 4) % 6) * 2
            img[row, min(col, SIZE - 5)] = 1.0
            img[row, min(col + 1, SIZE - 5)] = 0.7
    else:
        raise ValueError(name)
    return normalize(np.clip(img, 0.0, 1.0))


def build_expanded_samples() -> list[Sample]:
    base_by_name = {sample.name: sample for sample in TEST_SAMPLES}
    samples: list[Sample] = [base_by_name[name] for name in ["disk", "two_spots", "frame"]]
    local = np.random.default_rng(181)
    extra_names = [name for name in EXPANDED_OOD_NAMES if name not in base_by_name]
    for idx, name in enumerate(extra_names):
        coeff_scale = 1.28
        coeffs = local.uniform(-coeff_scale, coeff_scale, size=4)
        coeffs += 0.05 * np.array([np.cos(idx), np.sin(idx), (-1) ** idx, 0.5 - 0.1 * idx])
        samples.append(Sample(name=name, object_pattern=make_extended_shape(name), coeffs=coeffs))
    return samples


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    fieldnames = list(rows[0].keys())
    with target.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize_sample_margins(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[float]] = {}
    grouped_cmo: dict[str, list[float]] = {}
    for row in rows:
        grouped.setdefault(str(row["sample"]), []).append(float(row["common_minus_wrongref_db"]))
        grouped_cmo.setdefault(str(row["sample"]), []).append(float(row["common_minus_ordinary_db"]))
    summary_rows = []
    for sample in sorted(grouped):
        margins = grouped[sample]
        ordinary_margins = grouped_cmo[sample]
        summary_rows.append(
            {
                "sample": sample,
                "repeat_count": len(margins),
                "common_minus_wrongref_db_mean": round(float(np.mean(margins)), 6),
                "common_minus_wrongref_db_min": round(float(np.min(margins)), 6),
                "common_minus_wrongref_positive_fraction": round(float(np.mean(np.array(margins) > NEGATIVE_MARGIN_EPS)), 6),
                "common_minus_ordinary_db_mean": round(float(np.mean(ordinary_margins)), 6),
                "common_minus_ordinary_db_min": round(float(np.min(ordinary_margins)), 6),
            }
        )
    return summary_rows


def main() -> None:
    samples = build_expanded_samples()
    repeat_rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []
    risk_rows: list[dict[str, object]] = []
    best_preview = None
    best_preview_score = -1e9

    for repeat_seed in REPEAT_SEEDS:
        trained = {}
        summary_by_condition: dict[str, dict[str, float]] = {}
        for cond_idx, condition in enumerate(CONDITIONS):
            masks, _history = train_condition(condition=condition, seed=17100 + repeat_seed * 37 + cond_idx)
            trained[condition] = masks

        preview_rows = []
        preview_names = ["disk", "frame", "diamond", "zigzag"]
        for sample in [sample for sample in samples if sample.name in preview_names]:
            row = [sample.object_pattern] + [np.zeros_like(sample.object_pattern) for _ in range(4)]
            for col, condition in enumerate(CONDITIONS, start=1):
                amp, phase = make_input(sample, condition, "sparse_tracker_decoy", "occupancy_guarded")
                row[col] = processor_forward(amp, phase, trained[condition])
            preview_rows.append(row)

        pair_margins = []
        for condition in CONDITIONS:
            scores = []
            mses = []
            for sample in samples:
                amp, phase = make_input(sample, condition, "sparse_tracker_decoy", "occupancy_guarded")
                pred = processor_forward(amp, phase, trained[condition])
                err = mse(pred, sample.object_pattern)
                score = psnr(pred, sample.object_pattern)
                scores.append(score)
                mses.append(err)
                detail_rows.append(
                    {
                        "repeat_seed": repeat_seed,
                        "sample": sample.name,
                        "condition": condition,
                        "psnr_db": round(score, 6),
                        "mse": round(err, 8),
                    }
                )
            summary_by_condition[condition] = {
                "ood_mean_psnr_db": float(np.mean(scores)),
                "ood_mean_mse": float(np.mean(mses)),
            }

        for sample in samples:
            bucket = {
                condition: next(
                    float(row["psnr_db"])
                    for row in detail_rows
                    if int(row["repeat_seed"]) == repeat_seed and str(row["sample"]) == sample.name and str(row["condition"]) == condition
                )
                for condition in CONDITIONS
            }
            cmw = bucket["common_path"] - bucket["wrong_reference"]
            cmo = bucket["common_path"] - bucket["ordinary"]
            pair_margins.append(cmw)
            risk_rows.append(
                {
                    "repeat_seed": repeat_seed,
                    "sample": sample.name,
                    "common_minus_wrongref_db": round(cmw, 6),
                    "common_minus_ordinary_db": round(cmo, 6),
                }
            )

        repeat_row = {
            "repeat_seed": repeat_seed,
            "expanded_ood_count": len(samples),
            "common_minus_ordinary_db": round(
                summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["ordinary"]["ood_mean_psnr_db"], 6
            ),
            "common_minus_wrongref_db": round(
                summary_by_condition["common_path"]["ood_mean_psnr_db"] - summary_by_condition["wrong_reference"]["ood_mean_psnr_db"], 6
            ),
            "expanded_pair_q10_repeat": round(percentile(pair_margins, 0.10), 6),
            "expanded_pair_min_repeat": round(min(pair_margins), 6),
            "expanded_pair_positive_fraction_repeat": round(sum(value > NEGATIVE_MARGIN_EPS for value in pair_margins) / len(pair_margins), 6),
        }
        repeat_rows.append(repeat_row)

        preview_score = 2.0 * float(repeat_row["expanded_pair_q10_repeat"]) + 0.2 * float(repeat_row["common_minus_ordinary_db"])
        if preview_score > best_preview_score:
            best_preview_score = preview_score
            best_preview = preview_rows

    all_pair_margins = [float(row["common_minus_wrongref_db"]) for row in risk_rows]
    all_cmo = [float(row["common_minus_ordinary_db"]) for row in repeat_rows]
    all_cmw = [float(row["common_minus_wrongref_db"]) for row in repeat_rows]
    sample_summary_rows = summarize_sample_margins(risk_rows)
    worst_samples = sorted(sample_summary_rows, key=lambda row: (float(row["common_minus_wrongref_db_min"]), float(row["common_minus_wrongref_db_mean"])))[:4]

    summary = {
        "confirmed_structure": {
            "wrongref_mode": "sparse_tracker_decoy",
            "encoding_mode": "occupancy_guarded",
        },
        "repeat_count": len(REPEAT_SEEDS),
        "expanded_ood_names": EXPANDED_OOD_NAMES,
        "expanded_ood_count": len(EXPANDED_OOD_NAMES),
        "expanded_pair_q10_db": round(percentile(all_pair_margins, 0.10), 6),
        "expanded_pair_min_db": round(min(all_pair_margins), 6),
        "expanded_pair_positive_fraction": round(sum(value > NEGATIVE_MARGIN_EPS for value in all_pair_margins) / len(all_pair_margins), 6),
        "common_minus_ordinary_db_mean": round(float(np.mean(all_cmo)), 6),
        "common_minus_ordinary_db_min": round(float(np.min(all_cmo)), 6),
        "common_minus_wrongref_db_mean": round(float(np.mean(all_cmw)), 6),
        "common_minus_wrongref_db_min": round(float(np.min(all_cmw)), 6),
        "worst_samples": worst_samples,
    }

    repeat_csv = OUT / "round18_expanded_ood_repeat_rows.csv"
    detail_csv = OUT / "round18_expanded_ood_detail.csv"
    pair_csv = OUT / "round18_expanded_ood_pair_rows.csv"
    sample_summary_csv = OUT / "round18_expanded_ood_sample_summary.csv"
    summary_json = OUT / "round18_expanded_ood_summary.json"
    summary_md = OUT / "round18_expanded_ood_summary.md"
    preview_png = OUT / "round18_expanded_ood_best_panel.png"

    write_csv(repeat_rows, repeat_csv)
    write_csv(detail_rows, detail_csv)
    write_csv(risk_rows, pair_csv)
    write_csv(sample_summary_rows, sample_summary_csv)
    summary_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    tile_images(best_preview, ["target", "ordinary", "common", "noncommon", "wrongref"], preview_png)

    lines = [
        "# Round 18 Expanded OOD Confirmation",
        "",
        "- confirmed structure: sparse_tracker_decoy + occupancy_guarded",
        f"- repeats: {len(REPEAT_SEEDS)}",
        f"- expanded OOD count: {len(EXPANDED_OOD_NAMES)}",
        f"- expanded pair q10: {summary['expanded_pair_q10_db']:+.3f} dB",
        f"- expanded pair min: {summary['expanded_pair_min_db']:+.3f} dB",
        f"- expanded pair positive fraction: {summary['expanded_pair_positive_fraction']:.3f}",
        f"- common minus ordinary mean: {summary['common_minus_ordinary_db_mean']:+.3f} dB",
        f"- common minus wrongref mean: {summary['common_minus_wrongref_db_mean']:+.3f} dB",
        f"- worst sample: {worst_samples[0]['sample']} with min {worst_samples[0]['common_minus_wrongref_db_min']:+.3f} dB" if worst_samples else "- worst sample: none",
        "- interpretation: this round asks whether the round17 upgraded Figure 5 reading survives a broader unseen-shape OOD set without changing the confirmed structure.",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
