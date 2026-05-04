# Iteration Log

## 2026-05-03 22:54 Asia/Shanghai

- Intake source reviewed and project identity locked.
- Unified project identifier created:
  - `field-free-topological-superconductivity-cm-josephson-20260503-2254`
- Local project workspace initialized with:
  - archive ledgers
  - manuscript skeleton
  - environment bootstrap scripts
  - environment check script
- Base environment check completed:
  - available: `numpy 2.3.5`, `pandas 2.2.3`
  - missing in current base runtime: `scipy`, `matplotlib`, `kwant`, `tinyarray`
- GitHub writeback target designated:
  - repository: `shangx108-code/opanai`
  - branch: `open-ai`
- Next action fixed:
  - write project skeleton to GitHub and start minimal model implementation inside this project root

## 2026-05-04 09:34 Asia/Shanghai

- Continued from the third selective weak-link branch with one narrower task only:
  - add a harder channel/orbital filter to cut the residual low-gap manifold
- Implemented new round-four script:
  - `scripts/run_channel_filtered_round4_scan.py`
- Model revisions in this round:
  - explicit orbital detuning split between the two junction rows
  - hard row-resolved channel filter that strongly down-weights the second junction row
  - narrower in-junction bandwidth and weaker interface transmission
  - sharper compensated-magnetic form factor on the active row
- Executed the coarse scan on the same `mu`, `phi`, and `M0` grid as the third run.
- Quantitative outcome:
  - total points: `936`
  - near-closing points with `min_gap < 5e-4`: `39`
  - third-scan baseline near-closing count: `125`
  - relative reduction: `68.8%`
  - near-closing `phi~pi` fraction: `0.154`
  - near-closing low-phase fraction: `0.231`
  - smallest gap: `0.000130` at `mu=2.000`, `M0=1.200`, `phi/pi=0.000`, `kx=-0.367`
- Main conclusion of this round:
  - clutter reduction is real and large
  - the residual low-gap manifold now collapses into three phi-flat families instead of a broad cloud
  - this is therefore a verified pruning success but not yet a phase-selective topological success
- Residual families recorded from the near-closing subset:
  - `(M0=0.4, mu=0.5)` across all sampled `phi`
  - `(M0=0.6, mu=1.0)` across all sampled `phi`
  - `(M0=1.2, mu=2.0)` across all sampled `phi`
- GitHub writeback completed in this round for:
  - `scripts/run_channel_filtered_round4_scan.py`
  - `results/channel-filtered-round4-scan-20260504/summary.md`
  - `results/channel-filtered-round4-scan-20260504/channel_filtered_round4_near_closing_points.csv`
- GitHub writeback still pending after this round for:
  - `results/channel-filtered-round4-scan-20260504/channel_filtered_round4_gap_scan.csv`
  - the three earlier full coarse scan CSV files from rounds one to three
- Next shortest action:
  - recover stronger phase sensitivity in the surviving active channel without reopening broad low-gap clutter
