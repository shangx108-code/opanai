# Nature Photonics Project State

## Last Updated
- Date: 2026-04-25
- Run type: scheduled continuation

## Current Stage
- Stage: Figure-4 package completed; manuscript-wide harmonization remains

## Current Overall Goal
- Build a Nature Photonics-competitive theory-and-simulation paper on quantum limits of nonlinear activation in photonic neural networks, with a quantitative resource framework, explicit same-axis comparisons, and submission-grade evidence.

## Evidence Actually Available In This Namespace
- Completed: a project-specific Nature Photonics namespace exists under `photonic-activation-natphoton` and contains the theory framework, benchmark spec, manuscript spine, same-axis comparison notes, and reproducible comparison code.
- Completed before this run: the project had a proved lower bound plus two concrete same-axis measurement routes: homodyne-conditioned AQMA proxy and displaced on-off counting.
- Completed before this run: a Figure-3 candidate package was generated from the saved analytical models, including plotting-ready CSV data and rendered SVG/PNG/PDF outputs for the three-curve same-axis comparison.
- Completed in this run: the Figure-3 package was advanced from figure-only status to manuscript-ready status by adding a bounded Results subsection draft, a tightened caption draft, and a single insertable claim sentence tied directly to the computed ratios and model limits.
- Completed in this run: a citation-verified literature-positioning paragraph was drafted from checked 2024-2025 comparison papers and tied directly to the project's current Figure-3 and task-level claims.
- Completed in this run: the literature-positioning block, Figure-3 Results package, and task-level benchmark package were fused into one continuous manuscript integration draft covering the end of the Introduction, the Fig. 3 subsection, the Fig. 3 to Fig. 4 bridge, the Fig. 4 subsection, and the Discussion carry-through.
- Completed in this run: the continuous integration draft was embedded into a full manuscript source file, `manuscript-v1.md`, inside the Nature Photonics project namespace.
- Completed in this run: that manuscript source was rendered successfully to a first full manuscript PDF, `manuscript-v1.pdf`, with 7 pages verified by `pdfinfo`.
- Completed in this run: the first supplement source, `supplement-v1.md`, was assembled directly from the saved theory framework, same-axis notes, task-level benchmark assumptions, and provenance files inside the Nature Photonics namespace.
- Completed in this run: that supplement source was rendered successfully to `supplement-v1.pdf`, with 6 pages verified by `pdfinfo`.
- Completed before this run in the project-specific namespace: a minimal task-level benchmark already shows a bounded but real system-level consequence of the single-neuron frontier.
- Completed in this run: the saved minimal task-level benchmark was converted into a standalone Figure-4 package consisting of a dedicated plotting script, a figure-specific CSV table, rendered SVG/PNG/PDF outputs, and a caption-ready submission package.
- Completed in this run: the rendered Figure-4 package preserves the mixed positive-and-negative systems result already present in the manuscript prose, including the `15/15`, `0/15`, and `9/30` evidence lines.
- Incomplete: the new Figure-4 object has been created in the project namespace, but it has not yet been integrated into the main manuscript source and harmonized with the full-paper caption style.

## Single Main Bottleneck
- The single main bottleneck is now manuscript-wide harmonization: the project has a real Figure-4 object, but the new figure and caption package have not yet been folded back into the main manuscript and final paper-wide style pass.

## Single Highest-Priority Action Completed In This Run
- Built the first standalone Figure-4 panel and caption package directly from the saved minimal task-level benchmark outputs.

## Deliverable From This Run
- First standalone Figure-4 package in the project-specific Nature Photonics namespace:
  - `figure4_task_level_panel.py`: plotting script that reads the saved benchmark summary and renders the figure package without introducing new task-level claims.
  - `figure4_task_level_panel/figure4_task_level_panel_data.csv`: plotting-ready table of the best-route margin-versus-baseline data plus the matched route-preference deltas.
  - `figure4_task_level_panel/figure4_task_level_panel.svg`
  - `figure4_task_level_panel/figure4_task_level_panel.png`
  - `figure4_task_level_panel/figure4_task_level_panel.pdf`
  - `figure4_submission_package.md`: caption draft, panel definitions, allowed/disallowed claims, and provenance notes.
  - The current Figure-4 package now makes reviewer-inspectable:
    - the per-task margin above the linear baseline at each scanned `(eta, budget)` setting
    - the task split between `two_moons` and `concentric_circles`
    - the matched homodyne-versus-on-off preference map that yields the saved `9/30` route-switch count
    - the selected hidden-layer width for the best implementable route at each plotted point

## What Is Genuinely Completed
- Completed: recovery of the real Nature Photonics project state from the project-specific namespace only.
- Completed: verified three-route same-axis evidence base remains available in this namespace.
- Completed: generated a real Figure-3 candidate panel from the lower bound, homodyne route, and displaced on-off route.
- Completed: rendered the panel successfully to PNG and PDF, so the figure is no longer only a note or unrendered script.
- Completed: wrote a bounded Results subsection and revised caption language that track the computed `1/eta` detector penalty and the route-dependent constant-factor overhead without claiming global optimality.
- Completed: wrote a citation-verified literature-positioning paragraph that states what nearby 2024-2025 papers already establish and what this project adds beyond them.
- Completed: fused the verified literature paragraph, the Fig. 3 claim package, and the real task-level benchmark into one continuous manuscript integration draft that preserves the existing numerical and claim boundaries.
- Completed: assembled those verified packages into one full manuscript source file within the Nature Photonics namespace.
- Completed: rendered a first full manuscript PDF from that source, so the project now has a paper-level object rather than only manuscript fragments.
- Completed: assembled the first supplementary source from existing project evidence only.
- Completed: rendered the first supplementary PDF, so the derivation and provenance burden is no longer absent from the paper package.
- Completed: created a dedicated Figure-4 plotting script tied directly to the saved minimal benchmark summary.
- Completed: rendered a standalone Figure-4 SVG, PNG, and PDF, so the systems-level result is no longer prose-only.
- Completed: wrote a figure-specific submission package with a caption draft and explicit allowed/disallowed claims for the current benchmark scope.

## What Is Still Incomplete
- Incomplete: the main manuscript source still needs to absorb the new Figure-4 object and caption.
- Incomplete: final caption package after manuscript-wide style harmonization.
- Incomplete: final submission archive package.
- Incomplete: all five reviewer acceptance estimates remain below 70%.

## Acceptance Probability Snapshot
- Status: improved, but still well below submission readiness.
- Conservative current estimate: `57-68%`.
- Basis: the project now has real top-level figure packages for both the single-neuron comparison and the task-level consequence, plus a full manuscript source/PDF and a paired supplement source/PDF. The estimate remains capped because the new Figure-4 package has not yet been integrated into the manuscript, manuscript-wide caption/style harmonization is still incomplete, and the final submission archive is absent.

## Recent Update Summary
- Recovered the real project state from the Nature Photonics-only namespace rather than borrowing from other projects.
- Generated the first Figure-3 candidate package from the saved same-axis models.
- Revised the figure package into manuscript-ready prose: the comparison can now be stated as a bounded design law saying that detector efficiency controls global frontier accessibility while receiver choice controls the residual constant-factor overhead in the fixed models studied here.
- Added a literature-positioning paragraph that separates the paper from recent work on repeated-scattering nonlinearity, field-programmable photonic nonlinearity, and low-photon task demonstrations without claiming generic programmability or universal superiority.
- Turned those separate packages into one continuous manuscript integration draft that now carries the reader from the Introduction gap statement through Fig. 3 and into the mixed Fig. 4 systems consequence.
- Advanced that integration draft into a real manuscript object by assembling `manuscript-v1.md` and rendering `manuscript-v1.pdf`.
- Closed the supplement-absence gap by assembling `supplement-v1.md` and rendering `supplement-v1.pdf`.
- Converted the saved minimal task-level benchmark into a real Figure-4 package with rendered SVG/PNG/PDF outputs and a caption-ready submission note.

## Next Immediate Action
- Integrate the new Figure-4 object into `manuscript-v1.md` and harmonize the full-paper caption style so the paper package reflects the new figure-level evidence consistently.
