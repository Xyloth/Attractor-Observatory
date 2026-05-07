from __future__ import annotations

import sys
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from factory_lowlevel.live_pipeline import available_adapters  # noqa: E402
from factory_lowlevel.router import routing_rejections  # noqa: E402
from factory_lowlevel.schemas import EmpiricalRecord, sha256  # noqa: E402


def test_task033_adapters_cover_five_higher_worlds():
    rows = available_adapters()
    worlds = {row["target_world"] for row in rows}
    assert {"crn", "field", "ecosystem", "origins_chemistry", "quasispecies"} <= worlds
    assert any(row["source_id"] == "source.kegg.ecoli_mg1655.metabolic_network" for row in rows)
    assert any(row["source_id"] == "source.ncbi.hiv1.reference_quasispecies_pilot" for row in rows)
    assert any(row["source_id"] == "source.gbif.jornada_basin.ecosystem_occurrences" for row in rows)


def test_task033_campaign021_report_records_private_runtime_result():
    report = json.loads((ROOT / "reports/campaign_021/full_report.json").read_text(encoding="utf-8-sig"))
    summary = report["summary"]
    assert summary["world_count"] == 5
    assert summary["records_ingested"] == 8
    assert summary["simulated_trace_count"] == 8
    assert summary["routing_rejections"] == 0
    assert summary["traces_by_world"] == {"crn": 1, "ecosystem": 1, "field": 3, "origins_chemistry": 2, "quasispecies": 1}
    assert report["mode_tag"] == "exploratory"

    rates = {(row["world_family"], row["motif"]): row["fire_count"] for row in report["motif_fire_rates"]}
    assert rates[("crn", "closure")] == 1
    assert rates[("origins_chemistry", "closure")] == 2
    assert rates[("quasispecies", "lineage")] == 1


def test_task033_router_rejects_underdetermined_higher_world_record():
    record = EmpiricalRecord(
        record_id=sha256({"bad": "crn"}),
        source_id="source.test",
        world_family="crn",
        record_type="kegg_metabolic_network_summary",
        canonical_name="Underdetermined CRN",
        payload={"world_parameters": {"initial_state": {"A": 1.0}}},
        provenance={"source_url": "https://example.org", "retrieved_at": "2026-05-06T00:00:00Z"},
        license_class="metadata_only",
    )
    rejections = routing_rejections([record], {"crn"})
    assert Counter(row.reason for row in rejections) == Counter({"crn_requires_initial_state_and_reactions": 1})
