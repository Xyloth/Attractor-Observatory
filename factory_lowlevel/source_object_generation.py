"""Validation harness for TASK-SOURCE-OBJ-GEN.

This is intentionally network-free by default. The adapters may validate live
source homes when explicitly requested, but the acceptance tests use bundled
authoritative source-object seeds so CI does not depend on external uptime.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from factory_lowlevel.adapters import (
    BoundaryRegionSamplesAdapter,
    EntityObservationsAdapter,
    ExternalChannelSamplesAdapter,
    PerturbationResponseEnsembleAdapter,
)
from factory_lowlevel.schemas import canonical_json, sha256


SOURCE_OBJECT_ADAPTERS = (
    PerturbationResponseEnsembleAdapter,
    EntityObservationsAdapter,
    ExternalChannelSamplesAdapter,
    BoundaryRegionSamplesAdapter,
)


REQUIRED_PROVENANCE_FIELDS = (
    "source_url",
    "source_home",
    "retrieval_timestamp",
    "retrieved_at",
    "parser_version",
    "authority",
    "license_class",
    "raw_exported",
)


def build_source_object_generation_report(
    *,
    cache_dir: str | Path = "reports/source_object_generation/source_cache",
    report_path: str | Path = "reports/source_object_generation/source_object_generation_report.json",
    allow_network: bool = False,
) -> dict[str, Any]:
    report_root = Path(report_path).parent
    report_root.mkdir(parents=True, exist_ok=True)

    corpus_rows: list[dict[str, Any]] = []
    all_records: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    source_ids: list[str] = []

    for adapter_cls in SOURCE_OBJECT_ADAPTERS:
        adapter = adapter_cls()
        result = adapter.fetch(cache_dir, allow_network=allow_network)
        source_ids.append(result.source.source_id)
        records = [record.to_dict() for record in result.records]
        all_records.extend(records)
        accepted_by_world = Counter(record["world_family"] for record in records if not record["payload"].get("is_decoy"))
        decoys_by_kind = Counter(record["payload"].get("decoy_kind") for record in records if record["payload"].get("is_decoy"))
        provenance_missing = [
            record["record_id"]
            for record in records
            if any(field not in record["provenance"] or record["provenance"][field] in ("", None) for field in REQUIRED_PROVENANCE_FIELDS)
            or record["provenance"].get("raw_exported") is not False
        ]
        source_map_missing = [
            record["record_id"]
            for record in records
            if not record["payload"].get("source_object_map") or not record["payload"].get("predicate_safe_split")
        ]
        methodology_missing = [record["record_id"] for record in records if record["payload"].get("methodology_review_required") is not True]
        private_marker_failures = [
            record["record_id"]
            for record in records
            if record["payload"].get("heldout_trajectory_pointer", {}).get("evidence_private") is False
        ]
        min_accepted_ok = all(count >= adapter.accepted_trial_count for count in accepted_by_world.values())
        decoy_ok = set(adapter.decoy_kinds) <= set(kind for kind in decoys_by_kind if kind)
        corpus_passed = (
            bool(records)
            and not result.audits
            and not provenance_missing
            and not source_map_missing
            and not methodology_missing
            and not private_marker_failures
            and min_accepted_ok
            and decoy_ok
        )
        if not corpus_passed:
            failures.append(
                {
                    "corpus": adapter.source_object_type,
                    "audit_count": len(result.audits),
                    "provenance_missing": provenance_missing[:8],
                    "source_map_missing": source_map_missing[:8],
                    "methodology_missing": methodology_missing[:8],
                    "private_marker_failures": private_marker_failures[:8],
                    "accepted_by_world": dict(accepted_by_world),
                    "decoys_by_kind": dict(decoys_by_kind),
                }
            )
        corpus_rows.append(
            {
                "corpus": adapter.source_object_type,
                "adapter_id": adapter.adapter_id,
                "source_id": result.source.source_id,
                "source_home": result.source.url,
                "license_class": result.source.license_class,
                "record_count": len(records),
                "accepted_count": sum(accepted_by_world.values()),
                "decoy_count": sum(decoys_by_kind.values()),
                "accepted_by_world": dict(sorted(accepted_by_world.items())),
                "decoys_by_kind": dict(sorted(decoys_by_kind.items())),
                "predicate_safe_split_documented": all(bool(record["payload"].get("predicate_safe_split")) for record in records),
                "source_object_map_declared": all(bool(record["payload"].get("source_object_map")) for record in records),
                "methodology_review_required_confirmed": all(record["payload"].get("methodology_review_required") is True for record in records),
                "provenance_complete": not provenance_missing,
                "audits": [audit.__dict__ for audit in result.audits],
                "warnings": list(result.warnings),
            }
        )

    records_by_corpus = defaultdict(int)
    accepted_by_corpus = defaultdict(int)
    decoys_by_corpus = defaultdict(int)
    for record in all_records:
        corpus = record["payload"]["source_object_type"]
        records_by_corpus[corpus] += 1
        if record["payload"].get("is_decoy"):
            decoys_by_corpus[corpus] += 1
        else:
            accepted_by_corpus[corpus] += 1

    content_hash = sha256(
        {
            "source_ids": sorted(source_ids),
            "record_ids": sorted(record["record_id"] for record in all_records),
            "records_by_corpus": dict(sorted(records_by_corpus.items())),
        }
    )
    report = {
        "task_id": "TASK-SOURCE-OBJ-GEN",
        "schema": "SourceObjectGenerationReport.v0",
        "mode_tag": "exploratory",
        "claim_bearing_promotions": 0,
        "status": "green" if not failures else "red",
        "corpus_count": len(corpus_rows),
        "total_records": len(all_records),
        "total_accepted_records": sum(accepted_by_corpus.values()),
        "total_decoy_records": sum(decoys_by_corpus.values()),
        "records_by_corpus": dict(sorted(records_by_corpus.items())),
        "accepted_by_corpus": dict(sorted(accepted_by_corpus.items())),
        "decoys_by_corpus": dict(sorted(decoys_by_corpus.items())),
        "corpora": corpus_rows,
        "pilot_ingestion_verification": {
            "trace_verification_applicable": False,
            "trace_verification_reason": "source-object corpora feed Round 2c lens recovery; they are not world-simulation traces",
            "provenance_completeness": all(row["provenance_complete"] for row in corpus_rows),
            "methodology_review_required_propagation": all(row["methodology_review_required_confirmed"] for row in corpus_rows),
            "d26_source_object_map_declared": all(row["source_object_map_declared"] for row in corpus_rows),
            "predicate_safe_split_documented": all(row["predicate_safe_split_documented"] for row in corpus_rows),
            "license_enforcement": "metadata_only_raw_exported_false_all_records",
        },
        "forbidden_zone_check": {
            "floor_connectivity_touched": False,
            "formalism_touched": False,
            "motif_contracts_touched": False,
            "claim_bearing_promotions": 0,
        },
        "failures": failures,
        "content_hash": content_hash,
    }
    Path(report_path).write_text(canonical_json(report), encoding="utf-8")
    return report


if __name__ == "__main__":
    result = build_source_object_generation_report()
    print(canonical_json({"status": result["status"], "total_records": result["total_records"], "content_hash": result["content_hash"]}))
