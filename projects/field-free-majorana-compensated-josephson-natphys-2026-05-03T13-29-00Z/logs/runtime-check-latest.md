# Runtime Check

- Timestamp: `2026-05-03T13:35:13Z`
- Python: `3.12.13`
- Platform: `Linux-6.12.47-x86_64-with-glibc2.39`
- Project root: `/workspace/memory/projects/field-free-majorana-compensated-josephson-natphys-2026-05-03T13-29-00Z`

## Module status

| Module | Status | Detail |
| --- | --- | --- |
| `numpy` | `ok` | `2.3.5` |
| `scipy` | `missing` | `No module named 'scipy'` |
| `matplotlib` | `missing` | `No module named 'matplotlib'` |
| `pandas` | `ok` | `2.2.3` |
| `kwant` | `missing` | `No module named 'kwant'` |
| `sympy` | `missing` | `No module named 'sympy'` |

## Interpretation

- `numpy/scipy/matplotlib/pandas` should be present for the first clean-limit calculation path.
- `kwant` is optional at setup time but may be needed later for transport-oriented workflows.
- Any missing package should be treated as an environment blocker only when the next concrete script requires it.
