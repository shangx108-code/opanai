# Benchmark-Root Real-Data Availability Report

## Scope

This report records the direct availability check for real benchmark-root natural-image files needed before `scripts/run_natural_object_evaluation.py` can be honestly promoted from `proxy-only` to benchmark-root evidence.

## Local staging check

- `data/natural_objects/imagenet-1k-ilsvrc2012-validation/`
  - current files: `12`
  - observed file pattern: `imagenet_proxy_000.png` through `imagenet_proxy_011.png`
  - benchmark-root ready: `no`
- `data/natural_objects/coco-2017-validation/`
  - current files: `12`
  - observed file pattern: `coco_proxy_000.png` through `coco_proxy_011.png`
  - benchmark-root ready: `no`

## Workspace-wide search

- A workspace search for directories named with `imagenet`, `ilsvrc`, or `coco` found only the same project-local staging roots and the matching temporary mirror.
- No additional licensed benchmark-root ImageNet or COCO directories were found elsewhere in the current workspace.

## Connected Drive search

- A connected Google Drive search in this round did not return accessible files matching the needed benchmark-root ImageNet/COCO natural-image inputs for this project.

## Operational conclusion

- Real benchmark-root ImageNet/COCO files are still unavailable to the active project root.
- Therefore rerunning `scripts/run_natural_object_evaluation.py` right now would only reproduce `proxy-only` natural-image evidence rather than the requested benchmark-root evidence.

## Exact unblock condition

The blocker clears only when both audited dataset roots contain real licensed benchmark-root files rather than proxy placeholders:

- `data/natural_objects/imagenet-1k-ilsvrc2012-validation/`
- `data/natural_objects/coco-2017-validation/`
