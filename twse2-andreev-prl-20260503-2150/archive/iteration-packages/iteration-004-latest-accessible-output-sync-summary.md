# Iteration 004 GitHub Sync Manifest

- Package: `iteration-004-latest-accessible-output-sync.zip`
- ZIP bytes: `3925739`
- Base64 bytes: `5303193`
- SHA256: `cb8fa739af437ca9cae418f2eb5245aa5b5a11bff5dcbbdf66c599519f2ef9ab`
- Base64 chunks: `7`

## Restore

```bash
cat iteration-004-latest-accessible-output-sync.base64.parts/part-* > iteration-004-latest-accessible-output-sync.zip.base64
base64 -d iteration-004-latest-accessible-output-sync.zip.base64 > iteration-004-latest-accessible-output-sync.zip
sha256sum iteration-004-latest-accessible-output-sync.zip
```

## Boundary

The package contains only files visible in the current execution environment. Step 3 channel-competition raw outputs were not visible here and were not fabricated; see `sync/MISSING_CHANNEL_COMPETITION_SYNC_NOTICE.md` inside the zip.
