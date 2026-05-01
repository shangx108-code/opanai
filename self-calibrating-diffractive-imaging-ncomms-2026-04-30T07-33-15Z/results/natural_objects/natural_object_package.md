# Natural-Object Package

## Status

- Package type: `protocol scaffold plus proxy execution boundary note`
- Execution status: `licensed benchmark-root execution not yet run; project-local proxy execution completed`
- Reason: the active root still does not contain the licensed raw benchmark roots required for a finalized `ImageNet-1k` or `COCO` run.

## Frozen protocol

- Datasets selected for the first auditable natural-object pass:
  - `ImageNet-1k / ILSVRC2012 validation`
  - `COCO 2017 validation`
- Proposed subset size: `64 + 64` images.
- Shared preprocessing for all methods: center-crop to square, resize to `128 x 128`, convert to grayscale, normalize to `[0, 1]`, then downsample to the active `12 x 12` frontend.
- Shared fairness rule: every method must use the exact same frozen subset and preprocessing chain.

## Included file

- `natural_object_subset_index.csv` freezes dataset version, selection rule, preprocessing, and license handling.
- Executed proxy-result files now also exist in the active root:
  - `mixed_train_natural_object_summary.json`
  - `mixed_train_natural_object_thickstats_summary.json`
  - `natural_object_summary.json`

## Interpretation boundary

This package closes the audit gap around source specification, subset-selection rules, preprocessing, and license handling. It does not by itself certify finalized benchmark execution. The active root now contains executed project-local proxy natural-image stress tests, but those files must remain labeled as proxy evidence rather than official `ImageNet-1k` or `COCO` benchmark results.

## True blocker

- Missing licensed raw benchmark datasets in the active root.
- Therefore a finalized natural-image benchmark table tied to the frozen `ImageNet-1k` and `COCO` roots still cannot be claimed in this round, even though proxy stress-test metrics are available.
