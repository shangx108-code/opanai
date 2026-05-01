# Figure Captions

## Main Figure Candidate 1. Dual-ledger benchmark overview

Performance of the four compared methods under the pre-registered dual-ledger protocol. The benchmark separates `same_family_heldout_aberration` from `new_family_heldout_object_family` and aggregates results across 10 seeds. `phase_only_stack` achieves the largest overall mean PSNR gain over the fixed baseline (`4.057 dB`, 95% CI `3.931-4.183`), but the ledger breakdown remains asymmetric: the gain is large for held-out aberrations (`7.593 dB`) and modest for held-out object-family shift (`0.521 dB`). This figure should therefore be cited as evidence for the best average dual-ledger trade-off, not as evidence that the phase-only frontend dominates every regime or eliminates object-family-shift difficulty.

## Main Figure Candidate 2. Proxy natural-image stress-test transfer

Proxy natural-image stress tests using project-local subsets matched to the frozen `ImageNet-1k` and `COCO` protocols. These panels must be labeled explicitly as proxy natural-image results and not as official `ImageNet-1k` or `COCO` benchmark evaluations. Under synthetic-only training, the pipeline becomes strongly negative on both proxy datasets (`-10.3924 dB` on `ImageNet-1k` proxy images and `-12.8547 dB` on `COCO` proxy images). After mixed training with proxy natural images, the mean gain becomes positive and remains positive after thickened validation (`+0.9841 +/- 0.2501 dB` on `ImageNet-1k` proxy images and `+1.4520 +/- 0.1370 dB` on `COCO` proxy images; 95% CI half-width). The intended interpretation is that training-distribution mismatch is a dominant source of the initial failure.

## Main Figure Candidate 3. Tolerance under common perturbations and mask-specific perturbations

First-order simulated tolerance diagnosis of the mixed-training phase-only frontend under common perturbations and phase-mask-specific perturbations. Under common perturbations, including mild reference-channel intensity noise and propagation-distance error within +/-5%, the recovered proxy-natural gain remains positive on both datasets. By contrast, the initial model is highly sensitive to mask-specific engineering errors: `1 px` and `2 px` lateral shift, as well as `3`-bit and `4`-bit phase quantization, drive the mean PSNR gain strongly negative. This figure should be used to distinguish reviewer-relevant shared robustness from phase-mask fabrication and alignment sensitivity, not as evidence of broad hardware robustness.

## Main Figure Candidate 4. Robust-mask mitigation

Effect of robust-mask training on the dominant engineering failure modes. Training with in-loop exposure to unperturbed masks, `4`-bit quantization, `3`-bit quantization, and `1 px` lateral shift improves clean-reference performance and converts the first-order `1 px` shift and `3/4`-bit quantization cases from strongly negative to positive-gain regimes. However, `2 px` lateral shift remains strongly negative on both proxy-natural datasets. The caption should therefore emphasize partial repair in a first-order simulated tolerance diagnosis rather than broad hardware robustness.
