# BTK Upgrade Result

Project: `twse2-andreev-prl`  
Date: 2026-04-30

## What was completed

The project now has a new BTK package:

- `btk-channel-resolved-multiorbital-semi-infinite-2026-04-30`

This package replaces the older scalar conductance proxy with:

1. a channel-resolved reflection calculation,
2. a multiorbital Nambu/BdG pairing structure,
3. explicit interface barrier `Z`,
4. explicit interface mixing `mixing_lambda`,
5. explicit interface orientation `alpha`.

The corresponding generation script is:

- `/workspace/memory/twse2-andreev-prl/code/generate_channel_resolved_multiorbital_btk.py`

## Main outcome

The kernel upgrade itself is successful and should now be treated as the active BTK engine.

However, the upgraded kernel does **not yet** close the PRL exclusion claim:

- the strongest compressed-V3 total peak contrast still appears in `s_wave`,
- the strongest valley asymmetry shifts to `valley_odd`,
- but the separation between pairing families is still modest rather than decisively exclusive.

## Quantitative readout to keep

- strongest total peak contrast: `s_wave`, `alpha = 0`, `Z = 0`, `mix = 0.35`, `eta = 0.05 meV`, `peak-background = 0.117763`
- strongest `K_B - K_T` peak-contrast asymmetry: `valley_odd`, `alpha = pi/3`, `Z = 2`, `mix = 0.35`, `eta = 0.05 meV`, `K_B - K_T = -0.137167`

## New active bottleneck

**use the upgraded channel-resolved multiorbital BTK kernel to design a null-model scan that forces ordinary same-sign `s`-wave to fail on at least one robust observable.**