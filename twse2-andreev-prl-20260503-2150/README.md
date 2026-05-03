# twse2-andreev-prl-20260503-2150

Canonical project root for the PRL-oriented twisted bilayer WSe2 theory project:

**Phase-sensitive Andreev fingerprints of unconventional pairing in twisted bilayer WSe2**

## Target venue

- Physical Review Letters (PRL)

## Project goal

- Build a two-valley moire BdG plus generalized BTK theory workflow for twisted bilayer WSe2.
- Separate the inner superconducting gap from the outer correlated feature.
- Use interface-orientation, intervalley-mixing, barrier, and in-plane-field selection rules to exclude ordinary same-sign s-wave pairing.

## Current bootstrap scope

- `user-materials/`: source planning notes supplied for project intake
- `src/`: minimal model helpers for WP1 and WP2
- `scripts/run_wp1_wp2.py`: first executable screening pass
- `configs/default_params.json`: shared model parameters
- `results/`: generated bootstrap outputs
- `manuscript/`: manuscript-facing text and future LaTeX assets
- `archive/`, `indexes/`, `logs/`: project tracking and traceability

## Quick start

```bash
cd /workspace/memory/projects/twse2-andreev-prl-20260503-2150
python scripts/run_wp1_wp2.py
```

## Bootstrap status

- Project root initialized on 2026-05-03 21:50 Asia/Shanghai.
- First environment target is a minimum runnable WP1-WP2 engine rather than a final publication-grade BTK solver.
- The next advancing action is to harden the generalized BTK layer on top of this scaffold.
