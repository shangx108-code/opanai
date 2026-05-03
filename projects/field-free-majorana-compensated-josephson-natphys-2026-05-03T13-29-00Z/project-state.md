# Project State

- Stage: `project initialization completed, model bootstrap pending`
- Current round main bottleneck: `resolved this round: canonical GitHub-backed project space and runtime skeleton`
- Next bottleneck: `build and validate the clean-limit BdG minimal model for phase diagram and gap-closing checks`
- Target journal line: `Nature Physics`

## Latest Real Progress

On 2026-05-03, the project received a new canonical identifier, a fixed
long-term archive root, a matching manuscript root, archive ledgers, source
material archiving, runtime-check tooling, and a project-local virtual
environment wrapper based on system site packages.

## Evidence Boundary

- No clean-limit phase diagram has been computed in this new canonical project space yet.
- No transport, impurity, or disorder result has been regenerated here yet.
- The current scientific basis is the uploaded planning brief, not newly rerun code.

## Runtime Status

- Available now: `numpy`, `pandas`
- Missing now: `scipy`, `matplotlib`, `kwant`, `sympy`
- External package installation through `pip` is currently blocked by network proxy restrictions in this environment.

## Immediate Next Action

Implement the first reproducible calculation path for the minimal compensated
magnetic Josephson-junction Hamiltonian in a `numpy`-first route, while keeping
the missing plotting and transport packages listed as explicit environment
blockers for later steps.
