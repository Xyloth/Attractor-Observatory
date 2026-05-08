"""Removal probe — mechanical liveness assessment.

Per spec §"Removal Probe Protocol", `cleanup_candidate_status ∈
{removable_clean, removable_with_warnings, not_removable}` requires a
recorded ``removal_probe`` with command and outcome. Without that, the
status defaults to ``unknown``.

PG-001 v1 declares a global probe-budget of zero per-file seconds (see
manifest's ``THRESHOLD_POLICY['probe']``). The probe routes every file
through one of:

* ``probe_declined`` for critical-path files (irreversible state risk).
* ``unknown`` (with ``removal_probe.decline_reason =
  removal_probe_over_budget``) for everything else.

The spec explicitly permits this under-claimed posture: "If running the
full probe is too expensive in a single PG-001 run, the manifest may
declare a probe-budget. Files exceeding the budget are recorded as
``unknown`` rather than ``removable_clean``; under-claimed status is
permitted, over-claimed is not."

The PG-001 v1 manifest also declares a branch-level cleanup-candidate
sentinel: the public test suite (``public_tests/test_pg001_*.py``)
collects without import errors against the published atlas. Per-file
stash/restore is deferred to PG-002 once the budget is sized against
real per-file cost data.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from project_genealogy.manifest import is_critical_path


def run_probe(
    rel_path: str,
    artifact_family: str,
    threshold_policy: dict[str, Any],
    edges_in: list[dict[str, Any]],
) -> dict[str, Any]:
    """Return the ``liveness`` block for the given file."""
    is_critical = is_critical_path(rel_path)
    imports_in = sum(1 for e in edges_in if e.get("edge_type") == "imports")
    validators = sum(1 for e in edges_in if e.get("edge_type") == "validates")
    citations = sum(1 for e in edges_in if e.get("edge_type") == "cites")
    runtime_refs = imports_in + validators

    common = {
        "downstream_reference_count": imports_in + citations,
        "runtime_reference_count": runtime_refs,
    }

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    if is_critical:
        return {
            **common,
            "last_touched_commit": "",
            "last_touched_date": "",
            "cleanup_candidate_status": "probe_declined",
            "cleanup_reason": (
                "critical-path file (persistence/lock/schema/adapter or "
                "shipped public surface); per-file stash/restore would "
                "risk irreversible state"
            ),
            "removal_probe": {
                "ran_at": timestamp,
                "command": "",
                "outcome": "declined",
                "diff_summary": "",
                "evidence_refs": [
                    {
                        "ref_id": f"probe::{rel_path}::critical",
                        "kind": "schema",
                        "locator": "project_genealogy/manifest.py:CRITICAL_PATH_PATTERNS",
                        "content_hash": "",
                        "evidence_private": False,
                        "note": "matched manifest critical-path pattern",
                    }
                ],
                "decline_reason": "removal_probe_declined_critical_path",
            },
        }

    return {
        **common,
        "last_touched_commit": "",
        "last_touched_date": "",
        "cleanup_candidate_status": "unknown",
        "cleanup_reason": (
            "PG-001 v1 declines per-file removal probes globally under "
            "removal_probe_over_budget; status defaults to unknown rather "
            "than over-claiming removable_clean"
        ),
        "removal_probe": {
            "ran_at": timestamp,
            "command": "",
            "outcome": "declined",
            "diff_summary": "",
            "evidence_refs": [
                {
                    "ref_id": f"probe::{rel_path}::budget",
                    "kind": "schema",
                    "locator": "input_manifest.json#threshold_policy.probe",
                    "content_hash": "",
                    "evidence_private": False,
                    "note": "probe budget zero per-file seconds in v1",
                }
            ],
            "decline_reason": "removal_probe_over_budget",
        },
    }
