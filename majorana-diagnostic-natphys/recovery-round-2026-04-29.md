# Recovery Round 2026-04-29

## Durable updates
- Confirmed blocker: the current scheduled-run workspace contains the Majorana project memory, but not the executable three-terminal benchmark scripts or the historical benchmark outputs needed for a real rerun. [active blocker]
- Recovered the three-terminal benchmark provenance into `/workspace/output/three-terminal-benchmark/RECOVERY_MANIFEST.md`. [verified]
- Recovered a machine-readable expected-asset list into `/workspace/output/three-terminal-benchmark/provenance_manifest.json`. [verified]
- Updated the project bottleneck from a generic "missing rerun" description to a concrete missing-bundle recovery state. [verified]

## Rejected from long-term state
- Any claim that the three-terminal numerical bundle itself has been regenerated. [unverified - do not commit]
- Any claim that `nu_ring` or `P_topo` were recomputed in this round. [unverified - do not commit]
- Any manuscript-strength interpretation upgrade based only on the recovered provenance files. [unverified - do not commit]

## Current stable bottleneck
- The shared three-terminal benchmark script path and historical bundle files are absent from the current workspace, so the full-device topology rerun cannot yet start.

## Next durable action
- Restore the shared three-terminal benchmark script and input/output bundle from persistent storage, then rerun the matched transport-plus-topology benchmark.
