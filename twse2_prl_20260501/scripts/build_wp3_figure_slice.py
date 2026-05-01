from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def load_best_cases() -> list[dict[str, object]]:
    return json.loads((RESULTS / "wp3_btk_best_cases.json").read_text())


def load_curves() -> list[dict[str, str]]:
    with (RESULTS / "wp3_btk_conductance_curves.csv").open() as handle:
        return list(csv.DictReader(handle))


def filter_rows(rows: list[dict[str, str]], candidate: str, eta: float, alpha: float, barrier: float) -> list[dict[str, str]]:
    selected = []
    for row in rows:
        if row["candidate"] != candidate:
            continue
        if abs(float(row["eta"]) - eta) > 1e-9:
            continue
        if abs(float(row["alpha"]) - alpha) > 1e-9:
            continue
        if abs(float(row["barrier_Z"]) - barrier) > 1e-9:
            continue
        selected.append(row)
    return selected


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    best_cases = load_best_cases()
    curves = load_curves()

    source_rows: list[list[object]] = []
    annotation_rows: list[list[object]] = []

    for case in best_cases:
        candidate = str(case["candidate"])
        eta = float(case["eta"])
        alpha = float(case["alpha"])
        barrier = float(case["barrier_Z"])
        subset = filter_rows(curves, candidate, eta, alpha, barrier)
        background = min(float(row["conductance"]) for row in subset)

        for row in subset:
            conductance = float(row["conductance"])
            source_rows.append(
                [
                    candidate,
                    eta,
                    alpha,
                    barrier,
                    float(row["bias"]),
                    conductance,
                    conductance - 1.0,
                    conductance - background,
                    float(row["mean_frustration"]),
                ]
            )

        annotation_rows.append(
            [
                candidate,
                eta,
                alpha,
                barrier,
                float(case["zero_bias_conductance"]),
                float(case["peak_conductance"]),
                float(case["peak_bias"]),
                float(case["peak_split"]),
                float(case["mean_frustration"]),
                str(case["signature"]),
            ]
        )

    write_csv(
        RESULTS / "wp3_prl_figure_slice_source_data.csv",
        [
            "candidate",
            "eta",
            "alpha",
            "barrier_Z",
            "bias",
            "conductance",
            "conductance_minus_one",
            "conductance_minus_curve_min",
            "mean_frustration",
        ],
        source_rows,
    )
    write_csv(
        RESULTS / "wp3_prl_figure_slice_annotations.csv",
        [
            "candidate",
            "eta",
            "alpha",
            "barrier_Z",
            "zero_bias_conductance",
            "peak_conductance",
            "peak_bias",
            "peak_split",
            "mean_frustration",
            "signature",
        ],
        annotation_rows,
    )

    lines = [
        "# WP3 PRL Figure Slice",
        "",
        "## Panel intent",
        "- Single-panel comparison of the three best candidate-resolved conductance traces from the minimal WP3 proxy.",
        "- Use `conductance_minus_one` for a raw BTK-style excess-conductance panel.",
        "- Use `conductance_minus_curve_min` if a baseline-shifted visual comparison is preferred.",
        "",
        "## Included traces",
    ]
    for case in best_cases:
        lines.append(
            f"- {case['candidate']}: eta={float(case['eta']):.2f}, alpha={float(case['alpha']):.3f}, Z={float(case['barrier_Z']):.2f}, "
            f"peak_bias={float(case['peak_bias']):.3f}, peak_split={float(case['peak_split']):.3f}, signature={case['signature']}"
        )
    lines.extend(
        [
            "",
            "## Recommended caption skeleton",
            "- Representative conductance traces from the minimal candidate-resolved BTK proxy.",
            "- The conventional s-wave case shows a broad zero-bias-centered enhancement without resolved finite-bias splitting.",
            "- The s_pm case becomes strongly zero-bias-enhanced only in the intervalley-active limit.",
            "- The chiral case instead develops a finite-bias-dominant subgap structure with a resolved split scale in the best slice.",
            "",
            "## Files",
            "- `wp3_prl_figure_slice_source_data.csv`: plot-ready traces.",
            "- `wp3_prl_figure_slice_annotations.csv`: peak and parameter annotations.",
        ]
    )
    (RESULTS / "wp3_prl_figure_slice_notes.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print((RESULTS / "wp3_prl_figure_slice_notes.md").read_text())


if __name__ == "__main__":
    main()
