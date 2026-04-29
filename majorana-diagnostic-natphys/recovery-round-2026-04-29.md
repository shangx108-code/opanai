# Recovery Round 2026-04-29

## Durable updates
- Confirmed blocker: the current scheduled-run workspace contains the Majorana project memory, but not the executable three-terminal benchmark scripts or the historical benchmark outputs needed for a real rerun. [active blocker]
- Recovered the three-terminal benchmark provenance into `/workspace/output/three-terminal-benchmark/RECOVERY_MANIFEST.md`. [verified]
- Recovered a machine-readable expected-asset list into `/workspace/output/three-terminal-benchmark/provenance_manifest.json`. [verified]
- Updated the project bottleneck from a generic "missing rerun" description to a concrete missing-bundle recovery state. [verified]
- Added a runnable recovery bootstrap at `/workspace/memory/majorana-diagnostic-natphys/code/majorana_recovery_bootstrap.py` that rebuilds the recovery folder and audits the scheduled-run environment. [verified]
- Re-ran the recovery bootstrap and regenerated `RECOVERY_MANIFEST.md`, `provenance_manifest.json`, `environment_audit.json`, and `missing_assets.json` in the current workspace. [verified]
- Confirmed that the current scheduled-run environment imports `numpy` and `pandas` but is missing `scipy` and `matplotlib`, so the benchmark rerun environment is still incomplete even before historical data restoration. [active blocker]
- Confirmed that no three-terminal benchmark entry script is present at the searched recovery paths and that all nine expected benchmark assets remain absent from the current workspace. [active blocker]

## Rejected from long-term state
- Any claim that the three-terminal numerical bundle itself has been regenerated. [unverified - do not commit]
- Any claim that `nu_ring` or `P_topo` were recomputed in this round. [unverified - do not commit]
- Any manuscript-strength interpretation upgrade based only on the recovered provenance files. [unverified - do not commit]
- Any claim that the environment is now fully ready for the three-terminal rerun. [unverified - do not commit]

## Current stable bottleneck
- The current workspace still lacks the shared three-terminal benchmark entry script and all historical bundle assets, and the scheduled-run Python environment is missing `scipy` and `matplotlib`, so the full-device topology rerun cannot yet start.

## Next durable action
- Restore the shared three-terminal benchmark script and historical bundle from persistent storage, then complete the missing scientific Python stack required by that script and start the matched transport-plus-topology rerun.
