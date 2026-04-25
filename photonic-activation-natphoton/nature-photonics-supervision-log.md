# Nature Photonics Supervision Log

## 2026-04-25 | Post-derivation supervision update

### Current version overall evaluation
- The project is still below Nature Photonics article standard, but this run produced a real theory advance rather than another planning layer.
- The completed bound is useful because it converts part of the activation story into an operational discrimination limit with explicit assumptions.

### What is now at least partially improved
- The theory section no longer has to begin from purely rhetorical language about "activation cost".
- One local quantity is now derivable and referee-checkable.

### What remains below target-journal standard
- The derivation is local and binary; the paper still lacks a unified framework and any benchmark that shows decision-relevant design consequences.
- There is still no figure-grade numerical evidence.
- The manuscript still lacks a verified novelty separation against 2024-2025 programmable-photonic-nonlinearity work.

### Core quality risk
- The new bound could still be rejected as mathematically neat but too elementary unless it is rapidly connected to a regime map, failure boundary, or architecture comparison that changes a design conclusion.

### Evidence-chain gap
- Missing link from analytical lower bound to real plots and hardware-relevant parameter regions
- Missing statement of where AQMA is expected to approach the bound and where it will not
- Missing text that positions the result against recent linear-optics-enabled nonlinear processing papers

### Must-correct items
1. Do not call the new result a full quantum limit for photonic neural networks; it is only a lower bound for one boundary decision primitive under stated assumptions.
2. Convert the bound into real numerical curves before using it as a central figure claim.
3. Write the limitations next to the result, not in a later cleanup pass.

### Priority adjustment
- Main bottleneck remains evidence completeness.
- Immediate sub-bottleneck is now narrower: convert the completed derivation into figure-ready numerical evidence.

### Permission to move to next phase
- Partial only.
- The project may move from pure theory strengthening toward first result generation, but not yet to manuscript-level claiming or full review iteration.

### Next supervision focus
- Whether the first numerical curve actually creates a design boundary that matters for Nature Photonics readers.

## 2026-04-25 | Post-scan supervision update

### Current version overall evaluation
- This run achieved the correct next move: the project now contains real numerical evidence derived from the proved lower bound, not just a symbolic statement.
- The quality level is still well below Nature Photonics article standard, but the evidence chain is more credible because the theory has now been exercised quantitatively.

### What is now genuinely improved
- A first lower-bound regime map now exists in numerical form.
- The project can now state concrete scale changes, for example:
  reducing the allowed boundary error from `0.40` to `0.01` raises the lower-bound mean boundary cost from `0.010205` to `0.807232`.
- The local linear encoding model also now exposes a concrete sharpness penalty:
  at `delta = 0.10`, the minimum gain rises from `1.010223` at `epsilon = 0.40` to `8.984607` at `epsilon = 0.01`.

### What remains below target-journal standard
- The new curve is still a lower bound only; without a concrete architecture trace, a referee can still say the result is physically unsurprising.
- No measured or simulated device route has yet been placed on the map.
- No final figure panel or manuscript subsection yet communicates the result in submission-grade form.

### Core quality risk
- If the project stops here, the curve will look like a mathematically inevitable monotonic tradeoff instead of a result that changes photonic design choices.

### Evidence-chain gap
- Missing explicit AQMA-like or other measurement-induced activation model to compare against the bound
- Missing statement of which region of the bound is physically accessible versus merely formal
- Missing figure assembly and caption logic that turn the data into a journal-relevant message

### Must-correct items
1. Use the numeric scan to make only lower-bound claims, not performance claims.
2. Add one concrete architecture curve next; otherwise the reader still cannot judge practical consequence.
3. Keep the local-linear encoding assumption visible whenever the `g_min(delta, epsilon)` map is discussed.

### Priority adjustment
- The main bottleneck has shifted from "absence of numerics" to "absence of a device-level comparison on the same axes."

### Permission to move to next phase
- Yes, but only one step forward:
  the project may now move from first result generation to first comparison generation.

### Next supervision focus
- Whether the first comparison demonstrates a nontrivial accessible or inaccessible region relative to the lower bound.
