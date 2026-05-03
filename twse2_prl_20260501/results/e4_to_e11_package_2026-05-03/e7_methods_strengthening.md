# E7 Methods strengthening block

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
