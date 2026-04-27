# Manuscript V0 Structure

## Working title
Self-calibrating diffractive optical neural operators for imaging through dynamic aberrations

## Claim boundary
- Verified: common-path pilot/reference improves recovery relative to no-reference and non-common-path settings in Gaussian surrogate, Zernike wave-optics PSF modeling, and task-level cross-task surrogate evaluations.
- Partially verified: the pilot channel carries useful information about instantaneous degradation, consistent with the current CRLB-style and local task-level bounds.
- Not verified: the central device-level claim for a fixed passive diffractive processor under a unified ordinary-D2NN versus pilot-assisted-D2NN protocol.
- Therefore, the current manuscript can be written as a strict submission scaffold, but not yet as a submission-ready paper.

## Abstract skeleton
Dynamic aberrations and weak scattering limit optical imaging across microscopy, free-space sensing, and coherent computational imaging. Existing correction strategies typically rely on wavefront sensing, adaptive hardware, iterative optimization, or substantial electronic post-processing. Here we study whether a fixed diffractive optical processor can exploit a co-propagating optical reference to infer the instantaneous aberration state and improve image formation without dynamic reconfiguration of the optical hardware. Numerical evidence from Gaussian surrogates, wave-optics modeling with dynamic Zernike aberrations, and task-level generalization tests supports the core mechanism that a common-path pilot channel reduces uncertainty about the current degradation. However, the decisive passive-processor comparison between ordinary and pilot-assisted diffractive networks remains outstanding. The present draft therefore establishes the manuscript logic, evidence boundaries, figure roles, and citation chain needed for a strict writing workflow, while reserving the device-level main claim for the next verified result package.

## Introduction

### Paragraph 1: broad context
Optical imaging in microscopy, remote sensing, free-space links, and coherent sensing is routinely degraded by dynamic aberrations, turbulence, scattering, defocus, and system drift [1-8]. The central difficulty is not only that these degradations reduce contrast and resolution, but that their state can vary over time and across scenes, turning image formation into a moving inverse problem rather than a fixed one [7-13]. Adaptive optics, wavefront shaping, and computational correction have each delivered important advances, yet they usually depend on active correction elements, explicit wavefront estimation, iterative optimization, or heavy digital reconstruction [2-4,9-13].

### Paragraph 2: specific gap
Diffractive optical neural networks and related free-space optical processors have recently expanded passive optical computing from static classification toward phase imaging, denoising, inverse design, and analog optical inference [14-23]. Even so, most diffractive architectures are optimized for a fixed forward model or for a training distribution that treats optical perturbations as nuisance variability rather than as an instantaneous latent state to be inferred [14-21]. What remains unresolved is whether a fixed passive diffractive processor can become condition-aware without active tuning: can the optics recover useful information about the present aberration state from the incoming field itself and use that information during image formation?

### Paragraph 3: why existing routes remain insufficient
Existing routes do not fully close this gap. Robust training can average over a family of degradations, but does not by itself guarantee access to the current degradation realization. Guide-star or wavefront-sensing methods can estimate the aberration state, but typically require dedicated sensing paths, adaptive elements, or separate correction loops [2-4,11,24-26]. Purely digital learning-based restoration can be powerful, yet it moves the burden to electronic computation, latency, and training assumptions that may fail out of distribution [12,13,27-36]. A physically appealing alternative is to let a known optical reference co-propagate with the object through the same unknown degradation, so that the optical input already contains a conditional observation of the present distortion state.

### Paragraph 4: this work and contributions
This paper develops that conditional-optics perspective for self-calibrating diffractive processing. We formulate a common-path pilot/reference scheme in which object and reference fields share the same dynamic degradation, and we test whether the resulting observation can improve downstream recovery in fixed diffractive pipelines. The present evidence package establishes three elements needed for the manuscript spine: first, a mechanism-level signal showing that common-path reference information improves recovery relative to no-reference and non-common-path controls; second, a wave-optics validation under dynamic Zernike aberrations together with information-theoretic and task-level bounds; and third, a cross-task analysis clarifying where the gain is strongest and where it remains weak. The final device-level claim, namely an ordinary-D2NN versus pilot-assisted-D2NN comparison under a unified protocol, is still pending and is explicitly reserved as the critical next result.

## Main text structure

### Methods

#### Section 1. Optical formulation of common-path self-calibration
- Define the input field as the sum of an object channel and a known pilot/reference channel after the same unknown degradation operator.
- State clearly that the detector measures intensity, so cross terms can expose degradation-dependent information.
- Distinguish between the already verified mechanism-level observation model and the still-pending passive diffractive processor instantiation.
- Key citations: [2-4,11,14-26].

#### Section 2. Forward models and dynamic degradation families
- Gaussian surrogate for the minimal mechanism check.
- Wave-optics pupil model with dynamic Zernike aberrations.
- Task-level surrogate maps for reconstruction, classification residual, and inverse-design proxy.
- Reserve a subsection for the forthcoming passive diffractive processor protocol.
- Key citations: [1-13,14-23].

#### Section 3. Metrics, controls, and evidence status
- Define no-reference, common-path, non-common-path, and wrong-reference controls.
- Use PSNR and PSF mismatch as primary current metrics; do not overemphasize coefficient recovery.
- Mark current device-level processor comparison as not yet available.

### Results

#### Result 1. Common-path reference reduces uncertainty in the minimal mechanism model
Text role:
- Introduce Figure 1 immediately after the section opening.
- Use Figure 1 to show the conditional-optics concept and the no-reference / non-common-path / common-path contrast.
- State that this figure establishes the mechanism direction, not the final processor claim.

#### Result 2. The signal persists in a wave-optics model with dynamic Zernike aberrations
Text role:
- Introduce Figure 2 when moving from surrogate intuition to a physically grounded pupil-based forward model.
- Explicitly state the current verified numbers from project memory: common-path improves OOD reconstruction PSNR over no-reference and non-common-path controls in the wave-optics protocol.
- Use the figure to argue that the effect survives a more realistic coherent propagation model.

#### Result 3. Information-theoretic and task-level analyses explain when the pilot channel helps
Text role:
- Introduce Figure 3 for CRLB-style and local task-level bound arguments.
- Use the main text to separate rigorous statements from interpretive ones.
- Make clear that the theorem is local and does not prove global blind inversion.

#### Result 4. Cross-task generalization is strongest for reconstruction and weaker for inverse design
Text role:
- Introduce Figure 4 as the cross-task result package.
- Emphasize that reconstruction carries the clearest positive signal, classification residual is modestly positive, and inverse-design remains weak.
- This figure should prevent the discussion from overgeneralizing the current evidence.

#### Result 5. Passive diffractive processor comparison under a unified protocol
Text role:
- Introduce Figure 5 only after the result exists.
- Figure 5 must become the manuscript pivot once ordinary D2NN and pilot-assisted D2NN are both run under the same dynamic-aberration protocol.
- Until then, this section remains a locked placeholder and a formal blocker for submission.

### Discussion
- Summarize what is actually established: common-path pilot observations carry useful state information and improve recovery in current models.
- Explain why this differs from plain robustness training.
- Discuss failure modes: low-information pilot, reference mismatch, non-common-path corruption, limited gain under some tasks, and possible disappearance of the advantage in device-level D2NN tests.
- Explicitly note that the present manuscript boundary is below full submission maturity until the passive-processor comparison is completed.

### Summary
- Restate the main conceptual advance in one restrained sentence.
- Restate the current strongest verified evidence in one sentence.
- Restate the decisive missing evidence in one sentence.

## Figure-to-text argument map

### Figure 1. Concept and mechanism controls
- Must be cited in Introduction paragraph 4 and Result 1.
- Must support only the conditional-observation mechanism.
- Must not be used to claim passive processor success.

### Figure 2. Wave-optics dynamic-aberration validation
- Must be cited in Result 2 and Discussion.
- Must support persistence of the effect under a Zernike pupil model.

### Figure 3. Information and task-level bounds
- Must be cited in Result 3.
- Must support the statement that the pilot channel carries finite information and can lower downstream loss floors locally.

### Figure 4. Cross-task generalization
- Must be cited in Result 4 and Discussion.
- Must support the narrow statement that the gain is task-dependent, strongest for reconstruction in the current evidence package.

### Figure 5. Ordinary D2NN vs pilot-assisted D2NN under shared protocol
- Must be cited in Result 5, Discussion, and Summary.
- This figure is mandatory for the final submission narrative.
- Current status: missing.

## Evidence ledger

### A. User-provided facts
- The project aims at Nature Communications.
- The topic is self-calibrating diffractive optical processing for imaging through dynamic aberrations.
- The manuscript should use a classic four-paragraph Introduction and organize the main text as Methods, Results, Discussion, and Summary.
- References should exceed 30 and every figure must be explicitly cited and used for argument.

### B. Model-derived but plausible content
- The present manuscript spine uses five main figures, with Figure 5 reserved for the decisive passive-processor comparison.
- The abstract skeleton and section transitions are drafted in a restrained Nature-like voice.
- The current figure roles are inferred from the project-state evidence already stored in memory.

### C. Missing or unverified content
- Unified ordinary D2NN versus pilot-assisted D2NN result package.
- Final manuscript figures and captions.
- Final bibliography formatting in journal style.
- Full Methods parameter table and supplementary note structure.
