from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from twse2_persistent_pipeline import DATA_ROOT, save_csv, save_json


SGF_TRIAL_DIR = DATA_ROOT / "sgf-semi-infinite-kspace-sparse-v3-2026-04-29"
OUTPUT_DIR = DATA_ROOT / "btk-generalized-valley-resolved-semi-infinite-2026-04-29"


def periodic_distance(x: np.ndarray, center: float) -> np.ndarray:
    wrapped = (x - center + 0.5) % 1.0 - 0.5
    return np.abs(wrapped)


def valley_projector(k2_grid: np.ndarray, center: float, width: float) -> np.ndarray:
    distance = periodic_distance(k2_grid, center)
    return np.exp(-0.5 * (distance / width) ** 2)


def build_valley_projectors(k2_grid: np.ndarray, width: float) -> dict[str, np.ndarray]:
    return {
        "K_B": valley_projector(k2_grid, center=1.0 / 3.0, width=width),
        "K_T": valley_projector(k2_grid, center=2.0 / 3.0, width=width),
        "total": np.ones_like(k2_grid, dtype=float),
    }


def pairing_profile(name: str, k2_grid: np.ndarray, valley_masks: dict[str, np.ndarray], delta0: float) -> np.ndarray:
    phase = 2.0 * np.pi * k2_grid
    kb = valley_masks["K_B"]
    kt = valley_masks["K_T"]
    valley_even = kb + kt
    valley_even = valley_even / max(float(np.max(valley_even)), 1e-12)
    valley_odd = kb - kt
    valley_odd = valley_odd / max(float(np.max(np.abs(valley_odd))), 1e-12)

    if name == "s_wave":
        return np.full_like(k2_grid, delta0)
    if name == "nodal_even":
        return delta0 * np.cos(phase)
    if name == "valley_even":
        return delta0 * valley_even
    if name == "valley_odd":
        return delta0 * valley_odd
    raise ValueError(name)


def generalized_btk_kernel(energy: float, gap: np.ndarray, transparency: float, eta: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    energy2 = float(energy) ** 2
    gap2 = np.abs(gap) ** 2
    denom = energy2 + gap2 + eta**2
    andreev = transparency * gap2 / denom
    normal_reflection = (1.0 - transparency) * energy2 / denom
    conductance = 1.0 + andreev - normal_reflection
    return conductance, andreev, normal_reflection


def load_sgf_maps() -> tuple[np.ndarray, np.ndarray, dict[str, np.ndarray]]:
    comparison = pd.read_csv(SGF_TRIAL_DIR / "edge_spectral_map_comparison.csv")
    k2_grid = np.sort(comparison["k2_reduced"].unique())
    energy_grid = np.sort(comparison["energy_meV"].unique())

    nk = len(k2_grid)
    ne = len(energy_grid)
    baseline_map = comparison["baseline_weight"].to_numpy().reshape(nk, ne)
    corrected_map = comparison["corrected_weight"].to_numpy().reshape(nk, ne)
    delta_map = comparison["delta_weight"].to_numpy().reshape(nk, ne)
    return k2_grid, energy_grid, {
        "baseline": baseline_map,
        "compressed_v3": corrected_map,
        "delta": delta_map,
    }


def build_background_weights(normal_map: np.ndarray) -> np.ndarray:
    high_bias = np.mean(normal_map[:, -20:], axis=1)
    return np.maximum(np.abs(high_bias), 1e-6)


def main() -> None:
    out_dir = OUTPUT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    k2_grid, energy_grid, map_bundle = load_sgf_maps()
    valley_width = 0.085
    valley_masks = build_valley_projectors(k2_grid=k2_grid, width=valley_width)

    barrier_values = [0.0, 0.5, 1.0, 2.0]
    eta_values = [0.05, 0.2, 0.5]
    pairings = ["s_wave", "nodal_even", "valley_even", "valley_odd"]
    delta0 = 1.5

    curve_rows: list[list[object]] = []
    robustness_rows: list[list[object]] = []
    projector_rows: list[list[object]] = []

    for valley_name, mask in valley_masks.items():
        for k2, value in zip(k2_grid, mask):
            projector_rows.append([valley_name, float(k2), float(value)])

    zero_idx = int(np.argmin(np.abs(energy_grid)))

    for model_name in ["baseline", "compressed_v3"]:
        normal_map = map_bundle[model_name]
        background = build_background_weights(normal_map)

        for pairing in pairings:
            gap_profile = pairing_profile(pairing, k2_grid, valley_masks, delta0)
            for eta in eta_values:
                for barrier in barrier_values:
                    transparency = 1.0 / (1.0 + barrier**2)
                    valley_curves: dict[str, list[float]] = {name: [] for name in valley_masks}
                    valley_andreev_curves: dict[str, list[float]] = {name: [] for name in valley_masks}
                    valley_normal_curves: dict[str, list[float]] = {name: [] for name in valley_masks}

                    for energy_index, energy in enumerate(energy_grid):
                        local_conductance, local_andreev, local_normal = generalized_btk_kernel(
                            energy=float(energy),
                            gap=gap_profile,
                            transparency=transparency,
                            eta=eta,
                        )
                        spectral_weight = np.maximum(np.abs(normal_map[:, energy_index]), 1e-8)
                        spectral_scale = np.clip(spectral_weight / background, 0.0, 8.0)
                        weighted_conductance = 1.0 + spectral_scale * (local_conductance - 1.0)
                        weighted_andreev = local_andreev * spectral_scale
                        weighted_normal = local_normal * spectral_scale

                        for valley_name, valley_mask in valley_masks.items():
                            weights = spectral_weight * valley_mask
                            weight_sum = max(float(np.sum(weights)), 1e-8)
                            valley_curves[valley_name].append(float(np.sum(weighted_conductance * weights) / weight_sum))
                            valley_andreev_curves[valley_name].append(float(np.sum(weighted_andreev * weights) / weight_sum))
                            valley_normal_curves[valley_name].append(float(np.sum(weighted_normal * weights) / weight_sum))

                    for valley_name in valley_masks:
                        conductance_curve = np.asarray(valley_curves[valley_name], dtype=float)
                        andreev_curve = np.asarray(valley_andreev_curves[valley_name], dtype=float)
                        normal_curve = np.asarray(valley_normal_curves[valley_name], dtype=float)
                        for energy, conductance, andreev, normal_reflection in zip(
                            energy_grid, conductance_curve, andreev_curve, normal_curve
                        ):
                            curve_rows.append(
                                [
                                    model_name,
                                    valley_name,
                                    pairing,
                                    barrier,
                                    eta,
                                    float(energy),
                                    float(conductance),
                                    float(andreev),
                                    float(normal_reflection),
                                ]
                            )

                        peak = float(np.max(conductance_curve))
                        background_level = float(np.mean(np.r_[conductance_curve[:20], conductance_curve[-20:]]))
                        robustness_rows.append(
                            [
                                model_name,
                                valley_name,
                                pairing,
                                barrier,
                                eta,
                                float(conductance_curve[zero_idx]),
                                peak,
                                background_level,
                                peak - background_level,
                                float(andreev_curve[zero_idx]),
                                float(normal_curve[zero_idx]),
                            ]
                        )

    robustness_df = pd.DataFrame(
        robustness_rows,
        columns=[
            "model",
            "valley",
            "pairing",
            "barrier_Z",
            "eta_meV",
            "zero_bias_conductance",
            "peak_conductance",
            "background_conductance",
            "peak_minus_background",
            "zero_bias_andreev",
            "zero_bias_normal_reflection",
        ],
    )

    baseline_total = robustness_df[
        (robustness_df["model"] == "baseline") & (robustness_df["valley"] == "total")
    ][["pairing", "barrier_Z", "eta_meV", "zero_bias_conductance", "peak_minus_background"]].rename(
        columns={
            "zero_bias_conductance": "baseline_zero_bias_conductance",
            "peak_minus_background": "baseline_peak_minus_background",
        }
    )
    corrected_total = robustness_df[
        (robustness_df["model"] == "compressed_v3") & (robustness_df["valley"] == "total")
    ][["pairing", "barrier_Z", "eta_meV", "zero_bias_conductance", "peak_minus_background"]].rename(
        columns={
            "zero_bias_conductance": "compressed_v3_zero_bias_conductance",
            "peak_minus_background": "compressed_v3_peak_minus_background",
        }
    )
    model_comparison = baseline_total.merge(corrected_total, on=["pairing", "barrier_Z", "eta_meV"], how="inner")
    model_comparison["delta_zero_bias_conductance"] = (
        model_comparison["compressed_v3_zero_bias_conductance"] - model_comparison["baseline_zero_bias_conductance"]
    )
    model_comparison["delta_peak_minus_background"] = (
        model_comparison["compressed_v3_peak_minus_background"] - model_comparison["baseline_peak_minus_background"]
    )

    corrected_kb = robustness_df[
        (robustness_df["model"] == "compressed_v3") & (robustness_df["valley"] == "K_B")
    ][["pairing", "barrier_Z", "eta_meV", "zero_bias_conductance", "peak_minus_background"]].rename(
        columns={
            "zero_bias_conductance": "kb_zero_bias_conductance",
            "peak_minus_background": "kb_peak_minus_background",
        }
    )
    corrected_kt = robustness_df[
        (robustness_df["model"] == "compressed_v3") & (robustness_df["valley"] == "K_T")
    ][["pairing", "barrier_Z", "eta_meV", "zero_bias_conductance", "peak_minus_background"]].rename(
        columns={
            "zero_bias_conductance": "kt_zero_bias_conductance",
            "peak_minus_background": "kt_peak_minus_background",
        }
    )
    valley_asymmetry = corrected_kb.merge(corrected_kt, on=["pairing", "barrier_Z", "eta_meV"], how="inner")
    valley_asymmetry["kb_minus_kt_zero_bias"] = (
        valley_asymmetry["kb_zero_bias_conductance"] - valley_asymmetry["kt_zero_bias_conductance"]
    )
    valley_asymmetry["kb_minus_kt_peak_contrast"] = (
        valley_asymmetry["kb_peak_minus_background"] - valley_asymmetry["kt_peak_minus_background"]
    )

    save_csv(
        out_dir / "conductance_curves.csv",
        [
            "model",
            "valley",
            "pairing",
            "barrier_Z",
            "eta_meV",
            "bias_meV",
            "conductance_generalized_btk",
            "andreev_component",
            "normal_reflection_component",
        ],
        curve_rows,
    )
    save_csv(
        out_dir / "robustness_summary.csv",
        list(robustness_df.columns),
        robustness_df.values.tolist(),
    )
    save_csv(
        out_dir / "model_comparison_summary.csv",
        list(model_comparison.columns),
        model_comparison.values.tolist(),
    )
    save_csv(
        out_dir / "valley_asymmetry_summary.csv",
        list(valley_asymmetry.columns),
        valley_asymmetry.values.tolist(),
    )
    save_csv(
        out_dir / "valley_projectors.csv",
        ["valley", "k2_reduced", "projector_weight"],
        projector_rows,
    )

    best_total = model_comparison.sort_values("delta_peak_minus_background", ascending=False).iloc[0]
    best_asym = valley_asymmetry.iloc[valley_asymmetry["kb_minus_kt_peak_contrast"].abs().argmax()]

    save_json(
        out_dir / "parameters.json",
        {
            "package_type": "valley_resolved_generalized_btk_semi_infinite_proxy",
            "normal_state_source": str(SGF_TRIAL_DIR / "edge_spectral_map_comparison.csv"),
            "model_variants": ["baseline", "compressed_v3"],
            "pairings": pairings,
            "barrier_values": barrier_values,
            "eta_values_meV": eta_values,
            "delta0_meV": delta0,
            "valley_centers_reduced_k2": {"K_B": 1.0 / 3.0, "K_T": 2.0 / 3.0},
            "valley_projector_width_reduced_k2": valley_width,
            "note": (
                "This package upgrades the older BTK minimal average into a valley-resolved generalized BTK proxy. "
                "It is explicitly anchored to the validated semi-infinite SGF compressed-V3 normal-state spectral map, "
                "but it still remains a proxy rather than a final multiorbital conductance benchmark."
            ),
            "best_total_peak_gain_case": {
                "pairing": str(best_total["pairing"]),
                "barrier_Z": float(best_total["barrier_Z"]),
                "eta_meV": float(best_total["eta_meV"]),
                "delta_peak_minus_background": float(best_total["delta_peak_minus_background"]),
            },
            "strongest_valley_asymmetry_case": {
                "pairing": str(best_asym["pairing"]),
                "barrier_Z": float(best_asym["barrier_Z"]),
                "eta_meV": float(best_asym["eta_meV"]),
                "kb_minus_kt_peak_contrast": float(best_asym["kb_minus_kt_peak_contrast"]),
            },
        },
    )

    summary = [
        "# Valley-Resolved Generalized BTK Package",
        "",
        "- Data status: generated",
        "- Method status: valley-resolved generalized BTK proxy anchored to the validated semi-infinite SGF compressed-V3 spectral map",
        f"- Model variants compared: baseline vs compressed-V3",
        f"- Pairings: {pairings}",
        f"- Barrier values: {barrier_values}",
        f"- Broadening values (meV): {eta_values}",
        f"- Valley projector width in reduced k2: {valley_width:.3f}",
        f"- Total conductance curves stored: {len(curve_rows) // len(energy_grid)}",
        (
            "- Strongest compressed-V3 total peak-contrast gain: "
            f"{best_total['pairing']} at Z={best_total['barrier_Z']}, eta={best_total['eta_meV']} meV "
            f"with d(peak-background)={best_total['delta_peak_minus_background']:.6f}"
        ),
        (
            "- Strongest compressed-V3 K_B vs K_T peak-contrast asymmetry: "
            f"{best_asym['pairing']} at Z={best_asym['barrier_Z']}, eta={best_asym['eta_meV']} meV "
            f"with K_B-K_T={best_asym['kb_minus_kt_peak_contrast']:.6f}"
        ),
        "- Caution: this package is already valley-resolved and compressed-V3-informed, but it is still a proxy benchmark rather than the final semi-infinite multiorbital BTK result.",
    ]
    (out_dir / "summary.md").write_text("\n".join(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
