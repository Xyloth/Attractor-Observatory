# Substance Audit W9 Origins Chemistry

Campaign: 008
Doctrine: D17.5
Measured simulation logic: 404 lines against a 500-line proxy floor

## v1.0 Section 3 components

- Surface chemistry: pore surfaces adsorb solution species, desorb products, and catalyze closure-supporting reactions under finite surface capacity.
- Transport limitation: pore-to-pore diffusion and optional fully mixed controls expose transport-limited closure behavior.
- Energy gradients: declared gradients drive anchored protocell-like boundary polymerization.
- Mineral and wet-dry chemistry: mineral weathering, wet-dry concentration, template memory, redox buffers, vesicle seeds, and protected microenvironments are active pore-level dynamics.
- Scenarios: surface-stabilized closure, transport-limited closure, and gradient-anchored protocell are parameter variations over one mechanistic pore network.
- Invariants: total material budget, surface capacity, nonnegative concentrations, gradient span, and closure diagnostics are exported.

## Implementation pointers

- `worlds/origins_chemistry/model.py:OriginsScenario` declares pore count, solution pools, surface capacity, adsorption/desorption rates, catalysis, diffusion, gradient strength, and control toggles.
- `OriginsChemistryWorld.step` updates mineral weathering, wet-dry concentration, adsorption, catalytic conversion, template feedback, redox buffering, desorption, boundary polymerization, vesicle seeding, boundary repair, and pore diffusion.
- `_wet_dry_factor`, `_mineral_weathering`, `_surface_template_feedback`, `_boundary_repair`, `_microenvironment_diagnostics`, `_diffuse`, `_mass`, `_pore_network_diagnostics`, `_benchmark_success`, and `export_trace` cover the substantive transport, budget, diagnostic, and trace surfaces.
- The controls toggle surface effects and energy-gradient effects without injecting benchmark-specific answers.

## Behavior gate evidence

- W9 positive benchmarks cover `surface_stabilized_closure`, `transport_limited_closure`, and `gradient_anchored_protocell`.
- Controls require surface catalysis to increase closure and energy gradients to increase boundary/gradient signal.
- Campaign 008 requires all W9 benchmarks, controls, event types, and invariants to pass before W9R/W9C are green.

## Invariant evidence

- Positive traces expose mass/budget residuals, concentration nonnegativity, surface occupancy, gradient span, and closure score.
- The validation report requires W9 positive trace invariants to pass.
- D14 lint reports zero benchmark-conditional state-writing violations for W9.

## Substance judgment

W9 is compact because the pore-network chemistry is expressed directly. It covers the origins-chemistry purpose of surface stabilization, transport limitation, gradient anchoring, mineral wet-dry chemistry, protected template memory, and protocell-like boundary persistence with controls. The remaining proxy-line gap does not correspond to a known missing v1.0 component.

Architect verdict: meets_spec_with_caveats
