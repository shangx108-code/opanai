#!/usr/bin/env python3
"""Targeted recomputation for the CMJJ Fig. 4 / Fig. 5 bottleneck.

This script keeps the baseline `generate_cmjj_source_data.py` untouched and
scans only the narrow control windows needed to retune the false-positive
panels. The goal is to find dot and impurity settings that still create local
near-zero mimics while remaining topologically trivial and nonlocal-silent.
"""

from __future__ import annotations

import importlib.util
import math
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path("/workspace/memory/majorana-diagnostic-natphys")
BASELINE_SCRIPT = PROJECT_ROOT / "code" / "generate_cmjj_source_data.py"
OUT_ROOT = PROJECT_ROOT / "data" / "fig4-fig5-targeted-retune-2026-05-01"


def load_baseline_module():
    module_name = "cmjj_targeted_retune"
    spec = importlib.util.spec_from_file_location(module_name, BASELINE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def scan_controls(module) -> pd.DataFrame:
    config = module.load_config()
    params = module.ModelParams(**config["model_params"])

    fig4 = config["fig4"]
    fig5 = config["fig5"]
    trivial_mu = fig4["trivial_mu"]
    chain_sites = fig4["chain_sites"]
    ring_sites = fig4["ring_sites"]
    transport_sites = fig5["chain_sites"]

    dot_phi_fracs = np.linspace(0.16, 0.24, 9)
    dot_strengths = np.linspace(1.7, 2.15, 10)
    impurity_phi_fracs = np.linspace(0.16, 0.24, 9)
    impurity_strengths = np.linspace(2.05, 2.25, 9)

    rows: list[dict[str, float | str | int]] = []

    def append_case(kind: str, phi_frac: float, strength: float) -> None:
        phi = float(phi_frac * math.pi)
        kwargs = {"dot_strength": strength} if kind == "dot" else {"impurity_strength": strength}
        eigvals, eigvecs = module.lowest_modes(
            chain_sites,
            trivial_mu,
            phi,
            params,
            num_modes=6,
            **kwargs,
        )
        profile = module.mode_profile(eigvecs[:, 0], chain_sites)
        nu_ring = module.ring_invariant(
            ring_sites,
            trivial_mu,
            phi,
            params,
            **kwargs,
        )
        obs0 = module.transport_observables(
            transport_sites,
            trivial_mu,
            phi,
            0.0,
            params,
            **kwargs,
        )
        obs13 = module.transport_observables(
            transport_sites,
            trivial_mu,
            phi,
            0.13,
            params,
            **kwargs,
        )
        rows.append(
            {
                "kind": kind,
                "phi_frac_pi": phi_frac,
                "phi": phi,
                "strength": strength,
                "min_abs_energy": float(np.min(np.abs(eigvals))),
                "edge_weight": module.edge_weight(profile),
                "nu_ring": nu_ring,
                "glr_zero_bias": obs0["glr_proxy"],
                "gll_zero_bias": obs0["gll_proxy"],
                "glr_probe_0p13": obs13["glr_proxy"],
                "gll_probe_0p13": obs13["gll_proxy"],
                "grr_probe_0p13": obs13["grr_proxy"],
            }
        )

    for phi_frac in dot_phi_fracs:
        for strength in dot_strengths:
            append_case("dot", float(phi_frac), float(strength))

    for phi_frac in impurity_phi_fracs:
        for strength in impurity_strengths:
            append_case("impurity", float(phi_frac), float(strength))

    return pd.DataFrame(rows)


def rank_candidates(df: pd.DataFrame) -> pd.DataFrame:
    candidates = df[(df["nu_ring"] == 1) & (df["min_abs_energy"] < 0.03)].copy()
    candidates["abs_glr_probe_0p13"] = candidates["glr_probe_0p13"].abs()
    candidates["nonlocal_local_ratio"] = (
        candidates["abs_glr_probe_0p13"] / candidates["gll_probe_0p13"].abs().clip(lower=1.0e-12)
    )
    candidates["score"] = (
        candidates["min_abs_energy"]
        + 0.25 * candidates["abs_glr_probe_0p13"]
        + 0.05 * candidates["nonlocal_local_ratio"]
    )
    return candidates.sort_values(["kind", "score", "min_abs_energy", "abs_glr_probe_0p13"]).reset_index(drop=True)


def write_summary(candidates: pd.DataFrame) -> None:
    top_dot = candidates[candidates["kind"] == "dot"].head(3)
    top_impurity = candidates[candidates["kind"] == "impurity"].head(3)

    lines = [
        "# Fig. 4 / Fig. 5 Targeted Retune Summary",
        "",
        "Objective: preserve misleading local near-zero structure in the controls while restoring",
        "a clearly trivial topology label and strongly suppressed nonlocal signal.",
        "",
        "## Decision",
        "- Dot control can be kept trivial while remaining near-zero by moving to the lower-phi side of the old sweep.",
        "- Impurity control also has a trivial near-zero window, but it sits on a narrower ridge than the dot case.",
        "- The next Fig. 4 / Fig. 5 rebuild should use one dot candidate and one impurity candidate from this table rather than the old first-pass settings.",
        "",
        "## Top dot candidates",
    ]

    for _, row in top_dot.iterrows():
        lines.append(
            f"- phi/pi={row['phi_frac_pi']:.3f}, dot_strength={row['strength']:.3f}, "
            f"min|E|={row['min_abs_energy']:.6f}, nu_ring={int(row['nu_ring'])}, "
            f"|GLR|(V=0.13)={row['abs_glr_probe_0p13']:.6e}, GLL(V=0.13)={row['gll_probe_0p13']:.6f}"
        )

    lines.extend(["", "## Top impurity candidates"])
    for _, row in top_impurity.iterrows():
        lines.append(
            f"- phi/pi={row['phi_frac_pi']:.3f}, impurity_strength={row['strength']:.3f}, "
            f"min|E|={row['min_abs_energy']:.6f}, nu_ring={int(row['nu_ring'])}, "
            f"|GLR|(V=0.13)={row['abs_glr_probe_0p13']:.6e}, GLL(V=0.13)={row['gll_probe_0p13']:.6f}"
        )

    lines.extend(
        [
            "",
            "## Recommended next rebuild settings",
            "- Dot mimic candidate: use the best-ranked dot row from `candidate_controls.csv`.",
            "- Impurity mimic candidate: use the best-ranked impurity row from `candidate_controls.csv`.",
            "- Recompute only Fig. 4 summary rows and Fig. 5 heatmaps around those candidates before any plotting or caption updates.",
        ]
    )

    (OUT_ROOT / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    module = load_baseline_module()
    full_scan = scan_controls(module)
    candidates = rank_candidates(full_scan)

    full_scan.to_csv(OUT_ROOT / "full_scan.csv", index=False)
    candidates.to_csv(OUT_ROOT / "candidate_controls.csv", index=False)
    write_summary(candidates)

    print(f"Wrote targeted retune outputs under {OUT_ROOT}")


if __name__ == "__main__":
    main()
