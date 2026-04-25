# Figure 4 Minimal Benchmark Package

## Purpose
Convert the Figure-3 single-neuron frontier into the first real task-level consequence test.

## Benchmark object
- Script: `task_level_benchmark.py`
- Outputs folder: `task_level_benchmark/`
- Tasks: `two_moons` and `concentric_circles`
- Model: one random linear feature layer, one noisy threshold-activation layer, ridge readout
- Constraint: fixed total activation photon budget per inference
- Implementable routes compared:
  - homodyne-conditioned activation
  - displaced on-off activation
- Oracle ceiling retained only as a non-implementable reference:
  - lower-bound-calibrated activation

## Key numerical findings from the saved run

### Linear no-activation baseline
- `two_moons`: `0.882` test accuracy
- `concentric_circles`: `0.484` test accuracy

### When activation is worth paying for
- On `concentric_circles`, the best implementable activation beats the linear baseline in all `15/15` scanned `(eta, budget)` conditions.
- Example gains:
  - `eta = 0.99`, budget `8`: homodyne reaches `0.766` versus linear `0.484`
  - `eta = 0.70`, budget `16`: homodyne reaches `0.795` versus linear `0.484`
  - `eta = 0.50`, budget `8`: on-off reaches `0.654` versus linear `0.484`

### When activation is not yet worth paying for
- On `two_moons`, the best implementable activation does not beat the linear baseline in any scanned condition up to budget `16`.
- The best gap at the top of the scan is still slightly negative:
  - `eta = 0.99`, budget `16`: on-off `0.878` versus linear `0.882`
  - `eta = 0.70`, budget `16`: on-off `0.847` versus linear `0.882`
  - `eta = 0.50`, budget `16`: homodyne `0.815` versus linear `0.882`

### Route preference is task dependent
- Although Figure 3 shows that displaced on-off is often closer to the single-neuron lower bound than homodyne, the task-level benchmark does not give a universal on-off win.
- In the scanned conditions, on-off beats homodyne in `9/30` matched `(task, eta, budget)` comparisons.
- Homodyne is the best implementable route in most `concentric_circles` conditions because the optimum width-budget trade-off shifts in its favor.
- On-off becomes the best implementable route only in a subset of higher-budget conditions, such as:
  - `concentric_circles`, `eta = 0.50`, budget `8`
  - `concentric_circles`, `eta = 0.99`, budget `16`
  - several `two_moons` conditions where it still fails to beat the linear baseline

## Manuscript-safe interpretation
- The Figure-3 neuron-level frontier does change system-level design conclusions in a bounded but real way.
- The first task-level consequence is not "measurement-induced activation always wins".
- The defensible claim is narrower and stronger:
  whether activation is worth paying for depends on task geometry, and the single-neuron ranking between implementable routes does not transfer trivially to system-level preference once total photon budget is fixed.

## Allowed claims
- The project now has one real task-level benchmark, not only a planned one.
- A nonlinear toy task with a weak linear baseline can justify paying for activation over the scanned budget range.
- A task that is already largely linearly separable may not justify activation even when the oracle ceiling suggests some remaining headroom.
- Task-level route preference can differ from single-neuron closeness-to-bound because width allocation and activation reliability trade off against each other.

## Disallowed claims
- Do not claim full-network superiority.
- Do not claim homodyne is globally better than on-off.
- Do not claim the toy-task result is already a chip-level feasibility map.
- Do not present the lower-bound-calibrated route as a physically implementable architecture.

## Immediate use in the manuscript
- This package can anchor a first Figure-4 narrative:
  "Task-level utility depends jointly on photon budget, detector efficiency, and task geometry; the best implementable activation route is not determined by the single-neuron frontier alone."
- The next stronger result should keep the same accounting but replace the random-feature surrogate with one tighter benchmark or add a verified literature-positioning subsection that explains why this negative-plus-positive task split matters for Nature Photonics readers.
