# Figure 4 Submission Package

## Objective of this package
- Convert the already saved minimal task-level benchmark into one manuscript-grade top-level figure object.
- Keep the claim bounded to the real benchmark already computed in this project namespace.

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

## Caption draft
**Figure 4 | Task-level worth of physical activation depends on task geometry, detector efficiency and total photon budget.**
**a,b,** Best implementable test-accuracy margin above the task-specific linear no-activation baseline for the saved minimal benchmark, plotted against total activation photon budget per inference for `two_moons` (**a**) and `concentric_circles` (**b**). Each point selects the better of the two implementable activation routes at that `(task, eta, budget)` setting, with line color denoting detector efficiency `eta` and marker shape denoting whether homodyne or displaced on-off counting is preferred. Width labels give the selected hidden-layer width for the best route. For `concentric_circles`, paying for activation is worthwhile across all `15/15` scanned settings, whereas for `two_moons` no implementable route exceeds the linear baseline within the scanned range up to budget `16`.
**c,** Difference between displaced on-off and homodyne test accuracy over the same `30` matched settings. The sign of this difference changes across tasks and budgets, and displaced on-off is better in only `9/30` comparisons. The systems-level conclusion is therefore narrower than a simple single-neuron ranking: the Fig. 3 frontier changes real design choices, but closeness to that frontier alone does not determine which implementable activation route is best once total photon budget must be distributed across a task.

## Allowed and disallowed claims

### Allowed
- The current project now has a standalone top-level Figure 4 object built directly from saved benchmark outputs.
- In this minimal benchmark, activation is clearly worthwhile for `concentric_circles` and not yet worthwhile for `two_moons` across the scanned settings.
- Route preference between homodyne and displaced on-off depends on task geometry, detector efficiency, and photon budget.

### Not allowed
- Do not claim full-network superiority.
- Do not claim either homodyne or on-off is globally best.
- Do not claim that this minimal benchmark is already a hardware feasibility map.
- Do not present the lower-bound reference as a physically implemented network.

## Provenance
- Numerical source: `task_level_benchmark.py`
- Saved benchmark summary: `task_level_benchmark/task_level_benchmark_summary.json`
- Figure generator: `figure4_task_level_panel.py`
- Figure outputs:
  - `figure4_task_level_panel/figure4_task_level_panel.svg`
  - `figure4_task_level_panel/figure4_task_level_panel.png`
  - `figure4_task_level_panel/figure4_task_level_panel.pdf`
  - `figure4_task_level_panel/figure4_task_level_panel_data.csv`

## What remains after this package
- Integrate the new Figure 4 object into the main manuscript and harmonize caption style across the full paper package.
- Assemble the final submission archive package.
