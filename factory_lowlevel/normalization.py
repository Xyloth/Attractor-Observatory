"""Trace-checkable normalizers for low-level Factory records."""

from __future__ import annotations

from typing import Any

from .schemas import EmpiricalRecord, NormalizedReference, sha256


def normalize_record(record: EmpiricalRecord) -> NormalizedReference:
    if record.world_family == "math_primitives":
        return _normalize_math(record)
    if record.world_family == "atomic_molecular_primitives":
        return _normalize_atomic(record)
    if record.world_family == "crn":
        return _normalize_crn(record)
    if record.world_family == "field":
        return _normalize_field(record)
    if record.world_family == "origins_chemistry":
        return _normalize_origins_chemistry(record)
    if record.world_family == "quasispecies":
        return _normalize_quasispecies(record)
    if record.world_family == "ecosystem":
        return _normalize_ecosystem(record)
    raise ValueError(f"no normalizer for world_family={record.world_family}")


def _predicate(name: str, expression: str, observed: Any) -> dict[str, Any]:
    return {"predicate": name, "expression": expression, "observed": observed, "trace_checkable": True}


def _normalize_math(record: EmpiricalRecord) -> NormalizedReference:
    primitive = record.payload["primitive_class"]
    process_roles = [
        {
            "role_id": f"process.math.{primitive}",
            "label": primitive,
            "predicate": _predicate("primitive_class_present", "payload.primitive_class != ''", primitive),
        }
    ]
    channels = [
        {
            "channel_id": "channel.phase_flow",
            "label": "phase_flow",
            "predicate": _predicate("state_equation_present", "payload.state_equation != ''", record.payload["state_equation"]),
        }
    ]
    effects = [
        {
            "effect_id": f"effect.{record.payload['expected_stable_form']}",
            "label": record.payload["expected_stable_form"],
            "predicate": _predicate("stable_form_declared", "payload.expected_stable_form != ''", record.payload["expected_stable_form"]),
        }
    ]
    overlap = [
        {
            "field_id": "overlap.state_space_flow_field",
            "label": "state_space_flow_field",
            "write": _predicate("equation_writes_vector_field", "state_equation contains dx/dt or dtheta/dt", record.payload["state_equation"]),
            "persist": _predicate("invariant_declared", "len(payload.invariants) > 0", record.payload["invariants"]),
            "read": _predicate("stable_form_reads_flow", "expected_stable_form derives from primitive_class", record.payload["expected_stable_form"]),
            "counterfactual": _predicate("parameter_counterfactual_declared", "len(payload.parameters) > 0", record.payload["parameters"]),
        }
    ]
    return _normalized(record, process_roles, channels, effects, overlap, confidence=0.92)


def _normalize_atomic(record: EmpiricalRecord) -> NormalizedReference:
    payload = record.payload
    if record.record_type == "small_molecule_topology_summary":
        process_roles = [
            {
                "role_id": "process.molecular.bond_topology",
                "label": "bond_topology",
                "predicate": _predicate("smiles_present", "payload.canonical_smiles != ''", payload["canonical_smiles"]),
            }
        ]
        channels = [
            {
                "channel_id": "channel.covalent_bond_graph",
                "label": "covalent_bond_graph",
                "predicate": _predicate("heavy_atoms_present", "payload.heavy_atom_count >= 1", payload["heavy_atom_count"]),
            }
        ]
        effects = [
            {
                "effect_id": "effect.molecular_topology_constraint",
                "label": "molecular_topology_constraint",
                "predicate": _predicate("topology_proxy_present", "payload.bond_topology_proxy.element_token_count >= 1", payload["bond_topology_proxy"]),
            }
        ]
        overlap = [
            {
                "field_id": "overlap.covalent_structure_field",
                "label": "covalent_structure_field",
                "write": _predicate("smiles_writes_graph", "canonical_smiles maps to bond topology", payload["canonical_smiles"]),
                "persist": _predicate("formula_persists_identity", "molecular_formula present", payload["molecular_formula"]),
                "read": _predicate("heavy_atom_count_reads_graph", "heavy_atom_count >= 1", payload["heavy_atom_count"]),
                "counterfactual": _predicate("bond_proxy_counterfactual", "changing SMILES changes topology proxy", payload["bond_topology_proxy"]),
            }
        ]
        return _normalized(record, process_roles, channels, effects, overlap, confidence=0.86)

    process_roles = [
        {
            "role_id": "process.atomic.energy_level_structure",
            "label": "energy_level_structure",
            "predicate": _predicate("energy_levels_observed", "payload.energy_level_count >= 2", payload["energy_level_count"]),
        }
    ]
    channels = [
        {
            "channel_id": "channel.electromagnetic_transition",
            "label": "electromagnetic_transition",
            "predicate": _predicate("level_gaps_present", "len(payload.first_level_gaps_eV) > 0", payload["first_level_gaps_eV"]),
        }
    ]
    effects = [
        {
            "effect_id": "effect.discrete_energy_spectrum",
            "label": "discrete_energy_spectrum",
            "predicate": _predicate("discrete_levels", "payload.energy_level_count > 1", payload["energy_level_count"]),
        }
    ]
    overlap = [
        {
            "field_id": "overlap.electron_shell_energy_field",
            "label": "electron_shell_energy_field",
            "write": _predicate("nucleus_charge_context", "payload.element_symbol present", payload["element_symbol"]),
            "persist": _predicate("multiple_energy_levels", "payload.energy_level_count >= 3", payload["energy_level_count"]),
            "read": _predicate("transitions_read_gaps", "first_level_gaps_eV are derived from levels", payload["first_level_gaps_eV"]),
            "counterfactual": _predicate("ionization_limit_present", "max_observed_level_eV > ground_state_eV", payload["max_observed_level_eV"]),
        }
    ]
    return _normalized(record, process_roles, channels, effects, overlap, confidence=0.89)


def _normalize_crn(record: EmpiricalRecord) -> NormalizedReference:
    payload = record.payload
    world_params = payload.get("world_parameters", {})
    reactions = world_params.get("reactions", [])
    process_roles = [
        {
            "role_id": "process.crn.metabolic_reaction_network",
            "label": "metabolic_reaction_network",
            "predicate": _predicate("reaction_edges_present", "len(payload.world_parameters.reactions) > 0", len(reactions)),
        }
    ]
    channels = [
        {
            "channel_id": "channel.mass_action_reaction_edge",
            "label": "mass_action_reaction_edge",
            "predicate": _predicate("rate_constants_declared", "all reactions carry rate_constant", all("rate_constant" in row for row in reactions)),
        }
    ]
    effects = [
        {
            "effect_id": "effect.metabolic_closure_substrate_flow",
            "label": "metabolic_closure_substrate_flow",
            "predicate": _predicate("species_count_present", "payload.species_count >= 2", payload.get("species_count", 0)),
        }
    ]
    overlap = [
        {
            "field_id": "overlap.reaction_network_topology",
            "label": "reaction_network_topology",
            "write": _predicate("kegg_edges_write_crn", "KEGG reaction edges map to CRN reactions", payload.get("reaction_edge_count", 0)),
            "persist": _predicate("organism_identity_persists", "payload.organism_code == eco", payload.get("organism_code")),
            "read": _predicate("world_reads_initial_state", "world_parameters.initial_state present", sorted(world_params.get("initial_state", {}))),
            "counterfactual": _predicate("edge_count_counterfactual", "changing reaction_edges changes reactions", payload.get("reaction_edge_count", 0)),
        }
    ]
    return _normalized(record, process_roles, channels, effects, overlap, confidence=0.83)


def _normalize_field(record: EmpiricalRecord) -> NormalizedReference:
    payload = record.payload
    world_params = payload.get("world_parameters", {})
    process_roles = [
        {
            "role_id": "process.field.reaction_diffusion_benchmark",
            "label": "reaction_diffusion_benchmark",
            "predicate": _predicate("benchmark_present", "payload.benchmark != ''", payload.get("benchmark")),
        }
    ]
    channels = [
        {
            "channel_id": "channel.diffusion_reaction_coupling",
            "label": "diffusion_reaction_coupling",
            "predicate": _predicate("reaction_model_present", "payload.reaction_model != ''", payload.get("reaction_model")),
        }
    ]
    effects = [
        {
            "effect_id": "effect.pattern_formation_parameter_space",
            "label": "pattern_formation_parameter_space",
            "predicate": _predicate("parameter_range_present", "len(payload.parameter_range) > 0", payload.get("parameter_range", {})),
        }
    ]
    overlap = [
        {
            "field_id": "overlap.field_parameter_space",
            "label": "field_parameter_space",
            "write": _predicate("benchmark_writes_field_config", "world_parameters.benchmark selects FieldWorld scenario", world_params.get("benchmark")),
            "persist": _predicate("citation_persists_benchmark", "provenance.source_url is DOI-backed", record.provenance.get("source_url")),
            "read": _predicate("world_reads_steps", "world_parameters.steps present", world_params.get("steps")),
            "counterfactual": _predicate("parameter_range_counterfactual", "changing feed/kill or a/b ranges changes regime", payload.get("parameter_range", {})),
        }
    ]
    return _normalized(record, process_roles, channels, effects, overlap, confidence=0.84)


def _normalize_origins_chemistry(record: EmpiricalRecord) -> NormalizedReference:
    payload = record.payload
    world_params = payload.get("world_parameters", {})
    process_roles = [
        {
            "role_id": "process.origins.prebiotic_surface_chemistry",
            "label": "prebiotic_surface_chemistry",
            "predicate": _predicate("chemistry_context_present", "payload.chemistry_context != ''", payload.get("chemistry_context")),
        }
    ]
    channels = [
        {
            "channel_id": "channel.mineral_surface_gradient",
            "label": "mineral_surface_gradient",
            "predicate": _predicate("parameter_basis_present", "payload.parameter_basis != ''", payload.get("parameter_basis")),
        }
    ]
    effects = [
        {
            "effect_id": "effect.prebiotic_closure_boundary",
            "label": "prebiotic_closure_boundary",
            "predicate": _predicate("origins_benchmark_declared", "payload.benchmark != ''", payload.get("benchmark")),
        }
    ]
    overlap = [
        {
            "field_id": "overlap.prebiotic_chemistry_parameter_space",
            "label": "prebiotic_chemistry_parameter_space",
            "write": _predicate("benchmark_writes_origins_scenario", "world_parameters.benchmark selects OriginsChemistryWorld scenario", world_params.get("benchmark")),
            "persist": _predicate("citation_persists_context", "provenance.source_url is DOI-backed", record.provenance.get("source_url")),
            "read": _predicate("world_reads_surface_terms", "world_parameters carries catalytic or gradient terms", world_params),
            "counterfactual": _predicate("surface_parameter_counterfactual", "changing catalytic/gradient terms changes closure or boundary", world_params),
        }
    ]
    return _normalized(record, process_roles, channels, effects, overlap, confidence=0.82)


def _normalize_quasispecies(record: EmpiricalRecord) -> NormalizedReference:
    payload = record.payload
    world_params = payload.get("world_parameters", {})
    process_roles = [
        {
            "role_id": "process.quasispecies.viral_sequence_population",
            "label": "viral_sequence_population",
            "predicate": _predicate("sequence_projection_present", "world_parameters.master_sequence != ''", world_params.get("master_sequence")),
        }
    ]
    channels = [
        {
            "channel_id": "channel.mutation_selection",
            "label": "mutation_selection",
            "predicate": _predicate("mutation_rate_present", "world_parameters.mutation_rate > 0", world_params.get("mutation_rate")),
        }
    ]
    effects = [
        {
            "effect_id": "effect.quasispecies_cloud",
            "label": "quasispecies_cloud",
            "predicate": _predicate("population_size_present", "world_parameters.population_size > 0", world_params.get("population_size")),
        }
    ]
    overlap = [
        {
            "field_id": "overlap.sequence_mutation_space",
            "label": "sequence_mutation_space",
            "write": _predicate("ncbi_sequence_writes_master_projection", "NCBI FASTA maps to binary master_sequence", world_params.get("master_sequence")),
            "persist": _predicate("accession_persists_identity", "payload.accession present", payload.get("accession")),
            "read": _predicate("world_reads_mutation_parameters", "world_parameters includes mutation/insertion/deletion rates", {key: world_params.get(key) for key in ("mutation_rate", "insertion_rate", "deletion_rate")}),
            "counterfactual": _predicate("sequence_counterfactual", "changing sequence window changes master projection", payload.get("sequence_window_length")),
        }
    ]
    return _normalized(record, process_roles, channels, effects, overlap, confidence=0.78)


def _normalize_ecosystem(record: EmpiricalRecord) -> NormalizedReference:
    payload = record.payload
    world_params = payload.get("world_parameters", {})
    process_roles = [
        {
            "role_id": "process.ecosystem.multi_trophic_occurrence_proxy",
            "label": "multi_trophic_occurrence_proxy",
            "predicate": _predicate("guild_counts_present", "len(payload.guild_occurrence_counts) > 0", payload.get("guild_occurrence_counts", {})),
        }
    ]
    channels = [
        {
            "channel_id": "channel.trophic_interaction_matrix",
            "label": "trophic_interaction_matrix",
            "predicate": _predicate("producer_grazer_predator_present", "producer/grazer/predator guilds present", payload.get("guild_occurrence_counts", {})),
        }
    ]
    effects = [
        {
            "effect_id": "effect.ecosystem_stability_proxy",
            "label": "ecosystem_stability_proxy",
            "predicate": _predicate("ecosystem_benchmark_declared", "world_parameters.benchmark != ''", world_params.get("benchmark")),
        }
    ]
    overlap = [
        {
            "field_id": "overlap.ecosystem_trophic_state_space",
            "label": "ecosystem_trophic_state_space",
            "write": _predicate("gbif_counts_write_initial_conditions", "GBIF guild counts map to initial trophic pools", payload.get("guild_occurrence_counts", {})),
            "persist": _predicate("site_geometry_persists_context", "payload.geometry present", payload.get("geometry")),
            "read": _predicate("world_reads_trophic_parameters", "world_parameters includes producer/grazer/predator pools", {key: world_params.get(key) for key in ("initial_producers", "initial_grazers", "initial_predators")}),
            "counterfactual": _predicate("guild_count_counterfactual", "changing guild counts changes initial trophic pools", payload.get("guild_occurrence_counts", {})),
        }
    ]
    return _normalized(record, process_roles, channels, effects, overlap, confidence=0.74)


def _normalized(
    record: EmpiricalRecord,
    process_roles: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    effects: list[dict[str, Any]],
    overlap: list[dict[str, Any]],
    *,
    confidence: float,
) -> NormalizedReference:
    audit_flags = []
    if not overlap:
        audit_flags.append("missing_overlap_field")
    if record.license_class not in {"cc0", "public_domain", "open", "metadata_only"}:
        audit_flags.append("restricted_license")
    normalized_id = sha256(
        {
            "record_id": record.record_id,
            "process_roles": process_roles,
            "interaction_channels": channels,
            "state_space_effects": effects,
            "overlap_fields": overlap,
        }
    )
    return NormalizedReference(
        normalized_id=normalized_id,
        empirical_record_id=record.record_id,
        world_family=record.world_family,
        process_roles=process_roles,
        interaction_channels=channels,
        state_space_effects=effects,
        overlap_fields=overlap,
        confidence=confidence,
        audit_flags=audit_flags,
    )
