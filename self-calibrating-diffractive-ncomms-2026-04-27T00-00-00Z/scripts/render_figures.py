from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGS = ROOT / "figures"

WIDTH = 1800
HEIGHT = 1200
MARGIN = 90
PANEL_GAP = 60
BG = (255, 255, 255)
TEXT = (20, 24, 34)
AXIS = (90, 96, 112)
GRID = (225, 228, 235)
COMMON = (34, 124, 157)
NOREF = (187, 95, 84)
NONCOMMON = (232, 172, 65)
WRONG = (142, 118, 181)
TRAIN = (48, 126, 97)
OOD = (176, 72, 95)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def group_rows(rows: Iterable[dict[str, str]], key: str) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(row[key], []).append(row)
    return grouped


def draw_title(draw: ImageDraw.ImageDraw, title: str, subtitle: str) -> None:
    draw.text((MARGIN, 30), title, fill=TEXT, font=font(46, bold=True))
    draw.text((MARGIN, 82), subtitle, fill=AXIS, font=font(24))


def draw_bar_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    rows: list[dict[str, str]],
    value_key: str,
    ylabel: str,
    colors: dict[str, tuple[int, int, int]],
    lower_is_better: bool = False,
) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=24, outline=(230, 232, 238), width=3, fill=(250, 251, 253))
    draw.text((x0 + 24, y0 + 18), title, fill=TEXT, font=font(28, bold=True))
    plot_left = x0 + 80
    plot_right = x1 - 30
    plot_top = y0 + 90
    plot_bottom = y1 - 85
    values = [float(row[value_key]) for row in rows]
    vmin = 0.0 if all(v >= 0 for v in values) else min(values)
    vmax = max(values)
    if vmax == vmin:
        vmax += 1.0
    if lower_is_better:
        vmax *= 1.15
    else:
        vmax *= 1.05
    for i in range(5):
        y = plot_top + i * (plot_bottom - plot_top) / 4
        draw.line((plot_left, y, plot_right, y), fill=GRID, width=2)
        tick_value = vmax - i * (vmax - vmin) / 4
        label = f"{tick_value:.3g}"
        draw.text((x0 + 18, y - 12), label, fill=AXIS, font=font(19))
    draw.line((plot_left, plot_top, plot_left, plot_bottom), fill=AXIS, width=3)
    draw.line((plot_left, plot_bottom, plot_right, plot_bottom), fill=AXIS, width=3)
    bar_gap = 36
    n = len(rows)
    total_gap = bar_gap * (n + 1)
    bar_width = int((plot_right - plot_left - total_gap) / n)
    for idx, row in enumerate(rows):
        value = float(row[value_key])
        cond = row.get("condition", row.get("stage", f"bar{idx}"))
        bar_x0 = plot_left + bar_gap + idx * (bar_width + bar_gap)
        bar_x1 = bar_x0 + bar_width
        bar_height = (value - vmin) / (vmax - vmin) * (plot_bottom - plot_top)
        bar_y0 = plot_bottom - bar_height
        draw.rounded_rectangle((bar_x0, bar_y0, bar_x1, plot_bottom), radius=18, fill=colors.get(cond, COMMON))
        draw.text((bar_x0, plot_bottom + 10), cond.replace("_", "\n"), fill=TEXT, font=font(18), align="center")
        draw.text((bar_x0, bar_y0 - 28), f"{value:.3g}", fill=TEXT, font=font(18))
    draw.text((plot_left, y1 - 42), ylabel, fill=AXIS, font=font(20))


def draw_processor_stage_panel(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    rows: list[dict[str, str]],
) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=24, outline=(230, 232, 238), width=3, fill=(250, 251, 253))
    draw.text((x0 + 24, y0 + 18), title, fill=TEXT, font=font(28, bold=True))
    plot_left = x0 + 90
    plot_right = x1 - 40
    plot_top = y0 + 100
    plot_bottom = y1 - 80
    data = [row for row in rows if row["metric"] == "ood_psnr_delta_baseline" or row["stage"] in {"round5b", "round6_best"}]
    values = []
    labels = []
    colors = []
    for row in data:
        if row["stage"] == "round5" and row["condition"] == "common_path":
            values.append(float(row["value"]))
            labels.append("Round 5\ncommon - ordinary")
            colors.append(COMMON)
        elif row["stage"] == "round5b" and row["condition"] == "common_path":
            ordinary = next(float(r["value"]) for r in rows if r["stage"] == "round5b" and r["condition"] == "ordinary_d2nn")
            values.append(float(row["value"]) - ordinary)
            labels.append("Round 5b\ncommon - ordinary")
            colors.append(COMMON)
        elif row["stage"] == "round6_best" and row["condition"] == "common_path":
            ordinary = next(float(r["value"]) for r in rows if r["stage"] == "round6_best" and r["condition"] == "ordinary_d2nn")
            values.append(float(row["value"]) - ordinary)
            labels.append("Round 6 best\ncommon - ordinary")
            colors.append(COMMON)
        elif row["stage"] == "round6_matched":
            values.append(float(row["value"]))
            labels.append("Round 6 matched\ncommon - noncommon")
            colors.append(NONCOMMON)
    vmax = max(max(values), 0.25)
    vmin = min(min(values), -0.25)
    for i in range(5):
        y = plot_top + i * (plot_bottom - plot_top) / 4
        draw.line((plot_left, y, plot_right, y), fill=GRID, width=2)
        tick_value = vmax - i * (vmax - vmin) / 4
        draw.text((x0 + 16, y - 10), f"{tick_value:+.2f}", fill=AXIS, font=font(19))
    zero_y = plot_bottom - (0 - vmin) / (vmax - vmin) * (plot_bottom - plot_top)
    draw.line((plot_left, zero_y, plot_right, zero_y), fill=AXIS, width=3)
    draw.line((plot_left, plot_top, plot_left, plot_bottom), fill=AXIS, width=3)
    bar_gap = 38
    bar_width = int((plot_right - plot_left - bar_gap * (len(values) + 1)) / len(values))
    for idx, value in enumerate(values):
        x_start = plot_left + bar_gap + idx * (bar_width + bar_gap)
        x_end = x_start + bar_width
        y_val = plot_bottom - (value - vmin) / (vmax - vmin) * (plot_bottom - plot_top)
        y_bar0, y_bar1 = sorted((zero_y, y_val))
        draw.rounded_rectangle((x_start, y_bar0, x_end, y_bar1), radius=18, fill=colors[idx])
        draw.text((x_start, y_bar1 + 10 if value < 0 else y_bar0 - 30), f"{value:+.3f}", fill=TEXT, font=font(18))
        draw.multiline_text((x_start - 6, plot_bottom + 10), labels[idx], fill=TEXT, font=font(17), spacing=2, align="center")
    draw.text((plot_left, y1 - 42), "Processor-level PSNR gain (dB)", fill=AXIS, font=font(20))


def render_fig2() -> None:
    rows = read_rows(DATA / "fig2_mechanism_waveoptics.csv")
    grouped = group_rows(rows, "panel")
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw_title(draw, "Figure 2 | Mechanism and wave-optics validation", "All bars are derived from previously reported project values.")
    panel_width = (WIDTH - 2 * MARGIN - 2 * PANEL_GAP) // 3
    panel_height = HEIGHT - 170
    boxes = []
    for i in range(3):
        x0 = MARGIN + i * (panel_width + PANEL_GAP)
        boxes.append((x0, 130, x0 + panel_width, 130 + panel_height))
    color_map = {"no_reference": NOREF, "non_common_path": NONCOMMON, "common_path": COMMON}
    draw_bar_panel(draw, boxes[0], "a  Gaussian surrogate OOD PSNR", grouped["Fig2a"], "value", "PSNR (dB)", color_map)
    draw_bar_panel(draw, boxes[1], "b  Zernike wave-optics OOD PSNR", grouped["Fig2b"], "value", "PSNR (dB)", color_map)
    draw_bar_panel(draw, boxes[2], "c  Zernike wave-optics PSF mismatch", grouped["Fig2c"], "value", "Mean PSF MSE", color_map, lower_is_better=True)
    img.save(FIGS / "figure2_mechanism_waveoptics.png", dpi=(300, 300))


def render_fig3() -> None:
    rows = read_rows(DATA / "fig3_information_transfer.csv")
    grouped = group_rows(rows, "panel")
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw_title(draw, "Figure 3 | Local information and task transfer", "Panels summarize the verified CRLB-style and cross-task ledger values.")
    panel_width = (WIDTH - 2 * MARGIN - PANEL_GAP) // 2
    panel_height = (HEIGHT - 190 - PANEL_GAP) // 2
    boxes = [
        (MARGIN, 130, MARGIN + panel_width, 130 + panel_height),
        (MARGIN + panel_width + PANEL_GAP, 130, WIDTH - MARGIN, 130 + panel_height),
        (MARGIN, 130 + panel_height + PANEL_GAP, MARGIN + panel_width, HEIGHT - 40),
        (MARGIN + panel_width + PANEL_GAP, 130 + panel_height + PANEL_GAP, WIDTH - MARGIN, HEIGHT - 40),
    ]
    draw_bar_panel(draw, boxes[0], "a  CRLB-style Fisher information", grouped["Fig3a"], "value", "Median trace", {"train": TRAIN, "ood": OOD})
    draw_bar_panel(draw, boxes[1], "b  Reconstruction transfer", grouped["Fig3b"], "value", "PSNR (dB)", {"no_reference": NOREF, "common_path": COMMON})
    draw_bar_panel(draw, boxes[2], "c  Classification residual", grouped["Fig3c"], "value", "Residual", {"no_reference": NOREF, "common_path": COMMON}, lower_is_better=True)
    draw_bar_panel(draw, boxes[3], "d  Inverse-design target MSE", grouped["Fig3d"], "value", "Target MSE", {"no_reference": NOREF, "common_path": COMMON}, lower_is_better=True)
    img.save(FIGS / "figure3_information_transfer.png", dpi=(300, 300))


def render_fig4() -> None:
    rows = read_rows(DATA / "fig4_processor_boundary.csv")
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)
    draw_title(draw, "Figure 4 | Processor-level evidence boundary", "The current processor result remains bounded and regime dependent.")
    panel_width = (WIDTH - 2 * MARGIN - PANEL_GAP) // 2
    box_a = (MARGIN, 130, MARGIN + panel_width, HEIGHT - 60)
    box_b = (MARGIN + panel_width + PANEL_GAP, 130, WIDTH - MARGIN, HEIGHT - 60)
    draw_processor_stage_panel(draw, box_a, "a  Stage-wise processor gain", rows)
    round6_rows = [row for row in rows if row["stage"] == "round6_best"]
    draw_bar_panel(
        draw,
        box_b,
        "b  Round 6 best OOD PSNR",
        round6_rows,
        "value",
        "PSNR (dB)",
        {
            "ordinary_d2nn": AXIS,
            "common_path": COMMON,
            "non_common_path": NONCOMMON,
            "wrong_reference": WRONG,
        },
    )
    img.save(FIGS / "figure4_processor_boundary.png", dpi=(300, 300))


def main() -> None:
    FIGS.mkdir(parents=True, exist_ok=True)
    render_fig2()
    render_fig3()
    render_fig4()


if __name__ == "__main__":
    main()
