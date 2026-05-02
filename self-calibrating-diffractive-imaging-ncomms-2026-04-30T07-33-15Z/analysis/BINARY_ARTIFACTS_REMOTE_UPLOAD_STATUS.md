# Binary artifact remote-upload status

Generated: 2026-05-02

## Requested action
Upload the complete binary products for the self-calibrating diffractive imaging Nature Communications project into the GitHub project long-term space.

## Result in this environment
The GitHub connector successfully writes UTF-8 repository files, and the project summary/manifest files have been committed to the `open-ai` branch. However, the available connector interface does not expose a direct binary-content upload endpoint for arbitrary local files, and the container-level `git`/`curl` route to `github.com` remains unavailable. Therefore the binary payloads listed below were verified locally and mirrored in the local long-term space, but were not pushed as native binary files through this connector session.

## Binary artifacts verified in local long-term space

| file | size_bytes | sha256 |
|---|---:|---|
| manuscript/main.pdf | 1839377 | a57a5bf7f5bc580e07f6b6529a26a31c3d79d5000bc683b7dbdb4e2e2761cd03 |
| supplement/supplement.pdf | 152946 | 014437a1d298ebc8e8ebc22646c1dec9595bfd1a43187bcc110b09e89924fe57 |
| figures/figure_tolerance_collapse.png | 107748 | e3919386b92447b91b34fdb6f8b640dc03682761b54a11eb57e464fd52d50690 |
| figures/figure_phase_quantization_failure.png | 77099 | c57451e04fd63e5837dd0c5691a1f816e82e9c41cb31c7062069bd6f6a524fc6 |
| figures/figure_psf_domain_gap.png | 77037 | 173e26862b24cb6dd987b48f87ebe093353f343d161864d573aeb23707c246ef |
| source_data/measured_psf_or_speckle_dataset.npz | 11437001 | recorded in local submission artifact manifest |
| source_data/heldout_family_full_eval.npz | 3942 | recorded in local submission artifact manifest |
| full mirror tarball | 15738377 | 44a081e096dbdff5973d7724877e87469d359a95d94ea087b0e89808db8f265d |

## Local source locations

- Full mirror directory: `/workspace/github-sync/open-ai/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z`
- Full mirror tarball: `/workspace/github-sync/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z-full.tar.gz`

## Manual native-binary upload command from a network-enabled machine

```bash
git clone --branch open-ai https://github.com/shangx108-code/opanai.git
cd opanai
mkdir -p self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z
# copy the full local mirror contents into the directory above, preserving paths
# then:
git add self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z
git commit -m "Add compiled diffractive imaging binary artifacts"
git push origin open-ai
```

## Boundary statement
This file is a remote audit/status record. It does not claim that the native binary files themselves have been uploaded through the connector. It records the verified local artifacts and the exact native Git command sequence needed once a network-enabled Git environment is available.
