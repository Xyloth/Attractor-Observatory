# Substance Audit W7 Swarm

Campaign: 008
Doctrine: D17.5
Measured simulation logic: 478 lines against a 500-line proxy floor

## v1.0 Section 3 components

- Agent-environment coupling: agents sense pheromone, food, damage, nest, target, and communication fields on a spatial grid.
- Collective coordination: pheromone trails, communication pulses, local memory, role switching, and consensus targeting are implemented as live dynamics.
- Task ecology: trail foraging, division of labour, collective repair, and consensus are separate parameterizations over the same agent mechanics.
- Controls: pheromone removal, randomized motion, and communication removal degrade the relevant benchmark rather than changing the success criterion.
- Invariants: agent counts, bounded fields, delivered food, repair state, role entropy, and consensus diagnostics are trace-exported.

## Implementation pointers

- `worlds/swarm/model.py:SwarmScenario` declares grid, agent, pheromone, communication, memory, sensor-noise, repair, and role-switch parameters.
- `SwarmWorld.step` coordinates sensing, role update, communication, movement, interaction, and field decay for every agent.
- `_sense`, `_update_role`, `_communicate`, `_move`, `_interact`, and `_decay_fields` are the substantive mechanism surface.
- `_swarm_diagnostics`, `_benchmark_success`, and `export_trace` expose delivered food, repair fraction, role entropy, consensus, dispersion, event types, and invariants.

## Behavior gate evidence

- W7 positive benchmarks cover `trail_foraging`, `division_of_labour`, `collective_repair`, and `consensus`.
- Controls require pheromone-enabled foraging to outperform random/no-pheromone motion and communication-enabled consensus to outperform no-communication dynamics.
- Campaign 008 requires all W7 positive traces and controls to pass, with at least five event types.

## Invariant evidence

- Trace state includes role counts, fields, food/damage outcomes, consensus, and bounded-grid diagnostics.
- The validation report requires positive W7 traces to have passed invariant checks.
- D14 lint reports zero benchmark-conditional state-writing violations for W7.

## Substance judgment

The 22-line shortfall is not evidence of a missing swarm component. The world has embodied agents, spatial fields, memory, communication, role allocation, task interaction, controls, and trace-backed invariants. The proxy floor should not force filler code.

Architect verdict: meets_spec_with_caveats

