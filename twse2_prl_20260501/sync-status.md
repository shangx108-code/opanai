# Sync Status

Generated: `2026-05-02`
Project: `twse2_prl_20260501`
Canonical path: `/workspace/memory/twse2_prl_20260501`
Remote target: `shangx108-code/opanai`, branch `open-ai`

## Summary

- Local long-term project space updated: `yes`
- Latest local additions include kernel invariance tests and r_he-onset tracking results: `yes`
- GitHub connector write access in this retry: `working for text-file update`
- This audit file was updated through the GitHub connector after fetching the remote SHA.

## Latest scientific artifacts to sync/check

- `scripts/build_rhe_onset_kernel_tracking.py`
- `results/rhe_onset_kernel_tracking_2026-05-02/`
- `scripts/run_kernel_invariance_tests.py`
- `results/kernel_invariance_tests_2026-05-02/`
- updated `scripts/build_channel_resolved_multiorbital_btk.py`
- updated `README.md`
- updated `project-space-index.md`

## Current evidence status

- alpha-window origin: kernel-intrinsic after basis-rotation and interface-mixing invariance tests
- explicit alpha-weighting: removed from channel-selection construction
- r_he onset extraction: implemented as a kernel-internal AR-onset diagnostic
- Delta_in tracking from r_he onset: verified in the local result package

## Remaining sync note

This file confirms that connector-based writes can reach the remote branch. Large CSV/PNG result files should be pushed or updated file-by-file next, or by a normal git push from an environment with direct GitHub network access.
