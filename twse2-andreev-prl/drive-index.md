# Drive Index

Last updated: 2026-04-29

## Google Drive status

- Google account identity check: passed
  - account: `Xin Shang <shangx108@gmail.com>`
- Google Drive file discovery / search: blocked
  - observed error: `ACCESS_TOKEN_SCOPE_INSUFFICIENT`
  - consequence: this round cannot honestly mark project data as already indexed or synced to Google Drive
  - required follow-up: re-authenticate / extend connector scopes before the next cloud-sync attempt

## Current local source bundle

- `/workspace/user_files/04-ws2.zip`
- `/workspace/tmp/ws2/s41467-025-64519-3.pdf`
- `/workspace/tmp/ws2/41467_2025_64519_MOESM1_ESM.pdf`
- `/workspace/tmp/ws2/41467_2025_64519_MOESM3_ESM.xlsx`

## Current local data artifacts ready for cloud sync

| Local path | Content type | Purpose | Version status | Google Drive status |
| --- | --- | --- | --- | --- |
| `/workspace/output/twse2_tb_reconstruction/reconstructed_hopping_table.csv` | table | current symmetry-completed hopping candidate | working main candidate | pending sync |
| `/workspace/output/twse2_tb_reconstruction/band_comparison.csv` | table | full k-path source vs reconstructed band comparison | working main candidate | pending sync |
| `/workspace/output/twse2_tb_reconstruction/high_symmetry_residuals.csv` | table | `Gamma / K^B / M / K^T` residual audit | working main candidate | pending sync |
| `/workspace/output/twse2_tb_reconstruction/band_reconstruction_check.png` | figure | visual band check against source arrays | working main candidate | pending sync |
| `/workspace/output/twse2_tb_reconstruction/summary.md` | summary | metric summary and honesty statement for the current candidate | working main candidate | pending sync |
| `/workspace/twse2_tb/reconstruct_tuo_tb.py` | code | reproducible Track-1 reconstruction script | working main script | pending sync |

## Pending sync queue

1. Recover Google Drive write/search scope.
2. Locate or create the project folder for `twse2-andreev-prl`.
3. Upload the Track-1 data artifacts listed above.
4. Record Google Drive folder URL, file IDs, and version labels back into this index.
