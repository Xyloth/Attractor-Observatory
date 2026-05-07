"""Streamlit-cached wrappers around the expensive adapter calls.

CB-011 fix #8/#10 — smoothness: James reported lag on room switching.
Profiling showed every render of every room calls
``parse_build_log()``, ``parse_campaign_reports()``, ``build_snapshot()``,
and ``load_records_for_world()`` from disk. With the W-1 mass-ingest
adding 1,394 records and the BUILD_LOG growing to 41 entries with
prose bodies, each cold call was 50-200 ms — and the autorefresh
loop was firing every 1.5 s, so the room was re-scanning the entire
reports/ tree several times per second.

These wrappers add a 10-second TTL via ``st.cache_data``: within a
10 s window, repeated calls return the cached payload. The
autorefresh loop still fires for liveness, but the heavy I/O happens
once per 10 s instead of every render. D17 binding stays intact —
``stale_cache: true`` flags surface in the underlying adapter, and
the cache TTL is a smoothness optimization, not a freshness override.
"""

from __future__ import annotations

from typing import Any


def _maybe_cache(ttl_seconds: int = 10):
    """Return ``st.cache_data(ttl=...)`` when Streamlit is in scope,
    else a no-op decorator. Lets these wrappers be importable from
    test code that doesn't run inside Streamlit."""
    try:
        import streamlit as st
        return st.cache_data(ttl=ttl_seconds, show_spinner=False)
    except Exception:
        def _identity(fn):
            return fn
        return _identity


@_maybe_cache(ttl_seconds=10)
def cached_build_log() -> dict[str, Any]:
    from control_room.adapters import parse_build_log
    return parse_build_log()


@_maybe_cache(ttl_seconds=10)
def cached_campaign_reports() -> dict[str, Any]:
    from control_room.adapters import parse_campaign_reports
    return parse_campaign_reports()


@_maybe_cache(ttl_seconds=10)
def cached_factory_store() -> dict[str, Any]:
    from control_room.adapters import parse_factory_store
    return parse_factory_store()


@_maybe_cache(ttl_seconds=10)
def cached_methods_falsifiers() -> dict[str, Any]:
    from control_room.adapters import parse_methods_falsifiers
    return parse_methods_falsifiers()


@_maybe_cache(ttl_seconds=10)
def cached_records_for_world(world_family: str) -> list[dict[str, Any]]:
    from control_room.rooms._world_drilldown import load_records_for_world
    return load_records_for_world(world_family)


@_maybe_cache(ttl_seconds=10)
def cached_audit_inbox_summary() -> dict[str, Any]:
    from control_room.rooms.factory_intake_dock import _audit_inbox_summary
    return _audit_inbox_summary()
