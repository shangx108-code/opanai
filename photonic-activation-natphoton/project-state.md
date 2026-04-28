# Project State

## Project
- Working title: Activation quantum cost for photonic neural networks
- Target journal: Laser & Photonics Reviews
- Source note: initialized from `/workspace/user_files/01-1-.txt` on 2026-04-25
- LPR reference bundle: `/workspace/user_files/01-cankao.zip` ingested on 2026-04-26

## Research goal
Build a publishable theory-and-simulation paper that turns the vague claim "photonic neural networks need nonlinearity" into a journal-grade result: a quantitative resource framework for nonlinear activation under quantum noise, finite shots, detector inefficiency and loss, together with a measurement-induced activation architecture, benchmark-grade evidence, and device-level design maps.

## Current stage
LPR manuscript-assembly stage. The project now has a formal theory framework, benchmark specification, LPR style notes, a complete LPR-facing rewrite draft, citation-checked novelty positioning, a Figure-3-grade single-neuron frontier package, a first task-level benchmark, and a stronger trainable-network benchmark under common photon-budget accounting.

## Current main bottleneck
Under the required fixed bottleneck order, the first real blocker is still an evidence-chain gap rather than prose assembly: the trainable systems evidence is stronger than before, but until it reaches beyond the original `concentric_circles` / `two_moons` pair the manuscript remains vulnerable to the criticism that the task-level design rule is geometry-specific.

## Highest-priority objective for the current round
Fuse the upgraded numerical evidence into the rewritten LPR manuscript so the paper moves from "strong components" to one submission-grade, reviewer-proof draft.

## Proposed central claim
The real scalability bottleneck of photonic neural networks is not linear optics but the physical cost of nonlinear activation; this cost can be cast as a quantum resource problem, and measurement-induced adaptive activation approaches the useful energy frontier only inside explicitly quantified detector-, loss-, and sampling-limited regimes.

## Mandatory evidence package
- Formal definition of activation quantum cost, discrimination cost, and task-level energy-accuracy cost
- Unified activation model covering electronic, Kerr-like, saturable, photon-counting, homodyne, and AQMA-style measurement-feedback activation
- Single-neuron approximation benchmark for at least five target activation families
- Same-axis frontier comparison against at least two implementable measurement-induced routes
- Task-level benchmark showing where activation is worth paying for and where it is not
- Stronger trainable-network benchmark under the same photon-budget accounting
- Robustness scans over detector efficiency, dark count, optical loss, and finite-shot sampling
- Clear positioning relative to recent LPR and adjacent photonic neural-network literature

## What is already strong
- The question is pitched at a field level rather than as one more classifier demo
- The AQMA architecture is mechanistic, testable, and now framed in venue-appropriate LPR language
- The project has a Figure-3-grade frontier package with regime annotations and claim boundaries
- The project has both a minimal task benchmark and a stronger trainable-network benchmark under the same accounting logic
- The uploaded LPR corpus provides venue-specific writing and framing guidance
- The novelty case is citation-checked against the strongest 2024-2025 comparator papers
- A complete LPR-style manuscript rewrite draft now exists and can absorb benchmark results directly

## What is still missing
- One fully integrated LPR main-text draft that replaces placeholder logic with the upgraded Figure-3 and Figure-4 narrative
- Final figure/caption packages aligned to the rewritten manuscript
- A fuller clean reference ledger beyond the current core set
- A final supplementary package with derivation details, benchmark assumptions, and provenance

## Acceptance probability (stage estimate)
- Laser & Photonics Reviews: 62-72% after LPR rewrite plus upgraded benchmark evidence
- Reason: the project now has a realistic venue target, a manuscript rewrite in the right journal voice, and materially stronger evidence than a concept-only draft. The main residual risk is assembly quality rather than basic scientific direction.

## Last update
2026-04-28: executed a focused trainable-benchmark geometry extension on a noisy XOR-quadrants task using `trainable_task_benchmark_xor_extension.py`. Under the same activation-photon accounting and three-repeat reseeding protocol, physical activation beats the trainable linear baseline in `14/15` scanned `(eta, budget)` settings on average, with `12/15` settings remaining above the `+0.02` margin threshold in all repeats. This narrows, but does not fully close, the remaining systems-evidence breadth gap; the manuscript was updated in place to reflect the new bounded three-regime task-geometry narrative.
