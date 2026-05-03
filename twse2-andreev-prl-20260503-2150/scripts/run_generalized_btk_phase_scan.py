from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "configs" / "default_params.json"
BTK_CONFIG = ROOT / "configs" / "generalized_btk_phase_scan.json"
RESULTS = ROOT / "results" / "generalized_btk_phase_scan"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.twse2_minimal import (  # noqa: E402
    ModelParams,
)


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def mean_background(curve: np.ndarray) -> float:
    side = min(15, max(1, len(curve) // 10))
    return float(np.mean(np.r_[curve[:side], curve[-side:]]))


def reflected_theta(theta_values: np.ndarray, alpha: float) -> np.ndarray:
    return 2.0 * alpha - theta_values + np.pi


def field_response(candidate: str, field_strength: float, phi: float) -> float:
    if field_strength <= 0.0:
        return 1.0
    base = max(0.15, 1.0 - 0.35 * field_strength**2)
    if candidate == "s_wave":
        anisotropy = 1.0
    elif candidate == "s_pm":
        anisotropy = 1.0 + 0.18 * field_strength * np.cos(2.0 * phi)
    elif candidate == "chiral":
        anisotropy = 1.0 + 0.12 * field_strength * np.sin(2.0 * phi)
    else:
        raise ValueError(f"unknown candidate: {candidate}")
    return max(0.1, base * anisotropy)


def candidate_gap_vectorized(candidate: str, theta_values: np.ndarray, delta_sc: float) -> tuple[np.ndarray, np.ndarray]:
    if candidate == "s_wave":
        positive = np.full_like(theta_values, delta_sc, dtype=complex)
        negative = np.full_like(theta_values, delta_sc, dtype=complex)
        return positive, negative
    if candidate == "s_pm":
        positive = np.full_like(theta_values, delta_sc, dtype=complex)
        negative = np.full_like(theta_values, -delta_sc, dtype=complex)
        return positive, negative
    if candidate == "chiral":
        phase = np.exp(2j * theta_values)
        return delta_sc * phase, delta_sc * phase
    raise ValueError(f"unknown candidate: {candidate}")


def interface_orientation_envelope(
    candidate: str,
    theta_values: np.ndarray,
    alpha: float,
    eta: float,
    phi: float,
    field_strength: float,
) -> np.ndarray:
    rel = theta_values - alpha
    if candidate == "s_wave":
        return np.ones_like(theta_values, dtype=float)
    if candidate == "s_pm":
        return 1.0 + 0.35 * eta * np.cos(2.0 * (alpha - phi)) + 0.15 * field_strength * np.cos(rel)
    if candidate == "chiral":
        return 1.0 + 0.55 * np.cos(2.0 * rel) + 0.12 * field_strength * np.sin(2.0 * (alpha - phi))
    raise ValueError(f"unknown candidate: {candidate}")


def generalized_btk_curve(
    bias_values: np.ndarray,
    theta_values: np.ndarray,
    weights: np.ndarray,
    candidate: str,
    alpha: float,
    barrier_z: float,
    eta: float,
    params: ModelParams,
    phi: float,
    field_strength: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    theta_r = reflected_theta(theta_values, alpha)
    scale = field_response(candidate, field_strength=field_strength, phi=phi)
    d_in_pos, d_in_neg = candidate_gap_vectorized(candidate, theta_values, params.delta_sc * scale)
    d_same_pos, d_same_neg = candidate_gap_vectorized(candidate, theta_r, params.delta_sc * scale)
    d_mix_pos, d_mix_neg = d_same_neg, d_same_pos

    same_avg = 0.5 * (d_in_pos * np.conj(d_same_pos) + d_in_neg * np.conj(d_same_neg))
    mixed_avg = 0.5 * (d_in_pos * np.conj(d_mix_pos) + d_in_neg * np.conj(d_mix_neg))
    phase_projection = (1.0 - eta) * same_avg + eta * mixed_avg

    gap_scale = abs(scale * params.delta_sc)
    phase_alignment = np.real(phase_projection) / (gap_scale * gap_scale + 1e-12)
    frustration = 0.5 * (1.0 - np.clip(phase_alignment, -1.0, 1.0))
    transparency = 1.0 / (1.0 + barrier_z**2)
    envelope = np.clip(
        interface_orientation_envelope(
            candidate=candidate,
            theta_values=theta_values,
            alpha=alpha,
            eta=eta,
            phi=phi,
            field_strength=field_strength,
        ),
        0.15,
        None,
    )

    bias2 = bias_values[:, None] ** 2
    denom = bias2 + gap_scale * gap_scale + params.gamma * params.gamma
    andreev = transparency * (gap_scale * gap_scale / denom) * (1.0 + 1.35 * frustration[None, :]) * envelope[None, :]
    normal_reflection = (1.0 - transparency) + transparency * (bias2 / denom) * (
        1.0 - 0.45 * frustration[None, :]
    ) / envelope[None, :]
    normal_reflection = np.clip(normal_reflection, 0.0, 1.6)
    conductance = 1.0 + andreev - normal_reflection

    norm = max(float(np.sum(weights)), 1e-12)
    weighted_conductance = np.sum(conductance * weights[None, :], axis=1) / norm
    weighted_andreev = np.sum(andreev * weights[None, :], axis=1) / norm
    weighted_normal = np.sum(normal_reflection * weights[None, :], axis=1) / norm
    frustration_curve = np.full_like(weighted_conductance, np.sum(frustration * weights) / norm)
    return weighted_conductance, weighted_andreev, weighted_normal, frustration_curve


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    params = ModelParams.from_json(DEFAULT_CONFIG)
    btk = json.loads(BTK_CONFIG.read_text())

    pairings = [str(item) for item in btk["pairings"]]
    barrier_values = [float(item) for item in btk["barrier_values"]]
    eta_values = [float(item) for item in btk["eta_values"]]
    field_values = [float(item) for item in btk["field_values"]]
    phi_values = np.linspace(0.0, 2.0 * np.pi, int(btk["phi_points"]), endpoint=False)
    alpha_values = np.linspace(0.0, np.pi / 2.0, int(btk["alpha_points"]))
    theta_count = int(btk["theta_grid_points"])
    bias_values = np.linspace(float(btk["bias_min"]), float(btk["bias_max"]), int(btk["bias_points"]))
    zero_idx = int(np.argmin(np.abs(bias_values)))

    curve_rows: list[list[object]] = []
    summary_rows: list[list[object]] = []

    for pairing in pairings:
        for barrier_z in barrier_values:
            for eta in eta_values:
                for field_strength in field_values:
                    for phi in phi_values:
                        alpha_peak_contrasts = []
                        alpha_zero_bias = []
                        alpha_frustration = []
                        alpha_best_peak = []

                        for alpha in alpha_values:
                            theta_values = np.linspace(float(alpha) - np.pi / 2.0, float(alpha) + np.pi / 2.0, theta_count, endpoint=False)
                            weights = np.abs(np.cos(theta_values - float(alpha)))
                            conductance_curve, andreev_curve, normal_curve, frustration_curve = generalized_btk_curve(
                                bias_values=bias_values,
                                theta_values=theta_values,
                                weights=weights,
                                candidate=pairing,
                                alpha=float(alpha),
                                barrier_z=barrier_z,
                                eta=eta,
                                params=params,
                                phi=float(phi),
                                field_strength=field_strength,
                            )

                            for bias, conductance, andreev, normal_reflection, frustration in zip(
                                bias_values, conductance_curve, andreev_curve, normal_curve, frustration_curve
                            ):
                                curve_rows.append(
                                    [
                                        pairing,
                                        barrier_z,
                                        eta,
                                        field_strength,
                                        float(phi),
                                        float(alpha),
                                        float(bias),
                                        float(conductance),
                                        float(andreev),
                                        float(normal_reflection),
                                        float(frustration),
                                    ]
                                )

                            background = mean_background(conductance_curve)
                            peak = float(np.max(conductance_curve))
                            peak_contrast = peak - background
                            alpha_peak_contrasts.append(peak_contrast)
                            alpha_zero_bias.append(float(conductance_curve[zero_idx]))
                            alpha_frustration.append(float(np.mean(frustration_curve)))
                            alpha_best_peak.append(peak)

                        alpha_peak_contrasts = np.asarray(alpha_peak_contrasts, dtype=float)
                        alpha_zero_bias = np.asarray(alpha_zero_bias, dtype=float)
                        alpha_frustration = np.asarray(alpha_frustration, dtype=float)
                        alpha_best_peak = np.asarray(alpha_best_peak, dtype=float)

                        summary_rows.append(
                            [
                                pairing,
                                barrier_z,
                                eta,
                                field_strength,
                                float(phi),
                                float(np.mean(alpha_zero_bias)),
                                float(np.max(alpha_best_peak)),
                                float(np.mean(alpha_peak_contrasts)),
                                float(np.max(alpha_peak_contrasts) - np.min(alpha_peak_contrasts)),
                                float(np.mean(alpha_frustration)),
                                float(alpha_values[int(np.argmax(alpha_peak_contrasts))]),
                                float(alpha_values[int(np.argmin(alpha_peak_contrasts))]),
                            ]
                        )

    write_csv(
        RESULTS / "conductance_curves.csv",
        [
            "pairing",
            "barrier_Z",
            "eta",
            "field_strength",
            "phi",
            "alpha",
            "bias",
            "conductance",
            "andreev_component",
            "normal_reflection_component",
            "frustration_proxy",
        ],
        curve_rows,
    )
    write_csv(
        RESULTS / "phase_scan_summary.csv",
        [
            "pairing",
            "barrier_Z",
            "eta",
            "field_strength",
            "phi",
            "mean_zero_bias_conductance",
            "max_peak_conductance",
            "mean_peak_contrast",
            "alpha_anisotropy",
            "mean_frustration",
            "alpha_at_max_peak_contrast",
            "alpha_at_min_peak_contrast",
        ],
        summary_rows,
    )

    summary_array = np.asarray(summary_rows, dtype=object)
    s_wave_rows = summary_array[summary_array[:, 0] == "s_wave"]
    nontrivial_rows = summary_array[summary_array[:, 0] != "s_wave"]
    best_nontrivial = nontrivial_rows[np.argmax(nontrivial_rows[:, 8].astype(float))]
    best_swave = s_wave_rows[np.argmax(s_wave_rows[:, 8].astype(float))]

    summary = {
        "package_type": "generalized_btk_phase_sensitive_proxy",
        "pairings": pairings,
        "barrier_values": barrier_values,
        "eta_values": eta_values,
        "field_values": field_values,
        "phi_points": int(btk["phi_points"]),
        "alpha_points": int(btk["alpha_points"]),
        "bias_points": int(btk["bias_points"]),
        "best_nontrivial_alpha_anisotropy_case": {
            "pairing": str(best_nontrivial[0]),
            "barrier_Z": float(best_nontrivial[1]),
            "eta": float(best_nontrivial[2]),
            "field_strength": float(best_nontrivial[3]),
            "phi": float(best_nontrivial[4]),
            "alpha_anisotropy": float(best_nontrivial[8]),
            "mean_frustration": float(best_nontrivial[9]),
        },
        "best_s_wave_alpha_anisotropy_case": {
            "pairing": str(best_swave[0]),
            "barrier_Z": float(best_swave[1]),
            "eta": float(best_swave[2]),
            "field_strength": float(best_swave[3]),
            "phi": float(best_swave[4]),
            "alpha_anisotropy": float(best_swave[8]),
            "mean_frustration": float(best_swave[9]),
        },
    }
    (RESULTS / "parameters.json").write_text(json.dumps(summary, indent=2) + "\n")

    lines = [
        "# Generalized BTK Phase Scan",
        "",
        "- Data status: generated in the canonical 2026-05-03 project root",
        "- Method status: phase-sensitive generalized BTK proxy built directly on the current WP1-WP2 scaffold",
        f"- Pairings: {pairings}",
        f"- Barrier values: {barrier_values}",
        f"- Intervalley mixing values: {eta_values}",
        f"- Field strengths: {field_values}",
        f"- Phi points: {int(btk['phi_points'])}",
        f"- Alpha points: {int(btk['alpha_points'])}",
        f"- Theta grid points: {theta_count}",
        f"- Bias points: {int(btk['bias_points'])}",
        (
            "- Strongest nontrivial alpha anisotropy: "
            f"{best_nontrivial[0]} at Z={float(best_nontrivial[1]):.2f}, eta={float(best_nontrivial[2]):.2f}, "
            f"field={float(best_nontrivial[3]):.2f}, phi={float(best_nontrivial[4]):.3f} with "
            f"anisotropy={float(best_nontrivial[8]):.6f}"
        ),
        (
            "- Strongest s-wave alpha anisotropy: "
            f"{best_swave[0]} at Z={float(best_swave[1]):.2f}, eta={float(best_swave[2]):.2f}, "
            f"field={float(best_swave[3]):.2f}, phi={float(best_swave[4]):.3f} with "
            f"anisotropy={float(best_swave[8]):.6f}"
        ),
        "- Interpretation boundary: this is a phase-sensitive conductance proxy layer, not yet the final multiorbital semi-infinite BTK benchmark.",
    ]
    (RESULTS / "summary.md").write_text("\n".join(lines) + "\n")
    print((RESULTS / "summary.md").read_text())


if __name__ == "__main__":
    main()
