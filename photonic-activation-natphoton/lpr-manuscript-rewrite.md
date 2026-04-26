# Activation Quantum Cost for Photonic Neural Networks: A Measurement-Induced Route Toward Practical Nonlinear Photonics

## Abstract
Photonic neural networks promise high-bandwidth and energy-efficient information processing because linear optical transformations can be executed in parallel with low latency. Their practical scalability, however, is still constrained by nonlinear activation, which commonly relies on electronic feedback, strong material nonlinearities, or measurement overhead that is difficult to compare across platforms. Here, a unified framework is introduced to quantify the physical cost of nonlinear activation in photonic neural networks. Three complementary metrics are defined: the activation quantum cost for functional approximation, the discrimination cost for noise-limited input separation, and the task-level energy-accuracy cost for system performance. Within this framework, electronic, Kerr-like, saturable, photon-counting, homodyne, and measurement-feedback activations are described by a common constrained channel model. A measurement-induced architecture, termed adaptive quantum measurement activation (AQMA), is then formulated as a practical route toward programmable nonlinear photonics in the few-photon regime. The resulting analysis clarifies which activation mechanisms are favorable under detector inefficiency, optical loss, finite-shot sampling, and feedback overhead, and it identifies the operating windows in which measurement-induced activation can approach the useful energy frontier. This framework provides a device-oriented basis for benchmarking nonlinear photonic intelligence hardware and for designing low-light photonic neural processors.

## 1. Introduction
Photonic neural networks have emerged as an attractive hardware route for machine learning because optics naturally supports high-throughput matrix operations, wavelength-division parallelism, and low-latency signal propagation. Recent progress in integrated Mach-Zehnder meshes, Kerr microcomb processors, thin-film lithium niobate platforms, and diffractive optical networks has pushed photonic computing beyond proof-of-concept demonstrations and toward increasingly capable neural hardware.[1-6] This momentum has sharpened a practical question: which parts of neural computation are already well served by photonics, and which parts still dominate the physical cost?

For most photonic neural-network platforms, the answer is no longer the linear transform. Programmable and low-loss photonic linear layers are advancing rapidly, as evidenced by recent progress in scalable tensor-core topologies, analytic-gradient training strategies, and power-efficient integrated meshes.[3-5] The more persistent bottleneck is nonlinear activation. In practice, activation is often realized through optoelectronic feedback, carrier or thermal effects, intrinsic material nonlinearity, or measurement-conditioned modulation. These routes differ strongly in optical power, latency, noise sensitivity, and hardware complexity, yet they are still compared mostly through task-specific accuracy or device-specific heuristics rather than through a shared physical metric.

This comparison problem has become more urgent as photonic artificial intelligence broadens from matrix multiplication accelerators to task-oriented computing systems. Recent LPR studies have demonstrated photonic perceptrons, physics-aware training, compact diffractive architectures, and multifunctional optical neural networks across diverse platforms.[2-6] These works establish the versatility of photonic neural processing, but they do not answer a more basic design question: how much physical resource is required to realize a useful nonlinear activation under realistic optical loss, detector inefficiency, and finite sampling? Without such a criterion, it remains difficult to judge when sophisticated nonlinear photonic schemes are genuinely worthwhile and when simpler alternatives remain preferable.

In this work, we recast nonlinear activation in photonic neural networks as a constrained physical channel-design problem. Instead of asking only whether an activation can be implemented, we ask how expensively it can be implemented in the few-photon regime while retaining functional fidelity and task usefulness. This shift leads to three metrics. The first is the activation quantum cost, which measures the minimum optical resource required to approximate a target nonlinear response within a specified tolerance. The second is the discrimination cost, which quantifies whether the activation remains informative once noise-induced overlap between nearby inputs is taken into account. The third is the task-level energy-accuracy cost, which links the activation layer to whole-network utility.

On top of this framework, we formulate adaptive quantum measurement activation, or AQMA, as a measurement-induced route to programmable nonlinear photonics. AQMA uses a weak optical tap, a photon-counting or homodyne measurement, and conditional modulation to synthesize activation responses that are difficult to obtain directly from low-power intrinsic optical nonlinearities. The central point of the present manuscript is not that measurement-induced activation is universally superior. Rather, the analysis identifies the practical operating windows in which measurement-induced activation can approach the useful energy frontier, and it makes equally explicit the regimes in which measurement overhead, detector noise, or feedback costs erase that advantage.

This article is therefore positioned as a design framework for nonlinear photonic intelligence hardware. In the following, a unified activation model is established, cost metrics are defined, AQMA is introduced as a practical architecture, and a benchmark protocol is organized for comparing competing activation mechanisms under common photonic constraints.

## 2. Unified Framework for Physical Activation in Photonic Neural Networks
We consider a scalar pre-activation variable `x` encoded into an optical state `rho_x`. A physical activation layer is then represented as a constrained channel `A_theta` that maps `rho_x` to an effective output `y` through an optical, material, or measurement-assisted nonlinear transformation. In the most general form used here,

`y = E[g_theta(m, u) | rho_x, eta, ell, xi, N_s]`

where `m` is the measurement outcome when measurement is present, `u` is a feed-forward or feedback control variable, `theta` denotes programmable parameters, `eta` is detector efficiency, `ell` is optical loss, `xi` collects nuisance noise terms, and `N_s` denotes the effective shot budget. This representation is intentionally broad enough to describe electronic activation, Kerr-like and saturable nonlinear response, photon-counting activation, homodyne-conditioned activation, and explicit measurement-feedback schemes within one comparison frame.

The value of this unified description is practical rather than purely formal. It allows every activation family to be evaluated under a common accounting rule: each candidate mechanism must be judged not only by the shape of its input-output response, but also by the resource required to realize that response, the noise penalty incurred during its realization, and the system-level consequence of using it inside a network. This is the central shift needed to compare nonlinear photonic hardware on equal terms.

## 3. Activation Quantum Cost and Discrimination Cost
Let `sigma(x)` be a target activation function defined on the working input interval `[x_min, x_max]`. The functional approximation error of a physical activation is written as

`E_act(theta) = integral w(x) |A_theta(x) - sigma(x)|^2 dx`

where `w(x)` is the relevant input weighting. Based on this quantity, the activation quantum cost is defined as the minimum average optical resource required to reach a target tolerance `epsilon`:

`C_AQC(sigma, epsilon) = min { n_bar(theta) : E_act(theta) <= epsilon }`

Here `n_bar` is the average photon number consumed per activation event under a clearly specified operating convention. This metric answers the first design question: how expensive is a nonlinear response in the few-photon regime?

Functional imitation alone is not sufficient for neural utility. A physical activation may approximate the shape of a target nonlinearity yet remain ineffective once shot noise, dark counts, finite sampling, or hardware noise broaden nearby outputs. To address this, a discrimination score is introduced for nearby encoded inputs `x_1` and `x_2`:

`D(x_1, x_2; theta) = |mu_1 - mu_2| / sqrt(var_1 + var_2)`

with `mu_i = E[y | x_i]` and `var_i = Var[y | x_i]`. The corresponding discrimination cost is defined as the minimum resource needed to keep this score above a target threshold across the difficult input pairs around the activation turning region. Together, `C_AQC` and discrimination cost prevent a misleading conclusion in which a response is judged favorable because it looks nonlinear on average while failing to provide reliable input separation in practice.

At the network level, these quantities connect naturally to a task-level energy-accuracy cost:

`C_task(A_0) = min { E_inf : Accuracy >= A_0 }`

where `E_inf` includes linear propagation, taps, detectors, and conditional modulation overhead. This three-level metric stack separates three distinct questions: whether an activation can imitate a desired response, whether it remains informative under realistic noise, and whether it ultimately improves task performance at acceptable system cost.

## 4. Adaptive Quantum Measurement Activation
The proposed AQMA architecture is motivated by a simple observation: low-power intrinsic optical nonlinearities are often weak, but optical measurements already provide sharply nonlinear statistical responses. AQMA harnesses this fact by extracting a small amount of information from the optical state and then using the measured information to shape the output nonlinearly.

In its threshold-counting form, a weak tap is taken from the signal and sent to a photon-counting detector. The output is conditioned on whether the measured count exceeds a threshold `k`, producing an activation of the form

`A_AQMA(x) = a_0 + a_1 P(n >= k | x, eta, ell, xi)`

This yields a naturally sigmoid-like response whose slope and working point are controlled by the tap ratio, threshold, and detector characteristics. In a homodyne-conditioned form, AQMA uses quadrature measurements and Bayesian estimation to generate a continuously tunable activation response. These two variants share the same photonic logic but emphasize different practical advantages: threshold AQMA is closer to minimal hardware implementation, whereas homodyne AQMA offers smoother programmability.

AQMA should not be interpreted as a universal replacement for other activation mechanisms. Its appeal lies instead in regimes where direct optical nonlinearity is too weak or too lossy, while measurement overhead remains moderate enough that the induced nonlinearity becomes resource-competitive. The framework developed here is designed precisely to delineate these regimes.

## 5. Benchmarking Protocol for Useful Nonlinear Photonics
To convert the framework into a practical evaluation tool, we organize the benchmark in three levels. The first level concerns single-neuron activation physics. Electronic, Kerr-like, saturable, photon-counting, homodyne, and AQMA activations are compared against target responses such as sigmoid-like, tanh-like, soft-threshold, binary stochastic, and saturating activations. The main outputs at this stage are the response curve, the activation quantum cost, and the discrimination cost. This stage reveals whether a nominally attractive activation family is intrinsically limited by optical resource or noise sensitivity.

The second level concerns small-network utility. A common optical network template is used to compare activations on tasks such as two-moons classification, concentric-circles classification, and low-light signal discrimination. These tasks are chosen not because they define the field's end goals, but because they isolate the utility of nonlinearity under controlled photonic constraints. The key output is the energy-accuracy frontier. This reveals whether a single-neuron advantage survives once activation cost is embedded into a full inference pipeline.

The third level concerns device-feasibility maps. Detector efficiency, optical loss, dark-count probability, and shot budget are scanned to identify useful, marginal, and not-worth-it operating regions. This stage is especially important for LPR-facing positioning because it connects the framework to photonic-device decision making rather than to abstract algorithmic comparison alone.

The first publishable target within this benchmark structure is not an exhaustive task sweep. It is a regime-boundary figure that answers a concrete question: under what optical resource and detector conditions does measurement-induced activation cease to be overhead-dominated and become a competitive nonlinear photonic primitive? Such a figure would already constitute a decision-relevant design result.

## 6. Device-Level Implications for Photonic Neural Hardware
The framework developed here has several consequences for the design of photonic neural processors. First, it shifts nonlinear activation from an implementation detail to an explicitly benchmarked systems bottleneck. This matters because different photonic platforms excel in different parts of the neural pipeline. A low-loss programmable mesh, for example, may be highly attractive for the linear transform while remaining activation-limited. Second, it shows that nonlinear photonics should not be judged solely by nominal response shape. The decisive quantity is whether a mechanism preserves useful discrimination after realistic noise and hardware overhead are included.

Third, the framework suggests that the most attractive nonlinear route may depend on operating regime rather than on a universally best device concept. At high optical power or loose power budgets, conventional optoelectronic activation may remain preferable. At very low power, intrinsic material nonlinearities may become too weak to be practical. Between these regimes, measurement-induced activation may provide a useful compromise if detector performance and feedback overhead are favorable. This regime-based view is better aligned with how photonic hardware is actually designed.

Finally, the present analysis points to an experimentally accessible validation route. A minimal AQMA testbed can be built from a weak coherent input, a beam splitter tap, a single detector arm, conditional modulation, and a compact linear optical layer. Even before a full photonic neural processor is assembled, such a setup could measure activation response curves, discrimination behavior, and operating-window boundaries directly.

## 7. Discussion and Outlook
This work reframes nonlinear activation in photonic neural networks as a resource problem that sits at the intersection of quantum measurement, nonlinear photonics, and hardware-aware machine learning. The main benefit of this viewpoint is not terminological. It is that physically distinct activation mechanisms can now be compared through a common set of quantities tied to implementation constraints, signal discrimination, and task performance.

Several important limitations should be stated clearly. First, the framework depends on an explicit accounting convention for optical energy, measurement overhead, and latency. These assumptions must remain visible, because different conventions can change the location of the useful operating window. Second, the present manuscript establishes the comparison framework and the AQMA architecture, but the strongest claims will ultimately depend on benchmark results that quantify the actual regime boundaries. Third, the framework does not imply that every useful activation must be quantum in a strict information-theoretic sense. Rather, it shows that low-light nonlinear activation becomes inseparable from quantum-limited measurement and noise considerations.

Despite these caveats, the framework is well suited to the next stage of nonlinear photonic hardware development. It provides a common language for comparing intrinsic optical nonlinearities, optoelectronic activation, and measurement-induced schemes, and it suggests a concrete route toward low-light photonic processors in which activation is optimized rather than merely added. In this sense, activation quantum cost is not only a metric for comparison; it is a design principle for practical photonic intelligence systems.

## 8. Experimental Section / Methods

### 8.1 Optical Encoding and Activation Model
The logical pre-activation variable is encoded into an optical state `rho_x` over a specified operating interval. All activation families are mapped onto the common channel model described in Section 2, with explicit accounting of detector efficiency, optical loss, nuisance noise, and effective shot budget.

### 8.2 Metrics
The benchmark uses three metrics. The activation quantum cost measures the minimum average photon number needed to realize a target activation to within a specified approximation tolerance. The discrimination cost measures the minimum resource required to preserve noise-limited separation of nearby inputs. The task-level energy-accuracy cost measures the minimum inference energy required to achieve a target task accuracy under the same accounting convention.

### 8.3 Candidate Activation Families
Electronic, Kerr-like, saturable, photon-counting, homodyne, and AQMA activations are parameterized under common encoding and noise assumptions. AQMA is studied in threshold-counting and homodyne-conditioned forms.

### 8.4 Benchmark Structure
The benchmark proceeds from single-neuron response analysis to small-network task evaluation and finally to device-feasibility mapping. The first milestone is a regime-boundary benchmark that identifies the useful operating window of measurement-induced activation under realistic detector and loss parameters.

## Supporting Information
Supporting Information is expected to include derivation details, accounting conventions, baseline parameter sweeps, sensitivity scans, and additional task results beyond the main-text benchmark figures.

## References
[1] X. Xu, M. Tan, B. Corcoran, J. Wu, T. G. Nguyen, A. Boes, S. T. Chu, B. E. Little, R. Morandotti, A. Mitchell, D. G. Hicks, D. J. Moss, Photonic Perceptron Based on a Kerr Microcomb for High-Speed, Scalable, Optical Neural Networks, Laser Photonics Rev. 2020, DOI: 10.1002/lpor.202000070.

[2] R. Chen, Y. Li, M. Lou, J. Fan, Y. Tang, B. Sensale-Rodriguez, C. Yu, W. Gao, Physics-Aware Machine Learning and Adversarial Attack in Complex-Valued Reconfigurable Diffractive All-Optical Neural Network, Laser Photonics Rev. 2022, DOI: 10.1002/lpor.202200348.

[3] Y. Huang, H. Yue, W. Ma, Y. Zhang, Y. Xiao, W. Wang, Y. Tang, X. Hu, H. Tang, T. Chu, Easily Scalable Photonic Tensor Core Based on Tunable Units with Single Internal Phase Shifters, Laser Photonics Rev. 2023, DOI: 10.1002/lpor.202300001.

[4] Y. Zhan, H. Zhang, H. Lin, L. K. Chin, H. Cai, M. F. Karim, D. P. Poenar, X. Jiang, M.-W. Mak, L. C. Kwek, A. Q. Liu, Physics-Aware Analytic-Gradient Training of Photonic Neural Networks, Laser Photonics Rev. 2024, DOI: 10.1002/lpor.202300445.

[5] Y. Zheng, R. Wu, Y. Ren, R. Bao, J. Liu, Y. Ma, M. Wang, Y. Cheng, Photonic Neural Network Fabricated on Thin Film Lithium Niobate for High-Fidelity and Power-Efficient Matrix Computation, Laser Photonics Rev. 2024, DOI: 10.1002/lpor.202400565.

[6] J. Cheng, C. Li, J. Dai, Y. Chu, X. Niu, X. Dong, J.-J. He, Direct Optical Convolution Computing Based on Arrayed Waveguide Grating Router, Laser Photonics Rev. 2024, DOI: 10.1002/lpor.202301221.

[7] X. Liu, T. Ma, Q. Bao, Z. Ma, G. Gao, J.-J. Xiao, Minimalist Optical Neural Computing: Optical Diffractive Neural Network by 2-level Quantized Pixel-Wise Optical Encoding, Laser Photonics Rev. 2025, DOI: 10.1002/lpor.202402303.

[8] H. Yan, Y. Sun, Y. Yu, R. Ma, X. Chen, Y. Chen, W. Wan, Multi-Functional Optical Neural Network in a Disordered Medium, Laser Photonics Rev. 2025, DOI: 10.1002/lpor.202501407.

[9] J. Fang, A. Swain, R. Unni, Y. Zheng, Decoding Optical Data with Machine Learning, Laser Photonics Rev. 2020, DOI: 10.1002/lpor.202000422.

[10] B. P. Doylend, A. P. Knights, The Evolution of Silicon Photonics as an Enabling Technology for Optical Interconnection, Laser Photonics Rev. 2012.
