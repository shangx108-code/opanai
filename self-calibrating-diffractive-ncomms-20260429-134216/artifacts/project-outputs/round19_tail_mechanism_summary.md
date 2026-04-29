# Round 19 Tail Mechanism And Risk Metrics

- fixed structure: sparse_tracker_decoy + occupancy_guarded
- transfer penalty q10: -0.457 dB
- tail CVaR20: -0.444 dB
- negative mass: +0.107 dB
- sample failure breadth: 0.333
- ordinary-window retention: 0.677

## Tail Readout
- zigzag: mean/min common-minus-wrongref = -0.398/-1.204 dB; mechanism = ordinary-support failure dominates: the shape is thin or fragmented enough that common-path itself falls outside the stable processor window
- offcenter_disk: mean/min common-minus-wrongref = +0.226/-0.992 dB; mechanism = wrong-reference tracking dominates: the decoy amplitude matches the object support too well under occupancy_guarded encoding
- half_ring: mean/min common-minus-wrongref = -0.033/-0.429 dB; mechanism = wrong-reference tracking dominates: the decoy amplitude matches the object support too well under occupancy_guarded encoding
- disk: mean/min common-minus-wrongref = +0.273/-0.404 dB; mechanism = wrong-reference tracking dominates: the decoy amplitude matches the object support too well under occupancy_guarded encoding

## Recommended Figure 5 Boundary
- Keep Figure 5 as a narrow-subset confirmation only.
- Use tail CVaR20, negative mass, and sample failure breadth alongside q10 when discussing exclusion risk.
- Treat zigzag-like fragmented thin paths and off-center sparse objects as the current dominant extrapolation failure family.
