# Figure 5 Formal Summary

## Figure role
Figure 5 is the processor-level evidence figure. In the current raw-output-driven package, it should be read as a structured progression rather than a single-number claim.

## Raw-output chain used here
- round6: restored minimal baseline
- round7: first broad scan locating an ordinary-beating window
- round8: repeat-stability narrowing around the ordinary-beating window
- round15: failed micro-tuning attempt on the frame/two_spots risk tail
- round16: structural redesign scan for wrong-reference exclusion
- round17: higher-repeat confirmation of the selected structural mode
- round18: expanded OOD boundary test

## Main supported statements
- The restored round6 baseline is reproducible but does not support a common-path-over-ordinary claim.
- A stronger ordinary-beating window appears in round7 and survives repeat-focused narrowing in round8.
- Pure micro-tuning does not close the frame/two_spots risk tail in round15.
- Structural redesign in round16 creates the first q10-positive risk-pair window.
- Round17 confirms the selected structure over 14 repeats with common-minus-ordinary mean 0.638199 dB and minimum 0.412787 dB, while common-minus-wrong-reference mean is 0.277964 dB and minimum is 0.047469 dB.
- Round18 shows that this structure remains locally useful but does not generalize cleanly across the expanded OOD set; the expanded wrong-reference positive fraction drops to 0.611111.

## Best-window summary
- round7 best config: layers=1, reference_weight=0.2, phase_mix=0.15, common-minus-ordinary=0.629795 dB
- round8 best repeat-stable config: layers=1, reference_weight=0.16, phase_mix=0.15, common-minus-ordinary mean=0.438228 dB, minimum=0.390058 dB
- round16 best structural mode: sparse_tracker_decoy + occupancy_guarded, q10=0.014774 dB
- round17 confirmed structure: sparse_tracker_decoy + occupancy_guarded, q10=0.090496 dB, min=-0.024772 dB

## Boundary
This package supports a local, repeat-stable ordinary-baseline advantage together with improved but still incomplete wrong-reference exclusion. It does not support a claim of broad processor-level self-calibration closure across the expanded OOD set.
