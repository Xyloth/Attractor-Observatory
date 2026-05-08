"""Four-layer persistence for the low-level Factory."""

from __future__ import annotations

import errno
import json
import os
import tempfile
import time
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


# CB-020: errno values that indicate transient Windows file-lock contention
# (anti-virus scan, Streamlit reader, Atlas reader, OneDrive sync, etc.).
# All five are recoverable with a backoff retry; ENOSPC / EROFS / etc. are
# real bugs that must propagate rather than be swallowed.
_TRANSIENT_WRITE_ERRNOS: frozenset[int] = frozenset({
    errno.EACCES,   # 13 — PermissionError (WinError 5 "Access is denied")
    errno.EAGAIN,   # 11 — Resource temporarily unavailable
    errno.EBUSY,    # 16 — Device or resource busy
    errno.EINVAL,   # 22 — Invalid argument (Windows MoveFileEx race on open dest)
    errno.ENOENT,   # 2  — temp-file vanished mid-replace (rare, but seen on Windows)
})


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
        # CB-016 fix: load existing on-disk JSON state into the dicts so
        # subsequent `write()` calls UPSERT the in-memory dicts rather
        # than REPLACING the persisted files. Without this, every
        # `run_live_factory_cycle` call wiped the prior cycle's records
        # — the bug surfaced in CB-015 T8 where 590 NIST + 50 KEGG
        # records were overwritten by a subsequent PubChem run.
        self._load_existing_from_disk()

    # ------------------------------------------------------------------
    # CB-016 — load-on-init recovery
    # ------------------------------------------------------------------
    def _load_existing_from_disk(self) -> None:
        """Populate in-memory dicts from existing JSON files in
        ``self.root`` if present. Missing files are normal (clean
        first-cycle start). Malformed files do NOT crash construction —
        they emit a self-audit entry and leave the corresponding dict
        empty so a fresh cycle can rebuild without overwriting unread
        records elsewhere.

        D9 binding: malformed state surfaces as an audit-queue item
        rather than silent loss. D14: never fabricates records to
        replace what couldn't be parsed.
        """
        loaders: list[tuple[str, str, callable]] = [
            ("empirical_records.json", "records", self._load_empirical_record),
            ("normalized_refs.json", "records", self._load_normalized_ref),
            ("evidence_graph.json", "edges", self._load_evidence_edge),
            ("audit_queue.json", "items", self._load_audit_item),
            ("source_cache_index.json", "entries", self._load_source_cache_entry),
            ("world_traces.json", "traces", self._load_world_trace),
        ]
        for filename, payload_key, loader in loaders:
            path = self.root / filename
            if not path.exists():
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError) as exc:
                # Self-audit a malformed persisted file. Don't raise —
                # the daemon's own audit pipeline observes this entry
                # on its next ingest cycle.
                audit_id = sha256({
                    "schema": "PersistenceLoadError.v1",
                    "path": str(path),
                    "error_type": type(exc).__name__,
                })
                self.audit_queue[audit_id] = AuditQueueItem(
                    audit_id=audit_id,
                    severity="high",
                    reason=f"persistence_load_failed:{filename}:{type(exc).__name__}",
                    record_id="",
                    source_id="factory_lowlevel.persistence",
                    recommended_action=(
                        f"inspect {path.as_posix()} for corruption; "
                        "the in-memory dict starts empty for this file "
                        "— the daemon will rebuild from cache on next cycle"
                    ),
                )
                continue
            rows = payload.get(payload_key) if isinstance(payload, dict) else payload
            if not isinstance(rows, list):
                continue
            for row in rows:
                if not isinstance(row, dict):
                    continue
                try:
                    loader(row)
                except (KeyError, TypeError, ValueError):
                    # Per-row malformations are skipped rather than
                    # raising — the daemon's full-cycle audit will catch
                    # systematic schema issues if they exist.
                    continue

    def _load_empirical_record(self, row: dict[str, Any]) -> None:
        # EmpiricalRecord is a frozen dataclass; use its constructor.
        rec = EmpiricalRecord(
            record_id=row["record_id"],
            source_id=row["source_id"],
            world_family=row["world_family"],
            record_type=row["record_type"],
            canonical_name=row["canonical_name"],
            payload=row.get("payload", {}) or {},
            provenance=row.get("provenance", {}) or {},
            license_class=row["license_class"],
            mode_tag=row.get("mode_tag", "exploratory"),
            schema_version=row.get("schema_version", "EmpiricalRecord.v1"),
        )
        self.empirical_records[rec.record_id] = rec

    def _load_normalized_ref(self, row: dict[str, Any]) -> None:
        ref = NormalizedReference(
            normalized_id=row["normalized_id"],
            empirical_record_id=row["empirical_record_id"],
            world_family=row["world_family"],
            process_roles=row.get("process_roles", []) or [],
            interaction_channels=row.get("interaction_channels", []) or [],
            state_space_effects=row.get("state_space_effects", []) or [],
            overlap_fields=row.get("overlap_fields", []) or [],
            confidence=float(row.get("confidence", 0.0)),
            audit_flags=row.get("audit_flags", []) or [],
            schema_version=row.get("schema_version", "NormalizedReference.v1"),
        )
        self.normalized_refs[ref.normalized_id] = ref

    def _load_evidence_edge(self, row: dict[str, Any]) -> None:
        edge = EvidenceEdge(
            edge_id=row["edge_id"],
            source=row["source"],
            target=row["target"],
            relation=row["relation"],
            evidence_record_ids=row.get("evidence_record_ids", []) or [],
            confidence=float(row.get("confidence", 0.0)),
        )
        self.evidence_edges[edge.edge_id] = edge

    def _load_audit_item(self, row: dict[str, Any]) -> None:
        item = AuditQueueItem(
            audit_id=row["audit_id"],
            severity=row["severity"],
            reason=row["reason"],
            record_id=row.get("record_id", "") or "",
            source_id=row.get("source_id", "") or "",
            recommended_action=row.get("recommended_action", "") or "",
        )
        self.audit_queue[item.audit_id] = item

    def _load_source_cache_entry(self, row: dict[str, Any]) -> None:
        entry = SourceCacheEntry(
            source_id=row["source_id"],
            cache_id=row["cache_id"],
            fetched_at=row["fetched_at"],
            url=row["url"],
            raw_content_hash=row["raw_content_hash"],
            raw_cache_path=row["raw_cache_path"],
            parser_version=row["parser_version"],
            license_class=row["license_class"],
            export_policy=row["export_policy"],
            record_count=int(row.get("record_count", 0)),
            retrieval_mode=row.get("retrieval_mode", "unknown"),
        )
        self.source_cache[entry.cache_id] = entry

    def _load_world_trace(self, row: dict[str, Any]) -> None:
        # World traces persist as raw dicts (not dataclasses).
        wf = row.get("world_family")
        if wf:
            self.world_traces[wf] = row

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
                "world_traces": len(self.world_traces),
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
    atomic_write_json(path, payload)
    return payload


def safe_read_json(
    path: str | Path,
    *,
    max_attempts: int = 6,
    base_backoff_seconds: float = 0.02,
    default: Any = None,
) -> Any:
    """Read JSON from ``path``; ride out transient Windows file-lock contention.

    CB-020 symmetric helper for ``atomic_write_json``. The Control Room
    Streamlit autorefresh + the daemon writer race on Windows: while
    ``Path.replace()`` swaps the destination, a concurrent reader's
    ``read_text()`` can see ``PermissionError [Errno 13]`` for the few
    milliseconds the OS holds the destination's exclusive lock. Without
    a retry, every Streamlit refresh tick has a small probability of
    showing stale-or-empty state to the user.

    On exhausted retries, returns ``default`` (default ``None``).
    Readers that want to distinguish "not present" from "race lost"
    should pass ``default=...`` and check the result; the typical
    reader is fine with ``None`` meaning "render empty state" because
    the next autorefresh tick will succeed.

    Backoff schedule: 20ms, 40ms, 80ms, 160ms, 320ms, 640ms ≈ 1.3s
    worst-case. Shorter than the writer budget because readers are
    expected to fail-soft (UI tolerates "no data this tick").
    """
    target = Path(path)
    if not target.exists():
        return default
    last_exc: OSError | None = None
    for attempt in range(max_attempts):
        try:
            raw = target.read_text(encoding="utf-8-sig")
        except OSError as exc:
            if exc.errno not in _TRANSIENT_WRITE_ERRNOS:
                raise
            last_exc = exc
            if attempt == max_attempts - 1:
                return default
            time.sleep(base_backoff_seconds * (2 ** attempt))
            continue
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Truncated mid-replace; backoff + retry. Replace is atomic
            # at the OS level but reader scheduling can produce partials.
            if attempt == max_attempts - 1:
                return default
            time.sleep(base_backoff_seconds * (2 ** attempt))
            continue
    # Unreachable; covered by `last_exc` paths above.
    if last_exc is not None:
        raise last_exc
    return default


def atomic_write_json(
    path: str | Path,
    payload: Any,
    *,
    max_attempts: int = 8,
    base_backoff_seconds: float = 0.05,
) -> Path:
    """Write JSON via same-directory temp file and atomic replace.

    CB-020 hardening: on Windows, when another process holds a transient
    handle on the destination file (Streamlit autorefresh reader, Atlas
    Tower poller, anti-virus scanner, OneDrive sync), the underlying
    ``os.replace`` raises one of:

    * ``OSError [Errno 22]`` (EINVAL) — Windows MoveFileEx fails because the
      destination already exists with an open handle.
    * ``PermissionError [WinError 5]`` (EACCES) — anti-virus or AV-class
      reader has the file locked.
    * ``OSError [Errno 16]`` (EBUSY) — same resource-busy class.

    All three are *transient*: a few hundred milliseconds of backoff is
    enough to ride out the race. A real bug (ENOSPC = disk full,
    EROFS = read-only filesystem, EISDIR = caller passed a directory) is
    NOT in the transient set — it propagates immediately so the caller
    sees the real failure, not an opaque timeout.

    Backoff schedule: 50ms, 100ms, 200ms, 400ms, 800ms, 1.6s, 3.2s, 6.4s
    = ~12.7s worst-case (within the daemon's per-source retry budget but
    generous enough to ride out a long anti-virus scan).
    """

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
        # CB-020 retry loop: replace() is the contention point.
        last_exc: OSError | None = None
        for attempt in range(max_attempts):
            try:
                Path(tmp_name).replace(out)
                last_exc = None
                break
            except OSError as exc:
                if exc.errno not in _TRANSIENT_WRITE_ERRNOS:
                    # Real bug — disk full, ROFS, etc. Propagate immediately.
                    raise
                last_exc = exc
                if attempt == max_attempts - 1:
                    # Exhausted budget — propagate the last transient error
                    # so the caller's retry logic / audit queue can surface it.
                    raise
                time.sleep(base_backoff_seconds * (2 ** attempt))
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
