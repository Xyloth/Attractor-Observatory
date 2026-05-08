from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import factory_lowlevel.live_pipeline as live_pipeline  # noqa: E402
from factory_lowlevel.persistence import verify_world_traces  # noqa: E402
from factory_lowlevel.schemas import sha256  # noqa: E402
from factory_lowlevel.adapters import KEGGEcoliCRNAdapter  # noqa: E402


def test_live_pipeline_persists_verifiable_world_traces_idempotently(tmp_path, monkeypatch):
    class OneRecordKEGGEcoliCRNAdapter(KEGGEcoliCRNAdapter):
        phase2_target_count = 1

    monkeypatch.setattr(live_pipeline, "evaluate_lenses", lambda evidence_rows: [])
    monkeypatch.setattr(live_pipeline, "ALL_FACTORY_ADAPTERS", (OneRecordKEGGEcoliCRNAdapter,))
    source_ids = ["source.kegg.ecoli_mg1655.metabolic_network"]
    kwargs = {
        "source_ids": source_ids,
        "allow_network": False,
        "store_root": tmp_path / "factory_store",
        "cache_dir": tmp_path / "source_cache",
        "run_root": tmp_path / "factory_runs",
        "trace_root": tmp_path / "traces",
        "trigger": "public_test_world_trace_persistence",
    }

    run = live_pipeline.run_live_factory_cycle(**kwargs)
    routed_worlds = {bundle["world_family"] for bundle in run["routed_worlds"]}
    snapshot = run["store_snapshot"]
    assert snapshot["counts"]["world_traces"] == len(routed_worlds)

    trace_path = Path(snapshot["paths"]["world_traces"])
    payload = json.loads(trace_path.read_text(encoding="utf-8"))
    traces = payload["traces"]
    assert {trace["world_family"] for trace in traces} == routed_worlds
    for trace in traces:
        assert trace["schema"] == "LowLevelWorldTrace.v1"
        assert trace["trace_content_hash"] == sha256(trace["body"])
        assert trace["verifier"]["predicate"] == "sha256_of_canonical_json(body) == trace_content_hash"
        assert trace["verifier"]["trace_checkable"] is True
        assert trace["verifier"]["deterministic"] is True

    verification = verify_world_traces(kwargs["store_root"])
    assert verification["present"] is True
    assert verification["all_pass"] is True

    rerun = live_pipeline.run_live_factory_cycle(**kwargs)
    assert rerun["store_snapshot"]["counts"]["world_traces"] == len(routed_worlds)
    rerun_payload = json.loads(trace_path.read_text(encoding="utf-8"))
    assert len(rerun_payload["traces"]) == len(routed_worlds)
