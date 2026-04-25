# Figure 4 Trainable Benchmark Package

## Goal of this package
Replace the earlier random-feature-only Figure-4 evidence with a tighter trainable-network benchmark under the same activation photon-budget accounting.

## Real assets produced in this run
- Reproducible benchmark script: `trainable_task_benchmark.py`
- Saved outputs in `trainable_task_benchmark/`
- Assumptions and claim-boundary note: `trainable_task_benchmark_assumptions.md`

## Benchmark definition
- Trainable linear input layer
- Trainable hidden threshold-like activation layer
- Trainable readout
- Tasks: `two_moons` and `concentric_circles`
- Route-dependent activation noise taken directly from Figure-3 boundary-error curves
- Fixed total activation photon budget per inference

## Linear baseline used here
- `two_moons`: `0.866`
- `concentric_circles`: `0.566`

## Manuscript-safe headline conclusions
1. The task-level design consequence survives hidden-layer training. The Figure-3 route physics is not washed out when the hidden representation is allowed to adapt.
2. Paying for activation is no longer a circles-only effect. In this tighter benchmark, the best implementable activation beats the trainable linear baseline in `22/30` scanned `(task, eta, budget)` settings.
3. The dependence on detector efficiency and photon budget remains real. Activation is still not justified in `8/30` scanned settings, all on `two_moons` at low or intermediate total budgets.
4. Route preference remains regime dependent rather than universal. On-off beats homodyne in `14/30` matched comparisons, so the best route still depends on task and budget even after training.

## Most useful positive regimes
- `two_moons`, `eta = 0.99`, budget `8`: on-off reaches `0.974` versus linear `0.866`.
- `two_moons`, `eta = 0.70`, budget `16`: on-off reaches `0.981` versus linear `0.866`.
- `concentric_circles`, `eta = 0.99`, budget `4`: on-off reaches `0.939` versus linear `0.566`.
- `concentric_circles`, `eta = 0.50`, budget `16`: homodyne reaches `0.974` versus linear `0.566`.

## Negative or near-negative regimes that must remain in the manuscript
- `two_moons`, `eta = 0.50`, budget `1`: best physical route reaches only `0.711` versus linear `0.866`.
- `two_moons`, `eta = 0.99`, budget `2`: best physical route is essentially tied with linear (`0.864` versus `0.866`).
- `two_moons`, `eta = 0.70`, budget `4`: the best gain is only `0.013`, which is below the manuscript's "clearly worth paying for" margin.

## Reviewer-safe interpretation
- The stronger benchmark improves the system-level evidence materially because the hidden representation is trained rather than frozen.
- The result should still be framed as a small trainable benchmark, not as a full end-to-end photonic-learning demonstration.
- The main design rule should now read:
  under fixed activation photon budget, the usefulness of photonic activation depends jointly on task geometry, detector efficiency, total budget, and receiver choice, and this dependence survives after the hidden layer is trained.

## Immediate manuscript insertion targets
- Replace the earlier Figure-4 prose that emphasizes only the random-feature surrogate.
- Add one sentence in the Results stating that the mixed route-and-budget dependence persists after hidden-layer training.
- Keep the Discussion explicit that large-scale task generality and full control-overhead accounting remain outside the current evidence package.
