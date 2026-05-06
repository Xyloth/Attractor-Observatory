"""Four-layer persistence for the low-level Factory."""

from __future__ import annotations

import json
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
        # Bug E fix: routed-world traces. Each ingest cycle persists a
        # WorldTrace per routed world_family with a recompute-able
        # content_hash so the trace verifier can prove integrity.
        self.world_traces: dict[str, dict[str, Any]] = {}

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

    def ingest_adapter_audits(self, audits: list[Any]) -> None:
        """Bug C fix: persist adapter-level honest negatives. ``audits`` is
        a list of ``factory_lowlevel.adapters.AdapterAudit`` instances —
        records that survived the schema gate but flagged a missing
        critical field (e.g., empty SMILES after a PubChem schema drift).
        Each becomes a real ``AuditQueueItem`` so the queue carries a
        reason and a recommended_action — never silent (D9/D17)."""
        for a in audits:
            audit_id = sha256(
                {"record": a.record_id, "source": a.source_id, "reason": a.reason}
            )
            self.audit_queue[audit_id] = AuditQueueItem(
                audit_id=audit_id,
                severity=a.severity,
                reason=a.reason,
                record_id=a.record_id,
                source_id=a.source_id,
                recommended_action=a.recommended_action,
            )

    def ingest_world_traces(
        self,
        bundles: list[Any],
        *,
        run_id_seed: str | None = None,
    ) -> None:
        """Bug E fix: persist a ``WorldTrace`` per routed world_family.

        Each trace contains the routed record + ref ids, a
        ``trace_content_hash`` recomputable from the trace body, and a
        ``verify`` payload structured so a downstream consumer can
        re-derive the hash without trusting the stored value. Schema:
        ``LowLevelWorldTrace.v1``.

        The trace is the concrete answer to "the routed records actually
        produced trace files; traces verify; trace content_hash matches
        declared" in the CB-008 brief.
        """
        for bundle in bundles:
            body = {
                "world_family": bundle.world_family,
                "empirical_record_ids": sorted(
                    record.record_id for record in bundle.empirical_records
                ),
                "normalized_ref_ids": sorted(
                    ref.normalized_id for ref in bundle.normalized_refs
                ),
                "empirical_record_count": len(bundle.empirical_records),
                "normalized_ref_count": len(bundle.normalized_refs),
                "run_id_seed": run_id_seed or "",
            }
            trace_hash = sha256(body)
            self.world_traces[bundle.world_family] = {
                "schema": "LowLevelWorldTrace.v1",
                "world_family": bundle.world_family,
                "trace_id": sha256(
                    {"world": bundle.world_family, "body": body, "salt": run_id_seed or ""}
                ),
                "trace_content_hash": trace_hash,
                "body": body,
                "verifier": {
                    "predicate": "sha256_of_canonical_json(body) == trace_content_hash",
                    "trace_checkable": True,
                    "deterministic": True,
                },
            }

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
            "world_traces": {
                "schema": "LowLevelWorldTraceSet.v1",
                "traces": [self.world_traces[k] for k in sorted(self.world_traces.keys())],
            },
        }
        paths = {}
        for name, payload in payloads.items():
            path = self.root / f"{name}.json"
            path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
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
                "world_traces": len(self.world_traces),
            },
            "content_hash": sha256({name: payload for name, payload in payloads.items()}),
        }
        (self.root / "snapshot.json").write_text(json.dumps(snapshot, sort_keys=True, indent=2) + "\n", encoding="utf-8")
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


def verify_world_traces(store_root: str | Path) -> dict[str, Any]:
    """Re-derive every world trace's ``trace_content_hash`` from its
    persisted body and compare. Returns ``{world_family: bool}`` plus a
    summary. Exists so a downstream consumer can prove trace integrity
    without trusting the in-memory store.
    """
    p = Path(store_root) / "world_traces.json"
    if not p.exists():
        return {"present": False, "verified": {}, "all_pass": False}
    payload = json.loads(p.read_text(encoding="utf-8"))
    results: dict[str, bool] = {}
    for trace in payload.get("traces", []):
        body = trace.get("body", {})
        recomputed = sha256(body)
        declared = trace.get("trace_content_hash", "")
        results[trace.get("world_family", "?")] = recomputed == declared
    return {
        "present": True,
        "verified": results,
        "all_pass": all(results.values()) and bool(results),
    }


def write_json(path: str | Path, payload: Any) -> Any:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return payload
