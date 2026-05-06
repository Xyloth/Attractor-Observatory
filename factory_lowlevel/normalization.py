"""Trace-checkable normalizers for low-level Factory records."""

from __future__ import annotations

from typing import Any

from .schemas import EmpiricalRecord, NormalizedReference, sha256


def normalize_record(record: EmpiricalRecord) -> NormalizedReference:
    if record.world_family == "math_primitives":
        return _normalize_math(record)
    if record.world_family == "atomic_molecular_primitives":
        return _normalize_atomic(record)
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
