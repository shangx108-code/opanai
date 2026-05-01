# Iteration 027 Robust Joint Fabrication Tolerance

- Timestamp: `2026-05-01T17:10:00Z`
- Action type: `robust_joint_fabrication_tolerance_execution`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `after the unmitigated linked tolerance scan, the missing question was whether robust-mask training truly opens the fabrication-tolerance safety window`

## Executed action

1. Added `scripts/run_joint_fabrication_tolerance_robust.py`.
2. Reused the same linked three-factor grid as iteration 026:
   - phase noise
   - layer misalignment
   - wavelength drift
3. Re-ran the grid with the robust-mask-trained phase-only stack.
4. Wrote a direct comparison table against the unmitigated boundary:
   - `results/tolerance_joint_robust/boundary_expansion_vs_unmitigated.csv`

## Verification result

- `UCID` clean branch improves substantially:
  - `0%` drift: `+2.5993 ± 0.0812 dB` vs unmitigated `+1.6409 ± 0.3407 dB`
  - `2%` drift: `+2.5192 ± 0.1570 dB` vs unmitigated `+1.6255 ± 0.3339 dB`
- `Kodak-PCD0992` clean branch improves but still fails:
  - `-0.2182 ± 0.0935 dB` vs unmitigated `-1.1084 ± 0.1963 dB`
- The linked pass region does **not** expand:
  - the only passing branch remains clean `UCID`
  - phase noise `0.05 rad` still fails on `UCID`: `-4.3309 ± 1.7409 dB`
  - mild misalignment `0.25 px / 0.5 deg` still fails on `UCID`: `-7.4303 ± 0.5466 dB`

## Interpretation boundary

This robust-mask strategy helps the clean operating point and the previously executed single-factor first-order cases, but it does not solve the linked fabrication-tolerance problem.

## Next shortest-path action

Stop treating the current robust-mask strategy as a likely route to broad hardware robustness. The next efficient move is either:
1. redesign the training objective around the linked perturbation distribution itself, or
2. tighten the manuscript claim boundary so the robust result is presented as clean-point margin improvement rather than safety-window expansion.
