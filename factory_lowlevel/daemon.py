"""Schedulable low-level Factory daemon hooks."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from .pipeline import run_low_level_factory
from .schemas import sha256, utc_now


DEFAULT_SESSION_LEDGER = Path("project_telemetry/low_level_factory_sessions.jsonl")


def run_factory_cycle(
    *,
    allow_network: bool = False,
    store_root: str | Path = "reports/campaign_016/daemon_store",
    cache_dir: str | Path = "reports/campaign_016/source_cache",
    session_ledger: str | Path = DEFAULT_SESSION_LEDGER,
    trigger: str = "manual_cycle",
) -> dict[str, Any]:
    run = run_low_level_factory(store_root=store_root, cache_dir=cache_dir, allow_network=allow_network)
    ledger_path = Path(session_ledger)
    prior_run_ids = _prior_run_ids(ledger_path)
    record = {
        "schema": "LowLevelFactorySessionRecord.v1",
        "session_id": sha256({"run_id": run["run_id"], "trigger": trigger, "seen_count": len(prior_run_ids)}),
        "run_id": run["run_id"],
        "trigger": trigger,
        "recorded_at": utc_now(),
        "requires_ai_runtime": False,
        "idempotent_duplicate_run_id": run["run_id"] in prior_run_ids,
        "store_counts": run["store_snapshot"]["counts"],
        "routed_worlds": run["routed_worlds"],
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return record


def run_daemon_loop(
    *,
    cycles: int = 1,
    sleep_seconds: int = 3600,
    allow_network: bool = False,
    session_ledger: str | Path = DEFAULT_SESSION_LEDGER,
) -> list[dict[str, Any]]:
    records = []
    for index in range(cycles):
        records.append(run_factory_cycle(allow_network=allow_network, session_ledger=session_ledger, trigger=f"loop_cycle_{index}"))
        if index < cycles - 1:
            time.sleep(sleep_seconds)
    return records


def _prior_run_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    run_ids = set()
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            run_ids.add(json.loads(line).get("run_id", ""))
        except json.JSONDecodeError:
            continue
    return {run_id for run_id in run_ids if run_id}
