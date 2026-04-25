# Role Assignments

## Coordinator
- Current task: convert the completed three-curve same-axis result into one submission-grade Figure-3 candidate and lock the exact main-text claim
- Inputs: theory framework, homodyne comparison note, displaced on-off comparison note, venue criteria, manuscript spine
- Deliverable: Figure-3 execution brief, panel order, and caption logic
- Completion standard: the next run can assemble one main-text figure and one Results subsection without reopening the comparison logic
- Dependency: none

## Theory
- Current task: formalize which claims are valid for fixed-displacement on-off counting versus globally optimized adaptive receivers
- Inputs: lower-bound derivation, homodyne comparison note, displaced on-off comparison note, theory framework
- Deliverable: assumptions-and-limitations note for Figure 3 and the Results subsection
- Completion standard: the manuscript can use "constant-factor overhead" language without implying global optimality
- Dependency: coordinator framing

## Code and Numerical Computation
- Current task: convert the saved comparison code into figure-ready tables and panel data for lower bound, homodyne, and displaced on-off routes
- Inputs: `same_axis_metrics.py`, homodyne comparison note, displaced on-off comparison note, benchmark specification
- Deliverable: reproducible Figure-3 data tables and plotting-ready exports
- Completion standard: the figure can be generated directly from saved numerical outputs
- Dependency: theory definitions

## Data Analysis
- Current task: turn the three-curve comparison into a device-facing interpretation with explicit near-frontier, moderate-penalty, and excluded regimes
- Inputs: homodyne comparison note, displaced on-off comparison note, journal criteria
- Deliverable: interpretation memo that defines the operational regions used in Figure 3 captioning
- Completion standard: a reader can infer a design decision from the figure rather than merely see three monotonic curves
- Dependency: theory + computation plan

## Figure Production
- Current task: assemble the first true Figure-3 candidate around lower bound, homodyne family, and displaced on-off family
- Inputs: homodyne comparison note, displaced on-off comparison note, manuscript spine, benchmark spec
- Deliverable: panel plan, axis definitions, legend rules, caption logic, and provenance checklist
- Completion standard: the result can be shown as a main-text figure without hidden assumptions
- Dependency: coordinator + data-analysis memo

## Writing
- Current task: draft the first Results subsection built around the now-completed three-curve same-axis comparison
- Inputs: homodyne comparison note, displaced on-off comparison note, manuscript spine, journal criteria
- Deliverable: manuscript paragraph set for the lower-bound-versus-two-route comparison
- Completion standard: the result can be inserted into the paper with bounded claims, explicit limitations, and a clear take-home sentence
- Dependency: coordinator + theory + figure plan

## Supervision
- Current task: prevent the new multi-route comparison from being overstated as a universal ordering of all measurement-induced activations
- Inputs: homodyne comparison note, displaced on-off comparison note, venue criteria, manuscript draft logic
- Deliverable: supervision note naming the claims that are now allowed and still disallowed
- Completion standard: the paper states "detector sets the global penalty; measurement sets the constant factor" only with explicit model boundaries
- Dependency: coordinator output

## Strict Review
- Current task: update the five-reviewer matrix after the second same-axis architecture comparison
- Inputs: lower-bound derivation, homodyne comparison note, displaced on-off comparison note, journal criteria
- Deliverable: revised reviewer matrix with dimension-by-dimension scores and stricter upgrade conditions
- Completion standard: acceptance probability reflects the broader evidence without ignoring the missing figure/manuscript package
- Dependency: coordinator output
