# Slice-matched alpha-rule ↔ BTK correlation

## What was built
- A fresh alpha-rule proxy table for the four pairing families used by the semi-infinite BTK package: `s_wave`, `nodal_even`, `valley_even`, `valley_odd`.
- A row-level slice-matched dataset that joins every alpha-rule family slice to every semi-infinite BTK slice for the same pairing family.
- Correlation summaries that ask whether alpha-rule family ordering tracks BTK family ordering on each `(model, valley, Z, eta_broadening)` slice.

## Focus slice chosen for the figure
- alpha-rule intervalley-mixing slice: `eta_mix=1.00`
- largest-magnitude compressed-V3 total peak-contrast correlation: `Z=0.0`, `eta_broadening=0.50 meV`, `rho=-0.105`, `r=-0.438`
- largest-magnitude compressed-V3 valley-asymmetry correlation: `Z=2.0`, `eta_broadening=0.50 meV`, `rho=-0.211`, `r=-0.422`

## Interpretation boundary
- The alpha-rule proxy still comes from the minimum runnable interface-sign screening model.
- The BTK side is the existing semi-infinite SGF-informed proxy package rather than the final multiorbital conductance kernel.
- Because the current BTK package does not yet scan interface alpha directly, this dataset measures family-order alignment, not a full alpha-resolved conductance closure.

## Key files
- `alpha_rule_family_slices.csv`
- `alpha_btk_pairing_slice_dataset.csv`
- `alpha_btk_correlation_summary.csv`
- `alpha_btk_valley_asymmetry_correlation.csv`
- `alpha_btk_correlation_figure.png`
