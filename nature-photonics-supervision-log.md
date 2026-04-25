# Nature Photonics Supervision Log

## Supervision Entry 2026-04-25

### Current Version Overall Evaluation
- The project has advanced beyond standalone packages. The paper now has one continuous manuscript integration draft, so the evidence chain runs from editorial positioning through Figure 3 to the first task-level consequence without a narrative break.

### Newly Verified Facts
- The real project materials were recoverable inside the Nature Photonics-only namespace under `photonic-activation-natphoton`.
- That namespace already contained the theory framework, manuscript spine, homodyne comparison note, displaced on-off comparison note, and reproducible same-axis code.
- A previous run generated a Figure-3 candidate package from those saved models and rendered it successfully to SVG, PNG, and PDF.
- This run revised that package into insertable manuscript prose with an evidence-bounded caption and claim sentence.
- The project-specific namespace also already contains a real minimal task-level benchmark with saved summary tables and interpretation bounds.
- This run also produced a checked literature-positioning paragraph using recent comparison papers from Nature Photonics (2024, 2025) and Nature Communications (2025).
- This run fused that verified literature block, the Figure-3 package, and the task-level benchmark package into one continuous manuscript integration draft.

### What Is Genuinely At Standard
- A lower bound plus two concrete measurement routes now exist on the same axes.
- The comparison is reproducible from saved code rather than existing only in prose.
- A figure candidate now exists as an actual rendered object, not just a planned panel.
- The figure is now accompanied by manuscript text that states the detector-driven `1/eta` penalty and the route-dependent prefactor without claiming universal receiver optimality.
- The project now has a reviewer-safe paragraph saying exactly what recent nearby papers already establish and why this manuscript's contribution is instead a cross-architecture resource framework plus bounded task-level design consequence.
- The project now has a continuous manuscript-grade narrative that carries the reader from the Introduction gap to the mixed task-level result without changing the bounded numerical or theoretical claim set.

### What Is Not Yet At Standard
- A task-level benchmark exists, but it is not yet integrated into the top-level manuscript-facing package strongly enough to satisfy journal-level presentation standards.
- No full-manuscript source or rendered manuscript PDF yet demonstrates that the new continuous draft fits a submission-like paper shell cleanly.

### Core Quality Risk
- The next quality risk is no longer narrative fragmentation at the paragraph level. It is packaging incompleteness: the project could still be rejected if the continuous draft remains outside a renderable manuscript source and PDF-level paper package.

### Evidence-Chain Gap
- The missing link is now manuscript-file embodiment of the new continuity, including section ordering, figure-number references, and renderable source.

### Must-Correct Item
- The next run must embed the new continuous draft into a full manuscript source and render the first manuscript PDF.

### Priority Adjustment
- The single main bottleneck is now full-manuscript source assembly around the finished integrated draft.
- Further expanding benchmarks before producing the first paper-level source and PDF would dilute progress.

### Allowed To Enter Next Stage?
- Yes. The project may now move from integration drafting into manuscript source assembly and first-render validation.

### Next Supervision Focus
- Check whether the next source-assembly pass preserves the new narrative continuity while remaining faithful to the bounded claim set and numerical evidence.

## Supervision Entry 2026-04-25 (first manuscript render)

### Current Version Overall Evaluation
- The project has crossed the main embodiment threshold. It now exists as a real manuscript source and a first rendered paper-level PDF rather than only as figure packages and integration notes.

### Newly Verified Facts
- The continuous manuscript integration draft was embedded into `manuscript-v1.md` inside the Nature Photonics project namespace.
- That source was rendered successfully to `manuscript-v1.pdf`.
- The rendered PDF is a real 7-page object verified by `pdfinfo`, so the current paper can now be inspected as a manuscript rather than as disconnected packages.

### What Is Genuinely At Standard
- The main text now has one continuous paper-level source.
- A first rendered manuscript PDF now exists.
- The current manuscript keeps the bounded Fig. 3 detector-penalty claim and the bounded Fig. 4 mixed task-level claim inside one document.

### What Is Not Yet At Standard
- No supplementary source or supplementary PDF yet carries the derivation burden, benchmark assumptions, and provenance needed for reviewer-level inspection.
- Figure 4 still exists as prose-level evidence in the manuscript rather than as a standalone manuscript-grade figure package.
- Caption and style harmonization across the full paper package is still incomplete.

### Core Quality Risk
- The dominant risk is now supplement absence rather than main-text absence. A reviewer can now read the paper, but cannot yet inspect the derivation and benchmark burden in a manuscript-paired supplement.

### Evidence-Chain Gap
- The missing evidence link is a rendered supplement that packages the theory framework, same-axis assumptions, and task-level benchmark assumptions in a form aligned to the manuscript claims.

### Must-Correct Item
- The next run must assemble the first supplementary source and render the first supplementary PDF.

### Priority Adjustment
- The single main bottleneck has moved from manuscript embodiment to supplement embodiment.
- Adding more benchmark scope before producing the supplement would again weaken packaging discipline.

### Allowed To Enter Next Stage?
- Yes. The project may now move from first-manuscript render into supplement assembly and package harmonization.

### Next Supervision Focus
- Check whether the supplement pass closes the derivation and provenance gap without widening the paper's claim boundary.

## Supervision Entry 2026-04-25 (first supplement render)

### Current Version Overall Evaluation
- The project has now cleared the supplement-absence barrier. The paper package contains a real main-text manuscript and a real supplementary PDF, so reviewer inspection is no longer blocked by missing derivation and provenance packaging.

### Newly Verified Facts
- A new supplement source, `supplement-v1.md`, was assembled from the saved theory framework, same-axis notes, task-level benchmark assumptions, benchmark summary, and provenance ledger.
- That source was rendered successfully to `supplement-v1.pdf`.
- `pdfinfo` verified the rendered supplement as a real 6-page PDF object.

### What Is Genuinely At Standard
- The lower-bound inverse used in the Figure-3 package is now written out explicitly in reviewer-inspectable form.
- The homodyne and displaced on-off receiver formulas are now packaged in a manuscript-paired supplement rather than only in internal notes.
- The task-level benchmark assumptions and provenance are now visible in a paired supplementary document.

### What Is Not Yet At Standard
- Figure 4 still remains prose-level in the current manuscript rather than a standalone manuscript-grade panel/caption object.
- The full package has not yet undergone final caption/style harmonization.
- The final submission archive is still absent.

### Core Quality Risk
- The dominant risk has moved again. It is no longer supplement absence. It is that the task-level systems claim is still carried mainly by prose and tables rather than by a dedicated top-level figure object.

### Evidence-Chain Gap
- The missing evidence link is a manuscript-grade Figure 4 panel and caption package created directly from the saved task-level outputs.

### Must-Correct Item
- The next run must convert the existing task-level benchmark outputs into a standalone Figure-4 package.

### Priority Adjustment
- The single main bottleneck moves from supplement embodiment to Figure-4 embodiment.
- Additional new benchmarks should still wait until the existing task-level result is packaged as a figure-level manuscript object.

### Allowed To Enter Next Stage?
- Yes. The project may now move from supplement assembly into figure-package completion and manuscript-wide harmonization.

### Next Supervision Focus
- Check whether the future Figure-4 package preserves the mixed positive-and-negative result without selective emphasis or inflated scope.

## Supervision Entry 2026-04-25 (first Figure-4 package)

### Current Version Overall Evaluation
- The project has now crossed the next packaging threshold. The task-level systems result is no longer carried only by prose and tables; it now exists as a rendered top-level figure object with an explicit caption draft and claim boundary.

### Newly Verified Facts
- A new plotting script, `figure4_task_level_panel.py`, was created directly in the project-specific Nature Photonics namespace.
- That script reads the saved minimal benchmark summary and wrote a figure-specific CSV table, `figure4_task_level_panel_data.csv`.
- The Figure-4 package was rendered successfully to `figure4_task_level_panel.svg`, `figure4_task_level_panel.png`, and `figure4_task_level_panel.pdf`.
- `pdfinfo` verified the rendered Figure-4 PDF as a real one-page PDF object.
- A new `figure4_submission_package.md` now records the panel definition, caption draft, allowed claims, disallowed claims, and provenance.

### What Is Genuinely At Standard
- The task-level benchmark is now embodied as a standalone figure-level manuscript object rather than remaining prose-only.
- The mixed systems result is preserved honestly at figure level: `concentric_circles` is positive across the scanned settings, `two_moons` is not, and route preference remains task dependent.
- The Figure-4 package is traceable back to the saved benchmark summary rather than to newly invented or recomputed numbers.

### What Is Not Yet At Standard
- The new Figure-4 object has not yet been integrated into the main manuscript source.
- Caption style and cross-reference harmonization across the full manuscript package remain incomplete.
- The final submission archive is still absent.

### Core Quality Risk
- The dominant risk is no longer missing Figure 4. It is package inconsistency: reviewers could still see a mismatch between the rendered figure package and the current manuscript source if integration is delayed.

### Evidence-Chain Gap
- The missing link is now manuscript-level incorporation of the new Figure-4 object and caption into the existing main-text draft.

### Must-Correct Item
- The next run must integrate the rendered Figure-4 package into `manuscript-v1.md` and harmonize full-paper caption style.

### Priority Adjustment
- The single main bottleneck moves from Figure-4 embodiment to manuscript-wide harmonization.
- Additional new benchmarks should still wait until the paper-level source reflects the figure objects already present.

### Allowed To Enter Next Stage?
- Yes. The project may now move from figure-package completion into manuscript integration and harmonization.

### Next Supervision Focus
- Check whether the manuscript integration pass preserves the current Figure-4 claim boundaries and visual evidence without widening scope.

## Supervision Entry 2026-04-25 (Figure-4 manuscript integration)

### Current Version Overall Evaluation
- The manuscript package is now internally coherent at the top level. Reviewers can inspect the single-neuron design-law result and the task-level consequence inside the same rendered main-text PDF, rather than inferring Fig. 4 only from prose plus a separate figure package.

### Newly Verified Facts
- `manuscript-v1.md` was updated to embed the rendered Figure-4 image directly in the Results section.
- The manuscript now carries a manuscript-facing Figure-4 caption that stays within the claim boundaries already defined in `figure4_submission_package.md`.
- The Methods section now states explicitly how Figure 4 is rendered from the saved task-level benchmark summary and what the present benchmark does not claim.
- The data/code availability statement was updated so it matches the real package already present in the project namespace.
- The revised `manuscript-v1.md` was rendered successfully to `manuscript-v1.pdf`.
- `pdfinfo` verified the updated manuscript as a real 8-page PDF object.

### What Is Genuinely At Standard
- The manuscript no longer lags behind the current Figure-4 package.
- The top-level paper object now presents both Fig. 3 and Fig. 4 directly, with bounded captions and methods wording.
- The current manuscript-plus-supplement package is coherent enough for a stricter next-stage evidence review.

### What Is Not Yet At Standard
- The systems-level conclusion still rests on a deliberately narrow minimal benchmark.
- No new robustness computation or broader task validation was added in this run.
- The final submission archive is still absent.

### Core Quality Risk
- The dominant risk has shifted again. It is no longer manuscript inconsistency. It is that reviewer confidence, especially on methods and evidence support, is still limited by narrow benchmark breadth.

### Evidence-Chain Gap
- The missing evidence link is one real robustness-strengthening result showing whether the current mixed Fig. 4 conclusion is stable beyond the saved minimal benchmark.

### Must-Correct Item
- The next run must execute one bounded robustness or evidence-strengthening action on the task-level claim.

### Priority Adjustment
- The single main bottleneck moves from manuscript-wide harmonization to systems-evidence breadth.
- Additional paper polish without new evidence would now produce diminishing returns.

### Allowed To Enter Next Stage?
- Yes. The project may now move from manuscript harmonization into review-guided robustness strengthening.

### Next Supervision Focus
- Check whether the next evidence-strengthening action materially raises reviewer confidence without widening the manuscript's claim boundary beyond a bounded design-law paper.

## Supervision Entry 2026-04-25 (trainable benchmark seed robustness)

### Current Version Overall Evaluation
- The systems-evidence package is now materially stronger than the current manuscript reveals. The project no longer relies only on a one-seed trainable benchmark claim: it now has a repeat-level robustness check that preserves the headline count while exposing the fragile edge cases honestly.

### Newly Verified Facts
- `trainable_task_benchmark_seed_robustness.py` was created and run successfully inside the Nature Photonics project namespace.
- The run completed three independently reseeded repeats of the trainable task benchmark.
- In every repeat, physical activation beat the trainable linear baseline in `22/30` scanned conditions.
- `21/30` conditions stayed above the manuscript's `+0.02` margin threshold in all three repeats.
- The fragile conditions were localized, not diffuse: all nine fragile cases are on `two_moons`, mostly at low and intermediate budgets.
- Route preference remains non-universal under reseeding; on-off beats homodyne in `20`, `13`, and `11` of `30` matched comparisons across the three repeats.

### What Is Genuinely At Standard
- The stronger trainable benchmark is now supported by a real robustness check rather than by a single-seed headline only.
- The project can now distinguish repeat-stable positive regimes from fragile near-threshold regimes in reviewer-inspectable saved outputs.
- The new systems evidence still supports the bounded design rule that activation utility depends jointly on task geometry, detector efficiency, total budget, and receiver choice.

### What Is Not Yet At Standard
- The manuscript and current Figure-4 package still foreground the older minimal benchmark rather than the stronger trainable-plus-robustness evidence.
- The robustness result still comes from a small one-hidden-layer benchmark, not from broader dataset or architecture coverage.
- The final submission archive is still absent.

### Core Quality Risk
- The dominant risk is now under-integration rather than under-computation. A reviewer could reasonably ask why the paper text still leans on the weaker systems benchmark when a stronger verified benchmark already exists in the project namespace.

### Evidence-Chain Gap
- The missing evidence link is manuscript embodiment of the stronger task-level result: Figure-4 definition, Results wording, and discussion language that reflect the seed-robust trainable benchmark and its explicit fragile exceptions.

### Must-Correct Item
- The next run must revise the manuscript-facing Figure-4 package so it is based on the trainable benchmark plus seed-robustness summary, not only on the older minimal benchmark.

### Priority Adjustment
- The single main bottleneck moves from raw systems-evidence breadth to synchronization of the strongest verified systems evidence into the paper.
- Additional new computation should wait unless manuscript revision uncovers a specific unsupported statement.

### Allowed To Enter Next Stage?
- Yes. The project may now move from robustness generation into manuscript and figure revision around the stronger trainable evidence package.

### Next Supervision Focus
- Check whether the next manuscript revision states the repeat-stable `22/30` result, names the fragile `two_moons` low-budget regimes, and keeps the scope bounded to a small trainable benchmark.

## Supervision Entry 2026-04-25 (Results-section synchronization)

### Current Version Overall Evaluation
- The manuscript is now more honest and more competitive at the Results level. The stronger systems evidence is no longer stranded outside the paper: the reader can now see both the surrogate Figure-4 scan and the trainable-plus-robustness extension in one bounded narrative.

### Newly Verified Facts
- The Figure-4-linked Results subsection in the main manuscript was revised to preserve the existing minimal surrogate benchmark as the base visualization rather than silently replacing it.
- The same subsection now states that a separate small trainable-hidden-layer benchmark beats the trainable linear baseline in `22/30` scanned settings.
- The manuscript now states that a three-repeat reseeded robustness check preserves that `22/30` headline in every repeat, with `21/30` settings staying above the `+0.02` margin threshold in all three repeats.
- The manuscript now names the localized fragile region explicitly as low- and intermediate-budget `two_moons`, including the `eta = 0.70, budget = 4` (`1/3` repeats positive) and `eta = 0.99, budget = 4` (`2/3` repeats positive) cases.
- The revised manuscript source was rendered successfully back to an 8-page PDF object.

### What Is Genuinely At Standard
- The strongest currently verified systems evidence is now visible in the reviewer-facing Results text.
- The manuscript now distinguishes robustly positive regimes from fragile near-threshold regimes instead of flattening them into one undifferentiated positive headline.
- The stronger trainable benchmark is now integrated without inflating scope into a hardware-readiness claim or a large-scale learning claim.

### What Is Not Yet At Standard
- The top-level Figure-4 caption and object still foreground the older minimal benchmark.
- Abstract, Discussion and Methods still lag behind the revised Results-level systems story.
- Final submission packaging remains absent.

### Core Quality Risk
- The dominant risk is now partial package mismatch rather than text absence. Reviewers can see the stronger systems evidence in the Results section, but the visual/caption package still says less than the text.

### Evidence-Chain Gap
- The missing link is figure-facing synchronization: caption, package note and, if needed, figure definition aligned to the trainable-plus-robustness evidence while keeping the bounded surrogate/training distinction explicit.

### Must-Correct Item
- The next run must revise the Figure-4 caption/package so the top-level visual evidence matches the upgraded Results story.

### Priority Adjustment
- The single main bottleneck remains synchronization, but it has moved from Results prose to figure-facing embodiment and paper-wide harmonization.
- Additional new computation should still wait unless that caption/package revision uncovers a specific unsupported statement.

### Allowed To Enter Next Stage?
- Yes. The project may now move from Results-section synchronization into figure-facing synchronization and final claim harmonization.

### Next Supervision Focus
- Check whether the next figure/package revision preserves the explicit distinction between the surrogate base visualization and the stronger trainable-plus-robustness extension while keeping all fragile regimes visible.

## Supervision Entry 2026-04-25 (figure-facing synchronization after trainable robustness)

### Current Version Overall Evaluation
- The paper has now crossed the previous synchronization gap. The stronger trainable-plus-robustness systems evidence is no longer stranded in the Results prose alone; it now reaches the Figure-4 object, the Figure-4 submission package and the manuscript caption.

### Newly Verified Facts
- `figure4_task_level_panel.py` was revised and executed successfully.
- The regenerated Figure-4 SVG, PNG and PDF now include an evidence-bounded annotation box sourced from the saved trainable robustness summary.
- That annotation box states only checked facts already present in the saved robustness outputs: `22/30` positive settings in every repeat, `21/30` settings above the `+0.02` margin threshold in all repeats, and localized fragile `two_moons` settings at `eta = 0.70`, budget `4` (`1/3`) and `eta = 0.99`, budget `4` (`2/3`).
- `figure4_submission_package.md` was revised so the caption package now makes the plotted surrogate-versus-trainable extension distinction explicit.
- The Figure-4 caption in `manuscript-v1.md` was revised accordingly.
- `manuscript-v1.pdf` was rendered successfully again and now verifies as a 9-page PDF object.

### What Is Genuinely At Standard
- The project now has a figure-facing Figure-4 package that no longer hides the stronger systems evidence behind prose-only description.
- The figure object itself now records the stronger trainable robustness extension without mislabeling the plotted surrogate panels as trainable data.
- The manuscript caption and the figure submission package now say the same bounded thing about Figure 4.

### What Is Not Yet At Standard
- The abstract still foregrounds the older surrogate-only systems message.
- The discussion still frames the evidence as primarily a stylized random-feature benchmark rather than as a surrogate-plus-trainable robustness package.
- The methods section still describes Figure 4 mainly through the minimal benchmark and does not yet name the trainable three-repeat extension.

### Core Quality Risk
- The dominant risk has shifted from figure-package mismatch to section-level mismatch: reviewers can now see the stronger systems evidence at figure level, but the abstract, discussion and methods still do not fully match that improved evidence boundary.

### Evidence-Chain Gap
- The missing link is full-paper harmonization of the synchronized Figure-4 story.

### Must-Correct Item
- The next run must revise abstract, discussion and methods so the paper states one consistent systems claim boundary everywhere.

### Priority Adjustment
- The single main bottleneck is now full-paper harmonization rather than figure-facing synchronization.
- New benchmark expansion should stay paused until that consistency pass is complete.

### Allowed To Enter Next Stage?
- Yes. The project may now move from figure-facing synchronization into full-paper harmonization.

### Next Supervision Focus
- Check whether the next harmonization pass preserves the surrogate-versus-trainable distinction, the localized fragile `two_moons` caveat and the current non-claims about generality.
