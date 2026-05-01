# Fig. 4 / Fig. 5 Targeted Retune Summary

Objective: preserve misleading local near-zero structure in the controls while restoring
a clearly trivial topology label and strongly suppressed nonlocal signal.

## Decision
- Dot control can be kept trivial while remaining near-zero by moving to the lower-phi side of the old sweep.
- Impurity control also has a trivial near-zero window, but it sits on a narrower ridge than the dot case.
- The next Fig. 4 / Fig. 5 rebuild should use one dot candidate and one impurity candidate from this table rather than the old first-pass settings.

## Top dot candidates
- phi/pi=0.160, dot_strength=2.150, min|E|=0.000477, nu_ring=1, |GLR|(V=0.13)=1.316433e-08, GLL(V=0.13)=2.026210
- phi/pi=0.170, dot_strength=2.150, min|E|=0.000828, nu_ring=1, |GLR|(V=0.13)=2.228896e-08, GLL(V=0.13)=2.027095
- phi/pi=0.160, dot_strength=2.100, min|E|=0.001201, nu_ring=1, |GLR|(V=0.13)=1.425875e-08, GLL(V=0.13)=2.028462

## Top impurity candidates
- phi/pi=0.220, impurity_strength=2.250, min|E|=0.003687, nu_ring=1, |GLR|(V=0.13)=3.424878e-07, GLL(V=0.13)=2.144810
- phi/pi=0.190, impurity_strength=2.250, min|E|=0.005365, nu_ring=1, |GLR|(V=0.13)=2.841415e-08, GLL(V=0.13)=2.121023
- phi/pi=0.180, impurity_strength=2.225, min|E|=0.005685, nu_ring=1, |GLR|(V=0.13)=1.513626e-08, GLL(V=0.13)=2.115343

## Recommended next rebuild settings
- Dot mimic candidate: use the best-ranked dot row from `candidate_controls.csv`.
- Impurity mimic candidate: use the best-ranked impurity row from `candidate_controls.csv`.
- Recompute only Fig. 4 summary rows and Fig. 5 heatmaps around those candidates before any plotting or caption updates.
