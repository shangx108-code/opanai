#!/usr/bin/env python3
"""Generate a Figure-3 candidate panel for same-axis activation comparisons."""

from __future__ import annotations

import csv
import math
from pathlib import Path


EPSILON_MIN = 0.01
EPSILON_MAX = 0.10
ETAS = (0.99, 0.70, 0.50)
SAMPLES = 160

ROOT = Path("/workspace/memory/photonic-activation-natphoton")
OUTDIR = ROOT / "figure3_same_axis_panel"


def lower_bound_error(n_bar: float) -> float:
    return 0.5 * (1.0 - math.sqrt(1.0 - math.exp(-4.0 * n_bar)))


def lower_bound_inverse(epsilon: float) -> float:
    return 0.25 * math.log(1.0 / (4.0 * epsilon * (1.0 - epsilon)))


def homodyne_error(n_bar: float, eta: float) -> float:
    return 0.5 * math.erfc(math.sqrt(2.0 * eta * n_bar))


def invert_homodyne_error(epsilon: float, eta: float) -> float:
    lo, hi = 0.0, 20.0
    for _ in range(240):
        mid = 0.5 * (lo + hi)
        if homodyne_error(mid, eta) > epsilon:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def kennedy_inverse(epsilon: float, eta: float, dark_count: float = 0.0) -> float:
    if 2.0 * epsilon <= dark_count:
        raise ValueError("Target error is below the dark-count floor.")
    return math.log((1.0 - dark_count) / (2.0 * epsilon - dark_count)) / (4.0 * eta)


def log_spaced(lo: float, hi: float, count: int) -> list[float]:
    step = (math.log10(hi) - math.log10(lo)) / (count - 1)
    return [10 ** (math.log10(lo) + i * step) for i in range(count)]


def x_map(epsilon: float, left: float, width: float) -> float:
    log_min = math.log10(EPSILON_MIN)
    log_max = math.log10(EPSILON_MAX)
    t = (math.log10(epsilon) - log_min) / (log_max - log_min)
    return left + width * t


def y_map(value: float, lo: float, hi: float, top: float, height: float) -> float:
    t = (value - lo) / (hi - lo)
    return top + height * (1.0 - t)


def polyline(points: list[tuple[float, float]], color: str, width: float, dash: str = "") -> str:
    joined = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline fill="none" stroke="{color}" stroke-width="{width:.2f}"'
        f'{dash_attr} points="{joined}" />'
    )


def text(x: float, y: float, value: str, size: int = 16, anchor: str = "start", weight: str = "400") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Helvetica, Arial, sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="#111827">{value}</text>'
    )


def line(x1: float, y1: float, x2: float, y2: float, color: str = "#9ca3af", width: float = 1.2, dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" '
        f'stroke="{color}" stroke-width="{width:.2f}"{dash_attr} />'
    )


def rect(x: float, y: float, width: float, height: float, fill: str, stroke: str = "none", stroke_width: float = 0.0) -> str:
    return (
        f'<rect x="{x:.2f}" y="{y:.2f}" width="{width:.2f}" height="{height:.2f}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.2f}" rx="4" ry="4" />'
    )


def build_dataset() -> list[dict[str, float | str]]:
    dataset: list[dict[str, float | str]] = []
    for epsilon in log_spaced(EPSILON_MIN, EPSILON_MAX, SAMPLES):
        n_lb = lower_bound_inverse(epsilon)
        dataset.append(
            {
                "epsilon": epsilon,
                "route": "lower-bound",
                "eta": "",
                "n_bar": n_lb,
                "ratio_to_lb": 1.0,
            }
        )
        for eta in ETAS:
            n_hom = invert_homodyne_error(epsilon, eta)
            n_ken = kennedy_inverse(epsilon, eta)
            dataset.append(
                {
                    "epsilon": epsilon,
                    "route": "homodyne",
                    "eta": eta,
                    "n_bar": n_hom,
                    "ratio_to_lb": n_hom / n_lb,
                }
            )
            dataset.append(
                {
                    "epsilon": epsilon,
                    "route": "on-off",
                    "eta": eta,
                    "n_bar": n_ken,
                    "ratio_to_lb": n_ken / n_lb,
                }
            )
    return dataset


def write_csv(dataset: list[dict[str, float | str]]) -> Path:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTDIR / "figure3_same_axis_panel_data.csv"
    with csv_path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(handle, fieldnames=["epsilon", "route", "eta", "n_bar", "ratio_to_lb"])
        writer.writeheader()
        for row in dataset:
            writer.writerow(row)
    return csv_path


def draw_panel(dataset: list[dict[str, float | str]]) -> Path:
    width = 1280
    height = 860
    margin_left = 110
    margin_right = 50
    top_a = 90
    panel_width = width - margin_left - margin_right
    panel_height = 260
    gap = 110
    top_b = top_a + panel_height + gap

    top_ylim = (0.0, 3.0)
    bottom_ylim = (1.0, 3.6)

    colors = {
        ("homodyne", 0.99): "#2563eb",
        ("homodyne", 0.70): "#60a5fa",
        ("homodyne", 0.50): "#93c5fd",
        ("on-off", 0.99): "#b91c1c",
        ("on-off", 0.70): "#ef4444",
        ("on-off", 0.50): "#fca5a5",
        ("lower-bound", ""): "#111827",
    }

    grouped: dict[tuple[str, float | str], list[dict[str, float | str]]] = {}
    for row in dataset:
        key = (str(row["route"]), row["eta"])
        grouped.setdefault(key, []).append(row)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff" />',
        text(margin_left, 42, "Figure 3 Candidate | Same-axis boundary-cost comparison", size=28, weight="700"),
        text(
            margin_left,
            68,
            "Lower bound versus homodyne-conditioned and displaced on-off measurement routes for coherent-boundary discrimination",
            size=16,
        ),
        text(margin_left - 55, top_a - 18, "a", size=24, weight="700"),
        text(margin_left - 55, top_b - 18, "b", size=24, weight="700"),
    ]

    for y_value in (0.0, 1.0, 2.0, 3.0):
        y = y_map(y_value, *top_ylim, top_a, panel_height)
        parts.append(line(margin_left, y, margin_left + panel_width, y, color="#e5e7eb", width=1.0))
        parts.append(text(margin_left - 14, y + 5, f"{y_value:.1f}", size=14, anchor="end"))

    for y_value in (1.0, 1.5, 2.0, 2.5, 3.0, 3.5):
        y = y_map(y_value, *bottom_ylim, top_b, panel_height)
        parts.append(line(margin_left, y, margin_left + panel_width, y, color="#e5e7eb", width=1.0))
        parts.append(text(margin_left - 14, y + 5, f"{y_value:.1f}", size=14, anchor="end"))

    for epsilon, label in ((0.01, "0.01"), (0.02, "0.02"), (0.05, "0.05"), (0.10, "0.10")):
        x = x_map(epsilon, margin_left, panel_width)
        parts.append(line(x, top_a, x, top_a + panel_height, color="#e5e7eb", width=1.0))
        parts.append(line(x, top_b, x, top_b + panel_height, color="#e5e7eb", width=1.0))
        parts.append(text(x, top_a + panel_height + 28, label, size=14, anchor="middle"))
        parts.append(text(x, top_b + panel_height + 28, label, size=14, anchor="middle"))

    parts.extend(
        [
            line(margin_left, top_a, margin_left, top_a + panel_height, color="#111827", width=1.5),
            line(margin_left, top_a + panel_height, margin_left + panel_width, top_a + panel_height, color="#111827", width=1.5),
            line(margin_left, top_b, margin_left, top_b + panel_height, color="#111827", width=1.5),
            line(margin_left, top_b + panel_height, margin_left + panel_width, top_b + panel_height, color="#111827", width=1.5),
            text(margin_left + panel_width / 2, top_a + panel_height + 58, "Target boundary error ε", size=18, anchor="middle"),
            text(margin_left + panel_width / 2, top_b + panel_height + 58, "Target boundary error ε", size=18, anchor="middle"),
            text(28, top_a + panel_height / 2, "Required mean photons n̄", size=18),
            text(28, top_b + panel_height / 2, "Penalty ratio n̄ / n̄LB", size=18),
            text(margin_left, top_a - 24, "Photon cost versus target boundary error", size=18, weight="600"),
            text(margin_left, top_b - 24, "Constant-factor overhead above the lower bound", size=18, weight="600"),
        ]
    )

    for key, rows in grouped.items():
        route, eta = key
        rows.sort(key=lambda row: float(row["epsilon"]))
        if route == "lower-bound":
            top_points = [
                (x_map(float(row["epsilon"]), margin_left, panel_width), y_map(float(row["n_bar"]), *top_ylim, top_a, panel_height))
                for row in rows
            ]
            parts.append(polyline(top_points, colors[key], 3.8))
            continue

        top_points = [
            (x_map(float(row["epsilon"]), margin_left, panel_width), y_map(float(row["n_bar"]), *top_ylim, top_a, panel_height))
            for row in rows
        ]
        bottom_points = [
            (
                x_map(float(row["epsilon"]), margin_left, panel_width),
                y_map(float(row["ratio_to_lb"]), *bottom_ylim, top_b, panel_height),
            )
            for row in rows
        ]
        dash = "" if route == "homodyne" else "10 7"
        parts.append(polyline(top_points, colors[key], 3.0, dash=dash))
        parts.append(polyline(bottom_points, colors[key], 3.0, dash=dash))

    legend_x = 760
    legend_y = 108
    parts.append(rect(legend_x - 18, legend_y - 34, 425, 128, "#ffffff", stroke="#d1d5db", stroke_width=1.2))
    legend_items = [
        ("#111827", "", "Lower bound"),
        ("#2563eb", "", "Homodyne, η = 0.99"),
        ("#60a5fa", "", "Homodyne, η = 0.70"),
        ("#93c5fd", "", "Homodyne, η = 0.50"),
        ("#b91c1c", "10 7", "Displaced on-off, η = 0.99"),
        ("#ef4444", "10 7", "Displaced on-off, η = 0.70"),
        ("#fca5a5", "10 7", "Displaced on-off, η = 0.50"),
    ]
    for idx, (color, dash, label) in enumerate(legend_items):
        y = legend_y + idx * 18
        parts.append(line(legend_x, y, legend_x + 44, y, color=color, width=3.0, dash=dash))
        parts.append(text(legend_x + 56, y + 5, label, size=13))

    note_x = 800
    note_y = 508
    parts.append(rect(note_x - 20, note_y - 62, 370, 92, "#f9fafb", stroke="#d1d5db", stroke_width=1.0))
    parts.append(text(note_x, note_y - 28, "Observed design law in this model:", size=15, weight="600"))
    parts.append(text(note_x, note_y - 6, "Detector efficiency moves both routes together", size=14))
    parts.append(text(note_x, note_y + 14, "through the global 1/η penalty, while the", size=14))
    parts.append(text(note_x, note_y + 34, "measurement architecture sets the prefactor.", size=14))

    footer = "Curves computed from the saved analytical models in same_axis_metrics.py; dashed lines denote displaced on-off routes."
    parts.append(text(margin_left, height - 24, footer, size=13))
    parts.append("</svg>")

    svg_path = OUTDIR / "figure3_same_axis_panel.svg"
    svg_path.write_text("\n".join(parts), encoding="utf-8")
    return svg_path


def main() -> None:
    dataset = build_dataset()
    csv_path = write_csv(dataset)
    svg_path = draw_panel(dataset)
    print(f"Wrote data table to {csv_path}")
    print(f"Wrote SVG figure to {svg_path}")


if __name__ == "__main__":
    main()
