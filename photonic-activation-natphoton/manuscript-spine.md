# Manuscript Spine

## Working title
Quantum limits of nonlinear activation in photonic neural networks

## One-sentence claim
Nonlinear activation in photonic neural networks should be treated as a quantum resource problem, and measurement-induced adaptive activation can approach the practical energy frontier only within specific detector-, loss-, and sampling-limited regimes that we quantify explicitly.

## Broad-reader problem statement
Linear optical transforms are already highly efficient and programmable, but scalable nonlinear activation remains the unresolved cost center in photonic neural networks. Without a quantitative resource framework, the field lacks a reliable way to judge when sophisticated photonic or measurement-based activations are genuinely useful.

## Gap against prior work
- Existing photonic neural-network demonstrations establish impressive linear processing and task-level functionality, but they do not supply a common resource metric for nonlinear activation.
- Recent work on nonlinear processing with linear optics and field-programmable photonic nonlinearity narrows the novelty space, so this paper must not claim generic programmability as its advance.
- The paper's distinct contribution is a framework that compares physically different nonlinear routes on common resource, discrimination, and task-performance axes.

## Abstract logic
1. State the field-level promise of photonic neural networks.
2. Identify nonlinear activation as the unresolved physical bottleneck.
3. Introduce activation quantum cost as the central metric.
4. State that multiple activation families are compared within one constrained model.
5. Claim a regime-based result, not unconditional superiority.
6. End with the device/design consequence.

## Introduction logic

### Paragraph 1
Photonic neural networks are attractive because optics performs linear transformations with high bandwidth and potentially low energy.

### Paragraph 2
The unresolved issue is not matrix multiplication but nonlinear activation, which often requires electronic feedback, strong material response, or measurement overhead.

### Paragraph 3
Recent advances have improved photonic programmability and low-light task demonstrations, but the field still lacks a unified criterion for the physical cost of nonlinearity.

### Paragraph 4
This paper asks a sharper question: how much optical resource is required to realize useful nonlinear activation under realistic noise and detector limits?

### Paragraph 5
Preview the answer: define a resource framework, compare activation families, introduce AQMA as a near-frontier architecture, and identify the regimes where measurement-induced activation is or is not worthwhile.

## Results structure

### Result 1
Unified activation framework and metric definitions

### Result 2
Single-neuron resource limits and failure boundaries

### Result 3
AQMA architecture and comparison against baseline activations

### Result 4
Task-level energy-accuracy frontier

### Result 5
Device-feasibility map and experimental route

## Methods backbone
- encoding convention
- detector and noise models
- optical loss accounting
- activation-family parameterization
- optimization procedure for `C_AQC`
- discrimination benchmark construction
- task-level training and inference accounting

## Discussion logic
- What the framework changes for photonic-AI design
- Why some low-photon nonlinear routes are attractive but not universally preferable
- What the present work does not yet claim
- Which experimental validation would be most decisive

## Supplementary burden
- derivation details
- additional baselines
- sensitivity scans
- implementation accounting assumptions
- extra task results that are informative but not main-text essential

## Editorial positioning rule
The paper must read as a physics-guided design framework with quantified limits, not as an ML benchmark paper decorated with photonics language.
