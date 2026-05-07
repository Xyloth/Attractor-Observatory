# Builder Launch Protocol — daily monitoring routine

**Audience:** any Builder Claude session (fresh or continuing) supervising the unattended Factory daemon during mass ingestion.

**Mode:** read this once at session start. Loop steps 1–6 each monitoring pass. End-of-session: log to BUILD_LOG.

**Companion docs:**

* `BUILDER_INGESTION_MONITORING_PLAYBOOK.md` — thresholds, stop/resume, triage rules
* `papers/methods/INGESTION_TARGETS.md` — per-world target density (PI-ratified)
* `scripts/SETUP_WORKTREE.md` — fresh-worktree setup (run once per worktree)
* `factory_lowlevel/launch_safety.py` — lock + signals + atomic checkpoint + resume verification

---

## Daily routine

### Step 1 — Check heartbeat + per-world progress

```python
from control_room.factory_heartbeat import read_factory_heartbeat
from factory_lowlevel.progress import read_ingestion_progress

hb = read_factory_heartbeat()
progress = read_ingestion_progress()

# Report:
print(f"daemon: {hb['status']}, age {hb.get('age_seconds','?')}s")
for world, p in sorted(progress.items()):
    pct = round(p['percent_complete'] * 100, 1)
    print(f"  {world}: {p['current_density']}/{p['target_density']} ({pct}%) — last_clean: {p['last_clean_cycle'] or 'pending'}")
```

Apply playbook §1.1 (heartbeat) thresholds. Apply §1.2 (audit queue depth) next.

### Step 2 — Triage audit queue

```python
from control_room.rooms.factory_intake_dock import _audit_inbox_summary, _compute_bulk_resolve_buckets

s = _audit_inbox_summary()
buckets = _compute_bulk_resolve_buckets(s["unresolved"])
total_routine = sum(b["count"] for b in buckets.values())
manual = s["unresolved_total"] - total_routine
print(f"audit: {s['unresolved_total']} unresolved / {total_routine} routine / {manual} manual")
```

Per playbook §5: bulk-resolve the 5 recognized buckets via the Audit Inbox UI's per-bucket button (or programmatically via `_audit_resolution_write`). **Never bulk-resolve outside the 5 patterns.** Manual items get individual treatment.

If `manual ≥ 10`: bring the daemon to a graceful stop (playbook §3) and triage offline. Manual items are the actual signal.

### Step 3 — Spot-check recent records

```python
from factory_lowlevel.index import IndexReader
reader = IndexReader()  # opens control_room/cache/index/factory_records.parquet
recent = reader.query_recent(hours=1)
print(f"last hour: {len(recent)} records ingested")

# Provenance completeness on the last 50:
required = {"source_url", "retrieval_timestamp", "parser_version"}
for r in recent[:50]:
    # IndexReader rows already include retrieval_timestamp + parser_version.
    if not r.get("retrieval_timestamp") or not r.get("parser_version"):
        print(f"  INCOMPLETE: {r['record_id']}")
```

Apply playbook §1.3 (provenance completeness ≥ 99 % pass / < 95 % stop).

### Step 4 — If any threshold hit → execute stop

Per playbook §3 graceful (SIGINT) preferred. Watch for:

* `status: stop_requested_after_current_cycle` heartbeat (in flight)
* `status: clean_shutdown` heartbeat (final)
* lock file removed (`<store>/.daemon_lock` absent)

If hard stop required, send SIGTERM and run `check_factory_store_integrity` before any resume. Surface integrity failures via `BUILD_LOG.md` + a new `TASK-CB-XXX` ticket.

### Step 5 — If thresholds clean → log "clean check"

```markdown
## YYYY-MM-DD HH:MM:SS EST — Daemon health check

Heartbeat: live (age 12s). Audit: 8 unresolved (0 high). Records last hour: 47 (μ=44, ±2σ). Provenance: 99.6% complete. Disk: +18 MiB (under 256 MiB cycle budget). **All green.**
```

Append to `BUILD_LOG.md` under today's date.

### Step 6 — End-of-session BUILD_LOG entry

At the end of a monitoring session, write a summary entry:

```markdown
## YYYY-MM-DD HH:MM:SS EST — Builder monitoring session N closed

Cycles observed: N. World progress at session end:
- W-1: 1394/1500 (93%)
- W1 crn: 12/50 (24%)
- ... (one row per world)

Audit triage: <total resolved> bulk-resolved (NIST=10, fixtures=20, ...);
<remaining> manual items routed to TASK-CB-XXX.

No stop signals issued. Daemon remained green throughout.
```

Or, if a stop was issued:

```markdown
## YYYY-MM-DD HH:MM:SS EST — Builder monitoring session N STOPPED

Stop reason: <which threshold tripped>. Daemon at status `clean_shutdown`
after cycle <N>. Integrity check: <ok / failed with rationale>.
Resume blocked pending: <ticket / fix>. Tracking under TASK-CB-XXX.
```

---

## Reference card — what to read in what order

When a fresh Builder Claude takes over monitoring mid-stream, read these four artifacts (in this order) before doing anything else:

1. `control_room/cache/factory_daemon_heartbeat.json` — current daemon state
2. `reports/factory_daemon_progress/*.json` — per-world progress
3. `BUILD_LOG.md` (last ~10 entries) — what the previous Builder observed
4. `BUILDER_INGESTION_MONITORING_PLAYBOOK.md` (this directory) — thresholds

That's the entire state needed to make a stop / continue / resume decision. Everything else is escalation context.

---

## Failure-mode quick reference

| Symptom                                                    | Where to look                                       | Likely action                          |
|------------------------------------------------------------|-----------------------------------------------------|----------------------------------------|
| Heartbeat absent                                           | `control_room/cache/factory_daemon_heartbeat.json`  | daemon crashed; check stderr.log       |
| Heartbeat stale > 15 min                                   | per playbook §1.1                                   | hard stop; investigate                 |
| `status: resume_aborted`                                   | `factory_lowlevel.launch_safety:check_factory_store_integrity` | manual integrity audit         |
| `status: start_refused_lock_held`                          | `<store>/.daemon_lock`                              | check holder PID alive; clear if not   |
| Audit queue ≥ 100                                          | playbook §5                                         | graceful stop + triage manual items    |
| Provenance < 95 %                                          | inspect failing records via IndexReader             | producer-side bug; fix adapter         |
| Trace verification failure                                 | `factory_lowlevel.persistence.verify_world_traces`  | producer-side bug; fix world model     |
| Disk delta > cycle budget                                  | playbook §1.6                                       | run `BudgetEnforcer.evict_lru` or raise cap |
| Daemon refusing to start (formalism missing)               | `factory_daemon.bat` fail-fast output               | run `scripts/setup_worktree.bat`       |

---

## Doctrine bindings active during monitoring

* **D7** — substance floors per world; targets in `INGESTION_TARGETS.md`
* **D9** — fail closed on doubt; never silently overwrite a possibly-corrupt store
* **D11** — verification gates pass before resume after a stop
* **D14** — never fabricate values; honest absence in heartbeat / progress
* **D17** — stale data flagged stale (heartbeat staleness, audit cache staleness)
* **D19** — every record carries source-bound provenance
* **D22** — empty rooms over mock data; no fake "all green" when checks haven't run
* **D24** — heartbeat freshness recomputed at read time
* **D26** — methodology_review_required surfaced honestly
* **D29** — private modules (formalism/worlds/trace) marked private; not exfiltrated
* **D31** — floor BFG read-separation enforced

When a doctrine fires during monitoring (e.g., D17 stale_cache flag), record which doctrine triggered the action in the BUILD_LOG entry. The audit trail compounds — future Builders learn the patterns.
