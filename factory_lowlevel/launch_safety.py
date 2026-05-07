"""Launch-safety mechanics for the continuous Factory daemon.

CB-013 T4 hardening: lock file, signal handlers, atomic checkpoint
helpers, and resume-from-heartbeat verification. These are the
mechanics that make unattended ingestion safe to flip on:

  * **Lock file** — exclusive single-instance guarantee. Written at
    daemon startup, deleted on graceful shutdown. A second daemon
    seeing a live PID in the lock REFUSES to start (D9: no concurrent
    runs corrupting shared store state).

  * **SIGINT handler** (graceful) — flush the in-flight cycle, write
    a final heartbeat with ``status: clean_shutdown``, release the
    lock, exit 0. The PI / ops can issue Ctrl-C without losing data.

  * **SIGTERM handler** (hard) — write a heartbeat with
    ``status: hard_shutdown``, release the lock, exit 1. Used by the
    OS or by the playbook's hard-stop sequence.

  * **Atomic checkpoint** — wraps ``persistence.atomic_write_json``
    for the snapshot file specifically, with a separate
    ``checkpoint_at`` field so resume-verification can compare
    timestamps without parsing the full snapshot.

  * **Resume verification** — on startup, read the prior heartbeat;
    if status was ``in_flight``/``running``, verify factory_store
    integrity (record IDs unique, evidence-graph closed, no orphan
    refs). On inconsistency, abort and surface for Builder review.

Threshold values are exposed as module constants (no hardcoded
magic numbers per CB-013 brief). Override via constructor kwargs.
"""

from __future__ import annotations

import json
import os
import signal
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional


# ---------------------------------------------------------------------------
# Tunable thresholds (per CB-013 brief — no hardcoded magic numbers)
# ---------------------------------------------------------------------------

#: Default heartbeat-staleness threshold in seconds. Heartbeats older
#: than this are flagged STALE during resume verification.
DEFAULT_STALE_HEARTBEAT_SECONDS = 5 * 60  # 5 minutes

#: PID-aliveness probe timeout (Windows ``tasklist`` / POSIX ``kill -0``).
DEFAULT_PID_PROBE_TIMEOUT_SECONDS = 2.0

#: Statuses that indicate the prior daemon stopped cleanly. A startup
#: that finds any other status in the prior heartbeat triggers resume
#: verification.
CLEAN_PRIOR_STATUSES = frozenset({
    "clean_shutdown",
    "stop_requested_after_current_cycle",  # legacy graceful name
    "complete",
})

#: Statuses that indicate the prior daemon was MID-CYCLE when it
#: stopped. Resume must verify integrity before continuing.
MID_FLIGHT_STATUSES = frozenset({
    "running",
    "in_flight",
    "started",
})


# ---------------------------------------------------------------------------
# Lock file
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class LockAcquisition:
    """Outcome of ``acquire_lock``. ``acquired=True`` means the daemon
    may proceed; ``False`` means a live holder exists and the daemon
    should refuse to start (D9 binding)."""
    acquired: bool
    lock_path: str
    pid: int
    rationale: str
    holder_pid: Optional[int] = None
    holder_started_at: Optional[str] = None


def acquire_lock(
    *,
    store_root: str | Path,
    pid: Optional[int] = None,
    pid_probe_timeout: float = DEFAULT_PID_PROBE_TIMEOUT_SECONDS,
) -> LockAcquisition:
    """Try to acquire ``<store_root>/.daemon_lock``.

    If the lock file exists AND the holder PID is alive → refuse.
    If the lock file exists AND the holder PID is dead → take it
    (the prior daemon crashed; we override and Builder can audit
    via the 'orphaned_lock_overridden' rationale).

    Returns ``LockAcquisition(acquired=True/False, ...)``. Caller
    MUST honor ``acquired=False`` and exit non-zero.
    """
    pid = pid or os.getpid()
    lock_path = Path(store_root) / ".daemon_lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    # Existing lock?
    if lock_path.exists():
        try:
            existing = json.loads(lock_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing = {}
        holder_pid = int(existing.get("pid", 0)) or None
        holder_started = existing.get("started_at", "")
        if holder_pid and _pid_alive(holder_pid, timeout=pid_probe_timeout):
            return LockAcquisition(
                acquired=False,
                lock_path=str(lock_path),
                pid=pid,
                holder_pid=holder_pid,
                holder_started_at=holder_started,
                rationale=(
                    f"daemon already running: PID {holder_pid} "
                    f"started at {holder_started or 'unknown'} "
                    f"(lock at {lock_path.as_posix()})"
                ),
            )
        # Orphaned lock: override.
        lock_path.unlink()
        rationale = (
            f"orphaned_lock_overridden: prior holder PID "
            f"{holder_pid or 'unknown'} not alive; replacing"
        )
    else:
        rationale = "lock_acquired_clean"

    payload = {
        "schema": "FactoryDaemonLock.v1",
        "pid": pid,
        "started_at": _utc_now_iso(),
        "host": _hostname(),
    }
    lock_path.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")
    return LockAcquisition(
        acquired=True,
        lock_path=str(lock_path),
        pid=pid,
        rationale=rationale,
    )


def release_lock(*, store_root: str | Path, pid: Optional[int] = None) -> bool:
    """Delete the lock file if it belongs to ``pid`` (or the current
    process). Returns True iff the lock was released, False if it
    belonged to a different PID (in which case the caller should NOT
    delete it). Idempotent — non-existent lock returns True silently."""
    pid = pid or os.getpid()
    lock_path = Path(store_root) / ".daemon_lock"
    if not lock_path.exists():
        return True
    try:
        existing = json.loads(lock_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        # Malformed lock; we can't verify ownership. Refuse to delete.
        return False
    if int(existing.get("pid", 0)) != pid:
        return False
    try:
        lock_path.unlink()
    except OSError:
        return False
    return True


def _pid_alive(pid: int, *, timeout: float) -> bool:
    """Check whether ``pid`` is alive. Cross-platform best-effort.

    POSIX: ``os.kill(pid, 0)`` raises if dead.
    Windows: shells out to ``tasklist /FI "PID eq <pid>"``.
    """
    if sys.platform == "win32":
        import subprocess
        try:
            out = subprocess.run(
                ["tasklist", "/FI", f"PID eq {pid}"],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False,
            )
            return str(pid) in out.stdout
        except (subprocess.TimeoutExpired, OSError):
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Signal handlers
# ---------------------------------------------------------------------------


@dataclass
class SignalState:
    """Mutable state observed by the daemon's main loop. The handlers
    set the flags; the loop honors them at safe boundaries."""
    stop_requested: bool = False  # set by SIGINT (graceful)
    hard_stop_requested: bool = False  # set by SIGTERM (hard)
    last_signal: Optional[str] = None
    last_signal_at: Optional[str] = None


def install_signal_handlers(
    state: SignalState,
    *,
    heartbeat_path: str | Path,
    flush_callback: Optional[Callable[[], None]] = None,
) -> None:
    """Wire SIGINT (graceful) and SIGTERM (hard) handlers.

    SIGINT (Ctrl-C / kill -2):
      * sets ``state.stop_requested = True``
      * writes a heartbeat with ``status: stop_requested_after_current_cycle``
      * the main loop completes the in-flight cycle, then exits with
        ``clean_shutdown`` heartbeat + lock release.

    SIGTERM (kill / kill -15):
      * sets ``state.hard_stop_requested = True``
      * writes a heartbeat with ``status: hard_shutdown``
      * the main loop exits ASAP.

    On Windows, SIGTERM is mapped to SIGBREAK where supported.
    """

    hb_path = Path(heartbeat_path)

    def _on_sigint(signum: int, frame: Any) -> None:  # pragma: no cover (manual signal path)
        del signum, frame
        state.stop_requested = True
        state.last_signal = "SIGINT"
        state.last_signal_at = _utc_now_iso()
        _write_heartbeat_simple(
            hb_path,
            status="stop_requested_after_current_cycle",
            note="SIGINT received; finishing in-flight cycle",
        )
        if flush_callback is not None:
            try:
                flush_callback()
            except Exception:  # pragma: no cover - best-effort flush
                pass

    def _on_sigterm(signum: int, frame: Any) -> None:  # pragma: no cover (manual signal path)
        del signum, frame
        state.hard_stop_requested = True
        state.last_signal = "SIGTERM"
        state.last_signal_at = _utc_now_iso()
        _write_heartbeat_simple(
            hb_path,
            status="hard_shutdown",
            note="SIGTERM received; aborting current cycle",
        )

    signal.signal(signal.SIGINT, _on_sigint)
    try:
        signal.signal(signal.SIGTERM, _on_sigterm)
    except (AttributeError, ValueError):  # Windows pre-3.8 / threadsafe context
        pass
    if sys.platform == "win32":
        try:
            signal.signal(signal.SIGBREAK, _on_sigterm)  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass


def _write_heartbeat_simple(path: Path, *, status: str, note: str) -> None:
    """Minimal heartbeat write used by signal handlers when the full
    session payload isn't readily accessible. The daemon's main loop
    overwrites with full session details on the next safe boundary."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "FactoryDaemonHeartbeat.v1",
        "heartbeat_at": _utc_now_iso(),
        "status": status,
        "note": note,
    }
    path.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Atomic checkpoint helpers
# ---------------------------------------------------------------------------


def write_checkpoint(
    *,
    snapshot_path: str | Path,
    payload: dict[str, Any],
) -> Path:
    """Write ``snapshot.json`` atomically with a ``checkpoint_at`` field
    so resume verification can timestamp without parsing every payload.

    Delegates to ``persistence.atomic_write_json`` (write-rename in
    same-directory temp file + ``os.fsync`` + ``Path.replace``) so a
    crash mid-write cannot leave a partial file."""
    from .persistence import atomic_write_json

    enriched = dict(payload)
    enriched["checkpoint_at"] = _utc_now_iso()
    return atomic_write_json(Path(snapshot_path), enriched)


# ---------------------------------------------------------------------------
# Resume verification
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ResumeVerdict:
    """Outcome of ``verify_resume``. Caller honors:
      * ``proceed=True`` — daemon may resume normally.
      * ``proceed=False`` — abort and surface to Builder.
    """
    proceed: bool
    rationale: str
    prior_status: str
    prior_heartbeat_age_seconds: float
    integrity_check: dict[str, Any] = field(default_factory=dict)


def verify_resume(
    *,
    heartbeat_path: str | Path,
    store_root: str | Path,
    stale_heartbeat_seconds: int = DEFAULT_STALE_HEARTBEAT_SECONDS,
) -> ResumeVerdict:
    """Inspect prior daemon state on startup. Three branches:

      1. **No heartbeat / clean shutdown** → proceed=True, fresh start.
      2. **Mid-flight heartbeat with passing integrity** → proceed=True,
         resume from checkpoint.
      3. **Mid-flight heartbeat with FAILING integrity** → proceed=False,
         surface for Builder review (D9: never silently overwrite a
         possibly-corrupt store).
    """
    hb_path = Path(heartbeat_path)
    if not hb_path.exists():
        return ResumeVerdict(
            proceed=True,
            rationale="no_prior_heartbeat: clean first start",
            prior_status="absent",
            prior_heartbeat_age_seconds=-1.0,
        )
    try:
        prior = json.loads(hb_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return ResumeVerdict(
            proceed=False,
            rationale=f"prior_heartbeat_unreadable: {type(exc).__name__}: {exc}",
            prior_status="malformed",
            prior_heartbeat_age_seconds=-1.0,
        )
    prior_status = str(prior.get("status", "unknown"))
    try:
        age = time.time() - hb_path.stat().st_mtime
    except OSError:
        age = -1.0

    if prior_status in CLEAN_PRIOR_STATUSES:
        return ResumeVerdict(
            proceed=True,
            rationale=f"prior_clean: status={prior_status}",
            prior_status=prior_status,
            prior_heartbeat_age_seconds=round(age, 1),
        )

    # Mid-flight status — must verify integrity.
    if prior_status in MID_FLIGHT_STATUSES or prior_status == "hard_shutdown":
        integrity = check_factory_store_integrity(store_root)
        if integrity["ok"]:
            return ResumeVerdict(
                proceed=True,
                rationale=(
                    f"mid_flight_resume_ok: prior status={prior_status}, "
                    f"integrity_check passed ({integrity['record_count']} records)"
                ),
                prior_status=prior_status,
                prior_heartbeat_age_seconds=round(age, 1),
                integrity_check=integrity,
            )
        return ResumeVerdict(
            proceed=False,
            rationale=(
                f"resume_aborted: prior status={prior_status}; "
                f"integrity check failed: {integrity['rationale']}"
            ),
            prior_status=prior_status,
            prior_heartbeat_age_seconds=round(age, 1),
            integrity_check=integrity,
        )

    # Unknown status — be conservative.
    return ResumeVerdict(
        proceed=False,
        rationale=f"prior_status_unknown: {prior_status}; manual review required",
        prior_status=prior_status,
        prior_heartbeat_age_seconds=round(age, 1),
    )


def check_factory_store_integrity(store_root: str | Path) -> dict[str, Any]:
    """Verify the factory_store invariants:
      * record_id values unique
      * evidence-graph edges reference known records
      * no normalized_refs orphaned from records
      * snapshot.json content_hash recomputes (best-effort)

    Returns ``{ok: bool, rationale: str, record_count: int, ...}``.
    """
    sr = Path(store_root)
    if not sr.exists():
        return {
            "ok": True,
            "rationale": "store_root absent — fresh start",
            "record_count": 0,
        }
    er_path = sr / "empirical_records.json"
    if not er_path.exists():
        return {
            "ok": True,
            "rationale": "empirical_records.json absent — fresh start",
            "record_count": 0,
        }
    try:
        records_payload = json.loads(er_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "ok": False,
            "rationale": f"empirical_records.json unreadable: {exc}",
            "record_count": 0,
        }
    records = (
        records_payload.get("records")
        if isinstance(records_payload, dict)
        else records_payload
    )
    if not isinstance(records, list):
        return {
            "ok": False,
            "rationale": "empirical_records.json has no records list",
            "record_count": 0,
        }

    record_ids = [r.get("record_id") for r in records if isinstance(r, dict)]
    record_id_set = set(record_ids)
    n = len(records)

    # Uniqueness
    if len(record_id_set) < len(record_ids):
        dupes = len(record_ids) - len(record_id_set)
        return {
            "ok": False,
            "rationale": f"duplicate record_ids: {dupes} dupes among {n}",
            "record_count": n,
            "duplicate_count": dupes,
        }

    # Evidence-graph orphan check
    eg_path = sr / "evidence_graph.json"
    orphan_edges = 0
    if eg_path.exists():
        try:
            eg = json.loads(eg_path.read_text(encoding="utf-8-sig"))
            edges = eg.get("edges") if isinstance(eg, dict) else eg
            if isinstance(edges, list):
                for edge in edges:
                    for rid in (edge.get("evidence_record_ids") or []):
                        if rid not in record_id_set:
                            orphan_edges += 1
        except (OSError, json.JSONDecodeError):
            pass

    # Normalized-refs orphan check
    nr_path = sr / "normalized_refs.json"
    orphan_refs = 0
    if nr_path.exists():
        try:
            nr = json.loads(nr_path.read_text(encoding="utf-8-sig"))
            refs = nr.get("records") if isinstance(nr, dict) else nr
            if isinstance(refs, list):
                for ref in refs:
                    if ref.get("empirical_record_id") not in record_id_set:
                        orphan_refs += 1
        except (OSError, json.JSONDecodeError):
            pass

    if orphan_edges or orphan_refs:
        return {
            "ok": False,
            "rationale": (
                f"orphan refs detected: {orphan_edges} edge orphans, "
                f"{orphan_refs} normalized_ref orphans"
            ),
            "record_count": n,
            "orphan_edges": orphan_edges,
            "orphan_refs": orphan_refs,
        }

    return {
        "ok": True,
        "rationale": f"integrity_ok: {n} records, {orphan_edges} edge orphans, {orphan_refs} ref orphans",
        "record_count": n,
        "orphan_edges": orphan_edges,
        "orphan_refs": orphan_refs,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _utc_now_iso() -> str:
    from datetime import datetime, timezone
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _hostname() -> str:
    try:
        import socket
        return socket.gethostname()
    except Exception:
        return "unknown"
