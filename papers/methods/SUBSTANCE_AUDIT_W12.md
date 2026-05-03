# Substance Audit W12 Symbiogenesis

Campaign: 008
Doctrine: D17.5
Measured simulation logic: 407 lines against a 600-line proxy floor

## v1.0 Section 3 components

- Two-level protocells: outer protocells host multiple subcells, and each subcell hosts a real inner CRN instance.
- Resource exchange: role-specific subcells exchange resources and products through live exchange channels.
- Vertical inheritance: outer protocell division partitions inherited subcells into daughters and records lineage.
- Horizontal exchange: subcells can move between outer protocells through explicit exchange events.
- Symbiotic outcomes: stable mutualism, cheater takeover, and eukaryogenesis-like fixation emerge from exchange, enforcement, inheritance, and integration parameters.

## Implementation pointers

- `worlds/symbiogenesis/model.py:NestedSubcell` and `OuterProtocell` define the nested biological structure.
- `SymbiogenesisWorld._init_outer_cells` creates outer protocells with producer, consumer, repairer, and cheater subcell roles backed by CRN worlds.
- `step` combines nested protocell dynamics with host/symbiont exchange, enforcement, cheating, integration, and inheritance.
- `_step_nested_protocells`, `_vertical_partition`, `_horizontal_exchange`, `_nested_summary`, and `export_trace` expose the nested mechanisms and lineage.

## Behavior gate evidence

- W12 positive benchmarks cover `stable_mutualism`, `cheater_takeover`, and `eukaryogenesis_fixation`.
- Controls require exchange-enabled mutualism to exceed no-exchange dynamics and inheritance-enabled fixation to exceed no-inheritance dynamics.
- Campaign 008 requires the W12 positive traces, controls, event surface, and invariants to pass.

## Invariant evidence

- Trace exports include outer cells, nested lineage, exchange channels, nested sub-CRN invariants, and open-budget boundedness.
- The validation report requires every positive W12 trace invariant to pass.
- D14 lint reports zero benchmark-conditional state-writing violations for W12.

## Substance judgment

W12 now matches the intended nested symbiogenesis structure: outer protocells, hosted sub-CRNs, resource exchange, vertical inheritance, horizontal exchange, cheaters, enforcement, and lineage. The remaining proxy-line gap does not identify a missing mechanistic requirement.

Architect verdict: meets_spec_with_caveats

