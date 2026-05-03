# Round 2 local Figure 5 matched scan summary

Project: `self-calibrating-diffractive-optical-neural-operators-20260426-103458`
Date: 2026-05-03
Target: Figure 5 minimal local scan and manuscript closure.

## Purpose

Round 2 tested whether the current phase-only passive D2NN / common-path reference window can support Figure 5 as a positive main-result comparison for a Nature Communications manuscript.

## Canonical decision

The local matched scan did **not** support promoting Figure 5 into a positive main-result figure.

## Key quantitative records

- Best rebuilt ordinary OOD mean PSNR: `8.647 dB`
- Best rebuilt common-path OOD mean PSNR: `8.446 dB`
- Best rebuilt common minus ordinary: `-0.123 dB`
- Best-config repeat, common minus ordinary: `-0.087 ± 0.021 dB`
- Positive repeat seeds: `0 / 3`

## Interpretation

The result is not a near-positive result. Under the canonical-root rebuild, the common-path reference processor underperforms the ordinary D2NN baseline in this local scan window. This result should therefore be treated as a boundary/negative control unless a new processor-level design is introduced.

## Manuscript action taken

- Figure 5 language was tightened.
- The manuscript no longer frames this scan as evidence that the current phase-only passive processor is nearly successful.
- The result motivated the Round 3 downgrade decision.

## GitHub sync status

Prepared for GitHub sync after connector recovery. No leaked token was used.
