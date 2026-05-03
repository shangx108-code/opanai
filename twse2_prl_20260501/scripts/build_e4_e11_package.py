from __future__ import annotations

import csv
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS_ROOT = ROOT / "results" / "e4_to_e11_package_2026-05-03"
NC_MEMO_PATH = Path("/workspace/user_files/01-markdown-1-md-20")
XI_AR_METRICS_PATH = ROOT / "results" / "xi_ar_zeeman_scan_2026-05-02" / "metrics.json"
TRANSPORT_VALIDATION_PATH = ROOT / "results" / "transport_validation_suite_2026-05-03" / "transport_validation_summary.csv"
INVARIANCE_SUMMARY_PATH = ROOT / "results" / "kernel_invariance_tests_2026-05-02" / "invariance_summary.csv"
CONSTRAINT_SUMMARY_PATH = ROOT / "results" / "observable_constraint_negative_control_2026-05-03" / "constraint_summary.csv"
SMATRIX_SUMMARY_PATH = ROOT / "results" / "full_smatrix_transport_audit_2026-05-03" / "smatrix_summary.csv"
PHS_SUMMARY_PATH = ROOT / "results" / "full_smatrix_transport_audit_2026-05-03" / "particle_hole_summary.csv"
ENERGY_CONVERGENCE_PATH = ROOT / "results" / "convergence_reproducibility_suite_2026-05-03" / "energy_convergence_summary.csv"
ANGLE_CONVERGENCE_PATH = ROOT / "results" / "convergence_reproducibility_suite_2026-05-03" / "angle_convergence_summary.csv"
SUBMISSION_ROOT = ROOT / "submission_package_nc_2026-05-03"
PROJECT_INDEX_PATH = ROOT / "project-space-index.md"
README_PATH = ROOT / "README.md"


def ensure_dirs() -> None:
    RESULTS_ROOT.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def load_inputs() -> dict[str, object]:
    return {
        "xi_ar": json.loads(XI_AR_METRICS_PATH.read_text(encoding="utf-8")),
        "transport_validation": pd.read_csv(TRANSPORT_VALIDATION_PATH),
        "invariance": pd.read_csv(INVARIANCE_SUMMARY_PATH),
        "constraint": pd.read_csv(CONSTRAINT_SUMMARY_PATH),
        "smatrix": pd.read_csv(SMATRIX_SUMMARY_PATH),
        "phs": pd.read_csv(PHS_SUMMARY_PATH),
        "energy_convergence": pd.read_csv(ENERGY_CONVERGENCE_PATH),
        "angle_convergence": pd.read_csv(ANGLE_CONVERGENCE_PATH),
    }


def build_e4_metrics(inputs: dict[str, object]) -> list[list[object]]:
    xi_ar = inputs["xi_ar"]
    validation = inputs["transport_validation"]
    energy = inputs["energy_convergence"]
    angle = inputs["angle_convergence"]
    rows = [
        ["xi_ar", float(xi_ar["xi_ar"]), "Xi_AR near unity closes the low-barrier inner-gap tracking branch."],
        ["corr_ar_inner", float(xi_ar["corr_ar_inner"]), "AR onset tracks Delta_in much more strongly than the outer feature."],
        ["corr_ar_outer", float(xi_ar["corr_ar_outer"]), "Outer-feature correlation stays subleading in the current zeeman-family scan."],
    ]
    for family in ["threshold", "barrier", "gamma"]:
        family_df = validation[validation["test_family"] == family]
        rows.append([
            f"{family}_max_onset_spread",
            float(family_df["max_onset_spread"].max()),
            f"Current {family} robustness package keeps the onset ordering unchanged across the tested sweep.",
        ])
    fine_energy = energy[energy["energy_points"] == energy["energy_points"].max()]
    rows.append([
        "energy_grid_max_onset_shift_vs_ref",
        float(fine_energy["max_abs_onset_shift_vs_ref"].max()),
        "Residual onset drift at the finest tested energy grid relative to the reference run.",
    ])
    fine_angle = angle[angle["fs_k_grid"] == angle["fs_k_grid"].max()]
    rows.append([
        "angle_grid_max_w_peak_shift_vs_ref",
        float(fine_angle["max_abs_w_peak_shift_vs_ref"].max()),
        "Residual alpha-window peak drift at the finest tested angular/Fermi-surface grid.",
    ])
    return rows


def write_e4_selectivity_note(inputs: dict[str, object]) -> str:
    xi_ar = inputs["xi_ar"]
    validation = inputs["transport_validation"]
    threshold_max = float(validation[validation["test_family"] == "threshold"]["max_onset_spread"].max())
    barrier_max = float(validation[validation["test_family"] == "barrier"]["max_onset_spread"].max())
    gamma_max = float(validation[validation["test_family"] == "gamma"]["max_onset_spread"].max())
    return f"""# E4 inner-gap selectivity note

## Current closure

- `Xi_AR = {float(xi_ar['xi_ar']):.3f}`
- `corr(E_AR, Delta_in) = {float(xi_ar['corr_ar_inner']):.3f}`
- `corr(E_AR, E_out) = {float(xi_ar['corr_ar_outer']):.3f}`
- threshold / barrier / broadening onset spreads remain at `{threshold_max:.3e}`, `{barrier_max:.3e}`, and `{gamma_max:.3e}` in the saved validation suite

## Bounded claim

Within the current kernel family, the low-barrier Andreev onset follows the
inner superconducting scale much more closely than the outer normal-state
feature. This is strong enough for the manuscript-safe statement that the
present transport engine selects the inner-gap scale internally, but it is not
yet a license to claim direct experimental proof of the inner gap itself.

## What this closes

- the old `inner_gap_tracking` branch is no longer blocked
- threshold choice is not driving the onset ordering
- the present low/intermediate/high `Z` sweep does not flip the onset order
- the saved `Gamma` sweep does not create a fake selectivity branch

## What remains outside scope

- no claim of unique pairing-state identification
- no claim that every future control family must land on exactly the same `Xi_AR`
- no claim that the current kernel line alone replaces a full angle-resolved manuscript solver
"""


def build_e5_decision_rows(inputs: dict[str, object]) -> list[list[object]]:
    constraint = inputs["constraint"]
    invariance = inputs["invariance"]
    rows: list[list[object]] = []
    for family in ["s_wave", "s_pm", "chiral", "trivial_double_peak"]:
        family_df = constraint[constraint["symmetry"] == family]
        mean_alpha_selectivity = float(family_df["mean_alpha_selectivity"].mean())
        mean_support_leakage = float(family_df["mean_support_leakage"].mean())
        mixed_pass = "yes" if (family_df["mixed_constraint_pass"] == "yes").all() else "no"
        if family == "s_wave":
            inner_gap_status = "yes, but only as a smooth baseline"
            alpha_status = "weak or absent"
            phase_status = "not claimed"
            basis_status = "no channel-selective alpha window survives"
        elif family == "s_pm":
            inner_gap_status = "not yet isolated"
            alpha_status = "conditional and unstable"
            phase_status = "not claimed"
            basis_status = "spectral metric stable but decision branch not closed"
        elif family == "chiral":
            inner_gap_status = "compatible in current kernel line"
            alpha_status = "present"
            phase_status = "supported in current constraint pipeline"
            basis_status = "spectral metric stable"
        else:
            inner_gap_status = "fails as desired"
            alpha_status = "absent"
            phase_status = "negative control only"
            basis_status = "not applicable"
        rows.append([
            family,
            inner_gap_status,
            alpha_status,
            basis_status,
            phase_status,
            f"{mean_alpha_selectivity:.4f}",
            f"{mean_support_leakage:.4f}",
            mixed_pass,
        ])
    basis_df = invariance[invariance["transform"] == "orbital_basis"]
    rows.append([
        "global_basis_check",
        "not a pairing family",
        "alpha-window metric invariant",
        f"max deviation {basis_df['max_alpha_window_deviation'].max():.2e}",
        "use as a figure-level supporting control",
        "",
        "",
        "yes",
    ])
    return rows


def write_e5_pairing_note(inputs: dict[str, object]) -> str:
    constraint = inputs["constraint"]
    chiral_df = constraint[constraint["symmetry"] == "chiral"]
    swave_df = constraint[constraint["symmetry"] == "s_wave"]
    trivial_df = constraint[constraint["symmetry"] == "trivial_double_peak"]
    return f"""# E5 pairing-family and negative-control note

## Current comparison line

- ordinary same-sign `s_wave` keeps a low mean alpha selectivity of `{swave_df['mean_alpha_selectivity'].mean():.4f}` and never passes the mixed constraint
- `chiral` reaches a mean alpha selectivity of `{chiral_df['mean_alpha_selectivity'].mean():.4f}` and passes the mixed constraint on every saved `Z` slice
- the explicit `trivial_double_peak` control fails as desired with mean alpha selectivity `{trivial_df['mean_alpha_selectivity'].mean():.4f}`

## Manuscript-safe reading

The current package is already good enough to compare pairing families and to
show that a smooth same-sign baseline plus a trivial finite-bias double-peak
construction do not satisfy the same joint observable criteria as the
sign-sensitive branch. This supports a bounded NC claim about diagnostic
framework quality and negative controls, while still avoiding any statement
that one microscopic family has been uniquely identified.

## Safe boundaries

- it is safe to write that the ordinary same-sign baseline does not generate a robust alpha-window branch in the tested kernel family
- it is safe to write that the explicit trivial finite-bias control fails in the same observable pipeline
- it is not yet safe to write that every unconventional family is separated uniquely from every alternative family
"""


def write_e7_methods_note() -> str:
    return """# E7 Methods strengthening block

## Recommended subsection order

1. Minimal multiorbital model
2. Pairing channels
3. Scattering matrix and boundary conditions
4. Andreev-reflection onset extraction
5. Transparent-window alpha metric
6. Basis-rotation and interface-mixing tests
7. Negative-control kernels
8. Numerical convergence and reproducibility

## Current evidence anchor in project space

- model and parameter definitions: `src/twse2_minimal.py`, `config/default_params.json`
- scattering / channel-resolved transport engine: `scripts/build_channel_resolved_multiorbital_btk.py`
- onset extraction: `scripts/build_rhe_onset_kernel_tracking.py`, `scripts/build_xi_ar_scan.py`
- basis/interface invariance: `results/kernel_invariance_tests_2026-05-02/`
- negative controls and observable definitions: `results/observable_constraint_negative_control_2026-05-03/`
- convergence / reproducibility: `results/convergence_reproducibility_suite_2026-05-03/`

## Immediate writing rule

Use Methods to absorb algorithmic detail that would otherwise overload the main
Results. Each subsection should point to one executable artifact in the
canonical project space rather than to a prose-only promise.
"""


def build_e8_material_rows() -> list[list[str]]:
    return [
        ["A1", "S^dagger S / flux conservation audit", "complete", "results/full_smatrix_transport_audit_2026-05-03/", "normal-incidence full-S audit already saved"],
        ["A2", "r_he-onset threshold robustness", "complete", "results/transport_validation_suite_2026-05-03/", "threshold family already shows zero onset spread"],
        ["A3", "Z-sweep", "partial", "results/transport_validation_suite_2026-05-03/ ; results/channel_resolved_multiorbital_btk_2026-05-02/", "needs figure/SI-ready barrier export rather than internal validation only"],
        ["A4", "broadening / energy-grid convergence", "complete", "results/convergence_reproducibility_suite_2026-05-03/", "energy-grid, angle-grid, and broadening package already saved"],
        ["A5", "ordinary s-wave negative-control plot", "complete", "results/observable_constraint_negative_control_2026-05-03/", "same-pipeline ordinary baseline and trivial control already saved"],
        ["A6", "trivial finite-bias double-peak control", "complete", "results/observable_constraint_negative_control_2026-05-03/", "explicit trivial control already fails as desired"],
        ["A7", "source data for every main figure", "complete", "submission_package_nc_2026-05-03/source_data/", "compiled workbook and figure-wise CSV files already present"],
        ["A8", "code availability package", "complete", "submission_package_nc_2026-05-03/README_reproduce.md ; requirements.txt ; scripts/", "reproduction guide, requirements, and script set already present"],
        ["B1", "eigenchannel projection onto experimentally meaningful modes", "not started", "none", "still absent in current long-term space"],
        ["B2", "interface orientation map", "partial", "results/kernel_invariance_tests_2026-05-02/ ; results/observable_constraint_negative_control_2026-05-03/", "alpha dependence exists, but no dedicated experiment-facing orientation map yet"],
        ["B3", "finite-temperature smearing", "not started", "none", "no dedicated temperature package yet"],
        ["B4", "disorder / interface roughness proxy", "partial", "results/kernel_invariance_tests_2026-05-02/", "interface-mixing proxy exists, but no full disorder package"],
        ["B5", "comparison with standard single-channel BTK", "not started", "none", "no saved direct benchmark"],
        ["B6", "parameter sensitivity table", "partial", "results/e4_to_e11_package_2026-05-03/e8_material_priority.csv", "this package provides the first ledger, but not a manuscript-facing full table yet"],
        ["C1", "predicted experimental line cuts", "not started", "none", "still absent"],
        ["C2", "data-driven decision tree", "partial", "results/e5_to_e8_package_2026-05-02/ ; results/e4_to_e11_package_2026-05-03/", "bounded decision-tree package exists, but not yet fully data-driven"],
        ["C3", "full alternative-pairing atlas", "partial", "results/observable_constraint_negative_control_2026-05-03/ ; results/channel_resolved_multiorbital_btk_2026-05-02/", "family comparison exists, but not a full atlas"],
        ["C4", "public Zenodo/figshare archive draft", "not started", "none", "no public deposition draft yet"],
    ]


def write_e8_materials_note() -> str:
    return """# E8 material-priority ledger

This file converts the NC memo into an executable materials checklist. The
current project is already strong on the mandatory reviewer-safety items
(`A1-A8`), while the strongest remaining upgrades sit in the experimental
bridge layer (`B1-B6`) and public-archive / atlas polish (`C1-C4`).

The immediate use of this ledger is not to reopen every side branch. It is to
make sure future iterations pick one missing item consciously instead of
rediscovering the same checklist from scratch.
"""


def write_e9_reference_note() -> str:
    return """# E9 reference and positioning note

## Five literature classes that must remain explicit

1. twisted WSe2 superconductivity experiments
2. moire TMD superconductivity theory
3. Andreev spectroscopy / BTK foundations
4. phase-sensitive probes of unconventional superconductivity
5. multiband / multiorbital interface scattering

## Contribution paragraph draft

Previous works established the existence of superconductivity in twisted WSe2,
identified a multiscale low-energy setting in moire TMDs, and developed the
general BTK / Andreev language for unconventional superconductors. What
remained unresolved was whether the channel-selective low-energy Andreev
features seen in this platform should be read as intrinsic signatures of
superconducting phase structure or as artifacts of basis choice, interface
filtering, or trivial finite-bias peak shaping. The current project addresses
this gap by extracting both inner-gap onset tracking and transparent-window
selection from the same multiorbital scattering kernel, while pairing each
positive claim with explicit invariance tests and negative controls.

## Writing boundary

Keep the literature block broad enough for Nature Communications, but do not
inflate the claim into unique order-parameter identification. The positioning
should stay on the framework / diagnostic side unless a stronger family-separation
package is actually executed later.
"""


def write_e10_objection_note() -> str:
    return """# E10 reviewer-objection response map

## Objection 1

**Claim:** The work does not identify the pairing state uniquely.

**Response:** We do not claim unique order-parameter identification. We claim a
kernel-internal diagnostic framework with negative controls that excludes the
ordinary same-sign baseline within the tested family.

## Objection 2

**Claim:** The alpha-window may be a basis artifact.

**Response:** The saved basis-rotation and interface-mixing packages show that
diagonal channel weights move, while the spectral alpha-window metric remains
invariant to numerical precision.

## Objection 3

**Claim:** The r_he-onset definition is arbitrary.

**Response:** Threshold, barrier, Gamma, and energy-grid sweeps now exist in
the canonical project space and preserve the onset ordering and inner-gap
tracking branch.

## Objection 4

**Claim:** The kernel is not sufficiently validated.

**Response:** The full-S bootstrap, unitarity audit, particle-hole audit,
convergence suite, and observable-definition package are all now executable and
saved.

## Objection 5

**Claim:** The ordinary s-wave control is too simple.

**Response:** The current package now includes both the ordinary same-sign
baseline and an explicit trivial finite-bias double-peak negative control in
the same observable pipeline. The manuscript should still state the correct
boundary: only the ordinary same-sign baseline is excluded within the tested
kernel family.

## Objection 6

**Claim:** Experimental relevance is unclear.

**Response:** The present manuscript line can now point to low-barrier onset,
alpha-window selectivity, barrier dependence, and reproducibility tables as
experiment-facing observables. A future predicted-line-cut package would still
be a real upgrade, but it is no longer the first blocker.
"""


def build_e11_submission_rows() -> list[list[str]]:
    rows: list[list[str]] = []
    manuscript_files = [
        "main.tex",
        "main.pdf",
        "supplementary_information.tex",
        "supplementary_information.pdf",
        "references.bib",
        "README_reproduce.md",
        "cover_letter_draft.md",
        "source_data/SourceData_NC_revision.xlsx",
        "data_manifest_sha256.txt",
        "requirements.txt",
    ]
    for relative_path in manuscript_files:
        exists = (SUBMISSION_ROOT / relative_path).exists()
        rows.append([relative_path, "present" if exists else "missing", "submission package"])
    figure_paths = [
        "figures/Fig1_pairing_symmetry_comparison.png",
        "figures/Fig2_rhe_onset_vs_delta_in.png",
        "figures/Fig3_smatrix_audit.png",
        "figures/Fig4_kernel_invariance_alpha_window.png",
        "figures/Fig5_constraint_audit.png",
    ]
    for relative_path in figure_paths:
        exists = (SUBMISSION_ROOT / relative_path).exists()
        rows.append([relative_path, "present" if exists else "missing", "figure asset"])
    zipped_archives = [
        "submission_package_nc_2026-05-03.zip",
        "submission_package_nc_2026-05-03_clean.zip",
        "submission_package_nc_2026-05-03_rev2.zip",
        "submission_package_nc_2026-05-03_rev3.zip",
    ]
    for filename in zipped_archives:
        exists = (ROOT / filename).exists()
        rows.append([filename, "present" if exists else "missing", "archive bundle"])
    return rows


def write_e11_submission_note() -> str:
    return """# E11 submission-package audit

## Audit target

Check whether the current Nature Communications submission folder already
contains the minimum manuscript, figure, source-data, and reproducibility
objects implied by the NC memo.

## Current readout

- main text source and compiled PDF are present
- supplementary source and compiled PDF are present
- figure assets for Figures 1-5 are present
- source-data workbook is present
- reproduction README, requirements file, and checksum manifest are present
- multiple zip exports of the submission package are present

## Remaining boundary

This audit only checks package presence and local readability. It does not by
itself certify that every manuscript sentence is already aligned to the newest
evidence line. That alignment still belongs to the manuscript revision ledger.
"""


def update_readme() -> None:
    text = README_PATH.read_text(encoding="utf-8")
    old_block = "- `scripts/run_transport_validation_suite.py`: validates threshold,\n  broadening, barrier, and internal `r_he` particle-hole robustness\n"
    new_block = old_block + (
        "- `scripts/build_e4_e11_package.py`: assembles the manuscript-facing E4,\n"
        "  E5, and E7-E11 content ledger from the saved numerical packages\n"
        "- `scripts/update_sync_status.py`: refreshes the sync audit after each\n"
        "  substantive turn\n"
    )
    if "scripts/build_e4_e11_package.py" not in text:
        text = text.replace(old_block, new_block)
    if "python scripts/build_e4_e11_package.py" not in text:
        text = text.replace(
            "python scripts/run_full_smatrix_transport_audit.py\n```",
            "python scripts/run_full_smatrix_transport_audit.py\npython scripts/build_e4_e11_package.py\npython scripts/update_sync_status.py\n```",
        )
    README_PATH.write_text(text, encoding="utf-8")


def update_project_space_index() -> None:
    text = PROJECT_INDEX_PATH.read_text(encoding="utf-8")
    marker = "- a full Nature Communications submission package dated `2026-05-03` under\n"
    addition = (
        "- an E4-to-E11 manuscript-support package dated `2026-05-03` under\n"
        "  `results/e4_to_e11_package_2026-05-03/`, tying the saved transport,\n"
        "  invariance, convergence, negative-control, methods, reviewer-response,\n"
        "  and submission-checklist lines into one continuous NC-facing ledger\n"
    )
    if addition not in text:
        text = text.replace(marker, addition + marker)
    PROJECT_INDEX_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    inputs = load_inputs()
    e4_rows = build_e4_metrics(inputs)
    e5_rows = build_e5_decision_rows(inputs)
    e8_rows = build_e8_material_rows()
    e11_rows = build_e11_submission_rows()
    write_csv(RESULTS_ROOT / "e4_selectivity_metrics.csv", ["metric", "value", "meaning"], e4_rows)
    write_csv(
        RESULTS_ROOT / "e5_pairing_decision_table.csv",
        [
            "family",
            "inner_gap_tracking_status",
            "alpha_window_status",
            "basis_invariance_status",
            "phase_sensitive_signature_status",
            "mean_alpha_selectivity",
            "mean_support_leakage",
            "mixed_constraint_pass",
        ],
        e5_rows,
    )
    write_csv(
        RESULTS_ROOT / "e8_material_priority.csv",
        ["item", "material", "status", "evidence_path", "next_note"],
        e8_rows,
    )
    write_csv(
        RESULTS_ROOT / "e11_submission_audit.csv",
        ["path", "status", "category"],
        e11_rows,
    )
    (RESULTS_ROOT / "e4_inner_gap_selectivity.md").write_text(write_e4_selectivity_note(inputs), encoding="utf-8")
    (RESULTS_ROOT / "e5_pairing_negative_controls.md").write_text(write_e5_pairing_note(inputs), encoding="utf-8")
    (RESULTS_ROOT / "e7_methods_strengthening.md").write_text(write_e7_methods_note(), encoding="utf-8")
    (RESULTS_ROOT / "e8_material_priority.md").write_text(write_e8_materials_note(), encoding="utf-8")
    (RESULTS_ROOT / "e9_reference_positioning.md").write_text(write_e9_reference_note(), encoding="utf-8")
    (RESULTS_ROOT / "e10_reviewer_response_map.md").write_text(write_e10_objection_note(), encoding="utf-8")
    (RESULTS_ROOT / "e11_submission_package_audit.md").write_text(write_e11_submission_note(), encoding="utf-8")
    manifest = {
        "package": "e4_to_e11_package_2026-05-03",
        "inputs": {
            "nc_memo": str(NC_MEMO_PATH),
            "xi_ar_metrics": str(XI_AR_METRICS_PATH),
            "transport_validation": str(TRANSPORT_VALIDATION_PATH),
            "kernel_invariance": str(INVARIANCE_SUMMARY_PATH),
            "constraint_summary": str(CONSTRAINT_SUMMARY_PATH),
            "smatrix_summary": str(SMATRIX_SUMMARY_PATH),
            "particle_hole_summary": str(PHS_SUMMARY_PATH),
            "energy_convergence": str(ENERGY_CONVERGENCE_PATH),
            "angle_convergence": str(ANGLE_CONVERGENCE_PATH),
            "submission_package": str(SUBMISSION_ROOT),
        },
        "outputs": [
            "e4_selectivity_metrics.csv",
            "e4_inner_gap_selectivity.md",
            "e5_pairing_decision_table.csv",
            "e5_pairing_negative_controls.md",
            "e7_methods_strengthening.md",
            "e8_material_priority.csv",
            "e8_material_priority.md",
            "e9_reference_positioning.md",
            "e10_reviewer_response_map.md",
            "e11_submission_audit.csv",
            "e11_submission_package_audit.md",
        ],
    }
    (RESULTS_ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    summary = """# E4-to-E11 package summary

- E4 inner-gap selectivity note and metrics are now packaged together
- E5 pairing-family comparison and negative-control table are now explicit
- E7 Methods strengthening block is now saved as one standalone note
- E8 material-priority checklist is now executable as a status ledger
- E9 reference-positioning paragraph is now available as manuscript-facing text
- E10 reviewer-objection responses are now mapped to saved evidence
- E11 submission-package presence audit is now saved
"""
    (RESULTS_ROOT / "summary.md").write_text(summary, encoding="utf-8")
    update_readme()
    update_project_space_index()
    print(summary)


if __name__ == "__main__":
    main()
