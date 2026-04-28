# Supervision Log

## 2026-04-25 | Round 1 initialization

### Overall evaluation
The project began with a strong problem choice and a plausible photonics angle, but it was still mostly a concept note.

### Most critical quality risk
The paper could have been rejected as a polished perspective disguised as a research article if the framework was not tied to decisive calculations and bounded claims.

### Plan-revision advice
1. Center the story on one quantity: activation quantum cost.
2. Make the first real technical output a formal framework with explicit assumptions.
3. Treat AQMA as a candidate route, not as an already proven superior architecture.

## 2026-04-25 | Round 2 after formalization

### Overall evaluation
The project became much healthier once the theory framework, benchmark specification, and manuscript spine were written. The key question shifted from framing to whether the numerics would reveal a real design boundary.

### Most critical quality risk
The project could become over-formalized without becoming more convincing if the first numerical cycle only confirmed obvious trade-offs.

### Plan-revision advice
1. Make the first numerical target a regime-boundary figure.
2. Require every upcoming figure to answer a yes-or-no design question.
3. Do not broaden tasks until the single-neuron and frontier comparisons are decisive.

## 2026-04-25 | Round 8 after upgraded benchmark evidence

### Overall evaluation
The project now contains real frontier evidence, a task-level benchmark, and a stronger trainable benchmark. The main bottleneck is no longer first-order evidence generation.

### Most critical quality risk
The project could lose acceptance probability by failing to convert stronger evidence into a coherent submission-grade manuscript.

### Plan-revision advice
1. Do not keep expanding benchmark variants unless manuscript assembly exposes a concrete inconsistency.
2. Replace old placeholder Figure-4 logic with the trainable benchmark narrative everywhere.
3. Preserve negative regions and non-universal route preference because they strengthen credibility.

## 2026-04-26 | Round 9 after LPR retargeting and rewrite

### Overall evaluation
The project is now much better matched to its target venue. The manuscript reads like an optics/photonics research article rather than a high-concept manifesto, and it now sits on top of a substantially stronger evidence base than a concept-only rewrite.

### Gap to target-journal standard
- Venue fit and article voice are now acceptable.
- The remaining weakness is assembly quality, not raw scientific direction.
- The paper still needs a tightly integrated main text and supplement before it can be treated as submission-ready.

### Most critical quality risk
The draft could still underperform in review if the upgraded evidence remains distributed across notes, figure packages, and benchmark folders instead of being merged into one clear article.

### Plan-revision advice
1. Treat the rewritten abstract and introduction as stable for one cycle.
2. Spend the next major effort on integrating Figure 3 and Figure 4 into the LPR draft.
3. Let final manuscript assembly, bibliography cleanup, and figure captioning drive the next round rather than more exploratory benchmarking.

## 2026-04-28 | Round 10 after XOR geometry extension

### Overall evaluation
The manuscript-facing task-level evidence is now less vulnerable to the criticism that the design rule was chosen by a convenient two-task contrast. A focused XOR extension added one intermediate nonlinear geometry under the same photon accounting and showed that the current picture remains selective rather than collapsing into either universal positivity or universal fragility.

### Gap to target-journal standard
- The first blocker under the fixed bottleneck order is still an evidence-chain gap, not writing polish.
- Geometry breadth is stronger than before, but the task-level evidence still lives in a small toy-task family rather than a wider benchmark suite.
- The paper is now better positioned to claim a bounded three-regime narrative, but not a task-generic law.

### Most critical quality risk
The new XOR evidence could be overused. It meaningfully narrows the systems-evidence gap, but it does not justify broad dataset-general claims or a full task survey framing.

### Newly verified facts
- `trainable_task_benchmark_xor_extension.py` was added and run successfully.
- The XOR extension produced auditable CSV, JSON, and Markdown outputs in `trainable_task_benchmark_xor_extension/`.
- Across three reseeded repeats, physical activation beat the trainable linear baseline in `14/15` scanned `(eta, budget)` settings on average.
- `12/15` XOR settings stayed above the `+0.02` margin threshold in all three repeats.
- The only fragile XOR conditions were the lowest-budget edge points at `eta = 0.50, budget = 1, 2` and `eta = 0.70, budget = 1`.

### Plan-revision advice
1. Update the main-text trainable-benchmark paragraph to absorb the XOR extension as a bounded geometry-breadth check rather than as a new headline benchmark family.
2. Preserve the narrative that weak-linear-baseline tasks are strongly positive, strong-linear-baseline tasks remain fragile at low budget, and intermediate nonlinear tasks are mostly positive but soften first at the noisiest low-budget edge.
3. Keep the next evidence pass comparably narrow, for example one architecture-side extension or one more controlled task family, instead of widening into a diffuse benchmark expansion.
