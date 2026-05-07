from __future__ import annotations

from collections import Counter
from pathlib import Path

from factory_lowlevel.adapters import (
    BoundaryRegionSamplesAdapter,
    EntityObservationsAdapter,
    ExternalChannelSamplesAdapter,
    PerturbationResponseEnsembleAdapter,
)
from factory_lowlevel.source_object_generation import build_source_object_generation_report


ADAPTERS = (
    PerturbationResponseEnsembleAdapter,
    EntityObservationsAdapter,
    ExternalChannelSamplesAdapter,
    BoundaryRegionSamplesAdapter,
)


def test_source_object_adapters_emit_required_records_and_decoys(tmp_path):
    for adapter_cls in ADAPTERS:
        adapter = adapter_cls()
        result = adapter.fetch(tmp_path / "cache", allow_network=False)
        accepted = [record for record in result.records if not record.payload["is_decoy"]]
        decoys = [record for record in result.records if record.payload["is_decoy"]]
        accepted_by_world = Counter(record.world_family for record in accepted)
        decoys_by_kind = Counter(record.payload["decoy_kind"] for record in decoys)

        assert not result.audits
        assert accepted
        assert all(count >= 30 for count in accepted_by_world.values())
        assert set(adapter.decoy_kinds) <= set(decoys_by_kind)
        assert all(record.mode_tag == "exploratory" for record in result.records)
        assert all(record.payload["claim_bearing"] is False for record in result.records)


def test_source_object_records_are_d26_d29_and_provenance_safe(tmp_path):
    required_provenance = {
        "source_url",
        "source_home",
        "retrieval_timestamp",
        "retrieved_at",
        "parser_version",
        "authority",
        "license_class",
        "raw_exported",
    }
    for adapter_cls in ADAPTERS:
        result = adapter_cls().fetch(tmp_path / "cache", allow_network=False)
        for record in result.records:
            assert record.license_class == "metadata_only"
            assert required_provenance <= set(record.provenance)
            assert record.provenance["raw_exported"] is False
            assert record.provenance["evidence_private"] is False
            assert record.payload["methodology_review_required"] is True
            assert record.payload["source_object_map"]["source_object_type"] == record.payload["source_object_type"]
            assert record.payload["source_object_map"]["predicate_inputs"]
            assert record.payload["source_object_map"]["lens_inputs"]
            assert record.payload["predicate_safe_split"]["split_locked"] is True
            pointer = record.payload.get("heldout_trajectory_pointer")
            if pointer:
                assert pointer["evidence_private"] is True


def test_source_object_report_goes_green(tmp_path):
    report = build_source_object_generation_report(
        cache_dir=tmp_path / "cache",
        report_path=tmp_path / "source_object_generation_report.json",
        allow_network=False,
    )
    assert report["status"] == "green"
    assert report["corpus_count"] == 4
    assert report["total_records"] == 499
    assert report["total_accepted_records"] == 450
    assert report["total_decoy_records"] == 49
    assert report["claim_bearing_promotions"] == 0
    assert report["pilot_ingestion_verification"]["provenance_completeness"] is True
    assert report["pilot_ingestion_verification"]["methodology_review_required_propagation"] is True
    assert report["pilot_ingestion_verification"]["d26_source_object_map_declared"] is True
    assert report["forbidden_zone_check"]["floor_connectivity_touched"] is False


def test_source_object_contracts_do_not_include_floor_connectivity(tmp_path):
    for adapter_cls in ADAPTERS:
        result = adapter_cls().fetch(tmp_path / "cache", allow_network=False)
        for record in result.records:
            serialized = str(record.to_dict()).lower()
            assert "floor_connectivity" not in serialized


def test_measurability_recovery_plan_marks_only_generated_non_floor_sources_ready():
    plan = Path("papers/methods/MEASURABILITY_RECOVERY_PLAN_v1.md").read_text(encoding="utf-8")
    assert plan.count("| perturbation_response_ensemble | yes_task_source_obj_gen |") == 6
    assert plan.count("| entity_observations | yes_task_source_obj_gen |") == 5
    assert plan.count("| external_channel_samples | yes_task_source_obj_gen_refresh |") == 1
    assert plan.count("| boundary_region_samples | yes_task_source_obj_gen |") == 1
    assert "| boundary_maintenance_reaction_network | no_can_be_generated |" in plan
    assert "| boundary_maintenance_transition_system | no_can_be_generated |" in plan
    ready_rows = [
        line
        for line in plan.splitlines()
        if line.startswith("| motif.") and "ready_for_round_2c_implementation" in line
    ]
    non_floor_ready_rows = [line for line in ready_rows if "motif.floor_connectivity.draft" not in line]
    assert len(non_floor_ready_rows) == 13
