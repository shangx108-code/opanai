from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = ROOT / "results" / "e5_e8_package_2026-05-02"
WP1_PATH = ROOT / "results" / "wp1_summary.json"
WP2_PATH = ROOT / "results" / "wp2_edge_proxy.csv"
ALPHA_META_PATH = ROOT / "results" / "alpha_btk_correlation_2026-05-02" / "metadata.json"
ROBUSTNESS_PATH = (
    Path("/workspace/memory/twse2-andreev-prl/data")
    / "btk-generalized-valley-resolved-semi-infinite-2026-04-29"
    / "robustness_summary.csv"
)


def ensure_dirs() -> None:
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def build_metric_atlas(
    wp1_summary: dict[str, object],
    wp2_df: pd.DataFrame,
    robustness_df: pd.DataFrame,
    alpha_meta: dict[str, object],
) -> tuple[list[list[object]], dict[str, float]]:
    inner_scale = float(wp1_summary["inferred_inner_scale"])
    outer_scale = float(wp1_summary["inferred_outer_scale"])
    outer_inner_ratio = outer_scale / inner_scale

    wp2_lookup = wp2_df.set_index(["candidate", "eta"])
    s_wave_eta1 = float(wp2_lookup.loc[("s_wave", 1.0), "avg_frustration"])
    spm_eta1 = float(wp2_lookup.loc[("s_pm", 1.0), "avg_frustration"])
    chiral_eta1 = float(wp2_lookup.loc[("chiral", 1.0), "avg_frustration"])

    s_wave_slices = robustness_df[robustness_df["pairing"] == "s_wave"]
    monotonic_flags: list[bool] = []
    for (_, _, eta_mev), group in s_wave_slices.groupby(["model", "valley", "eta_meV"], sort=True):
        ordered = group.sort_values("barrier_Z")
        values = ordered["peak_minus_background"].tolist()
        monotonic_flags.append(all(values[idx + 1] <= values[idx] + 1e-12 for idx in range(len(values) - 1)))
    s_wave_monotonic_fraction = sum(monotonic_flags) / len(monotonic_flags)

    compressed_v3_total_eta05 = robustness_df[
        (robustness_df["model"] == "compressed_v3")
        & (robustness_df["valley"] == "total")
        & (robustness_df["eta_meV"] == 0.5)
        & (robustness_df["pairing"] == "s_wave")
    ].sort_values("barrier_Z")
    z0_peak = float(compressed_v3_total_eta05.iloc[0]["peak_minus_background"])
    z2_peak = float(compressed_v3_total_eta05.iloc[-1]["peak_minus_background"])
    z2_over_z0 = z2_peak / z0_peak

    figure_meta = alpha_meta["figure_meta"]
    best_alpha_btk_r = float(figure_meta["best_pearson_r"])
    best_alpha_btk_rho = float(figure_meta["best_spearman_rho"])

    rows = [
        ["outer_inner_ratio", outer_inner_ratio, "WP1", "> 1 indicates a two-scale regime is present before AR selectivity is tested."],
        ["s_wave_eta1_avg_frustration", s_wave_eta1, "WP2", "Ordinary same-sign reference should stay near zero in the interface-sign proxy."],
        ["s_pm_eta1_avg_frustration", spm_eta1, "WP2", "Intervalley sign-changing proxy activates strongly when eta -> 1."],
        ["chiral_eta1_avg_frustration", chiral_eta1, "WP2", "Phase-winding proxy retains finite boundary frustration even without intervalley activation."],
        ["s_wave_peak_contrast_monotonic_fraction_vs_Z", s_wave_monotonic_fraction, "semi-infinite BTK", "Fraction of s-wave slices with strictly monotonic decreasing peak contrast as Z increases."],
        ["s_wave_peak_contrast_z2_over_z0_eta0p5", z2_over_z0, "semi-infinite BTK", "Compressed-V3 total-response suppression ratio between Z=2 and Z=0 at eta=0.5 meV."],
        ["best_alpha_btk_peak_contrast_r", best_alpha_btk_r, "alpha-BTK package", "Largest-magnitude compressed-V3 total peak-contrast Pearson correlation within the chosen eta_mix panel."],
        ["best_alpha_btk_peak_contrast_rho", best_alpha_btk_rho, "alpha-BTK package", "Matched Spearman rank correlation for the highlighted alpha-BTK slice."],
        ["xi_ar", "pending", "E4 follow-up", "Need low-barrier AR scan on the same parameter family to certify inner-gap selectivity."],
        ["A_phi", "pending", "future phi scan", "Need explicit phi-dependent conductance to quantify angular anisotropy."],
        ["S_split", "pending", "future phi scan", "Need low-energy peak splitting or critical-closing scan to define the split-scale metric."],
    ]
    metrics = {
        "outer_inner_ratio": outer_inner_ratio,
        "s_wave_eta1": s_wave_eta1,
        "spm_eta1": spm_eta1,
        "chiral_eta1": chiral_eta1,
        "s_wave_monotonic_fraction": s_wave_monotonic_fraction,
        "z2_over_z0": z2_over_z0,
        "best_alpha_btk_r": best_alpha_btk_r,
        "best_alpha_btk_rho": best_alpha_btk_rho,
    }
    return rows, metrics


def build_failure_map(metrics: dict[str, float]) -> list[list[object]]:
    return [
        [
            "inner_gap_tracking",
            "same parameter family must make AR follow the inner gap rather than the outer feature",
            "two-scale prerequisite exists (outer/inner ratio > 1), but Xi_AR is not yet computed",
            "not yet tested",
            "blocked",
            "run low-barrier AR scans on the WP1 parameter family and compute Xi_AR",
        ],
        [
            "orientation_selectivity",
            "ordinary same-sign s-wave should fail if strong alpha/phi selectivity is required",
            "current interface-sign proxy keeps s-wave frustration at numerical zero, but no explicit alpha-form-factor conductance scan exists yet",
            "smooth reference only",
            "blocked",
            "add alpha-resolved conductance or explicit interface form factor before claiming orientation exclusion",
        ],
        [
            "barrier_nonmonotonicity",
            "ordinary same-sign s-wave should fail if the target response requires nonmonotonic peak contrast vs Z",
            f"current semi-infinite BTK package gives monotonic decreasing s-wave peak contrast on 100% of tested slices; Z=2/Z=0 suppression at eta=0.5 meV is {metrics['z2_over_z0']:.3f}",
            "monotonic decreasing baseline",
            "ready as negative control",
            "use once a target nonmonotonic experimental or model-side curve is established",
        ],
        [
            "phi_dependent_peak_response",
            "ordinary same-sign s-wave should fail if low-energy peaks split, enhance, or close critically under phi rotation",
            "phi-resolved conductance is not yet in the current package",
            "not yet tested",
            "blocked",
            "add phi scan before using this branch in the exclusion claim",
        ],
    ]


def write_decision_tree(metrics: dict[str, float]) -> str:
    return f"""# E6 decision tree status

## Active branches from the current package

1. Two-scale prerequisite:
   `outer/inner = {metrics['outer_inner_ratio']:.2f}` from WP1, so the project is already in a regime where inner-gap selectivity is meaningful once AR is scanned on the same parameter family.

2. Ordinary same-sign interface baseline:
   the WP2 proxy keeps `s_wave` frustration at `{metrics['s_wave_eta1']:.3e}` even at `eta=1`, while `s_pm` rises to `{metrics['spm_eta1']:.3f}` and `chiral` stays finite at `{metrics['chiral_eta1']:.3f}`. The current proxy therefore already separates a smooth same-sign reference from unconventional families at the sign-screening level.

3. Barrier-response negative control:
   the current semi-infinite BTK package yields monotonic decreasing `s_wave` peak contrast on all tested slices (`fraction = {metrics['s_wave_monotonic_fraction']:.2f}`). This means any future nonmonotonic target curve can be used immediately as an exclusion branch against ordinary same-sign behavior.

4. Family-ordering side constraint:
   the current alpha-BTK package reaches its strongest compressed-V3 total-response ordering at `r = {metrics['best_alpha_btk_r']:.3f}` and `rho = {metrics['best_alpha_btk_rho']:.3f}`. This is strong enough to keep as an ordering-level side constraint, but still too weak to describe as a direct alpha-resolved closure.

## Pending branches before the full PRL atlas

- `Xi_AR`: still missing. This is the next hard gate for turning the two-scale WP1 result into a pairing-sensitive transport claim.
- `A_phi`: still missing. This branch is required before claiming strong angular selectivity.
- `S_split`: still missing. This branch is required before claiming field-angle-controlled splitting or critical closing.

## Current decision rule

Use the present package only for the following bounded statement:

> the current minimal engine already isolates a smooth ordinary same-sign baseline,
> identifies unconventional sign-sensitive families at the interface-proxy level,
> and provides a moderate ordering-level alpha-BTK constraint.

Do not yet use it to claim a full decision tree for pairing identification.
"""


def write_prl_gate(metrics: dict[str, float]) -> str:
    return f"""# E7 PRL gate sheet

## Gate 1: new diagnostic rather than another pairing catalog
- Status: partial
- Evidence: the project already combines WP1 two-scale calibration, WP2 interface-sign screening, and an alpha-BTK ordering package.
- Remaining blocker: the decision tree is not yet complete until `Xi_AR`, `A_phi`, and `S_split` are computed on the same parameter family.

## Gate 2: explicit inner-gap selectivity argument
- Status: partial
- Evidence: WP1 already gives a two-scale regime with `outer/inner = {metrics['outer_inner_ratio']:.2f}`.
- Remaining blocker: no low-barrier AR scan has yet shown `E_AR` tracking the inner scale instead of the outer feature.

## Gate 3: ordinary same-sign s-wave excluded by one parameter family
- Status: blocked
- Evidence: the current package already locks in an ordinary same-sign smooth baseline and a monotonic-Z negative control.
- Remaining blocker: the same parameter family has not yet been pushed through the full set of four exclusion axes (`Xi_AR`, orientation, Z, phi`).

## Gate 4: broad-audience experimental atlas
- Status: partial
- Evidence: the current package supports a bounded decision-tree preprint layer, not yet a submission-grade atlas.
- Remaining blocker: explicit phi-resolved and AR-selectivity metrics are still missing.

## Current journal judgment

At its present state, the package is already stronger than a generic pairing catalog,
but it is not yet sufficient for the full PRL claim. The project is closest to a
PRL-ready route only if the next quantitative turn closes `Xi_AR` first and then
adds at least one explicit phi branch.
"""


def write_manuscript_scaffold() -> str:
    return """# E8 manuscript scaffold

## Abstract-level sentence

We develop a phase-sensitive transport workflow for twisted bilayer WSe2 that
separates a smooth ordinary same-sign baseline from sign-sensitive unconventional
families, while keeping the present alpha-BTK package explicitly at the level of
an ordering constraint rather than a direct alpha-resolved conductance closure.

## Figure map

### Figure 1: model and candidate space
- Use: WP1 normal-plus-correlated background plus WP2 candidate library.
- Current status: ready for a theory schematic and bounded candidate paragraph.

### Figure 2: tunnelling vs AR selectivity
- Use: WP1 two-scale calibration.
- Current status: only the high-barrier / DOS side is ready.
- Missing: low-barrier AR scan and `Xi_AR`.

### Figure 3: alpha-Z-phi transport fingerprints
- Use: semi-infinite BTK package plus alpha-BTK ordering panel.
- Current status: Z-side negative control and ordering-level side constraint are available.
- Missing: phi-dependent branch and explicit alpha form factor.

### Figure 4: decision tree and s-wave failure map
- Use: E5 failure-map package plus E6 decision-tree package.
- Current status: manuscript logic is ready in bounded form.
- Missing: enough quantitative branches to upgrade the map from “pre-PRL gate sheet” to “submission-grade atlas”.

## Result-section order

1. establish the two-scale regime from WP1 without overselling AR selectivity
2. show that the interface-sign proxy separates ordinary same-sign from unconventional families
3. introduce the alpha-BTK package only as an ordering-level side constraint
4. present the s-wave failure map as a structured exclusion program, not as an already completed proof

## Writing boundary

- Do not claim direct microscopic pairing identification yet.
- Do not write that ordinary same-sign s-wave is already excluded on all four axes.
- It is safe to say that the current package has fixed the negative-control logic,
  the ordering-constraint language, and the next quantitative gate.
"""


def main() -> None:
    ensure_dirs()

    wp1_summary = json.loads(WP1_PATH.read_text(encoding="utf-8"))
    wp2_df = pd.read_csv(WP2_PATH)
    robustness_df = pd.read_csv(ROBUSTNESS_PATH)
    alpha_meta = json.loads(ALPHA_META_PATH.read_text(encoding="utf-8"))

    metric_rows, metrics = build_metric_atlas(wp1_summary, wp2_df, robustness_df, alpha_meta)
    failure_rows = build_failure_map(metrics)
    decision_tree = write_decision_tree(metrics)
    prl_gate = write_prl_gate(metrics)
    manuscript_scaffold = write_manuscript_scaffold()

    write_csv(
        RESULTS_ROOT / "e5_swave_failure_map.csv",
        ["axis", "target_requirement", "current_evidence", "ordinary_swave_status", "status", "next_blocker"],
        failure_rows,
    )
    write_csv(
        RESULTS_ROOT / "e6_metric_atlas.csv",
        ["metric", "value", "source", "meaning"],
        metric_rows,
    )
    (RESULTS_ROOT / "e6_decision_tree.md").write_text(decision_tree, encoding="utf-8")
    (RESULTS_ROOT / "e7_prl_gate.md").write_text(prl_gate, encoding="utf-8")
    (RESULTS_ROOT / "e8_manuscript_scaffold.md").write_text(manuscript_scaffold, encoding="utf-8")

    manifest = {
        "package": "e5_e8_package_2026-05-02",
        "inputs": {
            "wp1_summary": str(WP1_PATH),
            "wp2_edge_proxy": str(WP2_PATH),
            "alpha_btk_metadata": str(ALPHA_META_PATH),
            "btk_robustness_summary": str(ROBUSTNESS_PATH),
        },
        "key_metrics": metrics,
        "outputs": [
            "e5_swave_failure_map.csv",
            "e6_metric_atlas.csv",
            "e6_decision_tree.md",
            "e7_prl_gate.md",
            "e8_manuscript_scaffold.md",
        ],
    }
    (RESULTS_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    summary = f"""# E5-E8 package summary

- E5 failure map written to `e5_swave_failure_map.csv`
- E6 metric atlas written to `e6_metric_atlas.csv`
- E6 decision tree written to `e6_decision_tree.md`
- E7 PRL gate sheet written to `e7_prl_gate.md`
- E8 manuscript scaffold written to `e8_manuscript_scaffold.md`

## Key metrics

- outer/inner ratio: {metrics['outer_inner_ratio']:.2f}
- s-wave eta=1 avg frustration: {metrics['s_wave_eta1']:.3e}
- s_pm eta=1 avg frustration: {metrics['spm_eta1']:.3f}
- chiral eta=1 avg frustration: {metrics['chiral_eta1']:.3f}
- s-wave monotonic-Z fraction: {metrics['s_wave_monotonic_fraction']:.2f}
- best alpha-BTK peak correlation r: {metrics['best_alpha_btk_r']:.3f}
"""
    (RESULTS_ROOT / "summary.md").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    main()
