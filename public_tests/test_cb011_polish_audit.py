"""Tests for CB-011 polish + audit fixes.

Covers:
  * Issue 4 — W-1 records adapter scans ALL stores under reports/
  * Issue 1 — BUILD_LOG parser produces structured entries (no docstring leak)
  * Issue 2 — pytest cache stale_cache flag fires when mtime is old
  * Issue 5 — other-world drilldown loader returns records for non-W-1 worlds
  * Issue 7 — FIRE button confirmation marker is well-formed
  * Issue 9 — bulk-resolve bucket computation classifies known patterns
  * Issue 8/10 — cached_adapters wrappers exist and call through

All tests deterministic, no Streamlit runtime, no network.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# Issue 4 — W-1 records adapter
# ---------------------------------------------------------------------------


def test_w1_records_aggregator_scans_multiple_stores(tmp_path, monkeypatch):
    """Records persisted under multiple ``reports/**/factory_store/`` and
    ``daemon_store/`` and ``final_store/`` paths must all surface for
    the same world_family. De-duplicated on record_id."""
    from control_room.rooms import _world_drilldown

    # Lay down two stores under tmp_path; both contain W-1 records,
    # one of which overlaps to test de-dup.
    s1 = tmp_path / "reports/campaign_test1/factory_store"
    s2 = tmp_path / "reports/task_other/final_store"
    s1.mkdir(parents=True)
    s2.mkdir(parents=True)
    s1_records = [
        {"record_id": "sha256:a", "world_family": "atomic_molecular_primitives"},
        {"record_id": "sha256:b", "world_family": "atomic_molecular_primitives"},
        {"record_id": "sha256:other", "world_family": "math_primitives"},
    ]
    s2_records = [
        {"record_id": "sha256:b", "world_family": "atomic_molecular_primitives"},  # dupe
        {"record_id": "sha256:c", "world_family": "atomic_molecular_primitives"},
    ]
    (s1 / "empirical_records.json").write_text(
        json.dumps({"records": s1_records}), encoding="utf-8"
    )
    (s2 / "empirical_records.json").write_text(
        json.dumps({"records": s2_records}), encoding="utf-8"
    )

    monkeypatch.setattr(_world_drilldown, "REPO_ROOT", tmp_path)
    out = _world_drilldown.load_records_for_world("atomic_molecular_primitives")
    rids = {r["record_id"] for r in out}
    assert rids == {"sha256:a", "sha256:b", "sha256:c"}


def test_w1_records_aggregator_returns_empty_for_unknown_world():
    """D22 honest absence: world with no records returns []."""
    from control_room.rooms._world_drilldown import load_records_for_world

    out = load_records_for_world("nonexistent_world_xyz")
    assert out == []


# ---------------------------------------------------------------------------
# Issue 1 — BUILD_LOG parser robustness
# ---------------------------------------------------------------------------


def test_build_log_parses_to_structured_entries():
    """BUILD_LOG.md must parse into structured entries with date +
    header + body fields — never returning the raw preamble in
    rationale (which was the docstring-leak failure mode)."""
    from control_room.adapters.build_log import parse_build_log

    r = parse_build_log()
    assert r["status"] == "ok"
    entries = r["data"]["entries"]
    assert len(entries) > 0
    for entry in entries:
        assert entry.get("date"), "every entry must carry a date"
        assert entry.get("header"), "every entry must carry a header"
        assert entry.get("kind") in {"work", "talk", "audit", "architect", "other"}


def test_build_log_handles_missing_file_gracefully(tmp_path):
    """Missing file → status=missing with rationale, no exception."""
    from control_room.adapters.build_log import parse_build_log

    r = parse_build_log(path=tmp_path / "nonexistent.md")
    assert r["status"] == "missing"
    assert "not found" in r["rationale"]


# ---------------------------------------------------------------------------
# Issue 2 — pytest stale_cache flag
# ---------------------------------------------------------------------------


def test_pytest_stale_cache_flag_fires_when_mtime_old(tmp_path):
    """A cache file older than ``stale_threshold_seconds`` triggers
    ``stale_cache: True`` in the adapter output (D17 binding)."""
    import os
    from control_room.adapters.pytest_cache import parse_pytest_cache

    cache = tmp_path / ".pytest_cache" / "v" / "cache"
    cache.mkdir(parents=True)
    lf = cache / "lastfailed"
    lf.write_text(json.dumps({"tests/test_x.py::test_y": True, "tests/test_x.py::test_z": True}), encoding="utf-8")
    # Stamp the file 7 hours ago — past the 6-hour default threshold
    old = time.time() - (7 * 3600)
    os.utime(lf, (old, old))

    r = parse_pytest_cache(cache_dir=tmp_path / ".pytest_cache")
    assert r["status"] == "ok"
    assert r["data"]["last_failed_count"] == 2
    assert r["data"]["stale_cache"] is True
    assert r["data"]["lastfailed_age_seconds"] > 6 * 3600
    assert "STALE" in r["rationale"]


def test_pytest_stale_cache_flag_does_not_fire_when_fresh(tmp_path):
    """Fresh cache: stale_cache=False so consumers display as live state."""
    from control_room.adapters.pytest_cache import parse_pytest_cache

    cache = tmp_path / ".pytest_cache" / "v" / "cache"
    cache.mkdir(parents=True)
    (cache / "lastfailed").write_text(json.dumps({"tests/test_x.py::test_y": True}), encoding="utf-8")

    r = parse_pytest_cache(cache_dir=tmp_path / ".pytest_cache")
    assert r["status"] == "ok"
    assert r["data"]["stale_cache"] is False


# ---------------------------------------------------------------------------
# Issue 5 — other-world drilldown
# ---------------------------------------------------------------------------


def test_other_world_drilldown_loader_returns_records_when_present():
    """Non-W-1 simulation worlds (origins_chemistry, crn, etc.) should
    surface their persisted records via the same aggregator. Verified
    on the live store: at least one record exists per active world."""
    from control_room.rooms._world_drilldown import load_records_for_world

    am = load_records_for_world("atomic_molecular_primitives")
    assert len(am) > 100, f"expected many W-1 records; got {len(am)}"
    mp = load_records_for_world("math_primitives")
    assert len(mp) > 0


# ---------------------------------------------------------------------------
# Issue 7 — FIRE button confirmation
# ---------------------------------------------------------------------------


def test_fire_button_confirmation_marker_well_formed():
    """The marker must conform to FireButtonConfirmation.v1 schema with
    confirmed_working_at, results, and what_works fields."""
    p = ROOT / "control_room/cache/fire_button_confirmed.json"
    assert p.exists(), "fire_button_confirmed.json should exist after CB-011 self-test"
    payload = json.loads(p.read_text(encoding="utf-8"))
    assert payload["schema"] == "FireButtonConfirmation.v1"
    assert payload["confirmed_working_at"]
    assert payload["confirmed_by"]
    assert payload["results"]["life_form_count"] >= 1
    assert payload["results"]["latest_run_json_committed"] is True
    assert isinstance(payload["what_works"], list) and len(payload["what_works"]) > 0


# ---------------------------------------------------------------------------
# Issue 9 — bulk-resolve buckets
# ---------------------------------------------------------------------------


def test_bulk_resolve_buckets_classify_known_patterns():
    """The five recognized patterns (NIST source-limited, planted-false-
    claim fixtures, contradictory polarity fixtures, stale_cache,
    general fixture) must each catch only items they apply to."""
    from control_room.rooms.factory_intake_dock import _compute_bulk_resolve_buckets

    items = [
        {"audit_id": "1", "reason": "nist_asd_no_energy_level_rows"},
        {"audit_id": "2", "reason": "nist_asd_no_energy_level_rows"},
        {"audit_id": "3", "reason": "planted false claim rejected by trace predicate"},
        {"audit_id": "4", "reason": "contradictory source-bound polarity"},
        {"audit_id": "5", "reason": "stale_cache:73966970s"},
        {"audit_id": "6", "reason": "real_unrecognized_thing"},  # NOT bucketed
    ]
    buckets = _compute_bulk_resolve_buckets(items)
    assert buckets["nist_source_limited"]["count"] == 2
    assert buckets["fixture_planted_false_claim"]["count"] == 1
    assert buckets["fixture_contradictory_polarity"]["count"] == 1
    assert buckets["stale_cache_artifact"]["count"] == 1
    # The unrecognized item lands in NO bucket.
    total_bucketed = sum(b["count"] for b in buckets.values())
    assert total_bucketed == 5


def test_bulk_resolve_first_match_wins_no_double_counting():
    """An item must land in AT MOST ONE bucket so resolution actions
    don't double-count it."""
    from control_room.rooms.factory_intake_dock import _compute_bulk_resolve_buckets

    items = [
        {"audit_id": "1", "reason": "nist_asd_no_energy_level_rows",
         "source_file": "reports/campaign_019/fixtures/some/audit_queue.json"},
    ]
    buckets = _compute_bulk_resolve_buckets(items)
    counts = sum(b["count"] for b in buckets.values())
    assert counts == 1, "first match wins; item must not be double-counted"


# ---------------------------------------------------------------------------
# Issue 8/10 — cached_adapters wrappers
# ---------------------------------------------------------------------------


def test_cached_adapters_module_exposes_expected_wrappers():
    """The smoothness optimization adds Streamlit-cached wrappers around
    expensive adapters. Each wrapper should be importable and callable."""
    import control_room.cached_adapters as ca

    expected = [
        "cached_build_log",
        "cached_campaign_reports",
        "cached_factory_store",
        "cached_methods_falsifiers",
        "cached_records_for_world",
        "cached_audit_inbox_summary",
    ]
    for name in expected:
        assert hasattr(ca, name), f"{name} missing from cached_adapters"
        assert callable(getattr(ca, name))


def test_cached_records_for_world_returns_same_payload_as_underlying():
    """The cache wrapper must return a payload structurally equivalent
    to the underlying adapter (no shape drift)."""
    from control_room.cached_adapters import cached_records_for_world
    from control_room.rooms._world_drilldown import load_records_for_world

    direct = load_records_for_world("math_primitives")
    cached = cached_records_for_world("math_primitives")
    assert {r.get("record_id") for r in direct} == {r.get("record_id") for r in cached}
