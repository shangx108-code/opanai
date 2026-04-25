# Verified Literature Positioning

## Purpose
Build a citation-verified novelty-positioning package that can be used directly in the Introduction, Results, and Discussion of the Nature Photonics manuscript.

## Verified primary-source basis
- Nature Photonics aims and scope page states that the journal publishes top-quality research in light generation, manipulation, and detection, with explicit coverage including optoelectronic devices and components, quantum optics, and nonlinear optics.
- Bandyopadhyay et al., *Single-chip photonic deep neural network with forward-only training*, Nature Photonics 18, 1335-1343 (published 2024-12-02), demonstrate a monolithically integrated coherent optical neural network that computes both linear and nonlinear functions on chip with 410 ps latency and 92.5% vowel-classification accuracy.
- Yildirim et al., *Nonlinear processing with linear optics*, Nature Photonics 18, 1076-1082 (published 2024-07-31), show that repeated-data multiple scattering can synthesize programmable linear and nonlinear transformations concurrently at low optical power.
- Wu et al., *Field-programmable photonic nonlinearity*, Nature Photonics 19, 725-732 (published 2025-04-15), demonstrate field-programmable nonlinear photonic hardware by spatially controlling carrier excitations in an active semiconductor and training polynomial photonic networks in situ.
- Wang et al., *An optical neural network using less than 1 photon per multiplication*, Nature Communications 13, 123 (published 2022-01-10), demonstrate low optical energy for optical dot products down to about 0.66 photons per multiplication.
- Ma et al., *Quantum-limited stochastic optical neural networks operating at a few quanta per activation*, Nature Communications 16, 359 (published 2025-01-03), demonstrate stochastic optical neural networks with single-photon detectors, physics-aware stochastic training, and MNIST classification in the approximately one-photon-per-activation regime.

## Comparator map

| Paper | What it establishes | Why it matters here | What it does **not** settle for this project |
| --- | --- | --- | --- |
| Bandyopadhyay et al. 2024 | Fully integrated coherent optical neural network with on-chip nonlinear activation and ultralow latency | Shows Nature Photonics interest in photonic-AI hardware with real nonlinear layers | Does not provide a common resource metric or lower bound for nonlinear activation cost across architectures |
| Yildirim et al. 2024 | Linear scattering and repeated data can realize nonlinear processing at low optical power | Prevents us from claiming that useful optical nonlinearity always requires intrinsic material nonlinearity or explicit optoelectronic activation | Does not compare physically different nonlinear routes on a common discrimination-cost axis, and does not ask when activation is worth paying for under a fixed photon budget |
| Wu et al. 2025 | Field-programmable nonlinear photonic microprocessor for polynomial networks | Raises the bar for programmability and device relevance | Does not frame nonlinear activation as a quantum-resource problem with lower bounds, detector-efficiency penalties, and task-level worth-it regions |
| Wang et al. 2022 | Sub-photon-per-multiplication optical dot-product inference | Occupies the low-photon linear-compute lane | Concerns mostly linear matrix operations plus downstream task accuracy, not the physical cost of nonlinear activation itself |
| Ma et al. 2025 | Single-photon-detector stochastic activations with physics-aware stochastic training in the few-quanta regime | Overlaps most strongly with our low-photon activation theme | Does not construct a cross-architecture activation-cost frontier, does not compare homodyne and displaced on-off routes against a lower bound, and does not derive the mixed result that activation can be worthwhile for some task geometries but not others under the same fixed-budget accounting |

## Reviewer-safe novelty claim
The manuscript should not claim generic photonic nonlinearity, generic low-power photonic AI, or generic programmability as its advance. The defensible novelty is narrower and sharper:

1. The paper treats nonlinear activation itself, rather than optical matrix multiplication or end-to-end classifier accuracy alone, as the physical object to be optimized.
2. It introduces one common resource language spanning a lower bound, two concrete measurement-induced routes, and a task-level fixed-budget benchmark.
3. It produces a mixed design-law result that recent comparator papers do not provide:
   the best implementable activation route is task dependent, and paying for activation is worthwhile only in task-and-budget regimes where nonlinear gain exceeds reliability loss from detector inefficiency, finite shots, and width-budget trade-off.

## Hard boundaries on what the manuscript may claim
- Do not claim the first unified treatment of photonic nonlinearity in general.
- Do not claim that measurement-induced activation is categorically superior to intrinsic or programmable material nonlinearity.
- Do not claim that low-photon activation automatically yields end-to-end system-energy advantage.
- Do not claim that the present task benchmark supersedes hardware demonstrations such as Wu et al. or Bandyopadhyay et al.

## Stronger positioning statement for the Introduction
Recent photonic-AI demonstrations have already shown that optical systems can deliver low-energy linear computation, on-chip nonlinear layers, and even programmable nonlinear processing. However, these advances answer different questions. They do not provide a common physical accounting of how expensive nonlinear activation itself is across distinct implementations, nor do they determine when paying that cost actually changes task-level design choices under realistic detector efficiency and finite-shot constraints. Our contribution is therefore not another claim that photonic nonlinearity is possible. It is a resource-and-regime framework that places lower bounds and implementable activation routes on the same axes, then tests whether their single-neuron ordering survives at fixed total activation budget.

## Results-side positioning sentence
Figure 3 should be framed against recent programmable and measurement-based photonic nonlinearity papers as a cross-architecture resource comparison, not as a new hardware demonstration. Figure 4 then supplies the missing systems consequence: closeness to the single-neuron frontier does not by itself determine the preferred activation route once task geometry and width allocation are included.

## Discussion-side positioning sentence
The main implication is not that one activation hardware wins universally, but that selective-journal photonic-AI claims should distinguish three different questions: can a nonlinear response be realized, how far above the physical frontier it sits, and whether paying for it is justified for the target task.

## Immediate manuscript inserts

### End-of-Introduction gap paragraph
Recent work has substantially tightened the design space for photonic neural nonlinearities. Integrated coherent processors have already combined optical matrix algebra with on-chip nonlinear activation and in situ training, low-power scattering-based systems have shown that nonlinear processing can emerge from nominally linear optical elements, and field-programmable nonlinear microprocessors now demonstrate dynamically reconfigurable polynomial photonic networks. Yet these advances do not answer the question addressed here: what is the physical cost of nonlinear activation itself, and when does paying that cost change the preferred photonic design under detector inefficiency, loss and finite-shot constraints? We therefore formulate nonlinear activation as a quantum-resource problem, compare lower bounds and implementable measurement-induced routes on common axes, and then test whether the resulting frontier alters task-level design conclusions under a fixed activation photon budget.

### Figure-3 to Figure-4 bridge paragraph
This literature separation matters for interpreting the transition from Fig. 3 to Fig. 4. Prior work establishes that photonic nonlinear processing can be implemented in several ways, including fully integrated on-chip activations, scattering-based polynomial transformations and stochastic few-photon detection. Our result is different in scope: Fig. 3 quantifies how detector efficiency and measurement architecture determine distance from a common activation frontier, whereas Fig. 4 asks whether that neuron-level ranking survives once total activation budget must be shared across a task. The answer is mixed: some nonlinear tasks justify paying for activation across the scanned budget range, whereas tasks with a strong linear baseline do not.

## Why this closes the current bottleneck
- The project now has a verified answer to the most obvious reviewer attack line: "how is this different from recent programmable/nonlinear photonic hardware papers?"
- The answer is now tied to specific primary-source papers and bounded claim language rather than placeholder novelty rhetoric.
- This removes the largest remaining Introduction-level ambiguity and unlocks cleaner manuscript integration.
