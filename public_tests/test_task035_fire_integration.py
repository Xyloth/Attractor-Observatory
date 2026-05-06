from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from factory_lowlevel.live_pipeline import run_live_factory_cycle, summarize_run  # noqa: E402


def test_task035_fire_button_pipeline_crn_seed(tmp_path):
    run = run_live_factory_cycle(
        target_worlds=["crn"],
        source_ids=["source.kegg.ecoli_mg1655.metabolic_network"],
        allow_network=False,
        store_root=tmp_path / "store",
        cache_dir=tmp_path / "source_cache",
        run_root=tmp_path / "runs",
        trace_root=tmp_path / "traces",
        trigger="fire_button_integration_test",
    )
    summary = summarize_run(run)
    assert summary["world_count"] == 1
    assert summary["records_ingested"] == 1
    assert summary["simulated_trace_count"] == 1
    assert [stage["stage"] for stage in run["pipeline_stages"]] == [
        "download",
        "parse",
        "normalize",
        "route",
        "world_simulate",
        "motif_evaluate",
        "audit",
    ]
    life_form = run["life_forms"][0]
    assert life_form["world_family"] == "crn"
    assert life_form["status"] == "simulated"
    assert life_form["motif_fires"]["closure"] is True
    assert life_form["evidence_private"] is True
    assert life_form["trace_path_status"] == "private_unshipped"

