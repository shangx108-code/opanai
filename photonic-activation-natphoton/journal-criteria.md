# Journal Criteria

## Target journal
Nature Photonics

## Verified venue notes
- Nature Photonics says it publishes top-quality peer-reviewed research in all areas of light generation, manipulation and detection.
- Its listed coverage explicitly includes optoelectronic devices and components, quantum optics, and nonlinear optics.
- The paper therefore needs both photonics substance and broad significance; a narrow machine-learning benchmark alone will not clear the bar.

## Practical standard for this project
To be competitive as a theory-and-simulation Nature Photonics article, this paper likely needs all of the following:
- a field-level question that matters beyond one dataset or one photonic implementation
- a conceptual advance that reorganizes how nonlinear activation is discussed or designed
- a physically interpretable metric or bound, not only empirical curves
- a realistic path to experimental validation or device-level decision-making
- clear separation from adjacent programmable-nonlinearity and low-photon-computing papers

## Current distance to threshold
- Scope fit: good
- Significance potential: medium to high
- Conceptual sharpness: medium to high
- Novelty separation from recent literature: still insufficient, but improving
- Evidence completeness: still insufficient, but materially improved
- Device relevance: now demonstrated more convincingly at the single-neuron boundary-discrimination level
- Broad-reader accessibility: improved, but not yet secured across a full manuscript

## Immediate venue-specific rules for this project
1. The main claim must be expressible without depending on a long list of ad hoc metrics.
2. "Quantum limit" language must be matched to explicit assumptions and clearly stated optimization targets.
3. "Useful nonlinear resource" must be defined operationally, not rhetorically.
4. The paper should state where measurement-induced activation loses, not only where it wins.
5. The main text should lead with physics and device consequences, not dataset performance.

## Citation caution
- All references copied from the source note must be treated as provisional until verified from primary sources.
- Recent 2024-2025 Nature-family photonics papers must be explicitly positioned because they directly affect the novelty threshold.

## What this run newly satisfies
- The project now has one concrete measurement-induced activation route on the same axes as the coherent-state discrimination lower bound.
- The project now has a second concrete same-axis route using displaced on-off counting.
- Detector efficiency now appears as an explicit device-facing control axis rather than as a generic future parameter.
- The paper can now support a stronger bounded statement that is plausible for Nature Photonics readers:
  detector efficiency sets the global accessibility of the frontier, while measurement choice sets a further constant-factor overhead above it.
- The project now has a submission-grade Figure-3 candidate with regime annotations, caption logic, claim boundaries, and Results-ready prose.
- The project now has a first real task-level benchmark package with reproducible outputs rather than only a planned Figure-4 placeholder.
- The manuscript can now support a more mature design statement:
  activation is worth paying for only in task-and-budget regimes where the nonlinear gain exceeds the fixed-budget reliability penalty.
- The benchmark now shows that implementable-route preference does not follow trivially from single-neuron closeness to the lower bound once width allocation is included.

## What this run still does not satisfy
- No verified literature-positioning subsection yet shows why the new mixed task-level result changes the novelty landscape relative to 2024-2025 photonic nonlinearity papers.
- No cleaned reference ledger yet separates checked primary citations from placeholders.
- No manuscript-grade Figure-3 to Figure-4 integration yet exists in one continuous Results flow.

## Current venue risk summary
- The paper is now less likely to be dismissed as incomplete on task-level consequence grounds, but it is still at risk of being judged insufficiently distinctive because the manuscript has not yet secured its literature-positioning argument or cleaned reference base.
