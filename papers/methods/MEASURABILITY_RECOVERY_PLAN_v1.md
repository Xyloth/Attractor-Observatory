# Measurability Recovery Plan v1

> **DX-002 public runtime boundary:** References to `formalism/*`, `trace/*`, `worlds/*`, `motifs/*`, or `validation/*` in this document are narrative or private-runtime evidence unless a shipped public file is explicitly linked. The executable implementation is held outside the public branch; citations to private paths are governed by D29 and should be read as `evidence_private: true` / `private_unshipped`, not as public-runnable verification.


Task: TASK-MEAS-PLAN  
Author: Codex 1.5x  
Status: planning artifact; no implementation; no claim-bearing promotion  
Structure preregistration: `papers/prereg/task_meas_plan/MEASURABILITY_RECOVERY_PLAN_v1.structure.signed.json`

## Purpose

This plan is a per-cell measurability assessment for the 33 Campaign 024 BAD motif x lens cells. The goal is honest measurability, not a green matrix. A cell is recovered only when it can produce legitimate substrate-blocked evidence under D26 and D27. Cells that are diagnostic-only, domain-inapplicable, architecturally circular, or blocked on BFG formalism are declared that way.

This is not an implementation spec. Lens variants are named and source objects are specified, but no code is authorized by this artifact. This is not a recovery commitment. A recoverable class means "scientifically possible after the named source object and controls exist," not "must be implemented."

## Taxonomy

| Class | Definition | Disposition |
|---|---|---|
| REF-STRUCT | Dirty lens implementation can be rewritten over an already-present independent source object. | Ready for Round 2b implementation after ordinary controls. |
| NEW-ABST | Recovery requires a substantively new lens abstraction over a meaningful object not used by v1. | Implement only after source map and variant contract are signed. |
| SCHEMA-SPLIT | Recovery requires predicate evidence and lens evidence to be exposed as separate source objects or held-out folds. | Needs source corpus generation or trace schema change first. |
| BAD-ARCH | Predicate and lens necessarily read the same fundamental object/fields, so independent evidence is impossible. | Permanently excluded as evidence. |
| DOMAIN-DECLINE | Lens family is not applicable to the motif/substrate; honest decline is the correct behavior. | Permanently decline for this motif-lens cell. |
| DIAG-ONLY | Lens is scientifically useful as an internal diagnostic but cannot be independent substrate-blocked evidence. | Permanent diagnostic-only surface; never promotion evidence. |
| FORMALISM-REQ | Recovery needs upstream ontology/formalism before source objects can be safely declared. | Await Architect + PI formalism ratification. |
| NEEDS_PI_ARCHITECT_DECISION | Codex cannot force a scientifically defensible primary class. | Escalate with framing question before implementation. |

## Forced-Class Rule And Escalation

Every Campaign 024 BAD cell receives exactly one primary recovery class. Compound labels such as "SCHEMA-SPLIT or DOMAIN-DECLINE" are forbidden. If a cell cannot be classified without an ontology/theory decision, it is `NEEDS_PI_ARCHITECT_DECISION` and routes to PI + Architect. This plan uses zero `NEEDS_PI_ARCHITECT_DECISION` cells; floor connectivity was `FORMALISM-REQ` in v1 and is reclassified here after D31 ratified the BFG measurement split.

## D27 Ratified Language

D27 - Substantive Lens Recovery:

> A BAD motif-lens cell is not recovered by renaming a detector or moving the same computation behind a new interface. A recovered lens must demonstrate a substantive source-object split from the predicate, survive adversarial ablation, and resist matched-decoy controls. New names or slightly altered fields are not enough.

Applied operationally here:

- `source-object split`: recovered cells declare the minimum independent object required.
- `adversarial ablation survival`: every recovered cell must pass four-axis controls plus source-object holdouts.
- `matched-decoy resistance`: every recovered cell needs label-opposite decoys matched on generator family, trace length, source-object counts, and coarse numeric distributions.
- `DIAG-ONLY` and `DOMAIN-DECLINE` cells cannot enter substrate-blocked evidence even if they produce useful plots.

## Per-Cell Measurability Table

| cell_id | c024_status | primary_recovery_class | source_object_required | source_exists | lens_variant_proposed | d26_risk | required_decoys_and_ablations | next_action |
|---|---|---|---|---|---|---|---|---|
| motif.autocatalytic_closure.draft x graph | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, process_flags; no clean generic graph refactor exists without event/payload/process-flag surfaces in this corpus) | DIAG-ONLY | same_as_predicate_unrecoverable | no_unrecoverable | none | bad_self_match | four-axis controls if displayed; diagnostic-only source warning; no substrate-blocked use | permanent_diagnostic_only |
| motif.autocatalytic_closure.draft x crnt | BAD (mechanical_d26=BAD; nondeclined=15; failure_mode=clean source-object map overlaps predicate fields) | DIAG-ONLY | same_as_predicate_unrecoverable | no_unrecoverable | none | bad_self_match | four-axis controls if displayed; reaction-declaration self-match guard; no substrate-blocked use | permanent_diagnostic_only |
| motif.autocatalytic_closure.draft x petri | BAD (mechanical_d26=BAD; nondeclined=15; failure_mode=historical lens surface contains event, event_transition_proxy, process_flags; clean source-object map overlaps predicate fields) | DIAG-ONLY | same_as_predicate_unrecoverable | no_unrecoverable | none | bad_self_match | four-axis controls if displayed; reaction-incidence self-match guard; no substrate-blocked use | permanent_diagnostic_only |
| motif.repair.draft x graph | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, process_flags; no clean generic graph refactor exists without event/payload/process-flag surfaces in this corpus) | NEW-ABST | perturbation_response_ensemble | yes_task_source_obj_gen | graph.perturbation_response | partial_requires_ablation | four-axis controls; predicate/lens source-object holdouts; matched no-recovery, exogenous-reset, and no-damage decoys | ready_for_round_2c_implementation |
| motif.repair.draft x crnt | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains process_flags; clean refactor produced no nondeclined evaluations on this motif corpus) | DOMAIN-DECLINE | none_required | no_unrecoverable | none | n_a_decline | four-axis decline stability only; no reaction-source fabrication | permanent_decline |
| motif.repair.draft x dynamical_systems | BAD (mechanical_d26=PARTIAL; nondeclined=60; failure_mode=PARTIAL cell collapses under ablation because the clean lens has no source left after denying shared predicate object state) | SCHEMA-SPLIT | perturbation_response_ensemble | yes_task_source_obj_gen | dynamical_systems.behavioral_recovery | partial_requires_ablation | four-axis controls; deny predicate trajectory to lens; deny ensemble summary to predicate; matched recovery/no-recovery decoys | ready_for_round_2c_implementation |
| motif.repair.draft x topology | BAD (mechanical_d26=PARTIAL; nondeclined=60; failure_mode=PARTIAL cell collapses under ablation because the clean lens has no source left after denying shared predicate object state) | SCHEMA-SPLIT | perturbation_response_ensemble | yes_task_source_obj_gen | topology.recovery_basin | partial_requires_ablation | four-axis controls; source-object holdouts; matched basin-radius decoys with same perturbation magnitudes | ready_for_round_2c_implementation |
| motif.repair.draft x petri | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, event_transition_proxy, process_flags; clean refactor produced no nondeclined evaluations on this motif corpus) | DOMAIN-DECLINE | none_required | no_unrecoverable | none | n_a_decline | four-axis decline stability only; no transition-system fabrication | permanent_decline |
| motif.repair.draft x statistical_mechanics | BAD (mechanical_d26=PARTIAL; nondeclined=60; failure_mode=historical lens surface contains event, event_statistics, process_flags; PARTIAL cell collapses under ablation because the clean lens has no source left after denying shared predicate object state) | SCHEMA-SPLIT | perturbation_response_ensemble | yes_task_source_obj_gen | statistical_mechanics.recovery_time_distribution | partial_requires_ablation | four-axis controls; source-object holdouts; matched recovery-time/no-recovery distribution decoys | ready_for_round_2c_implementation |
| motif.repair.draft x control_theory | BAD (mechanical_d26=PARTIAL; nondeclined=60; failure_mode=historical lens surface contains control_or_memory_token, event, process_flags, token; PARTIAL cell collapses under ablation because the clean lens has no source left after denying shared predicate object state) | SCHEMA-SPLIT | perturbation_response_ensemble | yes_task_source_obj_gen | control_theory.recovery_response_model | partial_requires_ablation | four-axis controls; source-object holdouts; matched perturbation-response decoys; exogenous reset negative | ready_for_round_2c_implementation |
| motif.repair.draft x information | BAD (mechanical_d26=PARTIAL; nondeclined=60; failure_mode=historical lens surface contains event, event_entropy, event_information; PARTIAL cell collapses under ablation because the clean lens has no source left after denying shared predicate object state) | SCHEMA-SPLIT | perturbation_response_ensemble | yes_task_source_obj_gen | information.perturbation_restoration_channel | partial_requires_ablation | four-axis controls; source-object holdouts; matched information-flow decoys with same state entropy | ready_for_round_2c_implementation |
| motif.externalized_memory.draft x graph | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, process_flags, token; no clean generic graph refactor exists without event/payload/process-flag surfaces in this corpus) | NEW-ABST | external_channel_samples | yes_task_source_obj_gen_refresh | graph.external_channel | partial_requires_ablation | four-axis controls; time-window source holdout; external-noise and internal-recurrence matched decoys | ready_for_round_2c_implementation |
| motif.externalized_memory.draft x crnt | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=clean refactor produced no nondeclined evaluations on this motif corpus) | DOMAIN-DECLINE | none_required | no_unrecoverable | none | n_a_decline | four-axis decline stability only; no chemical-network fabrication | permanent_decline |
| motif.externalized_memory.draft x petri | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, event_transition_proxy; clean refactor produced no nondeclined evaluations on this motif corpus) | DOMAIN-DECLINE | none_required | no_unrecoverable | none | n_a_decline | four-axis decline stability only; no transition-system fabrication | permanent_decline |
| motif.replication_lineage.draft x graph | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, process_flags, token; no clean generic graph refactor exists without event/payload/process-flag surfaces in this corpus) | SCHEMA-SPLIT | entity_observations | yes_task_source_obj_gen | graph.phylogenetic_reconstruction | partial_requires_ablation | four-axis controls; declared-lineage/entity-observation holdouts; randomized-sequence and no-temporal-order decoys | ready_for_round_2c_implementation |
| motif.replication_lineage.draft x crnt | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=clean refactor produced no nondeclined evaluations on this motif corpus) | DOMAIN-DECLINE | none_required | no_unrecoverable | none | n_a_decline | four-axis decline stability only; no reaction-source fabrication | permanent_decline |
| motif.replication_lineage.draft x dynamical_systems | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event; clean refactor produced no nondeclined evaluations on this motif corpus) | SCHEMA-SPLIT | entity_observations | yes_task_source_obj_gen | dynamical_systems.population_frequency_trajectory | partial_requires_ablation | four-axis controls; lineage/entity source holdouts; growth-without-inheritance matched decoys | ready_for_round_2c_implementation |
| motif.replication_lineage.draft x topology | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=clean refactor produced no nondeclined evaluations on this motif corpus) | SCHEMA-SPLIT | entity_observations | yes_task_source_obj_gen | topology.tree_space_geometry | partial_requires_ablation | four-axis controls; declared-lineage blind reconstruction; randomized tree-space and no-parent decoys | ready_for_round_2c_implementation |
| motif.replication_lineage.draft x petri | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, event_transition_proxy, process_flags; clean refactor produced no nondeclined evaluations on this motif corpus) | DOMAIN-DECLINE | none_required | no_unrecoverable | none | n_a_decline | four-axis decline stability only; no reproduction-transition fabrication | permanent_decline |
| motif.replication_lineage.draft x statistical_mechanics | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, event_statistics, process_flags; clean refactor produced no nondeclined evaluations on this motif corpus) | SCHEMA-SPLIT | entity_observations | yes_task_source_obj_gen | statistical_mechanics.lineage_branching_distribution | partial_requires_ablation | four-axis controls; entity-observation holdout; matched population-size and branch-count decoys | ready_for_round_2c_implementation |
| motif.replication_lineage.draft x control_theory | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains control_or_memory_token, event, token; clean refactor produced no nondeclined evaluations on this motif corpus) | DOMAIN-DECLINE | none_required | no_unrecoverable | none | n_a_decline | four-axis decline stability only; no control-channel fabrication | permanent_decline |
| motif.replication_lineage.draft x information | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, event_entropy, event_information; clean refactor produced no nondeclined evaluations on this motif corpus) | SCHEMA-SPLIT | entity_observations | yes_task_source_obj_gen | information.heritable_information | partial_requires_ablation | four-axis controls; sequence/lineage source holdouts; randomized-sequence and similar-without-descent decoys | ready_for_round_2c_implementation |
| motif.self_maintained_boundary.draft x graph | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, process_flags, token; no clean generic graph refactor exists without event/payload/process-flag surfaces in this corpus) | NEW-ABST | boundary_region_samples | yes_task_source_obj_gen | graph.boundary_region | clean_after_recovery | four-axis controls; boundary-region source holdout; static-shell and randomized-adjacency decoys | ready_for_round_2c_implementation |
| motif.self_maintained_boundary.draft x crnt | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains process_flags; clean refactor produced no nondeclined evaluations on this motif corpus) | SCHEMA-SPLIT | boundary_maintenance_reaction_network | no_can_be_generated | crnt.boundary_maintenance_network | clean_after_recovery | four-axis controls; boundary-object/reaction-network holdouts; no-maintenance and external-reset decoys | awaiting_source_corpus_generation |
| motif.self_maintained_boundary.draft x petri | BAD (mechanical_d26=CLEAN; nondeclined=0; failure_mode=historical lens surface contains event, event_transition_proxy, process_flags; clean refactor produced no nondeclined evaluations on this motif corpus) | SCHEMA-SPLIT | boundary_maintenance_transition_system | no_can_be_generated | petri.boundary_maintenance_transitions | clean_after_recovery | four-axis controls; boundary-object/transition-system holdouts; no-maintenance and randomized-transition decoys | awaiting_source_corpus_generation |
| motif.floor_connectivity.draft x graph | BAD (C024 failure preserved; historical graph surface used event/proxy surfaces and no clean generic graph refactor existed before D31) | NEW-ABST | bfg_row_disjoint_trajectory_geometry | yes_campaign_026 | graph.basin_recovery_graph | clean_after_row_split | four-axis controls; D31 read-separation AST; predicate/lens row holdouts; randomized-equivalence and disconnected-floor decoys | ready_for_round_2c_implementation |
| motif.floor_connectivity.draft x crnt | BAD (C024 failure preserved; clean refactor produced no nondeclined evaluations and no reaction-network object exists at the basin-geometry layer) | DOMAIN-DECLINE | none_required | no_unrecoverable | none | n_a_decline | four-axis decline stability only; no reaction-network fabrication | permanent_decline |
| motif.floor_connectivity.draft x dynamical_systems | BAD (C024 failure preserved; clean refactor produced no nondeclined evaluations before D31 trajectory source object existed) | NEW-ABST | bfg_row_disjoint_trajectory_geometry | yes_campaign_026 | dynamical_systems.basin_return_dynamics | clean_after_row_split | four-axis controls; D31 read-separation AST; row-disjoint basin-return holdout; point-attractor and disconnected-graph decoys | ready_for_round_2c_implementation |
| motif.floor_connectivity.draft x topology | BAD (C024 failure preserved; clean refactor produced no nondeclined evaluations before D31 trajectory point cloud source object existed) | NEW-ABST | bfg_row_disjoint_trajectory_geometry | yes_campaign_026 | topology.basin_recovery_geometry | clean_after_row_split | four-axis controls; topology source holdout; randomized-equivalence decoys | ready_for_round_2c_implementation |
| motif.floor_connectivity.draft x petri | BAD (C024 failure preserved; historical Petri surface used event transition proxies) | NEW-ABST | bfg_row_disjoint_trajectory_geometry | yes_campaign_026 | petri.recovery_transition_net | clean_after_row_split | four-axis controls; transition-row holdout; matched transition-count decoys that do not read fiber labels | ready_for_round_2c_implementation |
| motif.floor_connectivity.draft x statistical_mechanics | BAD (C024 failure preserved; historical surface used event statistics and no clean recovery-time distribution source existed) | NEW-ABST | bfg_row_disjoint_trajectory_geometry | yes_campaign_026 | statistical_mechanics.recovery_time_distribution | partial_requires_ablation | four-axis controls; deny return_status; censored recovery-time decoys; same-connectivity/different-invariant decoys | ready_for_round_2c_implementation |
| motif.floor_connectivity.draft x control_theory | BAD (C024 failure preserved; historical surface used event/control tokens and no row-disjoint return-system source existed) | NEW-ABST | bfg_row_disjoint_trajectory_geometry | yes_campaign_026 | control_theory.return_controllability | clean_after_row_split | four-axis controls; reachability holdout; same-function/disconnected perturbation decoys | ready_for_round_2c_implementation |
| motif.floor_connectivity.draft x information | BAD (C024 failure preserved; historical surface used event entropy/information proxies) | NEW-ABST | bfg_row_disjoint_trajectory_geometry | yes_campaign_026 | information.recovery_information_flow | partial_requires_ablation | four-axis controls; deny perturbation_magnitude; randomized-equivalence information decoys | ready_for_round_2c_implementation |

## Per-Class Summary

- n_REF_STRUCT: 0. Cells: none.
- n_NEW_ABST: 10. Cells: motif.repair.draft x graph; motif.externalized_memory.draft x graph; motif.self_maintained_boundary.draft x graph; motif.floor_connectivity.draft x graph; motif.floor_connectivity.draft x dynamical_systems; motif.floor_connectivity.draft x topology; motif.floor_connectivity.draft x petri; motif.floor_connectivity.draft x statistical_mechanics; motif.floor_connectivity.draft x control_theory; motif.floor_connectivity.draft x information.
- n_SCHEMA_SPLIT: 12. Cells: motif.repair.draft x dynamical_systems; motif.repair.draft x topology; motif.repair.draft x statistical_mechanics; motif.repair.draft x control_theory; motif.repair.draft x information; motif.replication_lineage.draft x graph; motif.replication_lineage.draft x dynamical_systems; motif.replication_lineage.draft x topology; motif.replication_lineage.draft x statistical_mechanics; motif.replication_lineage.draft x information; motif.self_maintained_boundary.draft x crnt; motif.self_maintained_boundary.draft x petri.
- n_BAD_ARCH: 0. Cells: none.
- n_DOMAIN_DECLINE: 8. Cells: motif.repair.draft x crnt; motif.repair.draft x petri; motif.externalized_memory.draft x crnt; motif.externalized_memory.draft x petri; motif.replication_lineage.draft x crnt; motif.replication_lineage.draft x petri; motif.replication_lineage.draft x control_theory; motif.floor_connectivity.draft x crnt.
- n_DIAG_ONLY: 3. Cells: motif.autocatalytic_closure.draft x graph; motif.autocatalytic_closure.draft x crnt; motif.autocatalytic_closure.draft x petri.
- n_FORMALISM_REQ: 0. Cells: none. TASK-FLOOR-BFG / Campaign 026 ratified D31 and supplied the row-disjoint BFG source object.
- n_NEEDS_PI_ARCHITECT_DECISION: 0. Cells: none. Framing questions: none in v1; floor formalism is now ratified as D31.

## Source-Object Generation Campaigns Required

### perturbation_response_ensemble

Cells: motif.repair.draft x graph; motif.repair.draft x dynamical_systems; motif.repair.draft x topology; motif.repair.draft x statistical_mechanics; motif.repair.draft x control_theory; motif.repair.draft x information.

Minimum corpus contract: repeated perturbation trials with perturbation magnitude, pre-state summary, post-damage summary, recovery time, restoration fraction, failure class, and held-out predicate/lens folds. Predicate may read a signed recovery verdict or held-out trajectory. Lenses read the ensemble distribution. Required decoys: same perturbation with no endogenous recovery; exogenous reset; no-damage passive stability; matched trace length/state dimensionality.

Estimated scope: medium. Requires new perturbation campaign fixtures for protocell and swarm substrates, world-engine integration for repeated trials, trace schema export for ensemble rows, and decoy generators. This is one coherent Round 2b batch.

TASK-SOURCE-OBJ-GEN status: generated as `factory_lowlevel.adapters.PerturbationResponseEnsembleAdapter` with 120 accepted records across CRN, field, ecosystem, and quasispecies substrates plus 16 required decoys. Source exists is now `yes_task_source_obj_gen`; affected cells are ready for Round 2c implementation, not claim-bearing promotion.

### entity_observations

Cells: motif.replication_lineage.draft x graph; motif.replication_lineage.draft x dynamical_systems; motif.replication_lineage.draft x topology; motif.replication_lineage.draft x statistical_mechanics; motif.replication_lineage.draft x information.

Minimum corpus contract: declared lineage ledger separated from entity observations. Entity observations include entity_id, birth_time, phenotype vector, genotype/sequence where available, boundary marker, and time ordering. Lens reconstructs or measures descent while blinded to declared parent/child edges. Required decoys: declared edges with randomized sequences; similar sequences without temporal parentage; growth without heritable descent; matched population size/branch count.

Estimated scope: medium-high. Requires trace schema extension and at least one substrate with independent entity/sequence observations. Protocell can generate entity observations; quasispecies/digital would be stronger if available in this batch.

TASK-SOURCE-OBJ-GEN status: generated as `factory_lowlevel.adapters.EntityObservationsAdapter` with 120 accepted records across quasispecies, symbiogenesis, digital, and morphogenesis substrates plus 12 required decoys. Source exists is now `yes_task_source_obj_gen`; affected cells are ready for Round 2c implementation, not claim-bearing promotion.

### external_channel_samples

Cells: motif.externalized_memory.draft x graph.

Minimum corpus contract: external medium samples and internal readback samples separated by time-window holdout. Predicate tests causal removal/scramble effect. Lens reads lagged dependence/channel graph over held-out windows. Required decoys: internal recurrence with no external channel; external noise channel with matched entropy; renamed channel keys/payloads.

Estimated scope: small. Current cognitive traces already contain attention shadow and kernel prediction histories; Round 2b can likely construct the source object from existing corpus plus decoys.

TASK-SOURCE-OBJ-GEN status: refreshed as `factory_lowlevel.adapters.ExternalChannelSamplesAdapter` with 120 accepted records across swarm, morphogenesis, cognitive, and digital substrates plus 12 required decoys. Source exists is now `yes_task_source_obj_gen_refresh`; the graph external-channel cell is ready for Round 2c implementation under the same no-promotion rule.

### boundary_region_samples

Cells: motif.self_maintained_boundary.draft x graph.

Minimum corpus contract: boundary region adjacency/exchange samples independent from boundary predicate fields. Predicate reads operational persistence and internal maintenance. Lens reads region graph, exchange adjacency, or compartment topology. Required decoys: static closed shell, external reset shell, randomized adjacency with same boundary count.

Estimated scope: medium. Requires region/adjacency export from protocell or W2-style boundary traces; may be generated from existing world internals if spatial compartment state exists.

TASK-SOURCE-OBJ-GEN status: generated as `factory_lowlevel.adapters.BoundaryRegionSamplesAdapter` with 90 accepted records across protocell, morphogenesis, and field substrates plus 9 required decoys. Source exists is now `yes_task_source_obj_gen`; the graph boundary-region cell is ready for Round 2c implementation. CRNT/Petri boundary-maintenance source objects remain awaiting their separate reaction-network and transition-system corpora.

### boundary_maintenance_reaction_network

Cells: motif.self_maintained_boundary.draft x crnt.

Minimum corpus contract: explicit reaction declarations for boundary-material production/maintenance, separate from boundary object fields. Required decoys: boundary present without maintenance reactions; external reset; reaction network with same counts but no boundary-material production.

Estimated scope: medium. Requires either adding explicit maintenance chemistry to protocell traces or sourcing a W2 chemistry substrate. Do not synthesize fake reaction declarations from boundary state after the fact.

### boundary_maintenance_transition_system

Cells: motif.self_maintained_boundary.draft x petri.

Minimum corpus contract: explicit transition system for boundary maintenance, separate from boundary object fields. Required decoys: transition count matched but no maintenance path; external reset; randomized transition incidence preserving place/transition counts.

Estimated scope: medium. Could be paired with the boundary maintenance chemistry campaign if transition declarations are emitted from the same source process.

### heldout_perturbation_fiber_graph

Cells: seven motif.floor_connectivity.draft cells now source-enabled by D31 / Campaign 026. CRNT permanently domain-declines.

Minimum corpus contract: D31 requires a signed predicate-side `outcome_summary`, row-disjoint lens-side `trajectory_geometry`, grouped-stratified validation holdout, AST-enforced read separation, and unit-level substrate-blocked shuffle. Required decoys: point-attractor/implementation-unique falsifier; same function similarity but disconnected perturbation graph; same connectivity score but invariant not preserved; randomized equivalence assignments preserving class sizes.

TASK-FLOOR-BFG status: generated as Campaign 026 with D31 trace schema, locked preprocessing classifier, seven non-CRNT floor lens outcomes (five straightforward NEW-ABST variants plus two explicitly risky variants; CRNT domain-declines), grouped-stratified perturbation corpus, and unit-level substrate-blocked controls. Source exists is now `yes_campaign_026`; floor cells are ready for Round 2c interpretation only, not claim-bearing promotion.

## Round 2b/2c Sequencing Recommendation

1. TASK-SOURCE-OBJ-GEN completed the four non-floor source-object corpora in this plan: `external_channel_samples`, `perturbation_response_ensemble`, `entity_observations`, and `boundary_region_samples`.
2. Round 2c implementation can now target 20 cells: six repair cells, five replication-lineage cells, one externalized-memory graph cell, one self-maintained-boundary graph cell, and seven floor-connectivity cells from Campaign 026.
3. Run boundary maintenance source campaigns separately: `boundary_maintenance_reaction_network` and `boundary_maintenance_transition_system` remain awaiting source-corpus generation.
4. Preserve this ordering for implementation: external-channel graph first as the cheapest sanity check, then repair, then lineage, then boundary-region graph.
5. Document permanent non-evidence cells now: autocatalytic closure graph/CRNT/Petri as DIAG-ONLY; eight DOMAIN-DECLINE cells as honest declines.
6. Floor connectivity formalism is now ratified as D31. Round 2c can include Campaign 026 floor cells, with CRNT documented as permanent DOMAIN-DECLINE.

Immediate implementation candidates if PI approves Round 2c: 20 cells. They are source-enabled only; none is claim-bearing until the corresponding lens implementation passes D26/D27/D31 controls and decoy ablations.

Cells PI/Architect must decide under `NEEDS_PI_ARCHITECT_DECISION`: 0. Cells PI/Architect must handle as formalism work: 0; D31 closed the floor formalism prerequisite.

Honest measurability count over the 33 Campaign 024 BAD cells:

- Legitimate substrate-blocked evidence after recovery, if planned source campaigns succeed: 22 cells; TASK-SOURCE-OBJ-GEN source-enabled 13 non-floor cells and TASK-FLOOR-BFG source-enabled 7 floor cells.
- Permanently not evidence: 11 cells (3 DIAG-ONLY + 8 DOMAIN-DECLINE).
- Formalism-pending, not measurable yet: 0 cells.
- Ready for Round 2c implementation after TASK-SOURCE-OBJ-GEN and TASK-FLOOR-BFG: 20 of the 22 recoverable cells. The remaining two need boundary-maintenance reaction-network and transition-system corpora.

If combined with the 15 Campaign 024 CLEAN cells, the best near-term matrix after non-floor recovery plus D31 floor recovery is 37 evidence-capable cells out of 48, 11 permanent non-evidence cells, and 0 floor cells awaiting formalism.

## Acceptance Gate Checklist

- All 33 Campaign 024 BAD cells classified exactly once: yes.
- No compound primary classes: yes.
- All source_object_required values are concrete: yes.
- D27 ratified language applied: yes.
- floor_connectivity x all 8 reclassified after D31: seven source-enabled evidence-capable cells plus CRNT DOMAIN-DECLINE.
- autocatalytic_closure x graph/CRNT/Petri classified DIAG-ONLY with `permanent_diagnostic_only`: yes.
- No implementation performed in the original TASK-MEAS-PLAN artifact; TASK-FLOOR-BFG later implemented the D31 floor formalism and this plan now records that update.

