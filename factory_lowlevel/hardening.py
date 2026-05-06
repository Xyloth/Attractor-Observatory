"""Live-mode hardening primitives for the low-level Factory."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .normalization import normalize_record
from .persistence import LowLevelFactoryStore, recover_json_tree
from .registry import SourceRegistry
from .router import route_records
from .schemas import AuditQueueItem, EmpiricalRecord, NormalizedReference, SourceCacheEntry, SourceDefinition, sha256, utc_now


class TransientFetchError(RuntimeError):
    """Raised by live adapters when a fetch may succeed on retry."""


class PartialResponseError(RuntimeError):
    """Raised when a source returns a truncated or incomplete payload."""

    def __init__(self, message: str, *, raw_payload: str | bytes = "") -> None:
        super().__init__(message)
        self.raw_payload = raw_payload


class SchemaMismatchError(RuntimeError):
    """Raised when an adapter sees an incompatible source schema."""

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


RECORD_REQUIRED_PAYLOAD_KEYS: dict[str, set[str]] = {
    "atomic_energy_level_summary": {
        "spectrum",
        "element_symbol",
        "ion_stage",
        "energy_level_count",
        "ground_state_eV",
        "max_observed_level_eV",
        "first_level_gaps_eV",
        "term_count",
        "configuration_count",
        "reference_count",
        "source_table",
    },
    "small_molecule_topology_summary": {
        "cid",
        "molecular_formula",
        "canonical_smiles",
        "molecular_weight",
        "heavy_atom_count",
        "bond_topology_proxy",
        "complexity",
        "source_table",
    },
    "canonical_dynamical_form": {
        "canonical_name",
        "primitive_class",
        "dimension",
        "state_equation",
        "parameters",
        "invariants",
        "expected_stable_form",
    },
}

NONNEGATIVE_NUMERIC_KEYS = {
    "energy_level_count",
    "term_count",
    "configuration_count",
    "reference_count",
    "molecular_weight",
    "heavy_atom_count",
    "complexity",
}

POSITIVE_NUMERIC_KEYS = {"dimension"}


@dataclass(frozen=True)
class LiveModeConfig:
    stale_after_seconds: int = 30 * 24 * 3600
    retry_limit: int = 2
    base_backoff_seconds: float = 1.0
    timeout_seconds: int = 20
    lock_stale_seconds: int = 6 * 3600
    requires_ai_runtime: bool = False


@dataclass
class HardeningAuditQueue:
    items: dict[str, AuditQueueItem] = field(default_factory=dict)

    def add(self, *, severity: str, reason: str, source_id: str, recommended_action: str, record_id: str = "unknown") -> AuditQueueItem:
        audit_id = sha256(
            {
                "severity": severity,
                "reason": reason,
                "source_id": source_id,
                "record_id": record_id,
                "recommended_action": recommended_action,
            }
        )
        item = AuditQueueItem(
            audit_id=audit_id,
            severity=severity,
            reason=reason,
            record_id=record_id,
            source_id=source_id,
            recommended_action=recommended_action,
        )
        self.items[audit_id] = item
        return item

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "LowLevelHardeningAuditQueue.v1",
            "items": [item.to_dict() for item in sorted(self.items.values(), key=lambda row: row.audit_id)],
            "count": len(self.items),
        }


class FactoryRunLock:
    """Atomic file lock for one local daemon instance."""

    def __init__(self, path: str | Path, *, stale_after_seconds: int = 6 * 3600) -> None:
        self.path = Path(path)
        self.stale_after_seconds = stale_after_seconds
        self.acquired = False

    def acquire(self) -> dict[str, Any]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists() and self._is_stale():
            stale_path = self.path.with_suffix(self.path.suffix + f".stale.{sha256(self.path.read_bytes()).removeprefix('sha256:')[:12]}")
            self.path.replace(stale_path)
        try:
            fd = os.open(str(self.path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            return {"acquired": False, "path": str(self.path), "reason": "lock_present"}
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps({"schema": "LowLevelFactoryRunLock.v1", "created_at": utc_now(), "pid": os.getpid()}, sort_keys=True) + "\n")
        self.acquired = True
        return {"acquired": True, "path": str(self.path), "reason": "ok"}

    def release(self) -> None:
        if self.acquired and self.path.exists():
            self.path.unlink()
        self.acquired = False

    def _is_stale(self) -> bool:
        age = datetime.now(timezone.utc).timestamp() - self.path.stat().st_mtime
        return age > self.stale_after_seconds


def cadence_to_seconds(cadence: str) -> int | None:
    normalized = cadence.strip().lower()
    return {
        "hourly": 3600,
        "daily": 24 * 3600,
        "weekly": 7 * 24 * 3600,
        "monthly": 30 * 24 * 3600,
    }.get(normalized)


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def cache_age_seconds(entry: SourceCacheEntry | dict[str, Any], *, now: datetime | None = None) -> float:
    row = entry.to_dict() if hasattr(entry, "to_dict") else dict(entry)
    fetched = parse_utc(str(row.get("fetched_at") or row.get("retrieved_at")))
    current = now or datetime.now(timezone.utc)
    return max(0.0, (current - fetched).total_seconds())


def refresh_due(source: SourceDefinition, entry: SourceCacheEntry | dict[str, Any] | None, *, now: datetime | None = None) -> bool:
    if entry is None:
        return True
    cadence = cadence_to_seconds(source.refresh_cadence)
    if cadence is None:
        return False
    return cache_age_seconds(entry, now=now) >= cadence


def stale_cache_audit(
    source: SourceDefinition,
    entry: SourceCacheEntry | dict[str, Any] | None,
    *,
    config: LiveModeConfig,
    audit_queue: HardeningAuditQueue,
    now: datetime | None = None,
) -> dict[str, Any]:
    if entry is None:
        return {"stale": False, "age_seconds": None, "audit_id": None}
    age = cache_age_seconds(entry, now=now)
    if age < config.stale_after_seconds:
        return {"stale": False, "age_seconds": age, "audit_id": None}
    audit = audit_queue.add(
        severity="medium",
        source_id=source.source_id,
        reason=f"stale_cache:{int(age)}s",
        recommended_action="refresh_source_before_live_promotion",
    )
    return {"stale": True, "age_seconds": age, "audit_id": audit.audit_id}


def load_source_cache_entries(store_root: str | Path) -> dict[str, dict[str, Any]]:
    path = Path(store_root) / "source_cache_index.json"
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    return {row["source_id"]: row for row in payload.get("entries", [])}


def replay_audit_queue(store_root: str | Path) -> dict[str, AuditQueueItem]:
    path = Path(store_root) / "audit_queue.json"
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8-sig"))
    items = {}
    for row in payload.get("items", []):
        item = AuditQueueItem(
            audit_id=row["audit_id"],
            severity=row["severity"],
            reason=row["reason"],
            record_id=row["record_id"],
            source_id=row["source_id"],
            recommended_action=row["recommended_action"],
        )
        items[item.audit_id] = item
    return items


def recover_session_ledger(path: str | Path, *, quarantine_dir: str | Path) -> dict[str, Any]:
    ledger = Path(path)
    quarantine_root = Path(quarantine_dir)
    quarantine_root.mkdir(parents=True, exist_ok=True)
    if not ledger.exists():
        return {"schema": "LowLevelSessionLedgerRecovery.v1", "valid_count": 0, "quarantined_count": 0, "run_ids": [], "audit_items": []}
    valid = []
    quarantined = []
    for index, line in enumerate(ledger.read_text(encoding="utf-8-sig").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            valid.append(json.loads(line))
        except json.JSONDecodeError as exc:
            quarantine_path = quarantine_root / f"{ledger.name}.line{index}.{sha256(line).removeprefix('sha256:')[:12]}.corrupt"
            quarantine_path.write_text(line + "\n", encoding="utf-8")
            quarantined.append({"line": index, "quarantine_path": str(quarantine_path), "error": str(exc)})
    if quarantined:
        tmp = ledger.with_suffix(ledger.suffix + ".tmp")
        tmp.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in valid), encoding="utf-8")
        tmp.replace(ledger)
    audit_items = [
        {
            "severity": "high",
            "reason": "malformed_session_ledger_line",
            "recommended_action": "quarantine_bad_line_and_rebuild_from_valid_sessions",
            "line": row["line"],
            "quarantine_path": row["quarantine_path"],
        }
        for row in quarantined
    ]
    return {
        "schema": "LowLevelSessionLedgerRecovery.v1",
        "valid_count": len(valid),
        "quarantined_count": len(quarantined),
        "run_ids": sorted({row.get("run_id", "") for row in valid if row.get("run_id")}),
        "audit_items": audit_items,
    }


def quarantine_payload(payload: str | bytes, *, quarantine_dir: str | Path, prefix: str) -> str:
    data = payload if isinstance(payload, bytes) else payload.encode("utf-8", errors="replace")
    root = Path(quarantine_dir)
    root.mkdir(parents=True, exist_ok=True)
    out = root / f"{prefix}.{sha256(data).removeprefix('sha256:')[:16]}.quarantine"
    out.write_bytes(data)
    return str(out)


def fetch_with_policy(
    adapter: Any,
    *,
    cache_dir: str | Path,
    existing_entry: dict[str, Any] | None,
    allow_network: bool,
    config: LiveModeConfig,
    audit_queue: HardeningAuditQueue,
    quarantine_dir: str | Path,
) -> dict[str, Any]:
    source = adapter.source_definition()
    due = refresh_due(source, existing_entry)
    stale = stale_cache_audit(source, existing_entry, config=config, audit_queue=audit_queue)
    attempts = []
    for attempt in range(config.retry_limit + 1):
        force_refresh = bool(due and allow_network)
        try:
            result = _call_fetch(adapter, cache_dir=cache_dir, allow_network=allow_network, timeout=config.timeout_seconds, force_refresh=force_refresh)
            return {
                "status": "ok",
                "source": source,
                "result": result,
                "attempts": attempts,
                "refresh_due": due,
                "force_refresh": force_refresh,
                "stale": stale,
            }
        except PartialResponseError as exc:
            qpath = quarantine_payload(exc.raw_payload, quarantine_dir=quarantine_dir, prefix=source.source_id)
            audit = audit_queue.add(
                severity="high",
                source_id=source.source_id,
                reason="partial_response_quarantined",
                recommended_action="hold_source_until_complete_payload_retrieved",
            )
            return {"status": "held", "source": source, "attempts": attempts, "audit_id": audit.audit_id, "quarantine_path": qpath, "stale": stale}
        except SchemaMismatchError as exc:
            audit = audit_queue.add(
                severity="high",
                source_id=source.source_id,
                reason=f"schema_mismatch:{exc}",
                recommended_action="adapter_review_before_rerun",
            )
            return {"status": "held", "source": source, "attempts": attempts, "audit_id": audit.audit_id, "schema_details": exc.details, "stale": stale}
        except TimeoutError as exc:
            attempts.append({"attempt": attempt + 1, "error_type": "TimeoutError", "backoff_seconds": _backoff(config, attempt)})
            if attempt >= config.retry_limit:
                audit = audit_queue.add(
                    severity="high",
                    source_id=source.source_id,
                    reason=f"timeout_retry_ceiling:{exc}",
                    recommended_action="manual_review_after_retry_ceiling",
                )
                return {"status": "held", "source": source, "attempts": attempts, "audit_id": audit.audit_id, "stale": stale}
        except TransientFetchError as exc:
            attempts.append({"attempt": attempt + 1, "error_type": "TransientFetchError", "backoff_seconds": _backoff(config, attempt)})
            if attempt >= config.retry_limit:
                audit = audit_queue.add(
                    severity="high",
                    source_id=source.source_id,
                    reason=f"transient_retry_ceiling:{exc}",
                    recommended_action="manual_review_after_retry_ceiling",
                )
                return {"status": "held", "source": source, "attempts": attempts, "audit_id": audit.audit_id, "stale": stale}
    raise AssertionError("unreachable fetch policy state")


def validate_adapter_result(
    result: Any,
    *,
    audit_queue: HardeningAuditQueue,
) -> dict[str, Any]:
    """Validate adapter-native record shape before normalization/persistence.

    This is intentionally source-agnostic but record-type-aware. It gives the
    daemon one structural chokepoint for SS-02/SS-03/AI-07/AI-08/AQ-03 without
    moving source parsing into the daemon.
    """

    source = result.source
    records = list(getattr(result, "records", []))
    required_key_violations: list[dict[str, Any]] = []
    unknown_key_census: dict[str, dict[str, int]] = {}
    numeric_violations: list[dict[str, Any]] = []
    duplicate_record_ids = _duplicates([record.record_id for record in records])
    duplicate_canonical_names = _duplicates([record.canonical_name for record in records])
    detector_anomalies: list[str] = []

    for record in records:
        expected = RECORD_REQUIRED_PAYLOAD_KEYS.get(record.record_type, set())
        payload = record.payload or {}
        missing = sorted(key for key in expected if _missing_payload_value(payload.get(key)))
        if missing:
            required_key_violations.append(
                {
                    "record_id": record.record_id,
                    "record_type": record.record_type,
                    "missing_keys": missing,
                }
            )
        unknown = sorted(key for key in payload if expected and key not in expected)
        if unknown:
            unknown_key_census.setdefault(record.record_type, {})
            for key in unknown:
                unknown_key_census[record.record_type][key] = unknown_key_census[record.record_type].get(key, 0) + 1
        numeric_violations.extend(_numeric_payload_violations(record))

    for warning in getattr(result, "warnings", []) or []:
        if str(warning).startswith("detector_anomaly:"):
            detector_anomalies.append(str(warning))

    for violation in required_key_violations:
        audit_queue.add(
            severity="high",
            source_id=source.source_id,
            record_id=violation["record_id"],
            reason=f"required_key_contract_missing:{','.join(violation['missing_keys'])}",
            recommended_action="hold_source_until_adapter_schema_review",
        )
    for record_id in duplicate_record_ids:
        audit_queue.add(
            severity="high",
            source_id=source.source_id,
            record_id=record_id,
            reason="duplicate_empirical_record_id",
            recommended_action="hold_source_until_duplicate_key_resolved",
        )
    for name in duplicate_canonical_names:
        audit_queue.add(
            severity="medium",
            source_id=source.source_id,
            record_id="unknown",
            reason=f"duplicate_canonical_name:{name}",
            recommended_action="review_source_for_duplicate_record_semantics",
        )
    for violation in numeric_violations:
        audit_queue.add(
            severity="high",
            source_id=source.source_id,
            record_id=violation["record_id"],
            reason=f"nonsensical_numeric_value:{violation['key']}={violation['value']}",
            recommended_action="hold_source_until_numeric_contract_review",
        )
    for anomaly in detector_anomalies:
        audit_queue.add(
            severity="medium",
            source_id=source.source_id,
            record_id="unknown",
            reason=f"source_native_detector_anomaly:{anomaly.removeprefix('detector_anomaly:')}",
            recommended_action="manual_detector_review_before_promotion",
        )

    hold_source = bool(required_key_violations or duplicate_record_ids or numeric_violations)
    return {
        "schema": "LowLevelAdapterValidation.v1",
        "source_id": source.source_id,
        "record_count": len(records),
        "required_key_violations": required_key_violations,
        "required_key_violation_count": len(required_key_violations),
        "unknown_key_census": unknown_key_census,
        "unknown_key_count": sum(sum(keys.values()) for keys in unknown_key_census.values()),
        "duplicate_record_ids": duplicate_record_ids,
        "duplicate_record_id_count": len(duplicate_record_ids),
        "duplicate_canonical_names": duplicate_canonical_names,
        "duplicate_canonical_name_count": len(duplicate_canonical_names),
        "numeric_violations": numeric_violations,
        "numeric_violation_count": len(numeric_violations),
        "detector_anomalies": detector_anomalies,
        "detector_anomaly_count": len(detector_anomalies),
        "hold_source": hold_source,
    }


def _missing_payload_value(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _duplicates(values: list[str]) -> list[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for value in values:
        if value in seen:
            dupes.add(value)
        seen.add(value)
    return sorted(dupes)


def _numeric_payload_violations(record: EmpiricalRecord) -> list[dict[str, Any]]:
    rows = []
    payload = record.payload or {}
    for key in NONNEGATIVE_NUMERIC_KEYS:
        if key in payload and isinstance(payload[key], (int, float)) and payload[key] < 0:
            rows.append({"record_id": record.record_id, "record_type": record.record_type, "key": key, "value": payload[key]})
    for key in POSITIVE_NUMERIC_KEYS:
        if key in payload and isinstance(payload[key], (int, float)) and payload[key] <= 0:
            rows.append({"record_id": record.record_id, "record_type": record.record_type, "key": key, "value": payload[key]})
    return rows


def _call_fetch(adapter: Any, *, cache_dir: str | Path, allow_network: bool, timeout: int, force_refresh: bool) -> Any:
    try:
        return adapter.fetch(cache_dir, allow_network=allow_network, timeout=timeout, force_refresh=force_refresh)
    except TypeError:
        return adapter.fetch(cache_dir, allow_network=allow_network, timeout=timeout)


def _backoff(config: LiveModeConfig, attempt: int) -> float:
    return round(config.base_backoff_seconds * (2 ** attempt), 6)


def run_hardened_low_level_factory(
    *,
    adapters: list[Any],
    store_root: str | Path,
    cache_dir: str | Path,
    allow_network: bool,
    session_ledger: str | Path,
    lock_path: str | Path,
    config: LiveModeConfig | None = None,
    trigger: str = "hardened_cycle",
) -> dict[str, Any]:
    cfg = config or LiveModeConfig()
    lock = FactoryRunLock(lock_path, stale_after_seconds=cfg.lock_stale_seconds)
    lock_result = lock.acquire()
    audit_queue = HardeningAuditQueue(replay_audit_queue(store_root))
    quarantine_dir = Path(store_root) / ".quarantine"
    if not lock_result["acquired"]:
        audit = audit_queue.add(
            severity="high",
            source_id="factory.daemon",
            reason="concurrent_run_lock_present",
            recommended_action="refuse_second_daemon_instance",
        )
        return {
            "schema": "LowLevelHardenedFactoryRun.v1",
            "status": "refused_lock",
            "requires_ai_runtime": False,
            "lock": lock_result,
            "audit_queue": audit_queue.to_dict(),
            "blocking_audit_id": audit.audit_id,
        }
    try:
        recovery = recover_json_tree(store_root, quarantine_dir=quarantine_dir) if Path(store_root).exists() else {"passed": True, "checked_count": 0, "quarantined_count": 0}
        ledger_recovery = recover_session_ledger(session_ledger, quarantine_dir=quarantine_dir)
        for item in ledger_recovery["audit_items"]:
            audit_queue.add(
                severity=item["severity"],
                source_id="factory.session_ledger",
                reason=item["reason"],
                recommended_action=item["recommended_action"],
            )
        existing_entries = load_source_cache_entries(store_root)
        registry = SourceRegistry()
        store = LowLevelFactoryStore(store_root)
        store.audit_queue.update(audit_queue.items)
        records: list[EmpiricalRecord] = []
        refs: list[NormalizedReference] = []
        fetch_reports = []
        warnings: list[str] = []
        for adapter in adapters:
            source = adapter.source_definition()
            registry.register(source)
            report = fetch_with_policy(
                adapter,
                cache_dir=cache_dir,
                existing_entry=existing_entries.get(source.source_id),
                allow_network=allow_network,
                config=cfg,
                audit_queue=audit_queue,
                quarantine_dir=quarantine_dir,
            )
            if report["status"] != "ok":
                fetch_reports.append(_serializable_fetch_report(report))
                continue
            result = report["result"]
            validation = validate_adapter_result(result, audit_queue=audit_queue)
            report["adapter_validation"] = validation
            fetch_reports.append(_serializable_fetch_report(report))
            if validation["hold_source"]:
                store.audit_queue.update(audit_queue.items)
                continue
            warnings.extend(getattr(result, "warnings", []))
            store.ingest_source_cache(result.cache_entry)
            store.ingest_empirical_records(result.records)
            records.extend(result.records)
            normalized_batch = []
            for record in result.records:
                try:
                    ref = normalize_record(record)
                except (KeyError, ValueError, TypeError) as exc:
                    audit_queue.add(
                        severity="high",
                        source_id=record.source_id,
                        record_id=record.record_id,
                        reason=f"normalization_schema_mismatch:{type(exc).__name__}",
                        recommended_action="adapter_review_before_rerun",
                    )
                    continue
                normalized_batch.append(ref)
                refs.append(ref)
            store.ingest_normalized_refs(normalized_batch)
            store.audit_queue.update(audit_queue.items)
        store.rebuild_evidence_graph()
        snapshot = store.write()
        routed = route_records(records, refs)
        session_record = {
            "schema": "LowLevelFactorySessionRecord.v2",
            "session_id": sha256({"run_id": snapshot["content_hash"], "trigger": trigger, "ledger_recovery": ledger_recovery["valid_count"]}),
            "run_id": snapshot["content_hash"],
            "trigger": trigger,
            "recorded_at": utc_now(),
            "requires_ai_runtime": False,
            "store_counts": snapshot["counts"],
            "audit_queue_count": len(store.audit_queue),
        }
        _append_jsonl(session_ledger, session_record)
        return {
            "schema": "LowLevelHardenedFactoryRun.v1",
            "status": "ok",
            "requires_ai_runtime": False,
            "lock": lock_result,
            "recovery": recovery,
            "ledger_recovery": ledger_recovery,
            "fetch_reports": fetch_reports,
            "registry": registry.to_dict(),
            "store_snapshot": snapshot,
            "routed_worlds": [bundle.to_dict() for bundle in routed],
            "records": [record.to_dict() for record in sorted(records, key=lambda row: row.record_id)],
            "normalized_refs": [ref.to_dict() for ref in sorted(refs, key=lambda row: row.normalized_id)],
            "audit_queue": {"items": [item.to_dict() for item in sorted(store.audit_queue.values(), key=lambda row: row.audit_id)], "count": len(store.audit_queue)},
            "warnings": warnings,
        }
    finally:
        lock.release()


def _serializable_fetch_report(report: dict[str, Any]) -> dict[str, Any]:
    row = {key: value for key, value in report.items() if key not in {"result", "source"}}
    row["source_id"] = report["source"].source_id
    if report.get("result") is not None:
        result = report["result"]
        row["record_count"] = len(result.records)
        row["cache_entry"] = result.cache_entry.to_dict()
    return row


def _append_jsonl(path: str | Path, payload: dict[str, Any]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")
