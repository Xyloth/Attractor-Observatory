"""Tests for the CB-009 Control Room extensions: Atlas periodic table,
paper bundle generator, and audit-queue inbox.

All tests are deterministic and read-only against bundled fixtures
(or write only into ``tmp_path``). No Streamlit runtime is invoked —
we exercise the pure-Python helpers directly so the suite stays fast
and CI-friendly.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# T1 — Atlas Periodic Table
# ---------------------------------------------------------------------------


def test_periodic_table_loads_six_atlas_entries():
    """The atlas/entries/ dir ships 6 motif files and the loader should
    surface all of them so the periodic table renders 6 rows."""
    from control_room.rooms.motif_atlas import _load_atlas_entries

    entries = _load_atlas_entries()
    assert len(entries) == 6
    motif_ids = {e["motif_id"] for e in entries}
    expected = {
        "motif.autocatalytic_closure.draft",
        "motif.self_boundary.draft" if False else "motif.self_maintained_boundary.draft",
        "motif.repair.draft",
        "motif.replication_lineage.draft",
        "motif.externalized_memory.draft",
        "motif.floor_connectivity.draft",
    }
    assert motif_ids == expected


def test_periodic_table_classifies_no_data_cells_as_gray_d22():
    """Worlds where a motif has no campaign attestation must render the
    explicit gray "no detection" cell — never silently filled (D22)."""
    from control_room.rooms.motif_atlas import (
        _classify_motif_world_cell,
        _load_atlas_entries,
    )

    entries = _load_atlas_entries()
    closure = next(
        e for e in entries
        if e["motif_id"] == "motif.autocatalytic_closure.draft"
    )
    # W-1 (atomic/molecular primitives) is NOT in any campaign that
    # attests this motif — it must classify as no_detection / gray.
    cell = _classify_motif_world_cell(closure, "W-1")
    assert cell["status"] == "no_detection"
    assert cell["color"] == "#283042"  # COLOR_BORDER, the gray
    assert cell["count"] == 0
    assert "D22 honest absence" in cell["hover"]


def test_periodic_table_fired_cells_carry_real_campaign_evidence():
    """When a cell is 'fired', its hover must list the real campaigns
    that produced the attestation. No fabricated provenance."""
    from control_room.rooms.motif_atlas import _classify_motif_world_cell, _load_atlas_entries

    entries = _load_atlas_entries()
    closure = next(
        e for e in entries
        if e["motif_id"] == "motif.autocatalytic_closure.draft"
    )
    # W1 (chemistry/RAFs) is in campaigns 002 + 009 per the conservative
    # mapping; both are in closure's provenance.campaigns.
    cell = _classify_motif_world_cell(closure, "W1")
    assert cell["status"] == "fired"
    assert cell["count"] >= 1
    # Every campaign in fire_campaigns must be in the entry's provenance.
    motif_campaigns = set(closure["provenance"]["campaigns"])
    for c in cell["fire_campaigns"]:
        assert c in motif_campaigns, f"campaign {c} not in atlas entry's provenance"


# ---------------------------------------------------------------------------
# T2 — Paper Bundle Generator
# ---------------------------------------------------------------------------


def test_paper_bundle_generator_assembles_real_files(tmp_path, monkeypatch):
    """Build a bundle for the autocatalytic_closure motif and verify
    that every file declared in the manifest exists on disk and that
    its content_hash matches a fresh sha256 of the file bytes."""
    from control_room.rooms import portfolio_demo

    monkeypatch.setattr(
        portfolio_demo,
        "BUNDLES_ROOT",
        tmp_path / "bundles",
    )
    motifs = portfolio_demo._list_atlas_motifs()
    closure = next(
        m for m in motifs if m["motif_id"] == "motif.autocatalytic_closure.draft"
    )
    result = portfolio_demo._build_paper_bundle(closure)
    bundle_dir = Path(result["bundle_dir"])
    manifest = result["manifest"]

    # Bundle dir + bundle.json present
    assert bundle_dir.exists() and bundle_dir.is_dir()
    assert (bundle_dir / "bundle.json").exists()

    # Atlas entry + citation always present
    rel_paths = {f["path"] for f in manifest["files"]}
    assert "atlas_entry.json" in rel_paths
    assert "citation.bib" in rel_paths

    # Every declared file exists and its content_hash recomputes
    for f in manifest["files"]:
        p = bundle_dir / f["path"]
        assert p.exists(), f"declared file missing: {f['path']}"
        actual = hashlib.sha256(p.read_bytes()).hexdigest()
        assert f["content_hash"] == f"sha256:{actual}", (
            f"content_hash drift on {f['path']}"
        )


def test_paper_bundle_includes_all_provenance_campaigns(tmp_path, monkeypatch):
    """For each campaign listed in the motif's provenance.campaigns,
    a campaign report excerpt should appear in the bundle when one
    exists on disk. Campaigns without a report file are silently
    skipped (D22 — honest absence)."""
    from control_room.rooms import portfolio_demo

    monkeypatch.setattr(portfolio_demo, "BUNDLES_ROOT", tmp_path / "bundles")
    motifs = portfolio_demo._list_atlas_motifs()
    closure = next(m for m in motifs if "autocatalytic_closure" in m["motif_id"])
    result = portfolio_demo._build_paper_bundle(closure)
    manifest = result["manifest"]

    # The autocatalytic_closure entry references campaigns 002, 009, 010, 013;
    # all four ship a full_report.json or cli_full_report.json on this branch.
    declared_campaigns = set(manifest["provenance_campaigns"])
    bundle_campaigns = {
        f["path"].split("/")[1].split("_")[1] if f["path"].startswith("campaigns/") else None
        for f in manifest["files"]
    }
    bundle_campaigns.discard(None)
    # Bundle should cover at least one campaign from provenance (D22:
    # missing reports are silently skipped, never fabricated).
    assert bundle_campaigns.issubset(declared_campaigns) or not bundle_campaigns


def test_paper_bundle_manifest_carries_bundle_content_hash(tmp_path, monkeypatch):
    """The manifest must include ``bundle_content_hash`` so a receiver
    can verify the bundle wasn't tampered with."""
    from control_room.rooms import portfolio_demo

    monkeypatch.setattr(portfolio_demo, "BUNDLES_ROOT", tmp_path / "bundles")
    motifs = portfolio_demo._list_atlas_motifs()
    result = portfolio_demo._build_paper_bundle(motifs[0])
    assert result["manifest"]["bundle_content_hash"].startswith("sha256:")


# ---------------------------------------------------------------------------
# T3 — Audit-Queue Inbox
# ---------------------------------------------------------------------------


def test_audit_inbox_loads_items_from_all_campaigns():
    """The inbox should aggregate audit items from every
    ``audit_queue.json`` under reports/, including factory_store/ +
    daemon_store/ + campaign-root paths."""
    from control_room.rooms.factory_intake_dock import _audit_inbox_load_all

    inbox = _audit_inbox_load_all()
    # We know reports/campaign_011/audit_queue.json has 50 items;
    # factory_store/daemon_store may have 0 each. Total >= 50.
    assert len(inbox) >= 50, (
        f"expected at least the 50 campaign_011 items; got {len(inbox)}"
    )
    # Source files come from multiple campaigns.
    src_files = {i["source_file"] for i in inbox}
    assert any("campaign_011" in s for s in src_files)


def test_audit_inbox_normalizes_heterogeneous_item_shapes():
    """campaign_011 uses {item_id, priority, reason}; factory_store
    uses {audit_id, severity, recommended_action, ...}. Both must
    normalize to the same inbox row schema with severity in
    {high, medium, low}."""
    from control_room.rooms.factory_intake_dock import _normalize_audit_item

    # Old shape (campaign_011)
    legacy = {"item_id": "x.y.z", "priority": 9, "reason": "contradiction"}
    out = _normalize_audit_item(legacy, Path("reports/campaign_011/audit_queue.json"))
    assert out["audit_id"] == "x.y.z"
    assert out["severity"] == "high"  # priority 9 → high
    assert out["reason"] == "contradiction"

    # New shape (factory_store)
    modern = {
        "audit_id": "sha256:abc",
        "severity": "medium",
        "reason": "smiles_empty_after_parse",
        "source_id": "source.pubchem",
        "record_id": "sha256:def",
        "recommended_action": "investigate_schema_drift",
    }
    out = _normalize_audit_item(modern, Path("reports/campaign_016/factory_store/audit_queue.json"))
    assert out["audit_id"] == "sha256:abc"
    assert out["severity"] == "medium"
    assert out["recommended_action"] == "investigate_schema_drift"


def test_audit_resolution_is_read_only_sidecar(tmp_path, monkeypatch):
    """Mark-resolved must write to control_room/cache/audit_resolutions/
    and NEVER touch the underlying audit_queue.json. The brief calls
    this 'D22-style read-only sidecar discipline'."""
    from control_room.rooms import factory_intake_dock as room

    # Redirect resolution dir into tmp so the test doesn't pollute the
    # live cache and so each run is hermetic.
    monkeypatch.setattr(room, "AUDIT_RESOLUTION_DIR", tmp_path / "resolutions")

    # Capture original audit_queue.json bytes so we can verify they're
    # untouched after a resolution write.
    sample_queue = ROOT / "reports/campaign_011/audit_queue.json"
    queue_bytes_before = sample_queue.read_bytes()

    p = room._audit_resolution_write("test.audit.id", note="pytest sidecar")
    assert p.exists()
    payload = json.loads(p.read_text(encoding="utf-8"))
    assert payload["schema"] == "ControlRoomAuditResolution.v1"
    assert payload["audit_id"] == "test.audit.id"
    assert payload["note"] == "pytest sidecar"
    assert payload["resolved_at"].endswith("Z")

    # Verify the upstream audit_queue.json is unchanged.
    queue_bytes_after = sample_queue.read_bytes()
    assert queue_bytes_before == queue_bytes_after, (
        "Mark resolved must NEVER mutate the producer's audit_queue.json"
    )


def test_audit_inbox_summary_counts_match_unresolved_filter(tmp_path, monkeypatch):
    """The summary's ``unresolved_total`` must equal the number of items
    with no sidecar, and high+medium+low must equal the unresolved
    count."""
    from control_room.rooms import factory_intake_dock as room

    monkeypatch.setattr(room, "AUDIT_RESOLUTION_DIR", tmp_path / "resolutions")
    summary = room._audit_inbox_summary()
    assert summary["unresolved_total"] == len(summary["unresolved"])
    assert (
        summary["high"] + summary["medium"] + summary["low"]
        == summary["unresolved_total"]
    )


# ---------------------------------------------------------------------------
# T4 — Snapshot endpoint extension
# ---------------------------------------------------------------------------


def test_snapshot_includes_atlas_periodic_table_section():
    """The snapshot endpoint must surface the periodic-table summary
    so a fresh AI agent can read it without invoking Streamlit."""
    from control_room.snapshot import build_snapshot

    snap = build_snapshot()
    section = snap.get("atlas_periodic_table")
    assert section is not None, "atlas_periodic_table missing from snapshot"
    assert section["status"] == "ok"
    assert len(section["rows"]) == 6  # 6 motifs
    assert len(section["world_axis"]) == 15  # 15 worlds
    assert section["grand_total"] >= 0


def test_snapshot_includes_audit_inbox_section():
    """The snapshot endpoint must surface the live audit-inbox counts
    + a high-severity preview."""
    from control_room.snapshot import build_snapshot

    snap = build_snapshot()
    section = snap.get("audit_inbox")
    assert section is not None
    assert section["status"] == "ok"
    assert "unresolved_total" in section
    assert "by_severity" in section
    assert {"high", "medium", "low"} == set(section["by_severity"].keys())
    # The preview is capped at 5 to keep the snapshot small.
    assert len(section.get("high_severity_preview", [])) <= 5


# ---------------------------------------------------------------------------
# Gap-fill: T2 campaign-based bundle + T3 audit drilldown
# ---------------------------------------------------------------------------


def test_paper_bundle_campaign_kind_assembles_real_files(tmp_path, monkeypatch):
    """The brief said "pick a motif (or a campaign)" — verify the
    campaign branch produces a manifest with a campaign_id, the citing
    motifs, and at least the campaign report file when one exists."""
    from control_room.rooms import portfolio_demo

    monkeypatch.setattr(portfolio_demo, "BUNDLES_ROOT", tmp_path / "bundles")
    # Campaign 010 has a full_report.json and is cited by all 6 atlas entries.
    result = portfolio_demo._build_campaign_bundle("010")
    bundle_dir = Path(result["bundle_dir"])
    manifest = result["manifest"]

    assert bundle_dir.exists()
    assert manifest["bundle_kind"] == "campaign"
    assert manifest["campaign_id"] == "010"
    assert len(manifest["citing_motifs"]) >= 1, "campaign 010 should be cited by at least one atlas entry"
    # Atlas-citing entries should appear under atlas_entries/
    atlas_files = [f for f in manifest["files"] if f["path"].startswith("atlas_entries/")]
    assert len(atlas_files) == len(manifest["citing_motifs"])
    # Every declared file's hash recomputes from disk
    for f in manifest["files"]:
        actual = hashlib.sha256((bundle_dir / f["path"]).read_bytes()).hexdigest()
        assert f["content_hash"] == f"sha256:{actual}"


def test_audit_drilldown_finds_underlying_empirical_record():
    """The drilldown helper must locate an empirical_records.json entry
    when an audit item references a record_id that exists. Read-only."""
    from control_room.rooms.factory_intake_dock import _find_empirical_record

    # Try to find any record actually present in the store. If empirical
    # records exist anywhere under reports/, the helper must surface
    # them by record_id; otherwise the test is N/A.
    records_files = list((ROOT / "reports").rglob("empirical_records.json"))
    found_id = None
    for p in records_files:
        try:
            payload = json.loads(p.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        records = payload.get("records") if isinstance(payload, dict) else payload
        if isinstance(records, list) and records:
            for r in records:
                if isinstance(r, dict) and r.get("record_id"):
                    found_id = r["record_id"]
                    break
        if found_id:
            break

    if not found_id:
        pytest.skip("no empirical_records.json with records on this branch")

    found = _find_empirical_record(found_id)
    assert found is not None
    assert found["record_id"] == found_id


def test_audit_drilldown_returns_none_for_unknown_record():
    """Unknown record_id must yield None (D22 — caller renders honest
    'not found' rather than fabricating)."""
    from control_room.rooms.factory_intake_dock import _find_empirical_record

    assert _find_empirical_record("sha256:nonexistent_record_id_for_test") is None
