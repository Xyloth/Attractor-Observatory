# Builder Ingestion Monitoring Playbook

**Audience:** Claude Builder (any session — fresh or continuing) supervising the unattended Factory daemon.

**Goal:** detect anomalies in the running daemon, decide warn vs stop, execute the right shutdown / triage / resume sequence without ambiguity.

**Doctrine:** D7–D31. **D9 hard** — fail closed on doubt. **D17 hard** — stale data flagged stale. **D22 hard** — honest absence; never report "all good" when checks haven't run.

---

## 1 — Per-cycle health checks

Run these in order. Each check returns `pass`/`warn`/`stop` per the thresholds in §2.

### 1.1 Heartbeat freshness

```python
from control_room.factory_heartbeat import read_factory_heartbeat
hb = read_factory_heartbeat()
# hb["status"] in {"live", "stale", "missing", "malformed"}
# hb["age_seconds"] for the live freshness signal
```

* `live` + `age_seconds < 5*60` → **pass**
* `live` + `5*60 ≤ age_seconds < 15*60` → **warn**
* `stale` (age ≥ stale_threshold of 5 min) OR `age_seconds ≥ 15*60` → **stop**
* `missing` → **stop** (daemon not running, or heartbeat path moved)
* `malformed` → **stop** (D9 — investigate before resuming)

### 1.2 Audit queue depth

```python
from control_room.rooms.factory_intake_dock import _audit_inbox_summary
s = _audit_inbox_summary()
# s["unresolved_total"], s["high"], s["medium"], s["low"]
```

* `unresolved_total < 30` → **pass**
* `30 ≤ unresolved_total < 100` → **warn** (triage, but not stop)
* `unresolved_total ≥ 100` → **stop** + triage (probable producer regression)

### 1.3 Provenance completeness rate

For each record in the active store, count records carrying every required field (`source_url`, `retrieval_timestamp`, `parser_version`, `license_class`, `authority`).

```python
import json
from pathlib import Path
records = json.loads(Path("reports/factory_daemon_progress/<world>.json").read_text())
# OR query factory_lowlevel/index.py for the cross-store view
```

* completeness ≥ 99 % → **pass**
* 95 % ≤ completeness < 99 % → **warn**
* completeness < 95 % → **stop** (real bug — D9 binding)

### 1.4 Trace verification rate

```python
from factory_lowlevel.persistence import verify_world_traces
v = verify_world_traces("reports/<task>/factory_store")
# v["verified"][world_family] == True for every world
```

* every world `True` → **pass**
* any world `False` → **stop** (real bug — D9 binding)

### 1.5 Records-per-cycle band

```python
# Read the last N=20 cycles from project_telemetry/factory_daemon_sessions.jsonl
# Compute mean μ + stdev σ of (completed_source_count - quarantined_source_count).
# Current cycle outside μ ± 2σ → warn.
```

* current within μ ± 2σ → **pass**
* current outside μ ± 2σ → **warn** (note in BUILD_LOG; not stop)
* current < 0.1 × μ for 3 consecutive cycles → **stop** (effective halt)

### 1.6 Disk usage delta

```python
from factory_lowlevel.budget import usage_snapshot, BudgetConfig
us = usage_snapshot(store_root, cache_dir)
# Compare us["store_total"] to last cycle's snapshot.
```

* delta ≤ per-cycle budget (default 256 MiB) → **pass**
* delta > per-cycle budget → **stop** (run `BudgetEnforcer.evict_lru` or raise cap)

---

## 2 — Anomaly threshold table

| Check                                | warn threshold              | stop threshold                  | doctrine |
|--------------------------------------|-----------------------------|---------------------------------|----------|
| heartbeat staleness                  | > 5 min                     | > 15 min                        | D24      |
| audit queue depth                    | ≥ 30                        | ≥ 100                           | D9       |
| provenance completeness              | < 99 %                      | < 95 %                          | D19      |
| trace verification                   | —                           | any failure                     | D9       |
| records-per-cycle (μ±2σ)             | outside band                | < 0.1×μ for 3 consecutive       | D11      |
| disk delta                           | —                           | > per-cycle budget              | D7       |
| heartbeat status `resume_aborted`    | —                           | always (manual integrity audit) | D9       |
| heartbeat status `start_refused_lock_held` | —                     | always (concurrent run conflict)| D9       |

**Thresholds are tunable** via `factory_lowlevel/launch_safety.py`
constants and `factory_lowlevel/budget.py:BudgetConfig`. No hardcoded
magic numbers in the daemon body. Reading the threshold from a
config means a tightening / loosening decision is logged in the
config file's git history.

---

## 3 — Stop signal mechanics

### Graceful (SIGINT — preferred)

```bash
# Send SIGINT to the daemon process.
# On POSIX:  kill -INT <pid>
# On Windows: Ctrl-C in the terminal running factory_daemon.bat
#             OR: taskkill /PID <pid>      (sends Ctrl+Break ≈ SIGTERM)
```

The handler in `factory_lowlevel/launch_safety.py:install_signal_handlers`:

1. Sets `SignalState.stop_requested=True`.
2. Writes a heartbeat with `status: stop_requested_after_current_cycle`.
3. The daemon main loop finishes the in-flight cycle (no records lost).
4. Writes a final heartbeat with `status: clean_shutdown`.
5. Releases the lock file (`factory_store/.daemon_lock`).
6. Exits 0.

**State preserved**: empirical_records.json, normalized_refs.json, evidence_graph.json, audit_queue.json, snapshot.json, session ledger row, world_traces.json, ingestion_progress JSON. All written via atomic write-rename (`persistence.atomic_write_json`).

### Hard (SIGTERM)

```bash
# POSIX:    kill -TERM <pid>     (or kill <pid>)
# Windows:  taskkill /PID <pid> /F
```

The handler:

1. Sets `SignalState.hard_stop_requested=True`.
2. Writes a heartbeat with `status: hard_shutdown`.
3. Daemon breaks out of any in-flight cycle within ~1 second.
4. Releases the lock.
5. Exits 1.

**Risk:** the in-flight source MAY have partially-persisted records (the per-source persistence call is itself atomic, but cross-source consistency for the cycle is not). Use SIGINT preferentially.

---

## 4 — Resume mechanics

```bash
# After a stop, just restart the daemon:
factory_daemon.bat --cycles 0 --target-world crn --target-world field
```

The startup sequence:

1. `verify_resume()` reads the prior heartbeat.
2. If prior `status` ∈ {`clean_shutdown`, `complete`, `stop_requested_after_current_cycle`} → resume normally.
3. If prior `status` ∈ {`running`, `in_flight`, `hard_shutdown`} → run `check_factory_store_integrity()`:
   * record_id uniqueness
   * evidence-graph edge → record_id resolves
   * normalized_ref → record_id resolves
   * If integrity passes → resume.
   * If integrity fails → **abort with a heartbeat `status: resume_aborted`** and surface to Builder. Never overwrite.
4. `acquire_lock()` writes `factory_store/.daemon_lock` with this PID.
5. `install_signal_handlers()` wires SIGINT/SIGTERM.
6. The main loop runs.

**Verifying state integrity post-resume:**

```python
from factory_lowlevel.launch_safety import check_factory_store_integrity
result = check_factory_store_integrity("reports/campaign_035/factory_store")
# {"ok": True, "rationale": "...", "record_count": N, "orphan_edges": 0, "orphan_refs": 0}
```

If the daemon `verify_resume` aborted, run `check_factory_store_integrity` manually, fix the orphans (or restore from backup), then re-launch.

---

## 5 — Audit-queue triage rules

Use `control_room.rooms.factory_intake_dock._compute_bulk_resolve_buckets` (CB-011 T9 helper) to categorize. Five recognized buckets:

| Bucket                              | Pattern                                            | Resolution reason                  | Action                       |
|-------------------------------------|----------------------------------------------------|------------------------------------|------------------------------|
| `nist_source_limited`               | `reason == "nist_asd_no_energy_level_rows"`        | `D17_honest_no_source_data_available` | **bulk-resolve**          |
| `fixture_planted_false_claim`       | "planted false claim rejected" in reason           | `D9_test_fixture_validation`       | **bulk-resolve**             |
| `fixture_contradictory_polarity`    | `reason == "contradictory source-bound polarity"`  | `D9_test_fixture_validation`       | **bulk-resolve**             |
| `stale_cache_artifact`              | `reason.startswith("stale_cache:")`                | `D17_stale_cache_artifact`         | **bulk-resolve**             |
| `fixture_general`                   | `source_file` contains `/fixtures/`                | `D9_test_fixture_validation`       | **bulk-resolve**             |
| **anything else**                   | (no pattern match)                                 | —                                  | **manual review** — do NOT bulk-resolve |

Builder rule: **never bulk-resolve outside these patterns.** Manual review items are the actual signal — they're what the daemon caught that the producer-side fixes haven't covered yet. Investigate; fix the producer; only THEN resolve.

When a manual review item resolves to a real producer bug:

1. Open a new ticket (`TASK-CB-XXX-AUDIT-FIX-<short-name>`) in the AI builder ledger.
2. The fix lands on a feature branch, never touches the daemon's running state.
3. After merge, the daemon picks up the fix on next cycle (no daemon restart needed for adapter fixes; `live_pipeline.run_live_factory_cycle` re-imports each call).

---

## 6 — Per-cycle review checklist (copy-paste for fresh Builder)

```markdown
### Cycle review · <UTC>

- [ ] heartbeat freshness: <status> / age <Xs>
- [ ] audit queue depth: <N> unresolved (<H> high, <M> med, <L> low)
- [ ] provenance completeness: <P>%
- [ ] trace verification: <K>/<K> worlds OK
- [ ] records-per-cycle: <delta> (μ=<μ>, 2σ=<σ>; within band: yes/no)
- [ ] disk delta: +<bytes> (within per-cycle budget: yes/no)

### Verdict

- [ ] all green → log "clean check at <UTC>" and continue
- [ ] warn observed (no stop) → log warn + investigation note
- [ ] stop required → execute §3 graceful stop + §5 triage
```

After every cycle review, append the result to `BUILD_LOG.md` under the current date. Format:

```markdown
## YYYY-MM-DD HH:MM:SS EST — Daemon health check

Heartbeat: live (age 12s). Audit queue: 8 unresolved (0 high). Records-per-cycle: 47 (μ=44, within ±2σ). Disk delta: +18 MiB (under 256 MiB budget). All green.
```

A fresh Builder Claude reading this log can see at a glance whether the daemon is healthy without running checks again.
