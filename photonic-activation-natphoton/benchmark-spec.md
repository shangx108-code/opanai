# Benchmark Specification

## Objective of this round
Generate the minimum benchmark package that can either support or falsify the paper's main claim.

## Benchmark hierarchy

### Level 1: Single-neuron activation physics
Purpose: determine whether each activation family can realize useful nonlinear responses in the few-photon regime.

Activation families to benchmark:
- electronic ReLU-like activation
- Kerr-like activation
- saturable activation
- photon-counting threshold activation
- homodyne-conditioned activation
- AQMA threshold variant
- AQMA homodyne/Bayesian variant

Target responses:
- sigmoid-like
- tanh-like
- ReLU-like soft threshold
- binary stochastic activation
- saturating activation

Primary outputs:
- activation response curves
- `E_act` versus `n_bar`
- `C_AQC` versus approximation tolerance
- `C_disc` around the turning region

Decision rule:
- An activation family is competitive only if it performs well on approximation and discrimination simultaneously.

### Level 2: Small-network utility benchmark
Purpose: test whether good single-neuron behavior survives at task level.

Recommended tasks:
- two-moons
- concentric circles
- low-light signal discrimination
- optional 4-class low-light image subset after the first three tasks are stable

Network template:
- optical linear layer
- physical activation layer
- optical linear layer
- physical activation layer
- readout

Primary outputs:
- accuracy versus photons per inference
- accuracy versus detector efficiency
- accuracy versus optical loss
- Pareto frontiers for competing activations

Decision rule:
- AQMA is publishable only if it creates a nontrivial design region where it is either best or tied-best under explicit constraints.

### Level 3: Device-feasibility maps
Purpose: convert benchmark results into a photonics-facing design guide.

Parameter scans:
- average photons per neuron: `1e-2` to `1e3`
- detector efficiency `eta`: `0.5` to `0.99`
- dark-count probability per gate: `1e-8` to `1e-3`
- optical loss `ell`: `0` to `10 dB`
- shot budget `N_s`: `1` to `1e5`

Primary outputs:
- energy-accuracy frontier
- detector-efficiency versus loss map
- dark-count sensitivity map
- useful / marginal / not-worth-it operating regions

Decision rule:
- Main-text hardware maps must answer a device question, not merely show colorful parameter scans.

## Common code path requirements

1. Shared encoding convention for all activation families
2. Shared detector and loss models where applicable
3. Shared training protocol for task-level comparisons
4. Shared accounting of optical and measurement resources
5. Reproducible seeds and saved config files

## Minimal repository structure

`quantum_activation/`

- `activations/`
- `detectors/`
- `noise/`
- `tasks/`
- `metrics/`
- `figures/`
- `configs/`

## Validation checks before trusting results

1. Recover the deterministic limit at high photon number where appropriate.
2. Recover monotonic degradation under increasing loss or decreasing efficiency.
3. Confirm that no-activation baselines fail on nonlinear-separable toy tasks.
4. Confirm that reported advantage regions survive at least modest hyperparameter variation.
5. Confirm that any reported frontier shift is not caused by inconsistent accounting.

## First-pass figure burden

- Figure 1: conceptual bottleneck and paper question
- Figure 2: unified activation framework and metric definitions
- Figure 3: `C_AQC` and `C_disc` comparison at single-neuron level
- Figure 4: AQMA versus baselines under realistic detector/loss constraints
- Figure 5: task-level energy-accuracy frontier
- Figure 6: chip-feasibility map

## Fail conditions

The paper should be downgraded from Nature Photonics ambition if any of the following occurs:

1. AQMA never wins or never materially changes the frontier.
2. The framework only restates obvious trade-offs without a new decision boundary.
3. The results depend on unrealistic detector assumptions not defensible for the target audience.
4. Task-level benefits vanish once measurement overhead is counted consistently.
