"""Locked MotifContract.v2 registry used by TASK-MOTIF-IMPL."""

from __future__ import annotations

from typing import Any

from .schema import LensContract, MotifContractV2, SourceObjectEntry


def som(source_object: str, type_: str, fields: list[str]) -> SourceObjectEntry:
    return SourceObjectEntry(source_object, type_, tuple(fields))


LENS_SOURCE_MAPS = {
    "graph": (
        som("events", "event_graph", ["type", "payload.actor_ids", "payload.parent_child_ids"]),
        som("state", "numeric_state_snapshot", ["state_key_presence", "trajectory_shape"]),
    ),
    "crnt": (
        som("parameter_record.reactions", "reaction_network", ["reactants", "products", "stoichiometric_rank"]),
        som("state", "numeric_state_snapshot", ["species_persistence"]),
    ),
    "dynamical_systems": (
        som("state", "numeric_state_snapshot", ["trajectory_shape", "terminal_drift", "recurrence"]),
    ),
    "topology": (
        som("state", "point_cloud", ["filtration_geometry", "connectivity_proxy"]),
    ),
    "petri": (
        som("parameter_record.reactions", "reaction_or_transition_network", ["reactants", "products", "incidence_rank"]),
        som("events", "event_transition_proxy", ["type"]),
        som("state", "numeric_state_snapshot", ["place_count"]),
    ),
    "statistical_mechanics": (
        som("events", "event_statistics", ["type", "rare_event_rate"]),
        som("state", "numeric_state_snapshot", ["energy_variance", "large_deviation_proxy"]),
    ),
    "control_theory": (
        som("events", "control_channel_proxy", ["type", "control_or_memory_token"]),
        som("state", "numeric_state_snapshot", ["observability_rank", "delta_rank"]),
    ),
    "information": (
        som("events", "event_information", ["type", "event_entropy"]),
        som("state", "numeric_state_snapshot", ["predictive_state_count", "delta_entropy"]),
    ),
}


def lens(lens_id: str, features: list[str], justification: str) -> LensContract:
    return LensContract(lens_id, tuple(features), LENS_SOURCE_MAPS[lens_id], justification)


COMMON_INVARIANCE = (
    "event_token_rename leaves predicate verdict unchanged",
    "state_key_rename leaves predicate verdict unchanged",
    "payload_key_rename leaves predicate verdict unchanged",
    "generator_id_erasure leaves predicate verdict unchanged",
    "metadata_identity_erasure leaves predicate verdict unchanged",
    "value_label_erasure leaves predicate verdict unchanged",
)

COMMON_PROMOTION_BLOCK = (
    "mode_tag remains exploratory in this campaign",
    "adversarial controls must pass",
    "D26 source-object-map audit must have no BAD primary evidence path",
    "Destroyer pass-2 required before any claim-bearing promotion",
)


def epi(world_family: str, instances: list[str], citations: list[str], mapping_status: str = "source_bound") -> dict[str, Any]:
    return {
        "world_family": world_family,
        "instances": instances,
        "citations": citations,
        "mapping_status": mapping_status,
        "substance_audit_signed": False,
    }


CONTRACTS: dict[str, MotifContractV2] = {
    "motif.autocatalytic_closure.draft": MotifContractV2(
        motif_id="motif.autocatalytic_closure.draft",
        semantic_definition="A declared reaction system contains a nonempty closed catalytic subset reachable from a declared food set under the Hordijk-Steel RAF/maxRAF criterion.",
        allowed_evidence=("parameter_record.food_set", "parameter_record.reactions.reactants", "parameter_record.reactions.products", "parameter_record.reactions.catalysts"),
        forbidden_evidence=("event types reaction_event/closure_event/surface_catalysis_event", "process_flags.closure", "scenario_id or benchmark strings", "expected_closure fields"),
        predicate_abstraction_layer="set-theoretic reaction-graph closure on declared reactions",
        predicate_source_object_map=(
            som("parameter_record.reactions", "reaction_declaration", ["reactants", "products", "catalysts"]),
            som("parameter_record.food_set", "food_set", ["species_ids"]),
        ),
        lens_abstraction_layer=(
            lens("graph", ["cycle_proxy", "branching_proxy", "process_flags.closure"], "CLEAN against the RAF predicate source objects, but process_flags remain an adversarial lens risk."),
            lens("crnt", ["reaction_count", "t_invariant_proxy", "persistence_indicator"], "BAD for predicate independence because it reads the same reaction declarations used by maxRAF."),
            lens("dynamical_systems", ["recurrence_rate", "stability", "process_flags.closure"], "CLEAN source objects but not a proof of RAF closure."),
            lens("topology", ["long_h1_cycles", "process_flags.closure"], "CLEAN source objects, exploratory only."),
            lens("petri", ["t_invariant_count", "transition_count", "process_flags.closure"], "BAD for direct overlap with reaction incidence objects."),
            lens("statistical_mechanics", ["large_deviation_rate", "energy_variance"], "CLEAN but weakly diagnostic."),
            lens("control_theory", ["controllability_proxy", "observability_proxy"], "Out-of-domain for native RAFs; retained for audit completeness."),
            lens("information", ["event_entropy", "delta_entropy_proxy", "process_flags.closure"], "CLEAN source objects, vulnerable to event-token generator correlation."),
        ),
        invariance_requirements=COMMON_INVARIANCE,
        decoy_controls=("reaction_event token on empty reaction set returns negative", "food-set rename without graph change preserves verdict"),
        promotion_requirements=COMMON_PROMOTION_BLOCK,
        known_failure_modes=("event-token closure leak from Campaign 020", "reaction declarations with catalysts omitted become insufficient/negative rather than patched"),
        empirically_positive_worlds=(
            epi("W1", ["RAF/autocatalytic reaction networks"], ["doi:10.1186/s13015-015-0042-8", "doi:10.1098/rsif.2023.0732"]),
            epi("W9", ["prebiotic RAF and autocatalytic-set chemistry"], ["doi:10.1186/1759-2208-3-5", "doi:10.3390/life8040062"]),
            epi("W6", ["mutualistic networks as generalized closure analogues"], ["doi:10.1038/nature07950", "doi:10.1146/annurev.ecolsys.38.091206.095818"], "EXPLORATORY"),
        ),
    ),
    "motif.repair.draft": MotifContractV2(
        motif_id="motif.repair.draft",
        semantic_definition="A perturbation causes measurable damage and the same system exhibits endogenous recovery or damage depletion without an exogenous reset.",
        allowed_evidence=("boundary damage/recovery trajectories", "numeric state trajectories showing drop-then-recovery", "nonnegative damage depletion series"),
        forbidden_evidence=("repair_event/sanction_event/homeostasis_event tokens", "process_flags.repair", "benchmark or repair_rate fields", "daemon retry/cache refresh as biological repair"),
        predicate_abstraction_layer="perturbation-recovery time-series semantics",
        predicate_source_object_map=(
            som("boundaries", "boundary_trajectory", ["membrane_integrity", "membrane_material", "particle_count"]),
            som("state", "numeric_state_snapshot", ["numeric_series_values"]),
        ),
        lens_abstraction_layer=(
            lens("graph", ["actor paths", "branching_proxy", "process_flags.repair"], "PARTIAL because graph reads state/event objects; process flag must be ablated."),
            lens("crnt", ["p_invariant_proxy", "persistence_indicator", "process_flags.repair"], "PARTIAL/BAD depending on repair chemistry source; ablation required."),
            lens("dynamical_systems", ["stability", "terminal drift", "recovery dynamics"], "BAD when it reads the same recovery trajectory as the predicate."),
            lens("topology", ["basin return", "connectivity"], "PARTIAL if built from the same state object; no repair causality."),
            lens("petri", ["p_invariant_count", "process_flags.repair"], "PARTIAL; conservation proxy requires ablation."),
            lens("statistical_mechanics", ["energy_variance", "large_deviation_rate", "process_flags.repair"], "PARTIAL; rare-event recovery may remain after flag removal."),
            lens("control_theory", ["controllability_proxy", "intervention channels", "process_flags.repair"], "PARTIAL; control path must not be the predicate path."),
            lens("information", ["delta_entropy_proxy", "event_entropy"], "PARTIAL if built from same state; exploratory."),
        ),
        invariance_requirements=COMMON_INVARIANCE,
        decoy_controls=("repair token without damage/recovery returns negative", "exogenous reset returns negative", "no-damage control returns negative or insufficient"),
        promotion_requirements=COMMON_PROMOTION_BLOCK,
        known_failure_modes=("passive stability mistaken for repair", "scenario hardcoding through repair_rate", "C020 repair labels read process_flags.repair"),
        empirically_positive_worlds=(
            epi("W-1/W0 biology-adjacent", ["DNA damage and enzymatic repair systems"], ["doi:10.1038/362709a0", "pmid:8469282"]),
            epi("W2", ["plasma membrane disruption and repair"], ["doi:10.1146/annurev.cellbio.19.111301.140101", "pmid:14570567"], "EXPLORATORY"),
            epi("W7", ["collective repair and nest maintenance analogues"], ["doi:10.1146/annurev.es.04.110173.000245"], "EXPLORATORY"),
        ),
    ),
    "motif.externalized_memory.draft": MotifContractV2(
        motif_id="motif.externalized_memory.draft",
        semantic_definition="An external medium is written/read such that removing or scrambling that medium changes future behavior relative to the intact run.",
        allowed_evidence=("attention_shadow_history", "kernel_prediction_history", "storage-erasure response deltas"),
        forbidden_evidence=("memory_write_event/external_mark_event/learning_gain_event tokens", "process_flags.memory", "attention_entropy alone", "benchmark strings naming memory"),
        predicate_abstraction_layer="causal external-channel read/write semantics",
        predicate_source_object_map=(
            som("attention_shadow_history", "external_medium_history", ["stored_numeric_mass"]),
            som("kernel_prediction_history", "readback_history", ["confidence", "kernel_forecast", "sensor"]),
        ),
        lens_abstraction_layer=(
            lens("graph", ["actor-medium paths", "process_flags.memory"], "CLEAN by source object but BAD if used as a token shortcut; adversarial review required."),
            lens("crnt", ["out_of_domain"], "Declines for memory; retained for contract completeness."),
            lens("dynamical_systems", ["recurrence_rate", "process_flags.memory"], "CLEAN source object, weak causal support."),
            lens("topology", ["connectivity", "process_flags.memory"], "CLEAN source object, not causal by itself."),
            lens("petri", ["out_of_domain"], "Declines for memory."),
            lens("statistical_mechanics", ["out_of_domain"], "Declines for memory."),
            lens("control_theory", ["observability_proxy", "memory_channel_count", "process_flags.memory"], "BAD when memory_channel_count reads memory/mark/prediction token vocabulary."),
            lens("information", ["predictive_state_count", "delta_entropy_proxy", "process_flags.memory"], "CLEAN source object but not sufficient for external storage."),
        ),
        invariance_requirements=COMMON_INVARIANCE,
        decoy_controls=("rename memory tokens", "scramble external medium should change future readback", "internal recurrence without external store is negative"),
        promotion_requirements=COMMON_PROMOTION_BLOCK,
        known_failure_modes=("event token memory leak", "internal recurrence confused with externalized storage", "attention entropy treated as verdict"),
        empirically_positive_worlds=(
            epi("W8", ["extended-mind/external-symbol memory systems"], ["doi:10.1093/analys/58.1.7"], "EXPLORATORY"),
            epi("W7", ["pheromone trail external memory"], ["doi:10.1007/BF01417909", "pmid:32546115"]),
            epi("W6", ["ecosystem niche-construction memory"], ["doi:10.1002/fee.1311"], "EXPLORATORY"),
        ),
    ),
    "motif.replication_lineage.draft": MotifContractV2(
        motif_id="motif.replication_lineage.draft",
        semantic_definition="A parent-child descent graph exists and carries reconstructable heritable structure across at least one generational edge.",
        allowed_evidence=("lineage.nodes", "lineage.edges.parent", "lineage.edges.child", "parent/child sequences or inherited boundary kind"),
        forbidden_evidence=("replication_event/division_event/vertical_inheritance_event tokens", "process_flags.lineage", "child count without parent linkage", "payload parent/child IDs used only as event counts"),
        predicate_abstraction_layer="phylogenetic/descent graph semantics",
        predicate_source_object_map=(
            som("lineage", "descent_graph", ["nodes", "edges.parent", "edges.child", "edges.parent_sequence", "edges.child_sequence"]),
            som("boundaries", "heritable_boundary_marker", ["boundary_kind"]),
        ),
        lens_abstraction_layer=(
            lens("graph", ["parent-child event paths", "branching_proxy", "process_flags.lineage"], "CLEAN against lineage ledger if using events, but token-coupled unless ablated."),
            lens("crnt", ["out_of_domain"], "Declines for lineage."),
            lens("dynamical_systems", ["out_of_domain"], "Declines for event-only lineage."),
            lens("topology", ["out_of_domain"], "No lineage semantics."),
            lens("petri", ["t_invariant_count", "process_flags.lineage"], "CLEAN/PARTIAL only when vertical inheritance is encoded as transitions."),
            lens("statistical_mechanics", ["large_deviation_rate", "process_flags.lineage"], "CLEAN by source object but weak; event flag must be ablated."),
            lens("control_theory", ["out_of_domain"], "Declines for lineage."),
            lens("information", ["heritable information proxy"], "EXPLORATORY unless tied to lineage graph independently."),
        ),
        invariance_requirements=COMMON_INVARIANCE,
        decoy_controls=("division token without child entity is negative", "reverse-time lineage fails", "random child states with no heritable similarity fail"),
        promotion_requirements=COMMON_PROMOTION_BLOCK,
        known_failure_modes=("replication token shortcut", "growth without inheritance", "entity count used as descent"),
        empirically_positive_worlds=(
            epi("W11", ["quasispecies descent and replication"], ["doi:10.1007/BF00623322"]),
            epi("W5", ["digital evolution lineages"], ["doi:10.1038/nature01568", "pmid:12736677"]),
            epi("W12", ["endosymbiotic/genomic inheritance"], ["doi:10.1186/gb-2001-2-6-reviews1018", "pmid:11423013"], "EXPLORATORY"),
        ),
    ),
    "motif.self_maintained_boundary.draft": MotifContractV2(
        motif_id="motif.self_maintained_boundary.draft",
        semantic_definition="An operationally closed exchange boundary persists while system-internal dynamics maintain or replenish boundary material.",
        allowed_evidence=("boundary closed_cycle/permeability", "boundary membrane material or particle maintenance", "entity-level boundary continuity"),
        forbidden_evidence=("boundary_event/engulfment_event tokens", "process_flags.boundary", "boundary_kind string alone", "external reset of a shell"),
        predicate_abstraction_layer="operational region/partition plus boundary-preservation semantics",
        predicate_source_object_map=(
            som("boundaries", "boundary_object", ["closed_cycle", "permeability", "membrane_material", "particle_count"]),
        ),
        lens_abstraction_layer=(
            lens("graph", ["process_flags.boundary", "actor paths"], "CLEAN by source object in current traces but token-coupled."),
            lens("crnt", ["p_invariant_proxy", "process_flags.boundary"], "PARTIAL only when boundary chemistry source is disjoint from boundary object."),
            lens("dynamical_systems", ["stability", "process_flags.boundary"], "PARTIAL; stability is not boundary maintenance."),
            lens("topology", ["long_h1_cycles", "process_flags.boundary"], "CLEAN/PARTIAL; topology later, operational predicate first."),
            lens("petri", ["p_invariant_count", "process_flags.boundary"], "PARTIAL; requires ablation."),
            lens("statistical_mechanics", ["energy_variance", "process_flags.boundary"], "CLEAN/PARTIAL; basin stability not enough."),
            lens("control_theory", ["controllability_proxy", "process_flags.boundary"], "CLEAN/PARTIAL; control overlap must be explicit."),
            lens("information", ["delta_entropy_proxy", "process_flags.boundary"], "CLEAN source object, weak support."),
        ),
        invariance_requirements=COMMON_INVARIANCE,
        decoy_controls=("closed shell without internal maintenance is negative", "external reset trap is negative", "boundary token alone is negative"),
        promotion_requirements=COMMON_PROMOTION_BLOCK,
        known_failure_modes=("persistent static shell mistaken for self-maintained boundary", "topological loop mistaken for operational boundary", "process_flags.boundary leak"),
        empirically_positive_worlds=(
            epi("W2", ["fatty-acid vesicle growth/division"], ["doi:10.1021/ja900919c", "pmid:19323552"]),
            epi("W6", ["mutualist boundary/ecological compartment analogues"], ["doi:10.1038/nature07950"], "EXPLORATORY"),
            epi("W12", ["endosymbiotic boundary maintenance"], ["doi:10.1186/gb-2001-2-6-reviews1018", "pmid:11423013"], "EXPLORATORY"),
        ),
    ),
    "motif.floor_connectivity.draft": MotifContractV2(
        motif_id="motif.floor_connectivity.draft",
        semantic_definition="Multiple implementation perturbations remain connected inside equivalence fibers that preserve function and declared invariants in Basin-Floor Geometry, evaluated under D31 row-disjoint predicate/lens partitions.",
        allowed_evidence=("bfg_predicate_rows.perturbation_event.outcome_summary.fiber_relationship", "classifier_hash signed at preprocessing", "unit-level predicate verdicts aggregated from predicate_row or validation_predicate_row partitions"),
        forbidden_evidence=("neutral_component_fraction/nested_lineage_edges/attention_entropy state keys", "neutral_percolation_event tokens", "process_flags.floor", "C020 label function", "trajectory_geometry in the predicate path", "same-row predicate/lens evaluation"),
        predicate_abstraction_layer="D31 BFG predicate-side outcome summaries over row-disjoint perturbation units",
        predicate_source_object_map=(
            som("bfg_predicate_rows.perturbation_event.outcome_summary", "BfgOutcomeSummary", ["fiber_relationship", "origin_fiber_id", "terminal_fiber_id", "fiber_distance", "fiber_graph_distance", "membership_confidence", "boundary_confidence", "return_status", "verdict_state", "classifier_hash"]),
        ),
        lens_abstraction_layer=(
            LensContract("graph", ("edge_connectivity", "mean_step_distance", "basin_radius_at_recovery"), (som("bfg_lens_rows.perturbation_event.trajectory_geometry", "BfgTrajectoryGeometry", ["recovery_path_states", "basin_radius_at_recovery"]),), "NEW-ABST: basin recovery graph over lens rows, row-disjoint from predicate summaries."),
            LensContract("crnt", ("domain_decline",), tuple(), "DOMAIN-DECLINE: no reaction-network source object exists at the generic BFG basin-geometry layer."),
            LensContract("dynamical_systems", ("velocity_damping", "recovery_time_steps"), (som("bfg_lens_rows.perturbation_event.trajectory_geometry", "BfgTrajectoryGeometry", ["return_velocity_profile", "recovery_time_steps"]),), "NEW-ABST: basin return dynamics over lens-row trajectories."),
            LensContract("topology", ("point_cloud_containment", "radial_variance", "basin_radius_at_recovery"), (som("bfg_lens_rows.perturbation_event.trajectory_geometry", "BfgTrajectoryGeometry", ["recovery_path_states", "basin_radius_at_recovery"]),), "NEW-ABST: topology over recovery trajectory point clouds."),
            LensContract("petri", ("transition_activity", "transition_persistence"), (som("bfg_lens_rows.perturbation_event.trajectory_geometry", "BfgTrajectoryGeometry", ["recovery_path_states"]),), "NEW-ABST: recovery-transition Petri net candidate over trajectory transitions, not fiber labels."),
            LensContract("statistical_mechanics", ("large_deviation_proxy", "recovery_time_steps", "censored_at_step"), (som("bfg_lens_rows.perturbation_event.trajectory_geometry", "BfgTrajectoryGeometry", ["drift_magnitude_envelope", "recovery_time_steps", "censored_at_step"]),), "PARTIAL/RISKY: recovery-time distribution can leak return status if implemented carelessly; C026 denies return_status and requires survival."),
            LensContract("control_theory", ("velocity_rank", "basin_radius_at_recovery", "state_dimension"), (som("bfg_lens_rows.perturbation_event.trajectory_geometry", "BfgTrajectoryGeometry", ["return_velocity_profile", "basin_radius_at_recovery", "recovery_path_states"]),), "NEW-ABST: return controllability over lens-row dynamics."),
            LensContract("information", ("velocity_drift_dependence", "perturbation_magnitude"), (som("bfg_lens_rows.perturbation_event.trajectory_geometry", "BfgTrajectoryGeometry", ["return_velocity_profile", "drift_magnitude_envelope", "recovery_time_steps"]), som("bfg_lens_rows.perturbation_event", "BfgPerturbationMetadata", ["perturbation_magnitude"])), "PARTIAL/RISKY: recovery information flow uses a perturbation magnitude covariate; C026 denies magnitude and requires noncollapse."),
        ),
        invariance_requirements=COMMON_INVARIANCE,
        decoy_controls=("C020 surface keys without BFG source return insufficient_evidence", "point-attractor falsifier returns negative", "implementation-unique perturbation returns negative", "D31 row-disjoint predicate/lens partitions have zero perturbation_id overlap", "validation holdout uses validation_predicate_row and validation_lens_row split"),
        promotion_requirements=COMMON_PROMOTION_BLOCK + ("C026 unit-level shuffle must pass on validation holdout before any future promotion gate can open",),
        known_failure_modes=("C020 label function surface-key coupling", "floor death contaminated if evaluated on C020 label function", "connectivity proxy used without BFG quotient basis"),
        empirically_positive_worlds=(
            epi("W5/W11", ["neutral networks in sequence spaces"], ["doi:10.1073/pnas.96.17.9716", "pmid:10449760"]),
            epi("W4/W11", ["phenotype-preserving genotype variation"], ["doi:10.1186/1471-2148-8-284", "doi:10.1038/nature01568"], "EXPLORATORY"),
            epi("W0", ["neutral manifolds in dynamical systems"], ["doi:10.1038/150563a0"], "EXPLORATORY"),
        ),
    ),
}


def all_contracts() -> dict[str, MotifContractV2]:
    return dict(CONTRACTS)


def contract_payloads() -> dict[str, dict[str, Any]]:
    return {motif_id: contract.to_dict() for motif_id, contract in CONTRACTS.items()}
