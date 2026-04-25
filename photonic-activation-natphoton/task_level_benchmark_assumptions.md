# Minimal Task-Level Benchmark Assumptions

## Purpose
Build the narrowest honest bridge from the Figure-3 single-neuron boundary-cost result to a system-level design consequence.

## What this benchmark does
- It uses a one-hidden-layer random-feature classifier on two standard nonlinear toy tasks: two-moons and concentric circles.
- Each hidden unit is treated as a threshold-like physical activation event.
- The activation flip probability is not fitted freely; it is set directly by the Figure-3 boundary-error models:
  - lower-bound ceiling
  - homodyne-conditioned route
  - displaced on-off route
- The total activation photon budget per inference is fixed, so increasing width reduces photons available per hidden unit.

## Why this bridge is theoretically acceptable
- Figure 3 already quantifies how much photon budget is needed to realize a noisy threshold decision around a boundary.
- A hidden threshold activation in a small classifier is the minimal system-level object that uses exactly such boundary decisions repeatedly.
- Fixing the total photon budget converts the single-neuron frontier into a real width-versus-reliability trade-off at the network level.
- The resulting benchmark therefore answers one concrete question:
  under a fixed activation-energy budget, does the preferred system design change when the activation route moves away from the lower frontier?

## What this benchmark is allowed to claim
- Whether the on-off and homodyne routes lead to different best accuracies under the same total activation budget.
- Whether paying for physical activation beats a linear no-activation baseline in the scanned toy-network setting.
- Whether detector efficiency changes the budget range where activation becomes worthwhile.

## What this benchmark is not allowed to claim
- It does not prove global optimality of any activation architecture.
- It does not prove end-to-end superiority for realistic large photonic neural networks.
- It does not yet compare against full electronic-activation energy accounting.
- It does not convert the toy-task result into a chip-level feasibility statement by itself.

## Completion standard for this round
- A real script must run from the current workspace.
- The run must save reproducible task-level outputs.
- The summary must state both positive regions and negative regions where activation is not worth paying for.
