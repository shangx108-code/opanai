# Iteration 028 Second-Generation Joint Training

- Timestamp: `2026-05-01T18:20:00Z`
- Action type: `secondgen_joint_perturbation_training`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `after the robust-mask linked scan, the missing question was whether a training objective that injects phase noise, misalignment, and wavelength drift jointly can actually widen the fabrication-tolerance window`

## Executed action

1. Added `scripts/run_joint_fabrication_tolerance_secondgen.py`.
2. Replaced first-order-only training exposure with a joint-perturbation training set containing:
   - clean
   - joint mild (`0.05 rad`, `0.25 px`, `0.5 deg`, `0.5%`)
   - joint moderate (`0.10 rad`, `0.50 px`, `1.0 deg`, `1.0%`)
3. Re-ran the same linked fabrication-style tolerance grid after second-generation training.
4. Wrote:
   - `results/tolerance_joint_secondgen/joint_tolerance_curve.csv`
   - `results/tolerance_joint_secondgen/failure_boundary.csv`
   - `results/tolerance_joint_secondgen/boundary_comparison.csv`

## Verification result

- The linked pass set does not expand.
- `UCID` remains positive only on the clean branch:
  - clean `0%` drift: `+2.3951 ± 0.2853 dB`
  - clean `2%` drift: `+2.3037 ± 0.3357 dB`
- The dominant linked failures remain failures:
  - `UCID`, phase noise only `0.05 rad`: `-4.7289 ± 1.9562 dB`
  - `UCID`, mild misalignment only `0.25 px / 0.5 deg`: `-8.3056 ± 2.1266 dB`
  - `Kodak-PCD0992`, clean `0%` drift: `-0.4409 ± 0.1989 dB`
- Relative to the first robust-mask strategy:
  - the clean `UCID` branch stays positive but is weaker (`+2.3951 dB` vs `+2.5993 dB`)
  - the clean Kodak deficit remains negative and is also weaker (`-0.4409 dB` vs `-0.2182 dB`)

## Interpretation boundary

This is a meaningful negative result. Joint perturbation exposure during training, in its current first-pass form, does not open the fabrication-tolerance safety window and does not outperform the simpler robust-mask strategy on the linked boundary metric.

## Next shortest-path action

Treat the first robust-mask strategy as the better current mitigation result for manuscript purposes. Any further second-generation training should be justified only if the objective, sampling, or architecture is changed enough to plausibly alter the boundary outcome.
