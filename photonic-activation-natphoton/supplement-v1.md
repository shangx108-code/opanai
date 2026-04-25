# Supplementary Information for "Quantum limits of nonlinear activation in photonic neural networks"

## Scope of this supplement

This supplement packages only the material that is already evidenced inside the Nature Photonics project namespace used in the current run. It does not claim additional simulations, broader benchmarks, adaptive-receiver optimality, or hardware-readiness results beyond the saved manuscript and benchmark files.

## Supplementary Note 1. Definitions used in the main text

The main text models a physical activation channel as

`A_theta : rho_x -> y`

with effective scalar output

`y = E[g_theta(m, u) | rho_x, eta, ell, xi, N_s]`.

The symbols are used exactly as follows.

- `rho_x`: encoded optical state carrying the scalar pre-activation variable `x`
- `m`: measurement outcome when the activation route is measurement-assisted
- `u`: any feed-forward or feedback control variable
- `eta`: detector efficiency
- `ell`: optical loss
- `xi`: nuisance noise not resolved further in the present benchmark
- `N_s`: effective shot budget

For a target nonlinear response `sigma(x)` over the operating domain, the framework file defines the weighted approximation loss

`E_act(theta) = integral w(x) |A_theta(x) - sigma(x)|^2 dx`.

The corresponding activation quantum cost is

`C_AQC(sigma, epsilon) = min_theta { n_bar(theta) : E_act(theta) <= epsilon }`,

where `n_bar` is the mean photon number per activation event at the operating point. The manuscript does not claim that low approximation error alone is sufficient for useful nonlinear activation. For that reason, the single-neuron comparison in the present paper is organized around a discrimination-cost viewpoint rather than around function fitting alone.

The discrimination score for two nearby encoded inputs `x_1` and `x_2` is

`D(x_1, x_2; theta) = |mu_1 - mu_2| / sqrt(var_1 + var_2)`,

with `mu_i = E[y | x_i]` and `var_i = Var[y | x_i]`.

The manuscript-level same-axis comparison then uses a concrete boundary-discrimination proxy and asks how much photon number is needed to reach a target boundary error `epsilon` for three cases: the coherent-state lower bound, a homodyne-conditioned route, and a displaced on-off route.

## Supplementary Note 2. Boundary-cost formulas used for Figure 3

### 2.1 Coherent-state lower bound

The saved comparison code models the boundary states as the coherent pair `|+a>` and `|-a>` with symmetric mean photon number

`n_bar = a^2`.

The lower-bound error used throughout the project is

`epsilon_lb(n_bar) = 1/2 * (1 - sqrt(1 - exp(-4 n_bar)))`.

To obtain the inverse cost curve used in the figure package, solve algebraically for `n_bar`.

Starting from

`2 epsilon = 1 - sqrt(1 - exp(-4 n_bar))`,

we rearrange to

`sqrt(1 - exp(-4 n_bar)) = 1 - 2 epsilon`.

Squaring both sides gives

`1 - exp(-4 n_bar) = (1 - 2 epsilon)^2 = 1 - 4 epsilon + 4 epsilon^2`,

so

`exp(-4 n_bar) = 4 epsilon (1 - epsilon)`.

Taking the logarithm yields the inverse curve used in `same_axis_metrics.py`,

`n_bar^lb(epsilon) = (1/4) ln(1 / (4 epsilon (1 - epsilon)))`.

This is the reference frontier used in the manuscript. The current paper treats it as a lower-bound design reference, not as a statement that all physically interesting receiver families have been exhausted.

### 2.2 Homodyne-conditioned route

For the homodyne proxy, the saved model uses single-shot homodyne measurement along the signal quadrature with detector efficiency `eta` and a zero-threshold decision rule. The corresponding boundary error is

`epsilon_hom(n_bar, eta) = 1/2 * erfc(sqrt(2 eta n_bar))`.

The inverse cost `n_bar^hom(epsilon, eta)` is not written in closed form in the current project files. Instead, `same_axis_metrics.py` computes it by direct numerical inversion of this monotone error curve on the interval `[0, 20]` using binary search. This inversion is therefore genuinely completed numerically, but not symbolically reduced in the present manuscript package.

### 2.3 Displaced on-off route

For the Kennedy-type displaced on-off receiver, the saved note fixes a displacement that nulls the `|+a>` hypothesis so that the post-displacement states are `|0>` and `|-2a>`. With detector efficiency `eta` and dark-count probability `p_d` per activation event, the model error is

`epsilon_ken(n_bar, eta, p_d) = 1/2 * [p_d + (1 - p_d) exp(-4 eta n_bar)]`.

In the no-dark-count case used for the current Figure-3 package, this reduces to

`epsilon_ken(n_bar, eta, 0) = 1/2 * exp(-4 eta n_bar)`.

The inverse cost follows directly:

`2 epsilon = exp(-4 eta n_bar)`,

so

`n_bar^ken(epsilon, eta, 0) = (1 / (4 eta)) ln(1 / (2 epsilon))`.

The code also retains the dark-count-aware inverse

`n_bar^ken(epsilon, eta, p_d) = (1 / (4 eta)) ln((1 - p_d) / (2 epsilon - p_d))`,

which is valid only when `2 epsilon > p_d`. The current manuscript does not use a dark-count sweep in the main text.

### 2.4 Numerical values quoted in the main text

The figure package and manuscript quote the same saved ratios above the lower bound in the `epsilon = 0.01-0.10` window.

- At `epsilon = 0.01`, displaced on-off requires `1.224 x`, `1.731 x`, and `2.423 x` the lower-bound photon cost for `eta = 0.99`, `0.70`, and `0.50`, whereas homodyne requires `1.693 x`, `2.394 x`, and `3.352 x`.
- At `epsilon = 0.10`, displaced on-off requires `1.591 x`, `2.250 x`, and `3.151 x`, whereas homodyne requires `1.624 x`, `2.297 x`, and `3.215 x`.

These values are copied from the already saved same-axis notes and correspond to the figure rendered from `figure3_same_axis_panel.py`.

## Supplementary Note 3. Task-level benchmark assumptions behind Figure 4 prose

The current project contains one real task-level benchmark intended only as the narrowest honest bridge from the single-neuron frontier to a systems-level design consequence. The saved script `task_level_benchmark.py` implements the following object.

- one random linear feature layer
- one noisy threshold-activation layer
- one ridge readout
- two toy nonlinear classification tasks: `two_moons` and `concentric_circles`
- fixed total activation photon budget per inference

The benchmark uses three activation-noise routes.

- `lower_bound`: non-implementable ceiling calibrated directly from the coherent lower-bound curve
- `homodyne`: implementable route with flip probability set by `epsilon_hom(n_bar, eta)`
- `on_off`: implementable route with flip probability set by `epsilon_ken(n_bar, eta, 0)`

For a chosen total activation photon budget `B` and hidden width `W`, the photon number assigned to each activation event is

`n_bar_per_neuron = B / W`.

The script maps the corresponding single-neuron boundary error directly to the per-neuron activation flip probability,

`p_flip = epsilon_route(n_bar_per_neuron, eta)`.

This construction is deliberately narrow. It does not train an end-to-end photonic network, and it does not include a full accounting for detector electronics, modulator latency, or chip-level overhead. Its purpose is only to test whether the route ordering from the single-neuron frontier survives once a fixed activation budget must be divided across a network surrogate.

The current saved benchmark summary supports the following manuscript-safe statements.

- The linear no-activation baseline is `0.882` on `two_moons` and `0.484` on `concentric_circles`.
- On `concentric_circles`, the best implementable activation beats the linear baseline in all `15/15` scanned `(eta, budget)` conditions.
- On `two_moons`, the best implementable activation does not beat the linear baseline in any scanned condition up to total budget `16`.
- Across matched `(task, eta, budget)` settings, on-off beats homodyne in `9/30` comparisons, so task-level route preference is not inherited trivially from the single-neuron ordering.

These claims remain bounded by the saved benchmark definition above and should not be widened into claims of global task superiority or chip-level feasibility.

## Supplementary Note 4. Evidence provenance in the current namespace

The present manuscript and supplement are grounded in the following already existing files inside the Nature Photonics project namespace.

- `manuscript-v1.md`: current main-text manuscript source
- `manuscript-v1.pdf`: first rendered main-text manuscript PDF
- `theory-framework.md`: project-level mathematical framing and metric definitions
- `aqma-homodyne-comparison.md`: same-axis homodyne route note and verified numerical table
- `kennedy-onoff-comparison.md`: same-axis displaced on-off route note and verified numerical table
- `same_axis_metrics.py`: reproducible script for the Figure-3 formulas and tabulated values
- `figure3_same_axis_panel.py`: rendering script for the Figure-3 panel package
- `figure3_same_axis_panel/figure3_same_axis_panel_data.csv`: plotting-ready same-axis data
- `task_level_benchmark_assumptions.md`: benchmark-scope and claim-boundary note
- `task_level_benchmark.py`: reproducible task-level benchmark script
- `task_level_benchmark/task_level_benchmark_summary.md`: benchmark summary used for manuscript prose
- `task_level_benchmark/task_level_benchmark_summary.json`: machine-readable benchmark summary
- `verified-reference-ledger.md`: reference-status ledger used for the checked literature-positioning paragraph

The current supplement does not certify anything beyond those files. In particular, the following remain incomplete after the present run.

- a standalone manuscript-grade Figure 4 panel and caption package
- broader robustness scans beyond the current toy-task benchmark
- a final submission archive bundle

## Supplementary References

1. Bandyopadhyay, A. et al. Single-chip photonic deep neural network with forward-only training. Nature Photonics 18, 1335-1343 (2024).
2. Yildirim, S. et al. Nonlinear processing with linear optics. Nature Photonics 18, 1076-1082 (2024).
3. Wu, X. et al. Field-programmable photonic nonlinearity. Nature Photonics 19, 725-732 (2025).
4. Wang, Z. et al. An optical neural network using less than 1 photon per multiplication. Nature Communications 13, 123 (2022).
5. Ma, Q. et al. Quantum-limited stochastic optical neural networks operating at a few quanta per activation. Nature Communications 16, 359 (2025).
