# Iteration Round 2026-05-01 Control Discriminant

## Scope

Built a control-discriminant test in the canonical long-term project space by
adding a phase-blind symmetric double-peak control channel and rerunning the
same `alpha-Z-phi` scan used for the chiral branch.

## New Artifacts

- `code/wp3_alpha_z_phi_btk.py` updated in place
- `data/wp3-control-discriminant-2026-05-01/conductance_curves.csv`
- `data/wp3-control-discriminant-2026-05-01/metrics_summary.csv`
- `data/wp3-control-discriminant-2026-05-01/discriminator_table.csv`
- `data/wp3-control-discriminant-2026-05-01/summary.md`

## What Is Now Verified

- The `control_double_peak` branch can generate finite-bias symmetric peaks, but
  remains strictly phase-blind on the tested grid.
- The control branch shows zero `phi` drift of positive peak position and zero
  `alpha` coupling of peak splitting.
- The `chiral` branch shows both:
  - maximum `phi` drift of positive peak position `0.0928`
  - maximum `alpha`-coupled change in peak splitting `0.1856`
- The `chiral` branch also breaks monotonic `Z` behavior across the full tested
  configuration set, while the control branch does not.

## Manuscript-Grade Reduction

Finite-bias peaks by themselves are not a sufficient chiral indicator. On the
same `alpha-Z-phi` grid, only the chiral branch shows phase-locked drift of the
finite-bias peak position together with `alpha`-coupled peak splitting, while a
phase-blind symmetric double-peak control cannot reproduce either feature.

## Consequence

The chiral claim now has a concrete control discriminant and has moved from
"interesting edge-peak behavior" to a substantially stronger phase-sensitive
statement. Further manuscript work should build around this control-based
discriminator rather than around finite-bias peaks alone.
