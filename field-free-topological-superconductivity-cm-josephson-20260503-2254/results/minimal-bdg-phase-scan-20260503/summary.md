# Minimal BdG Phase Scan Summary

## Goal

First quantitative check of whether a compensated-magnetic, phase-biased Josephson model produces phase-tuned gap closings consistent with a topological transition window.

## Model

- Two coupled proximitized channels representing the left and right superconducting sides of a Josephson junction
- Momentum-dependent compensated magnetic splitting: `M(k) = M0 cos(k)`
- Rashba term: `alpha sin(k)`
- Explicit left-right superconducting phase bias: `+phi/2` and `-phi/2`

## Scan grid

- `mu`: 9 points from -2.00 to 2.00
- `phi/pi`: 13 points from 0.00 to 1.00
- `M0`: 9 points from 0.00 to 1.60
- `k`: 121 points in the Brillouin zone

## Quantitative result

- Total parameter points: `1053`
- Smallest gap found: `0.000000` at `mu=-2.000`, `M0=0.800`, `phi/pi=1.000`, `k=0.000`
- Near-closing points with threshold `0.001`: `64`
- Points with exploratory topological indicator `-1`: `0`
- Fraction of near-closing points concentrated within `|phi-pi| < 0.35`: `0.188`
- Gap median across the full scan: `0.010545`

## Interpretation

- The script successfully produces reproducible gap minima across the full coarse grid, so the project now has a real executable starting point instead of a conceptual outline.
- However, this coarse effective model is still too permissive: near-closure points remain broadly distributed in phase and the exploratory topological indicator does not flip sign anywhere on the scanned grid.
- The immediate scientific implication is not a confirmed topological window, but a verified model-selection bottleneck: the next model revision must sharpen phase selectivity and yield a cleaner invariant change before transport claims are worth building on.
- This is a useful first closure because it rules out treating the current ad hoc junction model as manuscript-grade evidence.

## Files

- `minimal_gap_scan.csv`: full parameter grid
- `near_closing_points.csv`: only points below the closing threshold
- `summary.md`: this result note

## Evidence status

- `partially verified`: the executable scan and its negative result are real, but the present model does not yet isolate a convincing topological regime.
