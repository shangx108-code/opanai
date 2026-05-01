# Neural-operator formalism note: self-calibrating-diffractive-ncomms

## Purpose
Provide a supplement-ready formal bridge from the pilot observation model to the bounded task-level claim used in Figure 3 and the cross-domain reading of Figure 4.

## Formal setup
Let:
- `x in X`: object function or object-bearing optical field
- `theta in Theta`: latent degradation state, such as dynamic aberration coefficients
- `r in R`: known pilot/reference field
- `A_theta`: state-indexed optical propagation operator acting on `(x, r)`
- `M`: measurement map, typically intensity readout
- `y_r = M(A_theta(x, r))`: pilot-assisted measurement
- `y_0 = M(A_theta(x, 0))`: no-reference measurement
- `G_phi: Y -> Z`: downstream task operator, parameterized by `phi`
- `T(x, theta)`: target associated with the downstream task
- `L(z, z_target)`: downstream task loss

The bounded project claim is not that `y_r` uniquely determines `theta` or globally inverts the forward model. The claim is narrower: `y_r` can reveal more task-relevant information about the current `theta` than `y_0`, especially when the pilot co-propagates through the same realization.

## Local linearization
Around an operating point `(x_*, theta_*)`, write the Fréchet expansion

`y_r ~= y_{r,*} + J_x^{(r)} (x - x_*) + J_theta^{(r)} (theta - theta_*)`

and similarly for `y_0`. The common-path pilot is useful when the pilot-assisted Jacobian preserves or amplifies task-relevant sensitivity to `theta` in directions that are weak or aliased in the no-reference case.

## Fisher-information reading
For an observation likelihood `p(y | x, theta, r)`, define the Fisher information matrix in `theta`

`I_r(theta) = E[(nabla_theta log p(y | x, theta, r)) (nabla_theta log p(y | x, theta, r))^T]`

The current CRLB-style scan supports only the bounded statement that `I_r(theta)` is finite and often stronger than the no-reference counterpart over much of the explored region. This implies a smaller local covariance floor for estimating task-relevant degradation coordinates, but only under the usual regularity and local-identifiability assumptions.

## Task-level bridge
Let `z = G_phi(y)` and consider the loss `L(z, T(x, theta))`. Around `y_*`, linearize the task map:

`G_phi(y) ~= G_phi(y_*) + J_G (y - y_*)`

Then the local loss floor inherits the pilot benefit only through the composition of:
- the observation sensitivity to `theta`
- the posterior covariance in the observation space
- the Jacobian of the task operator

This is why the current theorem is local and task-dependent. A pilot can improve one downstream domain strongly while improving another only weakly if the latter is less aligned with the operator directions in which the pilot reduces uncertainty.

## Cross-domain interpretation
The current verified domains are:
- reconstruction
- classification residual
- inverse-design surrogate

These do not share the same output space, but they do share the same latent degradation family. The present Figure 4 evidence is therefore best read as a cross-domain demonstration of one mechanism, not as three unrelated benchmarks.

Current interpretation:
- reconstruction benefits most because it depends on preserving fine field information
- classification residual benefits modestly because the decision statistic compresses the observation
- inverse-design surrogate remains nearly neutral because its target is only weakly aligned with the pilot-revealed state coordinates in the current setup

## Claim boundary
- Verified: the current evidence supports a task-dependent local advantage interpretation
- Not verified: global invertibility, universal gains across all domains, or a full theorem that every diffractive neural operator with a pilot will self-calibrate
