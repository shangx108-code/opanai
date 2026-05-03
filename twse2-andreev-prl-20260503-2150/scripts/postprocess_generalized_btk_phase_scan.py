from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCAN_DIR = ROOT / "results" / "generalized_btk_phase_scan"
GITHUB_DIR = SCAN_DIR / "github_mirror"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open() as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def choose_best_case(rows: list[dict[str, str]], pairing: str) -> dict[str, str]:
    candidates = [row for row in rows if row["pairing"] == pairing]
    return max(candidates, key=lambda row: float(row["alpha_anisotropy"]))


def nearest_alpha(rows: list[dict[str, str]], target: float) -> str:
    return min(rows, key=lambda row: abs(float(row["alpha"]) - target))["alpha"]


def main() -> None:
    GITHUB_DIR.mkdir(parents=True, exist_ok=True)
    summary_rows = read_csv(SCAN_DIR / "phase_scan_summary.csv")
    curve_rows = read_csv(SCAN_DIR / "conductance_curves.csv")

    top_cases = sorted(summary_rows, key=lambda row: float(row["alpha_anisotropy"]), reverse=True)[:12]
    write_csv(
        SCAN_DIR / "top_phase_cases.csv",
        list(top_cases[0].keys()),
        top_cases,
    )

    selected_cases = [
        choose_best_case(summary_rows, "s_wave"),
        choose_best_case(summary_rows, "s_pm"),
        choose_best_case(summary_rows, "chiral"),
    ]

    compact_rows: list[dict[str, str]] = []
    case_manifest_rows: list[dict[str, str]] = []
    for case in selected_cases:
        case_key = {
            "pairing": case["pairing"],
            "barrier_Z": case["barrier_Z"],
            "eta": case["eta"],
            "field_strength": case["field_strength"],
            "phi": case["phi"],
        }
        matching = [
            row
            for row in curve_rows
            if all(row[key] == value for key, value in case_key.items())
        ]
        unique_alpha_rows = []
        seen_alpha = set()
        for row in matching:
            alpha = row["alpha"]
            if alpha not in seen_alpha:
                unique_alpha_rows.append(row)
                seen_alpha.add(alpha)

        alpha_max = case["alpha_at_max_peak_contrast"]
        alpha_min = case["alpha_at_min_peak_contrast"]
        alpha_mid = nearest_alpha(unique_alpha_rows, target=0.7853981633974483)
        chosen_alphas = {alpha_max, alpha_min, alpha_mid}

        for row in matching:
            if row["alpha"] in chosen_alphas:
                compact_rows.append(row)

        case_manifest_rows.append(
            {
                "pairing": case["pairing"],
                "barrier_Z": case["barrier_Z"],
                "eta": case["eta"],
                "field_strength": case["field_strength"],
                "phi": case["phi"],
                "alpha_at_max_peak_contrast": alpha_max,
                "alpha_at_min_peak_contrast": alpha_min,
                "alpha_mid_reference": alpha_mid,
                "alpha_anisotropy": case["alpha_anisotropy"],
                "mean_peak_contrast": case["mean_peak_contrast"],
            }
        )

    write_csv(
        SCAN_DIR / "compact_reference_curves.csv",
        list(compact_rows[0].keys()),
        compact_rows,
    )
    write_csv(
        SCAN_DIR / "compact_reference_cases.csv",
        list(case_manifest_rows[0].keys()),
        case_manifest_rows,
    )

    summary_lines = [
        "# Generalized BTK Compact Package",
        "",
        "- Purpose: GitHub-friendly compact mirror for the much larger local raw conductance grid",
        "- Included cases: best s-wave, best s_pm, best chiral by alpha anisotropy",
        "- Included alphas per case: max-contrast alpha, min-contrast alpha, and mid-angle reference",
        f"- Top anisotropy cases stored separately: {len(top_cases)}",
        f"- Compact curve rows: {len(compact_rows)}",
        "- Full raw `conductance_curves.csv` remains the authoritative local dense grid",
    ]
    (SCAN_DIR / "compact_package_summary.md").write_text("\n".join(summary_lines) + "\n")

    github_curve_rows = compact_rows[::5]
    github_top_cases = top_cases[:8]
    write_csv(
        GITHUB_DIR / "top_phase_cases_github.csv",
        list(github_top_cases[0].keys()),
        github_top_cases,
    )
    write_csv(
        GITHUB_DIR / "compact_reference_cases_github.csv",
        list(case_manifest_rows[0].keys()),
        case_manifest_rows,
    )
    write_csv(
        GITHUB_DIR / "compact_reference_curves_github.csv",
        list(github_curve_rows[0].keys()),
        github_curve_rows,
    )
    github_lines = [
        "# Generalized BTK GitHub Mirror Package",
        "",
        "- Purpose: small GitHub mirror derived from the canonical local dense conductance grid",
        f"- Stored top anisotropy cases: {len(github_top_cases)}",
        f"- Stored compact reference cases: {len(case_manifest_rows)}",
        f"- Stored sparse curve rows: {len(github_curve_rows)}",
        "- Full dense `conductance_curves.csv` remains in the canonical local project space",
    ]
    (GITHUB_DIR / "github_mirror_summary.md").write_text("\n".join(github_lines) + "\n")
    print((SCAN_DIR / "compact_package_summary.md").read_text())


if __name__ == "__main__":
    main()
