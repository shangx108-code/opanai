# Round-6 Row-Asymmetric Recoupling Scan

## Goal

Restore phase leverage only through the surviving active row and its nearest bank interface, while keeping the suppressed row locked down.

## Best candidate

- `t_interface_left_active = 0.2`
- `alpha_interface_left_active = 0.3`
- `alpha_junction_x_active = 0.14`
- `barrier_active = 2.3`
- family-level `phi~pi` wins: `2/3`
- family-level minima at `phi=pi`: `2/3`
- mean phase-gain score: `0.006407`
- mean family gap spread: `0.000003`

## Full-scan result for the best candidate

- total points: `936`
- near-closing points: `104`
- near-closing `phi~pi` fraction: `0.154`
- near-closing low-phase fraction: `0.231`
- smallest gap: `0.000045` at `mu=1.000`, `M0=0.600`, `phi/pi=1.000`

## Interpretation

- This round restores phase leverage only on the active row side, not across the full junction.
- Compare directly against round four baseline: near-closing count `39`, `phi~pi` fraction `0.154`, low-phase fraction `0.231`.
- Compare directly against round five best uniform recoupling: near-closing count `204`, `phi~pi` fraction `0.147`, low-phase fraction `0.235`.

## Evidence status

- `locally promising but still too global`
