# Substance Audit W6 Ecosystem

Campaign: 008
Doctrine: D17.5
Measured simulation logic: 484 lines against a 500-line proxy floor

## v1.0 Section 3 components

- Multi-trophic patch population dynamics: producers, grazers, predators, decomposers, and regenerating abiotic resource are updated in every patch.
- Spatial coupling: dispersal and interaction-radius pressure couple neighboring patches without benchmark-specific state writing.
- Ecological transitions: Lotka-Volterra cycling, May-style interaction instability, Allee collapse, and shock-driven regime shift are represented as parameterized scenarios.
- Perturbation response: external shock and recovery are explicit dynamics; disabling them is the control path.
- Invariants: nonnegative populations/resources, bounded open budget, and diagnostic regime metrics are exported in the trace.

## Implementation pointers

- `worlds/ecosystem/model.py:EcosystemScenario` declares all scenario parameters, including interaction strength, dispersal, Allee terms, shock schedule, and control toggles.
- `EcosystemWorld.step` integrates growth, grazing, predation, mortality, decomposition, disturbance, dispersal, and patch-level interaction pressure.
- `_interaction_pressure`, `_apply_shock`, and `_disperse` implement the cross-patch mechanics required by the world specification.
- `_ecosystem_diagnostics`, `_benchmark_success`, and `export_trace` expose oscillation strength, spectral radius, collapse depth, hysteresis area, trace events, and invariant checks.

## Behavior gate evidence

- W6 positive benchmarks cover `lotka_volterra`, `may_stability`, `allee_collapse`, and `regime_shift`.
- Causal controls compare active shock against no-shock dynamics and active interaction matrix against flattened interactions.
- Campaign 008 report requires all positive benchmarks to pass, all controls to exceed threshold, at least five event types, and passed invariants before W6R/W6C can be green.

## Invariant evidence

- Trace exports include nonnegative population/resource checks and open-budget residuals.
- The validation report requires every positive W6 trace to report `invariants_passed = true`.
- D14 lint reports zero benchmark-conditional state-writing violations for W6.

## Substance judgment

The 16-line gap is below the proxy floor and does not identify a missing v1.0 component. The implemented world is already a multi-trophic, spatial, perturbable ecosystem with controls and invariants. Adding 16 lines would be weaker evidence than this component audit.

Architect verdict: meets_spec_with_caveats

