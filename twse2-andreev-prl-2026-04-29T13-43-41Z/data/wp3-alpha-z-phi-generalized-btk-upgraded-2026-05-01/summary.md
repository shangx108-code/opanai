# WP3 alpha-Z-phi generalized BTK summary

- Data status: generated
- Kernel status: upgraded alpha-Z-phi generalized BTK proxy with interface-competition resonance built on the current WP1-WP2 pairing library
- Barrier values: [0.0, 0.5, 1.0, 2.0, 3.0]
- Alpha values (rad): [0.0, 0.5236, 1.0472]
- Phi values (rad): [0.0, 0.3927, 0.7854, 1.1781, 1.5708, 1.9635, 2.3562, 2.7489, 3.1416]
- Eta values: [0.0, 0.5, 1.0]

## Candidate highlights
- s_wave: strongest peak contrast = 0.857 at eta=0.00, alpha=0.000, phi=1.571, Z=0.0
- s_wave: strongest phi anisotropy = 0.005 at eta=0.00, alpha=0.000, Z=3.0
- s_wave: strongest alpha anisotropy = 0.000 at eta=0.00, Z=3.0
- s_wave: fraction of tested (eta, phi) groups with monotonic Z dependence = 1.00
- s_pm: strongest peak contrast = 2.364 at eta=1.00, alpha=0.000, phi=1.571, Z=0.5
- s_pm: strongest phi anisotropy = 0.034 at eta=0.50, alpha=0.000, Z=2.0
- s_pm: strongest alpha anisotropy = 0.372 at eta=1.00, Z=1.0
- s_pm: fraction of tested (eta, phi) groups with monotonic Z dependence = 0.56
- chiral: strongest peak contrast = 0.902 at eta=0.00, alpha=0.000, phi=0.785, Z=3.0
- chiral: strongest phi anisotropy = 0.094 at eta=0.00, alpha=0.000, Z=2.0
- chiral: strongest alpha anisotropy = 0.004 at eta=0.00, Z=2.0
- chiral: fraction of tested (eta, phi) groups with monotonic Z dependence = 0.00

## First-pass reading
- s_wave should stay comparatively smooth in phi and alpha if the kernel is behaving sensibly.
- s_pm should turn on more strongly when eta is finite and when the interface orientation is favorable.
- chiral should keep a finite low-energy response even away from the strongest intervalley-mixing limit.
- The upgraded kernel explicitly allows a mid-barrier resonance, so non-monotonic Z behavior is now permitted rather than ruled out by construction.
