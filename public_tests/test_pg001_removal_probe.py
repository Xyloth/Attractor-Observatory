"""PG-001 removal-probe protocol tests.

PG18 — every cleanup_candidate_status with a `removable_*` or
`not_removable` verdict carries a recorded ``removal_probe.command`` and
``removal_probe.outcome``. Bare ``unknown`` and ``probe_declined`` are
allowed, and the manifest's probe budget makes the latter the dominant
state in v1.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parent.parent
DOSSIER_DIR = REPO_ROOT / "reports" / "project_genealogy" / "dossiers"
MANIFEST_PATH = REPO_ROOT / "reports" / "project_genealogy" / "input_manifest.json"


def _require_manifest():
    if not MANIFEST_PATH.is_file():
        pytest.skip("input_manifest.json absent")
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _all_dossiers():
    if not DOSSIER_DIR.is_dir():
        pytest.skip("no dossiers published")
    return sorted(DOSSIER_DIR.glob("*.json"))


def test_critical_paths_are_probe_declined() -> None:
    """Critical paths declared in the manifest must be ``probe_declined``."""
    import re
    manifest = _require_manifest()
    patterns = manifest["critical_path_patterns"]
    dossiers = _all_dossiers()
    seen_one = False
    for p in dossiers:
        d = json.loads(p.read_text(encoding="utf-8"))
        rel = d["file"]["path"]
        if any(re.search(pat, rel) for pat in patterns):
            seen_one = True
            assert d["liveness"]["cleanup_candidate_status"] == "probe_declined", (
                f"{rel} matches critical-path pattern but status="
                f"{d['liveness']['cleanup_candidate_status']}"
            )
            assert d["liveness"]["removal_probe"]["decline_reason"] == "removal_probe_declined_critical_path"
    assert seen_one, "No critical-path dossiers found — manifest patterns may be wrong"


def test_non_removable_status_carries_probe_evidence() -> None:
    """Any positive removable verdict must record probe.command and probe.outcome."""
    dossiers = _all_dossiers()
    seen_status_counter: Counter[str] = Counter()
    for p in dossiers:
        d = json.loads(p.read_text(encoding="utf-8"))
        liv = d["liveness"]
        status = liv.get("cleanup_candidate_status", "unknown")
        seen_status_counter[status] += 1
        if status in {"removable_clean", "removable_with_warnings", "not_removable"}:
            rp = liv["removal_probe"]
            assert rp.get("command"), f"{p.name} {status} without probe.command"
            assert rp.get("outcome"), f"{p.name} {status} without probe.outcome"
    # PG-001 v1 budget defaults to zero per-file seconds so under-claimed
    # `unknown` plus `probe_declined` should dominate; that is acceptable
    # per spec §"Removal Probe Protocol".
    assert seen_status_counter["unknown"] + seen_status_counter["probe_declined"] > 0


def test_probe_decline_reasons_are_canonical() -> None:
    """Probe decline reasons must come from the manifest's decline taxonomy."""
    manifest = _require_manifest()
    canonical = set(manifest["decline_taxonomy"])
    dossiers = _all_dossiers()
    for p in dossiers:
        d = json.loads(p.read_text(encoding="utf-8"))
        liv = d["liveness"]
        reason = liv["removal_probe"].get("decline_reason", "")
        if reason:
            assert reason in canonical, f"{p.name} probe decline_reason {reason} is non-canonical"
