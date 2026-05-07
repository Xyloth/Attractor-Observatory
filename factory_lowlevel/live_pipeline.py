"""TASK-033 multi-world Factory live runner.

This module leaves the Campaign 016 W-1/W0 runner unchanged and adds an
exploratory, source-bound path for higher-world ingestion into W1/W3/W6/W9/W11.
Runtime remains daemon code, not AI-in-the-loop: adapters fetch/parse, the
router validates, world constructors simulate, and formal lenses evaluate.
"""

from __future__ import annotations

import json
import hashlib
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:  # D29: private formalism runtime is optional on the public branch.
    from formalism.lens_registry import MOTIFS, _label_feature_for_motif, evaluate_lenses
except ModuleNotFoundError as exc:  # pragma: no cover - exercised by public-surface installs.
    if exc.name and exc.name.split(".")[0] != "formalism":
        raise
    MOTIFS = (
        "motif.autocatalytic_closure.draft",
        "motif.self_maintained_boundary.draft",
        "motif.repair.draft",
        "motif.replication_lineage.draft",
        "motif.externalized_memory.draft",
        "motif.floor_connectivity.draft",
    )

    def _label_feature_for_motif(motif_id: str, trace: dict[str, Any]) -> bool:
        flags = trace.get("process_flags", {}) if isinstance(trace, dict) else {}
        if not isinstance(flags, dict):
            flags = {}
        short = _motif_short(motif_id)
        return bool(flags.get(short) or flags.get(motif_id) or flags.get(short.replace("closure", "autocatalytic_closure")))

    def evaluate_lenses(evidence_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        rows = []
        for evidence in evidence_rows:
            trace = evidence.get("trace", {})
            trace_id = trace.get("manifest", {}).get("trace_id", sha256(trace)) if isinstance(trace, dict) else sha256(evidence)
            rows.append(
                {
                    "lens_id": "public_runtime_boundary",
                    "motif_id": evidence.get("motif_id"),
                    "trace_id": trace_id,
                    "declined": True,
                    "prediction_score": 0.0,
                    "evidence_private": True,
                    "trace_path_status": "private_unshipped",
                    "decline_reason": "private formalism runtime is not shipped on the public branch; D29 narrative fallback",
                }
            )
        return rows

try:  # D29: trace schema lives in the private trace plane.
    from trace.schema.v1 import canonical_json, trace_content_hash
except ModuleNotFoundError as exc:  # pragma: no cover - exercised by public-surface installs.
    if exc.name and exc.name.split(".")[0] != "trace":
        raise

    def canonical_json(payload: Any) -> str:
        return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)

    def trace_content_hash(trace: dict[str, Any]) -> str:
        return hashlib.sha256(canonical_json(trace).encode("utf-8")).hexdigest()

from .adapters import (
    AllenBrainCognitiveAdapter,
    AvidaDigitalTraceAdapter,
    BioModelsHypergraphAdapter,
    FlyBaseMorphogenProfileAdapter,
    GBIFJornadaEcosystemAdapter,
    KEGGEcoliCRNAdapter,
    KEGGOrganismCRNAdapter,
    MathPrimitivesCatalogAdapter,
    MovebankSwarmBehaviorAdapter,
    NCBIEndosymbiosisGenomeAdapter,
    NCBIHIVQuasispeciesAdapter,
    NISTAtomicSpectraAdapter,
    PhysiomeMultiscaleAdapter,
    PrebioticChemistryCatalogAdapter,
    PubChemSmallMoleculeAdapter,
    ReactionDiffusionBenchmarkAdapter,
    SzostakLiposomeProtocellAdapter,
)
from .normalization import normalize_record
from .persistence import LowLevelFactoryStore, atomic_write_json
from .registry import SourceRegistry
from .router import route_records, routing_rejections
from .schemas import AuditQueueItem, EmpiricalRecord, NormalizedReference, sha256, utc_now


TASK033_ADAPTERS = (
    KEGGEcoliCRNAdapter,
    ReactionDiffusionBenchmarkAdapter,
    GBIFJornadaEcosystemAdapter,
    PrebioticChemistryCatalogAdapter,
    NCBIHIVQuasispeciesAdapter,
)

# CB-015 T4 — KEGG generalized to top-50 reference organisms.
# Registered as a separate adapter from KEGGEcoliCRNAdapter so the
# original eco-only path remains available for tests that pin the
# legacy single-organism behavior. The generalized adapter emits one
# record per organism (50 records when --allow-network).
CB015_ADAPTERS = (
    KEGGOrganismCRNAdapter,
)

TASK035_ADAPTERS = (
    SzostakLiposomeProtocellAdapter,
    FlyBaseMorphogenProfileAdapter,
    AvidaDigitalTraceAdapter,
    MovebankSwarmBehaviorAdapter,
    AllenBrainCognitiveAdapter,
    BioModelsHypergraphAdapter,
    NCBIEndosymbiosisGenomeAdapter,
    PhysiomeMultiscaleAdapter,
)

ALL_FACTORY_ADAPTERS = (
    NISTAtomicSpectraAdapter,
    PubChemSmallMoleculeAdapter,
    MathPrimitivesCatalogAdapter,
    *TASK033_ADAPTERS,
    *TASK035_ADAPTERS,
    *CB015_ADAPTERS,
)

WORLD_LABELS = {
    "atomic_molecular_primitives": "W-1 Atomic / Molecular",
    "math_primitives": "W0 Math Primitives",
    "crn": "W1 CRN",
    "protocell": "W2 Protocell",
    "field": "W3 Field",
    "morphogenesis": "W4 Morphogenesis",
    "digital": "W5 Digital",
    "ecosystem": "W6 Ecosystem",
    "swarm": "W7 Swarm",
    "cognitive": "W8 Cognitive",
    "origins_chemistry": "W9 Origins Chemistry",
    "hypergraph_reactions": "W10 Hypergraph Reactions",
    "quasispecies": "W11 Quasispecies",
    "symbiogenesis": "W12 Symbiogenesis",
    "multiscale": "W13 Multiscale",
}

LIVE_STAGE_IDS = ("download", "parse", "normalize", "route", "world_simulate", "motif_evaluate", "audit")


def available_adapters() -> list[dict[str, Any]]:
    rows = []
    for adapter_cls in ALL_FACTORY_ADAPTERS:
        adapter = adapter_cls()
        source = adapter.source_definition()
        rows.append(
            {
                "adapter_id": adapter.adapter_id,
                "source_id": source.source_id,
                "name": source.name,
                "target_world": source.target_world,
                "target_world_label": WORLD_LABELS.get(source.target_world, source.target_world),
                "refresh_cadence": source.refresh_cadence,
                "retrieval_mode_default": source.retrieval_mode_default,
            }
        )
    return rows


def run_live_factory_cycle(
    *,
    target_worlds: list[str] | None = None,
    source_ids: list[str] | None = None,
    allow_network: bool = False,
    store_root: str | Path = "reports/campaign_021/factory_store",
    cache_dir: str | Path = "reports/campaign_021/source_cache",
    run_root: str | Path = "control_room/cache/factory_runs",
    trace_root: str | Path = "reports/campaign_021/traces",
    trigger: str = "manual_fire",
) -> dict[str, Any]:
    started_at = utc_now()
    run_root = Path(run_root)
    trace_root = Path(trace_root)
    live_state_path = run_root / "latest_state.json"
    _write_live_state(live_state_path, stage="download", status="running", started_at=started_at, target_worlds=target_worlds or [], source_ids=source_ids or [])

    adapters = _select_adapters(target_worlds=target_worlds, source_ids=source_ids)
    registry = SourceRegistry()
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
        store.ingest_adapter_audits(getattr(result, "audits", []))
        records.extend(result.records)
    _write_live_state(live_state_path, stage="parse", status="running", record_count=len(records), source_count=len(adapters))

    for record in records:
        refs.append(normalize_record(record))
    store.ingest_normalized_refs(refs)
    _write_live_state(live_state_path, stage="normalize", status="running", normalized_count=len(refs))

    requested_worlds = set(target_worlds or [adapter.source_definition().target_world for adapter in adapters])
    route_rejections = routing_rejections(records, requested_worlds)
    for rejection in route_rejections:
        audit_id = sha256({"routing_rejection": rejection.to_dict()})
        store.audit_queue[audit_id] = AuditQueueItem(
            audit_id=audit_id,
            severity=rejection.audit_severity,
            reason=f"routing_rejection:{rejection.reason}",
            record_id=rejection.record_id,
            source_id=rejection.source_id,
            recommended_action="hold_record_for_audit_before_world_simulation",
        )
    routed = route_records(records, refs, requested_worlds)
    _write_live_state(live_state_path, stage="route", status="running", routed_worlds=[bundle.world_family for bundle in routed], rejection_count=len(route_rejections))

    trace_rows = []
    for bundle in routed:
        for record in bundle.empirical_records:
            trace_rows.append(_simulate_record(record, trace_root=trace_root))
            _write_live_state(
                live_state_path,
                stage="world_simulate",
                status="running",
                latest_record=record.canonical_name,
                trace_count=len(trace_rows),
            )
    traces = [row["trace"] for row in trace_rows if row.get("trace") is not None]

    evidence_rows = _build_evidence_rows(traces)
    evaluations = evaluate_lenses(evidence_rows) if evidence_rows else []
    life_forms = _life_forms(trace_rows, evaluations)
    motif_fire_rates = _motif_fire_rates(life_forms)
    _write_live_state(live_state_path, stage="motif_evaluate", status="running", trace_count=len(traces), life_form_count=len(life_forms))

    store.rebuild_evidence_graph()
    snapshot = store.write()
    completed_at = utc_now()
    run_payload = {
        "schema": "Task033MultiWorldFactoryRun.v1",
        "mode_tag": "exploratory",
        "requires_ai_runtime": False,
        "trigger": trigger,
        "started_at": started_at,
        "completed_at": completed_at,
        "allow_network": bool(allow_network),
        "target_worlds": sorted(requested_worlds),
        "source_ids": [adapter.source_definition().source_id for adapter in adapters],
        "registry": registry.to_dict(),
        "store_snapshot": snapshot,
        "routed_worlds": [bundle.to_dict() for bundle in routed],
        "routing_rejections": [row.to_dict() for row in route_rejections],
        "records": [record.to_dict() for record in sorted(records, key=lambda row: row.record_id)],
        "normalized_refs": [ref.to_dict() for ref in sorted(refs, key=lambda row: row.normalized_id)],
        "trace_records": [_trace_row_public(row) for row in trace_rows],
        "lens_evaluations": evaluations,
        "life_forms": life_forms,
        "motif_fire_rates": motif_fire_rates,
        "warnings": warnings,
        "pipeline_stages": [{"stage": stage, "status": "done"} for stage in LIVE_STAGE_IDS],
    }
    run_id = sha256({key: value for key, value in run_payload.items() if key != "run_id"})
    run_payload["run_id"] = run_id
    run_payload["content_hash"] = run_id
    run_path = run_root / f"run_{run_id.removeprefix('sha256:')[:16]}.json"
    _safe_write_json(run_path, run_payload)
    _safe_write_json(run_root / "latest_run.json", run_payload)
    _write_live_state(live_state_path, stage="audit", status="done", run_id=run_id, audit_count=snapshot["counts"]["audit_queue_items"], run_path=str(run_path))
    return run_payload


def _select_adapters(*, target_worlds: list[str] | None, source_ids: list[str] | None) -> list[Any]:
    selected_worlds = set(target_worlds or [])
    selected_sources = set(source_ids or [])
    adapters = []
    for adapter_cls in ALL_FACTORY_ADAPTERS:
        adapter = adapter_cls()
        source = adapter.source_definition()
        if selected_sources and source.source_id not in selected_sources:
            continue
        if selected_worlds and source.target_world not in selected_worlds:
            continue
        adapters.append(adapter)
    if not adapters:
        raise ValueError("no adapters selected for requested target_worlds/source_ids")
    return adapters


def _simulate_record(record: EmpiricalRecord, *, trace_root: Path) -> dict[str, Any]:
    record_trace_dir = trace_root / record.world_family
    trace_path = record_trace_dir / f"{record.record_id.removeprefix('sha256:')[:16]}.json"
    if not (Path(__file__).resolve().parents[1] / "worlds").exists():
        return {
            "record_id": record.record_id,
            "canonical_name": record.canonical_name,
            "source_id": record.source_id,
            "world_family": record.world_family,
            "trace": None,
            "trace_path": None,
            "rejections": [
                {
                    "record_id": record.record_id,
                    "reason": "private_world_runtime_unshipped",
                    "evidence_private": True,
                    "trace_path_status": "private_unshipped",
                    "recommended_action": "use public campaign reports or request private runtime access from PI",
                }
            ],
        }
    if record.world_family == "atomic_molecular_primitives":
        from worlds.atomic_molecular_primitives.model import AtomicMolecularPrimitivesWorld

        constructed = AtomicMolecularPrimitivesWorld.from_empirical_records([record])
    elif record.world_family == "math_primitives":
        from worlds.math_primitives.model import MathPrimitivesWorld

        constructed = MathPrimitivesWorld.from_empirical_records([record])
    elif record.world_family == "crn":
        from worlds.crn.model import CRNWorld

        constructed = CRNWorld.from_empirical_records([record])
    elif record.world_family == "protocell":
        from worlds.protocell.model import ProtocellWorld

        constructed = ProtocellWorld.from_empirical_records([record])
    elif record.world_family == "field":
        from worlds.field.model import FieldWorld

        constructed = FieldWorld.from_empirical_records([record])
    elif record.world_family == "morphogenesis":
        from worlds.morphogenesis.model import MorphogenesisWorld

        constructed = MorphogenesisWorld.from_empirical_records([record])
    elif record.world_family == "digital":
        from worlds.digital.model import DigitalWorld

        constructed = DigitalWorld.from_empirical_records([record])
    elif record.world_family == "swarm":
        from worlds.swarm.model import SwarmWorld

        constructed = SwarmWorld.from_empirical_records([record])
    elif record.world_family == "cognitive":
        from worlds.cognitive.model import CognitiveWorld

        constructed = CognitiveWorld.from_empirical_records([record])
    elif record.world_family == "origins_chemistry":
        from worlds.origins_chemistry.model import OriginsChemistryWorld

        constructed = OriginsChemistryWorld.from_empirical_records([record])
    elif record.world_family == "hypergraph_reactions":
        from worlds.hypergraph_reactions.model import HypergraphReactionWorld

        constructed = HypergraphReactionWorld.from_empirical_records([record])
    elif record.world_family == "ecosystem":
        from worlds.ecosystem.model import EcosystemWorld

        constructed = EcosystemWorld.from_empirical_records([record])
    elif record.world_family == "quasispecies":
        from worlds.quasispecies.model import QuasispeciesWorld

        constructed = QuasispeciesWorld.from_empirical_records([record])
    elif record.world_family == "symbiogenesis":
        from worlds.symbiogenesis.model import SymbiogenesisWorld

        constructed = SymbiogenesisWorld.from_empirical_records([record])
    elif record.world_family == "multiscale":
        from worlds.multiscale.model import MultiscaleWorld

        constructed = MultiscaleWorld.from_empirical_records([record])
    else:
        return {"record_id": record.record_id, "world_family": record.world_family, "trace": None, "trace_path": None, "rejections": [{"record_id": record.record_id, "reason": "no_world_constructor"}]}
    world = constructed.get("world")
    if world is None:
        return {"record_id": record.record_id, "world_family": record.world_family, "trace": None, "trace_path": None, "rejections": constructed.get("rejections", [])}
    trace = world.export_trace(str(trace_path))
    trace.setdefault("audit_notes", []).append(
        {
            "note_id": "task033_source_bound_projection",
            "record_id": record.record_id,
            "source_id": record.source_id,
            "source_url": record.provenance.get("source_url"),
            "mode_tag": "exploratory",
            "claim_promotion_allowed": False,
        }
    )
    trace["manifest"]["trace_id"] = "sha256:" + trace_content_hash(trace)
    trace_path.write_text(canonical_json(trace) + "\n", encoding="utf-8")
    return {
        "record_id": record.record_id,
        "canonical_name": record.canonical_name,
        "source_id": record.source_id,
        "world_family": record.world_family,
        "trace_path": str(trace_path),
        "trace_id": trace.get("manifest", {}).get("trace_id"),
        "trace": trace,
        "rejections": constructed.get("rejections", []),
    }


def _build_evidence_rows(traces: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for trace in traces:
        trace_id = trace.get("manifest", {}).get("trace_id", sha256(trace))
        for motif_id in MOTIFS:
            rows.append(
                {
                    "evidence_id": sha256({"trace_id": trace_id, "motif_id": motif_id}),
                    "trace": trace,
                    "motif_id": motif_id,
                    "split": "holdout",
                    "label": _label_feature_for_motif(motif_id, trace),
                }
            )
    return rows


def _life_forms(trace_rows: list[dict[str, Any]], evaluations: list[dict[str, Any]]) -> list[dict[str, Any]]:
    evals_by_trace_motif: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in evaluations:
        evals_by_trace_motif[(row["trace_id"], row["motif_id"])].append(row)
    out = []
    for trace_row in trace_rows:
        trace = trace_row.get("trace")
        if trace is None:
            out.append(
                {
                    "record_id": trace_row["record_id"],
                    "canonical_name": trace_row.get("canonical_name", trace_row["record_id"]),
                    "world_family": trace_row["world_family"],
                    "trace_path": None,
                    "motif_fires": {},
                    "lens_nondeclines": {},
                    "status": "rejected",
                    "rejections": trace_row.get("rejections", []),
                }
            )
            continue
        trace_id = trace.get("manifest", {}).get("trace_id", "")
        motif_fires = {}
        lens_nondeclines = {}
        lens_fire_counts = {}
        for motif_id in MOTIFS:
            short = _motif_short(motif_id)
            motif_rows = evals_by_trace_motif[(trace_id, motif_id)]
            motif_fires[short] = bool(_label_feature_for_motif(motif_id, trace))
            lens_nondeclines[short] = sum(1 for row in motif_rows if not row["declined"])
            lens_fire_counts[short] = sum(1 for row in motif_rows if not row["declined"] and row["prediction_score"] >= 0.5)
        out.append(
            {
                "record_id": trace_row["record_id"],
                "canonical_name": trace_row.get("canonical_name", trace_row["record_id"]),
                "source_id": trace_row.get("source_id"),
                "world_family": trace_row["world_family"],
                "trace_id": trace_id,
                "trace_path": trace_row.get("trace_path"),
                **_trace_path_boundary(trace_row.get("trace_path")),
                "motif_fires": motif_fires,
                "lens_nondeclines": lens_nondeclines,
                "lens_fire_counts": lens_fire_counts,
                "status": "simulated",
            }
        )
    return out


def _motif_fire_rates(life_forms: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[bool]] = defaultdict(list)
    for item in life_forms:
        if item.get("status") != "simulated":
            continue
        for motif_short, fired in item.get("motif_fires", {}).items():
            grouped[(item["world_family"], motif_short)].append(bool(fired))
    rows = []
    for (world, motif), values in sorted(grouped.items()):
        rows.append(
            {
                "world_family": world,
                "motif": motif,
                "trace_count": len(values),
                "fire_count": sum(1 for value in values if value),
                "fire_rate": round(sum(1 for value in values if value) / max(len(values), 1), 6),
            }
        )
    return rows


def _trace_row_public(row: dict[str, Any]) -> dict[str, Any]:
    public = {key: value for key, value in row.items() if key != "trace"}
    public.update(_trace_path_boundary(public.get("trace_path")))
    return public


def _trace_path_boundary(trace_path: str | None) -> dict[str, Any]:
    if not trace_path:
        return {}
    normalized = str(trace_path).replace("\\", "/")
    if "/traces/" in normalized or normalized.endswith("/traces") or "/daemon_traces/" in normalized:
        return {
            "evidence_private": True,
            "evidence_private_reason": "trace_path points at generated trace storage, not the shipped public surface",
            "trace_path_status": "private_unshipped",
        }
    return {"evidence_private": False, "trace_path_status": "dereferenceable"}


def _motif_short(motif_id: str) -> str:
    return {
        "motif.autocatalytic_closure.draft": "closure",
        "motif.self_maintained_boundary.draft": "boundary",
        "motif.repair.draft": "repair",
        "motif.replication_lineage.draft": "lineage",
        "motif.externalized_memory.draft": "memory",
        "motif.floor_connectivity.draft": "floor",
    }.get(motif_id, motif_id)


def _write_live_state(path: Path, **payload: Any) -> None:
    prior = {}
    if path.exists():
        try:
            prior = json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            prior = {}
    stage_history = list(prior.get("stage_history", []))
    stage_history.append({"at": utc_now(), **payload})
    state = {
        **prior,
        **payload,
        "updated_at": utc_now(),
        "stage_history": stage_history[-200:],
    }
    _safe_write_json(path, state)


def _safe_write_json(path: Path, payload: Any) -> None:
    try:
        atomic_write_json(path, payload)
        return
    except PermissionError:
        data = json.dumps(payload, sort_keys=True, indent=2) + "\n"
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(data, encoding="utf-8")
            return
        except PermissionError:
            fallback = path.parent / f"{path.stem}_{utc_now().replace(':', '').replace('-', '')}{path.suffix}"
            atomic_write_json(fallback, payload)


def summarize_run(run: dict[str, Any]) -> dict[str, Any]:
    source_bytes = 0
    for entry in run.get("registry", {}).get("sources", []):
        source_bytes += len(json.dumps(entry, sort_keys=True).encode("utf-8"))
    simulated = [item for item in run.get("life_forms", []) if item.get("status") == "simulated"]
    by_world = Counter(item["world_family"] for item in simulated)
    return {
        "schema": "Task033MultiWorldFactorySummary.v1",
        "run_id": run["run_id"],
        "mode_tag": "exploratory",
        "adapter_count": len(run.get("source_ids", [])),
        "world_count": len(by_world),
        "simulated_trace_count": len(simulated),
        "records_ingested": len(run.get("records", [])),
        "normalized_refs": len(run.get("normalized_refs", [])),
        "routing_rejections": len(run.get("routing_rejections", [])),
        "source_registry_bytes": source_bytes,
        "traces_by_world": dict(sorted(by_world.items())),
        "motif_fire_rates": run.get("motif_fire_rates", []),
        "warnings": run.get("warnings", []),
    }
