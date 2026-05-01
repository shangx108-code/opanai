# Joint Fabrication-Tolerance Summary

Executed linked scan over phase noise, layer misalignment, and wavelength drift.

## Executed grid

- Seeds: `0, 1, 2`
- Monte Carlo repeats per noisy operating point: `4`
- Phase-noise levels (rad RMS): `0.000, 0.050, 0.100, 0.200`
- Wavelength-drift levels (fraction): `0.000, 0.005, 0.010, 0.020`
- Misalignment levels:
  - `clean`: shift sigma `0.00 px`, rotation sigma `0.00 deg`
  - `mild`: shift sigma `0.25 px`, rotation sigma `0.50 deg`
  - `moderate`: shift sigma `0.50 px`, rotation sigma `1.00 deg`
  - `severe`: shift sigma `1.00 px`, rotation sigma `2.00 deg`

## Failure-boundary snapshot

- `Kodak-PCD0992`:
  - clean-point state `fail`, first mean-fail drift `0.000`
- `UCID`:
  - clean-point state `pass`, first mean-fail drift `not reached`

## Files

- `joint_tolerance_curve.csv`: joint-grid tolerance curve with gain CI and degradation CI
- `degradation_ci.csv`: degradation-focused view of the same grid
- `failure_boundary.csv`: wavelength-drift failure boundary conditioned on phase noise and misalignment
- `axis_tolerance_curves.csv`: one-factor slices for quick plotting
