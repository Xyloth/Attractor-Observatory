"""Factory Intake Dock - Room 9 live multi-world console.

TASK-033 turns this room from a low-level preview into a daemon-backed FIRE
console. The UI aims source adapters at target worlds, starts the autonomous
Factory subprocess, polls live stage state, and renders the persisted run
record. No Control Room code fabricates records or writes Factory science
state; the subprocess owns ingestion/simulation/evaluation writes.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from control_room.components import (
    metric_card,
    panel,
    render_empty_state,
    render_html,
    room_emblem,
    status_pill,
)


ROOM_ID = "factory_intake_dock"
ROOM_NAME = "Factory Intake Dock"
ROOM_ICON = ">>"
ROOM_TAGLINE = "Aim the autonomous Factory at real sources, FIRE, and watch traces land."
ROOM_PHASE = "Phase 2"

REPO_ROOT = Path(__file__).resolve().parents[2]
CACHE_DIR = REPO_ROOT / "control_room" / "cache"
RUN_ROOT = CACHE_DIR / "factory_runs"
SUBPROCESS_STATE_PATH = CACHE_DIR / "factory_subprocess_state.json"
LIVE_STATE_PATH = RUN_ROOT / "latest_state.json"
LATEST_RUN_PATH = RUN_ROOT / "latest_run.json"
SESSION_LEDGER = REPO_ROOT / "project_telemetry" / "low_level_factory_sessions.jsonl"

PIPELINE_STAGES = (
    ("download", "Download"),
    ("parse", "Parse"),
    ("normalize", "Normalize"),
    ("route", "Route"),
    ("world_simulate", "World simulate"),
    ("motif_evaluate", "Motif evaluate"),
    ("audit", "Audit"),
)


def render() -> None:
    import streamlit as st

    render_html(room_emblem(ROOM_NAME, ROOM_TAGLINE, ROOM_ID))

    sources = _discover_sources()
    latest_run = _read_json(LATEST_RUN_PATH)
    live_state = _read_json(LIVE_STATE_PATH)
    subprocess_state = _read_subprocess_state()
    in_flight = _subprocess_in_flight(subprocess_state)
    recent_runs = _load_recent_runs()

    # CB-009 T3 — live audit-queue badge under the room emblem so the
    # PI sees "10 unresolved" before scrolling to the inbox section.
    audit_summary = _audit_inbox_summary()
    if audit_summary["unresolved_total"] > 0:
        render_html(
            f'<div style="display:inline-flex;align-items:center;gap:10px;'
            f'background:var(--bg-panel,#121826);border:1px solid var(--warning,#f5a623);'
            f'border-radius:999px;padding:6px 14px;margin:6px 0 14px;'
            f'box-shadow:0 0 16px rgba(245,166,35,0.18);">'
            f'<span style="font-family:var(--font-mono,monospace);font-size:0.74rem;'
            f'color:var(--warning,#f5a623);letter-spacing:0.06em;text-transform:uppercase;">audit inbox</span>'
            f'<span style="font-family:var(--font-display,sans-serif);font-size:1.2rem;'
            f'color:var(--fg1,#f8f9fa);font-weight:600;">{audit_summary["unresolved_total"]}</span>'
            f'<span style="font-family:var(--font-mono,monospace);font-size:0.7rem;color:var(--fg4,#6c7484);">'
            f'unresolved · {audit_summary["high"]} high / {audit_summary["medium"]} med / {audit_summary["low"]} low</span>'
            f'</div>'
        )

    cols = st.columns(4)
    with cols[0]:
        render_html(metric_card("Subprocess", "running" if in_flight else "idle", "active" if in_flight else "verified", f"pid {subprocess_state.get('pid')}" if in_flight else "ready"))
    with cols[1]:
        render_html(metric_card("Last run", (latest_run.get("run_id") or "none")[:12], "verified" if latest_run else "unavailable", latest_run.get("completed_at", "no run")[:19].replace("T", " ")))
    with cols[2]:
        render_html(metric_card("Life forms", str(len(latest_run.get("life_forms", []))) if latest_run else "0", "trace" if latest_run else "unavailable", "simulated trace records"))
    with cols[3]:
        warnings = len(latest_run.get("warnings", [])) + len(latest_run.get("routing_rejections", [])) if latest_run else 0
        render_html(metric_card("Audit signals", str(warnings), "warning" if warnings else "verified", "warnings + rejections"))

    # CB-009 T3 — Audit-Queue Inbox section
    _render_audit_inbox(audit_summary)

    st.markdown('<span class="cap">aim - target world and source adapter</span>', unsafe_allow_html=True)
    by_world: dict[str, list[dict[str, Any]]] = {}
    for source in sources:
        by_world.setdefault(source["target_world"], []).append(source)
    world_options = sorted(by_world)
    selected_worlds = st.multiselect(
        "target worlds",
        options=world_options,
        default=[world for world in world_options if world in {"crn", "field", "ecosystem", "origins_chemistry", "quasispecies"}],
        format_func=lambda world: _world_label(world, by_world),
        key="factory_dock_target_worlds",
    )
    selected_source_options = [source for world in selected_worlds for source in by_world.get(world, [])]
    selected_source_ids = st.multiselect(
        "source adapters",
        options=[source["source_id"] for source in selected_source_options],
        default=[source["source_id"] for source in selected_source_options],
        format_func=lambda source_id: _source_label(source_id, sources),
        key="factory_dock_sources",
    )

    st.markdown('<span class="cap">parameters - source-bound inputs</span>', unsafe_allow_html=True)
    param_cols = st.columns(5)
    selected_set = set(selected_source_ids)
    with param_cols[0]:
        if "source.kegg.ecoli_mg1655.metabolic_network" in selected_set:
            st.text_input("KEGG organism", value="eco (E. coli K-12 MG1655)", disabled=True, key="factory_param_kegg")
    with param_cols[1]:
        if "source.peer_reviewed.reaction_diffusion_benchmarks" in selected_set:
            st.selectbox("W3 benchmark", options=["all bundled benchmarks", "gray_scott", "brusselator", "schnakenberg"], index=0, disabled=True, key="factory_param_w3")
    with param_cols[2]:
        if "source.gbif.jornada_basin.ecosystem_occurrences" in selected_set:
            st.text_input("GBIF site", value="Jornada Basin bbox", disabled=True, key="factory_param_w6")
    with param_cols[3]:
        if "source.peer_reviewed.prebiotic_chemistry_catalog" in selected_set:
            st.selectbox("W9 catalog", options=["all bundled DOI records", "surface_stabilized_closure", "gradient_anchored_protocell"], index=0, disabled=True, key="factory_param_w9")
    with param_cols[4]:
        if "source.ncbi.hiv1.reference_quasispecies_pilot" in selected_set:
            st.text_input("NCBI accession", value="K03455.1", disabled=True, key="factory_param_ncbi")

    options_cols = st.columns([1, 1, 4])
    with options_cols[0]:
        allow_network = st.checkbox("allow network", value=False, key="factory_dock_allow_network")
    with options_cols[1]:
        live_mode = st.checkbox("live poll", value=True, key="factory_dock_live_poll")
    with options_cols[2]:
        render_html(panel("Route preview", _route_preview(sources, selected_source_ids)))

    # CB-011 fix #7 — surface the FIRE-button confirmation marker.
    # Builder ran a real cycle end-to-end on the date in the marker;
    # James can see "confirmed working at <UTC>" without having to
    # press FIRE blindly.
    confirmation_path = CACHE_DIR / "fire_button_confirmed.json"
    if confirmation_path.exists():
        try:
            confirm = json.loads(confirmation_path.read_text(encoding="utf-8-sig"))
            ts = confirm.get("confirmed_working_at", "")
            results = confirm.get("results", {})
            render_html(
                f'<div style="margin:8px 0;padding:10px 14px;'
                f'background:rgba(61,220,132,0.06);border:1px solid var(--verified,#3ddc84);'
                f'border-radius:12px;display:flex;align-items:center;gap:14px;">'
                f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;'
                f'background:var(--verified,#3ddc84);box-shadow:0 0 8px rgba(61,220,132,0.6);"></span>'
                f'<div style="font-family:var(--font-mono);font-size:0.78rem;color:var(--fg2);">'
                f'<b style="color:var(--verified,#3ddc84);">FIRE button confirmed working</b> '
                f'at {ts} · {results.get("wall_clock_seconds","?")}s cycle · '
                f'{results.get("life_form_count","?")} life forms · '
                f'<code style="color:var(--fg3);">{(results.get("run_id","")or"")[:30]}…</code>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
        except (OSError, json.JSONDecodeError):
            pass

    fire_disabled = in_flight or not selected_source_ids
    if st.button("FIRE - run multi-world Factory", type="primary", disabled=fire_disabled, use_container_width=True, key="factory_dock_fire"):
        _fire(allow_network=allow_network, target_worlds=selected_worlds, source_ids=selected_source_ids)
        st.rerun()

    # CB-011 fix #8/#10 — smoothness: only poll FAST (1.5 s) while a
    # cycle is actually in flight. When idle, slow to 8 s so the room
    # stops re-rendering every 1.5 s and the rest of the dashboard
    # feels iOS-smooth. James reported room-switching lag from the
    # tight pre-CB-011 polling loop.
    if hasattr(st, "autorefresh"):
        if in_flight:
            st.autorefresh(interval=1500, key="factory_dock_live_refresh_active")
        elif live_mode:
            st.autorefresh(interval=8000, key="factory_dock_live_refresh_idle")

    st.markdown('<span class="cap">pipeline - live stage state</span>', unsafe_allow_html=True)
    render_html(_pipeline_visual(live_state=live_state, in_flight=in_flight, latest_run=latest_run))
    if live_state:
        render_html(panel("Latest stage", _stage_details(live_state)))

    if subprocess_state.get("last_error"):
        render_html(
            '<div class="empty-state" style="border-color: var(--failed); border-style: solid;">'
            '<div class="empty-label" style="color: var(--failed);">subprocess failed</div>'
            f'<div class="empty-reason">{subprocess_state.get("last_error", "")[:900]}</div>'
            "</div>"
        )

    st.markdown('<span class="cap">life forms - real trace outputs</span>', unsafe_allow_html=True)
    life_forms = latest_run.get("life_forms", []) if latest_run else []
    if life_forms:
        render_html(panel("Live results stream", _life_form_rows(life_forms)))
        labels = [f'{item.get("world_family")} - {item.get("canonical_name", item.get("record_id", ""))}' for item in life_forms]
        selected_label = st.selectbox("drill down", options=labels, key="factory_life_form_drilldown")
        selected = life_forms[labels.index(selected_label)]
        with st.expander("trace + lens evaluations", expanded=True):
            st.json(_drilldown_payload(selected, latest_run))
    else:
        render_empty_state(
            reason="no multi-world Factory run has produced life-form trace outputs yet",
            expected_artifact="press FIRE to create control_room/cache/factory_runs/latest_run.json",
        )

    st.markdown('<span class="cap">real-data motif fire rates</span>', unsafe_allow_html=True)
    rates = latest_run.get("motif_fire_rates", []) if latest_run else []
    if rates:
        render_html(panel("Per world x motif", _rate_rows(rates)))
    else:
        render_empty_state(reason="no motif-evaluation output yet", expected_artifact="latest_run.json motif_fire_rates")

    st.markdown('<span class="cap">run history</span>', unsafe_allow_html=True)
    if recent_runs:
        render_html(panel("Recent FIRE records", _history_rows(recent_runs[-12:])))
    else:
        render_empty_state(reason=f"no runs in {SESSION_LEDGER.relative_to(REPO_ROOT).as_posix()}", expected_artifact="FIRE creates a session-ledger row")


def _discover_sources() -> list[dict[str, Any]]:
    try:
        from factory_lowlevel.live_pipeline import available_adapters
    except Exception:
        return []
    try:
        return available_adapters()
    except Exception:
        return []


def _world_label(world: str, by_world: dict[str, list[dict[str, Any]]]) -> str:
    label = by_world.get(world, [{}])[0].get("target_world_label", world)
    return f"{label} ({len(by_world.get(world, []))} source)"


def _source_label(source_id: str, sources: list[dict[str, Any]]) -> str:
    for source in sources:
        if source["source_id"] == source_id:
            return f'{source.get("target_world_label", source.get("target_world"))}: {source.get("name", source_id)}'
    return source_id


def _route_preview(sources: list[dict[str, Any]], selected_source_ids: list[str]) -> str:
    if not selected_source_ids:
        return '<div style="color:var(--warning);font-family:var(--font-body);">No source selected. FIRE is disabled.</div>'
    rows = []
    for source in sources:
        if source["source_id"] not in selected_source_ids:
            continue
        rows.append(
            '<div style="display:grid;grid-template-columns:190px 1fr 120px;gap:12px;align-items:center;'
            'padding:8px 0;border-bottom:1px dashed var(--border);">'
            f'{status_pill(source.get("target_world_label", source["target_world"]), status="trace")}'
            f'<span style="font-family:var(--font-body);color:var(--fg2);font-size:0.9rem;">{source["name"]}</span>'
            f'<span style="font-family:var(--font-mono);color:var(--fg4);font-size:0.72rem;">{source.get("refresh_cadence", "")}</span>'
            "</div>"
        )
    return "".join(rows)


def _pipeline_visual(*, live_state: dict[str, Any], in_flight: bool, latest_run: dict[str, Any]) -> str:
    current = live_state.get("stage")
    done = latest_run and not in_flight
    cells = []
    for stage_id, label in PIPELINE_STAGES:
        if in_flight and stage_id == current:
            color = "var(--active)"
            state = "running"
            anim = "animation: pulse-soft var(--motion-pulse) ease-in-out infinite;"
        elif done or _stage_seen(live_state, stage_id):
            color = "var(--verified)"
            state = "done"
            anim = ""
        else:
            color = "var(--fg5)"
            state = "idle"
            anim = ""
        cells.append(
            f'<div style="flex:1;min-width:0;padding:12px 10px;background:var(--bg-panel);border-left:3px solid {color};'
            f'border-radius:8px;text-align:center;box-shadow:0 0 16px -10px {color};{anim}">'
            f'<div style="font-family:var(--font-mono);font-size:0.66rem;color:var(--fg4);text-transform:uppercase;">{stage_id}</div>'
            f'<div style="font-family:var(--font-display);font-size:0.9rem;color:{color};font-weight:600;">{label}</div>'
            f'<div style="font-family:var(--font-body);font-size:0.68rem;color:var(--fg4);">{state}</div>'
            "</div>"
        )
    return f'<div style="display:flex;gap:8px;align-items:stretch;margin-bottom:14px;">{"".join(cells)}</div>'


def _stage_seen(live_state: dict[str, Any], stage_id: str) -> bool:
    return any(row.get("stage") == stage_id for row in live_state.get("stage_history", []))


def _stage_details(live_state: dict[str, Any]) -> str:
    rows = []
    for key in ("stage", "status", "record_count", "normalized_count", "trace_count", "life_form_count", "audit_count", "latest_record", "run_id"):
        if key in live_state:
            rows.append(
                '<div style="display:grid;grid-template-columns:150px 1fr;gap:12px;padding:4px 0;border-bottom:1px dashed var(--border);">'
                f'<span style="font-family:var(--font-mono);color:var(--fg4);font-size:0.74rem;">{key}</span>'
                f'<span style="font-family:var(--font-body);color:var(--fg2);font-size:0.9rem;">{live_state[key]}</span>'
                "</div>"
            )
    return "".join(rows)


def _life_form_rows(life_forms: list[dict[str, Any]]) -> str:
    rows = []
    for item in life_forms:
        fires = item.get("motif_fires", {})
        fired = [name for name, value in fires.items() if value]
        motif_text = ", ".join(fired) if fired else "no motif fires"
        status = "trace" if fired else "warning"
        rows.append(
            '<div style="display:grid;grid-template-columns:170px 1fr 220px 130px;gap:12px;align-items:center;'
            'padding:9px 0;border-bottom:1px dashed var(--border);">'
            f'{status_pill(item.get("world_family", "unknown"), status="trace")}'
            f'<span style="font-family:var(--font-body);color:var(--fg1);font-size:0.92rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{item.get("canonical_name", item.get("record_id", ""))}</span>'
            f'<span style="font-family:var(--font-mono);color:var(--fg3);font-size:0.75rem;">{motif_text}</span>'
            f'{status_pill(item.get("status", "unknown"), status=status)}'
            "</div>"
        )
    return "".join(rows)


def _drilldown_payload(selected: dict[str, Any], latest_run: dict[str, Any]) -> dict[str, Any]:
    trace_id = selected.get("trace_id")
    evaluations = [
        {
            "lens_id": row["lens_id"],
            "motif_id": row["motif_id"],
            "declined": row["declined"],
            "prediction_score": row["prediction_score"],
            "decline_reason": row.get("decline_reason"),
        }
        for row in latest_run.get("lens_evaluations", [])
        if row.get("trace_id") == trace_id
    ]
    return {
        "life_form": selected,
        "lens_evaluations": evaluations,
    }


def _rate_rows(rates: list[dict[str, Any]]) -> str:
    rows = []
    for row in rates:
        status = "verified" if row.get("fire_count", 0) else "warning"
        rows.append(
            '<div style="display:grid;grid-template-columns:170px 180px 120px 1fr;gap:12px;align-items:center;'
            'padding:7px 0;border-bottom:1px dashed var(--border);">'
            f'{status_pill(row.get("world_family", ""), status="trace")}'
            f'<span style="font-family:var(--font-mono);color:var(--fg2);font-size:0.78rem;">{row.get("motif")}</span>'
            f'{status_pill(str(row.get("fire_count", 0)) + "/" + str(row.get("trace_count", 0)), status=status)}'
            f'<span style="font-family:var(--font-body);color:var(--fg3);font-size:0.86rem;">fire rate {row.get("fire_rate")}</span>'
            "</div>"
        )
    return "".join(rows)


def _history_rows(recent_runs: list[dict[str, Any]]) -> str:
    rows = []
    for row in reversed(recent_runs):
        rows.append(
            '<div style="display:grid;grid-template-columns:170px 180px 1fr 130px;gap:12px;align-items:center;'
            'padding:7px 0;border-bottom:1px dashed var(--border);">'
            f'<span style="font-family:var(--font-mono);color:var(--fg4);font-size:0.72rem;">{(row.get("recorded_at") or "")[:19].replace("T", " ")}</span>'
            f'<span style="font-family:var(--font-mono);color:var(--fg2);font-size:0.72rem;">{(row.get("run_id") or "")[:16]}</span>'
            f'<span style="font-family:var(--font-body);color:var(--fg3);font-size:0.86rem;">{", ".join(row.get("target_worlds", [])) or row.get("trigger", "")}</span>'
            f'{status_pill(str(row.get("life_form_count", "-")) + " traces", status="trace")}'
            "</div>"
        )
    return "".join(rows)


def _fire(*, allow_network: bool, target_worlds: list[str], source_ids: list[str]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {"allow_network": bool(allow_network), "target_worlds": target_worlds, "source_ids": source_ids}
    code = (
        "from factory_lowlevel.daemon import run_multi_world_factory_cycle;"
        "import json;"
        f"args=json.loads({json.dumps(json.dumps(payload))});"
        "r=run_multi_world_factory_cycle(**args);"
        "print(json.dumps({'ok': True, 'run_id': r.get('run_id')}))"
    )
    cmd = [sys.executable, "-c", code]
    env = dict(os.environ)
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    creationflags = 0x08000000 if sys.platform == "win32" else 0
    stdout_path = CACHE_DIR / "factory_subprocess_stdout.log"
    stderr_path = CACHE_DIR / "factory_subprocess_stderr.log"
    proc = subprocess.Popen(
        cmd,
        cwd=str(REPO_ROOT),
        env=env,
        stdout=stdout_path.open("wb"),
        stderr=stderr_path.open("wb"),
        creationflags=creationflags,
    )
    state = {
        "pid": proc.pid,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "allow_network": bool(allow_network),
        "target_worlds": target_worlds,
        "source_ids": source_ids,
        "stdout_path": str(stdout_path),
        "stderr_path": str(stderr_path),
    }
    SUBPROCESS_STATE_PATH.write_text(json.dumps(state, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {}


def _read_subprocess_state() -> dict[str, Any]:
    return _read_json(SUBPROCESS_STATE_PATH)


def _subprocess_in_flight(state: dict[str, Any]) -> bool:
    pid = state.get("pid")
    if not pid or state.get("last_exited_at"):
        return False
    try:
        if sys.platform == "win32":
            out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True, timeout=2, check=False)
            alive = str(pid) in out.stdout
        else:
            os.kill(pid, 0)
            alive = True
    except (OSError, subprocess.SubprocessError):
        alive = False
    if alive:
        return True
    state["last_exited_at"] = datetime.now(timezone.utc).isoformat()
    stderr_path = Path(state.get("stderr_path", ""))
    if stderr_path.exists():
        stderr = stderr_path.read_text(encoding="utf-8", errors="replace").strip()
        if stderr:
            state["last_error"] = stderr
    SUBPROCESS_STATE_PATH.write_text(json.dumps(state, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return False


def _load_recent_runs() -> list[dict[str, Any]]:
    if not SESSION_LEDGER.exists():
        return []
    rows: list[dict[str, Any]] = []
    try:
        for line in SESSION_LEDGER.read_text(encoding="utf-8-sig").splitlines():
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    except OSError:
        return []
    return rows


# ---------------------------------------------------------------------------
# CB-009 T3 — Audit-Queue Inbox
# ---------------------------------------------------------------------------


AUDIT_RESOLUTION_DIR = CACHE_DIR / "audit_resolutions"


def _normalize_audit_item(item: dict[str, Any], source_path: Path) -> dict[str, Any]:
    """Coerce heterogeneous audit-item shapes into the inbox row schema.

    Different daemons / campaigns use different keys (campaign_011 uses
    item_id+priority+reason; factory_store uses audit_id+severity+
    recommended_action+reason+record_id+source_id). This normalizes to
    a single shape so the inbox can render uniformly.
    """
    audit_id = item.get("audit_id") or item.get("item_id") or ""
    # Severity normalization: factory_store uses 'high|medium|low';
    # campaign_011 uses numeric priority (8/9 commonly). Map any
    # priority >= 8 to 'high', 4-7 to 'medium', else 'low'.
    raw_sev = item.get("severity")
    if raw_sev:
        severity = str(raw_sev).lower()
    else:
        prio = item.get("priority")
        if isinstance(prio, (int, float)):
            severity = "high" if prio >= 8 else "medium" if prio >= 4 else "low"
        else:
            severity = "medium"
    return {
        "audit_id": audit_id,
        "severity": severity,
        "reason": item.get("reason", ""),
        "source_id": item.get("source_id") or item.get("source", ""),
        "record_id": item.get("record_id", ""),
        "recommended_action": item.get("recommended_action", item.get("action", "")),
        "created_at": item.get("created_at", item.get("recorded_at", "")),
        "raw_priority": item.get("priority"),
        "source_file": str(source_path.relative_to(REPO_ROOT)) if source_path.is_absolute() else str(source_path),
    }


def _audit_inbox_load_all() -> list[dict[str, Any]]:
    """Scan reports/ for audit_queue.json files and merge into a single
    inbox list. Per CB-009 T3, sources include factory_store/,
    daemon_store/, and campaign-root audit_queue.json files."""
    inbox: list[dict[str, Any]] = []
    reports_root = REPO_ROOT / "reports"
    if not reports_root.exists():
        return inbox
    for q in sorted(reports_root.rglob("audit_queue.json")):
        try:
            payload = json.loads(q.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            items = payload.get("items") or payload.get("records") or []
        elif isinstance(payload, list):
            items = payload
        else:
            items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            inbox.append(_normalize_audit_item(item, q))
    return inbox


def _audit_resolution_status(audit_id: str) -> dict[str, Any] | None:
    """Return the resolution sidecar dict for ``audit_id`` if present.
    Resolutions live in control_room/cache/audit_resolutions/<audit_id>.json
    and are READ-ONLY sidecars to the underlying audit queue (D22-style:
    we never mutate the producer's queue file; we annotate alongside)."""
    AUDIT_RESOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    safe_id = "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in audit_id)
    p = AUDIT_RESOLUTION_DIR / f"{safe_id}.json"
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None


def _audit_resolution_write(audit_id: str, note: str = "") -> Path:
    """Persist a resolution sidecar for ``audit_id``. Sidecar payload is
    {audit_id, resolved_at, resolved_by, note} — never mutates the
    underlying audit_queue.json."""
    AUDIT_RESOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    safe_id = "".join(c if c.isalnum() or c in ("-", "_", ".") else "_" for c in audit_id)
    p = AUDIT_RESOLUTION_DIR / f"{safe_id}.json"
    payload = {
        "schema": "ControlRoomAuditResolution.v1",
        "audit_id": audit_id,
        "resolved_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "resolved_by": "control_room.factory_intake_dock.audit_inbox",
        "note": note,
    }
    p.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    return p


def _audit_inbox_summary() -> dict[str, Any]:
    """Compute the live counts used by the room-emblem badge + inbox
    section header. Excludes any item with a resolution sidecar."""
    inbox = _audit_inbox_load_all()
    unresolved = [i for i in inbox if _audit_resolution_status(i["audit_id"]) is None]
    by_sev = {"high": 0, "medium": 0, "low": 0}
    for i in unresolved:
        by_sev[i["severity"] if i["severity"] in by_sev else "medium"] += 1
    return {
        "all_items": inbox,
        "unresolved": unresolved,
        "unresolved_total": len(unresolved),
        "resolved_total": len(inbox) - len(unresolved),
        "high": by_sev["high"],
        "medium": by_sev["medium"],
        "low": by_sev["low"],
    }


def _render_audit_inbox(audit_summary: dict[str, Any]) -> None:
    """Render the audit-queue inbox: grouped by severity, with filter,
    drilldown, and 'Mark resolved' that writes a sidecar."""
    import streamlit as st

    st.markdown('<span class="cap">audit inbox · daemon-emitted honest negatives</span>', unsafe_allow_html=True)

    inbox = audit_summary["all_items"]
    if not inbox:
        render_empty_state(
            reason="no audit_queue.json files in reports/ contain items",
            expected_artifact="reports/<campaign>/{factory_store,daemon_store}/audit_queue.json with items",
        )
        return

    # Filter controls
    filt_cols = st.columns([2, 2, 2, 2])
    with filt_cols[0]:
        sev_filter = st.multiselect(
            "severity",
            options=["high", "medium", "low"],
            default=["high", "medium", "low"],
            key="audit_inbox_sev_filter",
        )
    with filt_cols[1]:
        sources_present = sorted({i["source_id"] for i in inbox if i["source_id"]})
        source_filter = st.multiselect(
            "source",
            options=sources_present,
            default=sources_present,
            key="audit_inbox_source_filter",
        )
    with filt_cols[2]:
        status_filter = st.selectbox(
            "status",
            options=["unresolved only", "resolved only", "all"],
            index=0,
            key="audit_inbox_status_filter",
        )
    with filt_cols[3]:
        render_html(
            f'<div style="font-family:var(--font-mono,monospace);font-size:0.74rem;'
            f'color:var(--fg3,#9aa0ac);padding:8px 0;">'
            f'<b>{audit_summary["unresolved_total"]}</b> unresolved · '
            f'<b>{audit_summary["resolved_total"]}</b> resolved · '
            f'<b>{len(inbox)}</b> total<br>'
            f'<span style="color:var(--warning,#f5a623);">{audit_summary["high"]}</span> high · '
            f'<span style="color:var(--active,#4fc3f7);">{audit_summary["medium"]}</span> med · '
            f'<span style="color:var(--fg4,#6c7484);">{audit_summary["low"]}</span> low'
            f'</div>'
        )

    # CB-011 fix #9 — Bulk-resolve UI. James's complaint: 72 items
    # most of which are auto-categorizable (NIST source-limited
    # transactinides + planted-false-claim test fixtures + contradictory-
    # polarity fixtures + stale-cache artifacts). Surface a one-click
    # bulk action per known pattern, write sidecars under the existing
    # CB-009 read-only-sidecar discipline.
    pattern_buckets = _compute_bulk_resolve_buckets(audit_summary["unresolved"])
    if any(b["count"] > 0 for b in pattern_buckets.values()):
        st.markdown(
            '<div style="margin-top:12px;padding:10px 14px;background:rgba(189,109,248,0.05);'
            'border:1px dashed rgba(189,109,248,0.4);border-radius:12px;">'
            '<div style="font-family:var(--font-mono);font-size:0.74rem;color:var(--motif,#bd6df8);'
            'letter-spacing:0.06em;text-transform:uppercase;margin-bottom:8px;">'
            'bulk resolve · auto-categorizable patterns'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        bulk_cols = st.columns(len(pattern_buckets))
        for i, (key, bucket) in enumerate(pattern_buckets.items()):
            with bulk_cols[i]:
                if bucket["count"] == 0:
                    render_html(
                        f'<div style="font-family:var(--font-mono);font-size:0.7rem;'
                        f'color:var(--fg4,#6c7484);padding:6px 0;">'
                        f'<b>{bucket["label"]}</b><br>0 items'
                        f'</div>'
                    )
                    continue
                btn_label = f'Resolve {bucket["count"]} · {bucket["label"]}'
                if st.button(btn_label, key=f"audit_bulk_{key}", use_container_width=True):
                    n = 0
                    for item in bucket["items"]:
                        _audit_resolution_write(
                            item["audit_id"],
                            note=f"bulk_resolve:{key}:{bucket['resolution_reason']}",
                        )
                        n += 1
                    st.success(
                        f"resolved {n} item(s) under reason "
                        f'"{bucket["resolution_reason"]}" — sidecars at '
                        f"control_room/cache/audit_resolutions/"
                    )
                    st.rerun()
                render_html(
                    f'<div style="font-family:var(--font-mono);font-size:0.66rem;'
                    f'color:var(--fg4,#6c7484);margin-top:4px;">'
                    f'reason: {bucket["resolution_reason"]}<br>'
                    f'doctrine: {bucket["doctrine_binding"]}'
                    f'</div>'
                )

    # Apply filters
    def _passes_status(item: dict[str, Any]) -> bool:
        resolved = _audit_resolution_status(item["audit_id"]) is not None
        if status_filter == "unresolved only":
            return not resolved
        if status_filter == "resolved only":
            return resolved
        return True

    filtered = [
        i for i in inbox
        if i["severity"] in sev_filter
        and (not source_filter or i["source_id"] in source_filter or not i["source_id"])
        and _passes_status(i)
    ]

    if not filtered:
        render_html(
            '<div style="font-family:var(--font-body,sans-serif);font-size:0.85rem;'
            'color:var(--fg4,#6c7484);margin:12px 0;padding:12px;'
            'background:var(--bg-panel,#121826);border:1px dashed var(--border,#283042);'
            'border-radius:14px;">'
            'no items match current filters'
            '</div>'
        )
        return

    # Group by severity in priority order
    sev_order = ["high", "medium", "low"]
    sev_color = {"high": "#ff5468", "medium": "#f5a623", "low": "#5b6478"}
    for sev in sev_order:
        bucket = [i for i in filtered if i["severity"] == sev]
        if not bucket:
            continue
        st.markdown(
            f'<div style="font-family:var(--font-mono,monospace);font-size:0.78rem;'
            f'color:{sev_color[sev]};margin:14px 0 6px;letter-spacing:0.06em;'
            f'text-transform:uppercase;font-weight:600;">'
            f'{sev} severity · {len(bucket)} item(s)</div>',
            unsafe_allow_html=True,
        )
        for item in bucket[:25]:  # cap at 25 per severity to keep the room scannable
            resolution = _audit_resolution_status(item["audit_id"])
            resolved = resolution is not None
            border_color = "var(--verified,#3ddc84)" if resolved else sev_color[sev]
            opacity = "0.6" if resolved else "1.0"
            audit_id_short = item["audit_id"][:48] + ("…" if len(item["audit_id"]) > 48 else "")
            resolved_pill = (
                '<span style="color:var(--verified,#3ddc84);font-family:var(--font-mono,monospace);'
                'font-size:0.7rem;font-weight:600;">RESOLVED</span>'
                if resolved else ""
            )
            # CB-009 T3 — click-to-drill: store audit_id in session_state
            # so the drilldown panel below can show the underlying record
            # / source-cache entry / failure context. The brief calls
            # this out explicitly: "Click item → drill into the
            # underlying record / source-cache entry / failure context".
            row_html = (
                f'<div style="opacity:{opacity};background:var(--bg-panel,#121826);'
                f'border:1px solid var(--border,#283042);border-left:3px solid {border_color};'
                f'border-radius:10px;padding:10px 14px;margin:6px 0;">'
                f'<div style="display:flex;align-items:baseline;gap:8px;flex-wrap:wrap;">'
                f'<span style="font-family:var(--font-mono,monospace);font-size:0.75rem;'
                f'color:var(--trace,#22d3ee);font-weight:600;">{audit_id_short}</span>'
                f'<span style="font-family:var(--font-mono,monospace);font-size:0.7rem;'
                f'color:var(--fg4,#6c7484);">{item["created_at"] or "no timestamp"}</span>'
                f'{resolved_pill}'
                f'</div>'
                f'<div style="font-family:var(--font-body,sans-serif);font-size:0.88rem;'
                f'color:var(--fg2,#e3e6ec);margin:6px 0;">{item["reason"] or "<i>no reason given</i>"}</div>'
                f'<div style="font-family:var(--font-mono,monospace);font-size:0.7rem;'
                f'color:var(--fg4,#6c7484);">'
                f'source: <span style="color:var(--fg3,#9aa0ac);">{item["source_id"] or "—"}</span> · '
                f'record: <span style="color:var(--fg3,#9aa0ac);">{(item["record_id"] or "—")[:42]}</span><br>'
                f'recommended: <span style="color:var(--fg3,#9aa0ac);">{(item["recommended_action"] or "—")[:120]}</span><br>'
                f'source_file: <span style="color:var(--fg3,#9aa0ac);">{item["source_file"]}</span>'
                f'</div>'
                f'</div>'
            )
            render_html(row_html)
            if not resolved:
                resolve_cols = st.columns([2, 1, 1])
                with resolve_cols[0]:
                    note = st.text_input(
                        "resolution note (optional)",
                        key=f"audit_note_{item['audit_id']}",
                        label_visibility="collapsed",
                        placeholder="resolution note (optional, persisted to sidecar)",
                    )
                with resolve_cols[1]:
                    if st.button("Drill", key=f"audit_drill_{item['audit_id']}", use_container_width=True):
                        st.session_state["audit_inbox_drilldown_id"] = item["audit_id"]
                        st.rerun()
                with resolve_cols[2]:
                    if st.button("Mark resolved", key=f"audit_resolve_{item['audit_id']}", use_container_width=True):
                        _audit_resolution_write(item["audit_id"], note=note)
                        st.rerun()
            else:
                render_html(
                    f'<div style="font-family:var(--font-mono,monospace);font-size:0.7rem;'
                    f'color:var(--verified,#3ddc84);margin:-4px 0 8px 14px;">'
                    f'resolved at {resolution.get("resolved_at", "?")} · '
                    f'note: {(resolution.get("note") or "—")[:80]}'
                    f'</div>'
                )

    # CB-009 T3 drilldown panel — surfaces the underlying record /
    # source-cache entry / failure context for the selected audit item.
    drill_id = st.session_state.get("audit_inbox_drilldown_id")
    if drill_id:
        target = next((i for i in inbox if i["audit_id"] == drill_id), None)
        if target is None:
            st.session_state.pop("audit_inbox_drilldown_id", None)
        else:
            _render_audit_drilldown(target)


def _render_audit_drilldown(item: dict[str, Any]) -> None:
    """Surface the underlying record + source-cache entry + failure
    context for the audit item selected by the user. Per the CB-009
    brief: 'Click item → drill into the underlying record /
    source-cache entry / failure context'. Read-only — never mutates."""
    import streamlit as st

    st.markdown(
        f'<div style="margin-top: 1.2rem; padding: 12px 14px; background: var(--bg-panel,#121826); '
        f'border: 1px solid var(--motif,#bd6df8); border-radius: 14px; '
        f'box-shadow: 0 0 18px rgba(189,109,248,0.15);">'
        f'<div style="font-family: var(--font-display,sans-serif); font-size: 1.05rem; color: var(--fg1,#f8f9fa); '
        f'font-weight: 600;">audit drilldown · {item["audit_id"][:60]}</div>'
        f'<div style="font-family: var(--font-mono,monospace); font-size: 0.72rem; color: var(--fg4,#6c7484); '
        f'margin: 4px 0 8px;">severity: {item["severity"]} · source: {item["source_id"] or "—"} · '
        f'recorded: {item["created_at"] or "no timestamp"}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Always show the audit item itself
    with st.expander("1. audit item (raw)", expanded=True):
        st.json(item)

    # If the audit references a record_id, hunt for the source record
    # in factory_store / daemon_store empirical_records.json files.
    if item.get("record_id"):
        record = _find_empirical_record(item["record_id"])
        with st.expander(f"2. underlying empirical record  ({'FOUND' if record else 'not found'})", expanded=bool(record)):
            if record:
                st.json(record)
            else:
                render_html(
                    '<div style="font-family:var(--font-body,sans-serif);font-size:0.85rem;'
                    'color:var(--fg4,#6c7484);">no empirical_records.json under reports/ '
                    'contains this record_id (D22 honest absence — the producer may have '
                    'wiped the contaminated record after audit).</div>'
                )

    # If the audit references a source_id, look up the source-cache entry
    if item.get("source_id"):
        cache_entry = _find_source_cache_entry(item["source_id"])
        with st.expander(f"3. source cache entry  ({'FOUND' if cache_entry else 'not found'})", expanded=False):
            if cache_entry:
                st.json(cache_entry)
            else:
                render_html(
                    '<div style="font-family:var(--font-body,sans-serif);font-size:0.85rem;'
                    'color:var(--fg4,#6c7484);">no source_cache_index.json under reports/ '
                    f'contains source_id={item["source_id"]}.</div>'
                )

    # Source file context — show the surrounding audit_queue.json file
    with st.expander(f"4. source file context  ({item['source_file']})", expanded=False):
        src_path = REPO_ROOT / item["source_file"]
        if src_path.exists():
            try:
                # Show only the relevant section to keep render sane.
                payload = json.loads(src_path.read_text(encoding="utf-8-sig"))
                if isinstance(payload, dict):
                    items = payload.get("items") or payload.get("records") or []
                else:
                    items = payload if isinstance(payload, list) else []
                # Find this item in the file
                matches = [
                    x for x in items
                    if isinstance(x, dict)
                    and (x.get("audit_id") == item["audit_id"] or x.get("item_id") == item["audit_id"])
                ]
                st.json({
                    "source_file": item["source_file"],
                    "total_items_in_file": len(items),
                    "matched_item": matches[0] if matches else None,
                })
            except (OSError, json.JSONDecodeError) as exc:
                st.error(f"could not parse {src_path}: {exc}")
        else:
            st.error(f"source file no longer exists: {src_path}")

    if st.button("Close drilldown", key="audit_close_drilldown"):
        st.session_state.pop("audit_inbox_drilldown_id", None)
        st.rerun()


def _find_empirical_record(record_id: str) -> dict[str, Any] | None:
    """Scan reports/**/empirical_records.json for a record matching
    ``record_id``. Returns the first match or None. Read-only."""
    reports = REPO_ROOT / "reports"
    if not reports.exists():
        return None
    for p in reports.rglob("empirical_records.json"):
        try:
            payload = json.loads(p.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        records = payload.get("records") if isinstance(payload, dict) else payload
        if not isinstance(records, list):
            continue
        for r in records:
            if isinstance(r, dict) and r.get("record_id") == record_id:
                return r
    return None


def _find_source_cache_entry(source_id: str) -> dict[str, Any] | None:
    """Scan reports/**/source_cache_index.json for an entry matching
    ``source_id``. Returns the first match or None. Read-only."""
    reports = REPO_ROOT / "reports"
    if not reports.exists():
        return None
    for p in reports.rglob("source_cache_index.json"):
        try:
            payload = json.loads(p.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        entries = payload.get("entries") if isinstance(payload, dict) else payload
        if not isinstance(entries, list):
            continue
        for e in entries:
            if isinstance(e, dict) and e.get("source_id") == source_id:
                return e
    return None


# ---------------------------------------------------------------------------
# CB-011 fix #9 — bulk-resolve pattern matching
# ---------------------------------------------------------------------------


# Catalog of recognized auto-resolvable patterns. Each entry maps a
# pattern key to (label, matcher predicate, resolution_reason,
# doctrine_binding). The matcher predicate takes a normalized inbox
# item dict and returns True iff the item belongs to this bucket.
_BULK_PATTERNS: list[tuple[str, str, "object", str, str]] = [
    (
        "nist_source_limited",
        "NIST source-limited (transactinides, etc.)",
        lambda i: i.get("reason") == "nist_asd_no_energy_level_rows",
        "D17_honest_no_source_data_available",
        "D17 — honest absence; NIST has no spectra for this element",
    ),
    (
        "fixture_planted_false_claim",
        "C019 fixture · planted false claim rejected",
        lambda i: "planted false claim rejected" in (i.get("reason") or "").lower(),
        "D9_test_fixture_validation",
        "D9 — fixture replay; predicate correctly rejected planted false claim",
    ),
    (
        "fixture_contradictory_polarity",
        "C011 fixture · contradictory polarity",
        lambda i: i.get("reason") == "contradictory source-bound polarity",
        "D9_test_fixture_validation",
        "D9 — synthetic conflict driver; intentional contradictory inputs",
    ),
    (
        "stale_cache_artifact",
        "Stale cache artifact",
        lambda i: (i.get("reason") or "").startswith("stale_cache:"),
        "D17_stale_cache_artifact",
        "D17 — cache surfaced as stale; not a live ingestion failure",
    ),
    (
        "fixture_general",
        "Other test-fixture audits",
        lambda i: any(
            tag in (i.get("source_file") or "").lower()
            for tag in ("/fixtures/", "_fixture", "campaign_019/fixtures")
        )
        and (i.get("reason") or "")
        not in {  # not already covered above
            "nist_asd_no_energy_level_rows",
            "contradictory source-bound polarity",
        },
        "D9_test_fixture_validation",
        "D9 — fixture replay; expected audit emission",
    ),
]


def _compute_bulk_resolve_buckets(
    unresolved_items: list[dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    """Group ``unresolved_items`` by recognized auto-resolvable pattern.

    Each item lands in AT MOST ONE bucket (first match wins; the
    pattern order is deliberately the most-specific first). Items that
    don't match any pattern are NOT placed in a bucket — they remain
    in the manual-review pool, which is the whole point of bulk
    categorization (extract the noise, leave the signal).
    """
    buckets: dict[str, dict[str, Any]] = {}
    for key, label, matcher, reason, binding in _BULK_PATTERNS:
        buckets[key] = {
            "label": label,
            "items": [],
            "count": 0,
            "resolution_reason": reason,
            "doctrine_binding": binding,
        }
    for item in unresolved_items:
        for key, _label, matcher, _reason, _binding in _BULK_PATTERNS:
            try:
                hit = matcher(item)
            except Exception:
                hit = False
            if hit:
                buckets[key]["items"].append(item)
                buckets[key]["count"] += 1
                break
    return buckets

