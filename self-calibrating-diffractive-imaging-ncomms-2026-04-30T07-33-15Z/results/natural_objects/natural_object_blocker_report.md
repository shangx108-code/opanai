# Natural-Object Evaluation Status Note

## Status

- Execution attempted: `yes`
- Execution completed: `yes`
- Active data route: `public-open-data Kodak/UCID subset`

## Resolution

The earlier benchmark-root ImageNet/COCO blocker is no longer the active natural-image execution path in this project root. The natural-image branch now uses staged public-open-data subsets:

- `Kodak-PCD0992 / unrestricted public release`
- `UCID / 1338 public citation subset`

Both subsets are frozen in `results/natural_objects/natural_object_subset_index.csv` and traced file-by-file in `results/natural_objects/public_dataset_download_manifest.csv`.

## Interpretation boundary

These runs are real public-data evaluations, not benchmark-root ImageNet/COCO evaluations. Manuscript language should therefore name the Kodak/UCID public protocol explicitly and avoid implying benchmark-root ImageNet/COCO validation.
