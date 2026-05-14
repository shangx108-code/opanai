# Submission Language Lock

## Purpose

This file locks one evidence-facing bottleneck only: how the manuscript, cover letter, and reviewer-facing prose should describe the processor-level `Figure 5` result without overstating the current evidence.

The governing evidence state is unchanged:

- Figures `1--4` carry the positive mechanism chain.
- `Figure 5` is retained as boundary / limit-setting evidence.
- No sentence may imply a robust ordinary-beating processor-level demonstration.

## Locked Title

**Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations**

Rationale:

- keeps the project identity
- centers mechanism rather than a device-win claim
- stays compatible with the current `Nature Communications` framing

## Locked Abstract

Dynamic aberrations make coherent imaging a time-varying inverse problem because the degradation state changes across frames and is not known at the moment of measurement. We ask whether a fixed diffractive optical processor can use a co-propagating reference to encode information about the instantaneous degradation without dynamic optical reconfiguration. Across Gaussian surrogate studies, wave-optics simulations with dynamic Zernike aberrations, pilot-information diagnostics, and cross-task evaluations, the current evidence supports a bounded mechanism claim: a common-path pilot can reduce uncertainty about the present degradation and improve downstream recovery relative to no-reference and non-common-path controls. The same evidence also defines a clear device-level boundary. In the present passive-processor protocol, the processor-level gain remains weak and configuration-sensitive, and the rebuilt NumPy baseline reaches only a near-tie with the best ordinary D2NN while showing at most a local matched advantage over the non-common-path control. The contribution of the manuscript is therefore mechanism-first rather than device-demonstration-first: it establishes an evidence-bounded conditional-optics framework for self-calibrating diffractive processing while making explicit the current processor-level limit.

## Locked Figure 5 Paragraph

Use this as the default replacement for the main `Figure 5` results paragraph:

`Figure 5 should be read as processor-level boundary evidence rather than as the manuscript's main positive result. The current passive diffractive processor no longer lacks a reproducible baseline: the rebuilt NumPy protocol identifies a real and locally favorable common-path window. However, that gain remains weak and configuration-sensitive. In the restored baseline, the best common-path OOD mean PSNR is effectively tied with the best ordinary D2NN, while the strongest matched common-path advantage is limited to a local comparison against the non-common-path control and does not establish a robust ordinary-beating result. Figure 5 therefore serves one specific argument role: it shows that processor-level self-calibration is no longer missing from the paper, but it remains limit-setting evidence rather than a mature device-level demonstration.`

## Locked Discussion Boundary Paragraph

Use this as the default replacement for the main discussion paragraph that closes the evidence boundary:

`The manuscript's main boundary is now explicit. Figures 1--4 support the conditional-optics mechanism and its persistence under the present surrogate, wave-optics, and cross-task protocols. Figure 5, by contrast, does not support a strong processor-level superiority claim. The current gain is small, architecture-sensitive, and not yet stabilized as a repeatable advantage over the ordinary D2NN baseline. That limitation should remain visible rather than hidden, because it identifies the present frontier of the approach: adding a common-path pilot can expose useful state information, but this does not yet guarantee a robust processor-level win in a fixed passive diffractive implementation.`

## Locked Cover-Letter Core Paragraph

Use this as the default core paragraph in the submission cover letter:

`Our manuscript advances a mechanism-first contribution in diffractive optical computing: we show that a common-path optical pilot can encode information about the instantaneous degradation state and thereby improve downstream imaging recovery under dynamic aberrations. The strongest evidence comes from the wave-optics and task-level analyses, which remain consistently aligned with this bounded claim. We also retain a processor-level passive diffractive comparison, not as a mature device demonstration, but as transparent limit-setting evidence showing where the present implementation remains weak. We believe this evidence-bounded framing is important for the field because it distinguishes a real conditional-optics mechanism from an overstated device-level claim.`

## Locked Reviewer-Reply Core Paragraph

Use this when a reviewer questions why `Figure 5` is retained despite the weak processor-level gain:

`We agree that the current processor-level evidence is not strong enough to support a robust device-level superiority claim, and we have revised the manuscript accordingly. In the revised framing, Figure 5 is retained only as boundary evidence. Its role is to show that the processor-level comparison is no longer absent and that a reproducible common-path diagnostic window exists, while also making clear that the present passive implementation remains weak, configuration-sensitive, and not yet ordinary-beating. We chose to keep this result visible because the negative and near-neutral outcomes are scientifically informative for assessing what a fixed self-calibrating diffractive processor can and cannot currently support.`

## Locked Reviewer-Robustness Addendum

Use this when a reviewer asks whether the boundary chain depends on threshold choice or anchor selection:

`The Round18 boundary chain remains directionally stable under the Round19 audit: 0/4 alternate anchors changed the manuscript role, whereas the Round17 control-family step is fully stable for only 3/9 audited threshold pairs. We therefore keep the Round17 sentence conservative and write it as a failure to recover stable common-specificity under the current criterion rather than as an absolute impossibility claim.`

## Forbidden Claim Patterns

Do not use any of the following claim shapes in the manuscript or submission package:

- `robustly outperforms the ordinary D2NN`
- `demonstrates processor-level self-calibration`
- `establishes a mature passive optical solution`
- `confirms a clear device-level advantage`
- `validates deployment-ready self-calibrating diffractive imaging`

## Safe Claim Patterns

Prefer these claim shapes instead:

- `supports a bounded conditional-optics mechanism`
- `retains Figure 5 as boundary / limit-setting evidence`
- `identifies a reproducible baseline and a local common-path window`
- `does not yet establish a robust ordinary-beating processor-level result`
- `makes the present device-level limit explicit`
- `does not recover stable common-specificity under the current criterion`

## Naming Lock

Use the following terms consistently:

- `common-path pilot`
- `ordinary D2NN`
- `pilot-assisted D2NN`
- `processor-level boundary evidence`
- `mechanism-first framing`

Avoid switching mid-document to stronger or looser substitutes such as:

- `successful self-calibrating device`
- `hardware-level validation`
- `clear processor-level superiority`
