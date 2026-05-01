# Iteration 016 Natural-Object Step 2

- Timestamp: `2026-05-01T00:00:00Z`
- Action type: `strict_step2_natural_object_execution`
- Stage: `active calculation/verification`
- Single bottleneck addressed: `step 2 required a real natural-object execution attempt inside the project root`

## Executed action

1. Added `scripts/run_natural_object_evaluation.py`.
2. Bound the natural-object input expectation to the project-space staging root:
   - `data/natural_objects/imagenet-1k-ilsvrc2012-validation`
   - `data/natural_objects/coco-2017-validation`
3. Executed the script to audit whether the raw datasets required by `results/natural_objects/natural_object_subset_index.csv` were actually present.

## Interpretation boundary

This iteration does not count as natural-object evaluation success unless raw datasets are present and the script can proceed past input audit into metric generation. Under strict 1->2->3 ordering, step 3 must not start if this input audit fails.

## Verification result

- `scripts/run_natural_object_evaluation.py` executed and exited with blocker code `2`.
- The project-space staging root was checked at:
  - `/workspace/memory/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z/data/natural_objects`
- Expected dataset directories were created:
  - `data/natural_objects/imagenet-1k-ilsvrc2012-validation`
  - `data/natural_objects/coco-2017-validation`
- Missing required dataset roots:
  - `imagenet-1k-ilsvrc2012-validation`
  - `coco-2017-validation`
- Output files generated:
  - `results/natural_objects/natural_object_input_audit.json`
  - `results/natural_objects/natural_object_blocker_report.md`
- Direct external fetch attempts for both COCO and ImageNet were blocked by outbound `403` tunnel failures in the current container, so the missing raw images could not be populated automatically in this round.
