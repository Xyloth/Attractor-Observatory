"""TASK-CB-020 — concurrency stress for live-state file writes.

Reproduces the race that quarantined 6 of 17 sources during the CB-019
daemon relaunch (08:23 EST 2026-05-08, PID 27516):

  ``OSError [Errno 22] Invalid argument: 'control_room/cache/factory_runs/latest_state.json'``
  ``PermissionError [WinError 5] Access is denied: '.evidence_graph.json.tmp' -> 'evidence_graph.json'``

Root cause: Streamlit Control Room (and Atlas Tower poller, anti-virus
scanners, OneDrive sync) periodically read ``latest_state.json`` /
``latest_run.json``. On Windows, ``Path.replace()`` (which is what
``atomic_write_json`` uses for the temp -> dest swap) raises
``OSError [Errno 22]`` (EINVAL) or ``PermissionError [WinError 5]``
(EACCES) when the destination has any open handle, even a transient
one. Pre-CB-020 ``_safe_write_json`` only caught ``PermissionError``,
so the EINVAL leaked, the daemon retried 3x, and quarantined the source.

CB-020 fix:

* ``factory_lowlevel.persistence.atomic_write_json`` retries the
  ``replace()`` step with exponential backoff (50ms -> 6.4s, ~12.7s
  worst-case) on a defined transient errno set: EACCES, EAGAIN,
  EBUSY, EINVAL, ENOENT.
* ``factory_lowlevel.live_pipeline._safe_write_json`` catches
  ``OSError`` (parent of PermissionError) and falls through to a
  non-atomic last-resort write that targets the canonical path
  (no orphan timestamped sibling).

These tests pin the contract:

1. ``test_atomic_write_json_concurrent_writer_reader`` — 1 writer
   + 1 reader, 200 iterations each. Pre-fix: probabilistic
   OSError on Windows. Post-fix: zero unhandled exceptions on
   either side; final JSON parses cleanly.
2. ``test_atomic_write_json_three_writers_two_readers_worst_case``
   — 3 writers + 2 readers (Streamlit + Atlas + daemon worst case).
3. ``test_atomic_write_json_retries_on_transient_oserror`` — unit
   test: monkey-patch ``Path.replace`` to fail N times with EINVAL,
   then succeed; verify the retry loop succeeds.
4. ``test_atomic_write_json_propagates_real_oserror`` — non-transient
   errno (ENOSPC = disk full) propagates immediately, NOT retried.
5. ``test_safe_write_json_orphan_fallback_writes_to_canonical_path``
   — when atomic_write_json fully exhausts retries, the fallback
   loops on the canonical path; never writes to a timestamped
   sibling that would orphan the data.

Runtime <2s. No daemon launch.
"""

from __future__ import annotations

import errno
import json
import sys
import threading
import time
from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# F4 — concurrency stress (1 writer + 1 reader)
# ---------------------------------------------------------------------------


def test_atomic_write_json_concurrent_writer_reader(tmp_path):
    """1 writer thread + 1 reader thread, 200 iterations each.

    Pre-CB-020: Windows ``Path.replace()`` raised OSError [Errno 22]
    on the writer side, AND ``read_text()`` raised PermissionError on
    the reader side, both when concurrent. Post-fix: writer's
    ``atomic_write_json`` retries on the transient errno set; reader's
    ``safe_read_json`` does the same with a tighter budget. Zero
    unhandled exceptions on either side; final state is well-formed."""
    from factory_lowlevel.persistence import atomic_write_json, safe_read_json

    target = tmp_path / "latest_state.json"
    iterations = 200
    write_errors: list[BaseException] = []
    read_errors: list[BaseException] = []
    successful_reads = {"n": 0}
    writes_done = threading.Event()

    def writer() -> None:
        try:
            for i in range(iterations):
                atomic_write_json(target, {"counter": i, "schema": "test.v1"})
        except BaseException as exc:  # noqa: BLE001
            write_errors.append(exc)
        finally:
            writes_done.set()

    def reader() -> None:
        deadline_iter = iterations
        while not writes_done.is_set() or deadline_iter > 0:
            try:
                payload = safe_read_json(target, default=None)
                if payload is not None:
                    assert payload.get("schema") == "test.v1"
                    successful_reads["n"] += 1
                    deadline_iter -= 1
            except BaseException as exc:  # noqa: BLE001
                read_errors.append(exc)
            time.sleep(0.001)

    t_w = threading.Thread(target=writer)
    t_r = threading.Thread(target=reader)
    t_w.start()
    t_r.start()
    t_w.join(timeout=30)
    t_r.join(timeout=10)

    assert not write_errors, (
        f"writer raised {len(write_errors)} exceptions; "
        f"first: {type(write_errors[0]).__name__}: {write_errors[0]}"
    )
    assert not read_errors, (
        f"reader raised {len(read_errors)} exceptions; "
        f"first: {type(read_errors[0]).__name__}: {read_errors[0]}"
    )
    # Reader must have completed at least one successful read; otherwise
    # safe_read_json's fail-soft default short-circuited everything.
    assert successful_reads["n"] >= iterations // 4, (
        f"only {successful_reads['n']}/{iterations} successful reads; "
        f"safe_read_json budget too tight or writer locking out reader"
    )
    final = safe_read_json(target)
    assert final["schema"] == "test.v1"
    assert 0 <= final["counter"] < iterations


# ---------------------------------------------------------------------------
# F4 — concurrency stress (3 writers + 2 readers, worst case)
# ---------------------------------------------------------------------------


def test_atomic_write_json_three_writers_two_readers_worst_case(tmp_path):
    """Worst case: 3 writers + 2 readers concurrent on the same path.

    Mimics Streamlit + Atlas Tower + daemon-monitor all polling while
    the daemon writes. With CB-020's retry-with-backoff (atomic_write_json
    + safe_read_json), must converge without unhandled exceptions on
    any side."""
    from factory_lowlevel.persistence import atomic_write_json, safe_read_json

    target = tmp_path / "latest_run.json"
    iterations = 100  # per writer
    write_errors: list[BaseException] = []
    read_errors: list[BaseException] = []
    successful_reads = {"n": 0}
    writers_done = threading.Event()
    writers_remaining = [3]
    lock = threading.Lock()

    def writer(thread_id: int) -> None:
        try:
            for i in range(iterations):
                atomic_write_json(
                    target,
                    {"writer": thread_id, "counter": i, "schema": "test.v1"},
                )
        except BaseException as exc:  # noqa: BLE001
            write_errors.append(exc)
        finally:
            with lock:
                writers_remaining[0] -= 1
                if writers_remaining[0] == 0:
                    writers_done.set()

    def reader(thread_id: int) -> None:
        deadline_iter = iterations * 2
        while not writers_done.is_set() or deadline_iter > 0:
            try:
                payload = safe_read_json(target, default=None)
                if payload is not None:
                    assert payload.get("schema") == "test.v1"
                    successful_reads["n"] += 1
                    deadline_iter -= 1
            except BaseException as exc:  # noqa: BLE001
                read_errors.append(exc)
            time.sleep(0.001)

    threads = [
        *(threading.Thread(target=writer, args=(i,)) for i in range(3)),
        *(threading.Thread(target=reader, args=(i,)) for i in range(2)),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=60)

    assert not write_errors, (
        f"writers raised {len(write_errors)} exceptions; "
        f"first: {type(write_errors[0]).__name__}: {write_errors[0]}"
    )
    assert not read_errors, (
        f"readers raised {len(read_errors)} exceptions; "
        f"first: {type(read_errors[0]).__name__}: {read_errors[0]}"
    )
    assert successful_reads["n"] >= iterations, (
        f"only {successful_reads['n']} successful reads across 2 readers; "
        f"writers may be locking out readers"
    )
    final = safe_read_json(target)
    assert final["schema"] == "test.v1"
    assert 0 <= final["writer"] < 3
    assert 0 <= final["counter"] < iterations


# ---------------------------------------------------------------------------
# Unit tests for the retry loop (deterministic, not race-dependent)
# ---------------------------------------------------------------------------


def test_atomic_write_json_retries_on_transient_oserror(tmp_path):
    """Inject OSError(EINVAL) on the first 3 replace() calls; verify
    the retry loop succeeds on the 4th attempt."""
    from factory_lowlevel import persistence

    target = tmp_path / "out.json"

    # Track call count + original replace
    call_count = {"n": 0}
    original_replace = Path.replace

    def flaky_replace(self: Path, dest: Any) -> Any:
        call_count["n"] += 1
        if call_count["n"] <= 3:
            raise OSError(errno.EINVAL, "Invalid argument", str(dest))
        return original_replace(self, dest)

    with patch.object(Path, "replace", flaky_replace):
        result = persistence.atomic_write_json(target, {"value": 42})

    assert result == target
    assert json.loads(target.read_text(encoding="utf-8-sig")) == {"value": 42}
    assert call_count["n"] == 4, f"expected 4 attempts (3 failures + 1 success), got {call_count['n']}"


def test_atomic_write_json_retries_on_permission_error(tmp_path):
    """PermissionError (EACCES) is a subclass of OSError; verify it's
    in the transient set and gets retried."""
    from factory_lowlevel import persistence

    target = tmp_path / "out.json"
    call_count = {"n": 0}
    original_replace = Path.replace

    def flaky_replace(self: Path, dest: Any) -> Any:
        call_count["n"] += 1
        if call_count["n"] <= 2:
            raise PermissionError(errno.EACCES, "Access is denied", str(dest))
        return original_replace(self, dest)

    with patch.object(Path, "replace", flaky_replace):
        persistence.atomic_write_json(target, {"value": "ok"})

    assert call_count["n"] == 3
    assert json.loads(target.read_text(encoding="utf-8-sig")) == {"value": "ok"}


def test_atomic_write_json_propagates_real_oserror(tmp_path):
    """Non-transient errno (ENOSPC = disk full) must propagate immediately,
    NOT be retried. Otherwise we'd waste 12s of backoff on a real bug."""
    from factory_lowlevel import persistence

    target = tmp_path / "out.json"
    call_count = {"n": 0}

    def disk_full_replace(self: Path, dest: Any) -> Any:
        call_count["n"] += 1
        raise OSError(errno.ENOSPC, "No space left on device", str(dest))

    with patch.object(Path, "replace", disk_full_replace):
        with pytest.raises(OSError) as exc_info:
            persistence.atomic_write_json(target, {"value": 1})

    assert exc_info.value.errno == errno.ENOSPC
    # Must NOT have retried — disk-full should fail fast.
    assert call_count["n"] == 1, (
        f"ENOSPC should propagate immediately (no retry), got {call_count['n']} attempts"
    )


def test_atomic_write_json_exhausts_retry_budget_then_raises(tmp_path):
    """Permanent EINVAL exhausts the 8-attempt budget then propagates.
    Verifies the retry loop has a hard ceiling — no infinite loop."""
    from factory_lowlevel import persistence

    target = tmp_path / "out.json"
    call_count = {"n": 0}

    def always_busy_replace(self: Path, dest: Any) -> Any:
        call_count["n"] += 1
        raise OSError(errno.EINVAL, "Invalid argument", str(dest))

    with patch.object(Path, "replace", always_busy_replace):
        with pytest.raises(OSError) as exc_info:
            # Use shorter base_backoff so this test stays under 1s
            persistence.atomic_write_json(target, {"value": 1}, base_backoff_seconds=0.001)

    assert exc_info.value.errno == errno.EINVAL
    assert call_count["n"] == 8, f"expected exactly 8 attempts, got {call_count['n']}"


# ---------------------------------------------------------------------------
# F5 — orphan-write fallback
# ---------------------------------------------------------------------------


def test_safe_write_json_orphan_fallback_writes_to_canonical_path(tmp_path):
    """When atomic_write_json's retry budget is exhausted, the
    _safe_write_json fallback must loop on the CANONICAL path (write_text
    direct) — never write to a timestamped sibling that orphans the data.

    Pre-CB-020 the fallback wrote ``f'{stem}_{ts}{suffix}'`` which the
    daemon never reads back; that's data-loss-as-success."""
    from factory_lowlevel import live_pipeline

    target = tmp_path / "latest_state.json"
    call_count = {"atomic": 0}

    def always_fail(*args, **kwargs):
        call_count["atomic"] += 1
        raise OSError(errno.EINVAL, "Invalid argument", str(target))

    # Make atomic_write_json always fail; verify _safe_write_json's
    # fallback writes to the canonical path (write_text), not orphan sibling.
    with patch.object(live_pipeline, "atomic_write_json", always_fail):
        live_pipeline._safe_write_json(target, {"recovered": True})

    # Canonical path was written by the fallback path
    assert target.exists(), "canonical path must be written by fallback"
    assert json.loads(target.read_text(encoding="utf-8-sig")) == {"recovered": True}

    # No orphan sibling files were created
    siblings = [p for p in tmp_path.iterdir() if p != target]
    orphan_pattern = "latest_state_"  # stem prefix of the OLD orphan format
    orphans = [p for p in siblings if p.name.startswith(orphan_pattern)]
    assert not orphans, f"fallback created orphan sibling files: {orphans}"


def test_safe_write_json_canonical_path_succeeds_on_first_atomic(tmp_path):
    """Happy path: when atomic_write_json succeeds, _safe_write_json
    is a no-op wrapper. Doesn't fall through to the slow path."""
    from factory_lowlevel import live_pipeline

    target = tmp_path / "latest_state.json"
    live_pipeline._safe_write_json(target, {"happy": True})
    assert json.loads(target.read_text(encoding="utf-8-sig")) == {"happy": True}


# ---------------------------------------------------------------------------
# F1 sanity — _safe_write_json now catches OSError, not just PermissionError
# ---------------------------------------------------------------------------


def test_safe_write_json_catches_oserror_not_just_permission_error(tmp_path):
    """Sanity check on the F1 fix: _safe_write_json's except clause
    must catch OSError (broad), not just PermissionError (narrow). The
    pre-CB-020 narrow catch is what let the EINVAL leak through and
    quarantine 6 sources in CB-019."""
    import ast

    src = (ROOT / "factory_lowlevel" / "live_pipeline.py").read_text(encoding="utf-8")
    tree = ast.parse(src)

    target_fn: ast.FunctionDef | None = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "_safe_write_json":
            target_fn = node
            break
    assert target_fn is not None, "_safe_write_json not found in live_pipeline.py"

    # Find the try/except inside _safe_write_json
    excepts: list[ast.ExceptHandler] = []
    for node in ast.walk(target_fn):
        if isinstance(node, ast.ExceptHandler):
            excepts.append(node)

    assert excepts, "_safe_write_json has no except handlers"

    # The first except wrapping atomic_write_json must catch OSError
    # (or a broader Exception). PermissionError-only is the pre-CB-020 bug.
    caught_names: list[str] = []
    for h in excepts:
        if h.type is None:
            caught_names.append("BaseException")
        elif isinstance(h.type, ast.Name):
            caught_names.append(h.type.id)
        elif isinstance(h.type, ast.Tuple):
            for el in h.type.elts:
                if isinstance(el, ast.Name):
                    caught_names.append(el.id)

    assert "OSError" in caught_names or "Exception" in caught_names or "BaseException" in caught_names, (
        f"_safe_write_json must catch OSError (or broader); only catches {caught_names}. "
        f"This is the CB-019 quarantine bug."
    )
