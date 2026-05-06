"""Source registry and license enforcement for low-level Factory sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from .schemas import ALLOWED_EXPORT_LICENSE_CLASSES, RESTRICTED_LICENSE_CLASSES, SourceDefinition


class SourceAdapter(Protocol):
    adapter_id: str

    def source_definition(self) -> SourceDefinition:
        ...


@dataclass
class SourceRegistry:
    sources: dict[str, SourceDefinition] = field(default_factory=dict)

    def register(self, source: SourceDefinition) -> None:
        if source.source_id in self.sources:
            raise ValueError(f"duplicate source_id: {source.source_id}")
        self.sources[source.source_id] = source

    def validate(self) -> dict[str, object]:
        rows = []
        violations = []
        for source in sorted(self.sources.values(), key=lambda row: row.source_id):
            export_allowed = source.license_class in ALLOWED_EXPORT_LICENSE_CLASSES
            restricted = source.license_class in RESTRICTED_LICENSE_CLASSES
            if restricted and source.retrieval_mode_default != "dry_run":
                violations.append(
                    {
                        "source_id": source.source_id,
                        "violation": "restricted_source_must_default_to_dry_run",
                    }
                )
            rows.append(
                {
                    **source.to_dict(),
                    "export_allowed": export_allowed,
                    "raw_redistribution_allowed": source.license_class in {"cc0", "public_domain", "open"},
                }
            )
        return {
            "schema": "LowLevelSourceRegistryValidation.v1",
            "source_count": len(rows),
            "sources": rows,
            "violations": violations,
            "passed": not violations,
        }

    def to_dict(self) -> dict[str, object]:
        validation = self.validate()
        return {
            "schema": "LowLevelSourceRegistry.v1",
            "sources": [source.to_dict() for source in sorted(self.sources.values(), key=lambda row: row.source_id)],
            "validation": validation,
        }
