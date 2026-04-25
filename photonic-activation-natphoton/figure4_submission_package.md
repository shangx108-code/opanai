# Figure 4 Submission Package

## Objective of this package
- Keep the already saved minimal task-level benchmark as the plotted Figure-4 object.
- Synchronize that plotted object with the stronger trainable-hidden-layer plus seed-robustness evidence that is now stated in the manuscript Results.
- Keep every claim bounded to the real benchmark and robustness outputs already computed in this project namespace.

## Figure contents

### Panel a
- Task: `two_moons`.
- Horizontal axis: total activation photon budget per inference.
- Vertical axis: accuracy margin of the best implementable activation route relative to the linear no-activation baseline.
- Line color: detector efficiency `eta`.
- Marker shape: which implementable route is best at that setting.
- Width labels above markers: selected hidden-layer width of the best route.

### Panel b
- Task: `concentric_circles`.
- Same axes and encodings as panel a.
- This panel shows the positive side of the benchmark: all scanned settings beat the linear baseline by more than `0.02` accuracy.

### Panel c
- Compact route-preference map over all `30` matched `(task, eta, budget)` settings.
- Cell value: `on_off accuracy - homodyne accuracy`.
- Blue cells indicate homodyne is better for that setting; red cells indicate on-off is better.
- This panel supports the bounded systems claim that route preference is not inherited trivially from the single-neuron frontier.

### Figure-embedded synchronization note
- The rendered figure now includes an annotation box that records the stronger trainable-hidden-layer check under the same photon accounting.
- That box states only saved facts from the real robustness outputs: activation beats the trainable linear baseline in `22/30` settings in every repeat, `21/30` settings remain above the `+0.02` margin threshold in all three repeats, and the remaining fragility is localized to low- and intermediate-budget `two_moons`.
- The note also names the two near-threshold settings that remain visibly fragile: `eta = 0.70`, budget `4` is positive in `1/3` repeats and `eta = 0.99`, budget `4` is positive in `2/3` repeats.

## Caption draft
**Figure 4 | Task-level worth of physical activation depends on task geometry, detector efficiency and total photon budget.**
**a,b,** Best implementable test-accuracy margin above the task-specific linear no-activation baseline for the saved minimal surrogate benchmark, plotted against total activation photon budget per inference for `two_moons` (**a**) and `concentric_circles` (**b**). Each point selects the better of the two implementable activation routes at that `(task, eta, budget)` setting, with line color denoting detector efficiency `eta` and marker shape denoting whether homodyne or displaced on-off counting is preferred. Width labels give the selected hidden-layer width for the best route. In this surrogate scan, paying for activation is worthwhile across all `15/15` `concentric_circles` settings, whereas no scanned `two_moons` setting exceeds the linear baseline.
**c,** Difference between displaced on-off and homodyne test accuracy over the same `30` matched settings. The sign changes across tasks and budgets, and displaced on-off is better in only `9/30` surrogate comparisons, so route preference is not inherited trivially from the single-neuron frontier.
**Figure note,** The annotation box records a separate stronger trainable-hidden-layer benchmark under the same activation-photon accounting. There, the best implementable physical activation beats the trainable linear baseline in `22/30` scanned settings in every one of three reseeded repeats, and `21/30` settings remain above a `+0.02` margin threshold in all repeats. The remaining fragility is localized to low- and intermediate-budget `two_moons`, with `eta = 0.70`, budget `4` positive in `1/3` repeats and `eta = 0.99`, budget `4` positive in `2/3` repeats. The figure therefore supports one bounded systems claim: detector efficiency, total photon budget, task geometry and receiver choice all matter, and hidden-layer training strengthens that conclusion without turning it into a universal superiority claim.

## Allowed and disallowed claims

### Allowed
- The current project now has a standalone top-level Figure 4 object built directly from saved benchmark outputs and synchronized to the stronger trainable robustness result.
- In the plotted surrogate benchmark, activation is clearly worthwhile for `concentric_circles` and not yet worthwhile for `two_moons` across the scanned settings.
- In the separate trainable-hidden-layer robustness check, activation beats the trainable linear baseline in `22/30` settings in every repeat, with the fragile remainder localized to `two_moons`.
- Route preference between homodyne and displaced on-off depends on task geometry, detector efficiency, and photon budget.

### Not allowed
- Do not claim full-network superiority.
- Do not claim either homodyne or on-off is globally best.
- Do not claim that this minimal benchmark is already a hardware feasibility map.
- Do not present the lower-bound reference as a physically implemented network.

## Provenance
- Numerical source: `task_level_benchmark.py`
- Saved benchmark summary: `task_level_benchmark/task_level_benchmark_summary.json`
- Trainable robustness source: `trainable_task_benchmark_seed_robustness.py`
- Trainable robustness summary: `trainable_task_benchmark_seed_robustness/seed_robustness_summary.json`
- Figure generator: `figure4_task_level_panel.py`
- Figure outputs:
  - `figure4_task_level_panel/figure4_task_level_panel.svg`
  - `figure4_task_level_panel/figure4_task_level_panel.png`
  - `figure4_task_level_panel/figure4_task_level_panel.pdf`
  - `figure4_task_level_panel/figure4_task_level_panel_data.csv`

## What remains after this package
- Harmonize the rest of the paper package, especially abstract, discussion and methods, to the stronger systems evidence now visible in the Figure-4-facing package.
- Assemble the final submission archive package.
