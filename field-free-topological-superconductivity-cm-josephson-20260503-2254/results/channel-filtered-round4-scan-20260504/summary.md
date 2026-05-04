# Round-4 Channel-Filtered Scan Summary

## Goal

Add one harder orbital/channel filter on top of the third selective weak-link branch so the residual low-gap manifold is pruned rather than merely reallocated in phase.

## Model change relative to the third scan

- Keep the six-row planar Josephson strip geometry unchanged
- Split the two junction rows by an explicit orbital detuning window
- Heavily down-weight the second junction row through a row-resolved channel filter
- Narrow the junction bandwidth further through smaller in-junction hopping and weaker interface transmission
- Sharpen the compensated-magnetic form factor so the active row carries most of the spectral weight

## Quantitative result

- Total parameter points: `936`
- Smallest gap found: `0.000130` at `mu=2.000`, `M0=1.200`, `phi/pi=0.000`, `kx=-0.367`
- Near-closing points with threshold `0.0005`: `39`
- Points with exploratory topological indicator `-1`: `182`
- Fraction of near-closing points within `|phi-pi| < 0.35`: `0.154`
- Fraction of near-closing points with `phi/pi < 0.25`: `0.231`
- Fraction of topological-indicator points concentrated near `phi ~ pi`: `0.154`
- Gap median across the full scan: `0.003876`
- Third-scan baseline: `125` near-closing points, `phi~pi` fraction `0.128`, low-phase fraction `0.288`
- Relative near-closing reduction versus the third scan: `68.800%`
- Residual near-closing families: `(M0=0.4, mu=0.5) x13, (M0=0.6, mu=1.0) x13, (M0=1.2, mu=2.0) x13`

## Interpretation

- This pass is intentionally harsher: it sacrifices a broader two-row junction manifold in favor of a more single-channel weak link.
- The decisive test was passed on total clutter: the near-closing count falls sharply relative to the third scan, and the low-phase leakage fraction also improves modestly.
- The remaining low-gap manifold is no longer broadly spread over parameter space; it collapses into a small number of almost phi-flat parameter families.
- The residual issue is now clearer than before: these survivors are not phase-focused around `phi ~ pi`, so the current filter cleans the spectrum but does not yet produce the desired phase-controlled closure pattern.

## Evidence status

- `verified for clutter reduction only`: this round succeeds at the user-requested pruning task, but the surviving low-gap families remain too phi-insensitive to support a manuscript-grade phase-selective topological claim.
