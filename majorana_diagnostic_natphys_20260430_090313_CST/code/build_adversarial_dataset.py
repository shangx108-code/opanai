#!/usr/bin/env python3

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "adversarial"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


ROWS = [
    {
        "sample_id": "adv-positive-baseline-001",
        "control_family": "positive_control",
        "adversarial_role": "sanity_anchor",
        "attack_target": "none",
        "failure_mode": "reference_topological_case",
        "intended_confusion": "none",
        "expected_local_peak": "yes",
        "expected_nonlocal_signal": "yes",
        "expected_topology_consistency": "yes",
        "difficulty_level": "baseline",
        "priority": "p0",
        "data_status": "pending_recompute",
        "evidence_reference": "figure-storyboard.md:24-29; review-history.md:134-138",
        "notes": "Reference topological control used to calibrate the adversarial set.",
    },
    {
        "sample_id": "adv-smooth-dot-001",
        "control_family": "smooth_dot",
        "adversarial_role": "local_peak_mimic",
        "attack_target": "local_tunnelling_only",
        "failure_mode": "dot_induced_false_positive",
        "intended_confusion": "strong local low-bias behavior without stable topology",
        "expected_local_peak": "yes",
        "expected_nonlocal_signal": "weak_or_ambiguous",
        "expected_topology_consistency": "no",
        "difficulty_level": "high",
        "priority": "p1",
        "data_status": "pending_recompute",
        "evidence_reference": "review-history.md:134-140; supervision-log.md:136-145",
        "notes": "Adversarial case meant to break any diagnosis that leans too hard on local zero-bias structure.",
    },
    {
        "sample_id": "adv-impurity-001",
        "control_family": "impurity",
        "adversarial_role": "subgap_mimic",
        "attack_target": "local_plus_partial_nonlocal",
        "failure_mode": "impurity_induced_near_zero_state",
        "intended_confusion": "subgap state that can imitate part of the Majorana transport signature",
        "expected_local_peak": "yes",
        "expected_nonlocal_signal": "weak_or_context_dependent",
        "expected_topology_consistency": "no",
        "difficulty_level": "high",
        "priority": "p1",
        "data_status": "pending_recompute",
        "evidence_reference": "user_files/02-2-.txt:359-383; review-history.md:134-140",
        "notes": "Adversarial impurity family aimed at stress-testing impurity-aware exclusion logic.",
    },
    {
        "sample_id": "adv-disorder-001",
        "control_family": "disorder",
        "adversarial_role": "dominant_false_positive",
        "attack_target": "entire_diagnostic_hierarchy",
        "failure_mode": "disorder_dominated_near_zero_state",
        "intended_confusion": "strongest false-positive family in current project memory",
        "expected_local_peak": "yes",
        "expected_nonlocal_signal": "potentially_nonzero_but_unstable",
        "expected_topology_consistency": "no_or_sample_dependent",
        "difficulty_level": "very_high",
        "priority": "p1",
        "data_status": "pending_recompute",
        "evidence_reference": "review-history.md:139-140; supervision-log.md:136-145",
        "notes": "Current memory says disorder remains too dominant relative to smooth-dot and impurity controls.",
    },
    {
        "sample_id": "adv-nonlocal-mimic-001",
        "control_family": "cross_family",
        "adversarial_role": "nonlocal_mimic",
        "attack_target": "nonlocal_signal_only",
        "failure_mode": "partial nonlocal resemblance without topological agreement",
        "intended_confusion": "break any rule that treats nonlocal response alone as decisive",
        "expected_local_peak": "variable",
        "expected_nonlocal_signal": "yes_or_borderline",
        "expected_topology_consistency": "no",
        "difficulty_level": "very_high",
        "priority": "p2",
        "data_status": "spec_only",
        "evidence_reference": "review-history.md:91-95; project-state.md:51-59",
        "notes": "Dataset slot reserved for cases where nonlocality alone looks encouraging but the full hierarchy still fails.",
    },
    {
        "sample_id": "adv-gap-reopening-mismatch-001",
        "control_family": "cross_family",
        "adversarial_role": "gap_topology_mismatch",
        "attack_target": "gap_reopening_interpretation",
        "failure_mode": "apparent spectral improvement without defensible topology layer",
        "intended_confusion": "challenge any visual reading of gap evolution without topology-aware support",
        "expected_local_peak": "variable",
        "expected_nonlocal_signal": "variable",
        "expected_topology_consistency": "uncertain_until_recomputed",
        "difficulty_level": "very_high",
        "priority": "p2",
        "data_status": "spec_only",
        "evidence_reference": "review-history.md:138-140; supervision-log.md:141-145",
        "notes": "Reserved for future adversarial examples once the topology layer is upgraded.",
    },
]


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = list(ROWS[0].keys())
    raw_path = RAW_DIR / "adversarial_dataset_v1.csv"
    write_csv(raw_path, fieldnames, ROWS)

    summary_rows = []
    counts: dict[str, int] = {}
    for row in ROWS:
        key = row["control_family"]
        counts[key] = counts.get(key, 0) + 1
    for key in sorted(counts):
        summary_rows.append({"control_family": key, "num_samples": counts[key]})

    summary_path = PROCESSED_DIR / "adversarial_dataset_v1_summary.csv"
    write_csv(summary_path, ["control_family", "num_samples"], summary_rows)

    print(f"Wrote {raw_path}")
    print(f"Wrote {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
