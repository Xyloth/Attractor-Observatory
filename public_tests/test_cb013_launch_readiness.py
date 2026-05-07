"""Tests for CB-013 launch readiness mechanics.

Covers:
  * launch_safety.acquire_lock / release_lock
  * launch_safety.verify_resume (clean / mid-flight / aborted)
  * launch_safety.check_factory_store_integrity (uniqueness, orphan refs)
  * launch_safety.write_checkpoint (atomic + checkpoint_at field)
  * progress.load_target_densities (targets doc parsing + D22 absence)
  * progress.write_ingestion_progress / read_ingestion_progress

Tests are deterministic, stay in tmp_path, and never invoke the
running daemon. No network calls.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# Lock file
# ---------------------------------------------------------------------------


def test_acquire_lock_clean_first_start(tmp_path):
    """No prior lock → acquired=True with rationale 'lock_acquired_clean'."""
    from factory_lowlevel.launch_safety import acquire_lock

    store = tmp_path / "store"
    store.mkdir()
    out = acquire_lock(store_root=store, pid=12345)
    assert out.acquired is True
    assert out.rationale == "lock_acquired_clean"
    assert (store / ".daemon_lock").exists()
    payload = json.loads((store / ".daemon_lock").read_text())
    assert payload["pid"] == 12345
    assert payload["schema"] == "FactoryDaemonLock.v1"


def test_acquire_lock_refuses_when_holder_alive(tmp_path):
    """Lock present + holder PID alive → acquired=False with rationale."""
    from factory_lowlevel.launch_safety import acquire_lock

    store = tmp_path / "store"
    store.mkdir()
    # Plant a lock with the current process's PID (definitely alive).
    my_pid = os.getpid()
    (store / ".daemon_lock").write_text(
        json.dumps({"pid": my_pid, "started_at": "2026-01-01T00:00:00Z"}),
        encoding="utf-8",
    )
    out = acquire_lock(store_root=store, pid=99999)
    assert out.acquired is False
    assert "already running" in out.rationale
    assert out.holder_pid == my_pid


def test_acquire_lock_overrides_orphaned_lock(tmp_path):
    """Lock present + holder PID NOT alive → override (orphaned)."""
    from factory_lowlevel.launch_safety import acquire_lock

    store = tmp_path / "store"
    store.mkdir()
    # Plant a lock with a deliberately-dead PID (well above any real range).
    (store / ".daemon_lock").write_text(
        json.dumps({"pid": 9999999, "started_at": "2026-01-01T00:00:00Z"}),
        encoding="utf-8",
    )
    out = acquire_lock(store_root=store, pid=12345)
    assert out.acquired is True
    assert "orphaned" in out.rationale.lower()


def test_release_lock_only_when_owned(tmp_path):
    """release_lock returns False if the lock belongs to a different PID."""
    from factory_lowlevel.launch_safety import release_lock

    store = tmp_path / "store"
    store.mkdir()
    (store / ".daemon_lock").write_text(
        json.dumps({"pid": 8888}), encoding="utf-8"
    )
    # Try to release as a different PID.
    assert release_lock(store_root=store, pid=12345) is False
    assert (store / ".daemon_lock").exists()  # untouched
    # Now release as the owning PID.
    assert release_lock(store_root=store, pid=8888) is True
    assert not (store / ".daemon_lock").exists()


def test_release_lock_idempotent_on_missing(tmp_path):
    """Releasing a non-existent lock returns True silently."""
    from factory_lowlevel.launch_safety import release_lock

    store = tmp_path / "store"
    store.mkdir()
    assert release_lock(store_root=store, pid=12345) is True


# ---------------------------------------------------------------------------
# Resume verification
# ---------------------------------------------------------------------------


def test_verify_resume_proceeds_on_no_prior_heartbeat(tmp_path):
    from factory_lowlevel.launch_safety import verify_resume

    out = verify_resume(
        heartbeat_path=tmp_path / "absent.json",
        store_root=tmp_path / "store",
    )
    assert out.proceed is True
    assert out.prior_status == "absent"


def test_verify_resume_proceeds_on_clean_shutdown(tmp_path):
    from factory_lowlevel.launch_safety import verify_resume

    hb = tmp_path / "hb.json"
    hb.write_text(json.dumps({"status": "clean_shutdown"}), encoding="utf-8")
    out = verify_resume(heartbeat_path=hb, store_root=tmp_path / "store")
    assert out.proceed is True
    assert out.prior_status == "clean_shutdown"


def test_verify_resume_aborts_on_unknown_status(tmp_path):
    """Unknown status → conservative abort (D9 binding)."""
    from factory_lowlevel.launch_safety import verify_resume

    hb = tmp_path / "hb.json"
    hb.write_text(json.dumps({"status": "totally_made_up"}), encoding="utf-8")
    out = verify_resume(heartbeat_path=hb, store_root=tmp_path / "store")
    assert out.proceed is False
    assert "unknown" in out.rationale


def test_verify_resume_runs_integrity_check_on_mid_flight(tmp_path):
    """Mid-flight status → integrity check decides proceed/abort."""
    from factory_lowlevel.launch_safety import verify_resume

    hb = tmp_path / "hb.json"
    hb.write_text(json.dumps({"status": "running"}), encoding="utf-8")
    store = tmp_path / "store"
    store.mkdir()
    # No empirical_records.json → integrity returns ok (fresh start).
    out = verify_resume(heartbeat_path=hb, store_root=store)
    assert out.proceed is True
    assert "mid_flight_resume_ok" in out.rationale


# ---------------------------------------------------------------------------
# Integrity check
# ---------------------------------------------------------------------------


def test_check_factory_store_integrity_detects_duplicate_record_ids(tmp_path):
    from factory_lowlevel.launch_safety import check_factory_store_integrity

    store = tmp_path / "store"
    store.mkdir()
    (store / "empirical_records.json").write_text(
        json.dumps({"records": [
            {"record_id": "sha256:a", "world_family": "x"},
            {"record_id": "sha256:a", "world_family": "x"},  # dupe
            {"record_id": "sha256:b", "world_family": "x"},
        ]}),
        encoding="utf-8",
    )
    out = check_factory_store_integrity(store)
    assert out["ok"] is False
    assert "duplicate" in out["rationale"]
    assert out["duplicate_count"] == 1


def test_check_factory_store_integrity_detects_orphan_evidence_edges(tmp_path):
    from factory_lowlevel.launch_safety import check_factory_store_integrity

    store = tmp_path / "store"
    store.mkdir()
    (store / "empirical_records.json").write_text(
        json.dumps({"records": [{"record_id": "sha256:a", "world_family": "x"}]}),
        encoding="utf-8",
    )
    (store / "evidence_graph.json").write_text(
        json.dumps({"edges": [
            {"edge_id": "e1", "evidence_record_ids": ["sha256:a"]},
            {"edge_id": "e2", "evidence_record_ids": ["sha256:nonexistent"]},
        ]}),
        encoding="utf-8",
    )
    out = check_factory_store_integrity(store)
    assert out["ok"] is False
    assert out["orphan_edges"] == 1


def test_check_factory_store_integrity_passes_clean_store(tmp_path):
    from factory_lowlevel.launch_safety import check_factory_store_integrity

    store = tmp_path / "store"
    store.mkdir()
    (store / "empirical_records.json").write_text(
        json.dumps({"records": [
            {"record_id": "sha256:a", "world_family": "x"},
            {"record_id": "sha256:b", "world_family": "x"},
        ]}),
        encoding="utf-8",
    )
    (store / "normalized_refs.json").write_text(
        json.dumps({"records": [
            {"normalized_id": "n1", "empirical_record_id": "sha256:a"},
            {"normalized_id": "n2", "empirical_record_id": "sha256:b"},
        ]}),
        encoding="utf-8",
    )
    out = check_factory_store_integrity(store)
    assert out["ok"] is True
    assert out["record_count"] == 2
    assert out["orphan_edges"] == 0
    assert out["orphan_refs"] == 0


# ---------------------------------------------------------------------------
# Atomic checkpoint
# ---------------------------------------------------------------------------


def test_write_checkpoint_adds_checkpoint_at_field(tmp_path):
    from factory_lowlevel.launch_safety import write_checkpoint

    p = tmp_path / "snapshot.json"
    write_checkpoint(snapshot_path=p, payload={"foo": "bar"})
    payload = json.loads(p.read_text())
    assert payload["foo"] == "bar"
    assert payload["checkpoint_at"]
    assert payload["checkpoint_at"].endswith("Z")


# ---------------------------------------------------------------------------
# Progress / targets
# ---------------------------------------------------------------------------


def test_load_target_densities_parses_canonical_block(tmp_path):
    from factory_lowlevel.progress import load_target_densities

    doc = tmp_path / "INGESTION_TARGETS.md"
    doc.write_text(
        "# Targets\n\n"
        "Some narrative.\n\n"
        "<!-- ingestion-targets:start -->\n\n"
        "| world_family | target | rationale |\n"
        "|--------------|-------:|-----------|\n"
        "| crn          |     50 | KEGG      |\n"
        "| field        |     40 | benchmarks|\n"
        "| ignored_outside_block | 999 | should not parse |\n"
        "\n<!-- ingestion-targets:end -->\n\n"
        "| outside_block | 1000 | not counted |\n",
        encoding="utf-8",
    )
    targets = load_target_densities(doc)
    assert targets == {"crn": 50, "field": 40, "ignored_outside_block": 999}
    # The row OUTSIDE the markers must NOT be parsed.
    assert "outside_block" not in targets


def test_load_target_densities_returns_empty_when_doc_missing(tmp_path):
    """D22: missing doc → empty dict, never fabricated targets."""
    from factory_lowlevel.progress import load_target_densities

    targets = load_target_densities(tmp_path / "absent.md")
    assert targets == {}


def test_load_target_densities_live_doc_has_15_worlds():
    """The shipped INGESTION_TARGETS.md has 15 world rows."""
    from factory_lowlevel.progress import load_target_densities

    targets = load_target_densities()
    assert len(targets) == 15
    assert "atomic_molecular_primitives" in targets
    assert targets["atomic_molecular_primitives"] >= 1
    assert "math_primitives" in targets


def test_write_ingestion_progress_per_world(tmp_path):
    """Each world the session touched gets one progress JSON file."""
    from factory_lowlevel.progress import write_ingestion_progress, read_ingestion_progress

    store = tmp_path / "store"
    store.mkdir()
    (store / "empirical_records.json").write_text(
        json.dumps({"records": [
            {"record_id": "r1", "world_family": "crn"},
            {"record_id": "r2", "world_family": "crn"},
            {"record_id": "r3", "world_family": "field"},
        ]}),
        encoding="utf-8",
    )
    targets_doc = tmp_path / "TARGETS.md"
    targets_doc.write_text(
        "<!-- ingestion-targets:start -->\n"
        "| crn   | 10 | x |\n"
        "| field | 20 | y |\n"
        "<!-- ingestion-targets:end -->\n",
        encoding="utf-8",
    )
    progress_root = tmp_path / "progress"

    session = {
        "cycle_index": 0,
        "started_at": "2026-05-07T08:00:00Z",
        "completed_at": "2026-05-07T08:01:00Z",
        "completed_source_ids": ["src.crn.kegg", "src.field.bench"],
        "quarantined_source_ids": [],
        "status": "complete",
    }
    state = {"last_success_by_source": {}}
    source_rows = [
        {"source_id": "src.crn.kegg", "target_world": "crn"},
        {"source_id": "src.field.bench", "target_world": "field"},
        {"source_id": "src.field.benchB", "target_world": "field"},
    ]
    written = write_ingestion_progress(
        session=session,
        state=state,
        store_root=store,
        source_rows=source_rows,
        targets_doc=targets_doc,
        progress_root=progress_root,
    )
    assert set(written.keys()) == {"crn", "field"}
    crn = json.loads((progress_root / "crn.json").read_text())
    assert crn["world_family"] == "crn"
    assert crn["target_density"] == 10
    assert crn["current_density"] == 2
    assert crn["percent_complete"] == 0.2

    # Reader returns the same payloads.
    rd = read_ingestion_progress(progress_root)
    assert set(rd.keys()) == {"crn", "field"}


def test_write_ingestion_progress_zero_target_when_doc_missing(tmp_path):
    """D22: target_density=0 + percent_complete=0 when targets doc absent."""
    from factory_lowlevel.progress import write_ingestion_progress

    store = tmp_path / "store"
    store.mkdir()
    (store / "empirical_records.json").write_text(
        json.dumps({"records": [{"record_id": "r1", "world_family": "crn"}]}),
        encoding="utf-8",
    )
    written = write_ingestion_progress(
        session={"completed_source_ids": ["s"], "quarantined_source_ids": []},
        state={"last_success_by_source": {}},
        store_root=store,
        source_rows=[{"source_id": "s", "target_world": "crn"}],
        targets_doc=tmp_path / "absent.md",
        progress_root=tmp_path / "progress",
    )
    payload = json.loads((tmp_path / "progress" / "crn.json").read_text())
    assert payload["target_density"] == 0
    assert payload["percent_complete"] == 0.0
