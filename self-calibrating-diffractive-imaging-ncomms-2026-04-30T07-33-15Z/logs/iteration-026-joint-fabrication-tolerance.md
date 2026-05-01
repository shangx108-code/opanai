# Iteration 026 Joint Fabrication Tolerance

- Timestamp: `2026-05-01T16:30:00Z`
- Action type: `joint_fabrication_tolerance_execution`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `the project still lacked a linked three-factor fabrication-style tolerance result with an explicit failure boundary`

## Executed action

1. Added `scripts/run_joint_fabrication_tolerance.py`.
2. Executed a linked tolerance grid over:
   - phase-mask phase noise
   - layer-wise lateral plus rotational misalignment
   - wavelength drift
3. Aggregated the run into three reviewer-facing deliverables:
   - `results/tolerance_joint/joint_tolerance_curve.csv`
   - `results/tolerance_joint/degradation_ci.csv`
   - `results/tolerance_joint/failure_boundary.csv`

## Verification result

- Seeds: `3` (`0-2`)
- Monte Carlo repeats per noisy operating point: `4`
- Positive region:
  - only `UCID` remains positive
  - only on the fully clean hardware branch
  - wavelength drift up to `2%` does not close that clean `UCID` branch:
    - `0%`: `+1.6409 ± 0.3407 dB`
    - `0.5%`: `+1.6470 ± 0.3373 dB`
    - `1.0%`: `+1.6454 ± 0.3354 dB`
    - `2.0%`: `+1.6255 ± 0.3339 dB`
- Immediate failure modes in the unmitigated stack:
  - `UCID`, phase noise only `0.05 rad`: `-3.6303 ± 1.4411 dB`
  - `UCID`, mild misalignment only `0.25 px / 0.5 deg`: `-7.5949 ± 0.4896 dB`
  - `Kodak-PCD0992` already fails at the clean point: `-1.1084 ± 0.1963 dB`
- Strongest interpretation:
  - the dominant fragility is fabrication-style phase/mask error
  - wavelength drift is secondary within the executed clean-branch window

## Interpretation boundary

This iteration adds a linked simulated fabrication-tolerance package, not fabricated-device evidence. The result narrows the safe hardware claim rather than broadening it.

## Next shortest-path action

Use the new boundary tables to decide whether the manuscript should foreground robust-mask mitigation as the only credible path to a hardware-facing claim, or whether Figure-level tolerance language should be tightened further around a clean-stack simulation boundary.
