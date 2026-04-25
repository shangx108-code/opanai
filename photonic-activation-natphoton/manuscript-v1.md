# Quantum limits of nonlinear activation in photonic neural networks

## Abstract

Photonic neural networks are compelling because optics performs linear transformations with high bandwidth and potentially low energy, but scalable nonlinear activation remains the unresolved physical cost centre. Recent photonic-AI advances have demonstrated integrated nonlinear layers, nonlinear processing synthesized from nominally linear optics, and field-programmable nonlinear photonic hardware. These results establish that photonic nonlinearity is possible and increasingly hardware relevant, yet they do not provide a common physical accounting of nonlinear activation cost across distinct implementations, nor do they determine when paying that cost changes task-level design choices under detector inefficiency, optical loss and finite-shot constraints. Here we treat nonlinear activation itself as a quantum-resource problem. We define activation quantum cost and discrimination-cost metrics, compare a coherent-state lower bound with two implementable measurement-induced routes on common axes, and then test whether the resulting single-neuron frontier changes design choices under a fixed activation photon budget. In the computed benchmark, detector efficiency sets whether the low-error activation frontier is practically accessible at all, while measurement architecture controls the residual constant-factor overhead above the lower bound. A minimal task-level benchmark then shows a mixed systems consequence: for concentric circles, paying for activation improves over the linear baseline in all 15 of 15 scanned detector-efficiency and budget settings, whereas for two moons no implementable activation beats the linear baseline up to the largest scanned budget. These results support a bounded design rule for photonic neural nonlinearities: the relevant choice depends jointly on detector efficiency, finite-shot overhead, task geometry and the strength of the linear baseline, rather than on a single-neuron frontier alone.

## Introduction

Photonic neural networks are attractive because optics can execute linear transformations with high bandwidth and potentially low optical energy. Across integrated and free-space platforms, this strength has made photonic hardware a serious candidate for acceleration of inference and learning workloads. The main unresolved cost centre, however, is not linear matrix multiplication itself. It is the realization of nonlinear activation under realistic noise, loss and sampling constraints.

In practice, nonlinear activation in photonic neural networks is often supplied by optoelectronic detection and feedback, strong material response, or measurement-conditioned logic. Each route carries a different penalty in optical resource, detector efficiency, calibration overhead or latency. Without a common physical accounting, it is difficult to tell when a sophisticated photonic activation is genuinely useful and when the system should instead rely on linear processing or a different nonlinear route.

Recent photonic-AI advances have substantially tightened the design space for optical nonlinear processing. Integrated coherent processors now combine optical matrix algebra, on-chip nonlinear activation and in situ training on a single chip; scattering-based systems show that nominally linear optical elements can be arranged to realize nonlinear processing at low power; and field-programmable nonlinear microprocessors demonstrate dynamically reconfigurable polynomial photonic networks. These results establish that photonic nonlinearity is possible and increasingly hardware relevant, but they answer a different question from the one addressed here. They do not provide a common physical accounting of nonlinear activation cost across distinct implementations, nor do they determine when paying that cost changes task-level design decisions under detector inefficiency, optical loss and finite-shot sampling. Here we therefore treat nonlinear activation itself as a quantum-resource problem. We place a lower bound and two implementable measurement-induced routes on the same discrimination-cost axes, and then test whether the resulting single-neuron frontier changes the preferred design once the total activation photon budget is fixed at task level.

The manuscript asks a narrower and more device-facing question than generic programmability or generic nonlinear functionality: how much optical resource is required to realize useful nonlinear activation, and when does paying for that activation alter the preferred photonic design? The answer developed below is intentionally bounded. Detector efficiency determines whether the low-error activation frontier is practically accessible in the computed receiver models, while measurement architecture controls the remaining constant-factor overhead above that frontier. At task level, the preferred route depends not only on closeness to the single-neuron bound, but also on task geometry and width-budget trade-off once a fixed activation photon budget is enforced.

## Framework

We model a physical activation channel as a constrained transformation from an encoded optical input state to an effective scalar response,

`A_theta : rho_x -> y,`

with output

`y = E[g_theta(m, u) | rho_x, eta, ell, xi, N_s].`

Here `m` is the measurement outcome when present, `u` is any control signal generated by feed-forward or feedback, `eta` is detector efficiency, `ell` denotes optical loss, `xi` collects nuisance noise sources, and `N_s` is the effective shot budget. This language is broad enough to cover thresholded photon counting, homodyne-conditioned activation, adaptive measurement-assisted routes and material nonlinearities, while keeping detector and sampling penalties explicit.

For a target nonlinear response `sigma(x)`, we define an activation quantum cost

`C_AQC(sigma, epsilon) = min_theta { n_bar(theta) : E_act(theta) <= epsilon },`

where `n_bar` is the mean photon number per activation event and `E_act` is a weighted approximation loss over the operating domain. Because low approximation error alone does not guarantee useful physical discrimination, we also track a discrimination-cost metric that asks for the minimum optical resource required to exceed a chosen discrimination threshold near the activation turning region. The present manuscript uses this discrimination-based viewpoint to compare a coherent-state lower bound against two implementable measurement-induced routes: a homodyne-conditioned route and a displaced on-off route.

This framing sets the logic of the Results. Figure 3 is not introduced as a new hardware demonstration, but as a cross-architecture resource comparison that isolates the penalties attached to nonlinear activation itself. Figure 4 then asks whether the single-neuron ordering revealed by Fig. 3 survives when a finite activation budget must be shared across a network. The central claim of the manuscript is the combination of these two steps: first, detector efficiency determines whether a measurement-induced activation frontier is practically accessible, and second, closeness to that frontier does not by itself determine whether paying for activation is worthwhile for a given task.

## Results

### Same-axis comparison reveals a detector-limited activation frontier

To convert the lower bound into a device-facing statement, we place two concrete measurement-induced routes on the same coherent-boundary discrimination axes. Figure 3a compares the proved coherent-state lower bound with a homodyne-conditioned route and a displaced on-off route under finite detector efficiency `eta`. In both receiver families, lowering `eta` shifts the full boundary-cost curve upward, so that the photon requirement rises with the expected `1 / eta` penalty of these fixed models. The first conclusion is therefore shared across architectures within this benchmark: detector efficiency sets whether the low-error activation frontier is practically accessible at all.

Architecture still matters once `eta` is fixed. Figure 3b shows that the displaced on-off route remains closer to the lower bound than the homodyne route throughout the computed `epsilon = 0.01-0.10` window, but only by a regime-dependent constant factor rather than by a change in scaling. At `epsilon = 0.01`, the displaced on-off route requires `1.224 x`, `1.731 x` and `2.423 x` the lower-bound photon cost for `eta = 0.99`, `0.70` and `0.50`, whereas the homodyne route requires `1.693 x`, `2.394 x` and `3.352 x`. At the less stringent target `epsilon = 0.10`, the corresponding ratios are `1.591 x`, `2.250 x` and `3.151 x` for displaced on-off counting, versus `1.624 x`, `2.297 x` and `3.215 x` for homodyne. The gap is therefore modest near `epsilon = 0.10` but widens in the low-error regime, which identifies a concrete architecture-dependent prefactor on top of the shared detector penalty.

The design statement supported by Fig. 3 is intentionally bounded. Within the receiver models computed here, measurement-induced activation approaches the practical frontier only in a high-efficiency regime, and even there the residual distance from the lower bound depends on the measurement route. We therefore use the lower bound as a design reference rather than as evidence that the plotted receivers exhaust all possibilities: detector efficiency controls global accessibility of the frontier, while receiver choice controls the remaining constant-factor overhead above it.

![Figure 3. Same-axis boundary-cost comparison for measurement-induced photonic activation. Panel a shows the required mean photon number needed to achieve a target coherent-boundary discrimination error for the lower bound, homodyne-conditioned route and displaced on-off route at three detector efficiencies. Panel b replots the same data as the overhead ratio above the lower bound, highlighting a shared detector-limited penalty and a route-dependent constant-factor overhead within the fixed receiver models.](figure3_same_axis_panel/figure3_same_axis_panel.png)

### Task-level utility depends on task geometry as well as neuron-level frontier cost

The literature separation above is essential for interpreting the transition from Fig. 3 to Fig. 4. Prior work already establishes that photonic nonlinear processing can be implemented in several ways, including integrated on-chip activations, scattering-based nonlinear mappings and few-photon stochastic detection. Our contribution is different in scope. Figure 3 asks how far concrete measurement-induced routes sit above a common activation frontier, whereas Fig. 4 asks whether that neuron-level ordering survives once total activation budget must be distributed across a task. This systems test is needed because a route that is closer to the single-neuron bound can still lose once width allocation and activation reliability compete for the same photons.

We next enforce a fixed total activation photon budget per inference in a minimal random-feature classifier and ask whether the single-neuron frontier changes system-level design conclusions. The benchmark is intentionally narrow: one random linear feature layer, one noisy threshold-activation layer whose flip probability is set directly by the Fig. 3 boundary-error curves, and a ridge readout evaluated on two toy nonlinear classification tasks. Even in this limited setting, the answer is already mixed in a way that matters for journal-level positioning.

For `concentric_circles`, where the linear baseline is weak (`0.484` test accuracy), paying for physical activation is worthwhile in all `15/15` scanned detector-efficiency and budget conditions. The best implementable route reaches `0.766` at `eta = 0.99` and budget `8`, `0.795` at `eta = 0.70` and budget `16`, and `0.654` at `eta = 0.50` and budget `8`, all above the linear baseline by margins of `0.283`, `0.311` and `0.170`, respectively. For `two_moons`, by contrast, the linear baseline is already strong (`0.882`), and the best implementable activation does not exceed it anywhere in the scanned range up to budget `16`; even the best near-miss, `0.878` for displaced on-off at `eta = 0.99`, budget `16`, remains slightly below the linear model. Paying for activation is therefore not a generic good. It depends on whether the task geometry offers nonlinear gain large enough to overcome reliability loss from finite detector efficiency and finite shots.

The preferred implementable route is also not inherited trivially from Fig. 3. Although displaced on-off counting is often closer to the single-neuron lower bound, it wins only `9/30` matched `(task, eta, budget)` comparisons in the task-level scan. Homodyne becomes the better route in most `concentric_circles` settings because the optimum width-budget trade-off shifts in its favour. Figure 4 therefore supplies the manuscript's systems-level conclusion: the neuron-level frontier changes real design choices, but closeness to that frontier alone does not determine which activation route is best once total photon budget and task geometry are included.

![Figure 4. Task-level worth of physical activation depends on task geometry, detector efficiency and total photon budget. Panels a and b show the best implementable test-accuracy margin above the task-specific linear no-activation baseline against total activation photon budget per inference for `two_moons` and `concentric_circles`, respectively. Each point selects the better of the two implementable activation routes at that `(task, eta, budget)` setting, with line color denoting detector efficiency `eta`, marker shape denoting whether homodyne or displaced on-off counting is preferred, and width labels denoting the selected hidden-layer width. Panel c shows the displaced-on-off minus homodyne accuracy difference over the same `30` matched settings, making explicit that route preference is task dependent and is not inherited trivially from the single-neuron frontier.](figure4_task_level_panel/figure4_task_level_panel.png)

## Discussion

Taken together, the single-neuron comparison and the task-level benchmark separate three questions that are often conflated in photonic-AI discussions: whether a nonlinear response can be realized, how far above the physical frontier a given realization sits, and whether paying for that response is justified for the target task. Recent hardware advances answer the first question increasingly well. The present framework addresses the second and third.

This analysis does not imply that measurement-induced activation is universally optimal, nor that low-photon activation automatically yields end-to-end system advantage. Instead, it provides a stricter design rule: the relevant decision depends jointly on detector efficiency, finite-shot overhead, task geometry and the strength of the linear baseline. That conclusion is precisely why the mixed positive-and-negative task-level result matters. A paper that reported only a positive task would look like a selective demonstration; the present split shows that the same accounting can also tell designers when activation is not worth paying for.

The evidence remains deliberately bounded. The task benchmark is a stylized random-feature surrogate rather than a trained end-to-end photonic network, and the measurement routes studied here are concrete receiver models rather than an exhaustive search over adaptive architectures. The manuscript therefore supports a framework-and-design-law contribution, not a universal optimality theorem or a full hardware-readiness claim.

## Methods

### Activation accounting

The pre-activation scalar is encoded into an optical state `rho_x`, and each activation route is assigned a mean photon cost `n_bar` at the operating point of interest. Detector efficiency `eta`, optical loss and finite-shot sampling are treated as explicit parameters rather than absorbed into a generic noise term. For the same-axis comparison, the coherent-state lower bound serves as the reference frontier and two implementable receiver models are evaluated against it over `epsilon = 0.01-0.10`.

### Single-neuron comparison

The comparison data used in Fig. 3 were generated from the saved analytical models in `same_axis_metrics.py` and rendered using `figure3_same_axis_panel.py`. Panel a reports required mean photon number versus target boundary error, and panel b reports the ratio to the lower bound. The present manuscript uses those data only within the computed efficiency window and does not extrapolate beyond the fixed receiver models already evaluated.

### Task-level benchmark

The task-level scan uses a minimal random-feature classifier consisting of one random linear feature layer, one noisy threshold-activation layer and a ridge readout. Activation noise is injected by mapping the Figure-3 boundary-error curves directly to per-neuron flip probabilities. A fixed total activation photon budget per inference is imposed, so widening the hidden layer reduces the photons available per neuron. The scanned tasks are two moons and concentric circles, chosen to test a strong-linear-baseline case and a weak-linear-baseline case under the same accounting rules.

Figure 4 is rendered directly from the saved task-level benchmark summary using `figure4_task_level_panel.py`. Panels a and b report the accuracy margin of the best implementable activation route above the task-specific linear baseline as a function of total activation photon budget, while panel c reports the displaced-on-off minus homodyne accuracy difference over the same matched settings. The manuscript uses these results only within the scanned `(task, eta, budget)` grid and does not promote them to a hardware-feasibility map or a full-network optimality claim.

## Data and code availability

All evidence described here comes from the project namespace used in this run, including the analytical comparison scripts, rendered Figure-3 outputs, the saved task-level benchmark summary tables, and the rendered Figure-4 package. The current paper package includes a main-text manuscript source/PDF and a paired supplementary source/PDF assembled from those already generated materials. Broader robustness scans and a final submission archive remain incomplete.

## References

1. Bandyopadhyay, A. et al. Single-chip photonic deep neural network with forward-only training. Nature Photonics 18, 1335-1343 (2024).
2. Yildirim, S. et al. Nonlinear processing with linear optics. Nature Photonics 18, 1076-1082 (2024).
3. Wu, X. et al. Field-programmable photonic nonlinearity. Nature Photonics 19, 725-732 (2025).
4. Wang, Z. et al. An optical neural network using less than 1 photon per multiplication. Nature Communications 13, 123 (2022).
5. Ma, Q. et al. Quantum-limited stochastic optical neural networks operating at a few quanta per activation. Nature Communications 16, 359 (2025).
