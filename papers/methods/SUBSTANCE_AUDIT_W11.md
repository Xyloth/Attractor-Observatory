# Substance Audit W11 Quasispecies

Campaign: 008
Doctrine: D17.5
Measured simulation logic: 428 lines against a 500-line proxy floor

## v1.0 Section 3 components

- Finite population sequence space: genomes live in a bounded binary sequence space with explicit population size and sequence counts.
- Mutation operators: point mutation, insertion, and deletion are stochastic and repair sequence length to the declared active landscape.
- Fitness landscapes: master-sequence, near-neutral, rugged, flat-control, and shifted landscapes are selected by scenario parameters.
- Error threshold: mutation-rate scans estimate master-sequence loss and critical mutation behavior from the model.
- Neutral networks: near-neutral component coverage, neutral retention, drift distance, diversity, and effective population size are measured from live counts.
- Innovation fronts: mutation-graph connectivity, neutral percolation, escape probability, and innovation mass are measured from parent-child transitions.

## Implementation pointers

- `worlds/quasispecies/model.py:QuasispeciesScenario` declares mutation, indel, selection, neutral-radius, landscape, and shift parameters.
- `QuasispeciesWorld.step` performs weighted reproduction, stochastic mutation, selection, drift accounting, landscape shift, and trace recording.
- `_fitness`, `_mutate_stochastic`, `_effective_population_size`, `_neutral_component_seed`, `_neutral_component_coverage`, `_innovation_diagnostics`, and `_error_threshold_scan` implement the core world mechanics.
- `_cloud_diagnostics`, `_benchmark_success`, and `export_trace` expose sequence diversity, master fraction, mean fitness, neutral retention, scan rows, and invariants.

## Behavior gate evidence

- W11 positive benchmarks cover `error_threshold`, `neutral_networks`, and `evolvable_robustness`.
- Controls require mutation-enabled diversity to exceed no-mutation diversity and selected recovery to exceed flat-landscape recovery.
- Campaign 008 requires all W11 positive traces, controls, event types, and invariants to pass before W11R/W11C are green.

## Invariant evidence

- Trace exports include finite population size, sequence-space declaration, effective population size, neutral component coverage, and nonnegative sequence counts.
- The validation report requires every W11 positive trace invariant to pass.
- D14 lint reports zero benchmark-conditional state-writing violations for W11.

## Substance judgment

W11 is no longer a toy generator. It now contains finite-population quasispecies dynamics, stochastic mutation/indel operators, landscape variation, explicit error-threshold scans, neutral-network exploration, and mutation-graph innovation diagnostics. The line gap is a proxy mismatch, not a missing component list.

Architect verdict: meets_spec_with_caveats
