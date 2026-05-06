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

    fire_disabled = in_flight or not selected_source_ids
    if st.button("FIRE - run multi-world Factory", type="primary", disabled=fire_disabled, use_container_width=True, key="factory_dock_fire"):
        _fire(allow_network=allow_network, target_worlds=selected_worlds, source_ids=selected_source_ids)
        st.rerun()

    if in_flight or live_mode:
        if hasattr(st, "autorefresh"):
            st.autorefresh(interval=1500, key="factory_dock_live_refresh")

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
