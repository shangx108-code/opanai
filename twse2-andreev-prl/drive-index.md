# Drive Index

Last updated: 2026-04-29

## Google Drive status

- Google account identity check: passed
  - account: `Xin Shang <shangx108@gmail.com>`
- Google Drive read-side connectivity: restored
  - profile lookup works
  - search queries run successfully
  - metadata reads are available
- Google Drive project search:
  - query `twse2 andreev prl`: no existing project file found
  - query `ws2 tuo andreev`: no existing project file found
- Current write-side limitation:
  - this session exposes account lookup, search, and metadata reads
  - it still does not expose a generic binary upload / folder-placement path for the current CSV + PNG + Python artifact bundle
  - consequence: this round cannot honestly mark the project artifacts as already uploaded into a stable Drive folder

## Current source availability

- The original workbook and archive were available in earlier workspace states.
- Track 1 remains runnable even when those temporary paths disappear because the source-band mirror is preserved in:
  - `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/band_comparison.csv`

## Persistent local project-space packages

| Package path | Purpose | Status | Google Drive status |
| --- | --- | --- | --- |
| `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/` | baseline Track-1 faithful candidate bundle | persistent local mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-ab-scan/` | `A-B` convention exclusion dataset | persistent local mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-kpath-scan/` | `k`-path mapping exclusion / candidate dataset | persistent local mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-kpath-best/` | best exact-`Gamma` path-mapping candidate package | persistent local mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-mixed-star-scan/` | shared mixed-star exclusion / candidate dataset | persistent local mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-asymmetric-short-range/` | isolated short-range asymmetry exclusion dataset | persistent local mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-asymmetric-c7/` | isolated `sqrt(7)` asymmetry exclusion dataset | persistent local mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29-coupled-path-c7/` | coupled path-plus-hopping best-faithful dataset | persistent local mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/data/track1-kclosure-2026-04-29/` | persistent Track-1 convention scan | persistent local mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/data/sgf-minimal-2026-04-29/` | SGF minimal edge-spectrum proxy package | persistent local mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/data/btk-minimal-2026-04-29/` | BTK / robustness minimal proxy package | persistent local mirror | pending sync |

## Persistent local code packages

| Code path | Purpose | Google Drive status |
| --- | --- | --- |
| `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-28-kpath/` | path-mapping scan code mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-29-asymmetry/` | asymmetric and coupled Track-1 scan code mirror | pending sync |
| `/workspace/memory/twse2-andreev-prl/code/twse2_persistent_pipeline.py` | persistent shared pipeline helpers | pending sync |
| `/workspace/memory/twse2-andreev-prl/code/run_track1_kclosure_scan.py` | persistent Track-1 convention scan entrypoint | pending sync |
| `/workspace/memory/twse2-andreev-prl/code/generate_sgf_minimal_package.py` | SGF minimal package generator | pending sync |
| `/workspace/memory/twse2-andreev-prl/code/generate_btk_minimal_package.py` | BTK minimal package generator | pending sync |

## Pending sync queue

1. Use a Drive session or connector surface that supports generic file upload and stable folder placement.
2. Locate or create the project folder for `twse2-andreev-prl`.
3. Upload the persistent Track-1 packages, including the new convention scan and the current coupled baseline package.
4. Upload the SGF minimal package.
5. Upload the BTK minimal package.
6. Upload the persistent code entrypoints used in the current project space.
7. Re-upload the original workbook and archive when a writable surface becomes available again.
8. Record Google Drive folder URL, file IDs, and version labels back into this index.
