# Drive Index

Last updated: 2026-04-28

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
  - this session exposes account lookup and search, but it still does not expose a generic binary upload / folder-placement path for the current CSV + PNG + Python artifact bundle
  - consequence: this round cannot honestly mark the Track-1, `k`-path, or mixed-star artifacts as already uploaded into a stable project folder

## Current workspace source availability check

- The originally cited source bundle paths are absent in the current 2026-04-28 UTC workspace snapshot.
- Track-1 computation remains runnable because the source-band columns are mirrored in:
  - `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/band_comparison.csv`
- The restored main workspace script is:
  - `/workspace/twse2_tb/reconstruct_tuo_tb.py`
- The current mixed-star scan entrypoint is:
  - `/workspace/twse2_tb/scan_mixed_star_gauges.py`
- Consequence:
  - Track 1 can continue locally and honestly
  - the original workbook and archive still need to be re-synced later when a generic upload surface is available

## Current local data artifacts ready for cloud sync

| Local path | Content type | Purpose | Version status | Google Drive status |
| --- | --- | --- | --- | --- |
| `/workspace/output/twse2_tb_reconstruction/reconstructed_hopping_table.csv` | table | current reconstructed hopping export | working candidate | pending sync |
| `/workspace/output/twse2_tb_reconstruction/band_comparison.csv` | table | current reconstructed band comparison | working candidate | pending sync |
| `/workspace/output/twse2_tb_reconstruction/high_symmetry_residuals.csv` | table | current residual audit | working candidate | pending sync |
| `/workspace/output/twse2_tb_reconstruction/band_reconstruction_check.png` | figure | current reconstruction figure | working candidate | pending sync |
| `/workspace/output/twse2_tb_reconstruction/summary.md` | summary | current reconstruction summary | working candidate | pending sync |
| `/workspace/output/twse2_ab_scan/ab_convention_scan.csv` | table | 162-candidate `A-B` convention ledger | exclusion dataset | pending sync |
| `/workspace/output/twse2_ab_scan/ab_convention_scan_top20.csv` | table | ranked top-20 `A-B` candidates | exclusion dataset | pending sync |
| `/workspace/output/twse2_ab_scan/best_exact_gamma_band_comparison.csv` | table | best exact-`Gamma` `A-B` comparison | exclusion dataset | pending sync |
| `/workspace/output/twse2_ab_scan/best_exact_gamma_band_check.png` | figure | best exact-`Gamma` `A-B` figure | exclusion dataset | pending sync |
| `/workspace/output/twse2_ab_scan/summary.md` | summary | `A-B` scan summary | exclusion dataset | pending sync |
| `/workspace/output/twse2_k_path_scan/k_path_mapping_scan.csv` | table | 180-candidate `k`-path mapping ledger | exclusion dataset | pending sync |
| `/workspace/output/twse2_k_path_scan/k_path_mapping_scan_top20.csv` | table | ranked top-20 `k`-path candidates | exclusion dataset | pending sync |
| `/workspace/output/twse2_k_path_scan/summary.md` | summary | `k`-path scan summary | exclusion dataset | pending sync |
| `/workspace/output/twse2_k_path_scan/best_exact_gamma_candidate/reconstructed_hopping_table.csv` | table | best exact-`Gamma` path-mapping hopping export | improved main candidate | pending sync |
| `/workspace/output/twse2_k_path_scan/best_exact_gamma_candidate/band_comparison.csv` | table | best exact-`Gamma` path-mapping band comparison | improved main candidate | pending sync |
| `/workspace/output/twse2_k_path_scan/best_exact_gamma_candidate/high_symmetry_residuals.csv` | table | best exact-`Gamma` path-mapping residual audit | improved main candidate | pending sync |
| `/workspace/output/twse2_k_path_scan/best_exact_gamma_candidate/band_reconstruction_check.png` | figure | best exact-`Gamma` path-mapping figure | improved main candidate | pending sync |
| `/workspace/output/twse2_k_path_scan/best_exact_gamma_candidate/summary.md` | summary | best exact-`Gamma` path-mapping summary | improved main candidate | pending sync |
| `/workspace/output/twse2_mixed_star_scan/mixed_star_scan.csv` | table | 162-candidate non-`A-B` mixed-star ledger | exclusion dataset | pending sync |
| `/workspace/output/twse2_mixed_star_scan/mixed_star_scan_top20.csv` | table | ranked top-20 mixed-star candidates | exclusion dataset | pending sync |
| `/workspace/output/twse2_mixed_star_scan/summary.md` | summary | mixed-star scan summary | exclusion dataset | pending sync |
| `/workspace/output/twse2_mixed_star_scan/best_exact_gamma_candidate/reconstructed_hopping_table.csv` | table | best exact-`Gamma` mixed-star hopping export | improved main candidate | pending sync |
| `/workspace/output/twse2_mixed_star_scan/best_exact_gamma_candidate/band_comparison.csv` | table | best exact-`Gamma` mixed-star band comparison | improved main candidate | pending sync |
| `/workspace/output/twse2_mixed_star_scan/best_exact_gamma_candidate/high_symmetry_residuals.csv` | table | best exact-`Gamma` mixed-star residual audit | improved main candidate | pending sync |
| `/workspace/output/twse2_mixed_star_scan/best_exact_gamma_candidate/band_reconstruction_check.png` | figure | best exact-`Gamma` mixed-star figure | improved main candidate | pending sync |
| `/workspace/output/twse2_mixed_star_scan/best_exact_gamma_candidate/summary.md` | summary | best exact-`Gamma` mixed-star summary | improved main candidate | pending sync |
| `/workspace/twse2_tb/reconstruct_tuo_tb.py` | code | restored Track-1 reconstruction script with workbook fallback | working main script | pending sync |
| `/workspace/twse2_tb/scan_k_path_mappings.py` | code | reproducible `k`-path mapping scan script | exclusion script | pending sync |
| `/workspace/twse2_tb/scan_mixed_star_gauges.py` | code | reproducible mixed-star scan script on top of the best `k`-path baseline | exclusion script | pending sync |

## Memory-folder mirror

- Persistent local mirror: `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-29/`
  - `reconstructed_hopping_table.csv`
  - `band_comparison.csv`
  - `high_symmetry_residuals.csv`
  - `band_reconstruction_check.png`
  - `summary.md`
- Persistent local mirror: `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-ab-scan/`
  - `ab_convention_scan.csv`
  - `ab_convention_scan_top20.csv`
  - `best_exact_gamma_band_comparison.csv`
  - `best_exact_gamma_band_check.png`
  - `summary.md`
- Persistent local mirror: `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-kpath-scan/`
  - `k_path_mapping_scan.csv`
  - `k_path_mapping_scan_top20.csv`
  - `summary.md`
- Persistent local mirror: `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-kpath-best/`
  - `reconstructed_hopping_table.csv`
  - `band_comparison.csv`
  - `high_symmetry_residuals.csv`
  - `band_reconstruction_check.png`
  - `summary.md`
- Persistent local mirror: `/workspace/memory/twse2-andreev-prl/data/track1-2026-04-28-mixed-star-scan/`
  - `mixed_star_scan.csv`
  - `mixed_star_scan_top20.csv`
  - `summary.md`
  - `reconstructed_hopping_table.csv`
  - `band_comparison.csv`
  - `high_symmetry_residuals.csv`
  - `band_reconstruction_check.png`
  - `best_exact_gamma_summary.md`
- Persistent local code mirror: `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-28-kpath/`
  - `reconstruct_tuo_tb.py`
  - `scan_k_path_mappings.py`
- Persistent local code mirror: `/workspace/memory/twse2-andreev-prl/code/track1-2026-04-28-mixed-star/`
  - `reconstruct_tuo_tb.py`
  - `scan_mixed_star_gauges.py`

## Pending sync queue

1. Use a Drive session or connector surface that supports generic file upload and stable folder placement.
2. Locate or create the project folder for `twse2-andreev-prl`.
3. Upload the current Track-1 reconstruction artifacts.
4. Upload the `A-B` convention scan artifacts.
5. Upload the `k`-path mapping scan artifacts and the improved best-candidate package.
6. Upload the mixed-star scan artifacts and the improved best-candidate package.
7. Upload the restored Track-1 scripts, including the new mixed-star scan entrypoint.
8. Re-upload the original workbook and archive when they become available again.
9. Record Google Drive folder URL, file IDs, and version labels back into this index.
