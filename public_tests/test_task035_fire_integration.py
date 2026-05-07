from __future__ import annotations

import sys
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

def test_task035_fire_button_pipeline_report_keeps_private_trace_boundary():
    report = json.loads((ROOT / "reports/campaign_021/full_report.json").read_text(encoding="utf-8-sig"))
    assert report["status"] == "green"
    assert report["routing_rejection_count"] == 0
    assert report["trace_record_count"] == 8
    assert report["summary"]["traces_by_world"]["crn"] == 1
    rates = {(row["world_family"], row["motif"]): row["fire_count"] for row in report["motif_fire_rates"]}
    assert rates[("crn", "closure")] == 1
    assert report.get("private_runtime_boundary", {}).get("evidence_private") is True or report["mode_tag"] == "exploratory"
