from __future__ import annotations

import csv
import json
import math
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path("/workspace/self-calibrating-diffractive-ncomms")
OUT = ROOT / "outputs"
SUMMARY_CSV = OUT / "round11_wrongref_v2_summary.csv"
REPEAT_CSV = OUT / "round11_wrongref_v2_repeat_rows.csv"
DETAIL_CSV = OUT / "round11_wrongref_v2_detail.csv"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def to_float(row: dict[str, str], key: str) -> float:
    return float(row[key])


def percentile(values: list[float], q: float) -> float:
    if not values:
        raise ValueError("percentile requires non-empty values")
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


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def std(values: list[float]) -> float:
    if not values:
        return 0.0
    mu = mean(values)
    return math.sqrt(sum((value - mu) ** 2 for value in values) / len(values))


def pick_best_config(summary_rows: list[dict[str, str]]) -> dict[str, str]:
    return max(summary_rows, key=lambda row: float(row["ranking_score"]))


def build_repeat_stats(repeat_rows: list[dict[str, str]], config_id: str) -> list[dict[str, object]]:
    rows = [row for row in repeat_rows if row["config_id"] == config_id]
    stats = []
    for row in rows:
        cmo = to_float(row, "common_minus_ordinary_db")
        cmw = to_float(row, "common_minus_wrongref_db")
        stats.append(
            {
                "repeat_seed": int(row["repeat_seed"]),
                "common_minus_ordinary_db": cmo,
                "common_minus_wrongref_db": cmw,
                "common_minus_noncommon_db": to_float(row, "common_minus_noncommon_db"),
                "sign_common_minus_ordinary": "positive" if cmo > 0 else "nonpositive",
                "sign_common_minus_wrongref": "positive" if cmw > 0 else "nonpositive",
            }
        )
    return sorted(stats, key=lambda item: item["repeat_seed"])


def build_sample_stats(detail_rows: list[dict[str, str]], config_id: str) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[str, object]]:
    filtered = [row for row in detail_rows if row["config_id"] == config_id and row["split"] == "ood"]
    by_repeat_sample: dict[tuple[str, str], dict[str, float]] = defaultdict(dict)
    for row in filtered:
        key = (row["repeat_seed"], row["sample"])
        by_repeat_sample[key][row["condition"]] = float(row["psnr_db"])

    sample_margins: dict[str, list[float]] = defaultdict(list)
    sample_ordinary_margins: dict[str, list[float]] = defaultdict(list)
    worst_case_counter: Counter[str] = Counter()
    repeat_worst_rows: list[dict[str, object]] = []

    for repeat_seed in sorted({key[0] for key in by_repeat_sample.keys()}, key=int):
        worst_sample = None
        worst_margin = None
        for sample in sorted({key[1] for key in by_repeat_sample.keys()}):
            bucket = by_repeat_sample.get((repeat_seed, sample))
            if not bucket or set(bucket.keys()) != {"ordinary", "common_path", "noncommon_path", "wrong_reference"}:
                continue
            cmw = bucket["common_path"] - bucket["wrong_reference"]
            cmo = bucket["common_path"] - bucket["ordinary"]
            sample_margins[sample].append(cmw)
            sample_ordinary_margins[sample].append(cmo)
            if worst_margin is None or cmw < worst_margin:
                worst_margin = cmw
                worst_sample = sample
        if worst_sample is not None and worst_margin is not None:
            worst_case_counter[worst_sample] += 1
            repeat_worst_rows.append(
                {
                    "repeat_seed": int(repeat_seed),
                    "worst_sample_common_minus_wrongref_db": worst_margin,
                    "worst_sample": worst_sample,
                }
            )

    sample_stats = []
    for sample, margins in sorted(sample_margins.items()):
        ordinary_margins = sample_ordinary_margins[sample]
        sample_stats.append(
            {
                "sample": sample,
                "repeat_count": len(margins),
                "common_minus_wrongref_db_mean": round(mean(margins), 6),
                "common_minus_wrongref_db_min": round(min(margins), 6),
                "common_minus_wrongref_db_q10": round(percentile(margins, 0.10), 6),
                "common_minus_wrongref_db_median": round(percentile(margins, 0.50), 6),
                "common_minus_wrongref_db_max": round(max(margins), 6),
                "common_minus_wrongref_positive_rate": round(sum(value > 0 for value in margins) / len(margins), 6),
                "common_minus_wrongref_db_std": round(std(margins), 6),
                "common_minus_ordinary_db_mean": round(mean(ordinary_margins), 6),
                "common_minus_ordinary_db_min": round(min(ordinary_margins), 6),
                "common_minus_ordinary_positive_rate": round(sum(value > 0 for value in ordinary_margins) / len(ordinary_margins), 6),
            }
        )

    all_cmw = [value for values in sample_margins.values() for value in values]
    all_cmo = [value for values in sample_ordinary_margins.values() for value in values]
    global_stats = {
        "sample_repeat_pair_count": len(all_cmw),
        "common_minus_wrongref_db_mean": round(mean(all_cmw), 6),
        "common_minus_wrongref_db_min": round(min(all_cmw), 6),
        "common_minus_wrongref_db_q10": round(percentile(all_cmw, 0.10), 6),
        "common_minus_wrongref_db_median": round(percentile(all_cmw, 0.50), 6),
        "common_minus_wrongref_positive_rate": round(sum(value > 0 for value in all_cmw) / len(all_cmw), 6),
        "common_minus_ordinary_db_mean": round(mean(all_cmo), 6),
        "common_minus_ordinary_db_min": round(min(all_cmo), 6),
        "common_minus_ordinary_positive_rate": round(sum(value > 0 for value in all_cmo) / len(all_cmo), 6),
        "worst_sample_frequency": dict(sorted(worst_case_counter.items())),
        "most_frequent_worst_sample": worst_case_counter.most_common(1)[0][0] if worst_case_counter else None,
    }
    return sample_stats, repeat_worst_rows, global_stats


def main() -> None:
    summary_rows = read_csv(SUMMARY_CSV)
    repeat_rows = read_csv(REPEAT_CSV)
    detail_rows = read_csv(DETAIL_CSV)
    best = pick_best_config(summary_rows)
    config_id = best["config_id"]

    repeat_stats = build_repeat_stats(repeat_rows, config_id)
    sample_stats, repeat_worst_rows, global_stats = build_sample_stats(detail_rows, config_id)

    repeat_positive_count = sum(row["common_minus_wrongref_db"] > 0 for row in repeat_stats)
    repeat_payload = {
        "repeat_count": len(repeat_stats),
        "common_minus_wrongref_all_positive": repeat_positive_count == len(repeat_stats),
        "common_minus_wrongref_positive_repeat_count": repeat_positive_count,
        "common_minus_wrongref_positive_repeat_fraction": round(repeat_positive_count / len(repeat_stats), 6),
        "common_minus_wrongref_worst_repeat_db": round(min(row["common_minus_wrongref_db"] for row in repeat_stats), 6),
        "common_minus_ordinary_all_positive": all(row["common_minus_ordinary_db"] > 0 for row in repeat_stats),
    }

    sample_csv = OUT / "round12_margin_sample_stats.csv"
    repeat_csv = OUT / "round12_margin_repeat_stats.csv"
    repeat_worst_csv = OUT / "round12_margin_repeat_worst_samples.csv"
    summary_json = OUT / "round12_margin_summary.json"
    summary_md = OUT / "round12_margin_summary.md"

    for rows, target in [
        (sample_stats, sample_csv),
        (repeat_stats, repeat_csv),
        (repeat_worst_rows, repeat_worst_csv),
    ]:
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    payload = {
        "status": "ok",
        "source_round": "round11_wrongref_v2",
        "best_config": {
            "config_id": int(best["config_id"]),
            "wrongref_mode": best["wrongref_mode"],
            "phase_mix": float(best["phase_mix"]),
            "reference_weight": float(best["reference_weight"]),
            "num_layers": int(best["num_layers"]),
        },
        "repeat_level": repeat_payload,
        "sample_level": global_stats,
        "top_risk_samples": sorted(sample_stats, key=lambda row: row["common_minus_wrongref_db_mean"])[:3],
        "artifacts": {
            "sample_csv": str(sample_csv),
            "repeat_csv": str(repeat_csv),
            "repeat_worst_csv": str(repeat_worst_csv),
            "summary_json": str(summary_json),
            "summary_md": str(summary_md),
        },
        "note": "Round12 is a diagnostic pass only; it reuses round11 assets and does not retrain any processor.",
    }
    summary_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Round 12 Margin Diagnostics",
        "",
        "- mode: no retraining; reuse round11 best focused configuration only",
        f"- best config: {best['wrongref_mode']} at phase_mix={float(best['phase_mix']):.3f}",
        f"- repeat-level positive count for common-minus-wrongref: {repeat_positive_count}/{len(repeat_stats)}",
        f"- worst repeat common-minus-wrongref: {repeat_payload['common_minus_wrongref_worst_repeat_db']:+.3f} dB",
        f"- sample-repeat positive rate for common-minus-wrongref: {global_stats['common_minus_wrongref_positive_rate']:.3f}",
        f"- sample-repeat q10 for common-minus-wrongref: {global_stats['common_minus_wrongref_db_q10']:+.3f} dB",
        f"- most frequent worst sample: {global_stats['most_frequent_worst_sample']}",
        "- interpretation: if the repeat-level sign still fails while the sample-repeat positive rate stays high, Figure 5 is in a near-threshold regime rather than a uniformly separable regime.",
    ]
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
