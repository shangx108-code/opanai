from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUT = PROJECT_ROOT / "artifacts" / "project-outputs"
SUB = PROJECT_ROOT / "artifacts" / "submission-package"
LOG = PROJECT_ROOT / "logs"


def ensure_dirs() -> None:
    SUB.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(rows: list[dict[str, object]], target: Path) -> None:
    with target.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def round6_rows() -> list[dict[str, object]]:
    metrics = read_csv(OUT / "round6_numpy_passive_d2nn_metrics.csv")
    summary = read_json(OUT / "round6_numpy_passive_d2nn_summary.json")
    rows: list[dict[str, object]] = []
    for row in metrics:
        rows.append(
            {
                "panel": "baseline",
                "source_round": "round6",
                "data_kind": "raw_metric",
                "sample_or_config": row["sample"],
                "repeat_or_split": row["split"],
                "condition_or_mode": row["condition"],
                "metric_name": "psnr_db",
                "metric_value": row["psnr_db"],
                "aux_value": row["mse"],
                "aux_name": "mse",
                "note": "minimal restored baseline",
            }
        )
    for row in summary["summary_rows"]:
        rows.append(
            {
                "panel": "baseline",
                "source_round": "round6",
                "data_kind": "summary",
                "sample_or_config": "ood_mean",
                "repeat_or_split": "ood",
                "condition_or_mode": row["condition"],
                "metric_name": "ood_mean_psnr_db",
                "metric_value": f'{row["ood_mean_psnr_db"]:.6f}',
                "aux_value": f'{row["train_final_mse"]:.8f}',
                "aux_name": "train_final_mse",
                "note": "condition summary",
            }
        )
    for name, value in summary["deltas_db"].items():
        rows.append(
            {
                "panel": "baseline",
                "source_round": "round6",
                "data_kind": "delta_summary",
                "sample_or_config": "ood_mean",
                "repeat_or_split": "ood",
                "condition_or_mode": "common_path",
                "metric_name": name,
                "metric_value": f"{value:.6f}",
                "aux_value": "",
                "aux_name": "",
                "note": "summary delta",
            }
        )
    return rows


def top_summary_rows(filename: str, panel: str, source_round: str) -> list[dict[str, object]]:
    rows = read_csv(OUT / filename)
    out_rows: list[dict[str, object]] = []
    for row in rows[:10]:
        for key, value in row.items():
            out_rows.append(
                {
                    "panel": panel,
                    "source_round": source_round,
                    "data_kind": "top_table",
                    "sample_or_config": row.get("config_id", row.get("sample", "row")),
                    "repeat_or_split": row.get("repeat_count", ""),
                    "condition_or_mode": key,
                    "metric_name": key,
                    "metric_value": value,
                    "aux_value": "",
                    "aux_name": "",
                    "note": filename,
                }
            )
    return out_rows


def repeat_rows(filename: str, panel: str, source_round: str) -> list[dict[str, object]]:
    rows = read_csv(OUT / filename)
    out_rows: list[dict[str, object]] = []
    for row in rows:
        identity = row.get("repeat_seed", row.get("sample", row.get("config_id", "row")))
        for key, value in row.items():
            if key in {"repeat_seed", "sample", "config_id"}:
                continue
            out_rows.append(
                {
                    "panel": panel,
                    "source_round": source_round,
                    "data_kind": "repeat_row",
                    "sample_or_config": identity,
                    "repeat_or_split": row.get("repeat_seed", row.get("sample", "")),
                    "condition_or_mode": key,
                    "metric_name": key,
                    "metric_value": value,
                    "aux_value": "",
                    "aux_name": "",
                    "note": filename,
                }
            )
    return out_rows


def sample_summary_rows(filename: str, panel: str, source_round: str) -> list[dict[str, object]]:
    rows = read_csv(OUT / filename)
    out_rows: list[dict[str, object]] = []
    for row in rows:
        sample = row.get("sample", "row")
        for key, value in row.items():
            if key == "sample":
                continue
            out_rows.append(
                {
                    "panel": panel,
                    "source_round": source_round,
                    "data_kind": "sample_summary",
                    "sample_or_config": sample,
                    "repeat_or_split": row.get("repeat_count", ""),
                    "condition_or_mode": key,
                    "metric_name": key,
                    "metric_value": value,
                    "aux_value": "",
                    "aux_name": "",
                    "note": filename,
                }
            )
    return out_rows


def generate_source_data() -> None:
    rows: list[dict[str, object]] = []
    rows.extend(round6_rows())
    rows.extend(top_summary_rows("round7_parameter_scan_top10.csv", "stable_window_scan", "round7"))
    rows.extend(top_summary_rows("round8_narrow_scan_summary.csv", "stable_window_repeat", "round8"))
    rows.extend(top_summary_rows("round15_risk_rescan_summary.csv", "risk_rescan", "round15"))
    rows.extend(top_summary_rows("round16_structural_scan_summary.csv", "structural_scan", "round16"))
    rows.extend(repeat_rows("round17_structural_confirm_repeat_rows.csv", "structural_confirm", "round17"))
    rows.extend(repeat_rows("round17_structural_confirm_risk_rows.csv", "risk_pairs", "round17"))
    rows.extend(sample_summary_rows("round18_expanded_ood_sample_summary.csv", "expanded_ood", "round18"))
    write_csv(rows, SUB / "figure5_source_data.csv")


def generate_summary_docs() -> None:
    round7 = read_json(OUT / "round7_parameter_scan_summary.json")
    round8 = read_json(OUT / "round8_narrow_scan_summary.json")
    round15 = read_json(OUT / "round15_risk_rescan_summary.json")
    round16 = read_json(OUT / "round16_structural_scan_summary.json")
    round17 = read_json(OUT / "round17_structural_confirm_summary.json")
    round18 = read_json(OUT / "round18_expanded_ood_summary.json")

    formal = f"""# Figure 5 Formal Summary

## Figure role
Figure 5 is the processor-level evidence figure. In the current raw-output-driven package, it should be read as a structured progression rather than a single-number claim.

## Raw-output chain used here
- round6: restored minimal baseline
- round7: first broad scan locating an ordinary-beating window
- round8: repeat-stability narrowing around the ordinary-beating window
- round15: failed micro-tuning attempt on the frame/two_spots risk tail
- round16: structural redesign scan for wrong-reference exclusion
- round17: higher-repeat confirmation of the selected structural mode
- round18: expanded OOD boundary test

## Main supported statements
- The restored round6 baseline is reproducible but does not support a common-path-over-ordinary claim.
- A stronger ordinary-beating window appears in round7 and survives repeat-focused narrowing in round8.
- Pure micro-tuning does not close the frame/two_spots risk tail in round15.
- Structural redesign in round16 creates the first q10-positive risk-pair window.
- Round17 confirms the selected structure over 14 repeats with common-minus-ordinary mean {round17["common_minus_ordinary_db_mean"]:.6f} dB and minimum {round17["common_minus_ordinary_db_min"]:.6f} dB, while common-minus-wrong-reference mean is {round17["common_minus_wrongref_db_mean"]:.6f} dB and minimum is {round17["common_minus_wrongref_db_min"]:.6f} dB.
- Round18 shows that this structure remains locally useful but does not generalize cleanly across the expanded OOD set; the expanded wrong-reference positive fraction drops to {round18["expanded_pair_positive_fraction"]:.6f}.

## Best-window summary
- round7 best config: layers={round7["best_config"]["num_layers"]}, reference_weight={round7["best_config"]["reference_weight"]}, phase_mix={round7["best_config"]["phase_mix"]}, common-minus-ordinary={round7["best_config"]["common_minus_ordinary_db"]:.6f} dB
- round8 best repeat-stable config: layers={round8["best_config"]["num_layers"]}, reference_weight={round8["best_config"]["reference_weight"]}, phase_mix={round8["best_config"]["phase_mix"]}, common-minus-ordinary mean={round8["best_config"]["common_minus_ordinary_db_mean"]:.6f} dB, minimum={round8["best_config"]["common_minus_ordinary_db_min"]:.6f} dB
- round16 best structural mode: {round16["best_config"]["wrongref_mode"]} + {round16["best_config"]["encoding_mode"]}, q10={round16["best_config"]["risk_pair_q10_db"]:.6f} dB
- round17 confirmed structure: {round17["wrongref_mode"]} + {round17["encoding_mode"]}, q10={round17["risk_pair_q10_db"]:.6f} dB, min={round17["risk_pair_min_db"]:.6f} dB

## Boundary
This package supports a local, repeat-stable ordinary-baseline advantage together with improved but still incomplete wrong-reference exclusion. It does not support a claim of broad processor-level self-calibration closure across the expanded OOD set.
"""
    (SUB / "figure5_formal_summary.md").write_text(formal, encoding="utf-8")

    caption = f"""# Figure 5 Caption Package

## Recommended title
Figure 5 | Raw-output-driven processor-level evidence for local ordinary-baseline advantage and incomplete exclusion closure

## Recommended caption
Figure 5 summarizes the processor-level evidence chain using only archived raw outputs from the current GitHub-backed long-term project space. Panel a establishes the restored round6 baseline, which is reproducible but does not support a common-path-over-ordinary claim. Panel b shows that a broader parameter scan and a repeat-focused narrowing identify a local ordinary-beating window: in round7 the best lightweight configuration yields a common-minus-ordinary gain of {round7["best_config"]["common_minus_ordinary_db"]:.3f} dB, and in round8 the best repeat-stable configuration retains a mean gain of {round8["best_config"]["common_minus_ordinary_db_mean"]:.3f} dB with a minimum of {round8["best_config"]["common_minus_ordinary_db_min"]:.3f} dB across four repeats. Panel c shows that continuous micro-tuning alone does not remove the frame/two_spots risk tail, whereas the structural mode scan produces a first q10-positive candidate and the round17 confirmation of {round17["wrongref_mode"]} plus {round17["encoding_mode"]} gives a risk-pair q10 of {round17["risk_pair_q10_db"]:.3f} dB, a minimum of {round17["risk_pair_min_db"]:.3f} dB, and a common-minus-ordinary mean of {round17["common_minus_ordinary_db_mean"]:.3f} dB across 14 repeats. Panel d marks the boundary of the result: the same confirmed structure weakens on the expanded out-of-distribution set in round18, where the common-minus-wrong-reference positive fraction falls to {round18["expanded_pair_positive_fraction"]:.3f} and several samples remain negative. Figure 5 therefore supports a local, repeat-stable ordinary-baseline advantage with improved but still incomplete wrong-reference exclusion, rather than a general processor-level proof of self-calibration.

## Panel roles
- Panel a: restored round6 baseline and why it is not the decisive result
- Panel b: round7 broad scan plus round8 repeat-stable ordinary-beating window
- Panel c: round15 failure, round16 structural search, and round17 confirmation
- Panel d: round18 expanded OOD boundary
"""
    (SUB / "figure5_caption_package.md").write_text(caption, encoding="utf-8")


def generate_availability_and_methods() -> None:
    data_text = """# Data Availability

Source data underlying Fig. 5 are provided as `figure5_source_data.csv` in this submission package. The underlying raw computational outputs used to assemble the Fig. 5 package are archived in `artifacts/project-outputs/`, including round6 baseline outputs, round7 and round8 scan summaries, round15 and round16 risk-tail scans, round17 confirmation repeats, round18 expanded-OOD summaries, and the paired diagnostic panel assets.
"""
    (SUB / "data_availability.md").write_text(data_text, encoding="utf-8")

    code_text = """# Code Availability

The restored round6 baseline script is archived at `code/project-scripts/round6_numpy_passive_d2nn.py`. The script that assembles the raw-output-driven Fig. 5 manuscript-support package is archived at `code/project-scripts/generate_figure5_formal_package.py`. Additional project scripts supporting the copied round7+ outputs remain traceable through the prior archived project space and can be consolidated further if a single-code-release package is required before submission.
"""
    (SUB / "code_availability.md").write_text(code_text, encoding="utf-8")

    methods_text = """# Methods Reproducibility

This Fig. 5 package is built from an explicit raw-output chain stored inside the current GitHub long-term project space. The restored round6 script was rerun in this space to regenerate the baseline raw metrics. The round7+ files included here were imported from the immediately preceding archived project space because they were already present there as committed raw outputs. The manuscript-support files in this package are therefore tied to concrete archived CSV, JSON, Markdown, PNG and PDF artifacts rather than to memory-only summaries.
"""
    (SUB / "methods_reproducibility.md").write_text(methods_text, encoding="utf-8")


def generate_registry() -> None:
    rows = []
    for path in sorted(OUT.glob("round6_*")):
        rows.append({"artifact_name": path.name, "artifact_type": "raw_output", "location": str(path), "status": "available", "role": "round6 baseline", "source": "current project space"})
    for name, role in [
        ("round7_parameter_scan_summary.csv", "round7 broad scan summary"),
        ("round7_parameter_scan_top10.csv", "round7 top configurations"),
        ("round8_narrow_scan_summary.csv", "round8 repeat-stable summary"),
        ("round8_narrow_scan_repeat_rows.csv", "round8 repeat rows"),
        ("round15_risk_rescan_summary.csv", "round15 failed micro-tuning summary"),
        ("round16_structural_scan_summary.csv", "round16 structural scan summary"),
        ("round17_structural_confirm_repeat_rows.csv", "round17 repeat confirmation"),
        ("round17_structural_confirm_risk_rows.csv", "round17 risk-pair rows"),
        ("round18_expanded_ood_sample_summary.csv", "round18 expanded OOD sample summary"),
        ("figure5_paired_diagnostic_panel.png", "Fig. 5 assembled panel image"),
    ]:
        rows.append({"artifact_name": name, "artifact_type": "raw_output", "location": str(OUT / name), "status": "available", "role": role, "source": "imported from previous archived project space into current project space"})
    for name in [
        "figure5_source_data.csv",
        "figure5_formal_summary.md",
        "figure5_caption_package.md",
        "data_availability.md",
        "code_availability.md",
        "methods_reproducibility.md",
    ]:
        rows.append({"artifact_name": name, "artifact_type": "submission_support", "location": str(SUB / name), "status": "generated", "role": "manuscript-support file", "source": "generated from raw-output chain in current project space"})
    write_csv(rows, SUB / "reproducibility_registry.csv")


def md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def generate_md5() -> None:
    targets = [
        PROJECT_ROOT / "code" / "project-scripts" / "round6_numpy_passive_d2nn.py",
        PROJECT_ROOT / "code" / "project-scripts" / "generate_figure5_formal_package.py",
        OUT / "round6_numpy_passive_d2nn_metrics.csv",
        OUT / "round7_parameter_scan_summary.csv",
        OUT / "round8_narrow_scan_summary.csv",
        OUT / "round15_risk_rescan_summary.csv",
        OUT / "round16_structural_scan_summary.csv",
        OUT / "round17_structural_confirm_repeat_rows.csv",
        OUT / "round18_expanded_ood_sample_summary.csv",
        OUT / "figure5_paired_diagnostic_panel.png",
        SUB / "figure5_source_data.csv",
        SUB / "figure5_formal_summary.md",
        SUB / "figure5_caption_package.md",
        SUB / "data_availability.md",
        SUB / "code_availability.md",
        SUB / "methods_reproducibility.md",
        SUB / "reproducibility_registry.csv",
    ]
    rows = [{"path": str(p), "file_name": p.name, "md5": md5(p), "size_bytes": p.stat().st_size} for p in targets]
    write_csv(rows, SUB / "md5_registry.csv")


def main() -> None:
    ensure_dirs()
    generate_source_data()
    generate_summary_docs()
    generate_availability_and_methods()
    generate_registry()
    generate_md5()


if __name__ == "__main__":
    main()
