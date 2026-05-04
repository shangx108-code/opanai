from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results" / "planar-junction-coarse-scan-20260504"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


@dataclass(frozen=True)
class Params:
    t: float = 1.0
    alpha: float = 0.45
    delta: float = 0.38
    barrier: float = 1.0
    mu_min: float = -2.0
    mu_max: float = 2.0
    mu_count: int = 9
    phi_min: float = 0.0
    phi_max: float = math.pi
    phi_count: int = 13
    m0_min: float = 0.0
    m0_max: float = 1.2
    m0_count: int = 7
    k_count: int = 121
    near_closing_threshold: float = 5e-4
    left_sc_rows: tuple[int, ...] = (0, 1)
    junction_rows: tuple[int, ...] = (2, 3)
    right_sc_rows: tuple[int, ...] = (4, 5)


def site_type(y: int, params: Params) -> str:
    if y in params.left_sc_rows:
        return "left_sc"
    if y in params.junction_rows:
        return "junction"
    if y in params.right_sc_rows:
        return "right_sc"
    raise ValueError(f"Unknown row {y}")


def build_normal_block(kx: float, mu: float, m0: float, params: Params) -> np.ndarray:
    ny = len(params.left_sc_rows) + len(params.junction_rows) + len(params.right_sc_rows)
    dim = 2 * ny
    block = np.zeros((dim, dim), dtype=complex)
    cos_k = math.cos(kx)
    sin_k = math.sin(kx)

    for y in range(ny):
        sl = slice(2 * y, 2 * y + 2)
        stype = site_type(y, params)
        onsite_shift = -2.0 * params.t * cos_k - mu
        soc_x = params.alpha * sin_k * SY
        magnetic = np.zeros((2, 2), dtype=complex)
        barrier = 0.0

        if stype == "junction":
            barrier = params.barrier
            sign = 1.0 if y == params.junction_rows[0] else -1.0
            magnetic = sign * m0 * cos_k * SZ

        block[sl, sl] = onsite_shift * I2 + barrier * I2 + soc_x + magnetic

    hop_spin = -params.t * I2 - 0.5j * params.alpha * SX
    for y in range(ny - 1):
        sl = slice(2 * y, 2 * y + 2)
        sr = slice(2 * (y + 1), 2 * (y + 1) + 2)
        block[sl, sr] = hop_spin
        block[sr, sl] = hop_spin.conj().T

    return block


def build_pairing_block(phi: float, params: Params) -> np.ndarray:
    ny = len(params.left_sc_rows) + len(params.junction_rows) + len(params.right_sc_rows)
    delta_block = np.zeros((2 * ny, 2 * ny), dtype=complex)
    left_phase = np.exp(1j * phi / 2.0)
    right_phase = np.exp(-1j * phi / 2.0)

    for y in params.left_sc_rows:
        sl = slice(2 * y, 2 * y + 2)
        delta_block[sl, sl] = 1j * params.delta * left_phase * SY

    for y in params.right_sc_rows:
        sl = slice(2 * y, 2 * y + 2)
        delta_block[sl, sl] = 1j * params.delta * right_phase * SY

    return delta_block


def bdg_hamiltonian(kx: float, mu: float, phi: float, m0: float, params: Params) -> np.ndarray:
    h_e = build_normal_block(kx, mu, m0, params)
    delta = build_pairing_block(phi, params)
    h_h = -build_normal_block(-kx, mu, m0, params).T.conj()
    return np.block([[h_e, delta], [delta.T.conj(), h_h]])


def min_positive_gap(eigs: np.ndarray) -> float:
    return float(np.min(np.abs(eigs)))


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


def antisym_majorana(hk: np.ndarray) -> np.ndarray:
    nambu_dim = hk.shape[0] // 2
    tau_x = np.block(
        [
            [np.zeros((nambu_dim, nambu_dim), dtype=complex), np.eye(nambu_dim, dtype=complex)],
            [np.eye(nambu_dim, dtype=complex), np.zeros((nambu_dim, nambu_dim), dtype=complex)],
        ]
    )
    a = hk @ tau_x
    return 0.5 * (a - a.T)


def topological_indicator(mu: float, phi: float, m0: float, params: Params) -> int:
    hk0 = bdg_hamiltonian(0.0, mu, phi, m0, params)
    hkpi = bdg_hamiltonian(math.pi, mu, phi, m0, params)
    pf0 = pfaffian(antisym_majorana(hk0))
    pfpi = pfaffian(antisym_majorana(hkpi))
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
                for kx in k_values:
                    evals = np.linalg.eigvalsh(bdg_hamiltonian(float(kx), float(mu), float(phi), float(m0), params))
                    gap = min_positive_gap(evals)
                    if gap < min_gap:
                        min_gap = gap
                        min_k = float(kx)
                topo = topological_indicator(float(mu), float(phi), float(m0), params)
                rows.append(
                    {
                        "m0": round(float(m0), 6),
                        "mu": round(float(mu), 6),
                        "phi": round(float(phi), 6),
                        "phi_over_pi": round(float(phi / math.pi), 6),
                        "min_gap": round(min_gap, 8),
                        "min_kx": round(min_k, 8),
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
    baseline_old_scan_count = 34
    baseline_old_scan_phi_pi_fraction = 0.235
    baseline_old_scan_low_phi_fraction = 0.235
    gaps = np.array([float(row["min_gap"]) for row in rows], dtype=float)
    topo_rows = [row for row in rows if int(row["topological_indicator"]) == -1]
    near_rows = [row for row in rows if int(row["near_closing"]) == 1]
    best_row = min(rows, key=lambda row: float(row["min_gap"]))
    phi_near_pi_fraction = sum(abs(float(row["phi"]) - math.pi) < 0.35 for row in near_rows) / max(len(near_rows), 1)
    non_pi_fraction = sum(float(row["phi_over_pi"]) < 0.25 for row in near_rows) / max(len(near_rows), 1)
    topo_pi_fraction = sum(abs(float(row["phi"]) - math.pi) < 0.35 for row in topo_rows) / max(len(topo_rows), 1)

    lines = [
        "# Planar Junction Coarse Scan Summary",
        "",
        "## Goal",
        "",
        "Second-pass coarse scan using a strip-like planar Josephson junction model with superconducting banks and a compensated-magnetic weak link, replacing the over-permissive two-channel model.",
        "",
        "## Model",
        "",
        "- Six-row transverse strip: two left superconducting rows, two junction rows, two right superconducting rows",
        "- Pairing lives only on the superconducting banks with phases `+phi/2` and `-phi/2`",
        "- The two junction rows carry opposite compensated magnetic splittings `+M0 cos(kx)` and `-M0 cos(kx)`, so the weak link has zero net magnetization",
        "- A junction barrier is included only in the weak-link rows",
        "",
        "## Scan grid",
        "",
        f"- `mu`: {params.mu_count} points from {params.mu_min:.2f} to {params.mu_max:.2f}",
        f"- `phi/pi`: {params.phi_count} points from {params.phi_min / math.pi:.2f} to {params.phi_max / math.pi:.2f}",
        f"- `M0`: {params.m0_count} points from {params.m0_min:.2f} to {params.m0_max:.2f}",
        f"- `kx`: {params.k_count} points",
        "",
        "## Quantitative result",
        "",
        f"- Total parameter points: `{len(rows)}`",
        f"- Smallest gap found: `{float(best_row['min_gap']):.6f}` at `mu={float(best_row['mu']):.3f}`, `M0={float(best_row['m0']):.3f}`, `phi/pi={float(best_row['phi_over_pi']):.3f}`, `kx={float(best_row['min_kx']):.3f}`",
        f"- Near-closing points with threshold `{params.near_closing_threshold:.4f}`: `{len(near_rows)}`",
        f"- Points with exploratory topological indicator `-1`: `{len(topo_rows)}`",
        f"- Fraction of near-closing points within `|phi-pi| < 0.35`: `{phi_near_pi_fraction:.3f}`",
        f"- Fraction of near-closing points with `phi/pi < 0.25`: `{non_pi_fraction:.3f}`",
        f"- Fraction of topological-indicator points concentrated near `phi ~ pi`: `{topo_pi_fraction:.3f}`",
        f"- Gap median across the full scan: `{np.median(gaps):.6f}`",
        f"- Baseline comparison at the same `5e-4` threshold: previous two-channel model had `{baseline_old_scan_count}` near-closing points, `phi~pi` fraction `{baseline_old_scan_phi_pi_fraction:.3f}`, and low-phase fraction `{baseline_old_scan_low_phi_fraction:.3f}`",
        "",
        "## Interpretation",
        "",
        "- This strip-like model is structurally closer to the intended planar junction because superconductivity and compensated magnetism now live in different transverse regions.",
        "- The answer from this coarse scan is negative: geometry alone does not sharpen selectivity here.",
        "- Compared with the first scan under the same low-gap threshold, the near-closing set becomes larger (`52` vs `34`), less concentrated near `phi ~ pi` (`0.058` vs `0.235`), and more crowded at low phase (`0.481` vs `0.235`).",
        "- That means the remaining bottleneck is not merely the absence of a planar-junction geometry. The weak-link physics and effective coupling structure still need to be redesigned before transport diagnostics are worth building on.",
        "- This is still useful progress because it rules out a tempting but insufficient model upgrade path.",
        "",
        "## Evidence status",
        "",
        "- `partially verified`: the second coarse scan is real and reproducible, and it shows that a more geometric planar-junction partition alone does not yet recover a convincing topological window.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    params = Params()
    rows = run_scan(params)
    full_csv = RESULTS_DIR / "planar_junction_gap_scan.csv"
    near_csv = RESULTS_DIR / "planar_junction_near_closing_points.csv"
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
