# Role Assignments

## Coordinator
- Current task: convert the uploaded concept note into a Nature-Physics-grade claim architecture and execution order
- Inputs: source note, venue criteria, recent literature overlap
- Deliverable: one-page project brief with bottleneck, claim, figure spine, and task dependencies
- Completion standard: the project has one primary claim and one primary rejection risk, both stated unambiguously
- Dependency: none

## Theory
- Current task: formalize the diagnostic hierarchy and define which observables are logically necessary, sufficient, or merely supportive
- Inputs: BdG model family, Green-function formalism, scattering-matrix invariant, disorder and impurity extensions
- Deliverable: a concise theory note defining the hierarchy and the minimum claim each observable can support
- Completion standard: the manuscript can state exactly why `G_LL` fails and what extra conditions elevate the claim to topology
- Dependency: coordinator framing

## Code and Numerical Computation
- Current task: build one reproducible pipeline that computes the same observable bundle for true and false zero modes
- Inputs: unified Hamiltonian, lead self-energies, parameter grids, disorder sampler
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
- Current task: turn the evidence chain into a five-figure main-text architecture
- Inputs: analyzed numerical outputs and manuscript claim hierarchy
- Deliverable: figure storyboard with caption logic, panel order, and what each panel proves
- Completion standard: every main claim maps to at least one indispensable figure panel
- Dependency: data-analysis memo

## Writing
- Current task: draft a concise Nature-Physics-style title, abstract, intro gap paragraph, and results section skeleton
- Inputs: verified novelty statement, figure storyboard, evidence chain
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
