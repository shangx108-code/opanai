# Planar Junction Coarse Scan Summary

## Goal

Second-pass coarse scan using a strip-like planar Josephson junction model with superconducting banks and a compensated-magnetic weak link, replacing the over-permissive two-channel model.

## Model

- Six-row transverse strip: two left superconducting rows, two junction rows, two right superconducting rows
- Pairing lives only on the superconducting banks with phases `+phi/2` and `-phi/2`
- The two junction rows carry opposite compensated magnetic splittings `+M0 cos(kx)` and `-M0 cos(kx)`, so the weak link has zero net magnetization
- A junction barrier is included only in the weak-link rows

## Scan grid

- `mu`: 9 points from -2.00 to 2.00
- `phi/pi`: 13 points from 0.00 to 1.00
- `M0`: 7 points from 0.00 to 1.20
- `kx`: 121 points

## Quantitative result

- Total parameter points: `819`
- Smallest gap found: `0.000004` at `mu=0.500`, `M0=0.400`, `phi/pi=0.667`, `kx=-0.105`
- Near-closing points with threshold `0.0005`: `52`
- Points with exploratory topological indicator `-1`: `0`
- Fraction of near-closing points within `|phi-pi| < 0.35`: `0.058`
- Fraction of near-closing points with `phi/pi < 0.25`: `0.481`
- Fraction of topological-indicator points concentrated near `phi ~ pi`: `0.000`
- Gap median across the full scan: `0.007825`
- Baseline comparison at the same `5e-4` threshold: previous two-channel model had `34` near-closing points, `phi~pi` fraction `0.235`, and low-phase fraction `0.235`

## Interpretation

- This strip-like model is structurally closer to the intended planar junction because superconductivity and compensated magnetism now live in different transverse regions.
- The answer from this coarse scan is negative: geometry alone does not sharpen selectivity here.
- Compared with the first scan under the same low-gap threshold, the near-closing set becomes larger (`52` vs `34`), less concentrated near `phi ~ pi` (`0.058` vs `0.235`), and more crowded at low phase (`0.481` vs `0.235`).
- That means the remaining bottleneck is not merely the absence of a planar-junction geometry. The weak-link physics and effective coupling structure still need to be redesigned before transport diagnostics are worth building on.
- This is still useful progress because it rules out a tempting but insufficient model upgrade path.

## Evidence status

- `partially verified`: the second coarse scan is real and reproducible, and it shows that a more geometric planar-junction partition alone does not yet recover a convincing topological window.
