from __future__ import annotations

import csv
import json
import math
from collections import defaultdict, deque
from pathlib import Path

import numpy as np

from round16_structural_modes_scan import encoding_gate, make_input, percentile
from round18_expanded_ood_confirmation import build_expanded_samples
from round6_numpy_passive_d2nn import GOOD_REFERENCE, SIZE
from wrong_reference_designs_v3 import edge_map, sparse_map, wrong_reference_v3


ROOT = Path("/workspace/self-calibrating-diffractive-ncomms")
OUT = ROOT / "outputs"
PAIR_CSV = OUT / "round18_expanded_ood_pair_rows.csv"
SAMPLE_SUMMARY_CSV = OUT / "round18_expanded_ood_sample_summary.csv"
ROUND18_SUMMARY_JSON = OUT / "round18_expanded_ood_summary.json"
ROUND17_SUMMARY_JSON = OUT / "round17_structural_confirm_summary.json"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def mean(values: list[float]) -> float:
    return float(sum(values) / len(values))


def circular_phase_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean(np.abs(np.angle(np.exp(1j * (a - b))))))


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    av = a.reshape(-1).astype(np.float64)
    bv = b.reshape(-1).astype(np.float64)
    denom = np.linalg.norm(av) * np.linalg.norm(bv)
    if denom <= 1e-12:
        return 0.0
    return float(np.dot(av, bv) / denom)


def connected_components(mask: np.ndarray) -> int:
    visited = np.zeros_like(mask, dtype=bool)
    count = 0
    neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if not mask[i, j] or visited[i, j]:
                continue
            count += 1
            queue: deque[tuple[int, int]] = deque([(i, j)])
            visited[i, j] = True
            while queue:
                x, y = queue.popleft()
                for dx, dy in neighbors:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < mask.shape[0] and 0 <= ny < mask.shape[1] and mask[nx, ny] and not visited[nx, ny]:
                        visited[nx, ny] = True
                        queue.append((nx, ny))
    return count


def center_radius(pattern: np.ndarray) -> float:
    yy, xx = np.indices(pattern.shape)
    mass = float(np.sum(pattern))
    if mass <= 1e-12:
        return 0.0
    cx = float(np.sum(xx * pattern) / mass)
    cy = float(np.sum(yy * pattern) / mass)
    center = (pattern.shape[0] - 1) / 2.0
    return float(np.sqrt((cx - center) ** 2 + (cy - center) ** 2) / center)


def shape_features(sample) -> dict[str, float]:
    pattern = sample.object_pattern
    edges = edge_map(pattern)
    sparse = sparse_map(pattern)
    gate = encoding_gate(pattern, "occupancy_guarded")
    binary = pattern > 0.25
    occupancy = float(np.mean(binary))
    components = connected_components(binary)
    flip_asym = float(np.mean(np.abs(pattern - pattern[:, ::-1])))
    top_bottom_asym = float(np.mean(np.abs(pattern - pattern[::-1, :])))
    return {
        "occupancy_fraction": occupancy,
        "edge_density": float(np.mean(edges)),
        "sparse_alignment": cosine_similarity(pattern, sparse),
        "gate_mean": float(np.mean(gate)),
        "component_count": float(components),
        "center_radius": center_radius(pattern),
        "horizontal_asymmetry": flip_asym,
        "vertical_asymmetry": top_bottom_asym,
        "thinness_ratio": float(np.mean(edges) / max(occupancy, 1e-6)),
    }


def input_diagnostics(sample) -> dict[str, float]:
    common_amp, common_phase = make_input(sample, "common_path", "sparse_tracker_decoy", "occupancy_guarded")
    wrong_amp, wrong_phase = make_input(sample, "wrong_reference", "sparse_tracker_decoy", "occupancy_guarded")
    ordinary_amp, ordinary_phase = make_input(sample, "ordinary", "sparse_tracker_decoy", "occupancy_guarded")
    wrong_ref_amp, wrong_ref_phase = wrong_reference_v3(sample, "sparse_tracker_decoy")
    gate = encoding_gate(sample.object_pattern, "occupancy_guarded")
    encoded_wrong_ref = gate * wrong_ref_amp
    encoded_good_ref = gate * GOOD_REFERENCE
    return {
        "wrongref_object_amp_alignment": cosine_similarity(encoded_wrong_ref, sample.object_pattern),
        "goodref_object_amp_alignment": cosine_similarity(encoded_good_ref, sample.object_pattern),
        "wrongref_goodref_amp_similarity": cosine_similarity(encoded_wrong_ref, encoded_good_ref),
        "common_wrong_input_amp_gap": float(np.mean(np.abs(common_amp - wrong_amp))),
        "common_wrong_input_phase_gap": circular_phase_distance(common_phase, wrong_phase),
        "ordinary_common_input_amp_gap": float(np.mean(np.abs(common_amp - ordinary_amp))),
        "ordinary_common_input_phase_gap": circular_phase_distance(common_phase, ordinary_phase),
        "wrongref_object_phase_alignment": cosine_similarity(np.cos(wrong_ref_phase), np.cos(sample.coeffs[0] * np.ones((SIZE, SIZE)))),
    }


def explain_row(row: dict[str, float]) -> str:
    if row["common_minus_ordinary_db_mean"] < 0:
        if row["thinness_ratio"] > 6.0 or row["component_count"] >= 3:
            return "ordinary-support failure dominates: the shape is thin or fragmented enough that common-path itself falls outside the stable processor window"
        return "ordinary-support failure dominates before exclusion can even be tested cleanly"
    if row["wrongref_object_amp_alignment"] > row["goodref_object_amp_alignment"] + 0.05:
        return "wrong-reference tracking dominates: the decoy amplitude matches the object support too well under occupancy_guarded encoding"
    if row["center_radius"] > 0.28:
        return "off-center support is a tail trigger: shifted energy lets the wrong-reference branch follow geometry that the common-path branch does not isolate cleanly"
    if row["thinness_ratio"] > 5.0:
        return "thin-edge geometry is the main tail source: occupancy_guarded gating suppresses support while wrong-reference still tracks the sparse structure"
    return "tail is mixed: common-path remains positive on average, but structural similarity keeps wrong-reference intermittently competitive"


def main() -> None:
    pair_rows = read_csv(PAIR_CSV)
    sample_summary_rows = read_csv(SAMPLE_SUMMARY_CSV)
    round18_summary = json.loads(ROUND18_SUMMARY_JSON.read_text(encoding="utf-8"))
    round17_summary = json.loads(ROUND17_SUMMARY_JSON.read_text(encoding="utf-8"))
    sample_map = {sample.name: sample for sample in build_expanded_samples()}

    sample_pairs: dict[str, list[float]] = defaultdict(list)
    for row in pair_rows:
        sample_pairs[row["sample"]].append(float(row["common_minus_wrongref_db"]))

    mechanism_rows: list[dict[str, object]] = []
    for row in sample_summary_rows:
        sample = sample_map[row["sample"]]
        features = shape_features(sample)
        diagnostics = input_diagnostics(sample)
        merged: dict[str, object] = {
            "sample": row["sample"],
            "repeat_count": int(row["repeat_count"]),
            "common_minus_wrongref_db_mean": round(float(row["common_minus_wrongref_db_mean"]), 6),
            "common_minus_wrongref_db_min": round(float(row["common_minus_wrongref_db_min"]), 6),
            "common_minus_wrongref_positive_fraction": round(float(row["common_minus_wrongref_positive_fraction"]), 6),
            "common_minus_ordinary_db_mean": round(float(row["common_minus_ordinary_db_mean"]), 6),
            "common_minus_ordinary_db_min": round(float(row["common_minus_ordinary_db_min"]), 6),
        }
        for key, value in features.items():
            merged[key] = round(float(value), 6)
        for key, value in diagnostics.items():
            merged[key] = round(float(value), 6)
        negative = [max(0.0, -value) for value in sample_pairs[row["sample"]]]
        merged["negative_mass_db"] = round(mean(negative), 6)
        merged["tail_cvar20_db"] = round(mean(sorted(sample_pairs[row["sample"]])[: max(1, math.ceil(0.2 * len(sample_pairs[row["sample"]])))]), 6)
        merged["mechanism_readout"] = explain_row(merged)  # type: ignore[arg-type]
        mechanism_rows.append(merged)

    mechanism_rows = sorted(mechanism_rows, key=lambda row: (float(row["common_minus_wrongref_db_min"]), float(row["common_minus_wrongref_db_mean"])))

    all_pair_margins = [float(row["common_minus_wrongref_db"]) for row in pair_rows]
    negative_values = [max(0.0, -value) for value in all_pair_margins]
    cvar20 = mean(sorted(all_pair_margins)[: max(1, math.ceil(0.2 * len(all_pair_margins)))])
    sample_failure_breadth = sum(float(row["common_minus_wrongref_positive_fraction"]) < 0.5 for row in mechanism_rows) / len(mechanism_rows)
    sample_negative_mean_breadth = sum(float(row["common_minus_wrongref_db_mean"]) < 0 for row in mechanism_rows) / len(mechanism_rows)
    transfer_penalty = round(float(round18_summary["expanded_pair_q10_db"]) - float(round17_summary["risk_pair_q10_db"]), 6)
    ordinary_window_retention = round(float(round18_summary["common_minus_ordinary_db_mean"]) / max(float(round17_summary["common_minus_ordinary_db_mean"]), 1e-9), 6)

    risk_metrics = {
        "legacy_metrics": {
            "round17_risk_pair_q10_db": round(float(round17_summary["risk_pair_q10_db"]), 6),
            "round18_expanded_pair_q10_db": round(float(round18_summary["expanded_pair_q10_db"]), 6),
            "round18_expanded_pair_positive_fraction": round(float(round18_summary["expanded_pair_positive_fraction"]), 6),
        },
        "new_metrics": {
            "tail_cvar20_db": round(cvar20, 6),
            "negative_mass_db": round(mean(negative_values), 6),
            "sample_failure_breadth": round(sample_failure_breadth, 6),
            "sample_negative_mean_breadth": round(sample_negative_mean_breadth, 6),
            "transfer_penalty_q10_db": transfer_penalty,
            "ordinary_window_retention": ordinary_window_retention,
        },
        "metric_interpretation": {
            "tail_cvar20_db": "mean margin across the worst 20% of sample-repeat pairs; captures how bad the tail gets once failure starts",
            "negative_mass_db": "average amount of negative margin across all sample-repeat pairs after clipping positive values to zero; measures total tail burden",
            "sample_failure_breadth": "fraction of OOD samples whose positive fraction falls below 0.5; measures whether failures are narrow or spread across shape families",
            "sample_negative_mean_breadth": "fraction of OOD samples whose mean common-minus-wrong-reference margin is already negative",
            "transfer_penalty_q10_db": "drop in q10 when moving from the narrow round17 subset to the expanded round18 OOD set",
            "ordinary_window_retention": "how much of the ordinary-baseline advantage survives after OOD expansion",
        },
    }

    summary_payload = {
        "status": "ok",
        "structure": {
            "wrongref_mode": "sparse_tracker_decoy",
            "encoding_mode": "occupancy_guarded",
        },
        "top_tail_samples": mechanism_rows[:4],
        "risk_metrics": risk_metrics,
    }

    mechanism_csv = OUT / "round19_tail_mechanism_summary.csv"
    metrics_json = OUT / "round19_risk_metrics.json"
    summary_md = OUT / "round19_tail_mechanism_summary.md"

    write_csv(mechanism_rows, mechanism_csv)
    metrics_json.write_text(json.dumps(summary_payload, indent=2), encoding="utf-8")

    lines = [
        "# Round 19 Tail Mechanism And Risk Metrics",
        "",
        "- fixed structure: sparse_tracker_decoy + occupancy_guarded",
        f"- transfer penalty q10: {risk_metrics['new_metrics']['transfer_penalty_q10_db']:+.3f} dB",
        f"- tail CVaR20: {risk_metrics['new_metrics']['tail_cvar20_db']:+.3f} dB",
        f"- negative mass: {risk_metrics['new_metrics']['negative_mass_db']:+.3f} dB",
        f"- sample failure breadth: {risk_metrics['new_metrics']['sample_failure_breadth']:.3f}",
        f"- ordinary-window retention: {risk_metrics['new_metrics']['ordinary_window_retention']:.3f}",
        "",
        "## Tail Readout",
    ]
    for row in mechanism_rows[:4]:
        lines.extend(
            [
                f"- {row['sample']}: mean/min common-minus-wrongref = {float(row['common_minus_wrongref_db_mean']):+.3f}/{float(row['common_minus_wrongref_db_min']):+.3f} dB; mechanism = {row['mechanism_readout']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Recommended Figure 5 Boundary",
            "- Keep Figure 5 as a narrow-subset confirmation only.",
            "- Use tail CVaR20, negative mass, and sample failure breadth alongside q10 when discussing exclusion risk.",
            "- Treat zigzag-like fragmented thin paths and off-center sparse objects as the current dominant extrapolation failure family.",
        ]
    )
    summary_md.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
