# Manuscript V0

## Title

Quantum limits of nonlinear activation in photonic neural networks

## Central Claim

Nonlinear activation, rather than linear optical matrix multiplication, sets the decisive resource bottleneck for low-photon photonic neural networks; a unified activation-cost framework can compare physical nonlinear mechanisms on the same energy-versus-functionality axis.

## Supported In This Version

1. The manuscript framing and literature positioning.
2. A first proxy implementation of several activation families within one numerical scaffold.
3. Preliminary evidence that measurement-induced AQMA-like activation can approximate sigmoid-like targets well at low photon budget in the current proxy model.
4. Device-aware scans showing that measurement-induced sigmoid-like activation remains achievable under finite efficiency, loss and dark count in the explored ranges.
5. A Monte Carlo two-moons benchmark showing nontrivial task-level sensitivity to photon budget and device parameters.
6. An analytic lower bound for binary discrimination cost under Poisson counting assumptions.
7. A second weak-signal benchmark showing that measurement-induced activations are competitive but not universally superior.

## Not Yet Supported In This Version

1. A rigorous lower-bound theorem deserving the phrase "quantum limit" in the strongest sense.
2. Task-level evidence on a broader benchmark suite with clearer platform realism.
3. Real device feasibility maps with named detector and photonic-platform windows.

## Abstract V0

Photonic neural networks promise low-latency and energy-efficient information processing, but their practical scalability is constrained by the physical cost of nonlinear activation. We formulate a comparative framework for activation mechanisms in photonic neural networks through an activation-cost viewpoint that tracks function-approximation error against optical resource budget. We implement proxy models for electronic, Kerr-like, saturable, photon-counting and adaptive quantum measurement activations within a common simulation scaffold, then extend the measurement-induced models to include detector efficiency, optical loss and dark count. Across the explored parameter ranges, sigmoid-like targets remain achievable with low photon budgets, whereas binary-like responses are substantially more expensive. A Monte Carlo two-moons benchmark further shows that measurement-induced activations retain useful task-level performance but degrade sharply as device constraints tighten. In parallel, we derive a Poisson discrimination lower bound that gives a rigorous baseline for binary activation cost under counting noise. Together these results support the broader hypothesis that nonlinear activation should be treated as a primary resource bottleneck in few-photon photonic inference, while also clarifying which parts of the "quantum limit" claim are already established and which still require stronger theory.

The current benchmark suite also shows that measurement-induced activation is not a universal winner. On the newly added weak-signal discrimination task, the best deterministic Kerr-like baseline slightly outperforms the current AQMA implementation, while AQMA still improves modestly with photon budget over threshold photon counting. This contrast strengthens the manuscript's intended positioning as a comparative framework with bounded claims.

## Introduction Closing Paragraph V0

Here we study nonlinear activation as a photonic resource-allocation problem rather than as an isolated device function. Our aim is not to introduce yet another architecture-specific optical neural network, but to establish a comparative framework that asks how much optical resource is required to realize a target nonlinear response under realistic noise, loss and detection constraints. This framing lets us compare material, measurement-induced and hybrid activation mechanisms on a common footing and identify when quantum measurement becomes a useful nonlinear resource in the few-photon regime.

## Results Opening Paragraph V0

We first built a minimal comparative simulation environment containing five activation families: ideal electronic rectification, Kerr-like response, saturable response, threshold photon counting and adaptive quantum measurement activation. In the present version, these models are used as controlled proxies rather than full hardware-faithful device models. Even at this stage, the scan separates target-function classes. Kerr-like response best matches tanh-like targets in the current proxy study, whereas photon-counting and AQMA-like models achieve the strongest low-budget fits for sigmoid-like activation. This separation is important because it suggests that the relevant comparison is not "which activation is universally best" but "which physical nonlinearity reaches the desired response class with the lowest resource cost."

## Results Note V1

The current data support a more nuanced Results section than the original concept note suggested. On the two-moons benchmark, measurement-induced activations improve steadily with photon budget and approach high accuracy by 3-10 photons, which is consistent with the idea that low-budget nonlinear resources can still be useful for curved decision boundaries. By contrast, on the weak-signal discrimination benchmark, deterministic Kerr-like activation remains strongest in the present setup, while AQMA provides only a modest improvement over threshold photon counting at higher budgets. This contrast is scientifically useful rather than disappointing: it shows that activation-resource conclusions depend on task class and target nonlinearity, which strengthens the paper's case for a comparative framework.
