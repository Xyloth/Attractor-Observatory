"""Snapshot endpoint for AI consumption.

Per CB-007 §5: a fresh AI agent (post-compaction Architect Claude,
fresh Codex 1.5x session, etc.) should be able to read ONE snapshot
file at session start instead of parsing 50 source files. This module
composes the structured digest from every adapter and writes it to
``control_room/snapshots/state_<UTC-timestamp>.json``.

Snapshots are append-only by file (each render writes a new file with
a UTC timestamp); the ``state_latest.json`` symlink-equivalent is
maintained as a stable read target. The directory is one of three
sidecar-writable paths permitted by the read-only enforcement test
(`control_room/{cache,snapshots,portfolio}/`).

D22 binding: every adapter's status is preserved verbatim in the
snapshot. Missing data is reported as "missing"; no plausible-defaults
pathway. AI consumers can rely on `snapshot[section]["status"] == "ok"`
to know real data is present.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from control_room.adapters import (
    parse_build_log,
    parse_builder_telemetry,
    parse_campaign_reports,
    parse_doctrine,
    parse_factory_store,
    parse_git_metadata,
    parse_methods_falsifiers,
    parse_negative_space,
    parse_pytest_cache,
)


SNAPSHOTS_DIR = Path(__file__).resolve().parent / "snapshots"
SNAPSHOT_LATEST = SNAPSHOTS_DIR / "state_latest.json"
SNAPSHOT_PRIOR = SNAPSHOTS_DIR / "state_prior.json"
SNAPSHOT_SCHEMA = "ControlRoomSnapshot.v1"
SNAPSHOT_GENERATION_COMMAND = "control_room.snapshot.write_snapshot()"


# Frozen mistake-catalog metadata mirroring docs/DOCTRINE.md & CB-005 rooms.
MISTAKE_CATALOG = [
    ("1", "Static-input contamination", "ratified"),
    ("2", "Direction inversion", "ratified"),
    ("3", "Soft enforcement / strict display", "ratified"),
    ("4", "Scenario-internal hardcoding", "ratified"),
    ("5", "Surface-coverage-without-substance", "ratified"),
    ("6", "Engineered passing", "ratified"),
    ("7", "Surface-labels-as-primitives", "ratified"),
    ("8", "Abstract-scalar-standing-in", "ratified"),
    ("9", "Spec-detail mismatch", "ratified"),
    ("10", "Test-architecture / substrate-presence mismatch", "ratified"),
    ("11", "Categorical confound through pooling", "ratified"),
    ("12", "Decorative completeness", "candidate"),
]


def build_snapshot() -> dict[str, Any]:
    """Compose the structured digest from every adapter."""
    git = parse_git_metadata(".")
    telemetry = parse_builder_telemetry()
    build_log = parse_build_log()
    campaigns = parse_campaign_reports()
    doctrine = parse_doctrine()
    falsifiers = parse_methods_falsifiers()
    negative_space = parse_negative_space()
    factory = parse_factory_store()
    pytest_cache = parse_pytest_cache()

    now = datetime.now(timezone.utc).isoformat()
    generation_binding = _generation_binding(git, now)

    snapshot: dict[str, Any] = {
        "schema": SNAPSHOT_SCHEMA,
        "generated_at": now,
        "generation_binding": generation_binding,
        "freshness_status": generation_binding["freshness_status"],
        "freshness_status_advisory_only": True,
        "freshness_policy": "D30: persisted freshness is advisory; load_latest/load_prior recompute against current HEAD at read time.",
        "purpose": (
            "Single-file digest for AI agents starting a fresh session. Read this file "
            "before parsing the 50+ source files referenced below. Each section carries "
            "{status, summary, details}. status=='ok' means real adapter data; "
            "status=='missing' means the source artifact is not on disk; "
            "status=='malformed' means the source exists but did not parse."
        ),
        "consumer_guidance": {
            "for_fresh_architect": [
                "Read 'project_health' first (1 sentence summary).",
                "Then 'recent_changes' (delta since last snapshot).",
                "Then 'current_agent_telemetry' for ongoing tasks.",
                "Then 'doctrine' for binding rules.",
                "Reach for the source files only when a section's details are insufficient.",
            ],
            "for_fresh_codex": [
                "Read 'pytest_status' and 'campaigns' first.",
                "Then 'detector_decline' (Campaign 016 honest-signal finding).",
                "Then 'mistake_catalog' for the 12 ratified failure classes.",
            ],
            "for_human_pi": [
                "All sections are dashboard-grade summaries; click into Control Room rooms for visual detail.",
            ],
        },
        "project_health": _project_health_summary(
            campaigns=campaigns, pytest_cache=pytest_cache, falsifiers=falsifiers,
            git=git, telemetry=telemetry,
        ),
        "current_agent_telemetry": _current_agent_telemetry(telemetry),
        "calibration_trajectory": _calibration_trajectory(telemetry),
        "campaigns": _campaigns_summary(campaigns),
        "doctrine": _doctrine_summary(doctrine),
        "mistake_catalog": _mistake_catalog_summary(),
        "falsifiers": _falsifiers_summary(falsifiers, negative_space),
        "evidence_boundaries": _evidence_private_summary(),
        "factory_state": _factory_state_summary(factory),
        "detector_decline": _detector_decline_summary(factory),
        # CB-009 T4 — atlas + audit-queue surfaces in the snapshot so a
        # fresh AI consumer reading state_latest.json sees the periodic
        # table coverage + the unresolved audit count without having to
        # walk reports/.
        "atlas_periodic_table": _atlas_periodic_table_summary(),
        "audit_inbox": _audit_inbox_snapshot_summary(),
        "git_state": _git_state_summary(git),
        "pytest_status": _pytest_status_summary(pytest_cache),
        "recent_changes": _recent_changes_summary(build_log),
        "raw_adapter_payloads": {
            "git_metadata": _strip_status(git),
            "builder_telemetry": _strip_status(telemetry),
            "build_log": _strip_status(build_log),
            "campaign_reports": _strip_status(campaigns),
            "doctrine": _strip_status(doctrine),
            "methods_falsifiers": _strip_status(falsifiers),
            "negative_space": _strip_status(negative_space),
            "factory_store": _strip_status(factory),
            "pytest_cache": _strip_status(pytest_cache),
        },
    }
    return snapshot


def write_snapshot(snapshot: dict[str, Any] | None = None) -> Path:
    """Write the snapshot to disk + maintain ``state_latest.json``.

    Returns the path of the timestamped snapshot file.
    """
    snapshot = snapshot if snapshot is not None else build_snapshot()
    SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    timestamped = SNAPSHOTS_DIR / f"state_{ts}.json"
    serialized = json.dumps(snapshot, sort_keys=True, indent=2, default=str)
    # Promote the previous "latest" to "prior" before overwriting (gives us
    # the diff baseline without a separate persistence pass).
    if SNAPSHOT_LATEST.exists():
        try:
            SNAPSHOT_PRIOR.write_text(SNAPSHOT_LATEST.read_text(encoding="utf-8"), encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            pass
    timestamped.write_text(serialized + "\n", encoding="utf-8")
    SNAPSHOT_LATEST.write_text(serialized + "\n", encoding="utf-8")
    return timestamped


def load_latest() -> dict[str, Any] | None:
    if not SNAPSHOT_LATEST.exists():
        return None
    try:
        payload = json.loads(SNAPSHOT_LATEST.read_text(encoding="utf-8"))
        return bind_snapshot_freshness(payload)
    except (OSError, json.JSONDecodeError):
        return None


def load_prior() -> dict[str, Any] | None:
    if not SNAPSHOT_PRIOR.exists():
        return None
    try:
        payload = json.loads(SNAPSHOT_PRIOR.read_text(encoding="utf-8"))
        return bind_snapshot_freshness(payload)
    except (OSError, json.JSONDecodeError):
        return None


def bind_snapshot_freshness(snapshot: dict[str, Any], *, repo_dir: str | Path = ".") -> dict[str, Any]:
    """Attach current-vs-generated freshness status to a loaded snapshot."""

    binding = dict(snapshot.get("generation_binding") or {})
    current = parse_git_metadata(repo_dir)
    if current.get("status") != "ok":
        binding["freshness_status"] = "unknown_git_unavailable"
        binding["freshness_checked_at"] = datetime.now(timezone.utc).isoformat()
    else:
        data = current["data"]
        current_sha = (data.get("last_commit") or {}).get("hash")
        current_branch = data.get("branch")
        stale_reasons = []
        if binding.get("commit_sha") and binding.get("commit_sha") != current_sha:
            stale_reasons.append("commit_moved")
        if binding.get("branch") and binding.get("branch") != current_branch:
            stale_reasons.append("branch_changed")
        binding["current_branch"] = current_branch
        binding["current_commit_sha"] = current_sha
        binding["freshness_status"] = "stale:" + ",".join(stale_reasons) if stale_reasons else "current"
        binding["freshness_checked_at"] = datetime.now(timezone.utc).isoformat()
    snapshot["generation_binding"] = binding
    snapshot["freshness_status"] = binding["freshness_status"]
    return snapshot


def diff_snapshots(prior: dict[str, Any] | None, current: dict[str, Any]) -> dict[str, Any]:
    """Diff two snapshots and return a structured delta payload.

    The diff focuses on user-meaningful changes: campaign status,
    pytest result, falsifier counts, doctrine count, what-changed log
    headers. First-launch (prior is None) returns an empty-state payload
    with explanation per D22.
    """
    if prior is None:
        return {
            "status": "first_launch",
            "rationale": (
                "No prior snapshot found. The first time the Control Room renders, "
                "there is no baseline to diff against. Subsequent renders will "
                "surface deltas here. Honest absence per D22."
            ),
            "deltas": [],
        }
    deltas: list[dict[str, Any]] = []
    # Campaigns delta — use membership (`in`) rather than None-status, since
    # a real campaign with no full_report.json carries status: None and
    # would otherwise show as "added" on every diff.
    prior_camps = {c.get("campaign_id"): c.get("status") for c in (prior.get("campaigns", {}).get("rows") or [])}
    current_camps = {c.get("campaign_id"): c.get("status") for c in (current.get("campaigns", {}).get("rows") or [])}
    for cid, status in current_camps.items():
        if cid is None:
            continue
        if cid not in prior_camps:
            deltas.append({"kind": "campaign_added", "id": cid, "status": status})
        elif prior_camps[cid] != status:
            deltas.append({
                "kind": "campaign_status_changed",
                "id": cid, "from": prior_camps[cid], "to": status,
            })
    # Pytest delta
    prior_pytest = (prior.get("pytest_status") or {}).get("last_failed_count")
    current_pytest = (current.get("pytest_status") or {}).get("last_failed_count")
    if prior_pytest != current_pytest and current_pytest is not None:
        deltas.append({"kind": "pytest_failed_count_changed", "from": prior_pytest, "to": current_pytest})
    # Falsifier count delta
    prior_fals = (prior.get("falsifiers") or {}).get("falsifier_count", 0)
    current_fals = (current.get("falsifiers") or {}).get("falsifier_count", 0)
    if prior_fals != current_fals:
        deltas.append({"kind": "falsifier_count_changed", "from": prior_fals, "to": current_fals})
    # Doctrine count delta
    prior_doc = (prior.get("doctrine") or {}).get("registry_count", 0)
    current_doc = (current.get("doctrine") or {}).get("registry_count", 0)
    if prior_doc != current_doc:
        deltas.append({"kind": "doctrine_registry_count_changed", "from": prior_doc, "to": current_doc})
    # New BUILD_LOG headers
    prior_headers = {e.get("header") for e in (prior.get("recent_changes") or {}).get("recent_entries", [])}
    for entry in (current.get("recent_changes") or {}).get("recent_entries", [])[:5]:
        h = entry.get("header")
        if h and h not in prior_headers:
            deltas.append({"kind": "build_log_entry_new", "date": entry.get("date"), "header": h})
    # Calibration delta
    prior_cb_delta = ((prior.get("calibration_trajectory") or {}).get("by_model") or {}).get("Claude (Builder)", {}).get("latest_delta")
    current_cb_delta = ((current.get("calibration_trajectory") or {}).get("by_model") or {}).get("Claude (Builder)", {}).get("latest_delta")
    if prior_cb_delta != current_cb_delta and current_cb_delta is not None:
        deltas.append({"kind": "claude_builder_latest_delta_changed", "from": prior_cb_delta, "to": current_cb_delta})
    return {
        "status": "delta_computed",
        "prior_generated_at": prior.get("generated_at"),
        "current_generated_at": current.get("generated_at"),
        "delta_count": len(deltas),
        "deltas": deltas,
    }


# ---------------------------------------------------------------------------
# Section builders — pure functions over adapter payloads
# ---------------------------------------------------------------------------


def _strip_status(adapter_payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "status": adapter_payload.get("status"),
        "rationale": adapter_payload.get("rationale"),
    }


def _generation_binding(git: dict[str, Any], generated_at: str) -> dict[str, Any]:
    data = git.get("data") if git.get("status") == "ok" else {}
    commit = (data or {}).get("last_commit") or {}
    return {
        "schema": "ControlRoomSnapshotGenerationBinding.v1",
        "branch": (data or {}).get("branch"),
        "commit_sha": commit.get("hash"),
        "commit_short": commit.get("short"),
        "generation_command": SNAPSHOT_GENERATION_COMMAND,
        "generation_timestamp": generated_at,
        "freshness_status": "current",
    }


def _project_health_summary(*, campaigns, pytest_cache, falsifiers, git, telemetry) -> dict[str, Any]:
    score = 100
    notes: list[str] = []
    if pytest_cache.get("status") == "ok":
        failed = pytest_cache["data"].get("last_failed_count", 0)
        nodeids = pytest_cache["data"].get("nodeid_count")
        if nodeids == 0:
            score -= 25
            notes.append("pytest cache reports zero collected tests")
        if failed and failed > 0:
            score -= 20
            notes.append(f"{failed} pytest tests failed last run")
    if campaigns.get("status") == "ok":
        rows = campaigns["data"]["campaigns"]
        green = sum(1 for c in rows if c.get("status") == "green")
        not_green = len(rows) - green
        if not_green > 0:
            score -= min(30, not_green * 5)
            notes.append(f"{not_green} of {len(rows)} campaigns not green")
    if falsifiers.get("status") == "ok":
        n_fals = falsifiers["data"].get("falsifier_doc_count", 0)
        if n_fals > 0:
            notes.append(f"{n_fals} falsifier records present (publishable per D17)")
    score = max(0, min(100, score))
    return {
        "status": "ok",
        "summary": f"Project health score: {score}/100. {'; '.join(notes) if notes else 'No active warnings.'}",
        "score": score,
        "notes": notes,
        "active_branch": (git.get("data") or {}).get("branch") if git.get("status") == "ok" else None,
    }


def _current_agent_telemetry(telemetry) -> dict[str, Any]:
    if telemetry.get("status") != "ok":
        return {"status": "missing", "rationale": telemetry.get("rationale")}
    by_model = telemetry["data"]["by_model"]
    rows = []
    for model, summary in by_model.items():
        rows.append({
            "model": model,
            "task_count": summary.get("task_count", 0),
            "delta_mean": summary.get("delta_mean"),
            "most_recent_task_id": summary.get("most_recent_task_id"),
        })
    return {"status": "ok", "summary": f"{len(rows)} agents with telemetry", "by_model": rows}


def _calibration_trajectory(telemetry) -> dict[str, Any]:
    if telemetry.get("status") != "ok":
        return {"status": "missing", "rationale": telemetry.get("rationale")}
    records = telemetry["data"]["records"]
    by_model: dict[str, list[dict[str, Any]]] = {}
    for r in records:
        if not isinstance(r.get("estimated_minutes"), (int, float)):
            continue
        if not isinstance(r.get("actual_minutes"), (int, float)):
            continue
        by_model.setdefault(r.get("model_name", "unknown"), []).append(r)
    summary: dict[str, Any] = {}
    for model, rows in by_model.items():
        rows = sorted(rows, key=lambda r: r.get("task_id", ""))
        deltas = [float(r["actual_minutes"]) / float(r["estimated_minutes"])
                  for r in rows if float(r["estimated_minutes"]) > 0]
        if not deltas:
            continue
        summary[model] = {
            "task_count": len(rows),
            "latest_delta": deltas[-1],
            "mean_delta": sum(deltas) / len(deltas),
            "min_delta": min(deltas),
            "max_delta": max(deltas),
        }
    return {"status": "ok", "summary": f"{len(summary)} models in trajectory", "by_model": summary}


def _campaigns_summary(campaigns) -> dict[str, Any]:
    if campaigns.get("status") != "ok":
        return {"status": "missing", "rationale": campaigns.get("rationale")}
    rows = campaigns["data"]["campaigns"]
    rows_summary = [
        {
            "campaign_id": c.get("campaign_id"),
            "status": c.get("status"),
            "passed_gate_count": c.get("passed_gate_count"),
            "gate_count": c.get("gate_count"),
        }
        for c in rows
    ]
    counts = Counter((c.get("status") or "unknown") for c in rows)
    return {
        "status": "ok",
        "summary": f"{len(rows)} campaigns; {counts.get('green', 0)} green, "
                   f"{counts.get('in_progress', 0)} in_progress, "
                   f"{counts.get('failed', 0)} failed",
        "rows": rows_summary,
        "status_counts": {str(k): v for k, v in counts.items()},
    }


def _doctrine_summary(doctrine) -> dict[str, Any]:
    if doctrine.get("status") != "ok":
        return {"status": "missing", "rationale": doctrine.get("rationale")}
    registry = doctrine["data"]["registry"]
    return {
        "status": "ok",
        "summary": f"{len(registry)} registry entries",
        "registry_count": len(registry),
        "ids": [d.get("id") for d in registry],
    }


def _mistake_catalog_summary() -> dict[str, Any]:
    return {
        "status": "ok",
        "summary": f"12 classes; 11 ratified, 1 candidate (Class 12 — Decorative Completeness)",
        "classes": [
            {"id": cls_id, "name": name, "status": status}
            for cls_id, name, status in MISTAKE_CATALOG
        ],
    }


def _falsifiers_summary(falsifiers, negative_space) -> dict[str, Any]:
    payload: dict[str, Any] = {"status": "ok"}
    if falsifiers.get("status") == "ok":
        f = falsifiers["data"]
        payload["falsifier_count"] = f.get("falsifier_doc_count", 0)
        payload["method_count"] = f.get("method_doc_count", 0)
        payload["falsifier_files"] = [d["name"] for d in f.get("falsifier_docs", [])]
    else:
        payload["falsifier_count"] = 0
        payload["falsifier_status"] = "missing"
    if negative_space.get("status") == "ok":
        payload["negative_space_count"] = negative_space["data"].get("entry_count", 0)
        payload["negative_space_files"] = [e["name"] for e in negative_space["data"].get("entries", [])]
    else:
        payload["negative_space_count"] = 0
        payload["negative_space_status"] = "missing"
    payload["summary"] = (
        f"{payload['falsifier_count']} falsifiers; "
        f"{payload['negative_space_count']} negative-space entries"
    )
    return payload


def _evidence_private_summary() -> dict[str, Any]:
    files = []
    total = 0
    for base in (Path("reports"), Path("papers/prereg")):
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.json")):
            if path.as_posix() == "reports/task_032_evidence_private_markers.json":
                continue
            try:
                payload = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                continue
            count = _count_evidence_private(payload)
            if count:
                files.append({"path": path.as_posix(), "evidence_private_count": count})
                total += count
    return {
        "status": "ok",
        "summary": f"{total} private/unshipped evidence references explicitly marked across {len(files)} files",
        "evidence_private_count": total,
        "file_count": len(files),
        "files": files[:25],
        "interpretation": "D23 candidate boundary: private trace evidence remains lineage, but is not presented as dereferenceable public artifact.",
    }


def _count_evidence_private(node: Any) -> int:
    if isinstance(node, dict):
        return (1 if node.get("evidence_private") is True else 0) + sum(_count_evidence_private(value) for value in node.values())
    if isinstance(node, list):
        return sum(_count_evidence_private(item) for item in node)
    return 0


def _factory_state_summary(factory) -> dict[str, Any]:
    if factory.get("status") != "ok":
        return {"status": "missing", "rationale": factory.get("rationale")}
    s = factory["data"].get("summary", {})
    return {
        "status": "ok",
        "summary": (
            f"empirical={s.get('empirical_count', 0)} normalized={s.get('normalized_count', 0)} "
            f"edges={s.get('edge_count', 0)} audit_queue={s.get('audit_queue_count', 0)} "
            f"private_evidence={s.get('evidence_private_count', 0)}"
        ),
        **s,
    }


def _detector_decline_summary(factory) -> dict[str, Any]:
    if factory.get("status") != "ok":
        return {"status": "missing", "rationale": factory.get("rationale")}
    s = factory["data"].get("summary", {})
    declined = s.get("detector_declined", 0)
    evals = s.get("detector_evaluations", 0)
    rate = s.get("detector_decline_rate", 0.0)
    note = (
        "Campaign 016 detector decline at low-level primitives is a load-bearing finding "
        "(D17: floor falsifiers are publishable). The 96/96 decline is rendered as honest "
        "signal in the Doctrine Console, not patched."
    )
    return {
        "status": "ok",
        "summary": f"detector_declined {declined}/{evals} (rate {rate:.2f})",
        "declined": declined,
        "evaluations": evals,
        "rate": rate,
        "interpretation_note": note,
    }


def _git_state_summary(git) -> dict[str, Any]:
    if git.get("status") != "ok":
        return {"status": "missing", "rationale": git.get("rationale")}
    d = git["data"]
    commit = d.get("last_commit", {})
    return {
        "status": "ok",
        "summary": f"branch {d.get('branch')} · last commit {commit.get('short')} ({commit.get('subject', '')[:60]})",
        "branch": d.get("branch"),
        "last_commit": commit,
        "recent_commit_count": d.get("recent_commit_count"),
    }


def _pytest_status_summary(pytest_cache) -> dict[str, Any]:
    if pytest_cache.get("status") != "ok":
        return {"status": "missing", "rationale": pytest_cache.get("rationale")}
    d = pytest_cache["data"]
    failed = d.get("last_failed_count", 0)
    nodes = d.get("nodeid_count")
    coverage = d.get("coverage_status")
    return {
        "status": "ok",
        "summary": f"pytest cache: {failed} last failed of {nodes if nodes is not None else '?'} nodeids ({coverage})",
        "last_failed_count": failed,
        "nodeid_count": nodes,
        "coverage_status": coverage,
    }


def _recent_changes_summary(build_log) -> dict[str, Any]:
    if build_log.get("status") != "ok":
        return {"status": "missing", "rationale": build_log.get("rationale")}
    entries = build_log["data"]["entries"][-10:][::-1]
    summary_entries = [
        {"date": e.get("date"), "header": e.get("header"), "kind": e.get("kind")}
        for e in entries
    ]
    return {
        "status": "ok",
        "summary": f"{len(entries)} most-recent BUILD_LOG entries",
        "recent_entries": summary_entries,
    }


# ---------------------------------------------------------------------------
# CB-009 T4 — Atlas + audit-inbox snapshot extensions
# ---------------------------------------------------------------------------


def _atlas_periodic_table_summary() -> dict[str, Any]:
    """Summarize the atlas periodic table for the snapshot.

    Returns per-motif row totals + grand totals so a fresh AI agent can
    see "which motifs touched which worlds" without invoking the
    Streamlit room. Mirrors the visible periodic-table tally rows.
    """
    try:
        from control_room.rooms.motif_atlas import (
            _WORLD_AXIS,
            _classify_motif_world_cell,
            _load_atlas_entries,
        )
    except ImportError as exc:
        return {"status": "missing", "rationale": f"motif_atlas import failed: {exc}"}

    entries = _load_atlas_entries()
    if not entries:
        return {
            "status": "missing",
            "rationale": "atlas/entries/ is empty or unreadable",
        }

    rows = []
    col_totals = {wid: 0 for wid, _, _ in _WORLD_AXIS}
    grand_total = 0
    for entry in entries:
        motif_id = entry.get("motif_id", "?")
        per_world = {}
        row_total = 0
        for wid, _, _ in _WORLD_AXIS:
            cell = _classify_motif_world_cell(entry, wid)
            per_world[wid] = {
                "count": cell["count"],
                "total": cell["total"],
                "status": cell["status"],
            }
            col_totals[wid] += cell["count"]
            row_total += cell["count"]
        grand_total += row_total
        rows.append({
            "motif_id": motif_id,
            "row_total": row_total,
            "per_world": per_world,
        })
    return {
        "status": "ok",
        "summary": (
            f"{len(entries)} motifs × {len(_WORLD_AXIS)} worlds; "
            f"{grand_total} cells fired across the table"
        ),
        "world_axis": [wid for wid, _, _ in _WORLD_AXIS],
        "rows": rows,
        "col_totals": col_totals,
        "grand_total": grand_total,
    }


def _audit_inbox_snapshot_summary() -> dict[str, Any]:
    """Summarize the live audit inbox: total/unresolved counts,
    high-severity preview list, and the inbox source files."""
    try:
        from control_room.rooms.factory_intake_dock import _audit_inbox_summary
    except ImportError as exc:
        return {"status": "missing", "rationale": f"factory_intake_dock import failed: {exc}"}

    s = _audit_inbox_summary()
    if not s["all_items"]:
        return {
            "status": "missing",
            "rationale": "no audit_queue.json items in reports/",
        }
    # Show the top 5 unresolved items (truncated reasons) so an AI
    # consumer sees concrete examples without expanding the full list.
    high_preview = [
        {
            "audit_id": i["audit_id"][:64],
            "severity": i["severity"],
            "reason": (i.get("reason") or "")[:120],
            "source_id": i.get("source_id", ""),
            "source_file": i.get("source_file", ""),
        }
        for i in s["unresolved"]
        if i["severity"] == "high"
    ][:5]
    source_files = sorted({i.get("source_file") for i in s["all_items"] if i.get("source_file")})
    return {
        "status": "ok",
        "summary": (
            f"{s['unresolved_total']} unresolved / {len(s['all_items'])} total "
            f"({s['high']} high · {s['medium']} med · {s['low']} low)"
        ),
        "unresolved_total": s["unresolved_total"],
        "resolved_total": s["resolved_total"],
        "by_severity": {
            "high": s["high"],
            "medium": s["medium"],
            "low": s["low"],
        },
        "high_severity_preview": high_preview,
        "source_files": source_files,
    }
