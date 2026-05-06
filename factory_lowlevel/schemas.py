"""Typed records for the low-level autonomous Factory v0.

The biology ingestion stack intentionally keeps BiologicalClaim semantics.
Campaign 016 adds an orthogonal low-level stack whose central persisted unit is
an EmpiricalRecord: a source-bound observation or curated canonical form, not a
biology claim and not an AI-authored assertion.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


ALLOWED_EXPORT_LICENSE_CLASSES = {"cc0", "public_domain", "open", "metadata_only"}
RESTRICTED_LICENSE_CLASSES = {"restricted", "nist_srd_raw"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256(payload: Any) -> str:
    if isinstance(payload, bytes):
        data = payload
    elif isinstance(payload, str):
        data = payload.encode("utf-8")
    else:
        data = canonical_json(payload).encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class SourceDefinition:
    source_id: str
    name: str
    url: str
    format: str
    license_class: str
    license_note: str
    refresh_cadence: str
    auth_required: bool = False
    target_world: str = ""
    adapter_id: str = ""
    retrieval_mode_default: str = "dry_run"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceCacheEntry:
    source_id: str
    cache_id: str
    fetched_at: str
    url: str
    raw_content_hash: str
    raw_cache_path: str
    parser_version: str
    license_class: str
    export_policy: str
    record_count: int
    retrieval_mode: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EmpiricalRecord:
    record_id: str
    source_id: str
    world_family: str
    record_type: str
    canonical_name: str
    payload: dict[str, Any]
    provenance: dict[str, Any]
    license_class: str
    mode_tag: str = "exploratory"
    schema_version: str = "EmpiricalRecord.v1"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NormalizedReference:
    normalized_id: str
    empirical_record_id: str
    world_family: str
    process_roles: list[dict[str, Any]]
    interaction_channels: list[dict[str, Any]]
    state_space_effects: list[dict[str, Any]]
    overlap_fields: list[dict[str, Any]]
    confidence: float
    audit_flags: list[str] = field(default_factory=list)
    schema_version: str = "NormalizedReference.v1"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceEdge:
    edge_id: str
    source: str
    target: str
    relation: str
    evidence_record_ids: list[str]
    confidence: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AuditQueueItem:
    audit_id: str
    severity: str
    reason: str
    record_id: str
    source_id: str
    recommended_action: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
