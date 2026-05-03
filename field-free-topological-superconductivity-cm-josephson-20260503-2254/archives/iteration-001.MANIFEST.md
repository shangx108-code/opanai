# iteration-001 archive manifest

Project: field-free-topological-superconductivity-cm-josephson-20260503-2254
Archive: iteration-001.zip
Iteration label: iteration-001
Created: 2026-05-04
Purpose: First executable minimal BdG phase scan archive for later manuscript synthesis and project review.

## Contents

- DATA_INDEX.md
- results/minimal-bdg-phase-scan-20260503/minimal_gap_scan.csv
- results/minimal-bdg-phase-scan-20260503/near_closing_points.csv
- results/minimal-bdg-phase-scan-20260503/summary.md
- scripts/run_minimal_bdg_phase_scan.py

## Checks

- ZIP bytes: 15675
- ZIP SHA256: fa07487389beb1f14cb78d0422aa959e86a8b9d0a40eac8ac7a9859ae82207ac
- Base64 sidecar lines: 275

## Restore from GitHub base64 sidecar

Run from the archive directory:

```bash
base64 -d iteration-001.zip.base64 > iteration-001.zip
sha256sum iteration-001.zip
```

The restored hash should match the ZIP SHA256 above.

## Scientific status

This archive captures the first complete executable scan. It confirms that the current minimal two-channel compensated-magnetic Josephson model runs reproducibly but does not yet isolate a convincing topological window. The next iteration should revise the model toward a more faithful planar Josephson geometry before transport claims are developed.
