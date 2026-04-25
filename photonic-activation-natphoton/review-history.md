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
