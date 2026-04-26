# Supervision Log

## 2026-04-25 Round 1

### Overall Assessment

The project direction is journal-aware and much stronger than a generic optical neural-network simulation paper. The strongest part is the framing around nonlinear activation as the true bottleneck. The weakest part is the absence of end-to-end evidence that the proposed framework changes conclusions at the task and hardware levels.

### Gap To Target Journal

Nature Photonics will likely expect more than a conceptual taxonomy. At minimum, the manuscript must show:

1. a genuinely general metric, not just one convenient proxy
2. numerical evidence that the metric predicts task-level performance shifts
3. realistic device-boundary analysis anchored to detector and platform constraints
4. clear positioning against 2024-2025 photonic nonlinearity and stochastic optical neural-network work

### Current Highest Risk

Referees may interpret the present draft direction as an under-validated framework paper if the manuscript stops at function-fitting scans.

### Required Strengthening

1. Add low-light benchmark tasks tied directly to photons per activation or photons per inference.
2. Add realistic detector efficiency, loss and dark-count models.
3. Distinguish when AQMA is superior and when existing nonlinear mechanisms remain preferable.
4. Prepare a sharper novelty paragraph against single-chip integrated nonlinear activations and SPD-based stochastic ONNs.

### Plan Correction

Do not spend the next round polishing prose first. The next round must prioritize evidence generation and only then expand the manuscript.

## 2026-04-26 Round 2

### Overall Assessment

The project has moved from concept-only framing to a genuine evidence-building phase. This is a meaningful upgrade: the paper now contains one analytic lower-bound component, one device-aware scan and one Monte Carlo benchmark.

### What Improved

1. The evidence base now includes real parameter sweeps with efficiency, loss and dark count.
2. The benchmark accuracy is no longer implied from function fitting alone.
3. The analytic bound provides a defensible floor for binary discrimination cost under Poisson statistics.

### Remaining Gap To Target Journal

1. One toy benchmark is still not enough for a top-tier venue.
2. The current lower bound is rigorous only for a defined discrimination setting, not for the full activation-approximation problem.
3. The device-feasibility story still needs clearer mapping to named photonic platforms and detector technologies.

### Current Highest Risk

The manuscript may still overuse the phrase "quantum limit" unless each occurrence is tied either to the proven discrimination bound or to an explicitly optimization-based numerical lower envelope.

### Plan Correction

The next round should prioritize:

1. a second benchmark or ablation that tests whether AQMA retains value under harsher noise or smaller feature budgets
2. a Methods-quality derivation note and notation cleanup
3. figure-ready source tables for the main data plots
