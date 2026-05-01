from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path("/workspace")
OUTPUT = ROOT / "output"
CSV_PATH = OUTPUT / "extdata_fig2_log_summary.csv"
XDOMAIN_CSV_PATH = OUTPUT / "cross_domain_demonstration_summary.csv"
PDF_PATH = OUTPUT / "self-calibrating-diffractive-ncomms-supplementary.pdf"


def load_rows() -> list[dict[str, str]]:
    with CSV_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def load_cross_domain_rows() -> list[dict[str, str]]:
    with XDOMAIN_CSV_PATH.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="SuppTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#17324d"),
            alignment=TA_CENTER,
            spaceAfter=10,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SuppSubtitle",
            parent=styles["Heading2"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=colors.HexColor("#4c6173"),
            alignment=TA_CENTER,
            spaceAfter=12,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SuppHeading",
            parent=styles["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=15,
            textColor=colors.HexColor("#17324d"),
            spaceBefore=8,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SuppBody",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13,
            textColor=colors.HexColor("#20252b"),
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="SuppSmall",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#465563"),
            spaceAfter=5,
        )
    )
    return styles


def draw_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#5c6770"))
    canvas.drawRightString(190 * mm, 10 * mm, f"Supplementary Information | Page {doc.page}")
    canvas.restoreState()


def make_table(rows: list[dict[str, str]], styles) -> Table:
    header = [
        Paragraph("<b>Metric</b>", styles["SuppSmall"]),
        Paragraph("<b>Condition</b>", styles["SuppSmall"]),
        Paragraph("<b>Mean value</b>", styles["SuppSmall"]),
        Paragraph("<b>Delta vs no-ref</b>", styles["SuppSmall"]),
        Paragraph("<b>Delta vs non-common</b>", styles["SuppSmall"]),
    ]
    body = []
    for row in rows:
        body.append(
            [
                Paragraph(row["metric"], styles["SuppSmall"]),
                Paragraph(row["condition"], styles["SuppSmall"]),
                Paragraph(f'{row["mean_value"]} {row["unit"]}', styles["SuppSmall"]),
                Paragraph(str(row["delta_vs_no_reference"]), styles["SuppSmall"]),
                Paragraph(str(row["delta_vs_noncommon_path"]), styles["SuppSmall"]),
            ]
        )
    table = Table([header] + body, colWidths=[55 * mm, 32 * mm, 28 * mm, 30 * mm, 32 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce8f3")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17324d")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9ba9b5")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f9fb")]),
            ]
        )
    )
    return table


def make_cross_domain_table(rows: list[dict[str, str]], styles) -> Table:
    header = [
        Paragraph("<b>Domain</b>", styles["SuppSmall"]),
        Paragraph("<b>Task metric</b>", styles["SuppSmall"]),
        Paragraph("<b>No-ref</b>", styles["SuppSmall"]),
        Paragraph("<b>Common-path</b>", styles["SuppSmall"]),
        Paragraph("<b>Delta</b>", styles["SuppSmall"]),
        Paragraph("<b>Reading</b>", styles["SuppSmall"]),
    ]
    body = []
    for row in rows:
        body.append(
            [
                Paragraph(row["domain"], styles["SuppSmall"]),
                Paragraph(row["task_metric"], styles["SuppSmall"]),
                Paragraph(str(row["no_reference"]), styles["SuppSmall"]),
                Paragraph(str(row["common_path"]), styles["SuppSmall"]),
                Paragraph(f'{row["delta_common_minus_no_reference"]} {row["unit"]}', styles["SuppSmall"]),
                Paragraph(row["interpretation"], styles["SuppSmall"]),
            ]
        )
    table = Table([header] + body, colWidths=[20 * mm, 34 * mm, 20 * mm, 24 * mm, 24 * mm, 55 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#dce8f3")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#17324d")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9ba9b5")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f9fb")]),
            ]
        )
    )
    return table


def build_story(rows: list[dict[str, str]], cross_rows: list[dict[str, str]]):
    styles = build_styles()
    story = []
    story.append(Spacer(1, 18 * mm))
    story.append(Paragraph("Supplementary Information", styles["SuppTitle"]))
    story.append(
        Paragraph(
            "Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations",
            styles["SuppSubtitle"],
        )
    )
    story.append(
        Paragraph(
            "This supplementary package is evidence-bounded. It compiles currently verified and partially verified material from the active project memory and workspace. It does not claim unverified turbulence, thin phase-screen, or experimental results.",
            styles["SuppBody"],
        )
    )
    story.append(
        Paragraph(
            "Verification basis: manuscript-v1-strict.md, project-state.md, supervision-log.md, round6/round7 local outputs, and the generated extdata_fig2_log_summary.csv in the current workspace.",
            styles["SuppSmall"],
        )
    )

    story.append(Spacer(1, 4 * mm))
    story.append(Paragraph("Supplementary Note 1 | Evidence Status", styles["SuppHeading"]))
    story.append(
        Paragraph(
            "Verified classes: Gaussian surrogate mechanism, Zernike wave-optics validation, CRLB-style pilot-information scan, local task-level bound note, and cross-task surrogate evaluation. Partially verified class: passive processor comparison under the shared ordinary-D2NN versus pilot-assisted-D2NN protocol. Unverified classes remain outside the scope of this supplement and are kept out of the central claim.",
            styles["SuppBody"],
        )
    )
    story.append(
        Paragraph(
            "Current project bottleneck: Figure 5 now supports a repeat-stable ordinary-versus-common-path advantage window, but the stricter exclusion claim against wrong-reference controls is still not stable enough to carry the manuscript's central promise.",
            styles["SuppBody"],
        )
    )

    story.append(Paragraph("Supplementary Table S1 | Extended Data Figure 2 log summary", styles["SuppHeading"]))
    story.append(
        Paragraph(
            "The active workspace does not currently contain the original round2 raw per-sample logs. The table below is therefore a verified summary table reconstructed from manuscript-bounded values already written into the project memory. It should be treated as a summary log, not as the underlying raw record.",
            styles["SuppBody"],
        )
    )
    story.append(make_table(rows, styles))
    story.append(
        Paragraph(
            "Interpretation: common-path improves OOD reconstruction PSNR by 1.353 dB over no-reference and 1.344 dB over non-common-path in the Zernike wave-optics protocol, while also reducing mean PSF mismatch relative to both controls.",
            styles["SuppSmall"],
        )
    )

    story.append(PageBreak())
    story.append(Paragraph("Supplementary Note 2 | Neural-operator formalism", styles["SuppHeading"]))
    story.append(
        Paragraph(
            "To make the self-calibration claim precise, the manuscript now treats the measurement as a state-indexed operator equation rather than one fixed image-to-image map. Let x belong to an object function space, let theta denote the latent degradation state, and let r be a known pilot field. The common-path observation is written as y = M(A_theta(x, r)), where A_theta is the state-indexed optical propagation operator and M is intensity readout. A downstream recovery or inference block is then a task operator G_phi mapping the measurement space into one task-dependent output space.",
            styles["SuppBody"],
        )
    )
    story.append(
        Paragraph(
            "The local theory statement is bounded. Around a nominal operating point, the current note linearizes both the observation operator and the downstream task map, then propagates pilot-induced covariance reduction through the task Jacobian. This supports a local task-level error-floor comparison, not a proof of global invertibility or universal blind recovery.",
            styles["SuppBody"],
        )
    )

    story.append(Paragraph("Supplementary Note 3 | Cross-domain demonstration", styles["SuppHeading"]))
    story.append(
        Paragraph(
            "The current Figure 4 evidence is best interpreted as a cross-domain demonstration of one mechanism across multiple output spaces sharing the same latent degradation family. Reconstruction, classification residual, and inverse-design surrogate do not ask for the same output, so their gains need not be equal even when the same pilot observation is used.",
            styles["SuppBody"],
        )
    )
    story.append(make_cross_domain_table(cross_rows, styles))
    story.append(
        Paragraph(
            "Current interpretation: reconstruction benefits most because it preserves fine field information, classification residual benefits modestly because the downstream statistic compresses the observation, and inverse-design remains nearly neutral because the present target is only weakly aligned with the pilot-revealed state directions.",
            styles["SuppBody"],
        )
    )

    story.append(Paragraph("Supplementary Note 4 | Processor-level boundary", styles["SuppHeading"]))
    story.append(
        Paragraph(
            "The first two-layer pure-reconstruction D2NN comparison remained neutral-to-negative, with common-path 0.191 dB below the ordinary D2NN. A later three-layer self-calibrating phase-only prototype yielded a weak positive object-zone OOD signal: common-path 11.559 dB, ordinary 11.356 dB, non-common-path 11.505 dB, and wrong-reference 11.350 dB. Round 8 then performed a 60-point local processor scan with four repeats per point and identified a repeat-stable ordinary-focused window at num_layers = 1, reference_weight = 0.16, and phase_mix = 0.15. In that window, common-path exceeded the ordinary baseline by 0.438 dB on average, with a positive worst-repeat margin of 0.390 dB. This establishes a real local processor-level advantage over the ordinary baseline and provides the fixed ordinary-positive anchor used by later structural confirmation rounds.",
            styles["SuppBody"],
        )
    )
    story.append(
        Paragraph(
            "Rounds 9 through 13 showed that stronger wrong-reference tests are better interpreted through paired diagnostics than through one mean PSNR gap, and they localized the hardest failures to frame and two_spots. Round 16 then replaced continuous micro-tuning with structural wrong-reference and encoding redesigns, and the best structure sparse_tracker_decoy plus occupancy_guarded first pushed the risk-pair lower decile above zero. Round 17 performed the higher-repeat confirmation of that same fixed structure. Under 14 repeats, the common-minus-ordinary mean is +0.638 dB with a +0.413 dB worst repeat, the common-minus-wrong-reference mean is +0.278 dB with a +0.047 dB worst repeat, the paired risk-sample lower decile is +0.090 dB, and the positive fraction is 0.964. The correct reading is therefore: ordinary-baseline advantage is locally repeat-stable, and structural redesign makes the paired exclusion diagnostic mostly positive under higher-repeat confirmation, but one risk-pair minimum remains slightly negative at -0.025 dB, so exclusion is still not fully closed.",
            styles["SuppBody"],
        )
    )

    story.append(Paragraph("Supplementary Note 5 | Reproducibility and archive status", styles["SuppHeading"]))
    story.append(
        Paragraph(
            "The active workspace currently contains reproducible round6 through round17 processor scripts and outputs, together with the current manuscript draft, review draft, reference ledger, neural-operator formalism note, and the cross-domain summary table. The project also maintains an automatically refreshed Drive-sync manifest, but actual Google Drive upload remains blocked by the lack of a writable upload endpoint in the current connector workflow.",
            styles["SuppBody"],
        )
    )
    story.append(
        Paragraph(
            "Known missing historical assets in the active workspace include the legacy round5 and round5b scripts and several associated processor-level outputs. They are still referenced in the project memory, but they are not presented here as if fully restored. The structurally redesigned wrong-reference families introduced in round16 are now partly evidence-bearing because sparse_tracker_decoy plus occupancy_guarded has been rerun and confirmed in round17, whereas the unused alternative designs should still be treated as comparative design objects rather than generalized evidence.",
            styles["SuppBody"],
        )
    )

    story.append(Paragraph("Supplementary Methods Snapshot", styles["SuppHeading"]))
    story.append(
        Paragraph(
            "Forward-model ladder used in this project: (i) Gaussian shared-blur surrogate for mechanism isolation; (ii) Zernike pupil wave-optics model for physically grounded dynamic-aberration validation; (iii) pilot-information and local task-level analyses; (iv) cross-domain surrogate evaluation across reconstruction, classification, and inverse-design outputs; and (v) passive phase-only D2NN processor comparisons. Current heavy dependencies such as torch, scipy, and matplotlib are unavailable in the network-restricted active environment, so the working reproducible chain is limited to numpy + Pillow for the present rebuild stage.",
            styles["SuppBody"],
        )
    )

    story.append(Paragraph("Supplementary Caption Guidance", styles["SuppHeading"]))
    story.append(
        Paragraph(
            "Extended Data Figure 2 should be captioned as a wave-optics summary figure, not as a raw-log dump. The current CSV is suitable as a compact summary table for downstream figure assembly, manuscript bookkeeping, or later reinsertion into a fully reconstructed round2 archive.",
            styles["SuppBody"],
        )
    )
    story.append(Paragraph("Supplementary Figure 5 caption guidance", styles["SuppHeading"]))
    story.append(
        Paragraph(
            "Figure 5 should now be captioned as a processor comparison with a repeat-stable ordinary-baseline advantage and structurally improved paired wrong-reference exclusion under higher-repeat confirmation. The caption should avoid claiming that self-calibration has been cleanly isolated at the processor level. Instead it should state that the present lightweight passive protocol supports a local common-path advantage over the ordinary baseline, that the round17 confirmed sparse_tracker_decoy plus occupancy_guarded structure yields a positive paired lower decile and a 0.964 positive fraction, and that one slight negative risk-pair tail at -0.025 dB still prevents a fully closed exclusion claim.",
            styles["SuppBody"],
        )
    )
    return story


def main() -> None:
    rows = load_rows()
    cross_rows = load_cross_domain_rows()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        title="Supplementary Information - self-calibrating-diffractive-ncomms",
        author="OpenAI Codex",
    )
    story = build_story(rows, cross_rows)
    doc.build(story, onFirstPage=draw_page_number, onLaterPages=draw_page_number)


if __name__ == "__main__":
    main()
