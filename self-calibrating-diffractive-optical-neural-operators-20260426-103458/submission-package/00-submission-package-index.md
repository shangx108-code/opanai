# Submission Package Index

## Package Identity

- Project: `self-calibrating-diffractive-optical-neural-operators-20260426-103458`
- Target journal: `Nature Communications`
- Package status: `current canonical package after round24 consistency sweep`
- Governing framing: `mechanism-first`
- Governing boundary: `Figure 5 is processor-level boundary / limit-setting evidence`

## Main Version Pointers

Use the following files as the current default submission package:

1. Manuscript main version:
   - `submission-package/01-manuscript-main.md`
2. Cover letter main version:
   - `submission-package/02-cover-letter-main.md`
3. Reviewer response main version:
   - `submission-package/03-reviewer-response-main.md`
4. Language lock / style guard:
   - `submission-package/04-language-lock.md`
5. Figure 5 short insert support file:
   - `submission-package/05-figure5-boundary-short-insert.tex`

## Source Mapping

- `01-manuscript-main.md`
  - derived from `memory/.../archive/manuscript-v1-strict.md`
  - round12 abstract, Result 5, and Discussion boundary text already applied
  - round24 Figure 5 quantitative support insert is available as a package support file, not as a separate manuscript version
- `02-cover-letter-main.md`
  - derived from `manuscript/round12-cover-letter-default.md`
  - current package role: canonical cover letter main version
- `03-reviewer-response-main.md`
  - derived from `manuscript/round12-reviewer-response-default.md`
  - current package role: canonical reviewer-response main version with round24 robustness wording aligned
- `04-language-lock.md`
  - derived from `manuscript/round12-submission-language-lock.md`
  - current package role: governing wording lock for all main-version files
- `05-figure5-boundary-short-insert.tex`
  - derived from locked Round18--19 numeric anchors plus round20--24 wording controls
  - intended as the canonical paste-ready Figure 5 support insert for the current writing pass

## Naming Rules

- When referring to the current manuscript in later notes, use `01-manuscript-main.md`.
- When referring to the current cover letter and reviewer response in later notes, use `02-cover-letter-main.md` and `03-reviewer-response-main.md`.
- Do not cite older `round12-*default*` filenames as the package primary once this index exists.
- Do not treat `05-figure5-boundary-short-insert.tex` as a separate manuscript version; it is a support insert under the current package.
- If a later round supersedes these files, update this index first, then update downstream references.

## Current Call Order

The current package should be read in this order:

1. `04-language-lock.md`
2. `01-manuscript-main.md`
3. `02-cover-letter-main.md`
4. `03-reviewer-response-main.md`
5. `05-figure5-boundary-short-insert.tex` when a compact Figure 5 numeric block is needed

## Non-blocking Compute Sidecar

- The current submission package does not depend on new compute to remain internally consistent.
- If additional compute is launched with Codex, it should be treated as a sidecar route for possible future strengthening, not as a blocker for the current package naming closure.
