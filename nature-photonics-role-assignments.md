# Nature Photonics Role Assignments

## Current Phase
- A real seed-robustness result now exists for the stronger trainable task benchmark; the immediate next phase is to move that stronger evidence into the manuscript-facing Figure-4 story.

## Role Task Table

### Coordinator
- Current task: replace the outdated minimal-benchmark emphasis with the now-verified trainable-plus-robustness evidence.
- Input: `manuscript-v1.md`, `figure4_submission_package.md`, `figure4_trainable_benchmark_package.md`, seed-robustness summary files, current review history.
- Output: one synchronized manuscript/figure revision target that upgrades systems evidence without widening the paper's scope.
- Completion standard: the next action must make the reviewer-facing paper reflect the strongest real evidence already in the namespace.
- Priority: highest

### Theorist
- Current task: preserve the new claim boundary created by the seed-robustness result.
- Input: trainable benchmark package, seed-robustness summary, current manuscript claim sentences.
- Output: manuscript-safe wording that states both the repeat-stable `22/30` headline and the explicitly fragile low-budget `two_moons` regimes.
- Completion standard: the stronger evidence must sharpen the claim, not inflate it into a general hardware-readiness statement.
- Priority: high

### Code And Numerical Computation
- Current task: hold the completed seed-robustness package fixed unless a manuscript-integration pass uncovers a specific missing statistic.
- Input: `trainable_task_benchmark_seed_robustness.py` and saved outputs.
- Output: no new computation requested in this run.
- Completion standard: already met for the present robustness pass.
- Priority: paused

### Data Analyst
- Current task: translate the seed-robustness outputs into the exact stable-versus-fragile regime split the manuscript should report.
- Input: `seed_robustness_summary.md`, `seed_robustness_summary.csv`, trainable benchmark summary.
- Output: a bounded interpretation map: repeat-stable positive regimes, fragile near-threshold regimes, and route-preference variability.
- Completion standard: the next manuscript revision should no longer flatten robust and fragile positive conditions into one undifferentiated claim.
- Priority: high

### Figure Lead
- Current task: prepare a revised Figure-4 direction that reflects the trainable benchmark and seed-robustness evidence rather than the older minimal benchmark only.
- Input: trainable benchmark package and seed-robustness outputs.
- Output: one revised figure or caption target for the next run.
- Completion standard: the next figure-facing revision must be traceable to saved trainable and robustness outputs.
- Priority: highest

### Manuscript Writer
- Current task: revise the Results and Figure-4 language so the manuscript matches the stronger task-level evidence already computed.
- Input: current manuscript source/PDF, trainable benchmark package, seed-robustness outputs.
- Output: one bounded manuscript revision that cites the repeat-stable `22/30` count and names the fragile exceptions.
- Completion standard: manuscript statements must match the real strengthened benchmark and its caveats.
- Priority: highest

### Supervisor
- Current task: treat manuscript lag behind the stronger evidence as the dominant risk.
- Input: seed-robustness outputs, current manuscript PDF, review history, journal criteria.
- Output: a next-stage supervision target focused on evidence synchronization and honest scope control.
- Completion standard: the project should not leave stronger verified evidence stranded outside the paper package.
- Priority: highest

### Strict Reviewers
- Current task: update acceptance estimates after the stronger trainable benchmark passed a real seed-robustness check.
- Input: trainable benchmark package, seed-robustness outputs, current manuscript source/PDF, prior review history.
- Output: revised reviewer matrix and the next upgrade condition.
- Completion standard: the project state must reflect that methods/results confidence improved even though the paper text has not yet caught up.
- Priority: high

## What Was Completed In This Run
- Completed: created and ran `trainable_task_benchmark_seed_robustness.py`.
- Completed: saved repeat-level and condition-level robustness outputs for the trainable benchmark.
- Completed: verified that the `22/30` positive-condition headline survives across all three repeats while `9/30` conditions remain fragile or negative.

## What Remains Incomplete
- Incomplete: the stronger trainable-plus-robustness evidence is not yet integrated into the manuscript or current Figure-4 story.
- Incomplete: final submission archive remains open.

## Next Immediate Deliverable
- One manuscript-facing Figure-4 and Results revision built directly from the trainable and seed-robustness outputs.
