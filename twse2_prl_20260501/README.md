# tWSe2 Transport Project Space

This directory contains a minimum runnable theory scaffold for the first two
work packages in the uploaded PRL planning notes:

- WP1: normal-state plus correlated-background calibration
- WP2: pairing-candidate library and symmetry screening

The goal is not a publication-grade final calculation yet. The goal is to turn
the paper outline into an executable starting point that already produces:

- a two-scale DOS summary for a minimal normal-plus-superconducting model
- a first-pass screening table for three pairing families at an interface
- a channel-resolved multiorbital BTK package with symmetry comparison,
  alpha-window channel selection, and Delta_in versus AR alignment checks

## Layout

- `config/default_params.json`: shared parameters
- `src/twse2_minimal.py`: model helpers
- `scripts/run_wp1_wp2.py`: runs the first two work packages
- `scripts/run_wp3_minimal_btk.py`: generates the first conductance-proxy follow-up
- `scripts/build_wp3_figure_slice.py`: extracts the figure-ready PRL panel slice from WP3 results
- `scripts/run_kernel_alpha_validation.py`: builds the fixed-(Z,phi,eta) alpha-sweep validation dataset and figure
- `scripts/run_kernel_alpha_multislice_validation.py`: extends the kernel-alpha validation to a small multislice robustness set
- `scripts/build_channel_resolved_multiorbital_btk.py`: builds the current
  channel-resolved BTK result package
- `scripts/build_rhe_onset_kernel_tracking.py`: extracts the AR onset directly
  from the internal `r_he(E)` block and checks `Delta_in` tracking
- `scripts/run_kernel_invariance_tests.py`: verifies orbital-basis and
  interface-mixing invariance of the kernel-derived alpha-window
- `scripts/run_transport_validation_suite.py`: validates threshold,
  broadening, barrier, and internal `r_he` particle-hole robustness
- `scripts/build_e4_e11_package.py`: assembles the manuscript-facing E4,
  E5, and E7-E11 content ledger from the saved numerical packages
- `scripts/update_sync_status.py`: refreshes the sync audit after each
  substantive turn
- `scripts/run_normal_incidence_wfm_audit.py`: exploratory explicit mode-match
  bootstrap for the normal-incidence chain
- `scripts/run_full_smatrix_transport_audit.py`: stable full-S bootstrap for
  the normal-incidence chain with explicit `r_ee/r_eh/r_he/r_hh` blocks,
  unitarity, and particle-hole audits
- `results/`: generated summary tables and markdown
- `prl-manuscript-draft-v1.md`: PRL-style manuscript draft based on the current minimal results
- `prl-manuscript-draft-v2.md`: integrated PRL-style manuscript draft with
  the `r_he(E)` transport closure and kernel-invariance transport result
- `prl-manuscript-draft-v3-compressed.md`: PRL-compressed draft with tighter
  title, abstract, opening introduction, and shorter transport Results
- `sync-status.md`: current sync checklist for the long-term project space

## Run

```bash
python scripts/run_wp1_wp2.py
python scripts/build_channel_resolved_multiorbital_btk.py
python scripts/build_rhe_onset_kernel_tracking.py
python scripts/run_kernel_invariance_tests.py
python scripts/run_transport_validation_suite.py
python scripts/run_full_smatrix_transport_audit.py
python scripts/build_e4_e11_package.py
python scripts/update_sync_status.py
```
