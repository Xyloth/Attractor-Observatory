"""End-to-end autonomous low-level Factory run."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .adapters import MathPrimitivesCatalogAdapter, NISTAtomicSpectraAdapter, PubChemSmallMoleculeAdapter
from .normalization import normalize_record
from .persistence import LowLevelFactoryStore
from .registry import SourceRegistry
from .router import route_records
from .schemas import EmpiricalRecord, NormalizedReference, utc_now


def run_low_level_factory(
    *,
    store_root: str | Path = "reports/campaign_016/factory_store",
    cache_dir: str | Path = "reports/campaign_016/source_cache",
    allow_network: bool = True,
) -> dict[str, Any]:
    registry = SourceRegistry()
    adapters = [NISTAtomicSpectraAdapter(), PubChemSmallMoleculeAdapter(), MathPrimitivesCatalogAdapter()]
    store = LowLevelFactoryStore(store_root)
    records: list[EmpiricalRecord] = []
    refs: list[NormalizedReference] = []
    warnings: list[str] = []

    for adapter in adapters:
        source = adapter.source_definition()
        registry.register(source)
        result = adapter.fetch(cache_dir, allow_network=allow_network)
        warnings.extend(result.warnings)
        store.ingest_source_cache(result.cache_entry)
        store.ingest_empirical_records(result.records)
        # CB-008 Bug C fix: route adapter-level honest negatives into the
        # audit queue so partial-data records never persist silently.
        if getattr(result, "audits", None):
            store.ingest_adapter_audits(result.audits)
        records.extend(result.records)
        normalized = [normalize_record(record) for record in result.records]
        store.ingest_normalized_refs(normalized)
        refs.extend(normalized)
    store.rebuild_evidence_graph()
    routed = route_records(records, refs)
    # CB-008 Bug E fix: persist routed-world traces with content_hash so
    # the trace verifier can prove every routed record produced a real
    # trace file (was: routed bundles returned in-memory only, never
    # persisted; the brief required "100% routed records produce
    # verified traces"). Run id seed is the pre-trace content hash so
    # subsequent runs with identical inputs get identical trace ids.
    store.ingest_world_traces(routed, run_id_seed=store.content_hash())
    snapshot = store.write()
    return {
        "schema": "LowLevelFactoryRun.v1",
        "run_id": snapshot["content_hash"],
        "started_at": utc_now(),
        "completed_at": utc_now(),
        "requires_ai_runtime": False,
        "registry": registry.to_dict(),
        "store_snapshot": snapshot,
        "routed_worlds": [bundle.to_dict() for bundle in routed],
        "records": [record.to_dict() for record in sorted(records, key=lambda row: row.record_id)],
        "normalized_refs": [ref.to_dict() for ref in sorted(refs, key=lambda row: row.normalized_id)],
        "warnings": warnings,
    }
