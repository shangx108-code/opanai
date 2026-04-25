# Nature Photonics Role Assignments

## Role task table

| Role | Current task | Input | Deliverable | Completion standard | Dependency |
| --- | --- | --- | --- | --- | --- |
| Coordinator | Re-anchor the paper spine around a now two-step evidence chain: proved lower bound plus first numerical boundary scan | Project concept, completed derivation, verified scan values | One-sentence core claim and updated comparison order | Claim states exactly that the current result is a lower-bound regime map, not yet a full device-advantage theorem | This run's computation |
| Theory | Specify one explicit AQMA-inspired measurement model that can be placed against the lower-bound curve without hidden assumptions | Completed lower bound, local encoding model, planned measurement route | Stated model equations and variables for effective boundary decision error and photon use | The model is detailed enough to generate numbers and explicit enough to criticize | Current scan + prior derivation |
| Code and Numerical Computation | Compute the first comparison between the lower-bound curve and one explicit measurement model | Lower-bound scan, theory model for AQMA-like route | Comparison table or curve set for one figure candidate | Computation runs end to end and outputs reproducible numeric comparison values | Theory model |
| Data Analysis | Turn the scan into a design statement about sharpness cost and where comparison must focus | Verified lower-bound values | Short analysis note defining meaningful win/loss regimes | Interpretation is tied to actual numbers and does not overclaim | Current scan |
| Figure Production | Convert the computed lower-bound scan into a formal figure panel specification | Verified `n_bar^min(epsilon)` values and `g_min(delta, epsilon)` map | Figure panel blueprint with axes, panel order, caption claim, and limitations note | Every plotted axis is backed by a completed computation | Current scan |
| Writing | Revise one theory/results subsection so the lower bound and the new numeric consequences appear together | Derivation, computed values, journal framing | Manuscript-ready subsection draft | Text includes formulas, parameter scan summary, and limitations in one place | Coordinator framing |
| Supervision | Check whether the new numeric scan creates a meaningful design boundary or only a trivial monotonic curve | Verified numerical outputs and intended figure claim | Supervision note on significance threshold | It is explicit whether the result changes a device-level conclusion yet | Current scan |
| Strict Review | Update reviewer estimates modestly for evidence gain while keeping device/novelty objections active | Updated project state plus current scan | Short reviewer update note | Review record distinguishes real progress from submission readiness | Coordinator summary |

## What was completed in this run
- Theory completed one explicit derivation for the lower bound on boundary discrimination cost for threshold-like activation.
- Code and numerical computation completed the first real scan from that bound.
- Data analysis now has verified values showing how boundary photon cost and required encoding gain grow as sharper activation decisions are demanded.

## What remains incomplete
- No AQMA-like comparison model has yet been specified and computed.
- No figure panel has yet been formally assembled from the numerical output.
- No manuscript section has yet been revised to integrate both the derivation and the scan.

## Next immediate deliverable
- One explicit comparison computation between the lower-bound curve and a stated AQMA-inspired measurement route.
