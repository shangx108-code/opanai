# Nature Photonics Project State

## Last Updated
- Date: 2026-04-25
- Run type: scheduled continuation

## Current Stage
- Stage: result-to-manuscript integration

## Current Overall Goal
- Build a Nature Photonics-competitive theory-and-simulation paper on quantum limits of nonlinear activation in photonic neural networks, with a quantitative resource framework, explicit same-axis comparisons, and submission-grade evidence.

## Evidence Actually Available In This Namespace
- Completed: a project-specific Nature Photonics namespace exists under `photonic-activation-natphoton` and contains the theory framework, benchmark spec, manuscript spine, same-axis comparison notes, and reproducible comparison code.
- Completed before this run: the project had a proved lower bound plus two concrete same-axis measurement routes: homodyne-conditioned AQMA proxy and displaced on-off counting.
- Completed before this run: a Figure-3 candidate package was generated from the saved analytical models, including plotting-ready CSV data and rendered SVG/PNG/PDF outputs for the three-curve same-axis comparison.
- Completed in this run: the Figure-3 package was advanced from figure-only status to manuscript-ready status by adding a bounded Results subsection draft, a tightened caption draft, and a single insertable claim sentence tied directly to the computed ratios and model limits.
- Completed in this run: a citation-verified literature-positioning paragraph was drafted from checked 2024-2025 comparison papers and tied directly to the project's current Figure-3 and task-level claims.
- Incomplete: the new subsection and the new literature paragraph are evidence-based, but they are not yet integrated into a full manuscript source or rendered manuscript PDF.
- Completed before this run in the project-specific namespace: a minimal task-level benchmark already shows a bounded but real system-level consequence of the single-neuron frontier.
- Incomplete: that task-level benchmark is still not integrated into the top-level manuscript package.

## Single Main Bottleneck
- The project now has a verified literature-positioning paragraph as a standalone package, so the main bottleneck shifts again to manuscript integration: the paper still does not place the verified Figure-3 and task-level claims into one continuous journal-facing Results and Introduction flow.

## Single Highest-Priority Action Completed In This Run
- Wrote one verified literature-positioning paragraph that distinguishes the paper from the strongest nearby 2024-2025 photonic nonlinearity and photonic-AI papers without overstating novelty.

## Deliverable From This Run
- Manuscript-ready literature-positioning paragraph for the Introduction/Results transition:
  - Recent Nature Photonics work on nonlinear processing with linear optics and recurrent linear scattering shows that repeated scattering can realize low-power nonlinear optical mappings and task demonstrations, and the 2025 field-programmable photonic nonlinearity paper pushes reconfigurable nonlinear hardware into the photonic-AI setting. These papers narrow the novelty space around "all-optical nonlinearity" and "programmable nonlinear photonics", so this manuscript should not claim either as its primary advance. The distinct contribution supported here is different: we formulate nonlinear activation as a quantum-resource problem, compare measurement-induced activation routes and a lower bound on the same photon-cost/error axes, and then show with a fixed-budget task benchmark that the neuron-level frontier changes when activation is worth paying for and that the preferred implementable route can depend on task geometry. The closest low-photon task demonstration we found, the 2025 Nature Communications work on quantum-limited stochastic optical neural networks, establishes that accurate inference is possible at a few quanta per activation in one trained stochastic architecture; our paper instead contributes a cross-architecture design law and a bounded criterion for when measurement-induced activation approaches the practical frontier and when it does not.
  - Evidence basis checked in this run:
    - `Nonlinear optical encoding enabled by recurrent linear scattering`, Nature Photonics 18, 1067-1075 (2024)
    - `Nonlinear processing with linear optics`, Nature Photonics 18, 1076-1082 (2024)
    - `Field-programmable photonic nonlinearity`, Nature Photonics 19, 725-732 (2025)
    - `Quantum-limited stochastic optical neural networks operating at a few quanta per activation`, Nature Communications 16, 359 (2025)
  - preserved novelty / non-novelty boundaries

## What Is Genuinely Completed
- Completed: recovery of the real Nature Photonics project state from the project-specific namespace only.
- Completed: verified three-route same-axis evidence base remains available in this namespace.
- Completed: generated a real Figure-3 candidate panel from the lower bound, homodyne route, and displaced on-off route.
- Completed: rendered the panel successfully to PNG and PDF, so the figure is no longer only a note or unrendered script.
- Completed: wrote a bounded Results subsection and revised caption language that track the computed `1/eta` detector penalty and the route-dependent constant-factor overhead without claiming global optimality.
- Completed: wrote a citation-verified literature-positioning paragraph that states what nearby 2024-2025 papers already establish and what this project adds beyond them.

## What Is Still Incomplete
- Incomplete: full-manuscript source integration of the new Figure-3 subsection and the new literature-positioning paragraph.
- Incomplete: final caption package after manuscript-wide style harmonization.
- Incomplete: task-level energy-accuracy evidence is available in the project-specific namespace but not yet integrated into the top-level manuscript package.
- Incomplete: full manuscript PDF, supplement PDF, and final archive package.
- Incomplete: all five reviewer acceptance estimates remain below 70%.

## Acceptance Probability Snapshot
- Status: improved, but still well below submission readiness.
- Conservative current estimate: `45-55%`.
- Basis: the project now has a real same-axis figure package, an evidence-bounded Results narrative, and a checked literature-positioning paragraph. The estimate remains capped because the text is still not integrated into a full manuscript flow, the task-level benchmark is not yet carried into the main manuscript, and no manuscript PDF or supplement package exists.

## Recent Update Summary
- Recovered the real project state from the Nature Photonics-only namespace rather than borrowing from other projects.
- Generated the first Figure-3 candidate package from the saved same-axis models.
- Revised the figure package into manuscript-ready prose: the comparison can now be stated as a bounded design law saying that detector efficiency controls global frontier accessibility while receiver choice controls the residual constant-factor overhead in the fixed models studied here.
- Added a literature-positioning paragraph that separates the paper from recent work on repeated-scattering nonlinearity, field-programmable photonic nonlinearity, and low-photon task demonstrations without claiming generic programmability or universal superiority.

## Next Immediate Action
- Integrate the verified literature-positioning paragraph and the existing Figure-3 / task-level packages into one continuous manuscript-grade Results and Introduction flow.
