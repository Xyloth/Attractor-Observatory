# Substance Audit W13 Multiscale

Campaign: 008
Doctrine: D17.5
Measured simulation logic: 442 lines against an 800-line proxy floor

## v1.0 Section 3 components

- Real inner-world hosting: macro entities host live W1 CRN and W2 protocell worlds rather than scalar placeholders.
- Upscale operators: inner-world closure, boundary, mass, and division signals are projected into macro population/resource dynamics.
- Downscale operators: macro feedback alters inner host feed multipliers, selection weights, and hosted world state.
- Cross-scale flux events: upscale, downscale, intervention, and hosted-fragment events are written to the trace with affected host ids.
- Per-scale invariants: hosted world invariant residuals and cross-scale flux ledger are exported and checked.

## Implementation pointers

- `worlds/multiscale/model.py:InnerWorldHost` wraps hosted W1/W2 worlds with scale ratio, feed multiplier, selection weight, coarse observables, and invariant residuals.
- `MultiscaleWorld._init_inner_hosts` creates multiple CRN and protocell inner worlds from real scenarios.
- `step` advances hosted worlds, upscales their coarse observables, updates macro/micro fields, applies interventions, and downscales macro pressure back into the hosts.
- `_step_inner_worlds`, `_upscale_host`, `_upscale_population`, `_downscale_to_inner_worlds`, `_cross_scale_diagnostics`, and `export_trace` implement the cross-scale substrate.

## Behavior gate evidence

- W13 positive benchmarks cover `nested_closure`, `boundary_from_coarse`, `scale_separation`, and `downscale_intervention`.
- Controls require upscale events to disappear when upscale is disabled and downscale events to disappear when downscale is disabled.
- Campaign 008 requires all W13 positive traces, controls, event types, and invariants to pass before W13R/W13C are green.

## Invariant evidence

- Trace exports include hosted inner fragments, inner host summaries, cross-scale flux ledger rows, per-scale invariant checks, projection agreement, and boundary integrity.
- The validation report requires every W13 positive trace invariant to pass.
- D14 lint reports zero benchmark-conditional state-writing violations for W13.

## Substance judgment

W13 is below its deliberately aggressive 800-line proxy, but the actual missing part identified by TASK-019 was real inner-world coupling. That coupling is now implemented with hosted W1/W2 instances, upscale/downscale operators, cross-scale flux, and per-scale invariants. The world is claim-bearing for Campaign 008 substrate completion while remaining eligible for future extension.

Architect verdict: meets_spec_with_caveats

