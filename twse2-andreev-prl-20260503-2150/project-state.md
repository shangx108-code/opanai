# Project State

- Current stage: `active calculation/verification bootstrap`
- Unique main bottleneck: `computational correctness and reproducibility gap`
- Why this is first: the project outline and target journal are already clear from intake materials, but the formal project root did not yet have a verified executable environment tied to the new canonical archive path.
- Latest real progress:
  - locked the canonical project identifier `twse2-andreev-prl-20260503-2150`
  - initialized the canonical project root and archive structure
  - installed a runnable WP1-WP2 minimal engine into the canonical root
- Current accepted evidence:
  - project objective, paper structure, and PRL positioning are specified in the two uploaded markdown notes
  - minimal code scaffold exists for two-scale DOS calibration and pairing-family screening
- Verified bootstrap status:
  - `scripts/run_wp1_wp2.py` runs successfully in the canonical root
  - first result package now exists under `results/`
  - inferred inner scale from the bootstrap BdG DOS: `0.1180`
  - inferred outer scale from the bootstrap normal DOS: `0.6740`
  - bootstrap outer/inner ratio: `5.71`
- Immediate next action: `harden the generalized BTK layer on top of the verified WP1-WP2 scaffold`
- Archive status note: `GitHub project root exists and core executable files are mirrored, but four text ledger files still need a later authenticated writeback`
