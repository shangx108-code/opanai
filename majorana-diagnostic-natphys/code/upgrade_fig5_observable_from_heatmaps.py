#!/usr/bin/env python3
"""Derive upgraded Fig. 5 observables from the candidate-rebuild heatmaps.

This keeps the transport solver fixed and upgrades only the readout layer.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path("/workspace/memory/majorana-diagnostic-natphys")
INPUT_ROOT = PROJECT_ROOT / "data" / "fig4-fig5-candidate-rebuild-2026-05-01"
OUT_ROOT = PROJECT_ROOT / "data" / "fig5-observable-upgrade-2026-05-01"

INPUT_FILES = {
    "positive": "fig5a_positive_transport_heatmap.csv",
    "dot": "fig5b_dot_candidate_transport_heatmap.csv",
    "impurity": "fig5c_impurity_candidate_transport_heatmap.csv",
}


def add_observables(df: pd.DataFrame) -> pd.DataFrame:
    eps = 1.0e-12
    out = df.copy()
    out["abs_glr"] = out["glr_proxy"].abs()
    out["nonlocal_fraction_maxlocal"] = out["abs_glr"] / (
        out[["gll_proxy", "grr_proxy"]].abs().max(axis=1) + eps
    )
    out["symmetric_nonlocal_score"] = (
        out["abs_glr"]
        * np.sqrt(np.clip(out["gll_proxy"], 0.0, None) * np.clip(out["grr_proxy"], 0.0, None))
        / (out["gll_proxy"].abs() + out["grr_proxy"].abs() + eps)
    )
    out["nonlocal_fraction_sum"] = out["abs_glr"] / (
        out["gll_proxy"].abs() + out["grr_proxy"].abs() + eps
    )
    return out


def summarize_metric(name: str, metric: str, datasets: dict[str, pd.DataFrame]) -> dict[str, float | str]:
    pos = datasets["positive"][metric]
    dot = datasets["dot"][metric]
    impurity = datasets["impurity"][metric]
    return {
        "metric": name,
        "positive_max": float(pos.max()),
        "dot_max": float(dot.max()),
        "impurity_max": float(impurity.max()),
        "positive_median": float(pos.median()),
        "dot_median": float(dot.median()),
        "impurity_median": float(impurity.median()),
        "positive_dot_max_ratio": float(pos.max() / max(dot.max(), 1.0e-15)),
        "positive_impurity_max_ratio": float(pos.max() / max(impurity.max(), 1.0e-15)),
        "positive_dot_median_ratio": float(pos.median() / max(dot.median(), 1.0e-15)),
        "positive_impurity_median_ratio": float(pos.median() / max(impurity.median(), 1.0e-15)),
    }


def write_summary(selection: pd.DataFrame) -> None:
    top = selection.iloc[0]
    text = f"""# Fig. 5 Observable Upgrade

This folder upgrades only the Fig. 5 readout layer while keeping the candidate
heatmaps and transport solver fixed.

## Selected observable

- Primary upgraded observable: `{top['metric']}`

## Why it was selected

- It gave the strongest worst-case full-bias median separation across the two
  control families among the tested readouts.
- For `{top['metric']}`, the positive/control median ratios are:
  - positive/dot = {top['positive_dot_median_ratio']:.3f}
  - positive/impurity = {top['positive_impurity_median_ratio']:.3f}
- The worst of those two ratios is `{min(float(top['positive_dot_median_ratio']), float(top['positive_impurity_median_ratio'])):.3f}`.

## Interpretation

- The upgraded observable suppresses broad-bias leakage better than raw
  `|G_LR|`.
- This is a readout-layer upgrade, not a new transport simulation.

## Files

- `observable_selection_table.csv`
- `fig5a_positive_observable_heatmap.csv`
- `fig5b_dot_candidate_observable_heatmap.csv`
- `fig5c_impurity_candidate_observable_heatmap.csv`
"""
    (OUT_ROOT / "summary.md").write_text(text, encoding="utf-8")


def main() -> None:
    OUT_ROOT.mkdir(parents=True, exist_ok=True)

    datasets = {
        key: add_observables(pd.read_csv(INPUT_ROOT / filename))
        for key, filename in INPUT_FILES.items()
    }

    metric_map = {
        "nonlocal_fraction_maxlocal": "nonlocal_fraction_maxlocal",
        "symmetric_nonlocal_score": "symmetric_nonlocal_score",
        "nonlocal_fraction_sum": "nonlocal_fraction_sum",
        "abs_glr": "abs_glr",
    }

    selection = pd.DataFrame(
        [summarize_metric(name, column, datasets) for name, column in metric_map.items()]
    )
    selection["worst_case_median_ratio"] = selection[
        ["positive_dot_median_ratio", "positive_impurity_median_ratio"]
    ].min(axis=1)
    selection["worst_case_max_ratio"] = selection[
        ["positive_dot_max_ratio", "positive_impurity_max_ratio"]
    ].min(axis=1)
    selection = selection.sort_values(
        ["worst_case_median_ratio", "worst_case_max_ratio"], ascending=False
    ).reset_index(drop=True)
    selection.to_csv(OUT_ROOT / "observable_selection_table.csv", index=False)

    primary_metric = str(selection.iloc[0]["metric"])
    metric_column = metric_map[primary_metric]

    for key, df in datasets.items():
        cols = [
            "case",
            "phi",
            "phi_frac_pi",
            "voltage",
            metric_column,
            "abs_glr",
            "gll_proxy",
            "grr_proxy",
            "glr_proxy",
        ]
        renamed = df[cols].rename(columns={metric_column: "observable"})
        renamed.to_csv(OUT_ROOT / f"{INPUT_FILES[key].replace('_transport_heatmap', '_observable_heatmap')}", index=False)

    manifest = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_root": str(INPUT_ROOT),
        "output_root": str(OUT_ROOT),
        "tested_observables": list(metric_map.keys()),
        "selected_observable": primary_metric,
    }
    (OUT_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    write_summary(selection)
    print(f"Wrote observable-upgrade outputs under {OUT_ROOT}")


if __name__ == "__main__":
    main()
