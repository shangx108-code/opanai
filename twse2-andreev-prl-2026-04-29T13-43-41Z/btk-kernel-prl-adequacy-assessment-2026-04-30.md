# BTK Kernel PRL Adequacy Assessment

Project: `twse2-andreev-prl`  
Date: 2026-04-30

## Decision

The current semi-infinite-informed BTK package is **not yet sufficient** to support PRL-level phase-sensitive exclusion claims on its own. It is strong enough to preserve the project line scientifically and to justify continued BTK-centered development, but it is still a **proxy kernel** rather than a manuscript-final generalized BTK engine.

## Why the answer is no

### 1. The current kernel is algebraic, not a scattering solution

In `generate_valley_resolved_generalized_btk.py`, the BTK core is

- `andreev = transparency * gap2 / denom`
- `normal_reflection = (1.0 - transparency) * energy2 / denom`
- `conductance = 1.0 + andreev - normal_reflection`

This is a useful conductance proxy, but it does not solve channel-resolved wave-function matching, a Nambu scattering matrix, or a surface-mode matching problem. Therefore it cannot yet carry a strong manuscript claim about phase-sensitive selection rules.

### 2. Pairing enters as a scalar profile rather than a multiorbital BdG structure

The current pairing library maps each candidate to a one-dimensional profile over `k2_grid`.

- `s_wave` is a constant scalar gap
- `nodal_even` is `delta0 * cos(phase)`
- `valley_even` and `valley_odd` are Gaussian-projector combinations

This is enough for sensitivity tests, but not enough to claim that the actual interface spectroscopy resolves the phase structure of a multivalley, multiorbital pairing matrix.

### 3. Valley resolution is imposed by Gaussian projectors, not derived from interface channels

The `K_B` and `K_T` separation is built from Gaussian masks centered at reduced `k2 = 1/3` and `2/3`. That means the present valley asymmetry is a controlled diagnostic construction, not yet a fully derived outcome of a microscopic interface-scattering problem.

### 4. The current kernel does not yet encode the PRL-critical interface variables

The present package sweeps `Z` and a broadening `eta`, but it does **not** yet implement the joint phase-sensitive control variables demanded by the project framing:

- interface orientation `alpha`
- explicit intervalley mixing at the interface
- incident-angle or transverse-channel integration derived from the real surface modes
- separation between physical broadening and interface mixing

Without these variables, the current BTK line cannot yet honestly support the manuscript claim that ordinary same-sign `s`-wave fails under a joint selection-rule test.

### 5. The strongest current asymmetry does not exclude ordinary `s`-wave

The current semi-infinite summary already reports the strongest `K_B - K_T` peak-contrast asymmetry in the `s_wave` channel. The direct robustness readout confirms the same pattern:

- strongest absolute valley peak-contrast difference: `s_wave`, `Z = 0.0`, `eta = 0.05 meV`, `K_B - K_T = -4.187808`

So the present kernel does not yet provide the one thing the PRL story most needs: a robust reason that ordinary same-sign `s`-wave fails while the unconventional family survives.

### 6. The package explicitly labels itself as a proxy benchmark

The active summary already states that this is still a proxy benchmark rather than the final semi-infinite multiorbital BTK result. That wording is scientifically correct and should be kept for now.

## What the current package is good for

The current BTK package is still useful for three narrower purposes:

1. It shows that the BTK line survives the normal-state upgrade from a finite-ribbon proxy to a validated semi-infinite SGF benchmark.
2. It preserves a real valley-resolved conductance asymmetry worth following.
3. It tells us that the next bottleneck is genuinely the BTK kernel itself, not a return to Track-1 normal-state reconstruction.

## Minimum upgrade required before PRL-level wording

The next BTK version should add the following minimum elements:

1. A channel-resolved generalized BTK or scattering-matrix solver built from the semi-infinite surface modes.
2. A multiorbital, multivalley BdG pairing matrix instead of the current scalar gap profile.
3. Explicit interface terms for barrier strength, intervalley mixing, and interface orientation.
4. Separation of physical Dynes-like broadening from interface mixing and transmission parameters.
5. A null-model test in which ordinary same-sign `s`-wave is subjected to the same joint selection-rule scan and fails on at least one robust observable.

## Practical ruling for the project

The main bottleneck should now be considered:

**BTK kernel upgrade required before PRL-grade phase-sensitive exclusion claims.**

Until that upgrade lands, the manuscript can safely say:

- the semi-infinite benchmark preserves a strong valley-resolved BTK response
- the BTK line remains scientifically promising

But it should not yet say:

- the present BTK package already excludes ordinary same-sign `s`-wave
- the present BTK ranking uniquely identifies the correct pairing family