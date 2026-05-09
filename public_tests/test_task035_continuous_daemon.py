from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from factory_lowlevel.continuous_daemon import cadence_seconds, run_continuous_daemon  # noqa: E402
from factory_lowlevel.live_pipeline import available_adapters  # noqa: E402
from factory_lowlevel.persistence import atomic_write_json  # noqa: E402
from factory_lowlevel.schemas import utc_now  # noqa: E402


def test_task035_daemon_cadence_mapping_is_conservative():
    assert cadence_seconds("hourly") == 3600
    assert cadence_seconds("daily") == 86400
    assert cadence_seconds("weekly") == 604800
    assert cadence_seconds("manual_spec_review") > cadence_seconds("monthly")
    assert cadence_seconds("unknown_source_label") == 86400


def test_task035_daemon_skips_when_sources_not_due(tmp_path):
    state = {
        "schema": "FactoryDaemonState.v1",
        "last_success_by_source": {row["source_id"]: utc_now() for row in available_adapters()},
    }
    state_path = tmp_path / "daemon_state.json"
    atomic_write_json(state_path, state)
    records = run_continuous_daemon(
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
        disk_budget_mb=512,
        retry_ceiling=1,
        retry_base_seconds=0.0,
    )
    assert records[0]["status"] == "complete"
    assert records[0]["due_source_ids"] == []
    assert records[0]["run_ids"] == []


def test_task035_daemon_refuses_over_budget_cache(tmp_path):
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    (cache_dir / "over_budget.bin").write_bytes(b"x")
    records = run_continuous_daemon(
        cycles=1,
        sleep_seconds=0,
        store_root=tmp_path / "store",
        cache_dir=cache_dir,
        run_root=tmp_path / "runs",
        trace_root=tmp_path / "traces",
        session_ledger=tmp_path / "sessions.jsonl",
        state_path=tmp_path / "state.json",
        heartbeat_path=tmp_path / "heartbeat.json",
        progress_root=tmp_path / "progress",
        disk_budget_mb=0,
        retry_ceiling=1,
        retry_base_seconds=0.0,
    )
    assert records[0]["status"] == "held_disk_budget"
    assert records[0]["audit_items"][0]["reason"] == "daemon_disk_budget_exceeded"


def test_task035_daemon_quarantines_failed_due_source(tmp_path, monkeypatch):
    rows = available_adapters()
    due = rows[0]["source_id"]
    state = {
        "schema": "FactoryDaemonState.v1",
        "last_success_by_source": {row["source_id"]: utc_now() for row in rows if row["source_id"] != due},
    }
    state_path = tmp_path / "daemon_state.json"
    atomic_write_json(state_path, state)

    def _fail_source(**kwargs):
        assert kwargs["source_ids"] == [due]
        raise RuntimeError("synthetic adapter failure")

    monkeypatch.setattr("factory_lowlevel.continuous_daemon.run_live_factory_cycle", _fail_source)
    records = run_continuous_daemon(
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
        disk_budget_mb=512,
        retry_ceiling=1,
        retry_base_seconds=0.0,
    )
    assert records[0]["status"] == "complete"
    assert records[0]["completed_source_ids"] == []
    assert records[0]["quarantined_source_ids"] == [due]
    assert records[0]["audit_items"][0]["reason"] == "adapter_retry_ceiling_exceeded"
