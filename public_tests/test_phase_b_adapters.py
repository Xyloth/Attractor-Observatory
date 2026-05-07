from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from factory_lowlevel.adapters import (  # noqa: E402
    AllenBrainCognitiveAdapter,
    AvidaDigitalTraceAdapter,
    BioModelsHypergraphAdapter,
    FlyBaseMorphogenProfileAdapter,
    GBIFJornadaEcosystemAdapter,
    MovebankSwarmBehaviorAdapter,
    NCBIEndosymbiosisGenomeAdapter,
    NCBIHIVQuasispeciesAdapter,
    PhysiomeMultiscaleAdapter,
    PrebioticChemistryCatalogAdapter,
    ReactionDiffusionBenchmarkAdapter,
    SzostakLiposomeProtocellAdapter,
)
from factory_lowlevel.router import routing_rejections  # noqa: E402
from factory_lowlevel.continuous_daemon import _apply_force_refresh  # noqa: E402


PHASE_B_ADAPTERS = {
    "protocell": (SzostakLiposomeProtocellAdapter, 50),
    "field": (ReactionDiffusionBenchmarkAdapter, 100),
    "morphogenesis": (FlyBaseMorphogenProfileAdapter, 100),
    "digital": (AvidaDigitalTraceAdapter, 50),
    "ecosystem": (GBIFJornadaEcosystemAdapter, 100),
    "swarm": (MovebankSwarmBehaviorAdapter, 50),
    "cognitive": (AllenBrainCognitiveAdapter, 50),
    "origins_chemistry": (PrebioticChemistryCatalogAdapter, 100),
    "hypergraph_reactions": (BioModelsHypergraphAdapter, 50),
    "quasispecies": (NCBIHIVQuasispeciesAdapter, 100),
    "symbiogenesis": (NCBIEndosymbiosisGenomeAdapter, 50),
    "multiscale": (PhysiomeMultiscaleAdapter, 3),
}


def test_phase_b_adapters_hit_ratified_phase1_targets_offline(tmp_path):
    for world, (adapter_cls, target) in PHASE_B_ADAPTERS.items():
        result = adapter_cls().fetch(tmp_path / "cache", allow_network=False)
        assert result.source.target_world == world
        assert len(result.records) == target
        assert result.cache_entry.record_count == target
        assert not result.audits
        assert {record.world_family for record in result.records} == {world}
        assert len({record.record_id for record in result.records}) == target


def test_phase_b_records_match_router_contract_and_provenance(tmp_path):
    required_provenance = {"source_url", "retrieval_timestamp", "parser_version", "authority", "raw_exported"}
    for world, (adapter_cls, _) in PHASE_B_ADAPTERS.items():
        result = adapter_cls().fetch(tmp_path / "cache", allow_network=False)
        assert routing_rejections(result.records, {world}) == []
        for record in result.records[:5]:
            assert required_provenance <= set(record.provenance)
            assert record.provenance["raw_exported"] is False
            assert record.license_class == result.source.license_class
            assert record.payload.get("methodology_review_required") is True
            assert isinstance(record.payload.get("world_parameters"), dict)


def test_phase_b_overlap_adapters_declare_distinct_simulation_cut(tmp_path):
    overlap_adapters = [
        GBIFJornadaEcosystemAdapter,
        MovebankSwarmBehaviorAdapter,
        NCBIHIVQuasispeciesAdapter,
    ]
    for adapter_cls in overlap_adapters:
        result = adapter_cls().fetch(tmp_path / "cache", allow_network=False)
        cuts = {record.payload.get("adapter_record_cut", "") for record in result.records[:8]}
        assert cuts
        assert all("Phase-B" in cut for cut in cuts)
        assert all("source-object" in cut or "source_object" in cut or "simulation" in cut for cut in cuts)


def test_w0_w1_payload_contract_routes_phase_a_records(tmp_path):
    from factory_lowlevel.adapters import KEGGOrganismCRNAdapter, MathPrimitivesCatalogAdapter

    math = MathPrimitivesCatalogAdapter().fetch(tmp_path / "cache", allow_network=False)
    crn_adapter = KEGGOrganismCRNAdapter(organism_codes=("eco",))
    crn = crn_adapter.fetch(tmp_path / "cache", allow_network=False)
    assert len(math.records) == 200
    assert len(crn.records) == 1
    assert routing_rejections(math.records, {"math_primitives"}) == []
    assert routing_rejections(crn.records, {"crn"}) == []
    assert all(isinstance(record.payload.get("world_parameters"), dict) for record in crn.records)

    source = crn_adapter.source_definition()
    raw = "path:ecj00010\tGlycolysis / Gluconeogenesis - Escherichia coli K-12 W3110\npath:ecj00020\tCitrate cycle - Escherichia coli K-12 W3110\n"
    record, audit = crn_adapter._record_for_organism(
        source=source,
        organism_code="ecj",
        organism_name="Escherichia coli K-12 W3110",
        kingdom="bacteria",
        raw=raw,
        retrieval_mode="cache",
    )
    assert audit is None
    assert routing_rejections([record], {"crn"}) == []


def test_force_refresh_clears_state_with_audit_payload():
    state = {"schema": "FactoryDaemonState.v1", "last_success_by_source": {"a": "2026-05-01T00:00:00Z", "b": "2026-05-01T00:00:00Z"}}
    row = _apply_force_refresh(state, clear_all=False, source_ids=["b", "missing"])
    assert row["record_type"] == "force_refresh_clearance"
    assert row["cleared_source_ids"] == ["b"]
    assert row["requested_missing_source_ids"] == ["missing"]
    assert set(state["last_success_by_source"]) == {"a"}

    row_all = _apply_force_refresh(state, clear_all=True, source_ids=[])
    assert row_all["cleared_source_ids"] == ["a"]
    assert state["last_success_by_source"] == {}
