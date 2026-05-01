from __future__ import annotations

import csv
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path("/workspace/self-calibrating-diffractive-ncomms")
OUT = ROOT / "outputs"

ROUND8_SUMMARY_CSV = OUT / "round8_narrow_scan_summary.csv"
ROUND17_SUMMARY_JSON = OUT / "round17_structural_confirm_summary.json"
ROUND17_REPEAT_CSV = OUT / "round17_structural_confirm_repeat_rows.csv"
ROUND17_PANEL = OUT / "round17_structural_confirm_best_panel.png"
ROUND17_RISK_REPEAT_CSV = OUT / "round17_structural_confirm_risk_rows.csv"

FIG_PNG = OUT / "figure5_paired_diagnostic_panel.png"
FIG_PDF = OUT / "figure5_paired_diagnostic_panel.pdf"
FIG_SUMMARY_MD = OUT / "figure5_paired_diagnostic_panel_summary.md"

WIDTH = 1680
HEIGHT = 1040
MARGIN = 40
GAP = 28
HEADER_H = 58
PANEL_W = (WIDTH - 2 * MARGIN - GAP) // 2
PANEL_H = (HEIGHT - HEADER_H - 2 * MARGIN - GAP) // 2

BG = (247, 248, 250)
INK = (22, 27, 32)
SUB = (78, 89, 102)
ACCENT = (31, 90, 155)
GOOD = (44, 127, 85)
WARN = (201, 133, 30)
BAD = (183, 63, 63)
LINE = (210, 216, 224)
CARD = (255, 255, 255)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = ["DejaVuSans-Bold.ttf", "Arial Bold.ttf"] if bold else ["DejaVuSans.ttf", "Arial.ttf"]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONT_TITLE = load_font(26, bold=True)
FONT_SUB = load_font(15)
FONT_PANEL = load_font(19, bold=True)
FONT_BODY = load_font(15)
FONT_SMALL = load_font(13)
FONT_TINY = load_font(11)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def draw_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=18, fill=CARD, outline=LINE, width=2)
    draw.text((x0 + 18, y0 + 14), title, font=FONT_PANEL, fill=INK)
    draw.line((x0 + 18, y0 + 48, x1 - 18, y0 + 48), fill=LINE, width=2)


def paste_scaled(base: Image.Image, overlay: Image.Image, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    ow, oh = overlay.size
    scale = min((x1 - x0) / ow, (y1 - y0) / oh)
    nw = max(1, int(ow * scale))
    nh = max(1, int(oh * scale))
    resized = overlay.resize((nw, nh), Image.Resampling.NEAREST)
    px = x0 + (x1 - x0 - nw) // 2
    py = y0 + (y1 - y0 - nh) // 2
    base.paste(resized, (px, py))


def bar(draw: ImageDraw.ImageDraw, x: int, y: int, width: int, height: int, value: float, vmin: float, vmax: float, fill: tuple[int, int, int]) -> None:
    draw.rounded_rectangle((x, y, x + width, y + height), radius=8, fill=(240, 242, 245))
    norm = 0 if vmax == vmin else (value - vmin) / (vmax - vmin)
    fill_w = int(width * max(0.0, min(1.0, norm)))
    if fill_w > 0:
        draw.rounded_rectangle((x, y, x + fill_w, y + height), radius=8, fill=fill)


def draw_repeat_bars(draw: ImageDraw.ImageDraw, rows: list[dict[str, str]], box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    width = x1 - x0
    draw.text((x0, y0), "Stable ordinary window", font=FONT_BODY, fill=INK)
    draw.text((x0, y0 + 20), "round8 best: L=1, w=0.16, p=0.15", font=FONT_SMALL, fill=SUB)
    best = max(rows, key=lambda r: float(r["common_minus_ordinary_db_mean"]))
    metrics = [
        ("mean common - ordinary", float(best["common_minus_ordinary_db_mean"]), 0.0, 0.6, GOOD),
        ("min common - ordinary", float(best["common_minus_ordinary_db_min"]), 0.0, 0.5, GOOD),
        ("mean common - wrongref", float(best["common_minus_wrongref_db_mean"]), -0.1, 0.15, WARN),
    ]
    cy = y0 + 50
    for label, value, vmin, vmax, color in metrics:
        draw.text((x0, cy), f"{label}: {value:+.3f} dB", font=FONT_SMALL, fill=INK)
        bar(draw, x0 + 222, cy + 1, width - 238, 16, value, vmin, vmax, color)
        cy += 28
    draw.text((x0, cy + 2), "Preview strip: best wrong-reference-v2 config", font=FONT_SMALL, fill=INK)


def draw_repeat_signs(draw: ImageDraw.ImageDraw, repeat_rows: list[dict[str, str]], summary: dict, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw.text((x0, y0), "Paired diagnostics", font=FONT_BODY, fill=INK)
    stats = summary
    summary_lines = [
        f"risk-pair positive fraction: {stats['risk_pair_positive_fraction']:.3f}",
        f"risk-pair q10 margin: {stats['risk_pair_q10_db']:+.3f} dB",
        f"mean common - wrongref: {stats['common_minus_wrongref_db_mean']:+.3f} dB",
        f"worst repeat common - wrongref: {stats['common_minus_wrongref_db_min']:+.3f} dB",
    ]
    yy = y0 + 22
    for line in summary_lines:
        draw.text((x0, yy), line, font=FONT_SMALL, fill=SUB if "fraction" not in line else INK)
        yy += 18

    chart_x0 = x0
    chart_y0 = yy + 10
    chart_x1 = x1 - 8
    chart_y1 = y1 - 16
    draw.rectangle((chart_x0, chart_y0, chart_x1, chart_y1), outline=LINE, width=1)
    zero_y = chart_y0 + int((chart_y1 - chart_y0) * 0.52)
    draw.line((chart_x0 + 8, zero_y, chart_x1 - 8, zero_y), fill=LINE, width=2)
    draw.text((chart_x0 + 8, zero_y - 18), "0", font=FONT_TINY, fill=SUB)

    vals = [float(r["common_minus_wrongref_db"]) for r in repeat_rows]
    vmin = min(min(vals), -0.06)
    vmax = max(max(vals), 0.20)
    step_x = (chart_x1 - chart_x0 - 40) / len(repeat_rows)
    for idx, row in enumerate(sorted(repeat_rows, key=lambda r: int(r["repeat_seed"]))):
        value = float(row["common_minus_wrongref_db"])
        x = chart_x0 + 24 + idx * step_x
        height = int((value - 0) / (vmax - vmin) * (chart_y1 - chart_y0 - 24))
        if value >= 0:
            top = zero_y - height
            bottom = zero_y
            color = GOOD
        else:
            top = zero_y
            bottom = zero_y - height
            color = BAD
        draw.rounded_rectangle((int(x), int(top), int(x + step_x * 0.55), int(bottom)), radius=6, fill=color)
        draw.text((int(x), chart_y1 - 16), f"r{row['repeat_seed']}", font=FONT_TINY, fill=SUB)
    draw.text((chart_x0 + 10, chart_y0 + 6), "repeat-level common - wrongref", font=FONT_TINY, fill=SUB)


def summarize_risk_rows(risk_rows: list[dict[str, str]]) -> list[dict[str, float | str]]:
    rows_by_sample: dict[str, list[dict[str, str]]] = {}
    for row in risk_rows:
        rows_by_sample.setdefault(row["sample"], []).append(row)
    summary = []
    for sample, rows in rows_by_sample.items():
        values = [float(r["common_minus_wrongref_db"]) for r in rows]
        positive = sum(1 for value in values if value > 0)
        summary.append(
            {
                "sample": sample,
                "common_minus_wrongref_db_mean": sum(values) / len(values),
                "common_minus_wrongref_db_min": min(values),
                "common_minus_wrongref_positive_rate": positive / len(values),
            }
        )
    return summary


def draw_risk_sample_panel(draw: ImageDraw.ImageDraw, risk_rows: list[dict[str, str]], risk_summary: list[dict[str, float | str]], box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw.text((x0, y0), "Risk samples", font=FONT_BODY, fill=INK)
    note = "frame and two_spots are now mostly positive, but one negative tail event still survives"
    draw.text((x0, y0 + 24), note, font=FONT_SMALL, fill=SUB)

    inner_y = y0 + 58
    sample_boxes = [
        (x0, inner_y, x0 + (x1 - x0 - 16) // 2, y1),
        (x0 + (x1 - x0 - 16) // 2 + 16, inner_y, x1, y1),
    ]
    for sample, sbox in zip(["frame", "two_spots"], sample_boxes):
        sx0, sy0, sx1, sy1 = sbox
        draw.rounded_rectangle(sbox, radius=12, fill=(250, 251, 252), outline=LINE, width=1)
        summary = next(item for item in risk_summary if item["sample"] == sample)
        draw.text((sx0 + 12, sy0 + 10), sample, font=FONT_SMALL, fill=INK)
        draw.text((sx0 + 12, sy0 + 30), f"mean/min: {float(summary['common_minus_wrongref_db_mean']):+.3f}/{float(summary['common_minus_wrongref_db_min']):+.3f} dB", font=FONT_TINY, fill=SUB)
        draw.text((sx0 + 12, sy0 + 46), f"positive rate: {float(summary['common_minus_wrongref_positive_rate']):.3f}", font=FONT_TINY, fill=SUB)
        baseline = sy1 - 34
        draw.line((sx0 + 12, baseline, sx1 - 12, baseline), fill=LINE, width=2)
        vals = [float(r["common_minus_wrongref_db"]) for r in risk_rows if r["sample"] == sample]
        vmin = min(min(vals), -0.18)
        vmax = max(max(vals), 0.26)
        step = (sx1 - sx0 - 36) / len(vals)
        for idx, row in enumerate(sorted([r for r in risk_rows if r["sample"] == sample], key=lambda r: int(r["repeat_seed"]))):
            value = float(row["common_minus_wrongref_db"])
            bar_h = int((value - 0) / (vmax - vmin) * (baseline - sy0 - 74))
            bx = sx0 + 18 + idx * step
            if value >= 0:
                top = baseline - bar_h
                bottom = baseline
                color = GOOD
            else:
                top = baseline
                bottom = baseline - bar_h
                color = BAD
            draw.rounded_rectangle((int(bx), int(top), int(bx + step * 0.5), int(bottom)), radius=5, fill=color)
        draw.text((sx0 + 12, baseline - 14), "0", font=FONT_TINY, fill=SUB)


def draw_protocol_panel(base: Image.Image, draw: ImageDraw.ImageDraw, best_panel: Image.Image, round17_summary: dict, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw.text((x0, y0), "Protocol + preview", font=FONT_BODY, fill=INK)
    info = [
        "controls: ordinary, common-path, non-common-path, wrong-reference",
        "stable ordinary window: round8 | L=1 | w=0.16 | p=0.15",
        "confirmed structure: sparse_tracker_decoy + occupancy_guarded | round17",
    ]
    yy = y0 + 22
    for line in info:
        draw.text((x0, yy), line, font=FONT_SMALL, fill=SUB)
        yy += 18
    paste_scaled(base, best_panel, (x0 + 8, yy + 6, x1 - 8, y1 - 10))
    draw.text((x0 + 12, y1 - 24), f"confirmed: c-o {round17_summary['common_minus_ordinary_db_mean']:+.3f} dB | c-w {round17_summary['common_minus_wrongref_db_mean']:+.3f} dB", font=FONT_TINY, fill=INK)


def main() -> None:
    round8_rows = read_csv(ROUND8_SUMMARY_CSV)
    round17_summary = load_json(ROUND17_SUMMARY_JSON)
    round17_repeat = read_csv(ROUND17_REPEAT_CSV)
    risk_rows = read_csv(ROUND17_RISK_REPEAT_CSV)
    risk_summary = summarize_risk_rows(risk_rows)
    best_panel = Image.open(ROUND17_PANEL).convert("RGB")

    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    draw.text((MARGIN, MARGIN - 2), "Figure 5 | Passive Processor Comparison Under Paired Diagnostics", font=FONT_TITLE, fill=INK)
    subtitle = "Repeat-stable ordinary advantage; structurally improved exclusion with one negative tail."
    draw.text((MARGIN, MARGIN + 28), subtitle, font=FONT_SUB, fill=SUB)

    panel_boxes = [
        (MARGIN, MARGIN + HEADER_H, MARGIN + PANEL_W, MARGIN + HEADER_H + PANEL_H),
        (MARGIN + PANEL_W + GAP, MARGIN + HEADER_H, WIDTH - MARGIN, MARGIN + HEADER_H + PANEL_H),
        (MARGIN, MARGIN + HEADER_H + PANEL_H + GAP, MARGIN + PANEL_W, HEIGHT - MARGIN),
        (MARGIN + PANEL_W + GAP, MARGIN + HEADER_H + PANEL_H + GAP, WIDTH - MARGIN, HEIGHT - MARGIN),
    ]
    titles = ["a  Stable Window", "b  Paired Metrics", "c  Repeat Signs", "d  Risk Samples"]
    for box, title in zip(panel_boxes, titles):
        draw_card(draw, box, title)

    inner_boxes = [(x0 + 18, y0 + 60, x1 - 18, y1 - 18) for x0, y0, x1, y1 in panel_boxes]
    draw_protocol_panel(image, draw, best_panel, round17_summary, inner_boxes[0])
    draw_repeat_bars(draw, round8_rows, inner_boxes[1])
    draw_repeat_signs(draw, round17_repeat, round17_summary, inner_boxes[2])
    draw_risk_sample_panel(draw, risk_rows, risk_summary, inner_boxes[3])

    footer = (
        f"risk-pair positive fraction {round17_summary['risk_pair_positive_fraction']:.3f} | "
        f"risk-pair q10 {round17_summary['risk_pair_q10_db']:+.3f} dB | "
        f"risk-pair min {round17_summary['risk_pair_min_db']:+.3f} dB | "
        f"worst repeat c-w {round17_summary['common_minus_wrongref_db_min']:+.3f} dB"
    )
    draw.text((MARGIN, HEIGHT - 20), footer, font=FONT_TINY, fill=SUB)

    image.save(FIG_PNG)
    image.save(FIG_PDF, "PDF", resolution=200.0)

    summary_lines = [
        "# Figure 5 Paired-Diagnostic Panel",
        "",
        "- panel a: protocol and preview strip tied to the round17 confirmed structural configuration",
        "- panel b: stable ordinary-baseline window metrics",
        "- panel c: round17 repeat-level sign structure and paired diagnostics",
        "- panel d: frame and two_spots risk-sample breakdown with one remaining negative tail event",
        f"- output png: {FIG_PNG}",
        f"- output pdf: {FIG_PDF}",
    ]
    FIG_SUMMARY_MD.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
