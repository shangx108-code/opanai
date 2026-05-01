# Kernel-alpha collapse figure spec v1

## Purpose

This figure is the PRL-critical validation figure for the current project line.
Its job is not to show that the proxy kernel produces some structure. Its job is
to show that the decisive observable either does or does not collapse when the
kernel is made phase-blind, and that the surviving non-collapse is explicitly
locked to interface orientation `\alpha`.

In one sentence, the figure must answer:

**Does the candidate-discriminating signal survive as an `\alpha`-structured
kernel response, or does it collapse to an orientation-blind curve once the
phase-sensitive part of the kernel is removed?**

## PRL decision criterion

The figure is a success only if it makes the following contrast visually hard to
argue with:

- the phase-sensitive branch retains a nontrivial `\alpha` dependence after
  normalization or recentering;
- the phase-blind or ordinary control branch collapses onto a single master
  curve under the same plotting rule;
- this contrast persists in a compact observable such as peak position, peak
  splitting, or excess-conductance trace shape.

If both branches collapse equally well, the PRL exclusion claim is weak.
If neither branch collapses, the figure is noisy rather than decisive.

## What “collapse” means here

For this project, “collapse” should not mean generic rescaling for aesthetics.
It should mean the following strict operational test:

1. Choose one observable extracted from the conductance kernel for each
   interface orientation `\alpha`.
2. Recenter or normalize only by a rule that is physically defensible and
   applied to every branch in the same way.
3. Plot the observable for multiple `\alpha` values on the same axes.
4. Ask whether the control branch becomes nearly `\alpha`-independent, while
   the phase-sensitive branch remains visibly separated or drifted.

The figure therefore compares **collapse quality** rather than only raw
amplitude.

## Recommended observable

Use **finite-bias peak position and peak splitting extracted from the kernel**
as the primary collapse observable.

Reason:

- zero-bias height alone is too easy to mimic by broadening;
- peak position drift is more tightly tied to phase-sensitive structure;
- peak splitting is the cleanest candidate for showing genuine `\alpha`-locked
  response rather than generic barrier renormalization.

Preferred definitions:

- `V_peak^+(\alpha)`: positive-bias peak position after background subtraction.
- `V_peak^-(\alpha)`: negative-bias peak position after background subtraction.
- `\Delta V_{\rm split}(\alpha)=V_peak^+(\alpha)-V_peak^-(\alpha)`.
- optional reduced observable:
  `\delta V_{\rm split}(\alpha)=\Delta V_{\rm split}(\alpha)-\overline{\Delta V_{\rm split}}`.

## Figure layout

Use a compact 4-panel PRL layout.

### Panel A: Raw kernel traces

- Plot three to five conductance traces from the phase-sensitive branch for
  different `\alpha` at fixed `Z`, `\eta`, and `\phi`.
- Use the chiral-like branch or the branch expected to survive the kernel test.
- Goal: show that the raw line shape visibly moves with `\alpha`.

### Panel B: Control-kernel traces

- Plot the matched control or ordinary branch on the same bias axis and the same
  extraction rule.
- Same `Z`, `\eta`, `\phi`, and same chosen set of `\alpha`.
- Goal: show that the control traces nearly sit on top of each other or differ
  only by trivial amplitude shifts.

### Panel C: Collapse metric

- Plot reduced or normalized curves after the agreed recentering rule.
- The control branch should collapse onto a master curve.
- The phase-sensitive branch should fail to collapse, or collapse only after an
  unphysical ad hoc shift.
- This is the “one look” panel.

Recommended y-axis:

- `G(V)-G_{\rm bg}` or normalized excess conductance.

Recommended x-axis:

- `V-\bar V_{\rm peak}` for each trace if the goal is to show shape collapse;
  otherwise use raw `V` if the main signal is peak drift itself.

### Panel D: Quantified alpha-locking

- Scatter or line plot of `V_peak^+(\alpha)` and/or `\Delta V_{\rm split}(\alpha)`.
- Put phase-sensitive and control branches on the same axes.
- Goal: one branch shows measurable `\alpha` drift or splitting modulation, the
  control stays flat within tolerance.

This panel is the quantitative anchor that prevents the figure from being
dismissed as curve-eye-balling.

## The winning visual contrast

The strongest version of the figure is:

- control branch: raw curves already similar, reduced curves collapse tightly,
  `\Delta V_{\rm split}(\alpha)` nearly flat;
- unconventional branch: raw curves drift with `\alpha`, reduced curves do not
  collapse onto one master line, and `\Delta V_{\rm split}(\alpha)` varies
  systematically with `\alpha`.

That is the exact contrast the referee should remember.

## Minimum data package required

To build this figure cleanly, the project needs the following tables saved in
the long-term space:

- one curve table for the phase-sensitive branch across a fixed
  `(\eta, Z, \phi)` slice and multiple `\alpha`;
- one matched curve table for the control branch across the same slice;
- one extracted-feature table containing
  `candidate, eta, Z, phi, alpha, V_peak^+, V_peak^-, \Delta V_split, G(0), G_bg`;
- one collapse-quality table with a scalar mismatch measure, for example RMS
  deviation from the branch-wise master curve.

## Current project status against this spec

What is already available now:

- a minimal candidate-resolved conductance proxy;
- figure-ready best-slice traces for `s_wave`, `s_pm`, and `chiral`;
- a first sign that the chiral branch develops finite-bias structure while the
  `s_pm` branch favors a zero-bias enhancement.

What is still missing for the actual kernel-alpha collapse figure:

- a fixed-slice scan over multiple `\alpha` values for the same branch with the
  same `Z`, `\eta`, and `\phi`;
- an explicit phase-blind control branch evaluated under the same extraction
  rule;
- a collapse-quality metric rather than only representative best traces.

So the present WP3 files are **not yet the collapse figure itself**. They are
the correct staging ground for it.

## Recommended next executable task

Build a dedicated dataset with:

- branch 1: phase-sensitive kernel slice, likely the chiral branch;
- branch 2: phase-blind control slice;
- fixed `Z`, fixed `\eta`, fixed `\phi`;
- sweep only `\alpha`;
- save both raw conductance traces and extracted
  `V_peak^\pm(\alpha), \Delta V_{\rm split}(\alpha)`.

If only one next coding action is allowed, do that before any new manuscript
polish.

## Caption skeleton

**Kernel-alpha collapse test for phase-sensitive discrimination.**
Panels A and B compare conductance traces generated from the phase-sensitive and
phase-blind kernels on the same `\alpha` slice set at fixed `Z`, `\eta`, and
`\phi`. Panel C shows the corresponding reduced traces after the common
collapse-normalization rule. The control branch collapses onto an
orientation-independent master curve, whereas the phase-sensitive branch
retains a systematic `\alpha`-locked deviation. Panel D quantifies this contrast
through the extracted peak positions and peak splitting
`\Delta V_{\rm split}(\alpha)`, demonstrating that the surviving branch carries
genuine interface-orientation information rather than a trivial broadening
effect.
