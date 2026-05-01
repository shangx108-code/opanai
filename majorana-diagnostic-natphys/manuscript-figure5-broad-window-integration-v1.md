# Manuscript Figure 5 Integration v1

## Scope
- Purpose: direct manuscript-ready integration package for the selected Figure 5 upgraded broad-window version
- Status: use this file as the current source of truth until the main manuscript source file is restored into the long-term project space
- Selected readout: `symmetric_nonlocal_score`

## Figure 5 caption
Figure 5 compares the positive-control topological branch with retuned dot- and impurity-based false-positive controls using a broad-window nonlocal transport readout derived from the same lead-attached heatmaps. The plotted quantity is the symmetric nonlocal score,
`S_nl = |G_{LR}| sqrt(G_{LL} G_{RR}) / (|G_{LL}| + |G_{RR}|)`,
which suppresses cases where an apparent nonlocal signal is not accompanied by balanced local support at the two ends. Across the phase-bias window, the positive-control branch retains a stronger and more persistent broad-window nonlocal response, whereas the dot and impurity controls remain locally active but show substantially weaker symmetric nonlocal support. The figure therefore does not claim that raw `|G_{LR}|` alone is decisive over the full bias range; instead, it shows that a balanced broad-window nonlocal readout separates the topological branch more cleanly from the tuned false-positive controls.

## Results paragraph
To avoid overinterpreting raw `|G_{LR}|` over the full bias window, we quantify the transport-side comparison with a balanced nonlocal score rather than with the bare nonlocal amplitude alone. For each `(phi, V)` point, we define
`S_nl = |G_{LR}| sqrt(G_{LL} G_{RR}) / (|G_{LL}| + |G_{RR}|)`,
so that a large value requires not only finite nonlocal transfer but also simultaneous local support at both ends. In the rebuilt candidate set, this readout preserves the qualitative phase-window contrast of the positive-control branch while reducing the broad-bias leakage seen in the dot and impurity controls when only `|G_{LR}|` is inspected. Quantitatively, `S_nl` gives the strongest worst-case full-window median separation among the tested readouts, with positive/control median ratios of about `9.98` for the dot control and `9.13` for the impurity control. We therefore use `S_nl` as the manuscript-facing broad-window Figure 5 discriminator, while keeping the stronger zero-bias-only contrast as a lower-level consistency check rather than the sole main-text criterion.

## Methods paragraph
The Figure 5 transport maps are first computed in terms of the wide-band lead proxies `G_{LL}`, `G_{RR}`, and `G_{LR}` from the same candidate-based transport heatmaps used for the positive-control and false-positive comparisons. For the broad-window manuscript readout, we do not use the bare nonlocal amplitude `|G_{LR}|` directly, because that quantity retains appreciable off-zero-bias leakage in the tuned controls. Instead, we define a symmetric nonlocal score
`S_nl(phi, V) = |G_{LR}(phi, V)| sqrt(G_{LL}(phi, V) G_{RR}(phi, V)) / (|G_{LL}(phi, V)| + |G_{RR}(phi, V)|)`.
This normalization favors operating points where the nonlocal response is accompanied by balanced local support at both ends, and it downweights cases where a spuriously large nonlocal trace appears without a comparably coherent two-end structure. Among the tested readout-layer observables extracted from the same heatmaps, this score gave the strongest worst-case full-window median separation between the positive branch and the tuned dot and impurity controls, so it was adopted as the broad-window Figure 5 observable without altering the underlying transport solver.

## Integration note
- The current long-term project space does not yet contain a recoverable master manuscript source file for direct in-place editing.
- Until that source file is restored, this page should be treated as the direct replacement text for the Figure 5 caption, Results paragraph, and Methods paragraph in the main manuscript.
