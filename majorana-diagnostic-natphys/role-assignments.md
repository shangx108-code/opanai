# Role Assignments

## Coordinator
- Current task: lock the next round around the full-device topology upgrade and prevent Figure 4 from drifting into premature finalization
- Inputs: topology-layer upgrade specification, venue criteria, current figure logic, manuscript package
- Deliverable: updated project brief and single benchmark target
- Completion standard: the project has one primary rejection risk, one primary topology-fix task, and one rebuild trigger for Figure 4
- Dependency: none

## Theory
- Current task: formalize the full-device inhomogeneous class-D invariant and its relation to the diagnostic hierarchy
- Inputs: BdG model family, Green-function formalism, Majorana-basis antisymmetrization, disorder and impurity extensions, topology-layer upgrade specification
- Deliverable: concise derivation block plus manuscript-ready explanation of `nu_ring`
- Completion standard: the manuscript can explain why the topology label and transport observables probe the same physical landscape
- Dependency: coordinator framing

## Code and Numerical Computation
- Current task: implement the full-device ring-invariant topology label in the shared three-terminal benchmark path
- Inputs: three-terminal operating-point table, inhomogeneous device Hamiltonians, barrier/temperature/disorder perturbations, topology-layer upgrade specification
- Deliverable: rerun data for `G_LL`, `G_RR`, `G_LR`, reopened-gap proxy, `nu_ring`, and `P_topo`
- Completion standard: positive, smooth-dot, impurity, and disorder families are evaluated with transport and topology on the same inhomogeneous instances
- Dependency: theory definitions

## Data Analysis
- Current task: quantify the decoupling between local-peak prevalence and topological-consistency probability
- Inputs: rerun tables containing local-peak score, `|G_LR|`, gap proxy, `nu_ring`, and `P_topo`
- Deliverable: analysis memo showing where false positives remain locally misleading but topologically inconsistent
- Completion standard: can state one concise discrimination rule and one robustness summary without leaning on the old backbone proxy
- Dependency: first-round numerics

## Figure Production
- Current task: rebuild Figure 4 as a consistency-filter figure rather than a nonlocal-only rescue figure
- Inputs: topology-layer upgrade specification and rerun numerical outputs
- Deliverable: updated Figure 4 panel order, caption, and legend logic
- Completion standard: the figure shows matched local anomaly, nonlocal signal, gap logic, and full-device topology on the same operating points
- Dependency: data-analysis memo

## Writing
- Current task: integrate the new full-device topology language into the Results and Figure 4 caption logic
- Inputs: topology-layer upgrade specification, verified novelty statement, figure storyboard, current draft files
- Deliverable: manuscript replacement paragraph and caption text
- Completion standard: the manuscript no longer describes the topology panel as a clean-backbone proxy or as a completed proof
- Dependency: coordinator + theory + figure plan

## Supervision
- Current task: police topology inflation and block any claim that the three-terminal figure is already final
- Inputs: topology-layer upgrade specification, claim architecture, literature map
- Deliverable: a supervision note naming the topology-specific rejection risks
- Completion standard: no manuscript text implies that topology has been established without the full-device rerun
- Dependency: coordinator output

## Strict Review
- Current task: simulate the first editorial triage against Nature Physics
- Inputs: current concept package
- Deliverable: reject-risk memo and conditions for moving the project into credible submission territory
- Completion standard: a realistic venue verdict with actionable thresholds, not generic encouragement
- Dependency: coordinator output
