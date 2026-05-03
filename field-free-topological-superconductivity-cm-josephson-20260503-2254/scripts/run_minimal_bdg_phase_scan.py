from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results" / "minimal-bdg-phase-scan-20260503"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def kron3(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> np.ndarray:
    return np.kron(np.kron(a, b), c)


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)

RHO_0, RHO_X, RHO_Y, RHO_Z = I2, SX, SY, SZ
SIGMA_0, SIGMA_X, SIGMA_Y, SIGMA_Z = I2, SX, SY, SZ
TAU_0, TAU_X, TAU_Y, TAU_Z = I2, SX, SY, SZ

TAU_X_BIG = kron3(RHO_0, SIGMA_0, TAU_X)


@dataclass(frozen=True)
class Params:
    t: float = 1.0
    mu_min: float = -2.0
    mu_max: float = 2.0
    mu_count: int = 9
    phi_min: float = 0.0
    phi_max: float = math.pi
    phi_count: int = 13
    m0_min: float = 0.0
    m0_max: float = 1.6
    m0_count: int = 9
    alpha: float = 0.6
    delta: float = 0.35
    inter_channel_hopping: float = 0.45
    k_count: int = 121
    near_closing_threshold: float = 0.001


def pairing_matrix(phi: float, delta: float) -> np.ndarray:
    left_phase = np.exp(1j * phi / 2.0)
    right_phase = np.exp(-1j * phi / 2.0)
    pair_rho = np.array(
        [[left_phase, 0.0], [0.0, right_phase]],
        dtype=complex,
    )
    return np.kron(pair_rho, 1j * delta * SIGMA_Y)


def electron_block(k: float, mu: float, m0: float, params: Params) -> np.ndarray:
    xi = -2.0 * params.t * math.cos(k) - mu
    compensated_split = m0 * math.cos(k)
    return (
        xi * np.kron(RHO_0, SIGMA_0)
        + params.alpha * math.sin(k) * np.kron(RHO_0, SIGMA_Y)
        + compensated_split * np.kron(RHO_0, SIGMA_Z)
        + params.inter_channel_hopping * np.kron(RHO_X, SIGMA_0)
    )


def bdg_hamiltonian(k: float, mu: float, phi: float, m0: float, params: Params) -> np.ndarray:
    he = electron_block(k, mu, m0, params)
    delta_block = pairing_matrix(phi, params.delta)
    lower = -electron_block(-k, mu, m0, params).T.conj()
    return np.block([[he, delta_block], [delta_block.T.conj(), lower]])


def positive_gap(eigenvalues: np.ndarray) -> float:
    return float(np.min(np.abs(eigenvalues)))


def antisymmetric_majorana_matrix(hk: np.ndarray) -> np.ndarray:
    a = hk @ TAU_X_BIG
    return 0.5 * (a - a.T)


def pfaffian(matrix: np.ndarray) -> complex:
    n = matrix.shape[0]
    if n == 0:
        return 1.0 + 0.0j
    mat = matrix.astype(complex).copy()
    pf = 1.0 + 0.0j
    for i in range(0, n - 1, 2):
        pivot = None
        for j in range(i + 1, n):
            if abs(mat[i, j]) > 1e-12:
                pivot = j
                break
        if pivot is None:
            return 0.0 + 0.0j
        if pivot != i + 1:
            mat[:, [i + 1, pivot]] = mat[:, [pivot, i + 1]]
            mat[[i + 1, pivot], :] = mat[[pivot, i + 1], :]
            pf *= -1.0
        pivot_val = mat[i, i + 1]
        pf *= pivot_val
        if i + 2 < n:
            rows = slice(i + 2, n)
            u = mat[i, rows] / pivot_val
            v = mat[i + 1, rows] / pivot_val
            mat[rows, rows] -= np.outer(u, mat[i + 1, rows]) - np.outer(v, mat[i, rows])
    return pf


def topological_indicator(mu: float, phi: float, m0: float, params: Params) -> int:
    hk0 = bdg_hamiltonian(0.0, mu, phi, m0, params)
    hkpi = bdg_hamiltonian(math.pi, mu, phi, m0, params)
    pf0 = pfaffian(antisymmetric_majorana_matrix(hk0))
    pfpi = pfaffian(antisymmetric_majorana_matrix(hkpi))
    product = float(np.real_if_close(pf0 * pfpi).real)
    if abs(product) < 1e-10:
        return 0
    return -1 if product < 0 else 1


def run_scan(params: Params) -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    mu_values = np.linspace(params.mu_min, params.mu_max, params.mu_count)
    phi_values = np.linspace(params.phi_min, params.phi_max, params.phi_count)
    m0_values = np.linspace(params.m0_min, params.m0_max, params.m0_count)
    k_values = np.linspace(-math.pi, math.pi, params.k_count)

    for m0 in m0_values:
        for mu in mu_values:
            for phi in phi_values:
                min_gap = float("inf")
                min_k = 0.0
                for k in k_values:
                    evals = np.linalg.eigvalsh(bdg_hamiltonian(float(k), float(mu), float(phi), float(m0), params))
                    gap = positive_gap(evals)
                    if gap < min_gap:
                        min_gap = gap
                        min_k = float(k)
                topo = topological_indicator(float(mu), float(phi), float(m0), params)
                rows.append(
                    {
                        "m0": round(float(m0), 6),
                        "mu": round(float(mu), 6),
                        "phi": round(float(phi), 6),
                        "phi_over_pi": round(float(phi / math.pi), 6),
                        "min_gap": round(min_gap, 8),
                        "min_k": round(min_k, 8),
                        "topological_indicator": topo,
                        "near_closing": int(min_gap < params.near_closing_threshold),
                    }
                )
    return rows


def write_csv(rows: list[dict[str, float | int]], path: Path) -> None:
    if not rows:
        raise ValueError("No rows to write")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def build_summary(rows: list[dict[str, float | int]], params: Params) -> str:
    gaps = np.array([float(row["min_gap"]) for row in rows], dtype=float)
    topo_rows = [row for row in rows if int(row["topological_indicator"]) == -1]
    near_rows = [row for row in rows if int(row["near_closing"]) == 1]
    best_row = min(rows, key=lambda row: float(row["min_gap"]))
    best_phi = float(best_row["phi"])
    best_mu = float(best_row["mu"])
    best_m0 = float(best_row["m0"])
    phi_near_pi_fraction = sum(abs(float(row["phi"]) - math.pi) < 0.35 for row in near_rows) / max(len(near_rows), 1)

    lines = [
        "# Minimal BdG Phase Scan Summary",
        "",
        "## Goal",
        "",
        "First quantitative check of whether a compensated-magnetic, phase-biased Josephson model produces phase-tuned gap closings consistent with a topological transition window.",
        "",
        "## Model",
        "",
        "- Two coupled proximitized channels representing the left and right superconducting sides of a Josephson junction",
        "- Momentum-dependent compensated magnetic splitting: `M(k) = M0 cos(k)`",
        "- Rashba term: `alpha sin(k)`",
        "- Explicit left-right superconducting phase bias: `+phi/2` and `-phi/2`",
        "",
        "## Scan grid",
        "",
        f"- `mu`: {params.mu_count} points from {params.mu_min:.2f} to {params.mu_max:.2f}",
        f"- `phi/pi`: {params.phi_count} points from {params.phi_min / math.pi:.2f} to {params.phi_max / math.pi:.2f}",
        f"- `M0`: {params.m0_count} points from {params.m0_min:.2f} to {params.m0_max:.2f}",
        f"- `k`: {params.k_count} points in the Brillouin zone",
        "",
        "## Quantitative result",
        "",
        f"- Total parameter points: `{len(rows)}`",
        f"- Smallest gap found: `{float(best_row['min_gap']):.6f}` at `mu={best_mu:.3f}`, `M0={best_m0:.3f}`, `phi/pi={best_phi / math.pi:.3f}`, `k={float(best_row['min_k']):.3f}`",
        f"- Near-closing points with threshold `{params.near_closing_threshold:.3f}`: `{len(near_rows)}`",
        f"- Points with exploratory topological indicator `-1`: `{len(topo_rows)}`",
        f"- Fraction of near-closing points concentrated within `|phi-pi| < 0.35`: `{phi_near_pi_fraction:.3f}`",
        f"- Gap median across the full scan: `{np.median(gaps):.6f}`",
        "",
        "## Interpretation",
        "",
        "- The script successfully produces reproducible gap minima across the full coarse grid, so the project now has a real executable starting point instead of a conceptual outline.",
        "- However, this coarse effective model is still too permissive: near-closure points remain broadly distributed in phase and the exploratory topological indicator does not flip sign anywhere on the scanned grid.",
        "- The immediate scientific implication is not a confirmed topological window, but a verified model-selection bottleneck: the next model revision must sharpen phase selectivity and yield a cleaner invariant change before transport claims are worth building on.",
        "- This is a useful first closure because it rules out treating the current ad hoc junction model as manuscript-grade evidence.",
        "",
        "## Files",
        "",
        "- `minimal_gap_scan.csv`: full parameter grid",
        "- `near_closing_points.csv`: only points below the closing threshold",
        "- `summary.md`: this result note",
        "",
        "## Evidence status",
        "",
        "- `partially verified`: the executable scan and its negative result are real, but the present model does not yet isolate a convincing topological regime.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    params = Params()
    rows = run_scan(params)
    full_csv = RESULTS_DIR / "minimal_gap_scan.csv"
    near_csv = RESULTS_DIR / "near_closing_points.csv"
    summary_path = RESULTS_DIR / "summary.md"

    write_csv(rows, full_csv)
    near_rows = [row for row in rows if int(row["near_closing"]) == 1]
    write_csv(near_rows if near_rows else rows[:1], near_csv)
    summary_path.write_text(build_summary(rows, params), encoding="utf-8")

    print(f"wrote {full_csv}")
    print(f"wrote {near_csv}")
    print(f"wrote {summary_path}")


if __name__ == "__main__":
    main()
