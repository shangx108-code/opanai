# CMJJ Source Data Package

This folder contains the first real source-data bundle for Figures 2-5 of the
compensated-magnetic Josephson-junction diagnostic branch.

## Model
- Minimal effective 1D compensated-magnetic Josephson-junction chain
- Momentum-space bulk model for the clean gap scan
- Real-space open chain for boundary spectra and transport
- Ring Pfaffian parity switch (`nu_ring`) for topology labels on finite devices

## Reproduction
Run:

```bash
python /workspace/memory/majorana-diagnostic-natphys/code/generate_cmjj_source_data.py
```

## Notes
- The current runtime does not provide `scipy` or `matplotlib`, so this package
  focuses on source data and metadata rather than rendered figures.
- All CSV files are plain UTF-8 and can be plotted later from the same project
  space once the preferred plotting stack is available.
