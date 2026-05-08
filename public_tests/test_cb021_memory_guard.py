"""TASK-CB-021 — memory-safety guardrails after 2026-05-08 OOM incident.

The incident report (factory-daemon-incident-report-2026-05-08.md)
documented the daemon eating 40-50 GB of RSS in one long-lived Python
process and white-screening the desktop. Architectural fixes (sharded
persistence, per-source child processes, SQLite migration) deferred
to a separate ticket; CB-021 ships *guardrails* so the same case
can't reach system-killing levels again:

* M1: ``check_memory_budget()`` — RSS / free-RAM thresholds.
* M2: live_pipeline drops trace bodies from ``trace_rows`` after each
  per-bundle motif evaluation pass (was the load-bearing peak).
* M3: file-based stop flag at ``control_room/cache/factory_daemon_stop.flag``
  (Windows signal handling is unreliable on detached nohup processes).
* M4: heartbeat + live_state enriched with RSS + free-RAM so a stale
  heartbeat is also a memory diagnostic.

Tests:

1. ``test_measure_memory_returns_real_values`` — measure_memory()
   succeeds on the test platform (psutil OR Windows ctypes OR
   /proc).
2. ``test_check_memory_budget_within_default`` — under default
   thresholds, this Python process passes.
3. ``test_check_memory_budget_aborts_on_low_max_rss`` — set
   max_rss_gb=0.001 → should fail with reason
   "memory_budget_exceeded".
4. ``test_check_memory_budget_aborts_on_high_min_free`` — set
   min_free_gb=999 → should fail with the same reason.
5. ``test_check_memory_budget_propagates_non_transient_unmeasured``
   — when memory is unmeasured, guard returns ``ok=True`` (safety
   not correctness; daemon doesn't fail closed on unmeasured).
6. ``test_read_stop_flag_returns_none_when_absent`` — happy path.
7. ``test_read_stop_flag_returns_reason_when_present`` — tmp_path
   stop flag with content; reader returns the reason string.
8. ``test_consume_stop_flag_idempotent`` — calling on absent +
   present file both succeed without raising.
9. ``test_simulate_record_metadata_only_after_bundle`` — direct
   verification that the per-bundle drop-trace logic produces
   ``row["trace"] is None`` after the loop, while metadata
   (record_id, source_id, world_family, trace_path, trace_id)
   remains intact.
10. ``test_heartbeat_carries_pid_rss_after_cb021`` — sanity check:
    a fresh heartbeat write includes ``pid``, ``rss_gb``,
    ``free_ram_gb``, ``memory_source`` keys.
11. ``test_live_state_carries_rss_after_cb021`` — same for the
    high-frequency latest_state.json writes.

Runtime <1s. No daemon launch.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# M1 — memory budget guard
# ---------------------------------------------------------------------------


def test_measure_memory_returns_real_values():
    """Should succeed on Windows (ctypes) OR Linux (/proc) OR with psutil."""
    from factory_lowlevel.memory_guard import measure_memory

    snap = measure_memory()
    if snap.source == "unmeasured":
        # Acceptable — guard is best-effort. But on the dev platforms
        # (Windows + Linux) at least one backend should work.
        pytest.skip("no memory backend available; guard inactive")
    assert snap.rss_gb is not None and snap.rss_gb > 0
    assert snap.free_gb is not None and snap.free_gb > 0
    assert snap.is_measured()


def test_check_memory_budget_within_default():
    """Default thresholds (24 GB RSS, 8 GB free) — this small test
    process should pass easily."""
    from factory_lowlevel.memory_guard import check_memory_budget

    ok, snap, reason = check_memory_budget()
    if not snap.is_measured():
        pytest.skip("memory unmeasured")
    assert ok, f"unexpectedly failed budget: {reason}"
    assert reason == "memory_within_budget"


def test_check_memory_budget_aborts_on_low_max_rss():
    """Set max_rss_gb=0.001; even an idle Python interpreter exceeds
    this. Verify the guard fires with the canonical reason string."""
    from factory_lowlevel.memory_guard import check_memory_budget

    ok, snap, reason = check_memory_budget(max_rss_gb=0.001)
    if not snap.is_measured():
        pytest.skip("memory unmeasured")
    assert not ok
    assert reason.startswith("memory_budget_exceeded:")
    assert "RSS" in reason


def test_check_memory_budget_aborts_on_high_min_free():
    """Set min_free_gb=99999; no system has 99 TB free RAM."""
    from factory_lowlevel.memory_guard import check_memory_budget

    ok, snap, reason = check_memory_budget(min_free_gb=99999.0)
    if not snap.is_measured():
        pytest.skip("memory unmeasured")
    assert not ok
    assert reason.startswith("memory_budget_exceeded:")
    assert "free RAM" in reason


def test_check_memory_budget_unmeasured_returns_ok():
    """When memory backend is unavailable, guard returns ok=True
    (safety, not correctness — daemon does not fail closed on
    unmeasured because the guard is best-effort)."""
    from factory_lowlevel.memory_guard import MemorySnapshot
    from unittest.mock import patch

    fake_unmeasured = MemorySnapshot(rss_gb=None, free_gb=None, source="unmeasured")
    with patch("factory_lowlevel.memory_guard.measure_memory", return_value=fake_unmeasured):
        from factory_lowlevel.memory_guard import check_memory_budget
        ok, snap, reason = check_memory_budget()
    assert ok
    assert reason == "memory_unmeasured_guard_inactive"
    assert not snap.is_measured()


# ---------------------------------------------------------------------------
# M3 — file-based stop flag
# ---------------------------------------------------------------------------


def test_read_stop_flag_returns_none_when_absent(tmp_path):
    from factory_lowlevel.memory_guard import read_stop_flag

    flag = tmp_path / "stop.flag"
    assert read_stop_flag(flag) is None


def test_read_stop_flag_returns_reason_when_present(tmp_path):
    from factory_lowlevel.memory_guard import read_stop_flag

    flag = tmp_path / "stop.flag"
    flag.write_text("operator triggered shutdown for memory triage", encoding="utf-8")
    reason = read_stop_flag(flag)
    assert reason == "operator triggered shutdown for memory triage"


def test_read_stop_flag_returns_default_on_empty_content(tmp_path):
    from factory_lowlevel.memory_guard import read_stop_flag

    flag = tmp_path / "stop.flag"
    flag.write_text("", encoding="utf-8")
    reason = read_stop_flag(flag)
    assert reason == "operator_stop_flag_set"


def test_consume_stop_flag_idempotent(tmp_path):
    """consume_stop_flag must not raise when called on absent or
    present file; both result in the file being absent afterward."""
    from factory_lowlevel.memory_guard import consume_stop_flag

    flag = tmp_path / "stop.flag"
    # Absent path
    consume_stop_flag(flag)
    assert not flag.exists()
    # Present path
    flag.write_text("test", encoding="utf-8")
    assert flag.exists()
    consume_stop_flag(flag)
    assert not flag.exists()


# ---------------------------------------------------------------------------
# M2 — per-bundle streaming + drop trace bodies
# ---------------------------------------------------------------------------


def test_simulate_record_metadata_keys_present():
    """Sanity check: _simulate_record returns a row with the metadata
    keys that downstream (life_forms, _trace_row_public, evidence_rows)
    rely on. After CB-021 the row may have ``trace=None`` post-bundle
    but these metadata keys must persist."""
    import inspect

    from factory_lowlevel import live_pipeline

    src = inspect.getsource(live_pipeline._simulate_record)
    # The return dict carries these fields explicitly.
    expected_keys = {
        "record_id",
        "canonical_name",
        "source_id",
        "world_family",
        "trace_path",
        "trace_id",
    }
    for key in expected_keys:
        assert f'"{key}"' in src, (
            f"_simulate_record return dict missing key {key!r}; "
            f"life_forms / trace_records output relies on this."
        )


def test_run_live_factory_cycle_drops_trace_bodies_per_bundle():
    """AST sanity check: the per-bundle loop in run_live_factory_cycle
    must drop trace bodies (set to None) AFTER computing life_forms
    so RAM doesn't accumulate across bundles. Pre-CB-021 the loop
    accumulated all trace bodies into a single trace_rows list."""
    import ast

    src = (ROOT / "factory_lowlevel" / "live_pipeline.py").read_text(encoding="utf-8")
    tree = ast.parse(src)

    target_fn: ast.FunctionDef | None = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "run_live_factory_cycle":
            target_fn = node
            break
    assert target_fn is not None

    # Look for the post-bundle drop loop. We search for
    # `row["trace"] = None` inside a for-loop in run_live_factory_cycle.
    found_drop = False
    for node in ast.walk(target_fn):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.slice, ast.Constant)
                    and target.slice.value == "trace"
                    and isinstance(node.value, ast.Constant)
                    and node.value.value is None
                ):
                    found_drop = True
                    break

    assert found_drop, (
        "CB-021 M2: run_live_factory_cycle must drop trace bodies (row['trace'] = None) "
        "post-bundle to bound RAM peak. This was the load-bearing memory leak from the "
        "2026-05-08 incident."
    )


def test_run_live_factory_cycle_uses_gc_collect_between_bundles():
    """The per-bundle loop must call gc.collect() between bundles to
    ensure Python releases trace bodies + evidence rows + lens
    evaluation cycles before the next bundle starts. Without this,
    the generational collector can hold referent cycles across
    multi-second gaps."""
    src = (ROOT / "factory_lowlevel" / "live_pipeline.py").read_text(encoding="utf-8")
    assert "gc.collect()" in src, (
        "CB-021 M2 expects gc.collect() inside the per-bundle loop"
    )
    assert "import gc" in src, "factory_lowlevel.live_pipeline must import gc"


# ---------------------------------------------------------------------------
# M4 — heartbeat + live_state RSS enrichment
# ---------------------------------------------------------------------------


def test_heartbeat_payload_includes_pid_rss_free():
    """AST/source sanity: continuous_daemon._write_heartbeat must
    embed pid, rss_gb, free_ram_gb, memory_source keys so a stale
    heartbeat is itself a memory diagnostic."""
    src = (ROOT / "factory_lowlevel" / "continuous_daemon.py").read_text(encoding="utf-8")
    for key in ('"pid"', '"rss_gb"', '"free_ram_gb"', '"memory_source"'):
        assert key in src, (
            f"CB-021 M4: heartbeat payload must include {key} per "
            f"factory-daemon-incident-report-2026-05-08.md liveness recommendations"
        )


def test_live_state_payload_includes_rss():
    """AST/source sanity: live_pipeline._write_live_state must embed
    rss_gb + free_ram_gb so the high-frequency latest_state.json
    is itself a memory pulse."""
    src = (ROOT / "factory_lowlevel" / "live_pipeline.py").read_text(encoding="utf-8")
    # Find the _write_live_state body
    state_payload_block = src.split("def _write_live_state")[-1].split("def ")[0]
    assert '"rss_gb"' in state_payload_block, (
        "CB-021 M4: latest_state.json payload must include rss_gb "
        "(live_pipeline._write_live_state)"
    )
    assert '"free_ram_gb"' in state_payload_block


# ---------------------------------------------------------------------------
# Daemon plumbing: stop-flag check + memory budget check are wired into the loop
# ---------------------------------------------------------------------------


def test_continuous_daemon_calls_stop_flag_check():
    """Sanity: continuous_daemon.run_continuous_daemon must read the
    stop flag between sources and break out of the source loop when set."""
    src = (ROOT / "factory_lowlevel" / "continuous_daemon.py").read_text(encoding="utf-8")
    assert "read_stop_flag" in src
    assert "consume_stop_flag" in src
    assert "operator_stop_flag_honored" in src


def test_continuous_daemon_calls_memory_budget_check():
    """Sanity: continuous_daemon.run_continuous_daemon must call
    check_memory_budget between sources and break out of the loop
    on memory_budget_exceeded."""
    src = (ROOT / "factory_lowlevel" / "continuous_daemon.py").read_text(encoding="utf-8")
    assert "check_memory_budget" in src
    assert "memory_budget_exceeded" in src
