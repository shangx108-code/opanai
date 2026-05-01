# Long-Term Project Space Index

Project: `twse2_prl_20260501`
Created: `2026-05-01T00:00:00Z`
Canonical project space: `/workspace/memory/twse2_prl_20260501`
Source snapshot copied from: `/workspace/twse2_prl_20260501`

## Purpose

This folder is the long-term project space for the current minimal tWSe2 PRL
engine. It captures the runnable WP1-WP2 scaffold from the workspace in one
stable repository location.

## Current contents

- runnable source code for the minimal model
- shared parameter configuration
- generated WP1 and WP2 result files
- a first WP3 conductance-proxy follow-up for candidate-resolved observable screening
- a PRL-style manuscript draft derived from the current minimal outputs
- top-level README for rerunning the scaffold

## Working rule

From this point onward, new project data for this chat should be saved here
first, then mirrored elsewhere only when needed.

All future data, scripts, results, notes, manuscript files, and other project
artifacts generated in this chat must be synchronized into this directory as
the canonical GitHub-backed long-term project space.

All substantive project data updates in this directory should also be committed
and pushed to the attached GitHub remote, so later sessions can inspect the
latest available files directly from the long-term project space.

The file `sync-status.md` should be refreshed after each substantive turn by
running `python scripts/update_sync_status.py`, so this project always carries a
local audit of its GitHub sync state.
