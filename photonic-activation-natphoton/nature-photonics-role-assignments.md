# Nature Photonics Role Assignments

## Role task table

| Role | Current task | Input | Deliverable | Completion standard | Dependency |
| --- | --- | --- | --- | --- | --- |
| Coordinator | Re-anchor the paper spine around the new discrimination-cost result without overstating it | Existing project concept, this run's derivation | One-sentence core claim and updated benchmark order | Claim explicitly states what is proved, what is conjectural, and what must be benchmarked next | This run's derivation |
| Theory | Generalize the completed two-state bound into a framework usable for smooth activations and alternative measurement routes | Coherent-state threshold derivation, activation families already planned | Unified notation note linking activation sharpness, decision error, and resource cost | At least one additional family or one smooth-activation local expansion is derived without hidden assumptions | This run's derivation |
| Code and Numerical Computation | Turn the bound into a real curve generator for photon cost versus error and margin | Completed bound, chosen encoding map, parameter ranges | First runnable script and data table for one figure candidate | Script runs end to end and writes reproducible numerical output from the analytical bound | Theory parameterization |
| Data Analysis | Define what would count as a meaningful regime shift relative to baseline measurement or electronic activation | Bound output and benchmark specification | Comparison memo with advantage, parity, and failure criteria | Each planned panel has a decision rule that does not depend on rhetorical interpretation | Numerical output |
| Figure Production | Promote the first derivation into a figure storyboard panel instead of a text-only claim | Bound expression and planned numerical scan | Figure-1/2 candidate panel description with axes, caption logic, and physical takeaway | Panel can be traced to exact equations and exact numerical data source | Numerical output + analysis memo |
| Writing | Draft the theory paragraph that introduces activation quantum cost through boundary discrimination | This run's derivation and journal framing | Manuscript-ready paragraph or subsection skeleton | Text states assumptions, physical meaning, and limitations cleanly enough for referee reading | Coordinator framing |
| Supervision | Check that the new derivation is used conservatively and does not get inflated into unsupported global claims | This run's derivation and current paper claim | Risk note on overclaim boundaries | No unsupported use of "optimal", "universal", or "advantage" remains | Writing update |
| Strict Review | Hold reviewer estimates roughly flat until numerics and literature separation catch up | Current project state plus new derivation | Short reviewer update note | Review history distinguishes theory progress from submission readiness | Coordinator summary |

## What was completed in this run
- Theory completed one explicit derivation for the lower bound on boundary discrimination cost for threshold-like activation.

## What remains incomplete
- No code path has yet converted the derivation into data.
- No figure panel has yet been generated from real numerical output.
- No manuscript section has yet been revised around the new result.

## Next immediate deliverable
- One runnable computation producing a photon-cost-versus-error curve for the derived lower bound.
