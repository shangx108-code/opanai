#!/usr/bin/env python3

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


EXPECTED_FILES = [
    ("three_terminal", "selected_operating_points.csv", "Three-terminal selected operating-point table", 1),
    ("three_terminal", "positive_three_terminal_scan.csv", "Positive-control three-terminal scan", 1),
    ("three_terminal", "positive_three_terminal_robustness.csv", "Positive-control robustness table", 1),
    ("three_terminal", "positive_three_terminal_bias.csv", "Positive-control bias trace", 1),
    ("three_terminal", "dot_three_terminal_bias.csv", "Smooth-dot false-positive bias trace", 1),
    ("three_terminal", "impurity_three_terminal_bias.csv", "Impurity false-positive bias trace", 1),
    ("three_terminal", "disorder_three_terminal_bias.csv", "Disorder false-positive bias trace", 1),
    ("transport", "positive_vz_scan.csv", "Positive-control transport scan", 2),
    ("transport", "smooth_dot_scan.csv", "Smooth-dot transport scan", 2),
    ("transport", "impurity_scan.csv", "Impurity transport scan", 2),
    ("transport", "disorder_scan.csv", "Disorder transport scan", 2),
    ("transport", "eta_scan.csv", "Eta-broadening scan", 2),
    ("transport", "positive_bias_trace.csv", "Positive-control two-terminal bias trace", 2),
    ("transport", "smooth_dot_bias_trace.csv", "Smooth-dot two-terminal bias trace", 2),
    ("transport", "impurity_bias_trace.csv", "Impurity two-terminal bias trace", 2),
    ("rashba", "positive_control_scan.csv", "First shared-code-path positive-control scan", 3),
    ("rashba", "smooth_dot_control_scan.csv", "First shared-code-path smooth-dot scan", 3),
]


def find_current_path(filename: str) -> str:
    candidates = [
        PROJECT_ROOT / "data" / "raw" / filename,
        PROJECT_ROOT / "data" / "processed" / filename,
        Path("/workspace/output/three-terminal-benchmark") / filename,
        Path("/workspace/output/transport-benchmark") / filename,
        Path("/workspace/output/rashba-benchmark") / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return ""


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    inventory_rows = []
    summary = {}

    for group, filename, description, priority in EXPECTED_FILES:
        current_path = find_current_path(filename)
        status = "present" if current_path else "missing"
        inventory_rows.append(
            {
                "group": group,
                "filename": filename,
                "description": description,
                "priority": priority,
                "status": status,
                "current_path": current_path,
            }
        )
        summary.setdefault(group, {"expected": 0, "present": 0, "missing": 0})
        summary[group]["expected"] += 1
        summary[group][status] += 1

    inventory_path = RAW_DIR / "benchmark_inventory.csv"
    with inventory_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["group", "filename", "description", "priority", "status", "current_path"],
        )
        writer.writeheader()
        writer.writerows(inventory_rows)

    priority_path = RAW_DIR / "benchmark_recovery_priority.csv"
    with priority_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["priority", "group", "filename", "description", "status"],
        )
        writer.writeheader()
        for row in sorted(inventory_rows, key=lambda item: (item["priority"], item["group"], item["filename"])):
            writer.writerow(
                {
                    "priority": row["priority"],
                    "group": row["group"],
                    "filename": row["filename"],
                    "description": row["description"],
                    "status": row["status"],
                }
            )

    summary_path = PROCESSED_DIR / "benchmark_inventory_summary.csv"
    with summary_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["group", "expected", "present", "missing"],
        )
        writer.writeheader()
        for group in sorted(summary):
            writer.writerow({"group": group, **summary[group]})

    print(f"Wrote {inventory_path}")
    print(f"Wrote {priority_path}")
    print(f"Wrote {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
