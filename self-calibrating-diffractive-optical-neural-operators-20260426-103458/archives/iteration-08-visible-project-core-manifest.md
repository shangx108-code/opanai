# iteration-08 visible project core sync manifest

Project: `self-calibrating-diffractive-optical-neural-operators-20260426-103458`
Date: 2026-05-04

## Requested long-running project space

`/workspace/memory/projects/self-calibrating-diffractive-optical-neural-operators-20260426-103458`

## Visible source used for this archive

`/workspace/self-calibrating-diffractive-optical-neural-operators-20260426-103458`

## Included files

- `manuscript/round1-complete-skeleton.pdf`
- `manuscript/round1-complete-skeleton.tex`
- `manuscript/round1-intake-draft.md`
- `manuscript/round8-figure5-boundary-note.md`
- `manuscript/manuscript-v1-strict.md`

## Missing from visible source

- None

## Archive

- ZIP: `iteration-08-visible-project-core.zip`
- SHA256: `13a265a1fcb6e1c29f122cff814adbf7d554f735a1bbd72c448b794887694225`
- Base64 sidecar: `iteration-08-visible-project-core.zip.base64`
- Split parts: `20`

## Restore

```bash
cat iteration-08-visible-project-core.zip.base64.part*.txt > iteration-08-visible-project-core.zip.base64
base64 -d iteration-08-visible-project-core.zip.base64 > iteration-08-visible-project-core.zip
sha256sum iteration-08-visible-project-core.zip
unzip iteration-08-visible-project-core.zip
```

Expected SHA256:

```text
13a265a1fcb6e1c29f122cff814adbf7d554f735a1bbd72c448b794887694225
```

## Note

This archive uses only files currently visible to the runtime. It should be unpacked into the long-running project space if the target `/workspace/memory/...` directory is writable in a persistent runtime.
