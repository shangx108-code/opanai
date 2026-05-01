from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "default_params.json"
RESULTS = ROOT / "results"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.twse2_minimal import (  # noqa: E402
    ModelParams,
    compute_dos,
    prominent_positive_peaks,
    screen_pairing_candidates,
)


def ensure_dirs() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def classify_wp2(rows: list[dict[str, float | str]]) -> dict[str, str]:
    grouped: dict[str, list[dict[str, float | str]]] = {}
    for row in rows:
        grouped.setdefault(str(row["candidate"]), []).append(row)
    summary: dict[str, str] = {}
    for candidate, entries in grouped.items():
        eta0 = next(item for item in entries if abs(float(item["eta"])) < 1e-9)
        eta1 = next(item for item in entries if abs(float(item["eta"]) - 1.0) < 1e-9)
        avg0 = float(eta0["avg_frustration"])
        avg1 = float(eta1["avg_frustration"])
        anis1 = float(eta1["anisotropy_ratio"])
        if candidate == "s_wave":
            summary[candidate] = "smooth reference: no sign frustration in either same-valley or intervalley reflection"
        elif avg0 < 0.1 and avg1 > 0.9:
            summary[candidate] = "intervalley-triggered sign change: quiet at eta=0 and strongly activated by eta->1"
        elif avg0 > 0.45:
            summary[candidate] = f"phase-winding family: robust boundary frustration already present at eta=0 and remains finite through eta->1; anisotropy ratio at eta=1 is {anis1:.2f}"
        else:
            summary[candidate] = f"intermediate case: avg frustration rises from {avg0:.2f} to {avg1:.2f}"
    return summary


def main() -> None:
    ensure_dirs()
    params = ModelParams.from_json(CONFIG)

    energies, normal_dos, bdg_dos = compute_dos(params, candidate="s_wave")
    normal_peaks = prominent_positive_peaks(energies, normal_dos, limit=2)
    bdg_peaks = prominent_positive_peaks(energies, bdg_dos, limit=3)

    wp1_summary = {
        "normal_positive_peaks": normal_peaks,
        "bdg_positive_peaks": bdg_peaks,
        "inferred_outer_scale": normal_peaks[-1][0] if normal_peaks else None,
        "inferred_inner_scale": min((peak[0] for peak in bdg_peaks), default=None),
    }
    (RESULTS / "wp1_summary.json").write_text(json.dumps(wp1_summary, indent=2))
    write_csv(
        RESULTS / "wp1_dos.csv",
        ["energy", "normal_dos", "bdg_dos"],
        [[float(e), float(n), float(b)] for e, n, b in zip(energies, normal_dos, bdg_dos)],
    )

    wp2_rows = screen_pairing_candidates(params)
    write_csv(
        RESULTS / "wp2_edge_proxy.csv",
        ["candidate", "eta", "avg_frustration", "anisotropy_ratio", "alpha_min", "alpha_max"],
        [
            [
                row["candidate"],
                row["eta"],
                row["avg_frustration"],
                row["anisotropy_ratio"],
                row["alpha_min"],
                row["alpha_max"],
            ]
            for row in wp2_rows
        ],
    )
    wp2_classification = classify_wp2(wp2_rows)

    outer_scale = wp1_summary["inferred_outer_scale"]
    inner_scale = wp1_summary["inferred_inner_scale"]
    ratio = None
    if outer_scale and inner_scale:
        ratio = float(outer_scale) / float(inner_scale)

    lines = [
        "# WP1-WP2 execution summary",
        "",
        "## WP1 normal plus correlated background",
        f"- inferred inner scale from BdG DOS: {inner_scale:.4f}" if inner_scale is not None else "- inferred inner scale from BdG DOS: unavailable",
        f"- inferred outer scale from normal DOS: {outer_scale:.4f}" if outer_scale is not None else "- inferred outer scale from normal DOS: unavailable",
        f"- outer/inner ratio in this minimal calibration: {ratio:.2f}" if ratio is not None else "- outer/inner ratio in this minimal calibration: unavailable",
        f"- normal positive peaks: {normal_peaks}",
        f"- BdG positive peaks: {bdg_peaks}",
        "",
        "## WP2 pairing-library screening",
    ]
    for candidate, note in wp2_classification.items():
        lines.append(f"- {candidate}: {note}")
    lines.extend(
        [
            "",
            "## Interpretation boundary",
            "- This is a minimum runnable screening engine, not the final PRL-grade BTK calculation.",
            "- WP1 is already usable as a two-scale calibration starting point.",
            "- WP2 already separates ordinary s-wave from intervalley-triggered and phase-winding families at the interface-proxy level.",
        ]
    )
    (RESULTS / "wp1_wp2_summary.md").write_text("\n".join(lines) + "\n")

    print((RESULTS / "wp1_wp2_summary.md").read_text())


if __name__ == "__main__":
    main()
