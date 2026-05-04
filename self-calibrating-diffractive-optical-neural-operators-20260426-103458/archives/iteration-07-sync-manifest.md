# iteration-07 sync manifest

Project: `self-calibrating-diffractive-optical-neural-operators-20260426-103458`
Date: 2026-05-04
Archive: `iteration-07-submission-hygiene-source.zip`
Archive base64 sidecar: `iteration-07-submission-hygiene-source.zip.base64`
SHA256: `63038118cd2d9dc1e6bd3c6675701e3833f2e623d3bce65f687a67e820aabde8`

## Scope

This archive synchronizes the current submission-hygiene round:
- active naming/title cleanup
- Figure/table callout and terminology consistency checkpoint
- submission-facing manuscript package
- Figure 5 boundary note
- cover letter and reviewer response template when present

## Included files

- `manuscript/manuscript-v1-strict.md`
- `manuscript/round1-complete-skeleton.tex`
- `manuscript/round1-intake-draft.md`
- `manuscript/round8-figure5-boundary-note.md`

## Missing files at packaging time

- `README.md`
- `manifest.md`
- `project-state.md`
- `iteration-log.md`
- `manuscript/round10-submission-reproducibility-ledger.md`
- `manuscript/round11-cover-letter-final.md`
- `manuscript/round11-reviewer-response-template.md`

## Restore command

```bash
base64 -d iteration-07-submission-hygiene-source.zip.base64 > iteration-07-submission-hygiene-source.zip
unzip iteration-07-submission-hygiene-source.zip
sha256sum iteration-07-submission-hygiene-source.zip
```

Expected SHA256:

```text
63038118cd2d9dc1e6bd3c6675701e3833f2e623d3bce65f687a67e820aabde8
```

## Current active naming

- Working project title: `Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations`
- Submission-facing title: `Common-path conditional optics with diffractive neural operators for imaging through dynamic aberrations`

## Boundary status

Figure 5 is locked as processor-level boundary / limit-setting evidence, not as a weak device-level success.

## Local sync note

The current Python-visible environment could not write into `/workspace/.../archives` because that path is read-only from this runtime. The archive was therefore generated in `/mnt/data` for user download and GitHub synchronization.

## GitHub binary note

The GitHub connector available in this session cannot directly ingest a local `/mnt/data/*.zip.base64` file; it only accepts inline UTF-8 content. Therefore this manifest is synchronized first. The local zip and zip.base64 are available as downloadable artifacts in this conversation, and can be uploaded manually or split into smaller `.partNN.base64` files if full GitHub-side binary reconstruction is required.
