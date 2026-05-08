"""CB-020 reader-loop: Streamlit autorefresh load proxy.

Polls the live-state files at Streamlit-class frequency (every 0.3s,
~10x faster than Streamlit's default 3s autorefresh) so the daemon's
write path is contended throughout the verify cycle. If the CB-020
fix is real, the daemon completes cleanly under this load.

Reads via the F3-compliant pattern: ``path.read_text(encoding="utf-8-sig")``,
single call per file, no held open() context. Uses the new
``safe_read_json`` helper to ride out reader-side races.

Logs every read failure (post-fix should be zero). Logs every 100 reads
to stdout so progress is visible. Exits when ``stop_path`` exists.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# Resolve project root from script location
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from factory_lowlevel.persistence import safe_read_json


LIVE_STATE = Path("control_room/cache/factory_runs/latest_state.json")
LATEST_RUN = Path("control_room/cache/factory_runs/latest_run.json")
HEARTBEAT = Path("control_room/cache/factory_daemon_heartbeat.json")
STOP_FLAG = Path("control_room/cache/cb020_reader_stop.flag")

POLL_INTERVAL = 0.3  # seconds; 10x faster than Streamlit's default 3s autorefresh


def main() -> int:
    n_reads = 0
    n_state = 0
    n_run = 0
    n_heartbeat = 0
    n_errors = 0
    start = time.time()
    last_log = start

    print(f"[reader-loop] starting at poll_interval={POLL_INTERVAL}s, stop flag={STOP_FLAG}", flush=True)
    print(f"[reader-loop] watching: {LIVE_STATE}, {LATEST_RUN}, {HEARTBEAT}", flush=True)

    while not STOP_FLAG.exists():
        try:
            for path, counter_name in [
                (LIVE_STATE, "n_state"),
                (LATEST_RUN, "n_run"),
                (HEARTBEAT, "n_heartbeat"),
            ]:
                payload = safe_read_json(path, default=None)
                if payload is not None:
                    if counter_name == "n_state":
                        n_state += 1
                    elif counter_name == "n_run":
                        n_run += 1
                    else:
                        n_heartbeat += 1
                n_reads += 1
        except BaseException as exc:  # noqa: BLE001
            n_errors += 1
            print(f"[reader-loop] ERROR @ read {n_reads}: {type(exc).__name__}: {exc}", flush=True)

        # Progress log every 30s
        now = time.time()
        if now - last_log >= 30:
            elapsed_min = (now - start) / 60
            rate = n_reads / (now - start) if (now - start) > 0 else 0
            print(f"[reader-loop] +{elapsed_min:.1f}m: reads={n_reads} ({rate:.1f}/s); state={n_state} run={n_run} hb={n_heartbeat}; errors={n_errors}", flush=True)
            last_log = now

        time.sleep(POLL_INTERVAL)

    elapsed_min = (time.time() - start) / 60
    print(f"[reader-loop] STOP flag detected, exiting at +{elapsed_min:.1f}m", flush=True)
    print(f"[reader-loop] FINAL: reads={n_reads}; state={n_state} run={n_run} hb={n_heartbeat}; errors={n_errors}", flush=True)
    return 0 if n_errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
