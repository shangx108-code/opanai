# Minimal Passive D2NN Protocol

## Purpose
- Define the next runnable data-completion target after environment bring-up.
- Keep the next iteration focused on the single bottleneck: ordinary D2NN versus pilot-assisted D2NN under one shared dynamic-aberration protocol.

## Required controls
1. no-reference ordinary processor
2. common-path pilot-assisted processor
3. non-common-path reference control
4. wrong-reference control

## Minimum outputs per run
1. `metrics.csv`
2. `summary.json`
3. `summary.md`
4. at least one panel PNG
5. one iteration-log entry

## Minimum metrics
1. reconstruction PSNR
2. intensity-domain MSE
3. control-to-control delta table
4. OOD split summary

## Environment constraint
- Current baseline environment must stay runnable with `numpy + Pillow`.
- Do not assume `matplotlib`, `scipy`, or `torch`.
