from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from factory_lowlevel.continuous_daemon import _run_source_with_retries  # noqa: E402
from factory_lowlevel.live_pipeline import _apply_trace_trim_policy  # noqa: E402
from factory_lowlevel.memory_guard import check_disk_budget  # noqa: E402
from factory_lowlevel.schemas import EmpiricalRecord  # noqa: E402
from factory_lowlevel.sharded_store import ShardedFactoryStore  # noqa: E402
from factory_lowlevel.streaming_run_writer import StreamingRunWriter  # noqa: E402
from factory_lowlevel.supervision import build_source_worker_command  # noqa: E402


def _record(record_id: str, world_family: str = "protocell") -> EmpiricalRecord:
    return EmpiricalRecord(
        record_id=record_id,
        source_id="source.test",
        world_family=world_family,
        record_type="test",
        canonical_name=f"record-{record_id}",
        payload={"x": 1},
        provenance={"source_url": "https://example.org", "retrieval_timestamp": "2026-05-09T00:00:00Z"},
        license_class="open",
    )


def test_f1_daemon_runs_source_through_child_process(monkeypatch, tmp_path):
    calls: list[dict[str, object]] = []

    def _fake_child(**kwargs):
        calls.append(kwargs)
        return {"status": "ok", "run_id": "sha256:child-run", "worker_exit_code": 0}

    monkeypatch.setattr("factory_lowlevel.continuous_daemon.run_source_child_process", _fake_child)
    result = _run_source_with_retries(
        source_id="source.szostak_liposome.protocell_benchmarks",
        allow_network=False,
        store_root=tmp_path / "store",
        cache_dir=tmp_path / "cache",
        run_root=tmp_path / "runs",
        trace_root=tmp_path / "traces",
        retry_ceiling=1,
        retry_base_seconds=0.0,
        trigger="test",
    )
    assert result["status"] == "ok"
    assert result["supervision"] == "child_process"
    assert calls and calls[0]["source_id"] == "source.szostak_liposome.protocell_benchmarks"


def test_f1_worker_command_is_module_child_entrypoint(tmp_path):
    command = build_source_worker_command(
        source_id="source.a",
        allow_network=True,
        store_root=tmp_path / "store",
        cache_dir=tmp_path / "cache",
        run_root=tmp_path / "runs",
        trace_root=tmp_path / "traces",
        trigger="unit",
        result_path=tmp_path / "result.json",
    )
    assert command[1:3] == ["-m", "factory_lowlevel.source_worker"]
    assert "--allow-network" in command


def test_f2_sharded_store_appends_and_streams_without_snapshot_load(tmp_path):
    store = ShardedFactoryStore(tmp_path / "store")
    manifest = store.append_records(_record(f"r{i}", "field") for i in range(12))
    assert manifest["appended_by_world"] == {"field": 12}
    first_two = []
    for row in store.iter_records("field"):
        first_two.append(row["record_id"])
        if len(first_two) == 2:
            break
    assert first_two == ["r0", "r1"]
    manifest2 = store.append_records([_record("r0", "field"), _record("r12", "field")])
    assert manifest2["appended_by_world"] == {"field": 1}
    assert manifest2["skipped_existing_or_invalid"] == 1


def test_f3_streaming_run_writer_writes_sections_before_manifest(tmp_path):
    writer = StreamingRunWriter(tmp_path / "runs", run_id_hint="unit")
    section = writer.write_section("records", [{"record_id": "r1"}])
    assert Path(section["path"]).exists()
    assert not (tmp_path / "runs" / "sections" / "unit" / "manifest.json").exists()
    manifest = writer.finish({"run_id": "sha256:unit"})
    assert Path(manifest["path"]).exists()
    assert "records" in manifest["sections"]


def test_f4_disk_budget_covers_store_and_trace_roots(tmp_path):
    store_root = tmp_path / "store"
    trace_root = tmp_path / "traces"
    store_root.mkdir()
    trace_root.mkdir()
    (store_root / "records.bin").write_bytes(b"x" * 16)
    (trace_root / "trace.bin").write_bytes(b"y" * 16)
    ok, snapshots, reason = check_disk_budget([store_root, trace_root], budget_bytes=8)
    assert not ok
    assert reason == "disk_budget_exceeded"
    assert {Path(snap.path).name for snap in snapshots} == {"store", "traces"}


def test_f5_trace_trim_policy_summarizes_oversized_trace():
    trace = {
        "manifest": {"trace_id": "pending"},
        "events": [{"payload": "x" * 50} for _ in range(20)],
        "state_history": [{"x": i} for i in range(20)],
        "process_flags": {"floor": True},
        "audit_notes": [],
    }
    trimmed, audit = _apply_trace_trim_policy(trace, record=_record("r-trim"), max_bytes=128)
    assert trimmed["trimmed"] is True
    assert trimmed["original_trace_content_hash"].startswith("sha256:")
    assert audit and audit["reason"] == "trace_trimmed_oversized_trace"
    assert "events" not in trimmed


def test_f6_live_pipeline_checks_stop_flag_inside_record_loop():
    src = (ROOT / "factory_lowlevel" / "live_pipeline.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    fn = next(node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef) and node.name == "run_live_factory_cycle")
    found = False
    for node in ast.walk(fn):
        if isinstance(node, ast.For) and "bundle.empirical_records" in ast.unparse(node.iter):
            body_src = "\n".join(ast.unparse(item) for item in node.body)
            found = "read_stop_flag" in body_src and "operator_stop_flag_honored_between_records" in body_src
            break
    assert found, "live pipeline must honor the stop flag between individual records"


def test_szostak_zero_division_threshold_is_no_division_not_exponential_growth():
    from worlds.protocell.model import ProtocellWorld

    world = ProtocellWorld()
    world.reset(
        seed=1,
        params={
            "division_threshold": 0.0,
            "initial_membrane_material": 6.5,
            "initial_membrane_integrity": 0.75,
            "initial_internal_resource": 18.0,
            "initial_closure_marker": 0.6,
            "membrane_production_rate": 0.0,
            "steps": 4,
            "dt": 0.25,
        },
    )
    for _ in range(4):
        world.step(0.25)
    assert sum(1 for cell in world.cells.values() if cell.alive) == 1
    assert world.division_records == []
