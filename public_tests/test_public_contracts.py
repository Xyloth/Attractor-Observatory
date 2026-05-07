from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from control_room.snapshot import bind_snapshot_freshness  # noqa: E402
from factory_lowlevel.adapters import PubChemSmallMoleculeAdapter  # noqa: E402


def _load_json(path: str | Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8-sig"))


def _sha256_bytes(path: str | Path) -> str:
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def _walk(node):
    if isinstance(node, dict):
        yield node
        for value in node.values():
            yield from _walk(value)
    elif isinstance(node, list):
        for item in node:
            yield from _walk(item)


def test_spec_lineage_hashes_match_raw_bytes():
    lineage = _load_json("spec/lineage.json")
    for row in lineage["entries"] + lineage["supporting_context"]:
        assert row["sha256"] == _sha256_bytes(row["source_path"])
        assert row["byte_size"] == len((ROOT / row["source_path"]).read_bytes())

    signature = lineage["signatures"][0]
    digest = hashlib.sha256(signature["signature_input"].encode("utf-8")).hexdigest()
    assert signature["signature_hash"] == digest
    assert signature["signature_id"] in {"task-032-builder-self-attestation", "task-dx-002-builder-self-attestation"}


def test_doctrine_registry_covers_all_binding_and_candidate_doctrines():
    registry = _load_json("docs/doctrine_registry.json")
    rows = registry["doctrines"]
    ids = {row["id"] for row in rows}
    expected = {f"D{i}" for i in range(7, 32)} | {"D17.5"}
    assert expected <= ids

    for row in rows:
        assert row["content_hash"] == "sha256:" + _sha256_bytes(row["path"])

    ratified = {row["id"]: row for row in rows if row.get("status") == "ratified"}
    assert {"D23", "D24", "D25", "D26", "D27", "D28", "D29", "D30", "D31"} <= set(ratified)
    assert all(ratified[did]["mode"] == "foundational" for did in ("D23", "D24", "D25", "D26", "D27", "D28", "D29", "D30", "D31"))


def test_telemetry_records_have_identity_and_one_active_estimate_per_task():
    rows = [
        json.loads(line)
        for line in (ROOT / "project_telemetry/ai_builder_tasks.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    task_record_ids = [row.get("task_record_id") for row in rows]
    assert all(task_record_ids)
    assert len(task_record_ids) == len(set(task_record_ids))

    active_estimates = defaultdict(int)
    for row in rows:
        assert row.get("task_id")
        assert row.get("record_type")
        if row["record_type"] in {"estimate", "actual_update"}:
            assert row.get("model_name")
        if row["record_type"] == "estimate":
            active_estimates[row["task_id"]] += 1
    assert all(count == 1 for count in active_estimates.values())


def test_pubchem_parser_accepts_live_schema_aliases():
    adapter = PubChemSmallMoleculeAdapter()
    source = adapter.source_definition()
    row = {
        "CID": 222,
        "MolecularFormula": "H3N",
        "MolecularWeight": "17.031",
        "SMILES": "N",
        "ConnectivitySMILES": "N",
        "Complexity": 0,
        "HeavyAtomCount": 1,
    }
    record = adapter._record_from_row(row, source)
    assert record.payload["canonical_smiles"] == "N"
    assert record.payload["heavy_atom_count"] == 1
    assert record.payload["bond_topology_proxy"]["element_token_count"] == 1


def test_campaign019_is_live_ready_after_red_gate_repairs():
    report = _load_json("reports/campaign_019/full_report.json")
    status = report["hardening_gate_status"]
    assert report["status"] == "green"
    assert report["live_ready"] is True
    assert status["gate_count"] == 59
    assert status["red_count"] == 0
    assert status["green_count"] == 59


def test_snapshot_has_d24_generation_binding_and_staleness_detection():
    snapshot = _load_json("control_room/snapshots/state_latest.json")
    binding = snapshot["generation_binding"]
    for key in ("branch", "commit_sha", "generation_command", "generation_timestamp", "freshness_status"):
        assert key in binding
    assert snapshot.get("freshness_status_advisory_only") is True or snapshot.get("freshness_status") in {"current", binding.get("freshness_status")}

    stale = json.loads(json.dumps(snapshot))
    stale["generation_binding"]["commit_sha"] = "sha256:not-current"
    checked = bind_snapshot_freshness(stale, repo_dir=ROOT)
    assert checked["freshness_status"].startswith("stale:")
    assert checked["generation_binding"]["freshness_checked_at"]
    assert snapshot["evidence_boundaries"]["evidence_private_count"] >= 1344


def test_private_trace_evidence_is_marked_at_point_of_use():
    marker_summary = _load_json("reports/task_032_evidence_private_markers.json")
    assert marker_summary["current_marker_count"] >= 1344

    missing_markers = []
    for path in list((ROOT / "reports").rglob("*.json")) + list((ROOT / "papers/prereg").rglob("*.json")):
        if path.name == "task_032_evidence_private_markers.json":
            continue
        try:
            payload = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            continue
        for row in _walk(payload):
            trace_paths = [value for key, value in row.items() if "trace_path" in key.lower()]
            if not trace_paths:
                continue
            statuses = [value for key, value in row.items() if key.lower().endswith("trace_path_status")]
            if "private_unshipped" in statuses:
                if row.get("evidence_private") is not True:
                    missing_markers.append(path)
    assert not missing_markers


def test_public_docs_do_not_point_at_missing_portfolio_pngs():
    docs = [ROOT / "README.md", ROOT / "Control_Room_README.md"]
    references = Counter()
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        for token in ("control_room/portfolio/", "tests/test_control_room_"):
            references[token] += text.count(token)
    assert references["control_room/portfolio/"] <= 1
    assert references["tests/test_control_room_"] == 0
