# E4 inner-gap selectivity note

## Current closure

- `Xi_AR = 1.011`
- `corr(E_AR, Delta_in) = 0.998`
- `corr(E_AR, E_out) = 0.299`
- threshold / barrier / broadening onset spreads remain at `0.000e+00`, `0.000e+00`, and `0.000e+00` in the saved validation suite

## Bounded claim

Within the current kernel family, the low-barrier Andreev onset follows the
inner superconducting scale much more closely than the outer normal-state
feature. This is strong enough for the manuscript-safe statement that the
present transport engine selects the inner-gap scale internally, but it is not
yet a license to claim direct experimental proof of the inner gap itself.

## What this closes

- the old `inner_gap_tracking` branch is no longer blocked
- threshold choice is not driving the onset ordering
- the present low/intermediate/high `Z` sweep does not flip the onset order
- the saved `Gamma` sweep does not create a fake selectivity branch

## What remains outside scope

- no claim of unique pairing-state identification
- no claim that every future control family must land on exactly the same `Xi_AR`
- no claim that the current kernel line alone replaces a full angle-resolved manuscript solver
