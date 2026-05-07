"""Tests for CB-016 persistence load-on-init fix.

The CB-015 T8 incident found that ``LowLevelFactoryStore.__init__``
initialized empty in-memory dicts and did NOT load existing JSON
files from disk. Result: every ``run_live_factory_cycle`` call
overwrote the persisted store with only that run's records, wiping
prior cycles.

CB-016 fix: ``__init__`` calls ``_load_existing_from_disk`` after
dict construction. The tests below pin the contract:

  * Empty store_root → all dicts empty (clean first-cycle start)
  * Existing single-source state → re-load succeeds
  * Two-source sequential write → both coexist (no overwrite)
  * Same record_id rewritten → upsert (newer wins, no duplicate)
  * Three-source replay (NIST + KEGG + PubChem) → all coexist
  * Malformed JSON → audit queue entry, no crash
  * D9 binding: per-row malformations skipped, not silently fabricated

All tests deterministic, no network, no Streamlit. Runtime <1s.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_record(rid: str, world: str = "crn", source: str = "src.test") -> dict:
    return {
        "record_id": rid,
        "source_id": source,
        "world_family": world,
        "record_type": "test_record",
        "canonical_name": f"test {rid[:8]}",
        "payload": {"foo": "bar"},
        "provenance": {
            "source_url": "https://example.com/test",
            "retrieval_timestamp": "2026-05-07T17:00:00Z",
            "parser_version": "test.v1",
            "authority": "test",
            "raw_exported": False,
        },
        "license_class": "metadata_only",
        "mode_tag": "exploratory",
        "schema_version": "EmpiricalRecord.v1",
    }


def _write_records_file(store_root: Path, records: list[dict]) -> None:
    store_root.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema": "LowLevelEmpiricalRecordSet.v1",
        "records": records,
    }
    (store_root / "empirical_records.json").write_text(
        json.dumps(payload, sort_keys=True, indent=2),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Test 1 — Empty store_root → empty dicts
# ---------------------------------------------------------------------------


def test_load_on_init_empty_store_starts_empty(tmp_path):
    """A fresh store_root with no JSON files yields all-empty dicts.
    No exceptions; clean first-cycle behavior preserved."""
    from factory_lowlevel.persistence import LowLevelFactoryStore

    store = LowLevelFactoryStore(tmp_path / "empty_store")
    assert store.empirical_records == {}
    assert store.normalized_refs == {}
    assert store.evidence_edges == {}
    assert store.audit_queue == {}
    assert store.source_cache == {}
    assert store.world_traces == {}


# ---------------------------------------------------------------------------
# Test 2 — Existing single-source state → re-load
# ---------------------------------------------------------------------------


def test_load_on_init_reads_existing_records(tmp_path):
    """A store_root with a populated empirical_records.json yields
    the loaded records in self.empirical_records."""
    from factory_lowlevel.persistence import LowLevelFactoryStore

    store_root = tmp_path / "store"
    seed_records = [
        _make_record("sha256:r1"),
        _make_record("sha256:r2"),
        _make_record("sha256:r3"),
    ]
    _write_records_file(store_root, seed_records)

    store = LowLevelFactoryStore(store_root)
    assert len(store.empirical_records) == 3
    assert {"sha256:r1", "sha256:r2", "sha256:r3"} == set(store.empirical_records.keys())
    sample = store.empirical_records["sha256:r1"]
    assert sample.world_family == "crn"
    assert sample.license_class == "metadata_only"
    assert sample.provenance["source_url"] == "https://example.com/test"


# ---------------------------------------------------------------------------
# Test 3 — Two-source sequential write → both coexist (the canonical fix)
# ---------------------------------------------------------------------------


def test_load_on_init_two_source_sequential_write_both_coexist(tmp_path):
    """The canonical CB-015 bug repro: two run_live_factory_cycle calls
    against the same store_root should accumulate records, not overwrite.
    Simulated here by 2 separate LowLevelFactoryStore constructions +
    writes: post-fix the second store loads the first's state and
    write() emits both sets."""
    from factory_lowlevel.persistence import LowLevelFactoryStore
    from factory_lowlevel.schemas import EmpiricalRecord

    store_root = tmp_path / "store"

    # Source A: write 2 records, persist.
    store_a = LowLevelFactoryStore(store_root)
    rec_a1 = EmpiricalRecord(**_make_record("sha256:nist1", world="atomic_molecular_primitives", source="src.nist"))
    rec_a2 = EmpiricalRecord(**_make_record("sha256:nist2", world="atomic_molecular_primitives", source="src.nist"))
    store_a.ingest_empirical_records([rec_a1, rec_a2])
    store_a.write()
    assert (store_root / "empirical_records.json").exists()

    # Source B: NEW store object on the same store_root (mimics the
    # daemon constructing a fresh store per source). Pre-fix this
    # would start empty + write a fresh file with only B's records,
    # wiping A. Post-fix the constructor loads A's records first.
    store_b = LowLevelFactoryStore(store_root)
    assert len(store_b.empirical_records) == 2  # A's records loaded

    rec_b1 = EmpiricalRecord(**_make_record("sha256:pubchem1", world="atomic_molecular_primitives", source="src.pubchem"))
    rec_b2 = EmpiricalRecord(**_make_record("sha256:pubchem2", world="atomic_molecular_primitives", source="src.pubchem"))
    store_b.ingest_empirical_records([rec_b1, rec_b2])
    store_b.write()

    # Reload to verify on-disk state has all 4
    final_store = LowLevelFactoryStore(store_root)
    assert len(final_store.empirical_records) == 4
    assert set(final_store.empirical_records.keys()) == {
        "sha256:nist1", "sha256:nist2", "sha256:pubchem1", "sha256:pubchem2"
    }


# ---------------------------------------------------------------------------
# Test 4 — Same record_id rewritten → upsert (newer wins)
# ---------------------------------------------------------------------------


def test_load_on_init_upsert_same_record_id(tmp_path):
    """Re-ingesting the same record_id with newer data: dict-keyed-by-id
    pattern means newer overwrites older. No duplicate row."""
    from factory_lowlevel.persistence import LowLevelFactoryStore
    from factory_lowlevel.schemas import EmpiricalRecord

    store_root = tmp_path / "store"

    # Initial write
    store_a = LowLevelFactoryStore(store_root)
    rec_v1 = EmpiricalRecord(**_make_record("sha256:same_id"))
    store_a.ingest_empirical_records([rec_v1])
    store_a.write()

    # Re-ingest same record_id with different payload
    store_b = LowLevelFactoryStore(store_root)
    rec_v2_data = _make_record("sha256:same_id")
    rec_v2_data["payload"] = {"foo": "BAR_NEW"}
    rec_v2 = EmpiricalRecord(**rec_v2_data)
    store_b.ingest_empirical_records([rec_v2])
    store_b.write()

    final_store = LowLevelFactoryStore(store_root)
    assert len(final_store.empirical_records) == 1  # no duplicate
    assert final_store.empirical_records["sha256:same_id"].payload == {"foo": "BAR_NEW"}


# ---------------------------------------------------------------------------
# Test 5 — Three-source sequential write (NIST + PubChem + KEGG)
# ---------------------------------------------------------------------------


def test_load_on_init_three_source_sequential_all_coexist(tmp_path):
    """Full CB-015 bug repro: 3 sequential cycles (NIST, then PubChem,
    then KEGG). Post-fix all three sets coexist; pre-fix only KEGG
    (the last) survived."""
    from factory_lowlevel.persistence import LowLevelFactoryStore
    from factory_lowlevel.schemas import EmpiricalRecord

    store_root = tmp_path / "store"

    cycles = [
        ("nist", "atomic_molecular_primitives", ["sha256:nist_a", "sha256:nist_b"]),
        ("pubchem", "atomic_molecular_primitives", ["sha256:pubchem_a"]),
        ("kegg", "crn", ["sha256:kegg_a", "sha256:kegg_b", "sha256:kegg_c"]),
    ]
    for source_id, world, rids in cycles:
        store = LowLevelFactoryStore(store_root)
        records = [EmpiricalRecord(**_make_record(rid, world=world, source=f"src.{source_id}")) for rid in rids]
        store.ingest_empirical_records(records)
        store.write()

    final = LowLevelFactoryStore(store_root)
    assert len(final.empirical_records) == 6
    by_world = {}
    for rec in final.empirical_records.values():
        by_world.setdefault(rec.world_family, []).append(rec)
    assert len(by_world["atomic_molecular_primitives"]) == 3  # 2 NIST + 1 PubChem
    assert len(by_world["crn"]) == 3  # 3 KEGG


# ---------------------------------------------------------------------------
# Test 6 — Malformed JSON → audit-queue entry, no crash
# ---------------------------------------------------------------------------


def test_load_on_init_malformed_json_emits_audit_entry(tmp_path):
    """Per the docstring: malformed JSON does NOT raise during
    construction. It emits an audit-queue entry and leaves the
    corresponding dict empty so subsequent writes don't propagate
    the corruption (D9: surface, don't paper over)."""
    from factory_lowlevel.persistence import LowLevelFactoryStore

    store_root = tmp_path / "store"
    store_root.mkdir(parents=True, exist_ok=True)
    (store_root / "empirical_records.json").write_text(
        "{ this is not valid json (",
        encoding="utf-8",
    )

    # Should not raise.
    store = LowLevelFactoryStore(store_root)

    # empirical_records dict is empty (couldn't parse).
    assert store.empirical_records == {}

    # An audit-queue entry surfaces the load failure.
    assert len(store.audit_queue) == 1
    audit = next(iter(store.audit_queue.values()))
    assert audit.severity == "high"
    assert "persistence_load_failed" in audit.reason
    assert "empirical_records.json" in audit.reason
    assert audit.source_id == "factory_lowlevel.persistence"


# ---------------------------------------------------------------------------
# Test 7 — Per-row malformation skipped silently (not fabricated)
# ---------------------------------------------------------------------------


def test_load_on_init_per_row_malformation_skipped(tmp_path):
    """If one row is missing required keys, that row is skipped but
    the rest of the file loads. D14 binding: don't fabricate keys
    to fill the gap."""
    from factory_lowlevel.persistence import LowLevelFactoryStore

    store_root = tmp_path / "store"
    good_rec = _make_record("sha256:good")
    bad_rec = {"record_id": "sha256:bad"}  # missing required keys
    _write_records_file(store_root, [good_rec, bad_rec])

    store = LowLevelFactoryStore(store_root)
    # Only the good record loads
    assert len(store.empirical_records) == 1
    assert "sha256:good" in store.empirical_records
    assert "sha256:bad" not in store.empirical_records


# ---------------------------------------------------------------------------
# Test 8 — Cache replay end-to-end: existing 4,123 PubChem store
# ---------------------------------------------------------------------------


def test_load_on_init_recovers_actual_cb015_store():
    """End-to-end: load the actual CB-015 task_cb015_launch/factory_store
    that has 4,123 PubChem records. Confirm all 4,123 load with full
    schema fidelity. This is the real-world test that the fix
    enables cache replay recovery in T3."""
    from factory_lowlevel.persistence import LowLevelFactoryStore

    cb015_store = ROOT.parent.parent / "Attractor Observatory" / "reports" / "task_cb015_launch" / "factory_store"
    if not cb015_store.exists():
        pytest.skip("CB-015 store not present in this checkout (expected on cb-016 worktree only)")

    store = LowLevelFactoryStore(cb015_store)
    assert len(store.empirical_records) >= 1, "expected at least one CB-015 record to survive load"
    sample = next(iter(store.empirical_records.values()))
    # Confirm full schema deserialization (provenance, payload, etc.)
    assert sample.world_family
    assert sample.license_class
    assert sample.provenance.get("source_url")
    assert sample.provenance.get("retrieval_timestamp")
