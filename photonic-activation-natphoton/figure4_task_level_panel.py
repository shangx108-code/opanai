#!/usr/bin/env python3
"""Render a manuscript-grade Figure 4 candidate from saved task-level outputs."""

from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SUMMARY_PATH = ROOT / "task_level_benchmark" / "task_level_benchmark_summary.json"
OUTDIR = ROOT / "figure4_task_level_panel"

TASK_ORDER = ("two_moons", "concentric_circles")
ETA_ORDER = (0.99, 0.70, 0.50)
BUDGET_ORDER = (1.0, 2.0, 4.0, 8.0, 16.0)

ETA_COLORS = {
    0.99: "#0f766e",
    0.70: "#14b8a6",
    0.50: "#99f6e4",
}

ROUTE_STYLES = {
    "homodyne": {"shape": "circle", "stroke": "#0f172a"},
    "on_off": {"shape": "diamond", "stroke": "#7f1d1d"},
}


def text(x: float, y: float, value: str, size: int = 16, anchor: str = "start", weight: str = "400", fill: str = "#111827") -> str:
    return (
        f'<text x="{x:.2f}" y="{y:.2f}" font-family="Helvetica, Arial, sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}">{value}</text>'
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


def polyline(points: list[tuple[float, float]], color: str, width: float) -> str:
    joined = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline fill="none" stroke="{color}" stroke-width="{width:.2f}" points="{joined}" />'


def circle(cx: float, cy: float, r: float, fill: str, stroke: str, stroke_width: float = 1.8) -> str:
    return (
        f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r:.2f}" fill="{fill}" '
        f'stroke="{stroke}" stroke-width="{stroke_width:.2f}" />'
    )


def diamond(cx: float, cy: float, r: float, fill: str, stroke: str, stroke_width: float = 1.8) -> str:
    points = [
        (cx, cy - r),
        (cx + r, cy),
        (cx, cy + r),
        (cx - r, cy),
    ]
    joined = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polygon points="{joined}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{stroke_width:.2f}" />'
    )


def marker(cx: float, cy: float, route: str, fill: str) -> str:
    style = ROUTE_STYLES[route]
    if style["shape"] == "circle":
        return circle(cx, cy, 6.0, fill, style["stroke"])
    return diamond(cx, cy, 6.8, fill, style["stroke"])


def load_summary() -> dict:
    return json.loads(SUMMARY_PATH.read_text(encoding="utf-8"))


def write_plot_table(rows: list[dict[str, float | str]]) -> Path:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUTDIR / "figure4_task_level_panel_data.csv"
    with csv_path.open("w", newline="", encoding="ascii") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "task",
                "eta",
                "total_budget",
                "best_route",
                "best_width",
                "best_test_accuracy",
                "linear_test_accuracy",
                "margin_vs_linear",
                "route_delta_on_off_minus_homodyne",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return csv_path


def x_map(index: int, left: float, width: float) -> float:
    if len(BUDGET_ORDER) == 1:
        return left + 0.5 * width
    return left + width * index / (len(BUDGET_ORDER) - 1)


def y_map(value: float, lo: float, hi: float, top: float, height: float) -> float:
    return top + height * (1.0 - (value - lo) / (hi - lo))


def collect_plot_rows(summary: dict) -> list[dict[str, float | str]]:
    route_delta_lookup = {
        (row["task"], float(row["eta"]), float(row["total_budget"])): float(row["on_off_minus_homodyne"])
        for row in summary["homodyne_vs_onoff"]
    }
    rows: list[dict[str, float | str]] = []
    for row in summary["best_implementable_per_condition"]:
        rows.append(
            {
                "task": row["task"],
                "eta": float(row["eta"]),
                "total_budget": float(row["total_budget"]),
                "best_route": row["route"],
                "best_width": int(row["width"]),
                "best_test_accuracy": float(row["mean_test_accuracy"]),
                "linear_test_accuracy": float(summary["linear_baseline"][row["task"]]),
                "margin_vs_linear": float(row["mean_test_accuracy"]) - float(summary["linear_baseline"][row["task"]]),
                "route_delta_on_off_minus_homodyne": route_delta_lookup[
                    (row["task"], float(row["eta"]), float(row["total_budget"]))
                ],
            }
        )
    rows.sort(key=lambda row: (TASK_ORDER.index(str(row["task"])), ETA_ORDER.index(float(row["eta"])), BUDGET_ORDER.index(float(row["total_budget"]))))
    return rows


def draw_svg(plot_rows: list[dict[str, float | str]], summary: dict) -> Path:
    width = 1400
    height = 980
    margin_left = 100
    panel_top = 165
    panel_width = 525
    panel_height = 330
    panel_gap = 110
    left_a = margin_left
    left_b = left_a + panel_width + panel_gap

    lower_top = 620
    lower_left = margin_left
    lower_width = width - 2 * margin_left
    cell_w = 72
    cell_h = 38
    group_gap = 18
    row_gap = 22

    y_lo = -0.30
    y_hi = 0.42

    by_task_eta: dict[tuple[str, float], list[dict[str, float | str]]] = {}
    for row in plot_rows:
        by_task_eta.setdefault((str(row["task"]), float(row["eta"])), []).append(row)

    for rows in by_task_eta.values():
        rows.sort(key=lambda row: BUDGET_ORDER.index(float(row["total_budget"])))

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#ffffff" />',
        text(margin_left, 44, "Figure 4 candidate | Task-level value of activation under a fixed photon budget", size=26, weight="700"),
        text(margin_left, 74, "Margins are measured against the task-specific linear no-activation baseline using the saved minimal benchmark outputs.", size=16),
        text(margin_left, 98, "Line color denotes detector efficiency eta. Marker shape denotes the best implementable route at that setting.", size=15),
        text(left_a - 45, panel_top - 18, "a", size=24, weight="700"),
        text(left_b - 45, panel_top - 18, "b", size=24, weight="700"),
        text(lower_left - 45, lower_top - 18, "c", size=24, weight="700"),
    ]

    panel_specs = [
        ("two_moons", left_a, "two_moons | strong linear baseline"),
        ("concentric_circles", left_b, "concentric_circles | weak linear baseline"),
    ]
    for task, left, title in panel_specs:
        parts.append(text(left, panel_top - 24, title, size=18, weight="600"))
        parts.append(rect(left, panel_top, panel_width, panel_height, "#ffffff", stroke="#111827", stroke_width=1.4))
        zero_y = y_map(0.0, y_lo, y_hi, panel_top, panel_height)
        parts.append(rect(left, panel_top, panel_width, zero_y - panel_top, "#ecfeff"))
        parts.append(rect(left, zero_y, panel_width, panel_top + panel_height - zero_y, "#fef2f2"))
        for y_value in (-0.30, -0.20, -0.10, 0.0, 0.10, 0.20, 0.30, 0.40):
            y = y_map(y_value, y_lo, y_hi, panel_top, panel_height)
            parts.append(line(left, y, left + panel_width, y, color="#e5e7eb", width=1.0))
            parts.append(text(left - 12, y + 5, f"{y_value:.1f}", size=13, anchor="end"))
        for idx, budget in enumerate(BUDGET_ORDER):
            x = x_map(idx, left + 20, panel_width - 40)
            parts.append(line(x, panel_top, x, panel_top + panel_height, color="#e5e7eb", width=1.0))
            parts.append(text(x, panel_top + panel_height + 26, f"{int(budget)}", size=13, anchor="middle"))
        parts.append(text(left + panel_width / 2, panel_top + panel_height + 56, "Total activation budget per inference", size=17, anchor="middle"))
        if task == "two_moons":
            parts.append(text(left - 68, panel_top + panel_height / 2, "Accuracy margin vs linear baseline", size=17, anchor="middle", weight="400"))

        for eta in ETA_ORDER:
            rows = by_task_eta[(task, eta)]
            points = [
                (
                    x_map(BUDGET_ORDER.index(float(row["total_budget"])), left + 20, panel_width - 40),
                    y_map(float(row["margin_vs_linear"]), y_lo, y_hi, panel_top, panel_height),
                )
                for row in rows
            ]
            color = ETA_COLORS[eta]
            parts.append(polyline(points, color, 3.4))
            for row, (x, y) in zip(rows, points):
                parts.append(marker(x, y, str(row["best_route"]), color))
                parts.append(text(x, y - 12, str(int(row["best_width"])), size=11, anchor="middle", fill="#334155"))

        positive_count = sum(1 for row in plot_rows if row["task"] == task and float(row["margin_vs_linear"]) > 0.02)
        total_count = sum(1 for row in plot_rows if row["task"] == task)
        note_fill = "#ecfeff" if task == "concentric_circles" else "#fff7ed"
        note_text = (
            f"Activation clearly worth paying for in {positive_count}/{total_count} settings"
            if task == "concentric_circles"
            else f"Activation clearly worth paying for in {positive_count}/{total_count} settings"
        )
        note_y = panel_top + 26 if task == "concentric_circles" else panel_top + 46
        parts.append(rect(left + 260, note_y - 18, 235, 34, note_fill, stroke="#cbd5e1", stroke_width=1.0))
        parts.append(text(left + 378, note_y + 4, note_text, size=12, anchor="middle", weight="600"))

    legend_x = left_b + 6
    legend_y = 118
    parts.append(rect(legend_x - 16, legend_y - 24, 455, 54, "#ffffff", stroke="#d1d5db", stroke_width=1.0))
    for idx, eta in enumerate(ETA_ORDER):
        x0 = legend_x + idx * 120
        parts.append(line(x0, legend_y, x0 + 34, legend_y, color=ETA_COLORS[eta], width=3.4))
        parts.append(text(x0 + 44, legend_y + 5, f"eta = {eta:.2f}", size=13))
    parts.append(circle(legend_x + 365, legend_y, 6.0, "#e2e8f0", "#0f172a"))
    parts.append(text(legend_x + 380, legend_y + 5, "homodyne best", size=13))
    parts.append(diamond(legend_x + 365, legend_y + 22, 6.8, "#e2e8f0", "#7f1d1d"))
    parts.append(text(legend_x + 380, legend_y + 27, "on-off best", size=13))

    parts.append(text(lower_left, lower_top - 24, "Route preference map: sign of (on-off accuracy - homodyne accuracy)", size=18, weight="600"))
    parts.append(text(lower_left, lower_top + cell_h * 2 + row_gap + 62, "Budget blocks are grouped by detector efficiency eta = 0.99, 0.70, 0.50 from left to right.", size=14))

    route_map = {
        (row["task"], float(row["eta"]), float(row["total_budget"])): float(row["route_delta_on_off_minus_homodyne"])
        for row in plot_rows
    }
    for row_idx, task in enumerate(TASK_ORDER):
        row_y = lower_top + row_idx * (cell_h + row_gap)
        parts.append(text(lower_left - 14, row_y + 24, task, size=14, anchor="end", weight="600"))
        cursor_x = lower_left
        for eta in ETA_ORDER:
            group_x = cursor_x
            parts.append(text(group_x + 2.5 * cell_w, row_y - 10, f"eta = {eta:.2f}", size=13, anchor="middle", weight="600"))
            for idx, budget in enumerate(BUDGET_ORDER):
                delta = route_map[(task, eta, budget)]
                fill = "#fecaca" if delta > 0 else "#bfdbfe"
                stroke = "#b91c1c" if delta > 0 else "#1d4ed8"
                label = f"{delta:+.3f}"
                x = group_x + idx * cell_w
                parts.append(rect(x, row_y, cell_w - 6, cell_h, fill, stroke=stroke, stroke_width=1.0))
                parts.append(text(x + (cell_w - 6) / 2, row_y + 16, f"B={int(budget)}", size=11, anchor="middle", weight="600"))
                parts.append(text(x + (cell_w - 6) / 2, row_y + 31, label, size=11, anchor="middle"))
            cursor_x += len(BUDGET_ORDER) * cell_w + group_gap

    note_x = lower_left + 860
    note_y = lower_top + 14
    parts.append(rect(note_x, note_y, 330, 110, "#f8fafc", stroke="#cbd5e1", stroke_width=1.0))
    parts.append(text(note_x + 16, note_y + 24, "Reviewer-safe readout:", size=15, weight="600"))
    parts.append(text(note_x + 16, note_y + 48, f"on-off beats homodyne in {summary['on_off_beats_homodyne_count']}/{summary['homodyne_comparison_count']} settings.", size=14))
    parts.append(text(note_x + 16, note_y + 70, "The best route switches with task geometry, eta, and budget.", size=14))
    parts.append(text(note_x + 16, note_y + 92, "Single-neuron closeness to the bound does not fix system-level preference.", size=14))

    footer = (
        "All values are drawn from task_level_benchmark_summary.json generated by the saved minimal benchmark. "
        "Width labels above markers denote the selected hidden-layer width for the best implementable route."
    )
    parts.append(text(margin_left, height - 24, footer, size=13))
    parts.append("</svg>")

    svg_path = OUTDIR / "figure4_task_level_panel.svg"
    svg_path.write_text("\n".join(parts), encoding="utf-8")

    png_path = OUTDIR / "figure4_task_level_panel.png"
    pdf_path = OUTDIR / "figure4_task_level_panel.pdf"
    subprocess.run(["inkscape", str(svg_path), "--export-filename", str(png_path)], check=True)
    subprocess.run(["inkscape", str(svg_path), "--export-filename", str(pdf_path)], check=True)
    return svg_path


def main() -> None:
    summary = load_summary()
    plot_rows = collect_plot_rows(summary)
    csv_path = write_plot_table(plot_rows)
    svg_path = draw_svg(plot_rows, summary)
    print(f"Wrote plot data to {csv_path}")
    print(f"Wrote SVG figure to {svg_path}")


if __name__ == "__main__":
    main()
