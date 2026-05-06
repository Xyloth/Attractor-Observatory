from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from factory_lowlevel.live_pipeline import TASK035_ADAPTERS, run_live_factory_cycle, summarize_run  # noqa: E402


TASK035_WORLDS = {
    "protocell",
    "morphogenesis",
    "digital",
    "swarm",
    "cognitive",
    "hypergraph_reactions",
    "symbiogenesis",
    "multiscale",
}


def test_task035_new_adapters_cover_remaining_worlds(tmp_path):
    worlds = set()
    for adapter_cls in TASK035_ADAPTERS:
        result = adapter_cls().fetch(tmp_path / "cache", allow_network=False)
        assert result.records
        assert not result.audits
        worlds.update(record.world_family for record in result.records)
    assert worlds == TASK035_WORLDS


def test_task035_public_all_world_smoke_cycle(tmp_path):
    run = run_live_factory_cycle(
        allow_network=False,
        store_root=tmp_path / "store",
        cache_dir=tmp_path / "source_cache",
        run_root=tmp_path / "runs",
        trace_root=tmp_path / "traces",
        trigger="public_test_task035_all_worlds",
    )
    summary = summarize_run(run)
    assert summary["world_count"] == 15
    assert summary["records_ingested"] == 32
    assert summary["simulated_trace_count"] == 32
    assert summary["routing_rejections"] == 0
    assert TASK035_WORLDS <= set(summary["traces_by_world"])
