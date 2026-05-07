# Factory Adapter Payload Contract

Status: Phase-B canonical contract. Mode: exploratory, source-bound.

This contract closes the CB-016 W0/W1 routing incident class: adapters and routers must agree on where simulation parameters live before records enter world construction.

## Canonical Direction

Codex chooses direction **B** as the forward contract: simulation parameters live under `EmpiricalRecord.payload.world_parameters` for all parameterized worlds. Descriptive source fields may remain top-level in `payload`, but router-gated simulation fields are read from `world_parameters`.

Rationale: all W1-W13 world constructors already consume `payload.world_parameters`; duplicating simulation fields at top level would create two mutable contracts and make schema drift harder to detect. W0 math primitives are the exception: the world consumes the full source record list through `records_as_params=True`, so no `world_parameters` namespace is required.

## Global Requirements

Every adapter record must provide:

- `record_id`, `source_id`, `world_family`, `record_type`, `canonical_name`
- `payload` with source-derived fields only
- `provenance.source_url`
- `provenance.retrieval_timestamp`
- `provenance.parser_version`
- `provenance.authority`
- `provenance.raw_exported`
- `license_class`
- `payload.methodology_review_required: true` for Phase-1 exploratory records

`world_parameters` is reserved for deterministic world-constructor inputs. It must not contain claim-bearing labels, motif verdicts, or lens outputs.

## Per-World Contract

| World | Accepted record_type | Router-required top-level payload field | Required `world_parameters` fields | Optional world-consumed fields |
|---|---|---|---|---|
| W-1 `atomic_molecular_primitives` | `atomic_energy_level_summary`, `small_molecule_topology_summary` | source summary fields; no `world_parameters` required | none | energy levels, topology proxies, element/molecule descriptors |
| W0 `math_primitives` | `canonical_dynamical_form` | `primitive_class`, `dimension`, `state_equation`, `parameters`, `expected_stable_form` | none | DOI/citation descriptors, recurrence/attractor metadata |
| W1 `crn` | `kegg_metabolic_network_summary` | `world_parameters` | `initial_state`, `reactions` | `steps`, `dt`, backend hints, source undertermination notes |
| W2 `protocell` | `liposome_protocell_benchmark` | `world_parameters` | `scenario_id` or `benchmark` | boundary/internal resource parameters, repair/division rates |
| W3 `field` | `reaction_diffusion_benchmark` | `world_parameters` | `benchmark` | parameter ranges, `steps`, export cadence |
| W4 `morphogenesis` | `flybase_morphogen_profile` | `world_parameters` | `scenario_id` or `benchmark` | morphogen profiles, mutation/pulse schedule fields |
| W5 `digital` | `avida_executable_genome_trace` | `world_parameters` | `scenario_id` or `benchmark` | mutation rates, reward schedules, parasite/task metadata |
| W6 `ecosystem` | `gbif_ecosystem_occurrence_summary` | `world_parameters` | `benchmark`, `initial_producers`, `initial_grazers`, `initial_predators` | decomposers, resource, interaction strength/radius, patch count |
| W7 `swarm` | `movebank_swarm_behavior_summary` | `world_parameters` | `scenario_id` or `benchmark` | agent count, behavior/source cut metadata |
| W8 `cognitive` | `allen_brain_cognitive_dataset` | `world_parameters` | `scenario_id` or `benchmark` | attention, noise, learning/control parameters |
| W9 `origins_chemistry` | `prebiotic_chemistry_benchmark` | `world_parameters` | `benchmark` | surface/gradient/polymerization rates, steps |
| W10 `hypergraph_reactions` | `biomodels_reaction_hypergraph` | `world_parameters` | `scenario_id` or `benchmark` | initial state, hyperedge parameters, backend hints |
| W11 `quasispecies` | `ncbi_hiv1_sequence_pilot` | `world_parameters` | `master_sequence`, `mutation_rate` | population size, insertion/deletion rates, landscape metadata |
| W12 `symbiogenesis` | `ncbi_endosymbiosis_genome_summary` | `world_parameters` | `scenario_id` or `benchmark` | host/symbiont coupling and dependency parameters |
| W13 `multiscale` | `physiome_multiscale_model` | `world_parameters` | `scenario_id` or `benchmark` | scale coupling, time-scale separation, nested-system parameters |

## Validation Pattern

Routing-time validation is intentionally shallow:

1. Verify `record.world_family` equals the selected target world.
2. Verify `record.record_type` is accepted by that world.
3. For parameterized worlds, verify `payload.world_parameters` is a dictionary.
4. Verify only the minimum constructor-critical keys listed above.

World construction performs deeper semantic validation and returns structured rejections. Rejections become audit items; records are not silently dropped.

## Incident Binding

CB-016 W0/W1 orphan records are resolved by treating `world_parameters` as canonical for W1 CRN and by documenting W0 as record-list driven. Future adapters must target this contract before daemon launch.
