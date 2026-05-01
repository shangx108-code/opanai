# Iteration Round 2026-05-01 WP3

## Scope

Executed Work Package 3 in the canonical long-term project space by adding a
minimum runnable `alpha-Z-phi` generalized BTK proxy on top of the current
WP1-WP2 pairing library.

## New Artifacts

- `code/wp3_alpha_z_phi_btk.py`
- `data/wp3-alpha-z-phi-generalized-btk-2026-05-01/conductance_curves.csv`
- `data/wp3-alpha-z-phi-generalized-btk-2026-05-01/metrics_summary.csv`
- `data/wp3-alpha-z-phi-generalized-btk-2026-05-01/parameters.json`
- `data/wp3-alpha-z-phi-generalized-btk-2026-05-01/summary.md`

## What Is Now Verified

- `s_wave` remains nearly smooth in both `phi` and `alpha` within the current kernel.
- `s_pm` develops the clearest interface-orientation sensitivity, with strongest
  alpha anisotropy `0.387` at `eta=0.50`, `Z=3.0`.
- `chiral` keeps a finite low-energy response already at `eta=0`, which is
  consistent with the intended phase-winding family behavior in this proxy.
- All three families remain monotonic in `Z` across the tested parameter grid.

## Interpretation Boundary

This run is already good enough to support a first Figure-3-style scan for
`alpha-Z-phi` structure, but it does **not** yet justify any claim of barrier
non-monotonicity. That part remains an open kernel-upgrade target rather than a
verified manuscript statement.

## Shortest Next Action

Upgrade the BTK kernel so that `Z` dependence can become genuinely
non-monotonic when the pairing phase structure and interface channel compete,
then rerun the same scan and compare directly against this `2026-05-01` package.
