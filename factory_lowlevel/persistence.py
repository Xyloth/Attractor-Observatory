"""Four-layer persistence for the low-level Factory."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .schemas import (
    ALLOWED_EXPORT_LICENSE_CLASSES,
    AuditQueueItem,
    EmpiricalRecord,
    EvidenceEdge,
    NormalizedReference,
    SourceCacheEntry,
    canonical_json,
    sha256,
)


class LowLevelFactoryStore:
    """Idempotent local persistence for Source Cache -> EmpiricalRecord -> NormalizedRefs -> Evidence Graph."""

    def __init__(self, root: str | Path = "reports/campaign_016/factory_store") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.source_cache: dict[str, SourceCacheEntry] = {}
        self.empirical_records: dict[str, EmpiricalRecord] = {}
        self.normalized_refs: dict[str, NormalizedReference] = {}
        self.evidence_edges: dict[str, EvidenceEdge] = {}
        self.audit_queue: dict[str, AuditQueueItem] = {}

    def ingest_source_cache(self, entry: SourceCacheEntry) -> None:
        self.source_cache[entry.cache_id] = entry

    def ingest_empirical_records(self, records: list[EmpiricalRecord]) -> None:
        for record in records:
            if record.license_class not in ALLOWED_EXPORT_LICENSE_CLASSES:
                audit_id = sha256({"record": record.record_id, "reason": "restricted_license"})
                self.audit_queue[audit_id] = AuditQueueItem(
                    audit_id=audit_id,
                    severity="high",
                    reason=f"record license {record.license_class} not export-allowed",
                    record_id=record.record_id,
                    source_id=record.source_id,
                    recommended_action="hold_in_source_cache_only",
                )
                continue
            self.empirical_records[record.record_id] = record

    def ingest_normalized_refs(self, refs: list[NormalizedReference]) -> None:
        for ref in refs:
            self.normalized_refs[ref.normalized_id] = ref
            for flag in ref.audit_flags:
                audit_id = sha256({"normalized": ref.normalized_id, "flag": flag})
                record = self.empirical_records.get(ref.empirical_record_id)
                self.audit_queue[audit_id] = AuditQueueItem(
                    audit_id=audit_id,
                    severity="medium",
                    reason=flag,
                    record_id=ref.empirical_record_id,
                    source_id=record.source_id if record else "unknown",
                    recommended_action="manual_adjudication_before_promotion",
                )

    def rebuild_evidence_graph(self) -> None:
        self.evidence_edges = {}
        by_world: dict[str, list[NormalizedReference]] = {}
        for ref in self.normalized_refs.values():
            by_world.setdefault(ref.world_family, []).append(ref)
        for world_family, refs in by_world.items():
            for axis in ("process_roles", "interaction_channels", "state_space_effects", "overlap_fields"):
                values = sorted({item["label"] for ref in refs for item in getattr(ref, axis)})
                for value in values:
                    record_ids = sorted(
                        ref.empirical_record_id for ref in refs for item in getattr(ref, axis) if item["label"] == value
                    )
                    edge_id = sha256({"world_family": world_family, "axis": axis, "value": value, "records": record_ids})
                    self.evidence_edges[edge_id] = EvidenceEdge(
                        edge_id=edge_id,
                        source=f"world:{world_family}",
                        target=f"{axis}:{value}",
                        relation=f"has_{axis[:-1] if axis.endswith('s') else axis}",
                        evidence_record_ids=record_ids,
                        confidence=round(len(record_ids) / max(len(refs), 1), 4),
                    )

    def write(self) -> dict[str, Any]:
        payloads = {
            "source_cache_index": {
                "schema": "LowLevelSourceCacheIndex.v1",
                "entries": [entry.to_dict() for entry in sorted(self.source_cache.values(), key=lambda row: row.cache_id)],
            },
            "empirical_records": {
                "schema": "LowLevelEmpiricalRecordSet.v1",
                "records": [record.to_dict() for record in sorted(self.empirical_records.values(), key=lambda row: row.record_id)],
            },
            "normalized_refs": {
                "schema": "LowLevelNormalizedReferenceSet.v1",
                "records": [ref.to_dict() for ref in sorted(self.normalized_refs.values(), key=lambda row: row.normalized_id)],
            },
            "evidence_graph": {
                "schema": "LowLevelEvidenceGraph.v1",
                "edges": [edge.to_dict() for edge in sorted(self.evidence_edges.values(), key=lambda row: row.edge_id)],
            },
            "audit_queue": {
                "schema": "LowLevelAuditQueue.v1",
                "items": [item.to_dict() for item in sorted(self.audit_queue.values(), key=lambda row: row.audit_id)],
            },
        }
        paths = {}
        for name, payload in payloads.items():
            path = self.root / f"{name}.json"
            atomic_write_json(path, payload)
            paths[name] = str(path)
        snapshot = {
            "schema": "LowLevelFactoryStoreSnapshot.v1",
            "paths": paths,
            "counts": {
                "source_cache_entries": len(self.source_cache),
                "empirical_records": len(self.empirical_records),
                "normalized_refs": len(self.normalized_refs),
                "evidence_edges": len(self.evidence_edges),
                "audit_queue_items": len(self.audit_queue),
            },
            "content_hash": sha256({name: payload for name, payload in payloads.items()}),
        }
        atomic_write_json(self.root / "snapshot.json", snapshot)
        return snapshot

    def content_hash(self) -> str:
        return sha256(
            {
                "source_cache": [entry.to_dict() for entry in sorted(self.source_cache.values(), key=lambda row: row.cache_id)],
                "empirical_records": [record.to_dict() for record in sorted(self.empirical_records.values(), key=lambda row: row.record_id)],
                "normalized_refs": [ref.to_dict() for ref in sorted(self.normalized_refs.values(), key=lambda row: row.normalized_id)],
                "evidence_edges": [edge.to_dict() for edge in sorted(self.evidence_edges.values(), key=lambda row: row.edge_id)],
                "audit_queue": [item.to_dict() for item in sorted(self.audit_queue.values(), key=lambda row: row.audit_id)],
            }
        )


def write_json(path: str | Path, payload: Any) -> Any:
    atomic_write_json(path, payload)
    return payload


def atomic_write_json(path: str | Path, payload: Any) -> Path:
    """Write JSON via same-directory temp file and atomic replace."""

    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    tmp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=out.parent,
            prefix=f".{out.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            tmp_name = handle.name
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        Path(tmp_name).replace(out)
    finally:
        if tmp_name is not None:
            tmp_path = Path(tmp_name)
            if tmp_path.exists():
                tmp_path.unlink()
    return out


def recover_json_artifact(path: str | Path, *, quarantine_dir: str | Path | None = None) -> dict[str, Any]:
    """Parse a JSON artifact or quarantine it if it is corrupt."""

    target = Path(path)
    if not target.exists():
        return {
            "schema": "LowLevelJsonRecoveryResult.v1",
            "status": "missing",
            "passed": False,
            "path": str(target),
            "quarantined": False,
            "reason": "artifact_missing",
        }
    raw = target.read_bytes()
    try:
        json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        quarantine_root = Path(quarantine_dir) if quarantine_dir is not None else target.parent / ".quarantine"
        quarantine_root.mkdir(parents=True, exist_ok=True)
        corruption_hash = sha256(raw)
        quarantine_path = quarantine_root / f"{target.name}.{corruption_hash.removeprefix('sha256:')[:16]}.corrupt"
        target.replace(quarantine_path)
        return {
            "schema": "LowLevelJsonRecoveryResult.v1",
            "status": "quarantined",
            "passed": True,
            "path": str(target),
            "quarantined": True,
            "quarantine_path": str(quarantine_path),
            "corruption_hash": corruption_hash,
            "error_type": exc.__class__.__name__,
            "error": str(exc),
        }
    return {
        "schema": "LowLevelJsonRecoveryResult.v1",
        "status": "ok",
        "passed": True,
        "path": str(target),
        "quarantined": False,
        "content_hash": sha256(raw),
    }


def recover_json_tree(root: str | Path, *, quarantine_dir: str | Path | None = None) -> dict[str, Any]:
    """Recover every top-level JSON artifact in a Factory store directory."""

    root_path = Path(root)
    paths = sorted(root_path.glob("*.json"))
    results = [recover_json_artifact(path, quarantine_dir=quarantine_dir) for path in paths]
    report = {
        "schema": "LowLevelJsonRecoveryTree.v1",
        "root": str(root_path),
        "checked_count": len(results),
        "ok_count": sum(1 for row in results if row["status"] == "ok"),
        "quarantined_count": sum(1 for row in results if row["status"] == "quarantined"),
        "missing_count": sum(1 for row in results if row["status"] == "missing"),
        "passed": all(row["status"] in {"ok", "quarantined"} and row["passed"] for row in results),
        "results": results,
    }
    report["content_hash"] = sha256({key: value for key, value in report.items() if key != "content_hash"})
    return report
