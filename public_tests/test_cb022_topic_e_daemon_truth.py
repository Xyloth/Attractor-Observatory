from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from control_room.snapshot import build_snapshot  # noqa: E402
from factory_lowlevel.continuous_daemon import run_continuous_daemon  # noqa: E402
from factory_lowlevel.live_pipeline import available_adapters  # noqa: E402
from factory_lowlevel.persistence import atomic_write_json  # noqa: E402
from factory_lowlevel.progress import read_ingestion_progress, write_ingestion_progress  # noqa: E402
from factory_lowlevel.schemas import utc_now  # noqa: E402


def test_progress_pointer_binds_to_state_hash_and_fails_empty_when_stale(tmp_path):
    state_path = tmp_path / "daemon_state.json"
    state = {
        "schema": "FactoryDaemonState.v1",
        "last_success_by_source": {"source.a": utc_now()},
    }
    atomic_write_json(state_path, state)
    progress_root = tmp_path / "progress"
    session = {
        "cycle_index": 0,
        "started_at": utc_now(),
        "completed_at": utc_now(),
        "completed_source_ids": ["source.a"],
        "quarantined_source_ids": [],
        "status": "complete",
    }
    source_rows = [{"source_id": "source.a", "target_world": "crn"}]

    write_ingestion_progress(
        session=session,
        state=state,
        store_root=tmp_path / "store",
        source_rows=source_rows,
        progress_root=progress_root,
        state_path=state_path,
    )

    progress = json.loads((progress_root / "crn.json").read_text(encoding="utf-8"))
    assert progress["file_semantics"] == "current_operator_truth"
    assert progress["last_updated_at"]
    assert progress["bound_to_state_hash"].startswith("sha256:")
    assert read_ingestion_progress(progress_root, state_path=state_path)["crn"]["world_family"] == "crn"

    state["last_success_by_source"]["source.b"] = utc_now()
    atomic_write_json(state_path, state)
    assert read_ingestion_progress(progress_root, state_path=state_path) == {}


def test_force_refresh_invalidates_progress_entries(tmp_path, monkeypatch):
    rows = available_adapters()
    due = rows[0]
    state = {
        "schema": "FactoryDaemonState.v1",
        "last_success_by_source": {row["source_id"]: utc_now() for row in rows},
    }
    state_path = tmp_path / "daemon_state.json"
    atomic_write_json(state_path, state)

    def _fake_cycle(**kwargs):
        return {"run_id": f"run_for_{kwargs['source_ids'][0]}"}

    monkeypatch.setattr("factory_lowlevel.continuous_daemon.run_live_factory_cycle", _fake_cycle)
    run_continuous_daemon(
        cycles=1,
        sleep_seconds=0,
        store_root=tmp_path / "store",
        cache_dir=tmp_path / "cache",
        run_root=tmp_path / "runs",
        trace_root=tmp_path / "traces",
        session_ledger=tmp_path / "sessions.jsonl",
        state_path=state_path,
        heartbeat_path=tmp_path / "heartbeat.json",
        progress_root=tmp_path / "progress",
        force_refresh_source=[due["source_id"]],
        disk_budget_mb=512,
        retry_ceiling=1,
        retry_base_seconds=0.0,
    )

    persisted_state = json.loads(state_path.read_text(encoding="utf-8"))
    assert persisted_state["force_refresh_invalidations"][0]["source_id"] == due["source_id"]
    progress = read_ingestion_progress(tmp_path / "progress", state_path=state_path)
    world_progress = progress[due["target_world"]]
    assert world_progress["invalidated_by_force_refresh"][0]["source_id"] == due["source_id"]


def test_snapshot_raw_file_declares_loader_policy():
    snapshot = build_snapshot()
    assert snapshot["raw_file_policy"] == "do_not_read_directly"
    assert snapshot["read_api"] == "control_room.snapshot.load_latest"
    assert snapshot["freshness_status_advisory_only"] is True
