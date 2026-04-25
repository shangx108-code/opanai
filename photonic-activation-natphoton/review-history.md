# Review History

## 2026-04-25 | Pre-manuscript triage

### Material reviewed
- Source note: `/workspace/user_files/01-1-.txt`

### Venue lens
Nature Photonics research article standard

### Reviewer-style verdict
Current outcome: major revision before a full draft even exists

### Why
1. The proposed topic is timely and broad enough for the journal, but the present evidence is still conceptual.
2. The note identifies the right bottleneck, yet it does not fully prove that activation quantum cost is both new and indispensable relative to adjacent recent work.
3. AQMA is promising as a proposed architecture, but no result yet shows a clear regime where it changes design decisions.

### Closest pressure points from current literature
- Nature Photonics aims and scope confirm fit for nonlinear optics, quantum optics, optoelectronic components, and emerging photonic applications.
- Bandyopadhyay et al., *Single-chip photonic deep neural network with forward-only training*, Nature Photonics 18, 1335-1343 (2024), raises the standard for photonic-AI relevance.
- Yildirim et al., *Nonlinear processing with linear optics*, Nature Photonics 18, 1076-1085 (2024), narrows the space for claims that nonlinearity always requires intrinsic material nonlinearity.
- Wu et al., *Field-programmable photonic nonlinearity*, Nature Photonics 19, 725-732 (2025), raises the bar for programmability and device-level relevance.
- Wang et al., *An optical neural network using less than 1 photon per multiplication*, Nature Communications 13, 123 (2022), already occupies the low-photon task-demonstration lane.

### Five-reviewer baseline
- Reviewer 1 (novelty-focused): 18%
- Reviewer 2 (theory-rigor-focused): 16%
- Reviewer 3 (device/implementation-focused): 14%
- Reviewer 4 (broad-reader clarity-focused): 22%
- Reviewer 5 (benchmark/comparison-focused): 15%

### Acceptance-probability trend
- Start-of-project estimate for Nature Photonics: 12-20%
- Upgrade condition to 25-35%: formalize the framework and produce first benchmark-grade numerical figures
- Upgrade condition to 35-50%: prove at least one actionable regime boundary where AQMA or measurement-induced activation changes the optimal design choice
- Upgrade condition to 50-70%: complete a manuscript package with clear literature separation, reproducible numerics, and submission-grade figures

## 2026-04-25 | Formalization-package review

### Material reviewed
- Theory framework: `/workspace/memory/photonic-activation-natphoton/theory-framework.md`
- Benchmark specification: `/workspace/memory/photonic-activation-natphoton/benchmark-spec.md`
- Manuscript spine: `/workspace/memory/photonic-activation-natphoton/manuscript-spine.md`

### Reviewer-style verdict
Current outcome: major revision, but materially stronger than concept-only stage

### What improved
1. The paper now has a central quantity, explicit assumptions, and a clear separation between function imitation, discrimination, and task-level usefulness.
2. The benchmark plan is structured around falsification, which is much healthier for a selective journal.
3. The manuscript spine is now journal-facing rather than note-like.

### Remaining blockers
1. No benchmark result yet demonstrates a design-changing regime boundary.
2. Novelty relative to recent programmable/nonlinear photonic work is still argued rather than shown.
3. The current package still lacks a first real figure, which keeps the acceptance ceiling low.

### Updated five-reviewer baseline
- Reviewer 1 (novelty-focused): 24%
- Reviewer 2 (theory-rigor-focused): 29%
- Reviewer 3 (device/implementation-focused): 18%
- Reviewer 4 (broad-reader clarity-focused): 31%
- Reviewer 5 (benchmark/comparison-focused): 21%

### Acceptance-probability trend
- Updated estimate for Nature Photonics: 18-26%
- Upgrade condition to 30-40%: generate the first regime-boundary benchmark and show where AQMA changes the frontier
- Upgrade condition to 40-55%: integrate benchmark evidence into a coherent manuscript package with verified literature separation

## 2026-04-25 | First same-axis architecture-comparison review

### Material reviewed
- Lower-bound project state entry
- Homodyne comparison note: `/workspace/memory/photonic-activation-natphoton/aqma-homodyne-comparison.md`

### Reviewer-style verdict
Current outcome: major revision, but now with the first concrete evidence that the framework produces a device-facing design law rather than only a formal lower bound

### What improved
1. The paper now has one concrete measurement-induced route on the same axes as the lower bound.
2. Detector efficiency has become a quantitative control variable with a clear penalty on boundary-energy cost.
3. The project can now make one bounded main-text claim about when a measurement-induced route stays near the frontier and when it does not.

### Remaining blockers
1. Only one architecture trace exists, so the comparison can still be dismissed as illustrative.
2. No submission-grade figure or caption package yet communicates the result.
3. Novelty relative to recent photonic nonlinearity papers is still only partially discharged because the comparison set remains too narrow.

### Five-reviewer dimension estimates
- Reviewer 1, novelty-focused:
  innovation/significance `34/100`; theory rigor `45/100`; method reliability `42/100`; data/results `37/100`; figure quality `20/100`; writing `28/100`; journal fit `44/100`; acceptance estimate `26%`.
- Reviewer 2, theory-rigor-focused:
  innovation/significance `36/100`; theory rigor `58/100`; method reliability `49/100`; data/results `40/100`; figure quality `20/100`; writing `30/100`; journal fit `45/100`; acceptance estimate `34%`.
- Reviewer 3, device/implementation-focused:
  innovation/significance `33/100`; theory rigor `46/100`; method reliability `47/100`; data/results `39/100`; figure quality `20/100`; writing `27/100`; journal fit `43/100`; acceptance estimate `27%`.
- Reviewer 4, broad-reader-clarity-focused:
  innovation/significance `35/100`; theory rigor `46/100`; method reliability `43/100`; data/results `41/100`; figure quality `22/100`; writing `33/100`; journal fit `47/100`; acceptance estimate `30%`.
- Reviewer 5, benchmark/comparison-focused:
  innovation/significance `35/100`; theory rigor `50/100`; method reliability `48/100`; data/results `45/100`; figure quality `21/100`; writing `29/100`; journal fit `45/100`; acceptance estimate `33%`.

### Review interpretation
- Reviewer 2 and Reviewer 5 move the most because the project now contains a real same-axis comparison rather than a bound alone.
- Reviewer 3 improves, but only modestly, because the detector-efficiency dependence is informative without yet being a full hardware-feasibility map.
- Reviewer 1 still sees a narrow evidence base because there is only one architecture beside the lower bound.

### Acceptance-probability trend
- Updated estimate for Nature Photonics: 24-34%
- Upgrade condition to 35-45%: add a second architecture baseline or a figure-grade accessible-region panel that makes the comparison feel field-relevant rather than illustrative
- Upgrade condition to 45-60%: integrate the comparison into manuscript text with verified literature separation and at least one stronger device-facing figure

## 2026-04-25 | Second same-axis architecture-comparison review

### Material reviewed
- Lower-bound project state entry
- Homodyne comparison note: `/workspace/memory/photonic-activation-natphoton/aqma-homodyne-comparison.md`
- Displaced on-off comparison note: `/workspace/memory/photonic-activation-natphoton/kennedy-onoff-comparison.md`
- Reproducible script: `/workspace/memory/photonic-activation-natphoton/same_axis_metrics.py`

### Reviewer-style verdict
Current outcome: major revision, but the paper is now meaningfully closer to a selective-journal result because the core comparison has moved from one route to a small architecture family.

### What improved
1. The evidence base now includes two physically distinct measurement-induced routes on the same axes as the lower bound.
2. The project can now separate two effects cleanly: detector efficiency sets the global `1 / eta` penalty, while measurement architecture changes the constant-factor overhead above the limit.
3. The numerical path is now reproducible from saved code rather than living only in prose.

### Remaining blockers
1. The new result is still not packaged as a submission-grade figure and caption.
2. The manuscript still lacks a verified literature-positioning paragraph against the strongest 2024-2025 photonic-nonlinearity papers.
3. There is still no task-level evidence showing whether the single-neuron frontier changes network-level design choices.

### Five-reviewer dimension estimates
- Reviewer 1, novelty-focused:
  innovation/significance `42/100`; theory rigor `52/100`; method reliability `50/100`; data/results `47/100`; figure quality `23/100`; writing `31/100`; journal fit `50/100`; acceptance estimate `33%`.
- Reviewer 2, theory-rigor-focused:
  innovation/significance `41/100`; theory rigor `64/100`; method reliability `58/100`; data/results `50/100`; figure quality `23/100`; writing `32/100`; journal fit `50/100`; acceptance estimate `39%`.
- Reviewer 3, device/implementation-focused:
  innovation/significance `40/100`; theory rigor `52/100`; method reliability `55/100`; data/results `49/100`; figure quality `23/100`; writing `30/100`; journal fit `49/100`; acceptance estimate `35%`.
- Reviewer 4, broad-reader-clarity-focused:
  innovation/significance `41/100`; theory rigor `52/100`; method reliability `51/100`; data/results `50/100`; figure quality `24/100`; writing `36/100`; journal fit `52/100`; acceptance estimate `36%`.
- Reviewer 5, benchmark/comparison-focused:
  innovation/significance `43/100`; theory rigor `58/100`; method reliability `58/100`; data/results `56/100`; figure quality `24/100`; writing `32/100`; journal fit `51/100`; acceptance estimate `41%`.

### Review interpretation
- Reviewer 5 improves the most because the comparison is no longer a single worked example.
- Reviewer 2 also moves upward because the constant-factor-versus-scaling distinction is now mathematically cleaner.
- Reviewer 1 remains restrained because novelty is still only partially secured until the manuscript explicitly positions the new comparison against recent photonic nonlinearity papers.

### Acceptance-probability trend
- Updated estimate for Nature Photonics: 31-41%
- Upgrade condition to 40-50%: assemble a main-text Figure 3 with clear regime annotations and a reviewer-safe Results subsection
- Upgrade condition to 50-65%: add verified literature separation and at least first task-level evidence that the single-neuron frontier changes system-level design choices
