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
