# Round 11 Wrong-reference v2 Focused Scan

- scan size: 10 focused configurations
- repeats per config: 8
- fixed num_layers: 1
- fixed reference_weight: 0.16
- phase_mix grid: 0.14, 0.15, 0.16, 0.17, 0.18
- tested wrongref_v2 modes: task_matched_decoy, anti_phase_plus_decoy
- best wrongref_v2 mode: anti_phase_plus_decoy
- best phase_mix: 0.170
- mean common minus ordinary: +0.491 dB
- min common minus ordinary: +0.346 dB
- mean common minus wrongref: +0.101 dB
- min common minus wrongref: -0.013 dB
- std common minus wrongref: 0.090 dB
- interpretation: this round only tests whether the two strongest wrong-reference v2 decoys can preserve a positive common-minus-wrongref gap inside the current ordinary-positive window
