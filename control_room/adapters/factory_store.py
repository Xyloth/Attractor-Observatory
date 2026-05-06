"""Parse Campaign 016 Factory store: empirical_records + normalized_refs +
evidence_graph + factory_intake_dock_state + detector_coverage.

Campaign 016 shipped a working autonomous Factory at the low level
(NIST atomic / PubChem molecules / math primitives). The Factory store
is the persistence layer; this adapter surfaces it for the Pulse Deck,
Doctrine Console, and Factory Intake Dock rooms.

Detector decline pattern (96/96 declined at low-level primitives) is
itself a load-bearing finding per Campaign 016's interpretation note —
'retained as honest signal for formalism extension rather than patched
during Campaign 016'. The adapter surfaces this verbatim; downstream
rooms are responsible for rendering it as a published signal, not
suppressing it. D17 (floor falsifiers are publishable) binds.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def parse_factory_store(
    factory_dir: str | Path = "reports/campaign_016/factory_store",
    intake_dock_state: str | Path = "reports/campaign_016/factory_intake_dock_state.json",
    detector_coverage: str | Path = "reports/campaign_016/detector_coverage.json",
) -> dict[str, Any]:
    """Parse Campaign 016 factory persistence + detector coverage."""
    fd = Path(factory_dir)
    if not fd.exists():
        return {
            "status": "missing",
            "data": None,
            "rationale": f"Campaign 016 factory_store not found at {fd.as_posix()}",
        }
    if not fd.is_dir():
        return {
            "status": "malformed",
            "data": None,
            "rationale": f"{fd.as_posix()} is not a directory",
        }
    payloads: dict[str, Any] = {}
    for filename, key in (
        ("empirical_records.json", "empirical"),
        ("normalized_refs.json", "normalized"),
        ("evidence_graph.json", "evidence"),
        ("audit_queue.json", "audit_queue"),
        ("source_cache_index.json", "source_cache"),
        ("snapshot.json", "snapshot"),
    ):
        path = fd / filename
        if not path.exists():
            payloads[key] = {"present": False, "path": path.as_posix()}
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
            payloads[key] = {"present": True, "path": path.as_posix(), "data": data}
        except (OSError, json.JSONDecodeError) as exc:
            payloads[key] = {"present": True, "path": path.as_posix(), "error": repr(exc)}
    intake_dock = _maybe_load(Path(intake_dock_state))
    detector = _maybe_load(Path(detector_coverage))
    summary = _summarize(payloads, intake_dock, detector)
    return {
        "status": "ok",
        "data": {
            "factory_dir": fd.as_posix(),
            "store_payloads": payloads,
            "intake_dock_state": intake_dock,
            "detector_coverage": detector,
            "summary": summary,
        },
        "rationale": (
            f"factory store: {summary['empirical_count']} empirical records, "
            f"{summary['normalized_count']} normalized refs, "
            f"{summary['edge_count']} evidence edges; "
            f"detector decline {summary['detector_decline_rate']:.2f} "
            f"({summary['detector_declined']}/{summary['detector_evaluations']})"
        ),
    }


def _maybe_load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"present": False, "path": path.as_posix()}
    try:
        return {
            "present": True,
            "path": path.as_posix(),
            "data": json.loads(path.read_text(encoding="utf-8-sig")),
        }
    except (OSError, json.JSONDecodeError) as exc:
        return {"present": True, "path": path.as_posix(), "error": repr(exc)}


def _summarize(
    payloads: dict[str, Any],
    intake_dock: dict[str, Any],
    detector: dict[str, Any],
) -> dict[str, Any]:
    def _count(payload_key: str, list_key: str) -> int:
        item = payloads.get(payload_key, {})
        if not item.get("present") or "data" not in item:
            return 0
        data = item["data"]
        if isinstance(data, dict):
            value = data.get(list_key)
            return len(value) if isinstance(value, list) else 0
        if isinstance(data, list):
            return len(data)
        return 0

    empirical = _count("empirical", "records")
    normalized = _count("normalized", "records")
    edges = _count("evidence", "edges")
    audit_queue = _count("audit_queue", "items") or _count("audit_queue", "records")
    source_cache = _count("source_cache", "entries") or _count("source_cache", "records")
    evidence_private_count = _count_private_evidence(payloads, intake_dock, detector)

    declined = 0
    evaluations = 0
    decline_rate = 0.0
    detector_data = detector.get("data") if detector.get("present") else {}
    if isinstance(detector_data, dict):
        # Attempt several shape variations.
        declined = int(detector_data.get("declined_count") or 0)
        evaluations = int(detector_data.get("evaluation_count") or 0)
    intake_dock_data = intake_dock.get("data") if intake_dock.get("present") else {}
    if isinstance(intake_dock_data, dict):
        ds = intake_dock_data.get("detector_summary") or {}
        if not declined:
            declined = int(ds.get("declined_count") or 0)
        if not evaluations:
            evaluations = int(ds.get("evaluation_count") or 0)
    if evaluations:
        decline_rate = declined / evaluations

    return {
        "empirical_count": empirical,
        "normalized_count": normalized,
        "edge_count": edges,
        "audit_queue_count": audit_queue,
        "source_cache_count": source_cache,
        "evidence_private_count": evidence_private_count,
        "evidence_private_status": "present" if evidence_private_count else "none_detected",
        "detector_declined": declined,
        "detector_evaluations": evaluations,
        "detector_decline_rate": decline_rate,
        "intake_dock_status": (intake_dock_data or {}).get("status"),
        "claim_bearing_promotions": (intake_dock_data or {}).get("claim_bearing_promotions"),
    }


def _count_private_evidence(*payload_roots: dict[str, Any]) -> int:
    count = 0

    def visit(node: Any) -> None:
        nonlocal count
        if isinstance(node, dict):
            if node.get("evidence_private") is True:
                count += 1
            for value in node.values():
                visit(value)
        elif isinstance(node, list):
            for item in node:
                visit(item)

    for root in payload_roots:
        visit(root)
    return count
