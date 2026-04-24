# Manuscript V0

## Title

Quantum limits of nonlinear activation in photonic neural networks

## Central Claim

Nonlinear activation, rather than linear optical matrix multiplication, sets the decisive resource bottleneck for low-photon photonic neural networks; a unified activation-cost framework can compare physical nonlinear mechanisms on the same energy-versus-functionality axis.

## Supported In This Version

1. The manuscript framing and literature positioning.
2. A first proxy implementation of several activation families within one numerical scaffold.
3. Preliminary evidence that measurement-induced AQMA-like activation can approximate sigmoid-like targets well at low photon budget in the current proxy model.

## Not Yet Supported In This Version

1. A rigorous lower-bound theorem deserving the phrase "quantum limit" in the strongest sense.
2. Task-level evidence on realistic benchmark networks.
3. Real device feasibility maps with detector efficiency and loss windows.

## Abstract V0

Photonic neural networks promise low-latency and energy-efficient information processing, but their practical scalability is constrained by the physical cost of nonlinear activation. We formulate a unified numerical framework for comparing activation mechanisms in photonic neural networks through an activation-cost viewpoint that tracks function-approximation error against optical resource budget. We implement proxy models for electronic, Kerr-like, saturable, photon-counting and adaptive quantum measurement activations within a common simulation scaffold. Preliminary scans show that measurement-induced activations can reproduce sigmoid-like responses at low photon budget, whereas binary-like responses remain substantially more expensive. These first results support the broader hypothesis that nonlinear activation should be treated as the dominant resource bottleneck in few-photon photonic inference. To reach journal-ready strength, the next stages will extend the framework to task-level energy-accuracy frontiers and detector-constrained device feasibility maps.

## Introduction Closing Paragraph V0

Here we study nonlinear activation as a photonic resource-allocation problem rather than as an isolated device function. Our aim is not to introduce yet another architecture-specific optical neural network, but to establish a comparative framework that asks how much optical resource is required to realize a target nonlinear response under realistic noise, loss and detection constraints. This framing lets us compare material, measurement-induced and hybrid activation mechanisms on a common footing and identify when quantum measurement becomes a useful nonlinear resource in the few-photon regime.

## Results Opening Paragraph V0

We first built a minimal comparative simulation environment containing five activation families: ideal electronic rectification, Kerr-like response, saturable response, threshold photon counting and adaptive quantum measurement activation. In the present version, these models are used as controlled proxies rather than full hardware-faithful device models. Even at this stage, the scan separates target-function classes. Kerr-like response best matches tanh-like targets in the current proxy study, whereas photon-counting and AQMA-like models achieve the strongest low-budget fits for sigmoid-like activation. This separation is important because it suggests that the relevant comparison is not "which activation is universally best" but "which physical nonlinearity reaches the desired response class with the lowest resource cost."
