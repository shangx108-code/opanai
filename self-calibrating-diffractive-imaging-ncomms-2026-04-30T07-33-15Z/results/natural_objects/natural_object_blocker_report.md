# Natural-Object Evaluation Blocker Report

## Status

- Execution attempted: `yes`
- Evaluation completed: `no`
- Reason: required raw natural-image datasets are missing from the project-space staging root.

## Missing inputs

- `ImageNet-1k / ILSVRC2012 validation`
  - expected path: `/workspace/memory/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z/data/natural_objects/imagenet-1k-ilsvrc2012-validation`
- `COCO / 2017 validation`
  - expected path: `/workspace/memory/self-calibrating-diffractive-imaging-ncomms-2026-04-30T07-33-15Z/data/natural_objects/coco-2017-validation`

## Rule

Strict 1->2->3 execution forbids moving to step 3 before step 2 has real inputs and produces metrics.
