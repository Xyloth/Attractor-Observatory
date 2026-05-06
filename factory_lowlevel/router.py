"""World router for low-level normalized Factory records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .schemas import EmpiricalRecord, NormalizedReference


WORLD_REQUIRED_RECORD_TYPES = {
    "atomic_molecular_primitives": {"atomic_energy_level_summary", "small_molecule_topology_summary"},
    "math_primitives": {"canonical_dynamical_form"},
    "crn": {"kegg_metabolic_network_summary"},
    "field": {"reaction_diffusion_benchmark"},
    "ecosystem": {"gbif_ecosystem_occurrence_summary"},
    "origins_chemistry": {"prebiotic_chemistry_benchmark"},
    "quasispecies": {"ncbi_hiv1_sequence_pilot"},
}


@dataclass(frozen=True)
class RoutingRejection:
    record_id: str
    source_id: str
    record_world: str
    target_world: str
    reason: str
    audit_severity: str = "medium"

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "source_id": self.source_id,
            "record_world": self.record_world,
            "target_world": self.target_world,
            "reason": self.reason,
            "audit_severity": self.audit_severity,
        }


@dataclass(frozen=True)
class RoutedWorldBundle:
    world_family: str
    empirical_records: list[EmpiricalRecord]
    normalized_refs: list[NormalizedReference]
    rejections: list[RoutingRejection] | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "world_family": self.world_family,
            "empirical_record_count": len(self.empirical_records),
            "normalized_ref_count": len(self.normalized_refs),
            "empirical_record_ids": sorted(record.record_id for record in self.empirical_records),
            "normalized_ref_ids": sorted(ref.normalized_id for ref in self.normalized_refs),
            "routing_rejections": [row.to_dict() for row in sorted(self.rejections or [], key=lambda item: item.record_id)],
        }


def validate_record_for_world(record: EmpiricalRecord, target_world: str) -> RoutingRejection | None:
    if target_world not in WORLD_REQUIRED_RECORD_TYPES:
        return RoutingRejection(
            record_id=record.record_id,
            source_id=record.source_id,
            record_world=record.world_family,
            target_world=target_world,
            reason=f"unknown_target_world:{target_world}",
            audit_severity="high",
        )
    if record.world_family != target_world:
        return RoutingRejection(
            record_id=record.record_id,
            source_id=record.source_id,
            record_world=record.world_family,
            target_world=target_world,
            reason=f"record_world_mismatch:{record.world_family}!={target_world}",
        )
    allowed_types = WORLD_REQUIRED_RECORD_TYPES[target_world]
    if record.record_type not in allowed_types:
        return RoutingRejection(
            record_id=record.record_id,
            source_id=record.source_id,
            record_world=record.world_family,
            target_world=target_world,
            reason=f"record_type_not_accepted:{record.record_type}",
        )
    payload = record.payload or {}
    world_params = payload.get("world_parameters")
    if target_world in {"crn", "field", "ecosystem", "origins_chemistry", "quasispecies"} and not isinstance(world_params, dict):
        return RoutingRejection(
            record_id=record.record_id,
            source_id=record.source_id,
            record_world=record.world_family,
            target_world=target_world,
            reason="missing_world_parameters",
            audit_severity="high",
        )
    if target_world == "crn":
        if not world_params.get("initial_state") or not world_params.get("reactions"):
            return RoutingRejection(record.record_id, record.source_id, record.world_family, target_world, "crn_requires_initial_state_and_reactions", "high")
    if target_world == "field" and not world_params.get("benchmark"):
        return RoutingRejection(record.record_id, record.source_id, record.world_family, target_world, "field_requires_benchmark", "high")
    if target_world == "origins_chemistry" and not world_params.get("benchmark"):
        return RoutingRejection(record.record_id, record.source_id, record.world_family, target_world, "origins_requires_benchmark", "high")
    if target_world == "ecosystem":
        required = ("initial_producers", "initial_grazers", "initial_predators", "benchmark")
        if any(world_params.get(key) in {None, ""} for key in required):
            return RoutingRejection(record.record_id, record.source_id, record.world_family, target_world, "ecosystem_requires_trophic_initial_conditions", "high")
    if target_world == "quasispecies":
        if not world_params.get("master_sequence") or not world_params.get("mutation_rate"):
            return RoutingRejection(record.record_id, record.source_id, record.world_family, target_world, "quasispecies_requires_sequence_and_mutation_rate", "high")
    return None


def routing_rejections(records: list[EmpiricalRecord], target_worlds: set[str] | None = None) -> list[RoutingRejection]:
    targets = set(target_worlds or {record.world_family for record in records})
    rows: list[RoutingRejection] = []
    for record in records:
        if record.world_family not in targets:
            rows.append(
                RoutingRejection(
                    record_id=record.record_id,
                    source_id=record.source_id,
                    record_world=record.world_family,
                    target_world=",".join(sorted(targets)),
                    reason="record_not_requested_for_selected_target_worlds",
                )
            )
            continue
        rejection = validate_record_for_world(record, record.world_family)
        if rejection is not None:
            rows.append(rejection)
    return rows


def route_records(records: list[EmpiricalRecord], refs: list[NormalizedReference], target_worlds: set[str] | None = None) -> list[RoutedWorldBundle]:
    by_world_records: dict[str, list[EmpiricalRecord]] = {}
    by_world_refs: dict[str, list[NormalizedReference]] = {}
    targets = set(target_worlds or {record.world_family for record in records} | {ref.world_family for ref in refs})
    rejections = routing_rejections(records, targets)
    rejected_ids = {row.record_id for row in rejections}
    for record in records:
        if record.world_family not in targets or record.record_id in rejected_ids:
            continue
        by_world_records.setdefault(record.world_family, []).append(record)
    for ref in refs:
        if ref.world_family not in targets or ref.empirical_record_id in rejected_ids:
            continue
        by_world_refs.setdefault(ref.world_family, []).append(ref)
    bundles = []
    for world in sorted(set(by_world_records) | set(by_world_refs)):
        bundles.append(
            RoutedWorldBundle(
                world_family=world,
                empirical_records=sorted(by_world_records.get(world, []), key=lambda row: row.record_id),
                normalized_refs=sorted(by_world_refs.get(world, []), key=lambda row: row.normalized_id),
                rejections=[row for row in rejections if row.record_world == world or row.target_world == world],
            )
        )
    return bundles
