# Project State

- Project ID: `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`
- Locked title: `Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations`
- Target journal: `Nature Communications`
- Stage: `active calculation/verification`
- First formal execution time: `2026-04-30T07-33-15Z`
- Authoritative concept source: `/workspace/user_files/01-1-.txt`

## Current single bottleneck

The project no longer lacks either an unmitigated, robust-mask, or second-generation linked tolerance result. The sharper bottleneck is now that neither the first-order robust-mask strategy nor a first-pass second-generation joint-perturbation training objective expands the linked pass region beyond the same clean `UCID` branch.

## Confirmed core story

1. A fixed passive diffractive optical processor co-propagates an object wave and a known reference wave, uses coherent interference to encode the instantaneous distortion state, and aims to restore images under dynamic aberrations without iterative adaptive optics.
2. Under the registered synthetic dual-ledger benchmark, `phase_only_stack` still provides the strongest overall average PSNR gain.
3. That benchmark advantage is carried mainly by held-out aberration generalization; held-out object-family shift remains much harder.
4. The public-data natural-image branch no longer rests on proxy placeholders. It now uses staged public subsets from `Kodak-PCD0992` and `UCID-1338`, with frozen file manifests and reproducibility hashes.

## New public-data execution results

- Synthetic-only public-data run:
  - `Kodak-PCD0992`: mean PSNR gain over fixed `-16.1404 dB`, better-than-fixed fraction `0.0`
  - `UCID`: mean PSNR gain over fixed `-12.1478 dB`, better-than-fixed fraction `0.0`
- Mixed-train public-data rerun:
  - `Kodak-PCD0992`: mean PSNR gain over fixed `-1.1311 dB`, better-than-fixed fraction `0.1111`
  - `UCID`: mean PSNR gain over fixed `+1.3828 dB`, better-than-fixed fraction `0.7917`
- Mixed-train public-data thickstats (`5` seeds, `12` held-out cases per seed):
  - `Kodak-PCD0992`: mean PSNR gain over fixed `-1.0544 ± 0.1434 dB` (95% CI half-width)
  - `UCID`: mean PSNR gain over fixed `+1.7261 ± 0.2319 dB` (95% CI half-width)

## Updated interpretation

- The old proxy-natural story of “positive gain on both datasets after mixed training” no longer survives contact with the public-data rerun.
- The new real-data interpretation is narrower:
  - mixed training materially reduces the natural-image failure
  - the recovery is dataset-dependent rather than universal
  - `UCID` becomes reproducibly positive
  - `Kodak-PCD0992` remains mildly negative even after mixed training
- Therefore the natural-image branch now supports a claim about training-distribution dependence and dataset heterogeneity, not a broad positive natural-image generalization claim.

## Tolerance and robustness results on the public-data branch

- In the mixed-train tolerance package, `phase_only_stack` remains positive on `UCID` under mild shared perturbations, but stays negative on `Kodak-PCD0992` even at clean reference and `±5%` propagation-distance error.
- `reference_psf_deconvolution` remains positive on both public datasets across the executed common perturbations.
- Phase-mask-specific perturbations remain the dominant engineering vulnerability:
  - `1 px` and `2 px` lateral shift are strongly negative on both datasets before mitigation
  - `3`-bit and `4`-bit quantization are also strongly negative on both datasets before mitigation
- Robust-mask training changes the picture asymmetrically:
  - `UCID` becomes strongly positive for clean reference, `1 px` shift, `3`-bit quantization, and `4`-bit quantization
  - `Kodak-PCD0992` improves dramatically relative to the unmitigated baseline, but remains slightly negative in clean reference and first-order perturbation cases
  - `2 px` lateral shift remains strongly negative on both datasets after mitigation

## New joint fabrication-tolerance execution results

- A linked three-factor scan is now executed in `results/tolerance_joint/` over:
  - phase-noise RMS: `0`, `0.05`, `0.10`, `0.20 rad`
  - layer misalignment levels:
    - clean: `0 px`, `0 deg`
    - mild: `0.25 px`, `0.5 deg`
    - moderate: `0.50 px`, `1.0 deg`
    - severe: `1.0 px`, `2.0 deg`
  - wavelength drift: `0`, `0.5%`, `1%`, `2%`
- `UCID` retains a positive gain-over-fixed region only for the clean-mask branch:
  - clean, `0%` drift: `+1.6409 ± 0.3407 dB`
  - clean, `0.5%` drift: `+1.6470 ± 0.3373 dB`
  - clean, `1.0%` drift: `+1.6454 ± 0.3354 dB`
  - clean, `2.0%` drift: `+1.6255 ± 0.3339 dB`
- `UCID` fails immediately once either fabrication-noise axis becomes nonzero in the current unmitigated stack:
  - phase noise only, `0.05 rad`: `-3.6303 ± 1.4411 dB`
  - mild misalignment only, `0.25 px / 0.5 deg`: `-7.5949 ± 0.4896 dB`
- `Kodak-PCD0992` has no passing region even at the clean point:
  - clean, `0%` drift: `-1.1084 ± 0.1963 dB`
- The dominant fragility is therefore fabrication-style phase/mask error, not wavelength drift.

## New robust-mask joint tolerance results

- A matched robust-mask version of the same linked three-factor scan now exists in `results/tolerance_joint_robust/`.
- The clean branch improves, but the pass region does not expand:
  - `UCID`, clean, `0%` drift: from `+1.6409 ± 0.3407 dB` to `+2.5993 ± 0.0812 dB`
  - `UCID`, clean, `2%` drift: from `+1.6255 ± 0.3339 dB` to `+2.5192 ± 0.1570 dB`
  - `Kodak-PCD0992`, clean, `0%` drift: from `-1.1084 ± 0.1963 dB` to `-0.2182 ± 0.0935 dB`, still below zero
- The same previously failing linked perturbation branches remain failing after robust-mask training:
  - `UCID`, phase noise only `0.05 rad`: `-4.3309 ± 1.7409 dB`
  - `UCID`, mild misalignment only `0.25 px / 0.5 deg`: `-7.4303 ± 0.5466 dB`
- Therefore the present robust-mask strategy improves clean-headroom and single-factor first-order cases, but does not open a broader linked fabrication-tolerance window.

## New second-generation joint-training results

- A first-pass second-generation training objective now exists in `results/tolerance_joint_secondgen/`.
- This objective injects linked perturbation variants during training itself rather than only first-order quantization and `1 px` shift exposure:
  - clean
  - joint mild: `0.05 rad`, `0.25 px`, `0.5 deg`, `0.5%`
  - joint moderate: `0.10 rad`, `0.50 px`, `1.0 deg`, `1.0%`
- The result does not widen the linked pass region:
  - `UCID`, clean, `0%` drift: `+2.3951 ± 0.2853 dB`
  - `UCID`, clean, `2%` drift: `+2.3037 ± 0.3357 dB`
  - `UCID`, phase noise only `0.05 rad`: `-4.7289 ± 1.9562 dB`
  - `UCID`, mild misalignment only `0.25 px / 0.5 deg`: `-8.3056 ± 2.1266 dB`
  - `Kodak-PCD0992`, clean, `0%` drift: `-0.4409 ± 0.1989 dB`
- Relative to the first robust-mask strategy, the second-generation objective remains positive on the same clean `UCID` branch but does not expand the pass set and underperforms the robust-mask clean point.

## Active manuscript-safe claim boundary

- Safe:
  - the hybrid diffractive frontend provides the best average trade-off in the registered synthetic dual-ledger benchmark
  - mixed training substantially reduces the natural-image transfer failure on real public data
  - public natural-image performance is strongly dataset-dependent
  - robust-mask training repairs first-order perturbation failures on `UCID` and sharply reduces them on `Kodak-PCD0992`, but does not establish broad hardware robustness
  - in the unmitigated stack, wavelength drift up to `2%` is comparatively mild when the hardware is otherwise clean, whereas phase noise and layer misalignment dominate the failure boundary
  - the robust-mask variant increases clean-branch margin on `UCID` and narrows the clean-point deficit on `Kodak-PCD0992`, but still does not expand the linked pass region beyond the clean `UCID` branch
  - the current second-generation joint-perturbation training objective is a valid negative result: it preserves only the same clean `UCID` pass branch and does not currently outperform the simpler robust-mask strategy on the linked boundary metric
- Unsafe:
  - claiming benchmark-root ImageNet/COCO validation
  - claiming broadly positive natural-image generalization across public datasets
  - claiming hardware robustness beyond first-order simulated perturbation repair
  - claiming a broad positive fabrication-tolerance window for the unmitigated phase-only stack
  - claiming that the current robust-mask strategy has solved linked fabrication tolerance
  - claiming that the present second-generation training objective has opened a broader fabrication-tolerance safety window

## Public-data protocol status

- Active natural-image protocol:
  - `Kodak-PCD0992 / unrestricted public release`
  - `UCID / 1338 public citation subset`
- Frozen subset size:
  - `12 + 12` images
- Traceability files:
  - `results/natural_objects/public_dataset_download_manifest.csv`
  - `results/natural_objects/public_dataset_download_manifest.json`
  - `results/natural_objects/public_dataset_protocol.md`
  - `archive/reproducibility_manifest.json`

## Automation

- Hourly iteration schedule: enabled
- Schedule timezone: `Asia/Shanghai`
- Stop condition: the manuscript, source-data package, and long-term GitHub project space all reflect the public-data recomputation and updated claim boundary.
