#!/usr/bin/env python3

import csv
import json
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "default_scan_config.json"
RESULTS_DIR = ROOT / "results"


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def normal_state(kx, ky, mu, displacement_field, zeeman_field, intervalley_mixing):
    xi = 0.35 * (kx**2 + ky**2) - mu
    gv = np.array(
        [
            intervalley_mixing,
            displacement_field + 0.10 * kx,
            0.10 * ky,
        ],
        dtype=float,
    )
    valley_split = np.linalg.norm(gv)
    return xi + valley_split + zeeman_field, xi - valley_split - zeeman_field


def gap_amplitude(candidate, kx, ky):
    if candidate == "s_wave":
        return 0.04
    if candidate == "valley_odd":
        return 0.03 + 0.015 * np.tanh(2.0 * kx)
    if candidate == "chiral_d":
        radius = np.hypot(kx, ky)
        phase_amp = radius**2 / (1.0 + radius**2)
        return 0.035 * phase_amp
    raise ValueError(f"unknown candidate: {candidate}")


def quasiparticle_energies(candidate, kx, ky, config):
    e_plus, e_minus = normal_state(
        kx,
        ky,
        config["mu"],
        config["displacement_field"],
        config["zeeman_field"],
        config["intervalley_mixing"],
    )
    delta = gap_amplitude(candidate, kx, ky)
    return np.sqrt(e_plus**2 + delta**2), np.sqrt(e_minus**2 + delta**2)


def summarize_candidate(candidate, grid, config):
    energies = []
    gap_values = []
    for kx in grid:
        for ky in grid:
            e1, e2 = quasiparticle_energies(candidate, kx, ky, config)
            energies.extend([e1, e2])
            gap_values.append(abs(gap_amplitude(candidate, kx, ky)))
    energies = np.asarray(energies)
    gap_values = np.asarray(gap_values)
    return {
        "candidate": candidate,
        "min_quasiparticle_energy": float(np.min(energies)),
        "median_quasiparticle_energy": float(np.median(energies)),
        "max_quasiparticle_energy": float(np.max(energies)),
        "min_gap_amplitude": float(np.min(gap_values)),
        "max_gap_amplitude": float(np.max(gap_values)),
    }


def main():
    config = load_config()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    grid = np.linspace(-1.0, 1.0, int(config["k_mesh"]))

    summaries = [
        summarize_candidate(candidate, grid, config)
        for candidate in config["candidate_states"]
    ]
    payload = {
        "description": "Initial reproducible bulk-gap scaffold summary. This is a v0 setup artifact, not publication-grade evidence.",
        "config": config,
        "summaries": summaries,
    }

    json_path = RESULTS_DIR / "initial_gap_summary.json"
    csv_path = RESULTS_DIR / "initial_gap_summary.csv"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summaries[0].keys()))
        writer.writeheader()
        writer.writerows(summaries)

    print(f"wrote {json_path}")
    print(f"wrote {csv_path}")


if __name__ == "__main__":
    main()
