# Feedback File Map

These are the core feedback files Codex should use. They are designed for one-pass execution, not project iteration.

## Files

- `01-run-report-template.md`: one per major run block
- `02-claim-evidence-template.md`: one per central claim check
- `03-figure-audit-template.md`: one per figure intended for manuscript use
- `04-blocker-template.md`: only when progress stops on a real blocker
- `05-parameter-register-template.csv`: cumulative parameter table for reusable runs

## Usage rule

Each major computation should return:

1. one run report
2. one claim-evidence sheet if the run tests a paper claim
3. one figure audit if the run creates a figure that might enter a draft

Do not skip the evidence label. Every file should say whether the evidence is `verified`, `partially verified`, `unverified`, `erroneous`, or `blocked`.
