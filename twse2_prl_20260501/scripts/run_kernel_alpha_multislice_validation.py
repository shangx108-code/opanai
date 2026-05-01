from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np

import run_kernel_alpha_validation as kav


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def choose_multislices(module, params, alpha_values: np.ndarray, fixed_eta: float, num_slices: int = 4) -> list[dict[str, float]]:
    scored: list[dict[str, float]] = []
    for phi in params.phi_values:
        for barrier in params.barrier_values:
            chiral_splits = []
            peak_strengths = []
            for alpha in alpha_values:
                biases, conductance, _ = kav.build_curve(
                    module, params, "chiral", fixed_eta, float(alpha), float(phi), float(barrier)
                )
                features = kav.extract_curve_features(biases, conductance)
                chiral_splits.append(features["peak_split"])
                peak_strengths.append(features["peak_minus_background"])
            alpha_split_coupling = float(max(chiral_splits) - min(chiral_splits))
            mean_peak_strength = float(np.mean(peak_strengths))
            score = alpha_split_coupling + 0.15 * mean_peak_strength
            scored.append(
                {
                    "eta": fixed_eta,
                    "phi": float(phi),
                    "barrier_Z": float(barrier),
                    "score": score,
                    "alpha_split_coupling": alpha_split_coupling,
                    "mean_peak_strength": mean_peak_strength,
                }
            )
    scored.sort(key=lambda row: row["score"], reverse=True)
    selected: list[dict[str, float]] = []
    used_barriers: set[float] = set()
    used_phis: set[float] = set()
    for row in scored:
        barrier = row["barrier_Z"]
        phi = row["phi"]
        # Encourage variation in both Z and phi before filling remaining slots.
        if len(selected) < num_slices:
            if barrier not in used_barriers or phi not in used_phis or len(selected) < 2:
                selected.append(row)
                used_barriers.add(barrier)
                used_phis.add(phi)
        if len(selected) >= num_slices:
            break
    if len(selected) < num_slices:
        for row in scored:
            if row in selected:
                continue
            selected.append(row)
            if len(selected) >= num_slices:
                break
    return selected[:num_slices]


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def build_svg(path: Path, slice_rows: list[dict[str, float]], branch_summary_rows: list[dict[str, float]]) -> None:
    width, height = 1100, 760
    x0, y0 = 90, 90
    panel_w, panel_h = 400, 220
    gap_x, gap_y = 120, 110
    panels = {
        "A": (x0, y0, panel_w, panel_h),
        "B": (x0 + panel_w + gap_x, y0, panel_w, panel_h),
        "C": (x0, y0 + panel_h + gap_y, panel_w, panel_h),
        "D": (x0 + panel_w + gap_x, y0 + panel_h + gap_y, panel_w, panel_h),
    }
    colors = {"chiral": "#c23b22", "control_double_peak": "#1f78b4"}

    def map_points(xs, ys, box, xlim, ylim):
        bx, by, bw, bh = box
        xmin, xmax = xlim
        ymin, ymax = ylim
        out = []
        for x, y in zip(xs, ys):
            px = bx + (x - xmin) / (xmax - xmin) * bw
            py = by + bh - (y - ymin) / (ymax - ymin) * bh
            out.append((px, py))
        return out

    def polyline(points, color, width=3.0, opacity=1.0):
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        return (
            f'<polyline fill="none" stroke="{color}" stroke-width="{width}" '
            f'stroke-opacity="{opacity}" points="{pts}" />'
        )

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white" />',
        '<style>text { font-family: Helvetica, Arial, sans-serif; fill: #111; } .small { font-size: 18px; } .axis { font-size: 16px; } .title { font-size: 24px; font-weight: 700; } .panel { font-size: 22px; font-weight: 700; }</style>',
        '<text x="90" y="38" class="title">Kernel–α multislice robustness validation</text>',
    ]

    slice_ids = np.arange(len(slice_rows))
    labels = [f"S{i+1}" for i in slice_ids]

    # Panel A: alpha split coupling across slices
    box = panels["A"]
    elements.extend([
        f'<text x="{box[0]}" y="{box[1]-18}" class="panel">A</text>',
        f'<text x="{box[0]+28}" y="{box[1]-18}" class="small">α-coupled peak splitting across slices</text>',
        f'<rect x="{box[0]}" y="{box[1]}" width="{box[2]}" height="{box[3]}" fill="none" stroke="#333" stroke-width="1.2" />',
    ])
    xlim = (-0.3, len(slice_rows) - 0.7 if len(slice_rows) > 1 else 0.7)
    ylim = (0.0, max(0.22, max(r["alpha_split_coupling"] for r in branch_summary_rows) * 1.15))
    for branch in ("chiral", "control_double_peak"):
        rows = [r for r in branch_summary_rows if r["candidate"] == branch]
        ys = np.array([r["alpha_split_coupling"] for r in rows])
        points = map_points(slice_ids, ys, box, xlim, ylim)
        elements.append(polyline(points, colors[branch], 3.0, 0.95))
        for px, py in points:
            elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{colors[branch]}" />')
    for idx, label in enumerate(labels):
        px = box[0] + (idx - xlim[0]) / (xlim[1] - xlim[0]) * box[2]
        elements.append(f'<text x="{px-10:.1f}" y="{box[1] + box[3] + 24}" class="axis">{label}</text>')
    elements.append(f'<text x="{box[0]+110}" y="{box[1]+28}" class="small" fill="{colors["chiral"]}">red: chiral</text>')
    elements.append(f'<text x="{box[0]+110}" y="{box[1]+52}" class="small" fill="{colors["control_double_peak"]}">blue: control</text>')

    # Panel B: collapse RMS mean
    box = panels["B"]
    elements.extend([
        f'<text x="{box[0]}" y="{box[1]-18}" class="panel">B</text>',
        f'<text x="{box[0]+28}" y="{box[1]-18}" class="small">Collapse RMS mean across slices</text>',
        f'<rect x="{box[0]}" y="{box[1]}" width="{box[2]}" height="{box[3]}" fill="none" stroke="#333" stroke-width="1.2" />',
    ])
    ylim = (0.0, max(0.45, max(r["collapse_rms_mean"] for r in branch_summary_rows) * 1.15))
    for branch in ("chiral", "control_double_peak"):
        rows = [r for r in branch_summary_rows if r["candidate"] == branch]
        ys = np.array([r["collapse_rms_mean"] for r in rows])
        points = map_points(slice_ids, ys, box, xlim, ylim)
        elements.append(polyline(points, colors[branch], 3.0, 0.95))
        for px, py in points:
            elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{colors[branch]}" />')
    for idx, label in enumerate(labels):
        px = box[0] + (idx - xlim[0]) / (xlim[1] - xlim[0]) * box[2]
        elements.append(f'<text x="{px-10:.1f}" y="{box[1] + box[3] + 24}" class="axis">{label}</text>')

    # Panel C: phi values per slice
    box = panels["C"]
    elements.extend([
        f'<text x="{box[0]}" y="{box[1]-18}" class="panel">C</text>',
        f'<text x="{box[0]+28}" y="{box[1]-18}" class="small">Fixed-slice parameter choices</text>',
        f'<rect x="{box[0]}" y="{box[1]}" width="{box[2]}" height="{box[3]}" fill="none" stroke="#333" stroke-width="1.2" />',
    ])
    for idx, row in enumerate(slice_rows):
        yy = box[1] + 45 + idx * 42
        elements.append(
            f'<text x="{box[0]+24}" y="{yy}" class="small">{labels[idx]}: φ={row["phi"]:.3f}, Z={row["barrier_Z"]:.1f}, η={row["eta"]:.2f}, score={row["score"]:.3f}</text>'
        )

    # Panel D: invariant verdict
    box = panels["D"]
    elements.extend([
        f'<text x="{box[0]}" y="{box[1]-18}" class="panel">D</text>',
        f'<text x="{box[0]+28}" y="{box[1]-18}" class="small">Invariant verdict</text>',
        f'<rect x="{box[0]}" y="{box[1]}" width="{box[2]}" height="{box[3]}" fill="none" stroke="#333" stroke-width="1.2" />',
    ])
    chiral_rows = [r for r in branch_summary_rows if r["candidate"] == "chiral"]
    control_rows = [r for r in branch_summary_rows if r["candidate"] == "control_double_peak"]
    chiral_good = all(r["alpha_split_coupling"] > 0.12 and r["collapse_rms_mean"] > 0.10 for r in chiral_rows)
    control_good = all(r["alpha_split_coupling"] < 1e-8 and r["collapse_rms_mean"] < 1e-6 for r in control_rows)
    verdict = "stable" if chiral_good and control_good else "mixed"
    elements.append(f'<text x="{box[0]+24}" y="{box[1]+52}" class="small">control collapse invariant: {"yes" if control_good else "no"}</text>')
    elements.append(f'<text x="{box[0]+24}" y="{box[1]+88}" class="small">phase-sensitive non-collapse invariant: {"yes" if chiral_good else "no"}</text>')
    elements.append(f'<text x="{box[0]+24}" y="{box[1]+136}" class="small">overall multislice verdict: {verdict}</text>')
    elements.append(f'<text x="{box[0]+24}" y="{box[1]+176}" class="small">criterion: control RMS≈0 and split-coupling≈0; chiral RMS>0.10 and split-coupling>0.12</text>')

    elements.append("</svg>")
    path.write_text("\n".join(elements), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    module = kav.load_legacy_kernel()
    params = module.WP3Params()
    alpha_values = np.linspace(0.0, np.pi / 2.0, 9)

    fixed_eta = 1.0
    slice_rows = choose_multislices(module, params, alpha_values, fixed_eta=fixed_eta, num_slices=4)

    all_curve_rows: list[list[object]] = []
    all_metric_rows: list[list[object]] = []
    branch_summary_rows: list[dict[str, float]] = []

    for slice_id, slice_row in enumerate(slice_rows, start=1):
        for candidate in ("chiral", "control_double_peak"):
            branch_curves: list[dict[str, object]] = []
            for alpha in alpha_values:
                biases, conductance, mean_f = kav.build_curve(
                    module,
                    params,
                    candidate,
                    float(slice_row["eta"]),
                    float(alpha),
                    float(slice_row["phi"]),
                    float(slice_row["barrier_Z"]),
                )
                features = kav.extract_curve_features(biases, conductance)
                record = {
                    "candidate": candidate,
                    "slice_id": slice_id,
                    "eta": float(slice_row["eta"]),
                    "phi": float(slice_row["phi"]),
                    "barrier_Z": float(slice_row["barrier_Z"]),
                    "alpha": float(alpha),
                    "biases": biases,
                    "conductance": conductance,
                    "mean_frustration": float(np.mean(mean_f)),
                    **features,
                }
                branch_curves.append(record)
                for bias, cond, fru in zip(biases, conductance, mean_f):
                    all_curve_rows.append(
                        [
                            slice_id,
                            candidate,
                            float(slice_row["eta"]),
                            float(slice_row["phi"]),
                            float(slice_row["barrier_Z"]),
                            float(alpha),
                            float(bias),
                            float(cond),
                            float(fru),
                        ]
                    )

            metrics_rows, summary, _, _ = kav.compute_branch_metrics(branch_curves)
            all_metric_rows.extend([[slice_id, *row] for row in metrics_rows])
            alpha_splits = [float(row["peak_split"]) for row in branch_curves]
            branch_summary_rows.append(
                {
                    "slice_id": float(slice_id),
                    "candidate": candidate,
                    "eta": float(slice_row["eta"]),
                    "phi": float(slice_row["phi"]),
                    "barrier_Z": float(slice_row["barrier_Z"]),
                    "score": float(slice_row["score"]),
                    "alpha_split_coupling": float(max(alpha_splits) - min(alpha_splits)),
                    "collapse_rms_mean": summary["collapse_rms_mean"],
                    "collapse_rms_max": summary["collapse_rms_max"],
                }
            )

    write_csv(
        RESULTS / "kernel_alpha_multislice_curves.csv",
        ["slice_id", "candidate", "eta", "phi", "barrier_Z", "alpha", "bias", "conductance", "mean_frustration"],
        all_curve_rows,
    )
    write_csv(
        RESULTS / "kernel_alpha_multislice_metrics.csv",
        [
            "slice_id",
            "candidate",
            "alpha",
            "eta",
            "phi",
            "barrier_Z",
            "zero_bias_conductance",
            "peak_conductance",
            "peak_bias",
            "peak_split",
            "background_conductance",
            "peak_minus_background",
            "mean_frustration",
            "collapse_rms",
        ],
        all_metric_rows,
    )
    write_csv(
        RESULTS / "kernel_alpha_multislice_summary.csv",
        [
            "slice_id",
            "candidate",
            "eta",
            "phi",
            "barrier_Z",
            "score",
            "alpha_split_coupling",
            "collapse_rms_mean",
            "collapse_rms_max",
        ],
        [
            [
                int(row["slice_id"]),
                row["candidate"],
                row["eta"],
                row["phi"],
                row["barrier_Z"],
                row["score"],
                row["alpha_split_coupling"],
                row["collapse_rms_mean"],
                row["collapse_rms_max"],
            ]
            for row in branch_summary_rows
        ],
    )

    build_svg(RESULTS / "kernel_alpha_multislice_validation_figure.svg", slice_rows, branch_summary_rows)

    chiral_rows = [r for r in branch_summary_rows if r["candidate"] == "chiral"]
    control_rows = [r for r in branch_summary_rows if r["candidate"] == "control_double_peak"]
    lines = [
        "# Kernel-alpha multislice validation summary",
        "",
        "## Selected fixed-(Z, phi, eta) slices",
    ]
    for idx, row in enumerate(slice_rows, start=1):
        lines.append(
            f"- S{idx}: eta={row['eta']:.2f}, phi={row['phi']:.3f}, Z={row['barrier_Z']:.1f}, score={row['score']:.4f}, alpha-split coupling={row['alpha_split_coupling']:.4f}"
        )
    lines.extend(
        [
            "",
            "## Branch invariance check",
        ]
    )
    for row in chiral_rows:
        lines.append(
            f"- S{int(row['slice_id'])} chiral: alpha-split coupling={row['alpha_split_coupling']:.4f}, mean collapse RMS={row['collapse_rms_mean']:.4f}, max collapse RMS={row['collapse_rms_max']:.4f}"
        )
    for row in control_rows:
        lines.append(
            f"- S{int(row['slice_id'])} control: alpha-split coupling={row['alpha_split_coupling']:.4f}, mean collapse RMS={row['collapse_rms_mean']:.4e}, max collapse RMS={row['collapse_rms_max']:.4e}"
        )
    chiral_good = all(r["alpha_split_coupling"] > 0.12 and r["collapse_rms_mean"] > 0.10 for r in chiral_rows)
    control_good = all(r["alpha_split_coupling"] < 1e-8 and r["collapse_rms_mean"] < 1e-6 for r in control_rows)
    lines.extend(
        [
            "",
            "## Verdict",
            f"- Control collapse invariant across tested slices: {'yes' if control_good else 'no'}",
            f"- Phase-sensitive non-collapse invariant across tested slices: {'yes' if chiral_good else 'no'}",
            "- Operational criterion: control should retain near-zero alpha-split coupling and near-zero collapse RMS, while chiral should retain nonzero alpha-split coupling together with a nonzero collapse RMS after common recentering and normalization.",
            "",
            "## Files",
            "- `kernel_alpha_multislice_curves.csv`",
            "- `kernel_alpha_multislice_metrics.csv`",
            "- `kernel_alpha_multislice_summary.csv`",
            "- `kernel_alpha_multislice_validation_figure.svg`",
        ]
    )
    (RESULTS / "kernel_alpha_multislice_validation_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print((RESULTS / "kernel_alpha_multislice_validation_summary.md").read_text())


if __name__ == "__main__":
    main()
