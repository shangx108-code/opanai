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
**a,** Required mean photon number `n_bar` needed to achieve a target coherent-boundary discrimination error `epsilon`, comparing the proved lower bound with two concrete measurement-induced routes: a homodyne-conditioned route (solid blue) and a displaced on-off route (dashed red). Color intensity denotes detector efficiency `eta`. For both measurement routes, decreasing `eta` shifts the required photon number upward across the full error window, showing that detector loss imposes a shared global penalty on activation cost within these fixed receiver models.
**b,** The same data plotted as the ratio `n_bar / n_bar^LB`, which isolates the constant-factor overhead above the quantum limit. The displaced on-off route stays closer to the lower bound than the homodyne route across the computed `epsilon = 0.01-0.10` window, with the clearest separation in the low-error regime. The shaded bands are heuristic guides for this benchmark only and are not universal thresholds. No claim is made here that either measurement route is globally optimal over all adaptive receivers, nor that this single-neuron comparison alone determines network-level performance.

## Main-text Results subsection draft
### Proposed subsection title
Same-axis comparison reveals a detector-limited activation frontier

### Insertable Results text
To turn the lower bound into a device-facing design statement, we placed two concrete measurement-induced routes on the same coherent-boundary discrimination axes. Figure 3a compares the proved coherent-state lower bound with a homodyne-conditioned route and a displaced on-off route under finite detector efficiency `eta`. In both receiver families, lowering `eta` shifts the full boundary-cost curve upward: for a fixed target error, the required photon number increases with the familiar `1 / eta` penalty of these models. The first conclusion is therefore architecture-independent within this benchmark. Detector efficiency determines whether the low-error frontier is practically accessible at all.

The architectural choice still matters once `eta` is fixed. Figure 3b shows that the displaced on-off route carries a smaller constant-factor overhead above the lower bound than the homodyne route throughout the computed `epsilon = 0.01-0.10` window. At `epsilon = 0.01`, the displaced on-off route requires `1.224 x`, `1.731 x` and `2.423 x` the lower-bound photon cost for `eta = 0.99`, `0.70` and `0.50`, respectively, whereas the homodyne route requires `1.693 x`, `2.394 x` and `3.352 x`. At the less stringent target `epsilon = 0.10`, the same ratios are `1.591 x`, `2.250 x` and `3.151 x` for displaced on-off counting, versus `1.624 x`, `2.297 x` and `3.215 x` for homodyne. The separation is modest near `epsilon = 0.10` but widens as the target error is pushed lower, which identifies a concrete architecture-dependent prefactor on top of the shared detector penalty.

These comparisons support a bounded design-law statement rather than a universal optimality claim. Within the fixed receiver models studied here, measurement-induced activation approaches the practical energy frontier only in a high-efficiency regime, and even there the remaining overhead depends on the measurement route. We therefore use the lower bound as a design reference, not as a claim that the plotted receivers exhaust all possibilities: detector efficiency sets the global accessibility of the frontier, while measurement architecture sets the distance above it. We do not claim that either concrete route is globally optimal over all adaptive receivers, and we do not infer network-level superiority from this single-neuron benchmark alone.

### Insertable claim sentence
For the concrete receivers computed in Fig. 3, detector efficiency governs whether the activation frontier is accessible at all, while measurement architecture controls the residual constant-factor photon overhead above the coherent-state limit.

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
