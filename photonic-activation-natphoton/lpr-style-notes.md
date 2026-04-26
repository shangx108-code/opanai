# LPR Style Notes

## Source set
- Uploaded reference bundle: `/workspace/user_files/01-cankao.zip`
- Extracted local corpus: `/workspace/tmp_lpr_refs/cankao/`
- Representative papers inspected:
  - Fang et al., *Decoding Optical Data with Machine Learning*, LPR (2020), DOI `10.1002/lpor.202000422`
  - Xu et al., *Photonic Perceptron Based on a Kerr Microcomb for High-Speed, Scalable, Optical Neural Networks*, LPR (2020), DOI `10.1002/lpor.202000070`
  - Zhan et al., *Physics-Aware Analytic-Gradient Training of Photonic Neural Networks*, LPR (2024), DOI `10.1002/lpor.202300445`
  - Zheng et al., *Photonic Neural Network Fabricated on Thin Film Lithium Niobate for High-Fidelity and Power-Efficient Matrix Computation*, LPR (2024), DOI `10.1002/lpor.202400565`
  - Liu et al., *Minimalist Optical Neural Computing*, LPR (2025), DOI `10.1002/lpor.202402303`

## Observed writing habits

### Abstract
- Opens with a broad but still field-specific motivation, usually in one sentence.
- Quickly names the unresolved bottleneck in sentence 2.
- Uses a decisive `Here, ...` sentence to state the main contribution.
- Summarizes 2-4 headline outcomes in compact quantitative or operational language.
- Ends with a consequence sentence such as `The results provide...`, `The work paves the way...`, or `This framework offers...`.

### Introduction
- Begins from the photonic-computing or photonic-device opportunity, not from abstract theory alone.
- Moves quickly from broad motivation to one specific bottleneck.
- Reviews adjacent literature in a compact, cumulative way rather than as a long catalogue.
- Makes the gap explicit before the manuscript's own contribution appears.
- Uses clear physical nouns: loss, fidelity, programmability, training overhead, scaling, throughput, energy efficiency.

### Results flow
- Section titles are functional and claim-bearing, for example `Physics-aware analytic-gradient training...` or `Photonic neural network fabricated...`.
- The results sequence usually goes from architecture or principle, to validation, to benchmark, to implication.
- Figures are expected to answer concrete device or systems questions rather than only offering conceptual cartoons.

### Tone
- Claims are confident but not ornamental.
- The prose is compact, technical, and applied-physics oriented.
- Broad significance is tied to performance, scalability, or implementation relevance.
- Papers usually avoid philosophical framing unless it translates into a measurable systems consequence.

### Discussion and ending
- The ending paragraph is short and forward-facing.
- It often emphasizes what the work enables for scalable photonics, practical deployment, or future integrated systems.
- Limitations are rarely overlong in the main text; they are acknowledged briefly and converted into next-step opportunities.

## Implications for this project

### What to keep
- Broad photonic-computing motivation
- Strong focus on nonlinear activation as the real bottleneck
- Device-facing implications of detector efficiency, loss, and sampling

### What to change from the Nature Photonics framing
- Reduce the emphasis on a field-reorganizing manifesto
- Increase emphasis on practical photonic design rules and benchmarkable operating windows
- Make the AQMA architecture feel like an implementable photonic scheme rather than a purely conceptual resource-theory object
- Keep the main claim technical and operational: when measurement-induced activation becomes worthwhile, and when it does not

## LPR-facing article template for this project
1. Title with a concrete technical noun phrase
2. Broad abstract with a `Here, ...` contribution sentence
3. Introduction with photonic-AI motivation, activation bottleneck, literature gap, and manuscript contribution
4. Results:
   - unified activation framework
   - activation quantum cost and discrimination cost
   - AQMA architecture
   - benchmark protocol and operating windows
   - device-level implications
5. Discussion
6. Experimental Section / Methods
7. Supporting Information note
