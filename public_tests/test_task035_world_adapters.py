from __future__ import annotations

import sys
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from factory_lowlevel.live_pipeline import TASK035_ADAPTERS  # noqa: E402


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


def test_task035_public_all_world_report_surface_is_honest():
    report = json.loads((ROOT / "reports/campaign_035/full_report.json").read_text(encoding="utf-8-sig"))
    summary = report["summary"]
    assert summary["world_count"] == 15
    assert summary["records_ingested"] == 32
    assert summary["simulated_trace_count"] == 32
    assert summary["routing_rejections"] == 0
    assert TASK035_WORLDS <= set(summary["traces_by_world"])
    assert report["trace_path_policy"]["evidence_private"] is True
    assert report["trace_path_policy"]["trace_path_status"] == "private_unshipped"
