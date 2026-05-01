# Iteration Log

## 2026-04-30T07:30:00Z

- Reconfirmed the canonical project identity as the PRL-oriented twisted bilayer WSe2 Andreev manuscript.
- Locked the long-term project slug to `twse2-andreev-prl-2026-04-29T13-43-41Z` using the inherited first-start timestamp.
- Added a reproducible environment bootstrap script, requirements file, and hourly iteration driver inside the long-term root.
- Created the canonical GitHub project root under `shangx108-code/opanai` on branch `open-ai`.
- Verified that the local hourly driver returns `ready_for_hourly_iteration: true`.
- Disabled the older overlapping two-hour schedule and kept only the new hourly schedule active.
- Reset the orchestration rule so hourly iterations stop only after five reviewer-style acceptance estimates all exceed 80 percent and the evidence chain is complete.

## 2026-04-30T08:00:00Z

- Audited the current semi-infinite-informed BTK package against the PRL claim boundary.
- Confirmed from the active kernel implementation that the present BTK engine is still a scalar proxy rather than a channel-resolved multiorbital scattering calculation.
- Closed the adequacy question with a negative result: the current BTK line is good enough to preserve the project direction, but not strong enough yet for PRL-grade phase-sensitive exclusion wording.
- Promoted `BTK kernel upgrade required` to the single active bottleneck.

## 2026-04-30T10:10:00Z

- Implemented and ran `generate_channel_resolved_multiorbital_btk.py`.
- Generated a new package `btk-channel-resolved-multiorbital-semi-infinite-2026-04-30` with channel-resolved reflection amplitudes, multiorbital BdG pairing matrices, interface orientation dependence, and interface mixing dependence.
- Verified that the upgrade itself is real: the project no longer depends on the old scalar BTK proxy as its only BTK line.
- Verified that exclusion is still not closed: the upgraded package still gives the strongest total peak contrast in `s_wave`, while the strongest valley asymmetry shifts to `valley_odd`.
- Promoted `selection-rule null-model scan with upgraded BTK kernel` to the new single active bottleneck.