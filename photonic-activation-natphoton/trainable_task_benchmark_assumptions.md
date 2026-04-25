# Trainable Task-Level Benchmark Assumptions

## Purpose
Upgrade the earlier random-feature surrogate to the smallest trainable-network benchmark that still preserves the paper's activation photon-budget accounting.

## What changed relative to the previous benchmark
- The hidden layer is now trainable rather than fixed random features.
- The linear baseline is now a trainable linear classifier rather than a ridge readout on raw inputs.
- The activation noise is still set directly by the Figure-3 boundary-error curves, so the route-dependent photonic physics is unchanged.

## Benchmark object
- One trainable linear input layer
- One trainable threshold-like hidden activation layer
- One trainable readout
- Two toy nonlinear classification tasks: `two_moons` and `concentric_circles`
- Fixed total activation photon budget per inference

## Physical accounting kept fixed
- For hidden width `W` and total activation budget `B`, each activation event receives
  `n_bar_per_neuron = B / W`.
- The activation flip probability is still tied directly to the single-neuron error models:
  - `lower_bound`
  - `homodyne`
  - `on_off`
- Detector efficiency `eta` enters only through those same route-error curves.

## Training rule
- Training uses a smooth surrogate for the noisy threshold activation:
  `a_train = epsilon + (1 - 2 epsilon) sigmoid(beta z)`.
- Evaluation switches back to the physical benchmark rule:
  threshold the hidden pre-activation and then flip each hidden unit independently with probability `epsilon`.
- This keeps optimization numerically stable while ensuring that reported validation and test accuracies are measured with the actual route-dependent physical noise model.

## What this benchmark is allowed to claim
- Whether the previous random-feature conclusion survives once the hidden layer is trained.
- Whether paying for photonic activation still depends on detector efficiency and total photon budget after task adaptation is allowed.
- Whether route preference remains nontrivial after training.

## What this benchmark is not allowed to claim
- It does not prove full end-to-end photonic training with device-realistic backpropagation.
- It does not include detector electronics, control latency, or modulator-energy overhead beyond the optical activation budget.
- It does not establish large-scale dataset generality.
- It does not certify hardware feasibility by itself.

## Completion standard for this round
- A real script must run from the current workspace and save reproducible outputs.
- The saved summary must compare against a trainable linear baseline.
- The conclusion must identify both regimes where activation is worthwhile and regimes where it is still not justified.
