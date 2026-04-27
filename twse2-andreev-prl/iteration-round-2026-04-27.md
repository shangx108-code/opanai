# Iteration Round 2026-04-27

## Current Stage

Theory strengthening, codebase gap assessment, and three-track execution planning for the twisted bilayer WSe2 Andreev PRL project.

## Current Overall Goal

Close the evidence chain required for a reviewer-safe manuscript by completing:

1. exact `K`-point valley closure of the Tuo tight-binding model,
2. an independent surface Green's-function benchmark,
3. a fully data-backed BTK plus robustness package.

## Single Main Bottleneck

The single main bottleneck remains **exact `K`-point valley closure of the true Tuo TB model**.  
Reason: both the surface Green's-function benchmark and the BTK / robustness package depend on a credible material benchmark. If the normal-state Hamiltonian is still ambiguous at `K^B / K^T`, the later two modules can still be informative, but they cannot yet count as the final material-specific closure demanded by the user.

## Three Priority Tracks

### Track 1: `K`-point valley closure

- Current status: `partial`
- Verified:
  - representative hoppings parsed from Eq. (S1)
  - candidate full hopping table exists
  - executable reconstruction script exists
  - `Gamma`-point closure achieved
- Still missing:
  - exact full star ordering / phase convention
  - exact reproduction of Fig. 1c at `K^B / K^T`
  - proof that the resulting table is the true Tuo TB rather than one plausible completion
- Required deliverables:
  - exact full lattice-vector hopping table
  - exact `H_TB(k)` script
  - reproduction plot with negligible residuals at all high-symmetry points
- Completion standard:
  - no remaining `K`-point ambiguity
  - true Tuo TB replacement can be stated without caveat

### Track 2: surface Green's-function benchmark

- Current status: `not started`
- Verified:
  - manuscript planning notes already specify SGF as an independent benchmark
- Still missing:
  - explicit semi-infinite geometry
  - recursive / iterative SGF implementation
  - edge spectral-weight observable definition
  - consistency check between SGF edge hierarchy and BTK hierarchy
- Required deliverables:
  - SGF implementation note
  - saved edge spectral datasets
  - one benchmark figure package for manuscript and supplement
- Completion standard:
  - SGF benchmark is numerically reproducible
  - low-energy edge spectral weight can be used as an independent theoretical cross-check

### Track 3: BTK + robustness full data package

- Current status: `not started`
- Verified:
  - revision notes already define the desired BTK boundary-matching structure, observable tuple, and robustness data objects
- Still missing:
  - valley-Nambu boundary-matching implementation
  - conductance scans over `alpha`, `Z`, `eta`, broadening, and candidate pairing families
  - saved parameter maps for the falsification metric and robustness figures
  - experimental-extraction-ready summary products
- Required deliverables:
  - BTK implementation note
  - saved conductance arrays
  - robustness parameter maps
  - manuscript-safe observable definitions and captions
- Completion standard:
  - every main BTK claim is backed by saved arrays and parameter scans, not by handpicked curves

## Role Task Table

| Role | Current task | Input | Deliverable | Completion standard |
| --- | --- | --- | --- | --- |
| 统筹者 | Keep the single main bottleneck on true TB closure while sequencing SGF and BTK as dependent tracks | Current project state, user completion rule | One-round execution order | No dilution into three equal-priority bottlenecks |
| 技术状态检查者 | Mark each of the three tracks as verified / partial / not started | Reconstruction script, revision notes, workspace search | Three-track status audit | No paper claims beyond actual files |
| 环境配置负责人 | Confirm the minimum runnable path for future SGF and BTK implementations | Python toolchain, current workspace | Environment readiness note | Distinguish runnable environment from missing code |
| 理论与数值负责人 A | Solve `K`-point valley closure | SI, Fig. S1, source data | exact TB closure package | true Tuo TB without ambiguity |
| 理论与数值负责人 B | Design SGF benchmark module | future exact TB + pairing library | SGF code/data spec | edge benchmark becomes reproducible |
| 理论与数值负责人 C | Design BTK and robustness module | future exact TB + interface model | BTK code/data spec | conductance and robustness fully data-backed |
| 稿件状态检查者 | Keep manuscript language bounded until Track 1 closes | revision notes, current state | allowed / forbidden phrasing list | no premature material-specific claims |

## Honest Stage Judgment

The project has now clearly split into three technical tracks, but it is still in **evidence generation**, not in final manuscript revision or submission packaging.

## Immediate Next Action

1. Continue pursuing exact `K`-point valley closure as the single main bottleneck.
2. In parallel at the planning level, define the SGF and BTK data products so they can start immediately once the exact TB closure lands.
3. Do not upgrade the manuscript from “candidate reconstruction” to “true Tuo TB” before Track 1 closes.
