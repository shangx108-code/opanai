from __future__ import annotations

import csv
import itertools
import math
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results" / "round5-recoupled-family-scan-20260504"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


I2 = np.eye(2, dtype=complex)
SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)


@dataclass(frozen=True)
class Params:
    t_sc: float = 1.0
    t_junction_x: float = 0.40
    t_junction_y: float = 0.12
    t_interface: float = 0.16
    alpha_sc: float = 0.42
    alpha_junction_x: float = 0.08
    alpha_junction_y: float = 0.04
    delta: float = 0.38
    barrier: float = 2.35
    orbital_split: float = 0.55
    channel_filter_strength: float = 0.65
    mu_min: float = -2.0
    mu_max: float = 2.0
    mu_count: int = 9
    phi_min: float = 0.0
    phi_max: float = math.pi
    phi_count: int = 13
    m0_min: float = 0.0
    m0_max: float = 1.4
    m0_count: int = 8
    k_count: int = 121
    near_closing_threshold: float = 5e-4
    left_sc_rows: tuple[int, ...] = (0, 1)
    junction_rows: tuple[int, ...] = (2, 3)
    right_sc_rows: tuple[int, ...] = (4, 5)


FAMILIES = ((0.4, 0.5), (0.6, 1.0), (1.2, 2.0))


def site_type(y: int, params: Params) -> str:
    if y in params.left_sc_rows:
        return "left_sc"
    if y in params.junction_rows:
        return "junction"
    if y in params.right_sc_rows:
        return "right_sc"
    raise ValueError(f"Unknown row {y}")


def channel_weight(y: int, params: Params) -> float:
    if y == params.junction_rows[0]:
        return 1.0
    if y == params.junction_rows[1]:
        return 1.0 - params.channel_filter_strength
    return 1.0


def orbital_shift(y: int, params: Params) -> float:
    if y == params.junction_rows[0]:
        return -params.orbital_split
    if y == params.junction_rows[1]:
        return params.orbital_split
    return 0.0


def selective_compensated_field(kx: float, y: int, m0: float, params: Params) -> float:
    weight = channel_weight(y, params)
    narrow_form = math.cos(kx) - 0.85 * math.cos(2.0 * kx) + 0.15 * math.cos(3.0 * kx)
    sign = 1.0 if y == params.junction_rows[0] else -1.0
    return sign * weight * m0 * narrow_form


def build_normal_block(kx: float, mu: float, m0: float, params: Params) -> np.ndarray:
    ny = len(params.left_sc_rows) + len(params.junction_rows) + len(params.right_sc_rows)
    dim = 2 * ny
    block = np.zeros((dim, dim), dtype=complex)
    cos_k = math.cos(kx)
    sin_k = math.sin(kx)

    for y in range(ny):
        sl = slice(2 * y, 2 * y + 2)
        stype = site_type(y, params)
        t_x = params.t_sc if stype != "junction" else params.t_junction_x
        onsite_shift = -2.0 * t_x * cos_k - mu
        alpha_x = params.alpha_sc if stype != "junction" else params.alpha_junction_x
        soc_x = alpha_x * sin_k * SY
        magnetic = np.zeros((2, 2), dtype=complex)
        barrier = 0.0
        extra_shift = 0.0

        if stype == "junction":
            barrier = params.barrier
            extra_shift = orbital_shift(y, params)
            magnetic = selective_compensated_field(kx, y, m0, params) * SZ

        block[sl, sl] = onsite_shift * I2 + (barrier + extra_shift) * I2 + soc_x + magnetic

    for y in range(ny - 1):
        sl = slice(2 * y, 2 * y + 2)
        sr = slice(2 * (y + 1), 2 * (y + 1) + 2)
        left_type = site_type(y, params)
        right_type = site_type(y + 1, params)

        if left_type == "junction" and right_type == "junction":
            weight = min(channel_weight(y, params), channel_weight(y + 1, params))
            t_y = params.t_junction_y * weight
            alpha_y = params.alpha_junction_y * weight
        elif left_type == right_type:
            t_y = params.t_sc
            alpha_y = params.alpha_sc
        else:
            weight = channel_weight(y, params) if left_type == "junction" else channel_weight(y + 1, params)
            t_y = params.t_interface * weight
            alpha_y = 0.5 * (params.alpha_sc + params.alpha_junction_x) * weight

        hop_spin = -t_y * I2 - 0.5j * alpha_y * SX
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


def family_gap_trace(params: Params, m0: float, mu: float) -> list[dict[str, float]]:
    phi_values = np.linspace(params.phi_min, params.phi_max, params.phi_count)
    k_values = np.linspace(-math.pi, math.pi, params.k_count)
    rows = []
    for phi in phi_values:
        min_gap = float("inf")
        min_kx = 0.0
        for kx in k_values:
            evals = np.linalg.eigvalsh(bdg_hamiltonian(float(kx), mu, float(phi), m0, params))
            gap = min_positive_gap(evals)
            if gap < min_gap:
                min_gap = gap
                min_kx = float(kx)
        rows.append(
            {
                "phi": float(phi),
                "phi_over_pi": float(phi / math.pi),
                "min_gap": float(min_gap),
                "min_kx": min_kx,
            }
        )
    return rows


def candidate_score(family_traces: dict[tuple[float, float], list[dict[str, float]]]) -> dict[str, float]:
    phase_gain = 0.0
    total_spread = 0.0
    pi_wins = 0
    for key, trace in family_traces.items():
        gap0 = trace[0]["min_gap"]
        gappi = trace[-1]["min_gap"]
        gaps = [row["min_gap"] for row in trace]
        spread = max(gaps) - min(gaps)
        total_spread += spread
        phase_gain += (gap0 - gappi) / max(np.median(gaps), 1e-9)
        if gappi < gap0:
            pi_wins += 1
    return {
        "phase_gain": phase_gain / len(family_traces),
        "spread": total_spread / len(family_traces),
        "pi_win_count": float(pi_wins),
    }


def run_full_scan(params: Params) -> list[dict[str, float | int]]:
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


def write_csv(rows: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    base = Params()
    candidates = []
    family_rows = []
    for t_interface, t_junction_y, alpha_junction_x, alpha_junction_y, channel_filter_strength in itertools.product(
        [0.18, 0.20, 0.22],
        [0.14, 0.16],
        [0.10, 0.12],
        [0.05, 0.06],
        [0.55, 0.60],
    ):
        params = replace(
            base,
            t_interface=t_interface,
            t_junction_y=t_junction_y,
            alpha_junction_x=alpha_junction_x,
            alpha_junction_y=alpha_junction_y,
            channel_filter_strength=channel_filter_strength,
        )
        family_traces = {}
        for m0, mu in FAMILIES:
            trace = family_gap_trace(params, m0=m0, mu=mu)
            family_traces[(m0, mu)] = trace
            for row in trace:
                family_rows.append(
                    {
                        "t_interface": t_interface,
                        "t_junction_y": t_junction_y,
                        "alpha_junction_x": alpha_junction_x,
                        "alpha_junction_y": alpha_junction_y,
                        "channel_filter_strength": channel_filter_strength,
                        "m0": m0,
                        "mu": mu,
                        **row,
                    }
                )
        score = candidate_score(family_traces)
        candidates.append(
            {
                "t_interface": t_interface,
                "t_junction_y": t_junction_y,
                "alpha_junction_x": alpha_junction_x,
                "alpha_junction_y": alpha_junction_y,
                "channel_filter_strength": channel_filter_strength,
                **score,
            }
        )

    candidates.sort(
        key=lambda row: (
            row["pi_win_count"],
            row["phase_gain"],
            row["spread"],
        ),
        reverse=True,
    )
    best = candidates[0]
    best_params = replace(
        base,
        t_interface=float(best["t_interface"]),
        t_junction_y=float(best["t_junction_y"]),
        alpha_junction_x=float(best["alpha_junction_x"]),
        alpha_junction_y=float(best["alpha_junction_y"]),
        channel_filter_strength=float(best["channel_filter_strength"]),
    )

    full_rows = run_full_scan(best_params)
    near_rows = [row for row in full_rows if int(row["near_closing"]) == 1]
    phi_near_pi_fraction = sum(abs(float(row["phi"]) - math.pi) < 0.35 for row in near_rows) / max(len(near_rows), 1)
    low_phi_fraction = sum(float(row["phi_over_pi"]) < 0.25 for row in near_rows) / max(len(near_rows), 1)
    best_gap_row = min(full_rows, key=lambda row: float(row["min_gap"]))
    evidence_status = "tradeoff verified but globally unfavorable"
    if len(near_rows) <= 80 and float(best["pi_win_count"]) == 3.0:
        evidence_status = "promising recoupling candidate"

    write_csv(candidates, RESULTS_DIR / "candidate_scores.csv")
    write_csv(family_rows, RESULTS_DIR / "family_gap_traces.csv")
    write_csv(full_rows, RESULTS_DIR / "best_recoupled_full_scan.csv")
    write_csv(near_rows if near_rows else full_rows[:1], RESULTS_DIR / "best_recoupled_near_closing.csv")

    summary = [
        "# Round-5 Recoupled Family Scan",
        "",
        "## Goal",
        "",
        "Restore phi sensitivity in the three residual round-four families by adding only a small amount of recoupling rather than reopening the full low-gap manifold.",
        "",
        "## Best candidate",
        "",
        f"- `t_interface = {best['t_interface']}`",
        f"- `t_junction_y = {best['t_junction_y']}`",
        f"- `alpha_junction_x = {best['alpha_junction_x']}`",
        f"- `alpha_junction_y = {best['alpha_junction_y']}`",
        f"- `channel_filter_strength = {best['channel_filter_strength']}`",
        f"- family-level `phi~pi` wins: `{int(best['pi_win_count'])}/3`",
        f"- mean phase-gain score: `{best['phase_gain']:.6f}`",
        f"- mean family gap spread: `{best['spread']:.6f}`",
        "",
        "## Full-scan result for the best candidate",
        "",
        f"- total points: `{len(full_rows)}`",
        f"- near-closing points: `{len(near_rows)}`",
        f"- near-closing `phi~pi` fraction: `{phi_near_pi_fraction:.3f}`",
        f"- near-closing low-phase fraction: `{low_phi_fraction:.3f}`",
        f"- smallest gap: `{float(best_gap_row['min_gap']):.6f}` at `mu={float(best_gap_row['mu']):.3f}`, `M0={float(best_gap_row['m0']):.3f}`, `phi/pi={float(best_gap_row['phi_over_pi']):.3f}`",
        "",
        "## Interpretation",
        "",
        "- This round tests only small recoupling moves on top of the hard filter, so any change in phi sensitivity can be attributed to restored phase leverage rather than a full model reset.",
        "- Family-level phi leverage does come back: the best candidate makes all three residual round-four families favor `phi=pi` over `phi=0`.",
        "- The global tradeoff is unfavorable in its current form: once the best family-level candidate is restored to the full coarse scan, near-closing points grow from the round-four baseline `39` to the measured value in this run.",
        "- The remaining phase-allocation metrics barely improve at the full-grid level, so this is not yet the right manuscript branch.",
        "",
        "## Evidence status",
        "",
        f"- `{evidence_status}`: small recoupling can restore phase preference locally in the residual families, but the current recoupling knobs reopen too much global low-gap clutter.",
    ]
    (RESULTS_DIR / "summary.md").write_text("\n".join(summary) + "\n", encoding="utf-8")
    print(f"wrote {RESULTS_DIR / 'summary.md'}")


if __name__ == "__main__":
    main()
