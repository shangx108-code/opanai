# Nature Photonics Role Assignments

## Current Phase
- The stronger trainable-plus-robustness evidence has now entered the manuscript Results text; the immediate next phase is to synchronize the Figure-4 caption/object and the remaining paper sections to that stronger evidence.

## Role Task Table

### Coordinator
- Current task: close the remaining gap between the revised Results text and the still-minimal Figure-4 package.
- Input: revised manuscript Results subsection, `figure4_submission_package.md`, `figure4_trainable_benchmark_package.md`, seed-robustness summary files, current review history.
- Output: one synchronized figure-facing revision target that upgrades systems evidence without widening the paper's scope.
- Completion standard: the next action must make the top-level visual/caption package reflect the strongest real evidence already described in the paper text.
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
- Current task: prepare a revised Figure-4 direction and caption that reflect the trainable benchmark and seed-robustness evidence rather than the older minimal benchmark only.
- Input: trainable benchmark package and seed-robustness outputs.
- Output: one revised figure or caption target for the next run.
- Completion standard: the next figure-facing revision must be traceable to saved trainable and robustness outputs.
- Priority: highest

### Manuscript Writer
- Current task: keep the revised Results subsection fixed and extend the same evidence discipline into caption and section harmonization.
- Input: revised manuscript source/PDF, trainable benchmark package, seed-robustness outputs.
- Output: one bounded follow-up revision that prevents the rest of the paper from lagging behind the updated Results text.
- Completion standard: not yet met until the stronger benchmark and its caveats appear consistently wherever Fig. 4 is summarized.
- Priority: highest

### Supervisor
- Current task: treat partial synchronization as the dominant risk.
- Input: revised manuscript PDF, Figure-4 package, review history, journal criteria.
- Output: a next-stage supervision target focused on figure/package synchronization and honest scope control.
- Completion standard: the project should not leave stronger verified evidence stranded in text while the top-level figure package still says less.
- Priority: highest

### Strict Reviewers
- Current task: update acceptance estimates after the paper text itself incorporated the stronger trainable benchmark and real seed-robustness check.
- Input: revised manuscript source/PDF, trainable benchmark package, seed-robustness outputs, prior review history.
- Output: revised reviewer matrix and the next upgrade condition.
- Completion standard: the project state must reflect that reviewer-visible evidence improved, while still recording the remaining figure-package mismatch.
- Priority: high

## What Was Completed In This Run
- Completed: revised the manuscript Results subsection so it now states the stronger trainable-hidden-layer benchmark and the repeat-stable `22/30` headline.
- Completed: the revised Results text now names the six robust high-budget `two_moons` gains and the localized fragile low/intermediate-budget `two_moons` regimes.
- Completed: re-rendered the manuscript PDF after the Results revision.

## What Remains Incomplete
- Incomplete: the Figure-4 caption/object still reflects the older minimal benchmark rather than the stronger trainable-plus-robustness evidence.
- Incomplete: abstract, discussion and methods harmonization to the stronger systems evidence remains open.
- Incomplete: final submission archive remains open.

## Next Immediate Deliverable
- One figure-facing Figure-4 caption/package revision built directly from the trainable and seed-robustness outputs.
