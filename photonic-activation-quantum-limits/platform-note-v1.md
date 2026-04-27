# Platform Note V1

Last updated: 2026-04-27

## Purpose

This note translates the abstract detector-efficiency and propagation-loss scan into representative integrated-photonics platform windows using primary-source numbers. The goal is not to claim exact device readiness for our architecture, but to show that the explored parameter space overlaps with realistic hardware regimes.

## Source-backed reference points

1. SiN passive waveguides:
   Nature reports that silicon nitride waveguides can exhibit losses below 0.1 dB/m at telecommunication wavelengths.
   Source: `https://www.nature.com/articles/s41586-022-05119-9`

2. Hybrid LiNbO3-on-SiN platform:
   Nature Communications reports linear propagation loss of 8.5 dB/m in a heterogeneously integrated LiNbO3-on-SiN platform.
   Source: `https://www.nature.com/articles/s41467-023-39047-7`

3. SNSPD efficiency window:
   Nature Photonics reports a maximum system detection efficiency of 82% at low count rate and 64% at 320 Mcps for a fast SNSPD system at 1,550 nm.
   Source: `https://www.nature.com/articles/s41566-023-01168-2`

4. III-V/SiN fully integrated short-wavelength PIC:
   Nature reports sub-dB/cm passive SiN loss in the 900-980 nm band and a photodiode responsivity above 0.6 A/W on a III-V/SiN integrated platform.
   Source: `https://www.nature.com/articles/s41586-022-05119-9`

## How These Numbers Enter Our Paper

1. The explored detector-efficiency range `0.55-0.99` overlaps the SNSPD operating points cited above.
2. The explored loss range `0-6 dB` is stricter than a per-metre platform-loss figure for low-loss SiN and hybrid LiNbO3-on-SiN waveguides, so our scan should be interpreted as a compact-system or effective-path-loss window rather than a statement about metre-scale delay lines.
3. The III-V/SiN short-wavelength platform sits well outside the low-loss telecom passive window when written in dB/m, which helps explain why our present manuscript should not overextend low-budget conclusions across all material stacks.

## Claim Discipline

The manuscript should say:

1. the explored efficiency-loss region overlaps realistic detector and passive-waveguide operating points
2. the exact mapping from platform-level propagation loss to circuit-level effective loss depends on routing length, couplers, modulators and readout architecture
3. therefore the platform map is a plausibility map, not a turnkey hardware specification
