"""World router for low-level normalized Factory records."""

from __future__ import annotations

from dataclasses import dataclass

from .schemas import EmpiricalRecord, NormalizedReference


@dataclass(frozen=True)
class RoutedWorldBundle:
    world_family: str
    empirical_records: list[EmpiricalRecord]
    normalized_refs: list[NormalizedReference]

    def to_dict(self) -> dict[str, object]:
        return {
            "world_family": self.world_family,
            "empirical_record_count": len(self.empirical_records),
            "normalized_ref_count": len(self.normalized_refs),
            "empirical_record_ids": sorted(record.record_id for record in self.empirical_records),
            "normalized_ref_ids": sorted(ref.normalized_id for ref in self.normalized_refs),
        }


def route_records(records: list[EmpiricalRecord], refs: list[NormalizedReference]) -> list[RoutedWorldBundle]:
    by_world_records: dict[str, list[EmpiricalRecord]] = {}
    by_world_refs: dict[str, list[NormalizedReference]] = {}
    for record in records:
        by_world_records.setdefault(record.world_family, []).append(record)
    for ref in refs:
        by_world_refs.setdefault(ref.world_family, []).append(ref)
    bundles = []
    for world in sorted(set(by_world_records) | set(by_world_refs)):
        bundles.append(
            RoutedWorldBundle(
                world_family=world,
                empirical_records=sorted(by_world_records.get(world, []), key=lambda row: row.record_id),
                normalized_refs=sorted(by_world_refs.get(world, []), key=lambda row: row.normalized_id),
            )
        )
    return bundles
