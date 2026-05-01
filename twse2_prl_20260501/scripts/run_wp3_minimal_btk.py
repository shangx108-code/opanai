from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "default_params.json"
RESULTS = ROOT / "results"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.twse2_minimal import ModelParams, candidate_gap, reflected_theta  # noqa: E402


@dataclass
class WP3Params:
    barrier_values: tuple[float, ...] = (0.0, 0.5, 1.0, 2.0)
    alpha_values: tuple[float, ...] = (0.0, np.pi / 6.0, np.pi / 3.0)
    eta_values: tuple[float, ...] = (0.0, 0.25, 0.5, 0.75, 1.0)
    bias_min: float = -0.24
    bias_max: float = 0.24
    bias_points: int = 241
    theta_points: int = 361
    resonance_width: float = 0.028
    split_scale: float = 0.050


def ensure_dirs() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def orientation_weight(theta: np.ndarray, alpha: float) -> np.ndarray:
    return np.abs(np.cos(theta - alpha))


def interface_mixing(alpha: float, eta: float, candidate: str) -> float:
    if candidate == "s_wave":
        return 0.10 * eta
    if candidate == "s_pm":
        return eta * (0.25 + 0.75 * np.cos(3.0 * alpha) ** 2)
    if candidate == "chiral":
        return 0.45 + 0.35 * eta
    raise ValueError(candidate)


def resonance_profile(
    bias: float,
    barrier: float,
    eta_eff: float,
    frustration: np.ndarray,
    candidate: str,
    params: WP3Params,
) -> np.ndarray:
    comp = 4.0 * (1.0 / (1.0 + barrier * barrier)) * (1.0 - 1.0 / (1.0 + barrier * barrier))
    width = params.resonance_width
    if candidate == "s_wave":
        return np.zeros_like(frustration)
    if candidate == "s_pm":
        center = 0.0
        amp = frustration * eta_eff * (0.35 + 0.85 * comp)
        return amp * width * width / ((bias - center) ** 2 + width * width)
    if candidate == "chiral":
        split = params.split_scale * (0.80 + 0.45 * comp + 0.35 * eta_eff)
        peak_plus = width * width / ((bias - split) ** 2 + width * width)
        peak_minus = width * width / ((bias + split) ** 2 + width * width)
        amp = frustration * (0.55 + 0.75 * comp)
        dip = 0.16 * width * width / (bias * bias + width * width)
        return amp * 0.5 * (peak_plus + peak_minus) - dip
    raise ValueError(candidate)


def local_conductance(
    bias: float,
    theta: np.ndarray,
    alpha: float,
    eta: float,
    barrier: float,
    candidate: str,
    model: ModelParams,
    params: WP3Params,
) -> tuple[np.ndarray, np.ndarray]:
    theta_r = reflected_theta(theta, alpha)
    eta_eff = interface_mixing(alpha, eta, candidate)

    d_in = candidate_gap(1, theta, candidate, model.delta_sc)
    d_same = candidate_gap(1, theta_r, candidate, model.delta_sc)
    d_opp = candidate_gap(-1, theta_r, candidate, model.delta_sc)
    d_mix = (1.0 - eta_eff) * d_same + eta_eff * d_opp

    denom_phase = np.abs(d_in) * np.abs(d_mix) + 1e-12
    frustration = 0.5 * (1.0 - np.real(d_in * np.conj(d_mix)) / denom_phase)
    transparency = 1.0 / (1.0 + barrier * barrier)
    gap2 = np.clip(np.abs(d_mix) ** 2, 1e-6, None)
    energy2 = bias * bias
    denom = energy2 + gap2 + model.gamma * model.gamma

    andreev = transparency * gap2 / denom * (1.0 + 1.20 * frustration)
    normal = (1.0 - transparency) * energy2 / denom + 0.10 * transparency * frustration
    leakage = (1.0 - transparency) * (0.03 + 0.18 * frustration)
    resonance = resonance_profile(bias, barrier, eta_eff, frustration, candidate, params)

    conductance = 1.0 + andreev + resonance - normal - leakage
    return conductance, frustration


def classify_signature(zero_bias: float, peak_bias: float, split: float, candidate: str) -> str:
    if candidate == "s_wave":
        return "broad zero-bias enhancement without split finite-bias peaks"
    if candidate == "s_pm":
        if abs(peak_bias) < 0.015 and zero_bias > 1.15:
            return "intervalley-activated zero-bias enhancement"
        return "weak intervalley-sensitive subgap response"
    if candidate == "chiral":
        if split > 0.06:
            return "split finite-bias peaks with suppressed zero-bias center"
        return "finite-bias-dominant subgap response"
    raise ValueError(candidate)


def main() -> None:
    ensure_dirs()
    model = ModelParams.from_json(CONFIG)
    params = WP3Params(eta_values=tuple(model.eta_values))

    theta = np.linspace(-np.pi / 2.0, np.pi / 2.0, params.theta_points)
    biases = np.linspace(params.bias_min, params.bias_max, params.bias_points)

    curve_rows: list[list[object]] = []
    metric_rows: list[list[object]] = []

    candidates = ("s_wave", "s_pm", "chiral")
    for candidate in candidates:
        for eta in params.eta_values:
            for alpha in params.alpha_values:
                weights = orientation_weight(theta, alpha)
                weight_sum = float(np.sum(weights))
                for barrier in params.barrier_values:
                    conductance_curve = np.zeros_like(biases)
                    frustration_curve = np.zeros_like(biases)
                    for idx, bias in enumerate(biases):
                        local_g, local_f = local_conductance(
                            bias=bias,
                            theta=theta,
                            alpha=alpha,
                            eta=eta,
                            barrier=barrier,
                            candidate=candidate,
                            model=model,
                            params=params,
                        )
                        conductance_curve[idx] = float(np.sum(local_g * weights) / weight_sum)
                        frustration_curve[idx] = float(np.sum(local_f * weights) / weight_sum)

                    zero_idx = int(np.argmin(np.abs(biases)))
                    background = float(np.mean(np.r_[conductance_curve[:20], conductance_curve[-20:]]))
                    peak_idx = int(np.argmax(conductance_curve))
                    pos_mask = biases > 0.0
                    neg_mask = biases < 0.0
                    pos_curve = conductance_curve[pos_mask]
                    neg_curve = conductance_curve[neg_mask]
                    pos_biases = biases[pos_mask]
                    neg_biases = biases[neg_mask]
                    pos_peak_idx = int(np.argmax(pos_curve))
                    neg_peak_idx = int(np.argmax(neg_curve))
                    pos_peak_bias = float(pos_biases[pos_peak_idx])
                    neg_peak_bias = float(neg_biases[neg_peak_idx])
                    peak_split = float(pos_peak_bias - neg_peak_bias)
                    signature = classify_signature(
                        zero_bias=float(conductance_curve[zero_idx]),
                        peak_bias=float(biases[peak_idx]),
                        split=peak_split,
                        candidate=candidate,
                    )

                    metric_rows.append(
                        [
                            candidate,
                            float(eta),
                            float(alpha),
                            float(barrier),
                            float(conductance_curve[zero_idx]),
                            float(np.max(conductance_curve)),
                            float(biases[peak_idx]),
                            background,
                            float(np.max(conductance_curve) - background),
                            float(np.mean(frustration_curve)),
                            pos_peak_bias,
                            neg_peak_bias,
                            peak_split,
                            signature,
                        ]
                    )

                    for bias, cond, fru in zip(biases[::4], conductance_curve[::4], frustration_curve[::4]):
                        curve_rows.append(
                            [
                                candidate,
                                float(eta),
                                float(alpha),
                                float(barrier),
                                float(bias),
                                float(cond),
                                float(fru),
                            ]
                        )

    write_csv(
        RESULTS / "wp3_btk_conductance_curves.csv",
        ["candidate", "eta", "alpha", "barrier_Z", "bias", "conductance", "mean_frustration"],
        curve_rows,
    )
    write_csv(
        RESULTS / "wp3_btk_metrics.csv",
        [
            "candidate",
            "eta",
            "alpha",
            "barrier_Z",
            "zero_bias_conductance",
            "peak_conductance",
            "peak_bias",
            "background_conductance",
            "peak_minus_background",
            "mean_frustration",
            "pos_peak_bias",
            "neg_peak_bias",
            "peak_split",
            "signature",
        ],
        metric_rows,
    )

    best_rows: list[dict[str, object]] = []
    for candidate in candidates:
        subset = [row for row in metric_rows if row[0] == candidate]
        best = max(subset, key=lambda row: row[8])
        best_rows.append(
            {
                "candidate": best[0],
                "eta": best[1],
                "alpha": best[2],
                "barrier_Z": best[3],
                "zero_bias_conductance": best[4],
                "peak_conductance": best[5],
                "peak_bias": best[6],
                "peak_minus_background": best[8],
                "mean_frustration": best[9],
                "peak_split": best[12],
                "signature": best[13],
            }
        )
    (RESULTS / "wp3_btk_best_cases.json").write_text(json.dumps(best_rows, indent=2))

    lines = [
        "# WP3 minimal conductance-proxy summary",
        "",
        "## Purpose",
        "- This is the first observable-level follow-up to the WP1-WP2 screening engine.",
        "- It is a minimal BTK-like conductance proxy, not yet a full self-consistent transport calculation.",
        "",
        "## Best candidate-resolved cases",
    ]
    for row in best_rows:
        lines.extend(
            [
                f"- {row['candidate']}: eta={row['eta']:.2f}, alpha={row['alpha']:.3f}, Z={row['barrier_Z']:.2f}",
                f"  zero-bias conductance={row['zero_bias_conductance']:.3f}, peak conductance={row['peak_conductance']:.3f} at bias={row['peak_bias']:.3f}, peak split={row['peak_split']:.3f}",
                f"  mean frustration={row['mean_frustration']:.3f}; signature={row['signature']}",
            ]
        )
    lines.extend(
        [
            "",
            "## Evidence boundary",
            "- The result is designed to test whether the pairing classes remain separable once converted into a conductance-like observable.",
            "- The result does not yet include a microscopic interface potential, self-consistent gap suppression, or a full PRL-grade BTK kernel.",
        ]
    )
    (RESULTS / "wp3_btk_summary.md").write_text("\n".join(lines) + "\n")

    print((RESULTS / "wp3_btk_summary.md").read_text())


if __name__ == "__main__":
    main()
