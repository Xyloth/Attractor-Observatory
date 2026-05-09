"""Per-source child-process supervision for the Factory daemon."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


def build_source_worker_command(
    *,
    source_id: str,
    allow_network: bool,
    store_root: str | Path,
    cache_dir: str | Path,
    run_root: str | Path,
    trace_root: str | Path,
    trigger: str,
    result_path: str | Path,
) -> list[str]:
    command = [
        sys.executable,
        "-m",
        "factory_lowlevel.source_worker",
        "--source-id",
        source_id,
        "--store-root",
        str(store_root),
        "--cache-dir",
        str(cache_dir),
        "--run-root",
        str(run_root),
        "--trace-root",
        str(trace_root),
        "--trigger",
        trigger,
        "--result-path",
        str(result_path),
    ]
    if allow_network:
        command.append("--allow-network")
    return command


def run_source_child_process(
    *,
    source_id: str,
    allow_network: bool,
    store_root: str | Path,
    cache_dir: str | Path,
    run_root: str | Path,
    trace_root: str | Path,
    trigger: str,
    timeout_seconds: int | None = None,
) -> dict[str, Any]:
    """Run one source in a short-lived worker process and return its result."""

    result_dir = Path(tempfile.mkdtemp(prefix="factory_source_worker_"))
    result_path = result_dir / f"{_safe_name(source_id)}.json"
    command = build_source_worker_command(
        source_id=source_id,
        allow_network=allow_network,
        store_root=store_root,
        cache_dir=cache_dir,
        run_root=run_root,
        trace_root=trace_root,
        trigger=trigger,
        result_path=result_path,
    )
    completed = subprocess.run(
        command,
        cwd=Path.cwd(),
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    if result_path.exists():
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    else:
        payload = {
            "status": "error",
            "error_type": "worker_result_missing",
            "error": completed.stderr.strip() or completed.stdout.strip(),
        }
    payload.setdefault("worker_exit_code", completed.returncode)
    payload.setdefault("worker_stdout_tail", completed.stdout[-4000:])
    payload.setdefault("worker_stderr_tail", completed.stderr[-4000:])
    return payload


def _safe_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in value)[:80]
