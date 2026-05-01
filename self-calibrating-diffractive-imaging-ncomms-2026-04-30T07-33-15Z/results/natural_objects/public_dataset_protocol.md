# Public Natural-Object Protocol

This protocol replaces the unavailable benchmark-root ImageNet/COCO branch with a directly staged public subset that can be re-downloaded from stable GitHub raw URLs.

## Datasets

- `Kodak-PCD0992 / unrestricted public release`
  - subset size: `12`
  - source repository: `https://github.com/girfa/ColorImageDatasets`
  - source subdirectory: `Kodak-PCD0992`
  - selection rule: Freeze kodim01.png through kodim12.png from the public Kodak-PCD0992 release mirrored in girfa/ColorImageDatasets.
  - preprocessing: center-crop to square, resize to 128x128, convert to grayscale, normalize to [0,1], then downsample to the active 12x12 frontend for all methods.
  - license note: The Kodak-PCD0992 dataset is described in the mirrored repository README as an unrestricted Kodak release.
- `UCID / 1338 public citation subset`
  - subset size: `12`
  - source repository: `https://github.com/girfa/ColorImageDatasets`
  - source subdirectory: `UCID-1338`
  - selection rule: Freeze numeric files 1.tif through 12.tif from the public UCID mirror in girfa/ColorImageDatasets.
  - preprocessing: center-crop to square, resize to 128x128, convert to grayscale, normalize to [0,1], then downsample to the active 12x12 frontend for all methods.
  - license note: Use the mirrored UCID subset with citation back to Schaefer and Stich, Proc. SPIE 5307 (2003), as documented in the repository README.

## Traceability

- Every staged file is listed with source URL, local path, byte size, and SHA-256 digest in `public_dataset_download_manifest.csv`.
- The frozen subset definition is recorded in `natural_object_subset_index.csv`.
- These files are public-open-data subsets, not ImageNet/COCO replacements.
