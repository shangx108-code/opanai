# Natural-Object Package

## Status

- Package type: `public-open-data execution package`
- Execution status: `ready for rerun on staged public Kodak and UCID subsets`
- Reason: benchmark-root ImageNet/COCO files were unavailable, so this branch now uses directly staged public datasets with frozen manifests.

## Frozen protocol

- Datasets selected for the auditable natural-object pass:
  - `Kodak-PCD0992 / unrestricted public release`
  - `UCID / 1338 public citation subset`
- Proposed subset size: `12 + 12` images.
- Shared preprocessing for all methods: center-crop to square, resize to `128 x 128`, convert to grayscale, normalize to `[0, 1]`, then downsample to the active `12 x 12` frontend.
- Shared fairness rule: every method must use the exact same frozen subset and preprocessing chain.

## Included files

- `natural_object_subset_index.csv` freezes dataset version, selection rule, preprocessing, and provenance handling.
- `public_dataset_download_manifest.csv` lists the exact downloaded raw files and digests.
- `public_dataset_protocol.md` records the public-data substitution boundary and traceability notes.

## Interpretation boundary

This package upgrades the natural-image branch from proxy-only placeholders to real public-open-data evaluation. It still does not justify claims about benchmark-root ImageNet/COCO performance, and the manuscript should name the Kodak/UCID protocol explicitly.

## Previous blocker status

- The old ImageNet/COCO benchmark-root blocker remains historically true but is no longer the active natural-image execution path in this project root.
