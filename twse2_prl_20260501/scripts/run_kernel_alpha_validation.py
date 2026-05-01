from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
LEGACY_KERNEL = Path(
    "/workspace/memory/twse2-andreev-prl-2026-04-29T13-43-41Z/code/wp3_alpha_z_phi_btk.py"
)


def load_legacy_kernel():
    spec = importlib.util.spec_from_file_location("legacy_wp3_alpha_z_phi_btk", LEGACY_KERNEL)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load legacy kernel from {LEGACY_KERNEL}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def extract_curve_features(biases: np.ndarray, conductance: np.ndarray) -> dict[str, float]:
    background = float(np.mean(np.r_[conductance[:25], conductance[-25:]]))
    zero_idx = int(np.argmin(np.abs(biases)))
    pos_mask = biases > 0.0
    neg_mask = biases < 0.0
    pos_curve = conductance[pos_mask]
    neg_curve = conductance[neg_mask]
    pos_biases = biases[pos_mask]
    neg_biases = biases[neg_mask]
    pos_peak_idx = int(np.argmax(pos_curve))
    neg_peak_idx = int(np.argmax(neg_curve))
    peak_idx = int(np.argmax(conductance))
    return {
        "zero_bias_conductance": float(conductance[zero_idx]),
        "peak_conductance": float(conductance[peak_idx]),
        "peak_bias": float(biases[peak_idx]),
        "background_conductance": background,
        "peak_minus_background": float(conductance[peak_idx] - background),
        "pos_peak_bias": float(pos_biases[pos_peak_idx]),
        "neg_peak_bias": float(neg_biases[neg_peak_idx]),
        "peak_split": float(pos_biases[pos_peak_idx] - neg_biases[neg_peak_idx]),
    }


def build_curve(
    module,
    params,
    candidate: str,
    eta: float,
    alpha: float,
    phi: float,
    barrier: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    theta = np.linspace(-np.pi / 2.0, np.pi / 2.0, params.theta_points)
    biases = np.linspace(params.bias_min, params.bias_max, params.bias_points)
    weights = module.orientation_weight(theta, alpha, candidate)
    weight_sum = float(np.sum(weights))
    conductance = np.zeros_like(biases)
    mean_frustration = np.zeros_like(biases)
    for idx, bias in enumerate(biases):
        local_c, _, _, local_f = module.local_btk_terms(
            bias=bias,
            theta=theta,
            alpha=alpha,
            phi=phi,
            eta=eta,
            barrier=barrier,
            candidate=candidate,
            params=params,
        )
        conductance[idx] = float(np.sum(local_c * weights) / weight_sum)
        mean_frustration[idx] = float(np.sum(local_f * weights) / weight_sum)
    return biases, conductance, mean_frustration


def choose_validation_slice(module, params, alpha_values: np.ndarray) -> dict[str, float]:
    best: dict[str, float] | None = None
    for eta in params.eta_values:
        for phi in params.phi_values:
            for barrier in params.barrier_values:
                chiral_splits = []
                peak_strengths = []
                for alpha in alpha_values:
                    biases, conductance, _ = build_curve(
                        module, params, "chiral", float(eta), float(alpha), float(phi), float(barrier)
                    )
                    features = extract_curve_features(biases, conductance)
                    chiral_splits.append(features["peak_split"])
                    peak_strengths.append(features["peak_minus_background"])
                alpha_split_coupling = float(max(chiral_splits) - min(chiral_splits))
                mean_peak_strength = float(np.mean(peak_strengths))
                score = alpha_split_coupling + 0.15 * mean_peak_strength
                if best is None or score > best["score"]:
                    best = {
                        "eta": float(eta),
                        "phi": float(phi),
                        "barrier_Z": float(barrier),
                        "score": score,
                        "alpha_split_coupling": alpha_split_coupling,
                        "mean_peak_strength": mean_peak_strength,
                    }
    if best is None:
        raise RuntimeError("Failed to choose validation slice")
    return best


def interpolate_shifted_curve(
    biases: np.ndarray,
    conductance: np.ndarray,
    background: float,
    peak_conductance: float,
    peak_bias: float,
    x_grid: np.ndarray,
) -> np.ndarray:
    amp = max(peak_conductance - background, 1e-9)
    normalized = (conductance - background) / amp
    shifted_x = biases - peak_bias
    return np.interp(x_grid, shifted_x, normalized, left=np.nan, right=np.nan)


def compute_branch_metrics(curves: list[dict[str, object]]) -> tuple[list[list[object]], dict[str, float], np.ndarray, np.ndarray]:
    x_grid = np.linspace(-0.12, 0.12, 241)
    shifted_curves = []
    metrics_rows: list[list[object]] = []
    for curve in curves:
        shifted = interpolate_shifted_curve(
            biases=np.asarray(curve["biases"]),
            conductance=np.asarray(curve["conductance"]),
            background=float(curve["background_conductance"]),
            peak_conductance=float(curve["peak_conductance"]),
            peak_bias=float(curve["peak_bias"]),
            x_grid=x_grid,
        )
        shifted_curves.append(shifted)
    shifted_stack = np.vstack(shifted_curves)
    master = np.nanmean(shifted_stack, axis=0)
    collapse_rms = []
    for curve, shifted in zip(curves, shifted_stack):
        diff = shifted - master
        rms = float(np.sqrt(np.nanmean(diff * diff)))
        collapse_rms.append(rms)
        metrics_rows.append(
            [
                curve["candidate"],
                curve["alpha"],
                curve["eta"],
                curve["phi"],
                curve["barrier_Z"],
                curve["zero_bias_conductance"],
                curve["peak_conductance"],
                curve["peak_bias"],
                curve["peak_split"],
                curve["background_conductance"],
                curve["peak_minus_background"],
                curve["mean_frustration"],
                rms,
            ]
        )
    summary = {
        "collapse_rms_mean": float(np.mean(collapse_rms)),
        "collapse_rms_max": float(np.max(collapse_rms)),
    }
    return metrics_rows, summary, x_grid, master


def svg_polyline(points: list[tuple[float, float]], color: str, width: float, opacity: float = 1.0) -> str:
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return (
        f'<polyline fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-opacity="{opacity}" points="{pts}" />'
    )


def map_points(xs: np.ndarray, ys: np.ndarray, box: tuple[float, float, float, float], xlim: tuple[float, float], ylim: tuple[float, float]) -> list[tuple[float, float]]:
    x0, y0, w, h = box
    xmin, xmax = xlim
    ymin, ymax = ylim
    points = []
    for x, y in zip(xs, ys):
        px = x0 + (x - xmin) / (xmax - xmin) * w
        py = y0 + h - (y - ymin) / (ymax - ymin) * h
        points.append((px, py))
    return points


def build_svg(
    path: Path,
    raw_curves: dict[str, list[dict[str, object]]],
    collapse_data: dict[str, dict[str, object]],
    summary_rows: list[dict[str, object]],
) -> None:
    width, height = 1180, 860
    margin_x = 80
    margin_y = 70
    panel_w = 470
    panel_h = 300
    gap_x = 85
    gap_y = 85
    colors = {
        "0.000": "#1b9e77",
        "0.196": "#d95f02",
        "0.393": "#7570b3",
        "0.589": "#e7298a",
        "0.785": "#66a61e",
        "0.982": "#e6ab02",
        "1.178": "#a6761d",
        "1.374": "#1f78b4",
        "1.571": "#b2df8a",
    }

    def color_for_alpha(alpha: float) -> str:
        return colors.get(f"{alpha:.3f}", "#444444")

    panels = {
        "A": (margin_x, margin_y, panel_w, panel_h),
        "B": (margin_x + panel_w + gap_x, margin_y, panel_w, panel_h),
        "C": (margin_x, margin_y + panel_h + gap_y, panel_w, panel_h),
        "D": (margin_x + panel_w + gap_x, margin_y + panel_h + gap_y, panel_w, panel_h),
    }

    elements = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white" />',
        '<style>text { font-family: Helvetica, Arial, sans-serif; fill: #111; } .small { font-size: 18px; } .axis { font-size: 16px; } .title { font-size: 24px; font-weight: 700; } .panel { font-size: 22px; font-weight: 700; }</style>',
        '<text x="80" y="34" class="title">Kernel–α validation figure (fixed Z, φ, η)</text>',
    ]

    # Panel A and B raw traces
    for panel_key, candidate, title in (
        ("A", "chiral", "Phase-sensitive kernel"),
        ("B", "control_double_peak", "Phase-blind control kernel"),
    ):
        box = panels[panel_key]
        x0, y0, w, h = box
        elements.append(f'<text x="{x0}" y="{y0-18}" class="panel">{panel_key}</text>')
        elements.append(f'<text x="{x0+28}" y="{y0-18}" class="small">{title}</text>')
        elements.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#333" stroke-width="1.2" />')
        xlim = (-0.20, 0.20)
        ylim = (0.4, 3.4)
        # axes
        zero_line = map_points(np.array([-0.20, 0.20]), np.array([1.0, 1.0]), box, xlim, ylim)
        elements.append(svg_polyline(zero_line, "#cccccc", 1.0))
        for curve in raw_curves[candidate]:
            mask = (curve["biases"] >= -0.20) & (curve["biases"] <= 0.20)
            xs = curve["biases"][mask]
            ys = curve["conductance"][mask]
            points = map_points(xs, ys, box, xlim, ylim)
            elements.append(svg_polyline(points, color_for_alpha(float(curve["alpha"])), 2.0, 0.95))
        elements.append(f'<text x="{x0 + w/2 - 40}" y="{y0 + h + 28}" class="axis">bias V</text>')
        elements.append(f'<text x="{x0 - 52}" y="{y0 + h/2}" class="axis" transform="rotate(-90 {x0 - 52},{y0 + h/2})">conductance</text>')

    # Panel C collapse comparison
    box = panels["C"]
    x0, y0, w, h = box
    elements.append(f'<text x="{x0}" y="{y0-18}" class="panel">C</text>')
    elements.append(f'<text x="{x0+28}" y="{y0-18}" class="small">Collapse after peak recentering and amplitude normalization</text>')
    elements.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#333" stroke-width="1.2" />')
    xlim = (-0.10, 0.10)
    ylim = (-0.05, 1.15)
    for branch, branch_color in (("chiral", "#c23b22"), ("control_double_peak", "#1f78b4")):
        for shifted in collapse_data[branch]["shifted_curves"]:
            points = map_points(collapse_data[branch]["x_grid"], shifted, box, xlim, ylim)
            elements.append(svg_polyline(points, branch_color, 1.5, 0.30))
        master = collapse_data[branch]["master_curve"]
        points = map_points(collapse_data[branch]["x_grid"], master, box, xlim, ylim)
        elements.append(svg_polyline(points, branch_color, 4.0, 1.0))
    elements.append(f'<text x="{x0 + 24}" y="{y0 + 30}" class="small" fill="#c23b22">red: phase-sensitive</text>')
    elements.append(f'<text x="{x0 + 24}" y="{y0 + 56}" class="small" fill="#1f78b4">blue: control</text>')
    elements.append(f'<text x="{x0 + w/2 - 95}" y="{y0 + h + 28}" class="axis">V - V_peak (recentered)</text>')
    elements.append(f'<text x="{x0 - 52}" y="{y0 + h/2}" class="axis" transform="rotate(-90 {x0 - 52},{y0 + h/2})">normalized excess</text>')

    # Panel D alpha locking metrics
    box = panels["D"]
    x0, y0, w, h = box
    elements.append(f'<text x="{x0}" y="{y0-18}" class="panel">D</text>')
    elements.append(f'<text x="{x0+28}" y="{y0-18}" class="small">α-locking and collapse metrics</text>')
    elements.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="#333" stroke-width="1.2" />')
    xlim = (0.0, math.pi / 2.0)
    ylim = (0.0, 0.20)
    for branch, color in (("chiral", "#c23b22"), ("control_double_peak", "#1f78b4")):
        rows = raw_curves[branch]
        xs = np.array([float(row["alpha"]) for row in rows])
        ys = np.array([float(row["peak_split"]) for row in rows])
        order = np.argsort(xs)
        points = map_points(xs[order], ys[order], box, xlim, ylim)
        elements.append(svg_polyline(points, color, 3.0, 0.95))
        for px, py in points:
            elements.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{color}" />')
    chiral_summary = next(row for row in summary_rows if row["candidate"] == "chiral")
    control_summary = next(row for row in summary_rows if row["candidate"] == "control_double_peak")
    elements.append(f'<text x="{x0 + 24}" y="{y0 + 34}" class="small">mean collapse RMS, chiral = {chiral_summary["collapse_rms_mean"]:.3f}</text>')
    elements.append(f'<text x="{x0 + 24}" y="{y0 + 60}" class="small">mean collapse RMS, control = {control_summary["collapse_rms_mean"]:.3f}</text>')
    elements.append(f'<text x="{x0 + w/2 - 35}" y="{y0 + h + 28}" class="axis">alpha</text>')
    elements.append(f'<text x="{x0 - 52}" y="{y0 + h/2}" class="axis" transform="rotate(-90 {x0 - 52},{y0 + h/2})">peak split</text>')

    elements.append("</svg>")
    path.write_text("\n".join(elements), encoding="utf-8")


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    module = load_legacy_kernel()
    params = module.WP3Params()

    alpha_values = np.linspace(0.0, np.pi / 2.0, 9)
    fixed = choose_validation_slice(module, params, alpha_values)

    raw_curves: dict[str, list[dict[str, object]]] = {"chiral": [], "control_double_peak": []}
    curve_rows: list[list[object]] = []

    for candidate in ("chiral", "control_double_peak"):
        for alpha in alpha_values:
            biases, conductance, mean_f = build_curve(
                module,
                params,
                candidate,
                float(fixed["eta"]),
                float(alpha),
                float(fixed["phi"]),
                float(fixed["barrier_Z"]),
            )
            features = extract_curve_features(biases, conductance)
            record = {
                "candidate": candidate,
                "eta": float(fixed["eta"]),
                "phi": float(fixed["phi"]),
                "barrier_Z": float(fixed["barrier_Z"]),
                "alpha": float(alpha),
                "biases": biases,
                "conductance": conductance,
                "mean_frustration_curve": mean_f,
                **features,
                "mean_frustration": float(np.mean(mean_f)),
            }
            raw_curves[candidate].append(record)
            for bias, cond, fru in zip(biases, conductance, mean_f):
                curve_rows.append(
                    [
                        candidate,
                        float(fixed["eta"]),
                        float(fixed["phi"]),
                        float(fixed["barrier_Z"]),
                        float(alpha),
                        float(bias),
                        float(cond),
                        float(fru),
                    ]
                )

    write_csv(
        RESULTS / "kernel_alpha_validation_curves.csv",
        ["candidate", "eta", "phi", "barrier_Z", "alpha", "bias", "conductance", "mean_frustration"],
        curve_rows,
    )

    metrics_rows: list[list[object]] = []
    summary_rows: list[dict[str, object]] = []
    collapse_data: dict[str, dict[str, object]] = {}
    for candidate in ("chiral", "control_double_peak"):
        branch_metrics_rows, summary, x_grid, master = compute_branch_metrics(raw_curves[candidate])
        metrics_rows.extend(branch_metrics_rows)
        alpha_splits = [float(row["peak_split"]) for row in raw_curves[candidate]]
        summary_row = {
            "candidate": candidate,
            "eta": float(fixed["eta"]),
            "phi": float(fixed["phi"]),
            "barrier_Z": float(fixed["barrier_Z"]),
            "alpha_split_coupling": float(max(alpha_splits) - min(alpha_splits)),
            **summary,
        }
        summary_rows.append(summary_row)
        shifted_curves = []
        for record in raw_curves[candidate]:
            shifted_curves.append(
                interpolate_shifted_curve(
                    np.asarray(record["biases"]),
                    np.asarray(record["conductance"]),
                    float(record["background_conductance"]),
                    float(record["peak_conductance"]),
                    float(record["peak_bias"]),
                    x_grid,
                )
            )
        collapse_data[candidate] = {
            "x_grid": x_grid,
            "master_curve": master,
            "shifted_curves": shifted_curves,
        }

    write_csv(
        RESULTS / "kernel_alpha_validation_metrics.csv",
        [
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
        metrics_rows,
    )
    write_csv(
        RESULTS / "kernel_alpha_validation_collapse_summary.csv",
        [
            "candidate",
            "eta",
            "phi",
            "barrier_Z",
            "alpha_split_coupling",
            "collapse_rms_mean",
            "collapse_rms_max",
        ],
        [
            [
                row["candidate"],
                row["eta"],
                row["phi"],
                row["barrier_Z"],
                row["alpha_split_coupling"],
                row["collapse_rms_mean"],
                row["collapse_rms_max"],
            ]
            for row in summary_rows
        ],
    )

    build_svg(
        RESULTS / "kernel_alpha_validation_figure.svg",
        raw_curves=raw_curves,
        collapse_data=collapse_data,
        summary_rows=summary_rows,
    )

    summary_lines = [
        "# Kernel-alpha validation summary",
        "",
        "## Fixed slice",
        f"- eta = {fixed['eta']:.2f}",
        f"- phi = {fixed['phi']:.3f}",
        f"- barrier Z = {fixed['barrier_Z']:.2f}",
        f"- chiral alpha-coupling score used for selection = {fixed['score']:.4f}",
        "",
        "## Branch comparison",
    ]
    for row in summary_rows:
        summary_lines.append(
            f"- {row['candidate']}: alpha-split coupling = {row['alpha_split_coupling']:.4f}, "
            f"mean collapse RMS = {row['collapse_rms_mean']:.4f}, max collapse RMS = {row['collapse_rms_max']:.4f}"
        )
    summary_lines.extend(
        [
            "",
            "## Interpretation",
            "- The control branch should be judged successful only if it remains nearly alpha-collapsed after common recentering and normalization.",
            "- The phase-sensitive branch should be judged successful only if it retains a measurable alpha-locked residual together with nonzero alpha-coupled peak splitting.",
            "",
            "## Files",
            "- `kernel_alpha_validation_curves.csv`",
            "- `kernel_alpha_validation_metrics.csv`",
            "- `kernel_alpha_validation_collapse_summary.csv`",
            "- `kernel_alpha_validation_figure.svg`",
        ]
    )
    (RESULTS / "kernel_alpha_validation_summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print((RESULTS / "kernel_alpha_validation_summary.md").read_text())


if __name__ == "__main__":
    main()
