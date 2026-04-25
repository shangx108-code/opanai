# Nature Photonics Project State

## Last Updated
- Date: 2026-04-25
- Run type: scheduled continuation after trainable-benchmark seed-robustness analysis

## Current Stage
- Stage: Results-generation and robustness-strengthening completed for the trainable task benchmark; next gap is manuscript integration of the stronger systems evidence

## Current Overall Goal
- Build a Nature Photonics-competitive theory-and-simulation paper on quantum limits of nonlinear activation in photonic neural networks, with a quantitative resource framework, explicit same-axis comparisons, and submission-grade evidence.

## Evidence Actually Available In This Namespace
- Completed: a project-specific Nature Photonics namespace exists under `photonic-activation-natphoton` and contains the theory framework, benchmark spec, manuscript spine, same-axis comparison notes, and reproducible comparison code.
- Completed before this run: the project had a proved lower bound plus two concrete same-axis measurement routes: homodyne-conditioned AQMA proxy and displaced on-off counting.
- Completed before this run: a Figure-3 candidate package was generated from the saved analytical models, including plotting-ready CSV data and rendered SVG/PNG/PDF outputs for the three-curve same-axis comparison.
- Completed before this run: the Figure-3 package was advanced to manuscript-ready status with a bounded Results subsection draft, a tightened caption draft, and a single insertable claim sentence tied directly to the computed ratios and model limits.
- Completed before this run: a citation-verified literature-positioning paragraph was drafted from checked 2024-2025 comparison papers and tied directly to the project's current Figure-3 and task-level claims.
- Completed before this run: the literature-positioning block, Figure-3 Results package, and task-level benchmark package were fused into one continuous manuscript integration draft covering the end of the Introduction, the Fig. 3 subsection, the Fig. 3 to Fig. 4 bridge, the Fig. 4 subsection, and the Discussion carry-through.
- Completed before this run: that integration draft was embedded into `manuscript-v1.md` and rendered successfully to a first full `manuscript-v1.pdf` with 7 pages verified by `pdfinfo`.
- Completed before this run: the first supplement source, `supplement-v1.md`, was assembled directly from the saved theory framework, same-axis notes, task-level benchmark assumptions, and provenance files inside the Nature Photonics namespace.
- Completed before this run: that supplement source was rendered successfully to `supplement-v1.pdf`, with 6 pages verified by `pdfinfo`.
- Completed before this run in the project-specific namespace: the saved minimal task-level benchmark was converted into a standalone Figure-4 package consisting of a dedicated plotting script, a figure-specific CSV table, rendered SVG/PNG/PDF outputs, and a caption-ready submission package.
- Completed before this run: the rendered Figure-4 package preserves the mixed positive-and-negative systems result already present in the manuscript prose, including the `15/15`, `0/15`, and `9/30` evidence lines.
- Completed before this run: the standalone Figure-4 object was integrated into `manuscript-v1.md`, including a manuscript-facing caption, a bounded Methods description, and an updated data/code availability statement aligned to the real current package.
- Completed before this run: the harmonized `manuscript-v1.md` was rendered successfully back to `manuscript-v1.pdf`, now verified by `pdfinfo` as an 8-page PDF object.
- Completed in this run: a new script, `trainable_task_benchmark_seed_robustness.py`, was created inside the project-specific namespace and run successfully to completion.
- Completed in this run: that script produced `seed_robustness_detail.csv`, `seed_robustness_summary.csv`, `seed_repeat_counts.csv`, `seed_robustness_summary.json`, and `seed_robustness_summary.md` inside `trainable_task_benchmark_seed_robustness/`.
- Completed in this run: across three independently reseeded data-split and training repeats, physical activation beat the trainable linear baseline in `22/30` scanned conditions in every repeat.
- Completed in this run: `21/30` scanned conditions stayed above the manuscript's `+0.02` margin threshold in all three repeats, while `9/30` conditions were shown explicitly to be fragile or negative under reseeding.
- Completed in this run: the fragile region was localized rather than hidden; it remains concentrated in `two_moons` at low and intermediate budgets, with `eta = 0.70, budget = 4` positive in only `1/3` repeats and `eta = 0.99, budget = 4` positive in `2/3` repeats.
- Incomplete: the main manuscript and current Figure-4 package still present the older minimal benchmark rather than the stronger trainable-plus-robustness evidence package.

## Single Main Bottleneck
- The single main bottleneck is now evidence-to-manuscript mismatch: the stronger trainable and seed-robust systems evidence now exists, but the reviewer-facing manuscript still foregrounds the older minimal benchmark rather than the improved result.

## Single Highest-Priority Action Completed In This Run
- Executed a real three-repeat seed-robustness analysis on the trainable task benchmark.

## Deliverable From This Run
- Seed-robustness package for the stronger trainable task benchmark in the project-specific Nature Photonics namespace:
  - `trainable_task_benchmark_seed_robustness.py`: reproducible robustness-analysis script that reuses the existing trainable benchmark and changes only the data-split and training seeds.
  - `trainable_task_benchmark_seed_robustness/seed_robustness_summary.md`: narrative summary of the repeat-level counts, robust positive regimes, and fragile regimes.
  - `trainable_task_benchmark_seed_robustness/seed_robustness_summary.csv`: condition-level mean margin, margin spread, route-win counts, and positive-repeat counts.
  - `trainable_task_benchmark_seed_robustness/seed_repeat_counts.csv`: per-repeat counts showing that the `22/30` headline held in every repeat.
  - The new reviewer-relevant evidence is now:
    - the trainable benchmark conclusion is not a one-seed accident at the headline-count level
    - the robust positive regimes are concentrated in all `15/15` concentric-circles settings plus six high-budget `two_moons` settings
    - the fragile or negative regimes are stated explicitly rather than averaged away

## What Is Genuinely Completed
- Completed: recovery of the real Nature Photonics project state from the project-specific namespace only.
- Completed: verified three-route same-axis evidence base remains available in this namespace.
- Completed: generated a real Figure-3 candidate panel from the lower bound, homodyne route, and displaced on-off route.
- Completed: rendered the panel successfully to PNG and PDF, so the figure is no longer only a note or unrendered script.
- Completed: wrote a bounded Results subsection and revised caption language that track the computed `1/eta` detector penalty and the route-dependent constant-factor overhead without claiming global optimality.
- Completed: wrote a citation-verified literature-positioning paragraph that states what nearby 2024-2025 papers already establish and what this project adds beyond them.
- Completed: fused the verified literature paragraph, the Fig. 3 claim package, and the real task-level benchmark into one continuous manuscript integration draft that preserves the existing numerical and claim boundaries.
- Completed: assembled those verified packages into one full manuscript source file within the Nature Photonics namespace.
- Completed: rendered a full manuscript PDF from that source, so the project now has a paper-level object rather than only manuscript fragments.
- Completed: assembled the first supplementary source from existing project evidence only.
- Completed: rendered the first supplementary PDF, so the derivation and provenance burden is no longer absent from the paper package.
- Completed: created a dedicated Figure-4 plotting script tied directly to the saved minimal benchmark summary.
- Completed: rendered a standalone Figure-4 SVG, PNG, and PDF, so the systems-level result is no longer prose-only.
- Completed: wrote a figure-specific submission package with a caption draft and explicit allowed/disallowed claims for the current benchmark scope.
- Completed: integrated the rendered Figure-4 object directly into the main manuscript source.
- Completed: regenerated the full manuscript PDF after that integration, so the top-level paper object now matches the current figure package.
- Completed: executed a stronger seed-robustness test on the trainable hidden-layer benchmark rather than on the earlier random-feature surrogate.
- Completed: verified that the headline `22/30` count is stable across three independently reseeded repeats.
- Completed: identified exactly which task-level settings are robustly positive in all repeats and which settings remain fragile near the decision boundary.

## What Is Still Incomplete
- Incomplete: the stronger trainable-plus-robustness benchmark has not yet replaced the older minimal benchmark in the manuscript-facing Figure-4 story.
- Incomplete: final submission archive package.
- Incomplete: all five reviewer acceptance estimates remain below 70%.

## Acceptance Probability Snapshot
- Status: improved, but still below submission readiness.
- Conservative current estimate: `65-69%`.
- Basis: this run added real systems-level robustness evidence on the stronger trainable benchmark and showed that the headline `22/30` count is repeat-stable, which directly raises confidence in methods and results support. The estimate remains capped because the stronger evidence has not yet been integrated into the manuscript or Figure-4 package, the benchmark is still small-scale, and the final submission archive is absent.

## Recent Update Summary
- Recovered the real project state from the Nature Photonics-only namespace rather than borrowing from other projects.
- Generated the first Figure-3 candidate package from the saved same-axis models.
- Revised the figure package into manuscript-ready prose: the comparison can now be stated as a bounded design law saying that detector efficiency controls global frontier accessibility while receiver choice controls the residual constant-factor overhead in the fixed models studied here.
- Added a literature-positioning paragraph that separates the paper from recent work on repeated-scattering nonlinearity, field-programmable photonic nonlinearity, and low-photon task demonstrations without claiming generic programmability or universal superiority.
- Turned those separate packages into one continuous manuscript integration draft that now carries the reader from the Introduction gap statement through Fig. 3 and into the mixed Fig. 4 systems consequence.
- Advanced that integration draft into a real manuscript object by assembling `manuscript-v1.md` and rendering `manuscript-v1.pdf`.
- Closed the supplement-absence gap by assembling `supplement-v1.md` and rendering `supplement-v1.pdf`.
- Converted the saved minimal task-level benchmark into a real Figure-4 package with rendered SVG/PNG/PDF outputs and a caption-ready submission note.
- Folded the rendered Figure-4 object back into `manuscript-v1.md`, tightened the manuscript-facing Fig. 4 caption and Methods wording, and regenerated `manuscript-v1.pdf` as an 8-page paper object.
- Added a real seed-robustness layer on top of the stronger trainable benchmark and verified that the `22/30` positive-condition headline survives across three independent reseeded repeats.
- Tightened the systems claim boundary further by naming the exact fragile regimes instead of treating all positive margins as equally secure.

## Next Immediate Action
- Replace the current minimal-benchmark-only Figure-4 and Results wording with the stronger trainable-plus-seed-robustness evidence package, while preserving the explicit fragile-regime caveats.
