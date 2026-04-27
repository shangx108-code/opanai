# Review History

## 2026-04-24 | Pre-manuscript triage

### Material reviewed
- Concept note: `/workspace/user_files/01-1-.txt`

### Venue lens
Nature Physics article standard

### Reviewer-style verdict
Current outcome: below editorial-send-out threshold

### Why
1. The topic is important enough, but the present contribution is not yet clearly differentiated from prior work on nonlocal conductance correlations and disorder-aware Majorana diagnostics.
2. The note promises many observables and platforms, but does not yet define the single strongest result that would make the paper memorable.
3. The manuscript architecture is still missing real result-based prioritization.

### Closest overlap already visible
- Yi-Hua Lai, Jay D. Sau, and S. Das Sarma, Phys. Rev. B 100, 045302 (2019): end-to-end conductance correlations for MBS vs ABS
- Haining Pan, Jay D. Sau, and S. Das Sarma, Phys. Rev. B 103, 014513 (2021): three-terminal nonlocal conductance with disorder and inhomogeneity
- Rodrigo A. Dourado et al., Phys. Rev. B 110, 014504 (2024): local-conductance protocol using Green functions and scattering matrix in three-terminal nanowires
- Andreas Pöschl et al., Phys. Rev. B 106, L241301 (2022): experimental nonlocal conductance spectroscopy of ABS in gate-defined InAs/Al nanowires

### Acceptance-probability trend
- Start-of-project estimate for Nature Physics: 8-15%
- Upgrade condition to 20-30%: produce a cleanly novel cross-platform diagnostic principle with quantitative robustness windows
- Upgrade condition to 35%+: complete figure-grade numerics and literature positioning showing why prior protocols do not already subsume the new result

## 2026-04-25 | Literature-verified manuscript-package review

### Material reviewed
- Updated project package draft: `/workspace/research/manuscript_package.md`
- LaTeX manuscript scaffold: `/workspace/output/compensated-magnetic-majorana-draft.tex`
- Toy-model output: `/workspace/output/toy-model/toy-model-summary.png`

### New literature fact that changes the novelty bar
- Yang, Sun, Xie and Law, *Topological altermagnetic Josephson junctions*, *npj Quantum Materials*, published 1 April 2026, now directly occupies the field-free altermagnetic Josephson-junction headline claim

### Reviewer-style verdict
Current outcome: still below editorial send-out threshold, but better positioned than the concept-only version

### Why
1. The manuscript has now shifted toward a stronger claim centered on a diagnostic hierarchy rather than a platform-only proposal.
2. The narrative is substantially improved for a broad-reader venue, especially in the title/abstract/introduction package.
3. The evidence chain is still incomplete: the toy model is only an internal stress test, not a submission-grade result.

### New strongest path to upgrade
- Finish a unified transport benchmark across one positive topological control and three false-positive controls
- State one precise diagnostic principle and its failure window
- Use the compensated-magnetic setting as the most timely application, not as the sole source of novelty

### Acceptance-probability trend
- After literature verification and manuscript packaging: 10-18%
- Upgrade condition to 25-35%: complete the benchmark and make the diagnostic hierarchy quantitative

## 2026-04-26 | Project-standard escalation review

### Material reviewed
- Internal theory note: `/workspace/research/diagnostic_hierarchy_theory_note.md`
- Updated project memory and execution standard

### Reviewer-style verdict
Current outcome: still far below send-out threshold, but the project now has a much more honest and audit-ready internal standard

### Why
1. The manuscript now has explicit evidence-completion criteria instead of a loose collection of desired observables.
2. The success threshold has been correctly redefined as >70% estimated acceptance probability plus a closed evidence checklist, which is appropriate for a Nature Physics push.
3. The missing piece is unchanged in substance: no shared-pipeline benchmark yet exists.

### Acceptance-probability trend
- Current estimate remains 10-18%
- No upgrade justified from documentation work alone
- Upgrade condition to 25-35% remains the first real benchmark milestone
- Upgrade condition to >50% requires complete positive/negative-control evidence plus robustness windows
- Upgrade condition to >70% requires a submission-grade manuscript with closed evidence gaps, verified references, figure-ready results, and a strong final supervision pass

## 2026-04-26 | First real-data benchmark check

### Material reviewed
- Benchmark script: `/workspace/research/rashba_benchmark.py`
- Positive-control data: `/workspace/output/rashba-benchmark/positive_control_scan.csv`
- False-positive data: `/workspace/output/rashba-benchmark/smooth_dot_control_scan.csv`
- Summary figure: `/workspace/output/rashba-benchmark/rashba-benchmark-summary.png`

### Reviewer-style verdict
Current outcome: useful internal progress, but still not yet a persuasive manuscript figure set

### What was learned
1. The project has now moved beyond pure concept documents and contains real computed benchmark data.
2. The smooth-dot false-positive control reaches a much smaller finite-size minimum gap than the positive control in the present sweep.
3. A simple end-to-end nonlocality score is not by itself sufficient, because both the positive and false-positive controls can reach high values in this first pass.

### Why this is scientifically useful
This is a good stress test of the paper's central philosophy. It shows that the manuscript should not replace one weak single diagnostic with another. Instead, the paper must keep the full hierarchy logic: local anomaly, gap reopening, topology label, and nonlocal transport together.

### Acceptance-probability trend
- Current estimate remains 10-18%
- Real-data progress achieved, but no major upgrade justified until transport and topology information are coupled in the same benchmark

## 2026-04-27 | Expanded transport benchmark review

### Material reviewed
- Benchmark script: `/workspace/research/majorana_transport_benchmark.py`
- Output bundle: `/workspace/output/transport-benchmark/`

### Reviewer-style verdict
Current outcome: the numerical evidence classes are substantially more complete, but the benchmark is still not yet a submission-grade argument

### What improved
1. The code now produces transport-side observables rather than only finite-chain spectral proxies.
2. The result bundle includes positive-control, smooth-dot, impurity, disorder, eta-broadening, and representative bias-trace outputs.
3. The project now has real stored data for several main-text and supplementary-style evidence categories.

### What remains limiting
1. The present parameter family still does not generate strong false-positive zero-bias peaks in the way needed for a convincing failure figure.
2. The reflection-based topology proxy is not yet numerically decisive in the current implementation.
3. The transport benchmark is still effectively two-terminal wide-band rather than a fully convincing three-terminal manuscript engine.

### Acceptance-probability trend
- Current estimate remains 10-18%
- Numerical coverage improved, but the evidence is not yet strong enough to justify a higher editorial-confidence estimate

## 2026-04-27 | Three-terminal figure rebuild review

### Material reviewed
- Three-terminal benchmark script: `/workspace/research/majorana_three_terminal_figures.py`
- Output bundle: `/workspace/output/three-terminal-benchmark/`

### Reviewer-style verdict
Current outcome: this is the first numerically coherent Figure 3/4 candidate set, but still not the final manuscript version

### What improved
1. The benchmark is now three-terminal rather than only two-terminal wide-band.
2. Smooth-dot, impurity, and disorder controls are tuned to more misleading local low-bias behavior than before.
3. Figure 3 now shows a real local-failure comparison, and Figure 4 now shows that the absolute nonlocal signal is stronger in the positive control than in the tuned false positives.

### What remains limiting
1. The topology layer in Figure 4 still relies on the clean-backbone criterion rather than a stronger inhomogeneous topological discriminator.
2. The disorder false positive remains too dominant relative to the smooth-dot and impurity cases.
3. The positive-control gap panel still shows a monotonic finite-size trend rather than a visually sharp gap-closing/reopening story.

### Acceptance-probability trend
- Current estimate can cautiously move to 14-22%
- Reason: Figure readiness and benchmark realism improved, but the topological and robustness layers are still below the threshold needed for a top-tier theory paper

## 2026-04-27 | Topology-layer triage review

### Material reviewed
- Project memory state for `majorana-diagnostic-natphys`
- New upgrade note: `topology-layer-upgrade-spec-2026-04-27.md`

### Reviewer-style verdict
Current outcome: the manuscript logic is cleaner, but no acceptance-probability upgrade is justified without the full-device topology rerun

### What improved
1. The project now has one explicit replacement target for the weak topology panel instead of a vague instruction to "strengthen topology".
2. The Figure 4 story is now constrained to a consistency-filter claim rather than a nonlocal-only rescue claim.
3. The writing layer has reusable text that can be inserted once the stronger topology data exist.

### What remains limiting
1. No new real numerical evidence was generated in this scheduled run.
2. The current workspace does not contain the benchmark scripts or stored outputs needed to execute the rerun from here.
3. The paper still lacks the decisive full-device topological discriminator evaluated on the same inhomogeneous instances as the transport observables.

### Acceptance-probability trend
- Current estimate remains 14-22%
- No upgrade justified from specification work alone
- Next upgrade condition: produce a rerun Figure 4 in which the positive control sustains nonlocal transport, gap reopening, and full-device topological parity over a finite robustness window while the dot and impurity false positives do not
