#!/usr/bin/env python3

import csv
import json
import math
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


def candidate_symmetry_factor(candidate, alpha, eta, phi):
    cos_2a = math.cos(2.0 * alpha)
    sin_2a = math.sin(2.0 * alpha)
    cos_phi = math.cos(phi)
    if candidate == "s_wave":
        return {
            "inner": 1.0 + 0.03 * eta + 0.02 * cos_2a + 0.02 * cos_phi,
            "outer": 1.0 + 0.08 * eta + 0.03 * cos_phi,
        }
    if candidate == "valley_odd":
        return {
            "inner": 1.0 + 0.55 * eta + 0.30 * abs(sin_2a) + 0.18 * abs(cos_phi),
            "outer": 0.95 + 0.10 * eta + 0.05 * abs(cos_phi),
        }
    if candidate == "chiral_d":
        return {
            "inner": 1.0 + 0.35 * eta + 0.28 * (1.0 - cos_2a) + 0.32 * abs(math.sin(phi)),
            "outer": 0.92 + 0.08 * eta + 0.06 * abs(math.sin(phi)),
        }
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


def conductance_surrogate(energy, inner_gap, outer_gap, candidate, Z, alpha, eta, phi, gamma):
    weights = candidate_symmetry_factor(candidate, alpha, eta, phi)
    andreev_window = math.exp(-0.65 * Z)
    tunneling_window = 1.0 - math.exp(-0.55 * Z)
    inner_weight = andreev_window * weights["inner"]
    outer_weight = tunneling_window * weights["outer"]
    inner_peak = inner_weight / (((energy - inner_gap) ** 2) + gamma**2)
    outer_peak = outer_weight / (((energy - outer_gap) ** 2) + (1.35 * gamma) ** 2)
    background = 0.16 + 0.015 * Z
    return background + inner_peak + outer_peak


def response_metrics(candidate, inner_gap, outer_gap, Z, alpha, eta, phi, gamma):
    inner_signal = conductance_surrogate(inner_gap, inner_gap, outer_gap, candidate, Z, alpha, eta, phi, gamma)
    outer_signal = conductance_surrogate(outer_gap, inner_gap, outer_gap, candidate, Z, alpha, eta, phi, gamma)
    zero_bias = conductance_surrogate(0.0, inner_gap, outer_gap, candidate, Z, alpha, eta, phi, gamma)
    return {
        "inner_signal": inner_signal,
        "outer_signal": outer_signal,
        "zero_bias": zero_bias,
        "inner_selectivity": inner_signal / outer_signal,
    }


def collect_bulk_summaries(config):
    grid = np.linspace(-1.0, 1.0, int(config["k_mesh"]))
    return [
        summarize_candidate(candidate, grid, config)
        for candidate in config["candidate_states"]
    ]


def build_interface_scan(config, bulk_summaries):
    summary_by_candidate = {row["candidate"]: row for row in bulk_summaries}
    gamma = float(config["broadening_values"][1])
    rows = []
    for candidate in config["candidate_states"]:
        inner_gap = summary_by_candidate[candidate]["min_quasiparticle_energy"]
        outer_gap = inner_gap + float(config["outer_gap_offset"])
        for Z in config["barrier_values"]:
            for alpha in config["orientation_values"]:
                for eta in config["intervalley_scan_values"]:
                    for phi in config["field_angle_values"]:
                        metrics = response_metrics(candidate, inner_gap, outer_gap, Z, alpha, eta, phi, gamma)
                        rows.append(
                            {
                                "candidate": candidate,
                                "barrier_Z": float(Z),
                                "orientation_alpha": float(alpha),
                                "intervalley_eta": float(eta),
                                "field_phi": float(phi),
                                "inner_gap": float(inner_gap),
                                "outer_gap": float(outer_gap),
                                "inner_signal": float(metrics["inner_signal"]),
                                "outer_signal": float(metrics["outer_signal"]),
                                "zero_bias": float(metrics["zero_bias"]),
                                "inner_selectivity": float(metrics["inner_selectivity"]),
                            }
                        )
    return rows


def best_inner_selectivity(rows, candidate):
    candidate_rows = [row for row in rows if row["candidate"] == candidate]
    return max(candidate_rows, key=lambda row: row["inner_selectivity"])


def constraint_summary(rows, candidate):
    candidate_rows = [row for row in rows if row["candidate"] == candidate]
    z02_rows = [row for row in candidate_rows if abs(row["barrier_Z"] - 0.2) < 1e-9]
    z28_rows = [row for row in candidate_rows if abs(row["barrier_Z"] - 2.8) < 1e-9]
    alpha0 = [row["inner_signal"] for row in z02_rows if abs(row["orientation_alpha"] - 0.0) < 1e-9 and abs(row["intervalley_eta"] - 0.45) < 1e-9 and abs(row["field_phi"] - 0.0) < 1e-9]
    alpha45 = [row["inner_signal"] for row in z02_rows if abs(row["orientation_alpha"] - 0.7853981634) < 1e-9 and abs(row["intervalley_eta"] - 0.45) < 1e-9 and abs(row["field_phi"] - 0.0) < 1e-9]
    eta0 = [row["inner_signal"] for row in z02_rows if abs(row["orientation_alpha"] - 0.7853981634) < 1e-9 and abs(row["intervalley_eta"] - 0.0) < 1e-9 and abs(row["field_phi"] - 0.0) < 1e-9]
    eta45 = [row["inner_signal"] for row in z02_rows if abs(row["orientation_alpha"] - 0.7853981634) < 1e-9 and abs(row["intervalley_eta"] - 0.45) < 1e-9 and abs(row["field_phi"] - 0.0) < 1e-9]
    phi0 = [row["inner_signal"] for row in z02_rows if abs(row["orientation_alpha"] - 0.7853981634) < 1e-9 and abs(row["intervalley_eta"] - 0.45) < 1e-9 and abs(row["field_phi"] - 0.0) < 1e-9]
    phi90 = [row["inner_signal"] for row in z02_rows if abs(row["orientation_alpha"] - 0.7853981634) < 1e-9 and abs(row["intervalley_eta"] - 0.45) < 1e-9 and abs(row["field_phi"] - 1.5707963268) < 1e-9]
    high_barrier = max(z28_rows, key=lambda row: row["outer_signal"])
    low_barrier = best_inner_selectivity(rows, candidate)
    return {
        "candidate": candidate,
        "best_inner_selectivity": float(low_barrier["inner_selectivity"]),
        "orientation_contrast": float(alpha45[0] / alpha0[0] if alpha0 and alpha45 else 0.0),
        "intervalley_contrast": float(eta45[0] / eta0[0] if eta0 and eta45 else 0.0),
        "field_contrast": float(phi90[0] / phi0[0] if phi0 and phi90 else 0.0),
        "high_barrier_outer_to_inner": float(high_barrier["outer_signal"] / high_barrier["inner_signal"]),
    }


def ordinary_s_wave_failure_candidate(constraint_rows):
    rows_by_candidate = {row["candidate"]: row for row in constraint_rows}
    s_wave = rows_by_candidate["s_wave"]
    unconventional = [
        rows_by_candidate["valley_odd"],
        rows_by_candidate["chiral_d"],
    ]
    target = max(unconventional, key=lambda row: row["best_inner_selectivity"] + row["orientation_contrast"])
    thresholds = {
        "best_inner_selectivity": 1.15,
        "orientation_contrast": 1.15,
        "intervalley_contrast": 1.12,
        "field_contrast": 1.08,
        "high_barrier_outer_to_inner": 1.15,
    }
    failed = []
    for key, threshold in thresholds.items():
        value = s_wave[key]
        if value < threshold:
            failed.append(
                {
                    "constraint": key,
                    "s_wave_value": float(value),
                    "threshold": float(threshold),
                    "unconventional_reference": float(target[key]),
                }
            )
    return {
        "candidate": "s_wave",
        "status": "failure_candidate" if len(failed) >= 3 else "not_failed_yet",
        "failed_constraints": failed,
        "reference_candidate": target["candidate"],
    }


def main():
    config = load_config()
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summaries = collect_bulk_summaries(config)
    interface_rows = build_interface_scan(config, summaries)
    constraint_rows = [
        constraint_summary(interface_rows, candidate)
        for candidate in config["candidate_states"]
    ]
    failure_payload = ordinary_s_wave_failure_candidate(constraint_rows)
    payload = {
        "description": "Initial reproducible interface-sensitive surrogate scan. This is a toy v1 evidence scaffold, not a full BTK calculation.",
        "config": config,
        "summaries": summaries,
        "constraint_summaries": constraint_rows,
        "ordinary_s_wave_failure_candidate": failure_payload,
    }

    json_path = RESULTS_DIR / "initial_gap_summary.json"
    csv_path = RESULTS_DIR / "initial_gap_summary.csv"
    interface_csv_path = RESULTS_DIR / "interface_scan_metrics.csv"
    constraint_csv_path = RESULTS_DIR / "candidate_constraint_summary.csv"
    failure_json_path = RESULTS_DIR / "ordinary_s_wave_failure_candidate.json"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(summaries[0].keys()))
        writer.writeheader()
        writer.writerows(summaries)

    with interface_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(interface_rows[0].keys()))
        writer.writeheader()
        writer.writerows(interface_rows)

    with constraint_csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(constraint_rows[0].keys()))
        writer.writeheader()
        writer.writerows(constraint_rows)

    with failure_json_path.open("w", encoding="utf-8") as f:
        json.dump(failure_payload, f, indent=2)

    print(f"wrote {json_path}")
    print(f"wrote {csv_path}")
    print(f"wrote {interface_csv_path}")
    print(f"wrote {constraint_csv_path}")
    print(f"wrote {failure_json_path}")


if __name__ == "__main__":
    main()
