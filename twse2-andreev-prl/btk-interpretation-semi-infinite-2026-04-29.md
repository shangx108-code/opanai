# BTK Interpretation Note

Project: `twse2-andreev-prl`  
Date: 2026-04-29

## Scope

This note compares the older valley-resolved generalized BTK package built on the finite-ribbon SGF proxy with the newer rerun built on the validated semi-infinite SGF benchmark. The goal is to decide which BTK statements remain robust enough for manuscript use.

## Current stage

The BTK rerun itself is complete. The present stage is interpretation and manuscript-language tightening rather than additional BTK generation.

## Robust conclusions to keep

1. The BTK signal remains strongly valley-asymmetric after replacing the finite-ribbon proxy by the semi-infinite SGF benchmark.
2. The `K_T` sector consistently dominates over `K_B` in the semi-infinite rerun across the strongest asymmetry cases.
3. The semi-infinite rerun still supports a nontrivial compressed-V3-dependent valley-resolved conductance response, so the BTK line remains scientifically usable.
4. The semi-infinite SGF upgrade materially changes the apparent BTK ranking across pairing channels, so the manuscript should treat the semi-infinite BTK package as the only active evidence line.

## Claims to remove or weaken

1. Do not keep the older statement that `nodal_even` is the strongest compressed-V3-enhanced BTK channel in general. That ranking was specific to the finite-ribbon SGF input.
2. Do not describe the finite-ribbon-input BTK package as the current working result. It is now a historical comparison only.
3. Do not claim that compressed-V3 generically enhances total BTK peak contrast across the main pairing families. In the semi-infinite rerun, `s_wave` and `nodal_even` are mostly suppressed rather than enhanced.
4. Do not use any pairing ranking that mixes finite-ribbon and semi-infinite BTK outputs in the same argument.

## Semi-infinite BTK manuscript-ready reading

1. The strongest total peak-contrast gain under the validated semi-infinite SGF input shifts to the `valley_odd` channel at large barrier (`Z=2.0`) and larger broadening (`eta=0.5 meV`), but the gain is modest (`delta peak-minus-background = 0.085`).
2. The clearest robust BTK feature under the semi-infinite input is not the total-gain ranking but the valley asymmetry itself.
3. The strongest valley asymmetry under the semi-infinite input appears in the `s_wave` channel at transparent interface settings (`Z=0.0`, `eta=0.05 meV`), with `K_B - K_T = -4.188` in peak contrast.
4. The semi-infinite rerun therefore shifts the narrative from “which pairing gives the largest compressed-V3 enhancement” toward “which valley-resolved signatures survive the stronger normal-state benchmark.”

## Recommended manuscript wording direction

Use wording closer to:

“After upgrading the normal-state input from a finite-ribbon edge proxy to a validated semi-infinite surface Green’s-function benchmark, the valley-resolved BTK response remains strongly asymmetric between the two valleys. The strongest robust feature is the persistence of a much larger `K_T` conductance contrast than `K_B`, whereas the pairing-channel ranking of total compressed-V3 enhancement becomes less universal than in the earlier proxy-level analysis.”

Avoid wording closer to:

“The BTK data identify `nodal_even` as the uniquely dominant pairing channel.”

## Next action

1. Keep only the semi-infinite SGF input BTK package as the manuscript-facing main branch.
2. Treat the finite-ribbon-input BTK package strictly as a historical sensitivity check.
3. If a stronger BTK claim is still needed later, the next upgrade should target the BTK kernel itself rather than return to the SGF line.
