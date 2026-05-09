"""Per-world ingestion progress tracking.

CB-013 T5: writes ``reports/<task_id>/ingestion_progress.json`` per
world per session so the BUILDER_INGESTION_MONITORING_PLAYBOOK can
report "W1 at 47%, last cycle clean, 5 routine audits" without
parsing the full session ledger.

Schema (``IngestionProgress.v1``)::

    {
        "schema": "IngestionProgress.v1",
        "file_semantics": "current_operator_truth",
        "last_updated_at": "<ISO-8601 UTC>",
        "bound_to_state_hash": "sha256:<factory_daemon_state.json bytes>",
        "world_family": "crn",
        "session_id": "<sha256>",
        "started_at": "<ISO-8601 UTC>",
        "target_density": 50,
        "current_density": 23,
        "percent_complete": 0.46,
        "sources_completed": [...],
        "sources_in_flight": [...],
        "sources_pending": [...],
        "last_clean_cycle": "<ISO-8601 UTC>",
        "audit_queue_at_last_check": 5
    }

Targets are read from ``papers/methods/INGESTION_TARGETS.md`` (T3
deliverable). When the targets doc is absent or doesn't carry a row
for a world_family, ``target_density`` defaults to 0 and
``percent_complete`` to 0.0 (D22: never fabricate a target the PI
hasn't ratified).

Storage path: ``reports/factory_daemon_progress/<world_family>.json``.
One file per world; rewritten atomically each cycle. Caller is the
daemon's per-cycle finalize block.
"""

from __future__ import annotations

import json
import hashlib
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

from .persistence import atomic_write_json
from .schemas import sha256, utc_now


PROGRESS_ROOT = Path("reports/factory_daemon_progress")
INGESTION_TARGETS_DOC = Path("papers/methods/INGESTION_TARGETS.md")


# Per-world target density. Loaded lazily so a missing targets doc
# doesn't break the daemon (D22 honest absence). Cached after first
# read to avoid re-parsing every cycle.
_targets_cache: dict[str, int] | None = None


def load_target_densities(
    targets_doc: Path | str = INGESTION_TARGETS_DOC,
) -> dict[str, int]:
    """Parse ``papers/methods/INGESTION_TARGETS.md`` for per-world
    target densities. Returns ``{world_family: target_density}``.

    The doc shape (per CB-013 T3): a markdown table with rows of the
    form ``| <world_family> | <target_density> | ...``. Missing rows
    or absent file → empty dict (D22: no fabricated targets).
    """
    p = Path(targets_doc)
    if not p.exists():
        return {}
    targets: dict[str, int] = {}
    try:
        text = p.read_text(encoding="utf-8-sig")
    except OSError:
        return {}
    # Match table rows: | world | density | ...
    # We look for the marker `<!-- ingestion-targets:start -->` to
    # confine parsing to the canonical block (avoids matching any
    # narrative tables elsewhere in the doc).
    body = text
    if "<!-- ingestion-targets:start -->" in text:
        body = text.split("<!-- ingestion-targets:start -->", 1)[1]
        if "<!-- ingestion-targets:end -->" in body:
            body = body.split("<!-- ingestion-targets:end -->", 1)[0]
    for line in body.splitlines():
        m = re.match(r"\|\s*([a-z_][a-z0-9_]*)\s*\|\s*(\d+)\s*\|", line)
        if not m:
            continue
        wf, dens = m.group(1), int(m.group(2))
        targets[wf] = dens
    return targets


def write_ingestion_progress(
    *,
    session: dict[str, Any],
    state: dict[str, Any],
    store_root: str | Path,
    source_rows: list[dict[str, Any]],
    targets_doc: Path | str = INGESTION_TARGETS_DOC,
    progress_root: Path | str = PROGRESS_ROOT,
    state_path: Path | str | None = None,
) -> dict[str, Path]:
    """Write one progress file per world this session touched.

    Aggregates from session + state + source registry:
      * ``sources_completed`` — drawn from ``session.completed_source_ids``
      * ``sources_in_flight`` — sources with retries pending (best-effort)
      * ``sources_pending``   — registered but not yet completed in ``state``
      * ``current_density``   — record count for that world_family in
                                ``store_root/empirical_records.json``
      * ``audit_queue_at_last_check`` — count of items in store's
                                        audit_queue.json
    """
    targets = load_target_densities(targets_doc)
    progress_root_p = Path(progress_root)
    progress_root_p.mkdir(parents=True, exist_ok=True)

    record_counts = _record_counts_per_world(store_root)
    audit_count = _audit_queue_count(store_root)

    # Group sources by world so we can write per-world.
    by_world: dict[str, list[dict[str, Any]]] = {}
    for row in source_rows:
        wf = str(row.get("target_world") or row.get("world_family") or "unknown")
        by_world.setdefault(wf, []).append(row)

    completed_sources_set = set(session.get("completed_source_ids") or [])
    quarantined_set = set(session.get("quarantined_source_ids") or [])
    last_success_by_source = (state or {}).get("last_success_by_source", {})
    state_hash = _state_binding_hash(state=state or {}, state_path=state_path)
    force_refresh_invalidations = list((state or {}).get("force_refresh_invalidations") or [])

    written: dict[str, Path] = {}
    session_id = session.get("session_id") or sha256({k: v for k, v in session.items() if k != "session_id"})
    session_started = session.get("started_at") or utc_now()

    for wf, rows in by_world.items():
        all_source_ids = [r["source_id"] for r in rows]
        completed = sorted(s for s in all_source_ids if s in completed_sources_set or last_success_by_source.get(s))
        in_flight = sorted(s for s in all_source_ids if s in quarantined_set)
        pending = sorted(s for s in all_source_ids if s not in completed and s not in in_flight)
        target = int(targets.get(wf, 0))
        current = int(record_counts.get(wf, 0))
        percent = round(current / target, 4) if target > 0 else 0.0
        last_updated_at = utc_now()
        world_invalidations = [
            item for item in force_refresh_invalidations
            if item.get("source_id") in all_source_ids or item.get("clear_all")
        ]
        payload = {
            "schema": "IngestionProgress.v1",
            "file_semantics": "current_operator_truth",
            "history_policy": "pointer_file_only; historical progress belongs in versioned snapshot paths",
            "last_updated_at": last_updated_at,
            "bound_to_state_hash": state_hash,
            "world_family": wf,
            "session_id": session_id,
            "started_at": session_started,
            "target_density": target,
            "current_density": current,
            "percent_complete": percent,
            "sources_completed": completed,
            "sources_in_flight": in_flight,
            "sources_pending": pending,
            "last_clean_cycle": (
                session.get("completed_at") or ""
                if session.get("status") in {"complete", "stop_requested"}
                else ""
            ),
            "audit_queue_at_last_check": audit_count,
            "invalidated_by_force_refresh": world_invalidations,
            "writer": "factory_lowlevel.progress.write_ingestion_progress",
            "written_at": last_updated_at,
        }
        out = progress_root_p / f"{wf}.json"
        atomic_write_json(out, payload)
        written[wf] = out
    return written


def read_ingestion_progress(
    progress_root: Path | str = PROGRESS_ROOT,
    *,
    state_path: Path | str | None = None,
) -> dict[str, dict[str, Any]]:
    """Return ``{world_family: progress_payload}`` for the playbook.

    D22: missing progress files yield an empty dict, never fabricated
    progress numbers.
    """
    root = Path(progress_root)
    if not root.exists():
        return {}
    out: dict[str, dict[str, Any]] = {}
    for f in sorted(root.glob("*.json")):
        try:
            payload = json.loads(f.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        if state_path is not None and not _progress_fresh_for_state(payload, state_path):
            continue
        wf = payload.get("world_family") or f.stem
        out[wf] = payload
    return out


def _state_binding_hash(*, state: dict[str, Any], state_path: Path | str | None) -> str:
    if state_path is not None:
        p = Path(state_path)
        if p.exists() and p.is_file():
            return "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()
    return sha256(state)


def _progress_fresh_for_state(payload: dict[str, Any], state_path: Path | str) -> bool:
    expected = payload.get("bound_to_state_hash")
    if not expected:
        return False
    p = Path(state_path)
    if not p.exists() or not p.is_file():
        return False
    actual = "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()
    return expected == actual


def _record_counts_per_world(store_root: str | Path) -> dict[str, int]:
    """Count records in ``store_root/empirical_records.json`` per world.
    Returns empty dict if the store is missing (D22)."""
    er = Path(store_root) / "empirical_records.json"
    if not er.exists():
        return {}
    try:
        payload = json.loads(er.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}
    records = payload.get("records") if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        return {}
    counts: Counter[str] = Counter()
    for r in records:
        if isinstance(r, dict):
            counts[r.get("world_family", "unknown")] += 1
    return dict(counts)


def _audit_queue_count(store_root: str | Path) -> int:
    """Count items in ``store_root/audit_queue.json``. 0 if absent."""
    aq = Path(store_root) / "audit_queue.json"
    if not aq.exists():
        return 0
    try:
        payload = json.loads(aq.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return 0
    items = (
        payload.get("items")
        if isinstance(payload, dict)
        else payload
    )
    if isinstance(items, list):
        return len(items)
    return 0
