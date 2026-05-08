"""Continuous-cycle launcher for unattended Factory ingestion.

CB-013 hardening: lock file, SIGINT/SIGTERM handlers, atomic
checkpoint, resume-from-heartbeat verification. See
``launch_safety.py`` for the underlying mechanics — this module wires
them into ``run_continuous_daemon``.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import sys
import time
from pathlib import Path
from typing import Any

from .launch_safety import (
    SignalState,
    acquire_lock,
    install_signal_handlers,
    release_lock,
    verify_resume,
    write_checkpoint,
)
from .live_pipeline import available_adapters, run_live_factory_cycle
from .memory_guard import (
    DEFAULT_MAX_RSS_GB,
    DEFAULT_MIN_FREE_GB,
    check_memory_budget,
    consume_stop_flag,
    measure_memory,
    read_stop_flag,
)
from .persistence import atomic_write_json
from .progress import write_ingestion_progress
from .schemas import sha256, utc_now


DEFAULT_LEDGER = Path("project_telemetry/factory_daemon_sessions.jsonl")
DEFAULT_STATE = Path("project_telemetry/factory_daemon_state.json")
DEFAULT_HEARTBEAT = Path("control_room/cache/factory_daemon_heartbeat.json")

_STOP_REQUESTED = False
_SIGNAL_STATE: SignalState = SignalState()


def cadence_seconds(label: str) -> int:
    normalized = (label or "").strip().lower()
    if normalized in {"hourly", "per_hour", "1h"}:
        return 60 * 60
    if normalized in {"daily", "per_day", "1d"}:
        return 24 * 60 * 60
    if normalized in {"weekly", "per_week", "1w"}:
        return 7 * 24 * 60 * 60
    if normalized in {"monthly", "per_month", "1mo"}:
        return 30 * 24 * 60 * 60
    if normalized in {"manual", "manual_spec_review", "dry_run"}:
        return 3650 * 24 * 60 * 60
    return 24 * 60 * 60


def run_continuous_daemon(
    *,
    cycles: int = 0,
    sleep_seconds: int = 3600,
    allow_network: bool = False,
    target_worlds: list[str] | None = None,
    source_ids: list[str] | None = None,
    store_root: str | Path = "reports/campaign_035/factory_store",
    cache_dir: str | Path = "reports/campaign_035/source_cache",
    run_root: str | Path = "control_room/cache/factory_runs",
    trace_root: str | Path = "reports/campaign_035/traces",
    session_ledger: str | Path = DEFAULT_LEDGER,
    state_path: str | Path = DEFAULT_STATE,
    heartbeat_path: str | Path = DEFAULT_HEARTBEAT,
    progress_root: str | Path = "reports/factory_daemon_progress",
    disk_budget_mb: int = 512,
    retry_ceiling: int = 3,
    retry_base_seconds: float = 2.0,
    cycle_backoff_seconds: int = 30,
    force_refresh: bool = False,
    force_refresh_source: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Run due source adapters repeatedly without AI runtime involvement.

    ``cycles=0`` means unbounded daemon mode. The function is intentionally
    source-granular: one bad adapter quarantines that source for the cycle while
    other due sources still run and write their own provenance-bound artifacts.
    """

    global _STOP_REQUESTED, _SIGNAL_STATE
    _STOP_REQUESTED = False
    _SIGNAL_STATE = SignalState()

    # CB-013 T4 — resume verification before any side-effects.
    resume = verify_resume(heartbeat_path=heartbeat_path, store_root=store_root)
    if not resume.proceed:
        atomic_write_json(
            Path(heartbeat_path),
            {
                "schema": "FactoryDaemonHeartbeat.v1",
                "heartbeat_at": utc_now(),
                "status": "resume_aborted",
                "rationale": resume.rationale,
                "prior_status": resume.prior_status,
                "integrity_check": resume.integrity_check,
            },
        )
        raise SystemExit(
            f"\nDaemon refusing to start: {resume.rationale}\n"
            f"Surface to Builder via control_room/cache/factory_daemon_heartbeat.json.\n"
        )

    # CB-013 T4 — exclusive lock file. Refuse second instance.
    lock = acquire_lock(store_root=store_root, pid=os.getpid())
    if not lock.acquired:
        atomic_write_json(
            Path(heartbeat_path),
            {
                "schema": "FactoryDaemonHeartbeat.v1",
                "heartbeat_at": utc_now(),
                "status": "start_refused_lock_held",
                "rationale": lock.rationale,
                "holder_pid": lock.holder_pid,
                "holder_started_at": lock.holder_started_at,
            },
        )
        raise SystemExit(f"\nDaemon refusing to start: {lock.rationale}\n")

    # CB-013 T4 — SIGINT/SIGTERM handlers. Replace prior single-handler.
    install_signal_handlers(_SIGNAL_STATE, heartbeat_path=heartbeat_path)

    state = _read_json(Path(state_path), default={"schema": "FactoryDaemonState.v1", "last_success_by_source": {}})
    clearance = _apply_force_refresh(
        state,
        clear_all=force_refresh,
        source_ids=force_refresh_source or [],
    )
    if clearance["cleared_source_ids"] or clearance["requested_missing_source_ids"]:
        _append_jsonl(session_ledger, clearance)
        atomic_write_json(Path(state_path), state)
    session_records: list[dict[str, Any]] = []
    cycle_index = 0
    while cycles <= 0 or cycle_index < cycles:
        started_at = utc_now()
        source_rows = _filter_sources(available_adapters(), target_worlds=target_worlds, source_ids=source_ids)
        due_sources = _due_sources(source_rows, state)
        session = {
            "schema": "FactoryContinuousDaemonSession.v1",
            "cycle_index": cycle_index,
            "started_at": started_at,
            "completed_at": "",
            "allow_network": bool(allow_network),
            "due_source_ids": [row["source_id"] for row in due_sources],
            "completed_source_ids": [],
            "quarantined_source_ids": [],
            "run_ids": [],
            "status": "running",
            "audit_items": [],
        }
        _write_heartbeat(heartbeat_path, session=session, status="running")

        disk_audit = _disk_budget_audit(cache_dir=cache_dir, store_root=store_root, budget_mb=disk_budget_mb)
        if disk_audit:
            session["status"] = "held_disk_budget"
            session["audit_items"].append(disk_audit)
            session["completed_at"] = utc_now()
            _append_jsonl(session_ledger, _with_session_id(session))
            _write_heartbeat(heartbeat_path, session=session, status=session["status"])
            session_records.append(session)
            if _STOP_REQUESTED:
                break
            cycle_index += 1
            time.sleep(cycle_backoff_seconds)
            continue

        for row in due_sources:
            # CB-013 T4: SIGINT (graceful) → finish current cycle then break;
            # SIGTERM (hard) → break immediately. Both surface in heartbeat.
            if _STOP_REQUESTED or _SIGNAL_STATE.stop_requested:
                break
            if _SIGNAL_STATE.hard_stop_requested:
                break
            # CB-021 M3: file-based stop flag (Windows-friendly safe stop).
            stop_reason = read_stop_flag()
            if stop_reason:
                session.setdefault("audit_items", []).append({
                    "reason": "operator_stop_flag_honored",
                    "stop_reason": stop_reason,
                    "severity": "info",
                    "recommended_action": "operator_initiated_clean_shutdown",
                })
                consume_stop_flag()
                break
            # CB-021 M1: memory budget guard. After the 2026-05-08 incident
            # where the daemon ate 40-50 GB RSS in one long-lived process
            # and white-screened the desktop, refuse to start the next
            # source if RSS or free-RAM are outside budget. Caller exits
            # cleanly with audit item; operator restarts on a smaller scope.
            mem_ok, snap, mem_reason = check_memory_budget()
            if not mem_ok:
                session.setdefault("audit_items", []).append({
                    "reason": "memory_budget_exceeded",
                    "diagnostic": mem_reason,
                    "rss_gb": snap.rss_gb,
                    "free_gb": snap.free_gb,
                    "measurement_source": snap.source,
                    "severity": "high",
                    "recommended_action": (
                        "abort cycle; restart daemon with smaller scope "
                        "(--source-id or --target-world); investigate "
                        "memory leak in trace_rows accumulation or store load"
                    ),
                })
                break
            source_id = row["source_id"]
            result = _run_source_with_retries(
                source_id=source_id,
                allow_network=allow_network,
                store_root=store_root,
                cache_dir=cache_dir,
                run_root=run_root,
                trace_root=trace_root,
                retry_ceiling=retry_ceiling,
                retry_base_seconds=retry_base_seconds,
                trigger=f"continuous_daemon_cycle_{cycle_index}",
            )
            if result["status"] == "ok":
                session["completed_source_ids"].append(source_id)
                session["run_ids"].append(result["run_id"])
                state.setdefault("last_success_by_source", {})[source_id] = utc_now()
            else:
                session["quarantined_source_ids"].append(source_id)
                session["audit_items"].append(result["audit"])
            # CB-021 M4: enriched heartbeat with RSS for liveness diagnosis.
            _write_heartbeat(heartbeat_path, session=session, status="running")

        session["completed_at"] = utc_now()
        if _SIGNAL_STATE.hard_stop_requested:
            session["status"] = "hard_shutdown"
        elif _STOP_REQUESTED or _SIGNAL_STATE.stop_requested:
            session["status"] = "stop_requested"
        else:
            session["status"] = "complete"
        atomic_write_json(Path(state_path), state)
        _append_jsonl(session_ledger, _with_session_id(session))
        # CB-013 T4: atomic checkpoint of factory_store snapshot so a
        # crash mid-write cannot corrupt downstream consumers.
        snapshot_path = Path(store_root) / "snapshot.json"
        if snapshot_path.exists():
            try:
                snap_payload = json.loads(snapshot_path.read_text(encoding="utf-8-sig"))
                write_checkpoint(snapshot_path=snapshot_path, payload=snap_payload)
            except (OSError, json.JSONDecodeError):
                pass
        _write_heartbeat(heartbeat_path, session=session, status=session["status"])
        # CB-013 T5: per-world progress tracking (one ingestion_progress.json
        # per world per session) so the BUILDER playbook can read progress
        # without parsing the full session ledger.
        try:
            write_ingestion_progress(
                session=session,
                state=state,
                store_root=store_root,
                source_rows=source_rows,
                progress_root=progress_root,
            )
        except Exception:  # pragma: no cover — progress write must never break the daemon
            pass
        session_records.append(session)
        if _STOP_REQUESTED or _SIGNAL_STATE.stop_requested or _SIGNAL_STATE.hard_stop_requested:
            break
        cycle_index += 1
        if cycles <= 0 or cycle_index < cycles:
            # CB-013 T4: SIGTERM check during sleep; sleep in 1s slices
            # so a hard-stop signal is honored within ~1 second.
            slept = 0
            while slept < sleep_seconds:
                if _SIGNAL_STATE.hard_stop_requested:
                    break
                time.sleep(1)
                slept += 1
    # CB-013 T4: clean shutdown finalize (lock release + final heartbeat).
    final_status = (
        "hard_shutdown" if _SIGNAL_STATE.hard_stop_requested
        else "clean_shutdown"
    )
    atomic_write_json(
        Path(heartbeat_path),
        {
            "schema": "FactoryDaemonHeartbeat.v1",
            "heartbeat_at": utc_now(),
            "status": final_status,
            "cycles_completed": cycle_index,
            "last_signal": _SIGNAL_STATE.last_signal,
            "last_signal_at": _SIGNAL_STATE.last_signal_at,
        },
    )
    release_lock(store_root=store_root, pid=os.getpid())
    return session_records


def _due_sources(source_rows: list[dict[str, Any]], state: dict[str, Any]) -> list[dict[str, Any]]:
    now = time.time()
    last_success = state.get("last_success_by_source", {})
    due = []
    for row in source_rows:
        last = last_success.get(row["source_id"])
        if not last:
            due.append(row)
            continue
        try:
            last_epoch = _parse_utc_epoch(last)
        except ValueError:
            due.append(row)
            continue
        if now - last_epoch >= cadence_seconds(row.get("refresh_cadence", "")):
            due.append(row)
    return due


def _apply_force_refresh(
    state: dict[str, Any],
    *,
    clear_all: bool,
    source_ids: list[str],
) -> dict[str, Any]:
    last_success = state.setdefault("last_success_by_source", {})
    before = set(last_success)
    if clear_all:
        requested = sorted(before)
    else:
        requested = sorted(set(source_ids))
    cleared = []
    missing = []
    for source_id in requested:
        if source_id in last_success:
            last_success.pop(source_id, None)
            cleared.append(source_id)
        else:
            missing.append(source_id)
    return {
        "schema": "FactoryDaemonForceRefreshClearance.v1",
        "record_type": "force_refresh_clearance",
        "cleared_at": utc_now(),
        "clear_all": bool(clear_all),
        "requested_source_ids": requested,
        "cleared_source_ids": cleared,
        "requested_missing_source_ids": missing,
        "reason": "operator requested refresh-cadence bypass before cycle",
    }


def _filter_sources(
    source_rows: list[dict[str, Any]],
    *,
    target_worlds: list[str] | None,
    source_ids: list[str] | None,
) -> list[dict[str, Any]]:
    worlds = set(target_worlds or [])
    sources = set(source_ids or [])
    filtered = []
    for row in source_rows:
        if worlds and row.get("target_world") not in worlds:
            continue
        if sources and row.get("source_id") not in sources:
            continue
        filtered.append(row)
    return filtered


def _run_source_with_retries(
    *,
    source_id: str,
    allow_network: bool,
    store_root: str | Path,
    cache_dir: str | Path,
    run_root: str | Path,
    trace_root: str | Path,
    retry_ceiling: int,
    retry_base_seconds: float,
    trigger: str,
) -> dict[str, Any]:
    errors = []
    for attempt in range(1, max(retry_ceiling, 1) + 1):
        try:
            run = run_live_factory_cycle(
                source_ids=[source_id],
                allow_network=allow_network,
                store_root=store_root,
                cache_dir=cache_dir,
                run_root=run_root,
                trace_root=trace_root,
                trigger=trigger,
            )
            return {"status": "ok", "run_id": run["run_id"], "attempts": attempt}
        except Exception as exc:  # pragma: no cover - deterministic tests cover success; failures are runtime environment.
            errors.append(f"{type(exc).__name__}:{exc}")
            if attempt < retry_ceiling:
                time.sleep(retry_base_seconds * (2 ** (attempt - 1)))
    return {
        "status": "quarantined",
        "audit": {
            "severity": "high",
            "source_id": source_id,
            "reason": "adapter_retry_ceiling_exceeded",
            "attempts": max(retry_ceiling, 1),
            "errors": errors,
            "recommended_action": "manual_adapter_review_before_next_refresh",
        },
    }


def _disk_budget_audit(*, cache_dir: str | Path, store_root: str | Path, budget_mb: int) -> dict[str, Any] | None:
    budget_bytes = int(budget_mb) * 1024 * 1024
    checked = {
        "source_cache_bytes": _tree_bytes(Path(cache_dir)),
        "audit_queue_bytes": _tree_bytes(Path(store_root) / "audit_queue") + _file_bytes(Path(store_root) / "audit_queue.json"),
    }
    if any(value > budget_bytes for value in checked.values()):
        return {
            "severity": "high",
            "reason": "daemon_disk_budget_exceeded",
            "budget_mb": budget_mb,
            "checked": checked,
            "recommended_action": "free_space_or_raise_budget_before_next_cycle",
        }
    return None


def _tree_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    return sum(child.stat().st_size for child in path.rglob("*") if child.is_file())


def _file_bytes(path: Path) -> int:
    return path.stat().st_size if path.exists() and path.is_file() else 0


def _read_json(path: Path, *, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return dict(default)
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError:
        return dict(default)


def _append_jsonl(path: str | Path, row: dict[str, Any]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, sort_keys=True) + "\n")


def _with_session_id(session: dict[str, Any]) -> dict[str, Any]:
    payload = dict(session)
    payload["session_id"] = sha256({key: value for key, value in session.items() if key != "session_id"})
    return payload


def _write_heartbeat(path: str | Path, *, session: dict[str, Any], status: str) -> None:
    # CB-021 M4: enrich heartbeat with PID, RSS, and free-RAM so a stale
    # heartbeat is also a memory diagnostic. After the 2026-05-08 incident
    # the heartbeat went stale at 19:45:22Z while RSS climbed to 40-50 GB
    # — without per-heartbeat RSS the operator had no fine-grained signal
    # to distinguish "stuck" from "OOM-crashing". Now every heartbeat
    # carries enough state to triage in seconds.
    snap = measure_memory()
    heartbeat = {
        "schema": "FactoryDaemonHeartbeat.v1",
        "heartbeat_at": utc_now(),
        "status": status,
        "cycle_index": session["cycle_index"],
        "due_source_count": len(session["due_source_ids"]),
        "completed_source_count": len(session["completed_source_ids"]),
        "quarantined_source_count": len(session["quarantined_source_ids"]),
        "run_ids": session["run_ids"],
        "audit_items": session["audit_items"],
        "pid": os.getpid(),
        "rss_gb": snap.rss_gb,
        "free_ram_gb": snap.free_gb,
        "memory_source": snap.source,
    }
    atomic_write_json(Path(path), heartbeat)


def _parse_utc_epoch(value: str) -> float:
    from datetime import datetime

    normalized = value.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized).timestamp()


def _install_signal_handler(heartbeat_path: str | Path) -> None:
    def _request_stop(signum: int, frame: Any) -> None:  # pragma: no cover - manual Ctrl-C path.
        del signum, frame
        global _STOP_REQUESTED
        _STOP_REQUESTED = True
        atomic_write_json(
            Path(heartbeat_path),
            {
                "schema": "FactoryDaemonHeartbeat.v1",
                "heartbeat_at": utc_now(),
                "status": "stop_requested_after_current_cycle",
            },
        )

    signal.signal(signal.SIGINT, _request_stop)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the Attractor Observatory Factory as a continuous daemon.")
    parser.add_argument("--cycles", type=int, default=0, help="Number of cycles to run; 0 means continuous.")
    parser.add_argument("--sleep-seconds", type=int, default=3600)
    parser.add_argument("--allow-network", action="store_true")
    parser.add_argument("--target-world", dest="target_worlds", action="append", default=None)
    parser.add_argument("--source-id", dest="source_ids", action="append", default=None)
    parser.add_argument("--store-root", default="reports/campaign_035/factory_store")
    parser.add_argument("--cache-dir", default="reports/campaign_035/source_cache")
    parser.add_argument("--run-root", default="control_room/cache/factory_runs")
    parser.add_argument("--trace-root", default="reports/campaign_035/traces")
    parser.add_argument("--session-ledger", default=str(DEFAULT_LEDGER))
    parser.add_argument("--state-path", default=str(DEFAULT_STATE))
    parser.add_argument("--heartbeat-path", default=str(DEFAULT_HEARTBEAT))
    parser.add_argument("--progress-root", default="reports/factory_daemon_progress")
    parser.add_argument("--disk-budget-mb", type=int, default=512)
    parser.add_argument("--retry-ceiling", type=int, default=3)
    parser.add_argument("--retry-base-seconds", type=float, default=2.0)
    parser.add_argument("--force-refresh", action="store_true", help="Clear all last_success_by_source entries before due-source selection.")
    parser.add_argument("--force-refresh-source", action="append", default=None, help="Clear one source_id from last_success_by_source before due-source selection. Repeatable.")
    args = parser.parse_args(argv)
    run_continuous_daemon(**vars(args))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
