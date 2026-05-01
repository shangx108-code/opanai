# Phase-sensitive Andreev fingerprints of unconventional pairing in twisted bilayer WSe2

Created: 2026-04-30 09:10:02 CST

This directory is the long-term project space for the PRL-oriented theory project on phase-sensitive Andreev diagnostics in twisted bilayer WSe2.

## Goal

Build a reproducible theory and computation workflow that can support the paper claim:

1. Andreev conductance selectively tracks the inner superconducting gap.
2. Ordinary same-sign s-wave cannot simultaneously satisfy the joint constraints from interface orientation, barrier transparency, intervalley mixing, and in-plane-field response.
3. The surviving pairing family is unconventional, with the first paper stopping at "beyond ordinary s-wave" unless stronger evidence is produced.

## Current structure

- `inputs/`: user-provided planning materials and source notes
- `config/`: project configuration and parameter presets
- `scripts/`: runnable theory and numerical scaffolds
- `results/`: generated tables and machine-readable outputs
- `logs/`: iteration logs and run notes
- `indexes/`: space manifest and archival pointers
- `notes/`: project notes that are not yet manuscript-ready
- `manuscript/`: paper-facing drafts and section assets

## First-round status

The project has been formally initialized. A minimal executable BdG scaffold is included and has been run once to produce a first machine-readable summary of candidate pairing states and gap statistics.
