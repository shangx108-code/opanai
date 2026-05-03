# Iteration 002 Data Package

Package name: `iteration-002.zip`
Project: `twse2-andreev-prl-20260503-2150`
Purpose: current generated data package for later manuscript-level synthesis and reproducibility review.

Included top-level directories:
- `configs/`
- `indexes/`
- `logs/`
- `results/`
- `scripts/`

Key dense data included:
- `results/generalized_btk_phase_scan/conductance_curves.csv`
- `results/generalized_btk_phase_scan/phase_scan_summary.csv`
- `results/generalized_btk_phase_scan/compact_reference_curves.csv`

Package status:
- Full local zip exists at the canonical local project space:
  - `/mnt/data/twse2-andreev-prl-20260503-2150/archive/iteration-packages/iteration-002.zip`
- Full local zip size: `13,423,776` bytes compressed.
- Full local uncompressed payload includes dense `conductance_curves.csv` with `152,934,403` bytes.
- SHA256: `5d10a5695485c2558f9e8116137cad8efb56a726048a03b8570363ceed2c9356`

GitHub sync status:
- This summary, manifest, and SHA256 are mirrored to GitHub for future manuscript-level lookup.
- The full binary `.zip` could not be uploaded directly through the available GitHub connector in this session because the exposed write path only supports UTF-8 text file creation/update.
- GitHub-friendly compact data remain mirrored under `results/generalized_btk_phase_scan/github_mirror/`.

Notes:
- This package includes the dense local conductance grid for future paper synthesis.
- For GitHub review, use the manifest plus compact mirror files; for full numerical reproduction, use the local `iteration-002.zip` package.
