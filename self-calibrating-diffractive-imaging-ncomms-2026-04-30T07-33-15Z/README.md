# Self-Calibrating Diffractive Imaging

Target journal: Nature Communications

Canonical project root created: 2026-04-30T07-33-15Z

This project studies passive self-calibrating diffractive optical neural operators for imaging through dynamic aberrations. The immediate goal of this project space is to provide a stable long-term root for iterative research execution, evidence tracking, environment validation, and future manuscript assembly.

Canonical long-term main space:

- GitHub repository: `shangx108-code/opanai`
- GitHub branch: `open-ai`
- GitHub project root: `self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`
- Current local working mirror: `/workspace/memory/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`

This means the project root definition is fixed and the substantive tracked project files are aligned to that canonical GitHub path. What remains incomplete is the evidence package itself, not the project-space placement.

Project layout:

- `config/`: stable project metadata and stop criteria
- `manuscript/`: draft text, outline, references, and compiled deliverables
- `results/`: reproducible outputs, tables, and future figures
- `scripts/`: executable utilities for environment checks and project-state validation
- `logs/`: per-iteration notes and scheduler-facing run logs
- `indexes/`: authoritative project indexes and handoff summaries

Current primary bottleneck:

- The linked fabrication-style tolerance scan is now executed, and it shows that the unmitigated stack has only a narrow clean-hardware positive region on `UCID`; mild phase noise or mild layer misalignment already closes that region.

Current first advancing action:

- Use the new `results/tolerance_joint/` boundary tables together with the Kodak/UCID public-data results to rewrite the manuscript and reviewer-facing claim boundary around a dataset-dependent public-data story plus a narrow clean-stack fabrication-tolerance window.
