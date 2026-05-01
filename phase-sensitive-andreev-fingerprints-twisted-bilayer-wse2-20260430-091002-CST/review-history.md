# Review History

## Internal Review Round 0

- Date: 2026-04-30 09:10:02 CST
- Stage: Project intake
- Acceptance estimate: 12-18%

### Main reasons for low acceptance

1. The project currently has concept strength but no evidence-grade computational package.
2. The central exclusion claim against ordinary same-sign s-wave has not yet been quantitatively tested.
3. The proposed inner-gap selectivity story is still a design target rather than a demonstrated result.

### Shortest repair actions

1. Build and run a minimal, reproducible scan that starts generating gap-selective observables.
2. Formalize an ordinary s-wave failure metric under the same parameter family used for unconventional candidates.
3. Turn the first real outputs into a figure map and caption-ready language with strict claim bounds.

## Internal Review Round 1

- Date: 2026-04-30 09:19:00 CST
- Stage: First interface-sensitive surrogate scan
- Acceptance estimate: 20-28%

### New evidence gained

1. The archived scan now outputs an explicit `inner_selectivity` metric together with orientation, intervalley, field-angle, and high-barrier contrast summaries.
2. In the current toy interface scan, s-wave becomes a machine-readable failure candidate because it misses three contrast thresholds at once: orientation, intervalley, and field-angle response.
3. The strongest unconventional reference in this round is `chiral_d`, with larger orientation and field-angle contrast than s-wave under the same saved metric logic.

### Why this is still not enough

1. The current response layer is still a surrogate and not yet a BTK-level calculation.
2. The thresholds are useful internal filters, but they are not yet justified as publication-ready discriminants.
3. Robustness against broadening and moderate scan perturbations has not yet been established.

### Shortest repair actions

1. Upgrade the current response model toward a more physical interface-scattering approximation.
2. Re-run the same metrics across broadening and parameter perturbation sweeps.
3. Preserve the same saved summary outputs so later evidence can be compared directly to this first failure candidate.
