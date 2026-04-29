#!/usr/bin/env python3

from __future__ import annotations

import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "three_terminal"
LOG_DIR = PROJECT_ROOT / "logs"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    selected_operating_points = [
        {
            "control_family": "positive_control",
            "figure_role": "topological_reference",
            "local_signal_goal": "reference_zero_bias_behavior",
            "data_status": "pending_recompute",
            "source_basis": "Recovered from project memory only",
            "evidence_reference": "review-history.md:126-140; figure-storyboard.md:45-51",
            "source_commit": "memory checkpoint only; no historical CSV recovered",
            "mu": "",
            "vz": "",
            "delta": "",
            "gamma_left": "",
            "gamma_right": "",
            "temperature": "",
            "bias_window": "",
            "notes": "Used as positive control in three-terminal benchmark package.",
        },
        {
            "control_family": "smooth_dot",
            "figure_role": "false_positive_local_failure",
            "local_signal_goal": "misleading_local_low_bias_behavior",
            "data_status": "pending_recompute",
            "source_basis": "Recovered from review history only",
            "evidence_reference": "review-history.md:134-140; supervision-log.md:129-146",
            "source_commit": "memory checkpoint only; no historical CSV recovered",
            "mu": "",
            "vz": "",
            "delta": "",
            "gamma_left": "",
            "gamma_right": "",
            "temperature": "",
            "bias_window": "",
            "notes": "Review history states this control was tuned to more misleading local low-bias behavior than before.",
        },
        {
            "control_family": "impurity",
            "figure_role": "false_positive_local_failure",
            "local_signal_goal": "misleading_local_low_bias_behavior",
            "data_status": "pending_recompute",
            "source_basis": "Recovered from review history only",
            "evidence_reference": "review-history.md:134-140; user_files/02-2-.txt:359-379",
            "source_commit": "memory checkpoint only; no historical CSV recovered",
            "mu": "",
            "vz": "",
            "delta": "",
            "gamma_left": "",
            "gamma_right": "",
            "temperature": "",
            "bias_window": "",
            "notes": "Review history states this control was tuned to more misleading local low-bias behavior than before.",
        },
        {
            "control_family": "disorder",
            "figure_role": "false_positive_local_failure",
            "local_signal_goal": "strongest_false_positive_case",
            "data_status": "pending_recompute",
            "source_basis": "Recovered from review history only",
            "evidence_reference": "review-history.md:139-140; supervision-log.md:136-145",
            "source_commit": "memory checkpoint only; no historical CSV recovered",
            "mu": "",
            "vz": "",
            "delta": "",
            "gamma_left": "",
            "gamma_right": "",
            "temperature": "",
            "bias_window": "",
            "notes": "Review history says the disorder case remained too dominant relative to smooth-dot and impurity.",
        },
    ]

    write_csv(
        RAW_DIR / "selected_operating_points.csv",
        [
            "control_family",
            "figure_role",
            "local_signal_goal",
            "data_status",
            "source_basis",
            "evidence_reference",
            "source_commit",
            "mu",
            "vz",
            "delta",
            "gamma_left",
            "gamma_right",
            "temperature",
            "bias_window",
            "notes",
        ],
        selected_operating_points,
    )

    scan_headers = [
        "record_id",
        "control_family",
        "sweep_parameter",
        "parameter_value",
        "observable_name",
        "observable_value",
        "data_status",
        "source_basis",
        "notes",
    ]
    write_csv(
        RAW_DIR / "positive_three_terminal_scan.csv",
        scan_headers,
        [
            {
                "record_id": "positive_scan_placeholder_001",
                "control_family": "positive_control",
                "sweep_parameter": "",
                "parameter_value": "",
                "observable_name": "",
                "observable_value": "",
                "data_status": "pending_recompute",
                "source_basis": "Expected raw file name recovered from archive checklist",
                "notes": "Placeholder row only. No numerical value has been reconstructed yet.",
            }
        ],
    )
    write_csv(
        RAW_DIR / "positive_three_terminal_robustness.csv",
        [
            "record_id",
            "control_family",
            "robustness_axis",
            "axis_value",
            "observable_name",
            "observable_value",
            "data_status",
            "source_basis",
            "notes",
        ],
        [
            {
                "record_id": "positive_robustness_placeholder_001",
                "control_family": "positive_control",
                "robustness_axis": "",
                "axis_value": "",
                "observable_name": "",
                "observable_value": "",
                "data_status": "pending_recompute",
                "source_basis": "Expected raw file name recovered from archive checklist",
                "notes": "Placeholder row only. No numerical value has been reconstructed yet.",
            }
        ],
    )

    for filename, control_family, notes in [
        ("positive_three_terminal_bias.csv", "positive_control", "Positive-control bias trace expected by archive checklist."),
        ("dot_three_terminal_bias.csv", "smooth_dot", "Smooth-dot false-positive bias trace expected by archive checklist."),
        ("impurity_three_terminal_bias.csv", "impurity", "Impurity false-positive bias trace expected by archive checklist."),
        ("disorder_three_terminal_bias.csv", "disorder", "Disorder false-positive bias trace expected by archive checklist."),
    ]:
        write_csv(
            RAW_DIR / filename,
            [
                "record_id",
                "control_family",
                "bias",
                "g_ll",
                "g_rr",
                "g_lr",
                "data_status",
                "source_basis",
                "notes",
            ],
            [
                {
                    "record_id": f"{control_family}_bias_placeholder_001",
                    "control_family": control_family,
                    "bias": "",
                    "g_ll": "",
                    "g_rr": "",
                    "g_lr": "",
                    "data_status": "pending_recompute",
                    "source_basis": "Expected raw file name recovered from archive checklist",
                    "notes": notes + " Placeholder row only.",
                }
            ],
        )

    write_csv(
        LOG_DIR / "three_terminal_batch1_status.csv",
        ["filename", "kind", "status", "contains_physical_numerical_results", "notes"],
        [
            {
                "filename": "selected_operating_points.csv",
                "kind": "recovery_metadata_seed",
                "status": "created",
                "contains_physical_numerical_results": "no",
                "notes": "Contains control-family metadata and blank numerical slots pending recomputation.",
            },
            {
                "filename": "positive_three_terminal_scan.csv",
                "kind": "recovery_placeholder",
                "status": "created",
                "contains_physical_numerical_results": "no",
                "notes": "Uses archive-backed filename with placeholder row only.",
            },
            {
                "filename": "positive_three_terminal_robustness.csv",
                "kind": "recovery_placeholder",
                "status": "created",
                "contains_physical_numerical_results": "no",
                "notes": "Uses archive-backed filename with placeholder row only.",
            },
            {
                "filename": "positive_three_terminal_bias.csv",
                "kind": "recovery_placeholder",
                "status": "created",
                "contains_physical_numerical_results": "no",
                "notes": "Uses archive-backed filename with placeholder row only.",
            },
            {
                "filename": "dot_three_terminal_bias.csv",
                "kind": "recovery_placeholder",
                "status": "created",
                "contains_physical_numerical_results": "no",
                "notes": "Uses archive-backed filename with placeholder row only.",
            },
            {
                "filename": "impurity_three_terminal_bias.csv",
                "kind": "recovery_placeholder",
                "status": "created",
                "contains_physical_numerical_results": "no",
                "notes": "Uses archive-backed filename with placeholder row only.",
            },
            {
                "filename": "disorder_three_terminal_bias.csv",
                "kind": "recovery_placeholder",
                "status": "created",
                "contains_physical_numerical_results": "no",
                "notes": "Uses archive-backed filename with placeholder row only.",
            },
        ],
    )

    print("Wrote first-batch three-terminal recovery CSV stubs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
