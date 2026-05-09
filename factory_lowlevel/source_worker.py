"""CLI worker that runs exactly one Factory source adapter."""

from __future__ import annotations

import argparse
import json
import traceback
from pathlib import Path

from .live_pipeline import run_live_factory_cycle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one Factory source in a child process.")
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--store-root", required=True)
    parser.add_argument("--cache-dir", required=True)
    parser.add_argument("--run-root", required=True)
    parser.add_argument("--trace-root", required=True)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--result-path", required=True)
    parser.add_argument("--allow-network", action="store_true")
    args = parser.parse_args(argv)

    result_path = Path(args.result_path)
    result_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        run = run_live_factory_cycle(
            source_ids=[args.source_id],
            allow_network=args.allow_network,
            store_root=args.store_root,
            cache_dir=args.cache_dir,
            run_root=args.run_root,
            trace_root=args.trace_root,
            trigger=args.trigger,
        )
        payload = {
            "status": "ok",
            "source_id": args.source_id,
            "run_id": run["run_id"],
            "record_count": len(run.get("records", [])),
            "trace_record_count": len(run.get("trace_records", [])),
        }
        result_path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return 0
    except Exception as exc:
        payload = {
            "status": "error",
            "source_id": args.source_id,
            "error_type": type(exc).__name__,
            "error": str(exc),
            "traceback_tail": traceback.format_exc()[-4000:],
        }
        result_path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return 1


if __name__ == "__main__":  # pragma: no cover - exercised via subprocess.
    raise SystemExit(main())
