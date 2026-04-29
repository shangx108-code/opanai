from __future__ import annotations

import json

import numpy as np
import pandas as pd

from twse2_persistent_pipeline import DATA_ROOT, save_csv, save_json


def dynes_dos(energy: np.ndarray, gap: np.ndarray, eta: float) -> np.ndarray:
    z = energy + 1j * eta
    return np.real(z / np.sqrt(z**2 - gap**2 + 0j))


def pairing_profile(name: str, k2_grid: np.ndarray, delta0: float) -> np.ndarray:
    phase = 2.0 * np.pi * k2_grid
    if name == "s_wave":
        return np.full_like(k2_grid, delta0)
    if name == "nodal_even":
        return delta0 * np.cos(phase)
    if name == "odd_proxy":
        return delta0 * np.sin(phase)
    raise ValueError(name)


def main() -> None:
    out_dir = DATA_ROOT / "btk-minimal-2026-04-29"
    out_dir.mkdir(parents=True, exist_ok=True)

    sgf_dir = DATA_ROOT / "sgf-minimal-2026-04-29"
    zero_bias = pd.read_csv(sgf_dir / "zero_bias_edge_profile.csv")
    k2_grid = zero_bias["k2_reduced"].to_numpy()
    weights = zero_bias["edge_spectral_weight_E0"].to_numpy()
    weights = np.maximum(weights, 1e-8)
    weights = weights / np.sum(weights)

    energy_grid = np.linspace(-8.0, 8.0, 321)
    barrier_values = [0.0, 0.5, 1.0, 2.0]
    eta_values = [0.05, 0.2, 0.5]
    pairings = ["s_wave", "nodal_even", "odd_proxy"]
    delta0 = 1.5

    rows: list[list[object]] = []
    robustness_rows: list[list[object]] = []

    for pairing in pairings:
        gap_profile = pairing_profile(pairing, k2_grid, delta0)
        for eta in eta_values:
            local_dos = np.asarray([dynes_dos(np.array([energy]), gap_profile, eta) for energy in energy_grid])
            averaged_dos = local_dos @ weights
            for barrier in barrier_values:
                transparency = 1.0 / (1.0 + barrier**2)
                conductance = 1.0 + transparency * (averaged_dos - 1.0)
                for energy, value in zip(energy_grid, conductance):
                    rows.append([pairing, barrier, eta, float(energy), float(value)])

                zero_idx = int(np.argmin(np.abs(energy_grid)))
                peak = float(np.max(conductance))
                background = float(np.mean(np.r_[conductance[:20], conductance[-20:]]))
                robustness_rows.append(
                    [
                        pairing,
                        barrier,
                        eta,
                        float(conductance[zero_idx]),
                        peak,
                        background,
                        peak - background,
                    ]
                )

    save_csv(
        out_dir / "conductance_curves.csv",
        ["pairing", "barrier_Z", "eta_meV", "bias_meV", "conductance_proxy"],
        rows,
    )
    save_csv(
        out_dir / "robustness_summary.csv",
        ["pairing", "barrier_Z", "eta_meV", "zero_bias_conductance", "peak_conductance", "background_conductance", "peak_minus_background"],
        robustness_rows,
    )
    save_json(
        out_dir / "parameters.json",
        {
            "package_type": "btk_proxy",
            "energy_window_meV": [-8.0, 8.0],
            "energy_grid_size": len(energy_grid),
            "pairings": pairings,
            "barrier_values": barrier_values,
            "eta_values_meV": eta_values,
            "delta0_meV": delta0,
            "normal_state_weight_source": str(sgf_dir / "zero_bias_edge_profile.csv"),
            "note": "This is a minimal BTK-like proxy package built on the SGF minimal edge weights, not yet a full multiorbital material-specific BTK calculation.",
        },
    )

    summary = [
        "# BTK Minimal Data Package",
        "",
        "- Data status: generated",
        "- Method status: BTK-like conductance proxy weighted by the SGF minimal edge profile",
        f"- Number of pairings: {len(pairings)}",
        f"- Barrier values: {barrier_values}",
        f"- Broadening values (meV): {eta_values}",
        f"- Total conductance curves stored: {len(pairings) * len(barrier_values) * len(eta_values)}",
        "- Caution: this package is a persistent minimal proxy only; it is not yet the final material-specific BTK benchmark required for the manuscript.",
    ]
    (out_dir / "summary.md").write_text("\n".join(summary), encoding="utf-8")


if __name__ == "__main__":
    main()
