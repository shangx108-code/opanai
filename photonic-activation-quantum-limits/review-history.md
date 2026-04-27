# Review History

## Round 1 Baseline Review

Date: 2026-04-25
Target journal: Nature Photonics
Manuscript maturity: project concept + v0 single-neuron proxy simulations

### Reviewer 1

- Focus: photonic neural-network hardware expert
- Main concern: The manuscript currently has no task-level demonstration that activation quantum cost predicts meaningful network behavior.
- Score by dimension:
  - innovation and significance: 7/10
  - theory and rigor: 4/10
  - methods and code reliability: 5/10
  - data and robustness: 3/10
  - figures and expression: 4/10
  - writing completeness: 4/10
  - journal fit: 6/10
- Acceptance probability: 24%

### Reviewer 2

- Focus: nonlinear optics specialist
- Main concern: The paper must justify why AQMA is physically distinct from existing measurement-plus-electronics activation schemes and why the proposed metric is not just a relabeling of signal-to-noise trade-offs.
- Acceptance probability: 22%

### Reviewer 3

- Focus: quantum optics and measurement theory
- Main concern: The theoretical section still lacks a rigorous lower-bound statement; current results are proxy scans rather than a demonstrated quantum limit.
- Acceptance probability: 18%

### Reviewer 4

- Focus: informed but non-specialist photonics referee
- Main concern: The paper concept is clear, but the evidence chain is incomplete and would likely read as promising rather than publication-ready.
- Acceptance probability: 28%

### Reviewer 5

- Focus: device-oriented photonic computing referee
- Main concern: No realistic detector/platform comparison is yet shown, so the design-map claim is premature.
- Acceptance probability: 25%

### Composite Assessment

- Current editorial tendency: reject / invite resubmission after major strengthening
- Main drag items:
  1. no task-level benchmark evidence
  2. no rigorous lower-bound theorem or defensible bound statement
  3. no realistic device-feasibility analysis

### Required Next-Round Actions

1. Generate benchmark results linking activation cost to inference accuracy.
2. Introduce detector efficiency, loss and dark-count scans.
3. Rewrite the central claim to separate "framework established" from "quantum limit proven", unless a true bound is derived.

## Round 2 Evidence Update

Date: 2026-04-26
New evidence added: device-aware activation scan, Monte Carlo two-moons benchmark, analytic Poisson discrimination lower bound

### Reviewer 1

- Updated view: The task-level evidence is no longer missing, but it is still narrow.
- Acceptance probability: 38%

### Reviewer 2

- Updated view: The manuscript is now better grounded physically, but the distinction between measurement-induced resource advantage and standard detect-and-electronics processing still needs sharper articulation.
- Acceptance probability: 34%

### Reviewer 3

- Updated view: The new discrimination bound is valuable, but it does not yet justify a universal "quantum limit" claim for all activation classes.
- Acceptance probability: 31%

### Reviewer 4

- Updated view: The manuscript is becoming legible as a framework paper with evidence, though the narrative still needs simplification and clearer scope control.
- Acceptance probability: 43%

### Reviewer 5

- Updated view: The added efficiency-loss scans help, but the platform map remains too abstract for acceptance.
- Acceptance probability: 37%

### Composite Assessment

- Current editorial tendency: major revision territory, not yet near acceptance
- Current main drag items:
  1. benchmark breadth is still limited
  2. theory is partially rigorous but not yet comprehensive
  3. platform-anchored feasibility map is still missing

## Round 3 Evidence Update

Date: 2026-04-26
New evidence added: weak-signal benchmark and figure-ready real-data plots

### Reviewer 1

- Updated view: Two benchmarks plus real-data plots make the manuscript materially stronger, but the benchmark suite still needs a sharper connection to device relevance.
- Acceptance probability: 46%

### Reviewer 2

- Updated view: The manuscript is improved by showing that AQMA is not universally best. This helps credibility, but the physics narrative around why different tasks prefer different nonlinearities still needs strengthening.
- Acceptance probability: 44%

### Reviewer 3

- Updated view: The theory remains careful and properly scoped, which is good. The next gain must come from extending the Methods-grade derivation and avoiding inflated language.
- Acceptance probability: 39%

### Reviewer 4

- Updated view: The paper is easier to believe now that both favorable and unfavorable regimes are shown. The storyline is closer to a publishable framework article.
- Acceptance probability: 51%

### Reviewer 5

- Updated view: The device scan plus figure drafts help, but the platform comparison is still too generic for a final acceptance recommendation.
- Acceptance probability: 45%

### Composite Assessment

- Current editorial tendency: still major revision, but plausibly moving toward the upper end of that range
- Current main drag items:
  1. platform-specific feasibility interpretation is still missing
  2. the benchmark-to-theory linkage needs cleaner exposition
  3. the strongest proven lower bound still covers only a subset of the full manuscript claim

## Round 4 Evidence Update

Date: 2026-04-27
New evidence added: threshold-activation photon-floor corollary, platform window note, platform figure, figure verification report

### Reviewer 1

- Updated view: The platform mapping is more concrete now, and the figure verification removes presentation risk. The remaining concern is whether the benchmark story is broad enough for the venue.
- Acceptance probability: 53%

### Reviewer 2

- Updated view: The manuscript is now materially more credible because it distinguishes hardware-plausible windows from abstract scans. The explanation of why Kerr-like behavior remains stronger on the weak-signal task should still be sharpened.
- Acceptance probability: 50%

### Reviewer 3

- Updated view: The new threshold-activation corollary is a real theoretical improvement. The paper still does not have a universal theorem for all activation classes, but the rigor bar is now noticeably higher.
- Acceptance probability: 47%

### Reviewer 4

- Updated view: The paper is steadily becoming a coherent framework article. The mix of favorable and limiting evidence now reads as deliberate rather than incomplete.
- Acceptance probability: 58%

### Reviewer 5

- Updated view: The platform figure and source-backed window note help substantially. A more explicit device-facing discussion section could move this from interesting to convincing.
- Acceptance probability: 52%

### Composite Assessment

- Current editorial tendency: still below acceptance, but now clearly moving through the stronger half of major revision
- Current main drag items:
  1. benchmark breadth is improved but still not yet enough for a 75% acceptance outlook
  2. the theory is significantly better but not yet fully universal
  3. the platform section still needs a direct discussion of routing length, coupling and system-level effective loss
