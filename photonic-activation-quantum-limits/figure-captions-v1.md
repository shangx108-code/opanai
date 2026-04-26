# Figure Captions V1

Last updated: 2026-04-26

## Figure: Energy-Accuracy Frontier

Real Monte Carlo benchmark results for measurement-induced activation in two representative tasks. Left: two-moons classification after a fixed random linear projection and ridge readout. Right: weak-signal discrimination using low-intensity multi-mode inputs with Poisson sampling and analog noise. For each photon budget, the plotted AQMA and photon-counting points show the best accuracy obtained across the explored detector efficiency, loss and dark-count settings. The two-moons task exhibits strong improvement with photon budget, reaching about 0.98 accuracy by 10 photons. The weak-signal task is substantially harder and yields only modest gains, with AQMA improving from about 0.51 to 0.54 across the same budget range. These real-data contrasts indicate that measurement-induced activation is task-dependent rather than universally dominant.

## Figure: Device Budget Heatmap

Minimum photon budget required to achieve activation-approximation error 0.01 for sigmoid-like targets at fixed dark count 0.01. Each cell is taken directly from the numerical scan over detector efficiency and optical loss. Lower photon budgets cluster in the high-efficiency, low-loss corner. Comparing AQMA and threshold photon counting shows that both mechanisms remain low-budget for sigmoid-like targets in the explored regime, whereas the corresponding binary-target scans are much more costly and are not shown here for visual clarity.

## Figure: Discrimination Bound

Analytic lower bound on the input-photon requirement for binary discrimination under Poisson counting noise. The curves are evaluated from the closed-form bound in the current Methods note for several representative efficiency-loss-dark-count settings. The bound rises rapidly with target SNR and shifts upward under reduced efficiency or additional loss, quantifying a resource floor that any binary-like activation mechanism must confront in the counting-limited regime.
