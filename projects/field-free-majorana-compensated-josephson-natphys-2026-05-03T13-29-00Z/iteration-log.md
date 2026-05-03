# Iteration Log

## 2026-05-03 | Round 1 | Archive and runtime bootstrap

### Main bottleneck

Set up the canonical GitHub-backed project root and prepare a reusable runtime
environment skeleton for future manuscript and computation work.

### Actions

1. Created canonical project root `projects/field-free-majorana-compensated-josephson-natphys-2026-05-03T13-29-00Z`.
2. Archived the uploaded source brief into `archive/source-materials/initial-project-brief-2026-05-03.txt`.
3. Created mandatory project ledgers and memory-state files.
4. Created manuscript, configs, scripts, results, logs, archive, and indexes directories.
5. Prepared runtime-check tooling for dependency and path validation.
6. Created a project-local virtual environment wrapper with system site packages.
7. Ran the runtime checker and recorded currently available and missing modules.
8. Confirmed that direct `pip install` is blocked by the current network proxy.

### Output status

- Files created locally in canonical long-term space: `yes`
- GitHub write-back completed: `pending verification`
- Runtime check completed: `yes`
- Environment completeness: `partial; numpy and pandas available, scipy/matplotlib/kwant/sympy missing`

### Next shortest advancing action

Verify the whole project root on GitHub, then start a `numpy`-first clean-limit
model script that does not depend on the currently missing external packages.
