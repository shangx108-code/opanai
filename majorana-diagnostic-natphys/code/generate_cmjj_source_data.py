#!/usr/bin/env python3
"""Generate source-data bundles for Figures 2-5 of the CMJJ diagnostic branch.

This script builds a minimal effective compensated-magnetic Josephson-junction
model that can be executed with the currently available runtime stack
(`numpy` and `pandas`, without `scipy` or `matplotlib`).

Outputs are written into the long-term project space under:
`/workspace/memory/majorana-diagnostic-natphys/data/cmjj-source-data-2026-05-01/`
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path("/workspace/memory/majorana-diagnostic-natphys")
CODE_ROOT = PROJECT_ROOT / "code"
CONFIG_PATH = PROJECT_ROOT / "config" / "cmjj_source_data_config.json"
DATA_ROOT = PROJECT_ROOT / "data" / "cmjj-source-data-2026-05-01"


SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
S0 = np.eye(2, dtype=complex)
TAU_X = np.array([[0, 1], [1, 0]], dtype=complex)
TAU_Z = np.array([[1, 0], [0, -1]], dtype=complex)
TAU_0 = np.eye(2, dtype=complex)
PAIRING_SPIN = np.array([[0, 1], [-1, 0]], dtype=complex)


@dataclass
class ModelParams:
    t: float = 1.0
    alpha: float = 0.8
    mc: float = 1.0
    bphi: float = 1.8
    delta: float = 0.5
    eta: float = 1.0e-3
    gamma_lead: float = 0.25


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def ensure_dirs() -> None:
    for path in [
        DATA_ROOT,
        DATA_ROOT / "source_data_fig2",
        DATA_ROOT / "source_data_fig3",
        DATA_ROOT / "source_data_fig4",
        DATA_ROOT / "source_data_fig5",
    ]:
        path.mkdir(parents=True, exist_ok=True)


def pairing_amplitude(delta: float, phi: float) -> float:
    return delta * math.cos(phi / 2.0)


def phase_field(bphi: float, phi: float) -> float:
    return bphi * math.sin(phi / 2.0)


def kspace_bdg(k: float, mu: float, phi: float, params: ModelParams) -> np.ndarray:
    beff = phase_field(params.bphi, phi)
    deff = pairing_amplitude(params.delta, phi)
    kinetic = (-2.0 * params.t * math.cos(k) - mu) * np.kron(TAU_Z, S0)
    soc = params.alpha * math.sin(k) * np.kron(TAU_Z, SY)
    compensated = params.mc * math.cos(k) * np.kron(TAU_0, SZ)
    phase_term = beff * np.kron(TAU_0, SX)
    pairing = deff * np.kron(TAU_X, S0)
    return kinetic + soc + compensated + phase_term + pairing


def build_real_space_bdg(
    num_sites: int,
    mu: float,
    phi: float,
    params: ModelParams,
    *,
    dot_strength: float = 0.0,
    dot_sigma: float = 4.0,
    impurity_strength: float = 0.0,
    disorder: np.ndarray | None = None,
    periodic: bool = False,
    apbc: bool = False,
) -> np.ndarray:
    num_e = 2 * num_sites
    h = np.zeros((num_e, num_e), dtype=complex)
    beff = phase_field(params.bphi, phi)
    hop = -params.t * S0 - 0.5j * params.alpha * SY + 0.5 * params.mc * SZ

    for site in range(num_sites):
        onsite_scalar = -mu
        if dot_strength:
            onsite_scalar += dot_strength * math.exp(-0.5 * (site / dot_sigma) ** 2)
        if disorder is not None:
            onsite_scalar += float(disorder[site])
        onsite = onsite_scalar * S0 + beff * SX
        if impurity_strength and site == num_sites // 2:
            onsite += impurity_strength * SZ

        sl = slice(2 * site, 2 * site + 2)
        h[sl, sl] += onsite

        neighbor = (site + 1) % num_sites
        if site < num_sites - 1 or periodic:
            sr = slice(2 * neighbor, 2 * neighbor + 2)
            factor = -1.0 if (periodic and apbc and site == num_sites - 1) else 1.0
            h[sl, sr] += factor * hop
            h[sr, sl] += factor * hop.conj().T

    pairing = np.zeros_like(h)
    deff = pairing_amplitude(params.delta, phi)
    for site in range(num_sites):
        sl = slice(2 * site, 2 * site + 2)
        pairing[sl, sl] += deff * PAIRING_SPIN

    return np.block([[h, pairing], [pairing.conj().T, -h.conj()]])


def majorana_antisymmetric_matrix(h_bdg: np.ndarray) -> np.ndarray:
    n = h_bdg.shape[0] // 2
    ident = np.eye(n, dtype=complex)
    transform = (1.0 / math.sqrt(2.0)) * np.block(
        [[ident, ident], [-1j * ident, 1j * ident]]
    )
    antisymmetric = -1j * transform @ h_bdg @ transform.conj().T
    return 0.5 * (antisymmetric - antisymmetric.T)


def pfaffian(matrix: np.ndarray) -> complex:
    work = matrix.copy().astype(complex)
    n = work.shape[0]
    pf = 1.0 + 0.0j
    for k in range(0, n - 1, 2):
        pivot = None
        for j in range(k + 1, n):
            if abs(work[k, j]) > 1.0e-12:
                pivot = j
                break
        if pivot is None:
            return 0.0 + 0.0j
        if pivot != k + 1:
            work[[k + 1, pivot], :] = work[[pivot, k + 1], :]
            work[:, [k + 1, pivot]] = work[:, [pivot, k + 1]]
            pf *= -1.0
        pivot_val = work[k, k + 1]
        pf *= pivot_val
        if k + 2 < n:
            rows = slice(k + 2, n)
            update = (
                np.outer(work[k, rows], work[k + 1, rows])
                - np.outer(work[k + 1, rows], work[k, rows])
            ) / pivot_val
            work[rows, rows] -= update
    return pf


def ring_invariant(
    num_sites: int,
    mu: float,
    phi: float,
    params: ModelParams,
    *,
    dot_strength: float = 0.0,
    impurity_strength: float = 0.0,
    disorder: np.ndarray | None = None,
) -> int:
    pf_vals = []
    for apbc in (False, True):
        h_bdg = build_real_space_bdg(
            num_sites,
            mu,
            phi,
            params,
            dot_strength=dot_strength,
            impurity_strength=impurity_strength,
            disorder=disorder,
            periodic=True,
            apbc=apbc,
        )
        pf_vals.append(pfaffian(majorana_antisymmetric_matrix(h_bdg)).real)
    sign = np.sign(pf_vals[0] * pf_vals[1])
    return int(sign) if sign != 0 else 0


def min_bulk_gap(mu: float, phi: float, params: ModelParams, k_values: np.ndarray) -> float:
    min_gap = np.inf
    for k in k_values:
        eigvals = np.linalg.eigvalsh(kspace_bdg(float(k), mu, phi, params))
        min_gap = min(min_gap, float(np.min(np.abs(eigvals))))
    return float(min_gap)


def lowest_modes(
    num_sites: int,
    mu: float,
    phi: float,
    params: ModelParams,
    *,
    dot_strength: float = 0.0,
    impurity_strength: float = 0.0,
    disorder: np.ndarray | None = None,
    num_modes: int = 12,
) -> tuple[np.ndarray, np.ndarray]:
    h_bdg = build_real_space_bdg(
        num_sites,
        mu,
        phi,
        params,
        dot_strength=dot_strength,
        impurity_strength=impurity_strength,
        disorder=disorder,
    )
    eigvals, eigvecs = np.linalg.eigh(h_bdg)
    order = np.argsort(np.abs(eigvals))
    sel = order[:num_modes]
    return eigvals[sel], eigvecs[:, sel]


def mode_profile(eigvec: np.ndarray, num_sites: int) -> np.ndarray:
    electron = eigvec[: 2 * num_sites].reshape(num_sites, 2)
    hole = eigvec[2 * num_sites :].reshape(num_sites, 2)
    weight = np.sum(np.abs(electron) ** 2 + np.abs(hole) ** 2, axis=1)
    return weight / np.sum(weight)


def edge_weight(profile: np.ndarray, edge_sites: int = 6) -> float:
    return float(np.sum(profile[:edge_sites]) + np.sum(profile[-edge_sites:]))


def spectral_isolation(abs_eigvals: np.ndarray) -> float:
    if len(abs_eigvals) < 3:
        return 0.0
    denom = max(abs_eigvals[0], 1.0e-12)
    return float(abs_eigvals[2] / denom)


def lead_gamma_matrices(num_sites: int, gamma: float) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    dim = 4 * num_sites

    def diag(indices: list[int]) -> np.ndarray:
        matrix = np.zeros((dim, dim), dtype=complex)
        for idx in indices:
            matrix[idx, idx] = gamma
        return matrix

    g_le = diag([0, 1])
    g_lh = diag([2 * num_sites, 2 * num_sites + 1])
    g_re = diag([2 * num_sites - 2, 2 * num_sites - 1])
    g_rh = diag([4 * num_sites - 2, 4 * num_sites - 1])
    return g_le, g_lh, g_re, g_rh


def transport_observables(
    num_sites: int,
    mu: float,
    phi: float,
    energy: float,
    params: ModelParams,
    *,
    dot_strength: float = 0.0,
    impurity_strength: float = 0.0,
    disorder: np.ndarray | None = None,
) -> dict[str, float]:
    h_bdg = build_real_space_bdg(
        num_sites,
        mu,
        phi,
        params,
        dot_strength=dot_strength,
        impurity_strength=impurity_strength,
        disorder=disorder,
    )
    g_le, g_lh, g_re, g_rh = lead_gamma_matrices(num_sites, params.gamma_lead)
    sigma = -0.5j * (g_le + g_lh + g_re + g_rh)
    green = np.linalg.inv(
        (energy + 1j * params.eta) * np.eye(h_bdg.shape[0], dtype=complex) - h_bdg - sigma
    )
    green_a = green.conj().T

    t_car = float(np.real(np.trace(g_le @ green @ g_rh @ green_a)))
    t_ec = float(np.real(np.trace(g_le @ green @ g_re @ green_a)))
    r_ar_l = float(np.real(np.trace(g_le @ green @ g_lh @ green_a)))
    r_ar_r = float(np.real(np.trace(g_re @ green @ g_rh @ green_a)))
    r_ee_l = float(np.real(np.trace(g_le @ green @ g_le @ green_a)))
    r_ee_r = float(np.real(np.trace(g_re @ green @ g_re @ green_a)))

    # These are wide-band lead proxies for the source-data stage.
    g_ll_proxy = 2.0 - r_ee_l + r_ar_l + t_car - t_ec
    g_rr_proxy = 2.0 - r_ee_r + r_ar_r + t_car - t_ec

    return {
        "t_car": t_car,
        "t_ec": t_ec,
        "glr_proxy": t_car - t_ec,
        "gll_proxy": g_ll_proxy,
        "grr_proxy": g_rr_proxy,
        "r_ar_left": r_ar_l,
        "r_ar_right": r_ar_r,
        "r_ee_left": r_ee_l,
        "r_ee_right": r_ee_r,
    }


def save_csv(df: pd.DataFrame, path: Path) -> None:
    df.to_csv(path, index=False)


def generate_fig2(config: dict, params: ModelParams) -> dict[str, str]:
    out = DATA_ROOT / "source_data_fig2"
    mu_values = np.linspace(*config["fig2"]["mu_range"], config["fig2"]["mu_points"])
    phi_values = np.linspace(
        config["fig2"]["phi_range"][0] * math.pi,
        config["fig2"]["phi_range"][1] * math.pi,
        config["fig2"]["phi_points"],
    )
    k_values = np.linspace(-math.pi, math.pi, config["fig2"]["k_points"])

    band_rows = []
    for k in np.linspace(-math.pi, math.pi, config["fig2"]["band_k_points"]):
        eigvals = np.linalg.eigvalsh(
            kspace_bdg(float(k), config["fig2"]["band_mu"], config["fig2"]["band_phi"] * math.pi, params)
        )
        for band_index, energy in enumerate(eigvals):
            band_rows.append({"k": k, "band_index": band_index, "energy": float(energy)})
    save_csv(pd.DataFrame(band_rows), out / "fig2a_normal_state_spin_splitting.csv")

    gap_rows = []
    inv_rows = []
    for mu in mu_values:
        for phi in phi_values:
            gap_rows.append(
                {
                    "mu": mu,
                    "phi": phi,
                    "bulk_gap": min_bulk_gap(float(mu), float(phi), params, k_values),
                }
            )
            inv_rows.append(
                {
                    "mu": mu,
                    "phi": phi,
                    "nu_ring": ring_invariant(
                        config["fig2"]["ring_sites"],
                        float(mu),
                        float(phi),
                        params,
                    ),
                }
            )

    save_csv(pd.DataFrame(gap_rows), out / "fig2b_bulk_gap_mu_phi.csv")
    save_csv(pd.DataFrame(inv_rows), out / "fig2c_ring_invariant_mu_phi.csv")

    refined_rows = []
    refined_mu = config["fig2"]["refined_mu"]
    for phi in np.linspace(0.0, 2.0 * math.pi, config["fig2"]["refined_phi_points"]):
        refined_rows.append(
            {
                "phi": phi,
                "bulk_gap": min_bulk_gap(refined_mu, float(phi), params, k_values),
                "nu_ring": ring_invariant(
                    config["fig2"]["ring_sites"],
                    refined_mu,
                    float(phi),
                    params,
                ),
            }
        )
    save_csv(
        pd.DataFrame(refined_rows),
        out / f"fig2d_refined_phi_cut_mu_{str(refined_mu).replace('.', 'p')}.csv",
    )

    return {"fig2_dir": str(out)}


def generate_fig3(config: dict, params: ModelParams) -> dict[str, str]:
    out = DATA_ROOT / "source_data_fig3"
    phi_values = np.linspace(
        config["fig3"]["phi_range"][0] * math.pi,
        config["fig3"]["phi_range"][1] * math.pi,
        config["fig3"]["phi_points"],
    )

    spectrum_rows = []
    metric_rows = []
    for phi in phi_values:
        eigvals, eigvecs = lowest_modes(
            config["fig3"]["chain_sites"],
            config["fig3"]["positive_mu"],
            float(phi),
            params,
            num_modes=config["fig3"]["num_modes"],
        )
        abs_eigs = np.sort(np.abs(eigvals))
        profile = mode_profile(eigvecs[:, 0], config["fig3"]["chain_sites"])
        for idx, energy in enumerate(eigvals):
            spectrum_rows.append({"phi": phi, "mode_index": idx, "energy": float(energy)})
        metric_rows.append(
            {
                "phi": phi,
                "min_abs_energy": float(abs_eigs[0]),
                "spectral_isolation": spectral_isolation(abs_eigs),
                "edge_weight": edge_weight(profile),
                "nu_ring": ring_invariant(
                    config["fig3"]["ring_sites"],
                    config["fig3"]["positive_mu"],
                    float(phi),
                    params,
                ),
            }
        )

    save_csv(pd.DataFrame(spectrum_rows), out / "fig3a_open_boundary_spectrum_vs_phi.csv")
    save_csv(pd.DataFrame(metric_rows), out / "fig3d_isolation_endweight_vs_phi.csv")

    topo_phi = config["fig3"]["topological_snapshot_phi"] * math.pi
    eigvals_topo, eigvecs_topo = lowest_modes(
        config["fig3"]["chain_sites"],
        config["fig3"]["positive_mu"],
        topo_phi,
        params,
        num_modes=config["fig3"]["num_modes"],
    )
    topo_profile = mode_profile(eigvecs_topo[:, 0], config["fig3"]["chain_sites"])
    save_csv(
        pd.DataFrame(
            {
                "site": np.arange(config["fig3"]["chain_sites"]),
                "weight": topo_profile,
                "snapshot_phi": topo_phi,
                "eigenvalue": float(eigvals_topo[0]),
            }
        ),
        out / "fig3b_topological_wavefunction_profile.csv",
    )

    mimic_phi = config["fig3"]["trivial_mimic_phi"] * math.pi
    eigvals_mimic, eigvecs_mimic = lowest_modes(
        config["fig3"]["chain_sites"],
        config["fig3"]["trivial_mu"],
        mimic_phi,
        params,
        dot_strength=config["fig3"]["trivial_dot_strength"],
        num_modes=config["fig3"]["num_modes"],
    )
    mimic_profile = mode_profile(eigvecs_mimic[:, 0], config["fig3"]["chain_sites"])
    save_csv(
        pd.DataFrame(
            {
                "site": np.arange(config["fig3"]["chain_sites"]),
                "weight": mimic_profile,
                "snapshot_phi": mimic_phi,
                "eigenvalue": float(eigvals_mimic[0]),
            }
        ),
        out / "fig3c_trivial_dot_mimic_profile.csv",
    )

    return {"fig3_dir": str(out)}


def generate_fig4(config: dict, params: ModelParams) -> dict[str, str]:
    out = DATA_ROOT / "source_data_fig4"
    chain_sites = config["fig4"]["chain_sites"]
    ring_sites = config["fig4"]["ring_sites"]
    trivial_phi = config["fig4"]["trivial_phi"] * math.pi
    trivial_mu = config["fig4"]["trivial_mu"]

    dot_rows = []
    for dot_strength in np.linspace(*config["fig4"]["dot_range"], config["fig4"]["dot_points"]):
        eigvals, eigvecs = lowest_modes(
            chain_sites,
            trivial_mu,
            trivial_phi,
            params,
            dot_strength=float(dot_strength),
            num_modes=6,
        )
        profile = mode_profile(eigvecs[:, 0], chain_sites)
        dot_rows.append(
            {
                "dot_strength": dot_strength,
                "min_abs_energy": float(np.min(np.abs(eigvals))),
                "edge_weight": edge_weight(profile),
                "nu_ring": ring_invariant(
                    ring_sites,
                    trivial_mu,
                    trivial_phi,
                    params,
                    dot_strength=float(dot_strength),
                ),
            }
        )
    save_csv(pd.DataFrame(dot_rows), out / "fig4a_dot_control_sweep.csv")

    impurity_rows = []
    for impurity_strength in np.linspace(
        *config["fig4"]["impurity_range"], config["fig4"]["impurity_points"]
    ):
        eigvals, eigvecs = lowest_modes(
            chain_sites,
            trivial_mu,
            trivial_phi,
            params,
            impurity_strength=float(impurity_strength),
            num_modes=6,
        )
        profile = mode_profile(eigvecs[:, 0], chain_sites)
        impurity_rows.append(
            {
                "impurity_strength": impurity_strength,
                "min_abs_energy": float(np.min(np.abs(eigvals))),
                "edge_weight": edge_weight(profile),
                "nu_ring": ring_invariant(
                    ring_sites,
                    trivial_mu,
                    trivial_phi,
                    params,
                    impurity_strength=float(impurity_strength),
                ),
            }
        )
    save_csv(pd.DataFrame(impurity_rows), out / "fig4b_impurity_control_sweep.csv")

    disorder_rows = []
    for disorder_strength in config["fig4"]["disorder_strengths"]:
        for seed in range(config["fig4"]["disorder_seeds"]):
            rng = np.random.default_rng(seed)
            disorder = rng.uniform(-disorder_strength / 2.0, disorder_strength / 2.0, chain_sites)
            eigvals, eigvecs = lowest_modes(
                chain_sites,
                trivial_mu,
                trivial_phi,
                params,
                disorder=disorder,
                num_modes=6,
            )
            profile = mode_profile(eigvecs[:, 0], chain_sites)
            disorder_rows.append(
                {
                    "disorder_strength": disorder_strength,
                    "seed": seed,
                    "min_abs_energy": float(np.min(np.abs(eigvals))),
                    "edge_weight": edge_weight(profile),
                    "nu_ring": ring_invariant(
                        ring_sites,
                        trivial_mu,
                        trivial_phi,
                        params,
                        disorder=disorder[:ring_sites],
                    ),
                }
            )
    save_csv(pd.DataFrame(disorder_rows), out / "fig4c_disorder_ensemble.csv")

    summary = pd.DataFrame(
        [
            {
                "case": "positive_control",
                "mu": config["fig4"]["positive_mu"],
                "phi": config["fig4"]["positive_phi"] * math.pi,
                "dot_strength": 0.0,
                "impurity_strength": 0.0,
                "nu_ring": ring_invariant(
                    ring_sites,
                    config["fig4"]["positive_mu"],
                    config["fig4"]["positive_phi"] * math.pi,
                    params,
                ),
            },
            {
                "case": "dot_mimic",
                "mu": trivial_mu,
                "phi": trivial_phi,
                "dot_strength": config["fig4"]["summary_dot_strength"],
                "impurity_strength": 0.0,
                "nu_ring": ring_invariant(
                    ring_sites,
                    trivial_mu,
                    trivial_phi,
                    params,
                    dot_strength=config["fig4"]["summary_dot_strength"],
                ),
            },
            {
                "case": "impurity_mimic",
                "mu": trivial_mu,
                "phi": trivial_phi,
                "dot_strength": 0.0,
                "impurity_strength": config["fig4"]["summary_impurity_strength"],
                "nu_ring": ring_invariant(
                    ring_sites,
                    trivial_mu,
                    trivial_phi,
                    params,
                    impurity_strength=config["fig4"]["summary_impurity_strength"],
                ),
            },
        ]
    )
    save_csv(summary, out / "fig4d_control_summary_table.csv")

    return {"fig4_dir": str(out)}


def generate_fig5(config: dict, params: ModelParams) -> dict[str, str]:
    out = DATA_ROOT / "source_data_fig5"
    chain_sites = config["fig5"]["chain_sites"]
    voltage_values = np.linspace(
        config["fig5"]["voltage_range"][0],
        config["fig5"]["voltage_range"][1],
        config["fig5"]["voltage_points"],
    )
    phi_values = np.linspace(
        config["fig5"]["phi_range"][0] * math.pi,
        config["fig5"]["phi_range"][1] * math.pi,
        config["fig5"]["phi_points"],
    )

    def heatmap_rows(case_name: str, mu: float, dot_strength: float = 0.0, impurity_strength: float = 0.0) -> list[dict]:
        rows = []
        for phi in phi_values:
            for voltage in voltage_values:
                obs = transport_observables(
                    chain_sites,
                    mu,
                    float(phi),
                    float(voltage),
                    params,
                    dot_strength=dot_strength,
                    impurity_strength=impurity_strength,
                )
                rows.append(
                    {
                        "case": case_name,
                        "phi": phi,
                        "voltage": voltage,
                        **obs,
                    }
                )
        return rows

    save_csv(
        pd.DataFrame(heatmap_rows("positive_control", config["fig5"]["positive_mu"])),
        out / "fig5a_positive_transport_heatmap.csv",
    )
    save_csv(
        pd.DataFrame(
            heatmap_rows(
                "dot_mimic",
                config["fig5"]["trivial_mu"],
                dot_strength=config["fig5"]["dot_strength"],
            )
        ),
        out / "fig5b_dot_transport_heatmap.csv",
    )
    save_csv(
        pd.DataFrame(
            heatmap_rows(
                "impurity_mimic",
                config["fig5"]["trivial_mu"],
                impurity_strength=config["fig5"]["impurity_strength"],
            )
        ),
        out / "fig5c_impurity_transport_heatmap.csv",
    )

    robustness_rows = []
    phi_probe = config["fig5"]["robustness_phi"] * math.pi
    for disorder_strength in config["fig5"]["robustness_disorder_strengths"]:
        for seed in range(config["fig5"]["robustness_seeds"]):
            rng = np.random.default_rng(seed)
            disorder = rng.uniform(-disorder_strength / 2.0, disorder_strength / 2.0, chain_sites)
            obs = transport_observables(
                chain_sites,
                config["fig5"]["positive_mu"],
                phi_probe,
                0.0,
                params,
                disorder=disorder,
            )
            robustness_rows.append(
                {
                    "disorder_strength": disorder_strength,
                    "seed": seed,
                    "phi": phi_probe,
                    **obs,
                }
            )
    save_csv(pd.DataFrame(robustness_rows), out / "fig5d_disorder_robustness.csv")

    return {"fig5_dir": str(out)}


def write_manifest(config: dict, params: ModelParams, outputs: dict[str, str]) -> None:
    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": "majorana-diagnostic-natphys",
        "branch": "compensated-magnetic-cmjj",
        "source_data_root": str(DATA_ROOT),
        "script": str(CODE_ROOT / "generate_cmjj_source_data.py"),
        "config": str(CONFIG_PATH),
        "model_params": asdict(params),
        "outputs": outputs,
        "notes": [
            "This source-data package is generated from a minimal 1D effective compensated-magnetic Josephson-junction chain.",
            "Topology maps in Fig. 2 and inhomogeneous control labels in Fig. 4 are both computed numerically rather than inserted by hand.",
            "Transport observables are wide-band lead proxies generated without scipy/matplotlib so the package can be reproduced in the current container.",
        ],
    }
    with (DATA_ROOT / "manifest.json").open("w", encoding="utf-8") as handle:
        json.dump(manifest, handle, indent=2)

    readme = """# CMJJ Source Data Package

This folder contains the first real source-data bundle for Figures 2-5 of the
compensated-magnetic Josephson-junction diagnostic branch.

## Model
- Minimal effective 1D compensated-magnetic Josephson-junction chain
- Momentum-space bulk model for the clean gap scan
- Real-space open chain for boundary spectra and transport
- Ring Pfaffian parity switch (`nu_ring`) for topology labels on finite devices

## Reproduction
Run:

```bash
python /workspace/memory/majorana-diagnostic-natphys/code/generate_cmjj_source_data.py
```

## Notes
- The current runtime does not provide `scipy` or `matplotlib`, so this package
  focuses on source data and metadata rather than rendered figures.
- All CSV files are plain UTF-8 and can be plotted later from the same project
  space once the preferred plotting stack is available.
"""
    (DATA_ROOT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    config = load_config()
    params = ModelParams(**config["model_params"])
    outputs: dict[str, str] = {}
    outputs.update(generate_fig2(config, params))
    outputs.update(generate_fig3(config, params))
    outputs.update(generate_fig4(config, params))
    outputs.update(generate_fig5(config, params))
    write_manifest(config, params, outputs)
    print(f"Wrote source data under {DATA_ROOT}")


if __name__ == "__main__":
    main()
