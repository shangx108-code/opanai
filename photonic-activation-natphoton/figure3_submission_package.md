# Figure 3 Submission Package

## Objective of this package
- Convert the completed three-curve same-axis comparison into one main-text figure object plus one Results-ready narrative block.
- Keep the claim bounded to the models actually computed in this project.

## Figure contents

### Panel a
- Horizontal axis: target boundary error `epsilon` over `0.01-0.10` on a log scale.
- Vertical axis: required mean photon number `n_bar`.
- Curves shown:
  - coherent-state lower bound
  - homodyne-conditioned route at `eta = 0.99, 0.70, 0.50`
  - displaced on-off route at `eta = 0.99, 0.70, 0.50`

### Panel b
- Horizontal axis: target boundary error `epsilon` over `0.01-0.10`.
- Vertical axis: penalty ratio `n_bar / n_bar^LB`.
- Shaded interpretation bands used only for reader guidance within this benchmark:
  - `1.0-1.4`: near-frontier
  - `1.4-2.0`: moderate overhead
  - `> 2.0`: detector-limited regime

## Caption draft
**Figure 3 | Same-axis boundary-cost comparison for measurement-induced photonic activation.**
**a,** Required mean photon number `n_bar` needed to achieve a target coherent-boundary discrimination error `epsilon`, comparing the proved lower bound with two concrete measurement-induced routes: a homodyne-conditioned route (solid blue) and a displaced on-off route (dashed red). Color intensity denotes detector efficiency `eta`. Both measurement routes move away from the lower bound as `eta` decreases, showing that detector loss imposes a shared global penalty on activation cost.
**b,** The same data plotted as the ratio `n_bar / n_bar^LB`, which isolates the constant-factor overhead above the quantum limit. The displaced on-off route is closer to the lower bound than the homodyne route in the low-error regime, while both routes enter a detector-limited region when `eta` is reduced. The shaded bands provide a visual guide to near-frontier, moderate-overhead and detector-limited operation within this benchmark only. No claim is made here that either measurement route is globally optimal over all adaptive receivers.

## Main-text Results subsection draft
### Proposed subsection title
Same-axis comparison reveals a detector-limited activation frontier

### Insertable Results text
To convert the lower bound into a device-facing design statement, we placed two concrete measurement-induced routes on the same coherent-boundary discrimination axes. Figure 3a compares the proved lower bound with a homodyne-conditioned route and a displaced on-off route under finite detector efficiency `eta`. Both routes inherit a strong global penalty as `eta` decreases, because the required photon number to reach a fixed target error grows approximately as `1 / eta` in these models. This means that detector quality controls whether the frontier is globally accessible at all, independent of the detailed measurement architecture.

The architectural choice still matters once `eta` is fixed. Figure 3b shows that the displaced on-off route carries a smaller constant-factor overhead above the lower bound than the homodyne route throughout the computed low-error window. At `epsilon = 0.01`, the displaced on-off route requires `1.224 x`, `1.731 x` and `2.423 x` the lower-bound photon cost for `eta = 0.99`, `0.70` and `0.50`, respectively, whereas the homodyne route requires `1.693 x`, `2.394 x` and `3.352 x`. At the more forgiving target `epsilon = 0.10`, the same ratios are `1.591 x`, `2.250 x` and `3.151 x` for displaced on-off counting, versus `1.624 x`, `2.297 x` and `3.215 x` for homodyne. The two routes therefore share the same detector-driven scaling penalty, but they remain separated by a non-negligible architecture-dependent prefactor.

These comparisons support a bounded design-law statement rather than a universal optimality claim. Within this benchmark, measurement-induced activation approaches the practical energy frontier only in a high-efficiency regime, and even there the remaining overhead depends on the measurement route. We therefore interpret the lower bound as a usable design reference: detector efficiency sets the global accessibility of the frontier, while measurement choice sets the distance above it. We do not claim that either concrete route is globally optimal over all adaptive receivers, nor that this single-neuron boundary benchmark alone determines full-network task accuracy.

## Allowed and disallowed claims

### Allowed
- Detector efficiency sets the dominant shared penalty for both measured routes in this benchmark.
- Measurement architecture changes the constant-factor overhead above the lower bound.
- The displaced on-off route is closer to the lower bound than the homodyne route over the computed `epsilon = 0.01-0.10` window.
- The comparison yields a main-text design law for when measurement-induced activation is near-frontier versus detector-limited.

### Not allowed
- "The displaced on-off route is globally optimal."
- "AQMA is proven optimal."
- "The single-neuron frontier directly guarantees network-level superiority."
- Any statement implying that the shaded bands are universal thresholds outside this benchmark.

## Provenance
- Numerical source: `same_axis_metrics.py`
- Figure generator: `figure3_same_axis_panel.py`
- Figure outputs:
  - `figure3_same_axis_panel/figure3_same_axis_panel.svg`
  - `figure3_same_axis_panel/figure3_same_axis_panel.png`
  - `figure3_same_axis_panel/figure3_same_axis_panel.pdf`
  - `figure3_same_axis_panel/figure3_same_axis_panel_data.csv`

## What remains after this package
- Verified literature-positioning paragraph against the strongest 2024-2025 photonic nonlinearity papers
- Task-level benchmark evidence linking the single-neuron frontier to system-level design choices
