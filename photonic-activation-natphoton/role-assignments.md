# Role Assignments

## Coordinator
- Current task: lock the one-sentence paper claim, one decisive bottleneck, and one benchmark sequence for the first full cycle
- Inputs: source note, venue criteria, literature snapshot, current project-state file
- Deliverable: round-1 execution brief and reviewer-risk map
- Completion standard: the project has one central claim, one top rejection risk, and one ordered benchmark plan
- Dependency: none

## Theory
- Current task: formalize the unified activation model and define the three resource metrics without hidden assumptions
- Inputs: activation families named in the source note, AQMA architecture sketch, venue criteria
- Deliverable: theory note with symbol definitions, regime assumptions, and equations suitable for Methods and main-text framing
- Completion standard: each metric has a precise optimization target, variables are defined, and the framework distinguishes function approximation from task-level performance
- Dependency: coordinator framing

## Code and Numerical Computation
- Current task: design the minimal reproducible simulation stack for single-neuron and small-network benchmarks
- Inputs: theory metric definitions, detector/loss/noise parameter ranges, target task list
- Deliverable: benchmark specification with module structure, parameter grids, and validation checks
- Completion standard: one code path can generate activation-approximation curves, energy-accuracy curves, and hardware-constraint phase maps
- Dependency: theory definitions

## Data Analysis
- Current task: define the comparison logic and failure criteria for competing activations
- Inputs: benchmark specification and literature baselines
- Deliverable: analysis memo stating what constitutes advantage, parity, or failure for AQMA relative to alternatives
- Completion standard: each main figure has a linked decision question and a non-ambiguous interpretation rule
- Dependency: theory + computation plan

## Figure Production
- Current task: convert the existing rough figure list into a submission-grade storyboard with proof burden per panel
- Inputs: current source note and analysis memo
- Deliverable: ordered figure outline with caption logic and panel-purpose mapping
- Completion standard: every main-text claim maps to at least one indispensable panel; no decorative figure remains
- Dependency: coordinator + data-analysis memo

## Writing
- Current task: reshape the concept note into a manuscript-grade title/abstract/introduction spine and Methods skeleton
- Inputs: coordinator brief, theory note, figure storyboard, verified literature positioning
- Deliverable: clean manuscript outline plus draft abstract and introduction logic
- Completion standard: a Nature Photonics referee can tell, within one read, what problem is solved and why prior work did not already solve it
- Dependency: coordinator + theory + figure plan

## Supervision
- Current task: keep the project from drifting into an under-supported manifesto
- Inputs: central claim, venue criteria, literature map
- Deliverable: supervision note naming the top three rejection risks and the corresponding evidence demands
- Completion standard: no claim of "quantum advantage", "universal", or "near-optimal" remains unsupported
- Dependency: coordinator output

## Strict Review
- Current task: perform the first five-reviewer stage estimate against Nature Photonics
- Inputs: current concept package and early manuscript architecture
- Deliverable: reviewer matrix with dimension scores, rejection logic, and acceptance-probability baseline
- Completion standard: the project has a realistic acceptance estimate plus explicit upgrade conditions for the next probability bracket
- Dependency: coordinator output
