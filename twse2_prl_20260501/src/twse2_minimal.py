from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np


TAU0 = np.eye(2, dtype=complex)
TAUX = np.array([[0, 1], [1, 0]], dtype=complex)
TAUY = np.array([[0, -1j], [1j, 0]], dtype=complex)
TAUZ = np.array([[1, 0], [0, -1]], dtype=complex)

SIG0 = np.eye(2, dtype=complex)
SIGX = np.array([[0, 1], [1, 0]], dtype=complex)
SIGY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGZ = np.array([[1, 0], [0, -1]], dtype=complex)


@dataclass
class ModelParams:
    mu: float
    t1: float
    t2: float
    v1: float
    mz: float
    displacement_field: float
    zeeman_field: float
    phi_field: float
    delta_corr: float
    delta_sc: float
    gamma: float
    k_grid: int
    energy_min: float
    energy_max: float
    energy_points: int
    theta_points: int
    alpha_points: int
    eta_values: list[float]

    @classmethod
    def from_json(cls, path: str | Path) -> "ModelParams":
        data = json.loads(Path(path).read_text())
        return cls(**data)


def kron(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.kron(a, b)


def normal_hamiltonian(kx: float, ky: float, p: ModelParams) -> np.ndarray:
    xi = (
        -2.0 * p.t1 * (np.cos(kx) + np.cos(ky))
        - 4.0 * p.t2 * np.cos(kx) * np.cos(ky)
        - p.mu
    )
    gvx = p.v1 * np.sin(kx)
    gvy = p.v1 * np.sin(ky)
    gvz = p.mz + p.displacement_field * (np.cos(kx) - np.cos(ky))
    field_x = p.zeeman_field * np.cos(p.phi_field)
    field_y = p.zeeman_field * np.sin(p.phi_field)
    h = (
        xi * kron(TAU0, SIG0)
        + gvx * kron(TAUX, SIG0)
        + gvy * kron(TAUY, SIG0)
        + gvz * kron(TAUZ, SIG0)
        + field_x * kron(TAU0, SIGX)
        + field_y * kron(TAU0, SIGY)
    )
    return h


def correlated_background(p: ModelParams) -> np.ndarray:
    return p.delta_corr * kron(TAUX, SIG0)


def onsite_pairing_matrix(candidate: str, theta: float, p: ModelParams) -> np.ndarray:
    singlet = 1j * SIGY
    if candidate == "s_wave":
        return p.delta_sc * kron(TAU0, singlet)
    if candidate == "s_pm":
        return p.delta_sc * kron(TAUZ, singlet)
    if candidate == "chiral":
        phase = np.exp(2j * theta)
        return p.delta_sc * phase * kron(TAU0, singlet)
    raise ValueError(f"unknown candidate: {candidate}")


def bdg_hamiltonian(kx: float, ky: float, p: ModelParams, candidate: str) -> np.ndarray:
    h_n = normal_hamiltonian(kx, ky, p) + correlated_background(p)
    theta = np.arctan2(ky, kx + 1e-15)
    delta = onsite_pairing_matrix(candidate, theta, p)
    upper = np.hstack([h_n, delta])
    lower = np.hstack([delta.conj().T, -h_n.conj()])
    return np.vstack([upper, lower])


def lorentzian_sum(energies: np.ndarray, evals: np.ndarray, gamma: float) -> np.ndarray:
    diff = energies[:, None] - evals[None, :]
    return np.sum(gamma / np.pi / (diff * diff + gamma * gamma), axis=1)


def compute_dos(p: ModelParams, candidate: str = "s_wave") -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    k_values = np.linspace(-np.pi, np.pi, p.k_grid, endpoint=False)
    energies = np.linspace(p.energy_min, p.energy_max, p.energy_points)
    normal_dos = np.zeros_like(energies)
    bdg_dos = np.zeros_like(energies)
    count = 0
    for kx in k_values:
        for ky in k_values:
            h_n = normal_hamiltonian(kx, ky, p) + correlated_background(p)
            e_n = np.linalg.eigvalsh(h_n).real
            normal_dos += lorentzian_sum(energies, e_n, p.gamma)
            h_bdg = bdg_hamiltonian(kx, ky, p, candidate)
            e_b = np.linalg.eigvalsh(h_bdg).real
            bdg_dos += lorentzian_sum(energies, e_b, p.gamma)
            count += 1
    return energies, normal_dos / count, bdg_dos / count


def prominent_positive_peaks(energies: np.ndarray, values: np.ndarray, limit: int = 3) -> list[tuple[float, float]]:
    mask = energies > 0
    e_pos = energies[mask]
    v_pos = values[mask]
    peak_ids: list[int] = []
    for idx in range(1, len(e_pos) - 1):
        if v_pos[idx] >= v_pos[idx - 1] and v_pos[idx] >= v_pos[idx + 1]:
            peak_ids.append(idx)
    ranked = sorted(peak_ids, key=lambda idx: v_pos[idx], reverse=True)
    selected = []
    for idx in ranked:
        energy = float(e_pos[idx])
        if all(abs(energy - prev[0]) > 0.03 for prev in selected):
            selected.append((energy, float(v_pos[idx])))
        if len(selected) >= limit:
            break
    return sorted(selected, key=lambda item: item[0])


def candidate_gap(valley: int, theta: float, candidate: str, delta_sc: float) -> complex:
    valley_phase = 1.0 if valley == 1 else -1.0
    if candidate == "s_wave":
        return delta_sc
    if candidate == "s_pm":
        return delta_sc * valley_phase
    if candidate == "chiral":
        return delta_sc * np.exp(2j * theta)
    raise ValueError(f"unknown candidate: {candidate}")


def reflected_theta(theta: float, alpha: float) -> float:
    return 2.0 * alpha - theta + np.pi


def surface_frustration(candidate: str, alpha: float, eta: float, p: ModelParams) -> float:
    thetas = np.linspace(alpha - np.pi / 2.0, alpha + np.pi / 2.0, p.theta_points, endpoint=False)
    weights = np.abs(np.cos(thetas - alpha))
    total = 0.0
    norm = 0.0
    for theta, weight in zip(thetas, weights):
        theta_r = reflected_theta(theta, alpha)
        same = 0.0
        mixed = 0.0
        for valley in (1, -1):
            d_in = candidate_gap(valley, theta, candidate, p.delta_sc)
            d_same = candidate_gap(valley, theta_r, candidate, p.delta_sc)
            d_opp = candidate_gap(-valley, theta_r, candidate, p.delta_sc)
            same += 0.5 * (1.0 - np.real(d_in * np.conj(d_same)) / (abs(d_in) * abs(d_same) + 1e-12))
            mixed += 0.5 * (1.0 - np.real(d_in * np.conj(d_opp)) / (abs(d_in) * abs(d_opp) + 1e-12))
        total += weight * ((1.0 - eta) * same / 2.0 + eta * mixed / 2.0)
        norm += weight
    return total / norm


def screen_pairing_candidates(p: ModelParams) -> list[dict[str, float | str]]:
    alpha_values = np.linspace(0.0, np.pi / 2.0, p.alpha_points)
    rows: list[dict[str, float | str]] = []
    for candidate in ("s_wave", "s_pm", "chiral"):
        metrics = []
        for eta in p.eta_values:
            values = [surface_frustration(candidate, alpha, eta, p) for alpha in alpha_values]
            avg = float(np.mean(values))
            anis = float((max(values) - min(values)) / (avg + 1e-12))
            rows.append(
                {
                    "candidate": candidate,
                    "eta": float(eta),
                    "avg_frustration": avg,
                    "anisotropy_ratio": anis,
                    "alpha_min": float(alpha_values[int(np.argmin(values))]),
                    "alpha_max": float(alpha_values[int(np.argmax(values))]),
                }
            )
            metrics.append((eta, avg, anis))
        # The per-eta rows are the main outputs; list retained for debugger readability.
        _ = metrics
    return rows
