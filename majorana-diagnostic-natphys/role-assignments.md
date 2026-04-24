# Role Assignments

## Coordinator
- Current task: lock the main claim around the diagnostic hierarchy and supervise the next benchmark round
- Inputs: source note, venue criteria, verified 2026 overlap, manuscript package
- Deliverable: updated project brief and execution order
- Completion standard: the project has one primary claim, one primary rejection risk, and one primary next experiment/calculation block
- Dependency: none

## Theory
- Current task: formalize the diagnostic hierarchy and state the failure boundary of each observable
- Inputs: BdG model family, Green-function formalism, scattering-matrix invariant, disorder and impurity extensions, manuscript draft
- Deliverable: concise theory note plus theorem-like statement or protocol statement
- Completion standard: the manuscript can say exactly which combination of observables is needed and what each one excludes
- Dependency: coordinator framing

## Code and Numerical Computation
- Current task: replace the toy-model stress test with a full transport benchmark
- Inputs: unified Hamiltonian, lead self-energies, parameter grids, disorder sampler, false-positive controls
- Deliverable: scripts/results for `G_LL`, `G_RR`, `G_LR`, gap evolution, `Q`, LDOS, and robustness scans
- Completion standard: one positive-control dataset and three negative-control datasets generated from the same code path
- Dependency: theory definitions

## Data Analysis
- Current task: define quantitative discrimination metrics and failure criteria
- Inputs: output tables/curves from the computation pipeline
- Deliverable: analysis memo stating which signatures are separable, where they overlap, and where the diagnostic fails
- Completion standard: can produce at least one confusion-matrix-style summary and one disorder-statistics conclusion
- Dependency: first-round numerics

## Figure Production
- Current task: keep the current storyboard but replace conceptual placeholders with benchmark-ready figures
- Inputs: analyzed numerical outputs and manuscript claim hierarchy
- Deliverable: figure storyboard with caption logic, panel order, and what each panel proves
- Completion standard: every main claim maps to at least one indispensable benchmarked panel
- Dependency: data-analysis memo

## Writing
- Current task: maintain the manuscript package and absorb benchmark results as they arrive
- Inputs: verified novelty statement, figure storyboard, evidence chain, current draft files
- Deliverable: manuscript scaffold ready to receive results
- Completion standard: a non-specialist condensed-matter referee can understand the problem, the gap in prior work, and the new contribution
- Dependency: coordinator + theory + figure plan

## Supervision
- Current task: police novelty inflation and prevent the paper from drifting into a review-style article
- Inputs: claim architecture and literature map
- Deliverable: a supervision note naming the top 3 rejection risks
- Completion standard: no unsupported "universal" or "robust" language remains without a matching evidence requirement
- Dependency: coordinator output

## Strict Review
- Current task: simulate the first editorial triage against Nature Physics
- Inputs: current concept package
- Deliverable: reject-risk memo and conditions for moving the project into credible submission territory
- Completion standard: a realistic venue verdict with actionable thresholds, not generic encouragement
- Dependency: coordinator output
