# Benchmark-Root Natural-Object Audit

This file records whether the active staging directories contain genuine benchmark-root natural images or only proxy placeholders.

## Status

- `ImageNet-1k / ILSVRC2012 validation`: `proxy_only` with `12` files in `/workspace/memory/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z/data/natural_objects/imagenet-1k-ilsvrc2012-validation`
  blocker: all staged files are proxy-named placeholders rather than benchmark-root images
- `COCO / 2017 validation`: `proxy_only` with `12` files in `/workspace/memory/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z/data/natural_objects/coco-2017-validation`
  blocker: all staged files are proxy-named placeholders rather than benchmark-root images

## Rule

Natural-image evidence may be promoted from `proxy-only` only when both dataset roots are benchmark-root ready and the staged subset can be traced to licensed ImageNet/COCO files rather than project-local placeholders.
