# Supplementary Failure Cases Under Object-Family Shift

This package documents representative cases in which the current phase-only stack falls below the fixed baseline under `new_family_heldout_object_family`.

## Main pattern

- `diag_x` is the most consistently negative held-out object family.
- `checker_blocks` is near the decision boundary but contains clear negative cases.
- `crescent` shows mixed behavior with a negative tail.
- `triangle` is comparatively stable and positive, so the failures are structure-dependent rather than uniformly distributed across the held-out ledger.

## Representative cases

### diag_x
- seed: `1`
- case_id: `14`
- aberration coefficients: defocus `-1.2102`, astig_x `0.8540`, coma_x `-0.2634`
- fixed low-resolution PSNR: `17.004 dB`
- phase-only low-resolution PSNR: `12.603 dB`
- phase-only gain over fixed: `-4.402 dB`
- interpretation: thin diagonal crossings concentrate oblique high-frequency content that is weakened by the 12x12 low-resolution frontend

### checker_blocks
- seed: `0`
- case_id: `8`
- aberration coefficients: defocus `-0.9192`, astig_x `-0.5008`, coma_x `-0.0087`
- fixed low-resolution PSNR: `18.801 dB`
- phase-only low-resolution PSNR: `16.451 dB`
- phase-only gain over fixed: `-2.350 dB`
- interpretation: periodic block structure creates alias-prone repeated edges and boundary leakage under object-family shift

### crescent
- seed: `0`
- case_id: `12`
- aberration coefficients: defocus `-1.3595`, astig_x `-0.0094`, coma_x `0.5558`
- fixed low-resolution PSNR: `18.598 dB`
- phase-only low-resolution PSNR: `16.134 dB`
- phase-only gain over fixed: `-2.463 dB`
- interpretation: curved asymmetric boundaries and hollow subtraction yield mixed low-contrast edge errors after the learned optical encoding

## Figure usage note

The panel image is intended as a supplementary figure candidate showing ground truth, aberrated input, fixed restoration, phase-only restoration, corresponding error maps, and the reference PSF for representative failure modes. It should be cited as evidence that the negative tail under `new_family_heldout_object_family` is structured and shape-dependent. It should not be cited as evidence that the phase-only frontend collapses uniformly across the entire object-family-shift ledger, because the aggregate mean gain on that ledger remains positive.

- panel: `results/failure_cases/object_shift_failure_cases_panel.png`
- table: `results/failure_cases/object_shift_failure_cases.csv`
