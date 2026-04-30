# Role Assignments

Last updated: 2026-04-30 09:10:02 CST

| Role | Current task | Input | Deliverable | Completion standard | Dependency |
| --- | --- | --- | --- | --- | --- |
| Coordinator | Keep project identity, main bottleneck, and stop condition fixed | Uploaded md plans, current state files | Updated state and iteration decisions | One active bottleneck only; no scope drift | None |
| Theory | Formalize the minimum normal-state plus pairing toy model for the first executable evidence | Uploaded md plans | Parameter definitions and decision metrics | Every symbol used by code is documented and bounded | Coordinator |
| Code and numerical | Extend the executable scaffold toward a minimal Andreev-selectivity scan | `scripts/minimal_bdg_scaffold.py` and config | Runnable scan script and outputs | Reproducible outputs saved under `results/` | Theory |
| Data analysis | Convert raw scan outputs into gap-selectivity and exclusion metrics | Result tables | Clean summary tables and short interpretation | Each key statement points to a saved table | Code and numerical |
| Figure | Define the first PRL-facing figure logic from real outputs | Summary tables | Figure map and caption skeleton | Every planned panel has an upstream data source | Data analysis |
| Writing | Keep claims below evidence while drafting reusable manuscript fragments | Project state and result summaries | Methods and Results fragments | No unsupported claim enters manuscript files | Coordinator, Data analysis |
| Reviewer simulation | Stress-test acceptance barriers and probability estimate | All archived outputs | Review-history updates | Risks are concrete and tied to missing evidence | All upstream |
