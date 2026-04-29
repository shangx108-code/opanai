from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path("/workspace/self-calibrating-diffractive-ncomms")
OUT = ROOT / "outputs"
DETAIL_CSV = OUT / "round11_wrongref_v2_detail.csv"
REPEAT_CSV = OUT / "round11_wrongref_v2_repeat_rows.csv"
SUMMARY_CSV = OUT / "round11_wrongref_v2_summary.csv"

RISK_SAMPLES = ["frame", "two_spots"]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def percentile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = (len(ordered) - 1) * q
    lo = math.floor(position)
    hi = math.ceil(position)
    if lo == hi:
        return ordered[lo]
    w = position - lo
    return ordered[lo] * (1.0 - w) + ordered[hi] * w


def choose_best_config(summary_rows: list[dict[str, str]]) -> dict[str, str]:
    return max(summary_rows, key=lambda row: float(row["ranking_score"]))


def build_condition_grid(detail_rows: list[dict[str, str]], config_id: str) -> dict[tuple[int, str], dict[str, float]]:
    grid: dict[tuple[int, str], dict[str, float]] = defaultdict(dict)
    for row in detail_rows:
        if row["config_id"] != config_id or row["split"] != "ood":
            continue
        key = (int(row["repeat_seed"]), row["sample"])
        grid[key][row["condition"]] = float(row["psnr_db"])
    return grid


def build_risk_rows(grid: dict[tuple[int, str], dict[str, float]]) -> list[dict[str, object]]:
    rows = []
    for repeat_seed, sample in sorted(grid.keys()):
        if sample not in RISK_SAMPLES:
            continue
        bucket = grid[(repeat_seed, sample)]
        ordinary = bucket["ordinary"]
        common = bucket["common_path"]
        noncommon = bucket["noncommon_path"]
        wrongref = bucket["wrong_reference"]
        rows.append(
            {
                "repeat_seed": repeat_seed,
                "sample": sample,
                "ordinary_psnr_db": round(ordinary, 6),
                "common_psnr_db": round(common, 6),
                "noncommon_psnr_db": round(noncommon, 6),
                "wrongref_psnr_db": round(wrongref, 6),
                "common_minus_ordinary_db": round(common - ordinary, 6),
                "common_minus_noncommon_db": round(common - noncommon, 6),
                "common_minus_wrongref_db": round(common - wrongref, 6),
                "wrongref_minus_ordinary_db": round(wrongref - ordinary, 6),
                "wrongref_beats_common": wrongref >= common,
                "noncommon_beats_common": noncommon >= common,
            }
        )
    return rows


def aggregate_risk_rows(risk_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in risk_rows:
        grouped[str(row["sample"])].append(row)

    summaries = []
    for sample, bucket in grouped.items():
        cmw = [float(row["common_minus_wrongref_db"]) for row in bucket]
        cmo = [float(row["common_minus_ordinary_db"]) for row in bucket]
        cmn = [float(row["common_minus_noncommon_db"]) for row in bucket]
        wmo = [float(row["wrongref_minus_ordinary_db"]) for row in bucket]
        summaries.append(
            {
                "sample": sample,
                "repeat_count": len(bucket),
                "common_minus_wrongref_db_mean": round(mean(cmw), 6),
                "common_minus_wrongref_db_min": round(min(cmw), 6),
                "common_minus_wrongref_db_q25": round(percentile(cmw, 0.25), 6),
                "common_minus_wrongref_db_median": round(percentile(cmw, 0.50), 6),
                "common_minus_wrongref_positive_rate": round(sum(v > 0 for v in cmw) / len(cmw), 6),
                "common_minus_ordinary_db_mean": round(mean(cmo), 6),
                "common_minus_ordinary_db_min": round(min(cmo), 6),
                "common_minus_noncommon_db_mean": round(mean(cmn), 6),
                "wrongref_minus_ordinary_db_mean": round(mean(wmo), 6),
                "wrongref_beats_common_count": sum(bool(row["wrongref_beats_common"]) for row in bucket),
                "noncommon_beats_common_count": sum(bool(row["noncommon_beats_common"]) for row in bucket),
            }
        )
    return sorted(summaries, key=lambda row: row["sample"])


def build_criteria_bundle(grid: dict[tuple[int, str], dict[str, float]], repeat_rows: list[dict[str, str]], config_id: str) -> dict[str, object]:
    pairs = []
    for (repeat_seed, sample), bucket in sorted(grid.items()):
        pairs.append(
            {
                "repeat_seed": repeat_seed,
                "sample": sample,
                "common_minus_wrongref_db": bucket["common_path"] - bucket["wrong_reference"],
                "common_minus_ordinary_db": bucket["common_path"] - bucket["ordinary"],
            }
        )

    cmw_pairs = [row["common_minus_wrongref_db"] for row in pairs]
    risk_pairs = [row["common_minus_wrongref_db"] for row in pairs if row["sample"] in RISK_SAMPLES]
    risk_worst_per_repeat = []
    all_worst_per_repeat = []
    for repeat_seed in sorted({row["repeat_seed"] for row in pairs}):
        repeat_bucket = [row for row in pairs if row["repeat_seed"] == repeat_seed]
        risk_bucket = [row for row in repeat_bucket if row["sample"] in RISK_SAMPLES]
        risk_worst_per_repeat.append(min(row["common_minus_wrongref_db"] for row in risk_bucket))
        all_worst_per_repeat.append(min(row["common_minus_wrongref_db"] for row in repeat_bucket))

    repeat_level_rows = [row for row in repeat_rows if row["config_id"] == config_id]
    repeat_cmw = [float(row["common_minus_wrongref_db"]) for row in repeat_level_rows]

    bundle = {
        "legacy_mean_common_minus_wrongref_db": round(mean(repeat_cmw), 6),
        "repeat_positive_fraction": round(sum(v > 0 for v in repeat_cmw) / len(repeat_cmw), 6),
        "sample_pair_positive_fraction": round(sum(v > 0 for v in cmw_pairs) / len(cmw_pairs), 6),
        "sample_pair_q10_db": round(percentile(cmw_pairs, 0.10), 6),
        "sample_pair_median_db": round(percentile(cmw_pairs, 0.50), 6),
        "worst_sample_margin_mean_db": round(mean(all_worst_per_repeat), 6),
        "worst_sample_margin_min_db": round(min(all_worst_per_repeat), 6),
        "risk_sample_positive_fraction": round(sum(v > 0 for v in risk_pairs) / len(risk_pairs), 6),
        "risk_sample_q25_db": round(percentile(risk_pairs, 0.25), 6),
        "risk_sample_median_db": round(percentile(risk_pairs, 0.50), 6),
        "risk_worst_repeat_margin_mean_db": round(mean(risk_worst_per_repeat), 6),
        "risk_worst_repeat_margin_min_db": round(min(risk_worst_per_repeat), 6),
    }
    return bundle


def main() -> None:
    summary_rows = read_csv(SUMMARY_CSV)
    repeat_rows = read_csv(REPEAT_CSV)
    detail_rows = read_csv(DETAIL_CSV)
    best = choose_best_config(summary_rows)
    config_id = best["config_id"]

    grid = build_condition_grid(detail_rows, config_id)
    risk_rows = build_risk_rows(grid)
    risk_summaries = aggregate_risk_rows(risk_rows)
    criteria_bundle = build_criteria_bundle(grid, repeat_rows, config_id)

    risk_csv = OUT / "round13_risk_sample_repeat_rows.csv"
    risk_summary_csv = OUT / "round13_risk_sample_summary.csv"
    criteria_json = OUT / "round13_figure5_criteria.json"
    summary_md = OUT / "round13_risk_mechanism_summary.md"

    for rows, path in [(risk_rows, risk_csv), (risk_summaries, risk_summary_csv)]:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

    payload = {
        "status": "ok",
        "source_round": "round11_wrongref_v2",
        "best_config": {
            "config_id": int(config_id),
            "wrongref_mode": best["wrongref_mode"],
            "phase_mix": float(best["phase_mix"]),
            "reference_weight": float(best["reference_weight"]),
            "num_layers": int(best["num_layers"]),
        },
        "risk_sample_summary": risk_summaries,
        "candidate_criteria": criteria_bundle,
        "mechanism_readout": {
            "frame_pattern": "common remains near ordinary on frame, while wrong-reference often matches or exceeds common, so exclusion fails through edge-dominated ambiguity rather than broad reconstruction collapse",
            "two_spots_pattern": "common strongly beats ordinary on two_spots, but wrong-reference intermittently tracks the same sparse-spot geometry, so exclusion remains positive on average but not uniformly across repeats",
        },
        "artifacts": {
            "risk_csv": str(risk_csv),
            "risk_summary_csv": str(risk_summary_csv),
            "criteria_json": str(criteria_json),
            "summary_md": str(summary_md),
        },
    }
    criteria_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = [
        "# Round 13 Risk-sample Mechanism Analysis",
        "",
        f"- best config analyzed: {best['wrongref_mode']} at phase_mix={float(best['phase_mix']):.3f}",
        f"- frame common-minus-wrongref mean/min: {risk_summaries[0]['common_minus_wrongref_db_mean']:+.3f}/{risk_summaries[0]['common_minus_wrongref_db_min']:+.3f} dB" if risk_summaries and risk_summaries[0]['sample']=='frame' else "",
        f"- two_spots common-minus-wrongref mean/min: {next(row for row in risk_summaries if row['sample']=='two_spots')['common_minus_wrongref_db_mean']:+.3f}/{next(row for row in risk_summaries if row['sample']=='two_spots')['common_minus_wrongref_db_min']:+.3f} dB",
        f"- candidate criterion, sample-pair positive fraction: {criteria_bundle['sample_pair_positive_fraction']:.3f}",
        f"- candidate criterion, sample-pair q10: {criteria_bundle['sample_pair_q10_db']:+.3f} dB",
        f"- candidate criterion, risk-sample positive fraction: {criteria_bundle['risk_sample_positive_fraction']:.3f}",
        f"- candidate criterion, risk worst-repeat margin min: {criteria_bundle['risk_worst_repeat_margin_min_db']:+.3f} dB",
        "- recommendation: move Figure 5 away from mean-PSNR-only exclusion and toward a paired distribution criterion built from sample-pair positive fraction, lower-quantile margin, and worst-sample margin.",
    ]
    summary_md.write_text("\n".join(line for line in lines if line) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
