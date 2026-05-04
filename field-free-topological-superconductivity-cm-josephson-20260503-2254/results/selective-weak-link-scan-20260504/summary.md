# Selective Weak-Link Scan Summary

## Goal

Third-pass coarse scan keeping the strip-like planar geometry fixed while making the weak link more selective through a stronger barrier, weaker interface tunneling, and a narrower compensated-magnetic momentum form.

## Model

- Same six-row strip geometry as the second scan
- Higher weak-link barrier than the planar-junction baseline
- Reduced interface hopping between superconducting banks and junction rows
- Reduced junction longitudinal hopping and weaker junction spin-orbit leakage
- Compensated-magnetic splitting changed to `M0 [cos(kx) - 0.65 cos(2kx)]` with opposite signs on the two junction rows

## Scan grid

- `mu`: 9 points from -2.00 to 2.00
- `phi/pi`: 13 points from 0.00 to 1.00
- `M0`: 8 points from 0.00 to 1.40
- `kx`: 121 points

## Quantitative result

- Total parameter points: `936`
- Smallest gap found: `0.000003` at `mu=0.000`, `M0=1.400`, `phi/pi=0.833`, `kx=-0.733`
- Near-closing points with threshold `0.0005`: `125`
- Points with exploratory topological indicator `-1`: `0`
- Fraction of near-closing points within `|phi-pi| < 0.35`: `0.128`
- Fraction of near-closing points with `phi/pi < 0.25`: `0.288`
- Fraction of topological-indicator points concentrated near `phi ~ pi`: `0.000`
- Gap median across the full scan: `0.004050`
- Baseline comparison against the second scan at the same threshold: `52` near-closing points, `phi~pi` fraction `0.058`, low-phase fraction `0.481`

## Interpretation

- This run isolates weak-link physics as the only major change relative to the second scan, so any improvement or failure here is directly attributable to the junction mechanism rather than the geometry.
- The result is mixed but informative: the near-closing set becomes more phase-selective than in the second scan, but it also becomes much larger overall.
- Relative to the second scan, the `phi ~ pi` fraction improves from `0.058` to the measured value in this run, and the low-phase fraction drops from `0.481`, so the weak-link redesign is moving spectral weight in the right direction.
- However, the total near-closing count grows from `52` to the measured value in this run, which means the stronger barrier and more selective magnetic form still leave too many generic soft-gap configurations alive.
- The current bottleneck is therefore narrower than before: weak-link selectivity helps, but it must now be combined with an additional mechanism that prunes the remaining broad low-gap manifold.

## Evidence status

- `partially verified`: this is the first revision that improves phase allocation in the right direction, but it does not yet reduce the low-gap clutter enough to count as a convincing topological window.
