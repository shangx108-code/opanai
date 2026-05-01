#!/usr/bin/env python3
"""Rebuild Fig. 4 summary rows and Fig. 5 heatmaps from locked candidate controls."""

from __future__ import annotations

import importlib.util
import json
import math
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path("/workspace/memory/majorana-diagnostic-natphys")
BASELINE_SCRIPT = PROJECT_ROOT / "code" / "generate_cmjj_source_data.py"
CANDIDATE_TABLE = (
    PROJECT_ROOT / "data" / "fig4-fig5-targeted-retune-2026-05-01" / "candidate_controls.csv"
)
OUT_ROOT = PROJECT_ROOT / "data" / "fig4-fig5-candidate-rebuild-2026-05-01"


def load_baseline_module():
    module_name = "cmjj_candidate_rebuild"
    spec = importlib.util.spec_from_file_location(module_name, BASELINE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def choose_candidates(candidates: pd.DataFrame) -> tuple[pd.Series, pd.Series]:
    dot = candidates[candidates["kind"] == "dot"].iloc[0]
    impurity = candidates[candidates["kind"] == "impurity"].iloc[0]
    return dot, impurity


def build_fig4_summary(module, config: dict, params, dot: pd.Series, impurity: pd.Series) -> pd.DataFrame:
    fig4 = config["fig4"]
    ring_sites = fig4["ring_sites"]
    rows = [
        {
            "case": "positive_control",
            "mu": fig4["positive_mu"],
            "phi_frac_pi": fig4["positive_phi"],
            "phi": fig4["positive_phi"] * math.pi,
            "dot_strength": 0.0,
            "impurity_strength": 0.0,
            "nu_ring": module.ring_invariant(
                ring_sites,
                fig4["positive_mu"],
                fig4["positive_phi"] * math.pi,
                params,
            ),
        },
        {
            "case": "dot_candidate",
            "mu": fig4["trivial_mu"],
            "phi_frac_pi": float(dot["phi_frac_pi"]),
            "phi": float(dot["phi"]),
            "dot_strength": float(dot["strength"]),
            "impurity_strength": 0.0,
            "nu_ring": module.ring_invariant(
                ring_sites,
                fig4["trivial_mu"],
                float(dot["phi"]),
                params,
                dot_strength=float(dot["strength"]),
            ),
        },
        {
            "case": "impurity_candidate",
            "mu": fig4["trivial_mu"],
            "phi_frac_pi": float(impurity["phi_frac_pi"]),
            "phi": float(impurity["phi"]),
            "dot_strength": 0.0,
            "impurity_strength": float(impurity["strength"]),
            "nu_ring": module.ring_invariant(
                ring_sites,
                fig4["trivial_mu"],
                float(impurity["phi"]),
                params,
                impurity_strength=float(impurity["strength"]),
            ),
        },
    ]
    return pd.DataFrame(rows)


def heatmap_rows(module, config: dict, params, *, case_name: str, mu: float, phi_values, voltage_values, dot_strength: float = 0.0, impurity_strength: float = 0.0):
    rows = []
    for phi in phi_values:
        for voltage in voltage_values:
            obs = module.transport_observables(
                config["fig5"]["chain_sites"],
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
                    "phi": float(phi),
                    "phi_frac_pi": float(phi / math.pi),
                    "voltage": float(voltage),
                    **obs,
                }
            )
    return pd.DataFrame(rows)


def write_summary(dot: pd.Series, impurity: pd.Series) -> None:
    text = f"""# Fig. 4 / Fig. 5 Candidate Rebuild

Locked control candidates used in this rebuild:

- Dot candidate: phi/pi={float(dot['phi_frac_pi']):.3f}, dot_strength={float(dot['strength']):.3f}, min|E|={float(dot['min_abs_energy']):.6f}
- Impurity candidate: phi/pi={float(impurity['phi_frac_pi']):.3f}, impurity_strength={float(impurity['strength']):.3f}, min|E|={float(impurity['min_abs_energy']):.6f}

Outputs in this folder:

- `fig4d_control_summary_table.csv`
- `fig5a_positive_transport_heatmap.csv`
- `fig5b_dot_candidate_transport_heatmap.csv`
- `fig5c_impurity_candidate_transport_heatmap.csv`
- `manifest.json`
"""
    (OUT_ROOT / "summary.md").write_text(text, encoding="utf-8")


def main() -> None:
    os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    os.environ.setdefault("MKL_NUM_THREADS", "1")

    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    module = load_baseline_module()
    config = module.load_config()
    params = module.ModelParams(**config["model_params"])

    candidates = pd.read_csv(CANDIDATE_TABLE)
    dot, impurity = choose_candidates(candidates)

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

    fig4_summary = build_fig4_summary(module, config, params, dot, impurity)
    fig4_summary.to_csv(OUT_ROOT / "fig4d_control_summary_table.csv", index=False)

    positive = heatmap_rows(
        module,
        config,
        params,
        case_name="positive_control",
        mu=config["fig5"]["positive_mu"],
        phi_values=phi_values,
        voltage_values=voltage_values,
    )
    dot_heatmap = heatmap_rows(
        module,
        config,
        params,
        case_name="dot_candidate",
        mu=config["fig5"]["trivial_mu"],
        phi_values=phi_values,
        voltage_values=voltage_values,
        dot_strength=float(dot["strength"]),
    )
    impurity_heatmap = heatmap_rows(
        module,
        config,
        params,
        case_name="impurity_candidate",
        mu=config["fig5"]["trivial_mu"],
        phi_values=phi_values,
        voltage_values=voltage_values,
        impurity_strength=float(impurity["strength"]),
    )

    positive.to_csv(OUT_ROOT / "fig5a_positive_transport_heatmap.csv", index=False)
    dot_heatmap.to_csv(OUT_ROOT / "fig5b_dot_candidate_transport_heatmap.csv", index=False)
    impurity_heatmap.to_csv(OUT_ROOT / "fig5c_impurity_candidate_transport_heatmap.csv", index=False)

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_candidate_table": str(CANDIDATE_TABLE),
        "baseline_script": str(BASELINE_SCRIPT),
        "output_root": str(OUT_ROOT),
        "dot_candidate": {
            "phi_frac_pi": float(dot["phi_frac_pi"]),
            "phi": float(dot["phi"]),
            "strength": float(dot["strength"]),
        },
        "impurity_candidate": {
            "phi_frac_pi": float(impurity["phi_frac_pi"]),
            "phi": float(impurity["phi"]),
            "strength": float(impurity["strength"]),
        },
        "outputs": [
            "fig4d_control_summary_table.csv",
            "fig5a_positive_transport_heatmap.csv",
            "fig5b_dot_candidate_transport_heatmap.csv",
            "fig5c_impurity_candidate_transport_heatmap.csv",
            "summary.md",
        ],
    }
    (OUT_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_summary(dot, impurity)
    print(f"Wrote candidate rebuild outputs under {OUT_ROOT}")


if __name__ == "__main__":
    main()
