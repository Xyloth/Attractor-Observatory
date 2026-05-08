# DX-003 Round 8 - Daemon State And Progress Cache Collision

round_id: 8
attack_angle: I attacked runtime liveness truth rather than static reports: daemon state, force-refresh records, due-source selection, and per-world ingestion progress files. The hypothesis was that the project could truthfully record a daemon control action while leaving operator-facing progress surfaces stale enough to imply ingestion is complete or clean when the next cycle would actually rerun everything.
elapsed_at_round_start: approximately 00:38:46 after T_start
elapsed_at_round_end: 00:40:56.9604478 after T_start

## Surfaces Examined

- `project_telemetry/factory_daemon_state.json`
- `project_telemetry/factory_daemon_sessions.jsonl`
- `project_telemetry/low_level_factory_sessions.jsonl`
- `reports/factory_daemon_progress/*.json`
- `factory_lowlevel/continuous_daemon.py`
- `factory_lowlevel/progress.py`

## Findings

### R8-F1 - Broken - Force-Refresh Clears Daemon State But Leaves Progress Files Saying Sources Are Complete

severity: amber
claim: The latest daemon control record is a `force_refresh_clearance` at `2026-05-08T12:23:10Z` that clears the daemon's `last_success_by_source` state. The state file now has zero successful sources. But all 15 per-world progress files were written earlier (`2026-05-07T16:26:09Z` or `2026-05-07T17:14:50Z`) and still list completed sources with empty `sources_pending`. An operator reading `reports/factory_daemon_progress/*.json` after the force-refresh sees stale completion state, while the daemon itself has forgotten those completions.

reproducer:

```powershell
python papers\falsification\DX-003\round_8_reproducers\daemon_state_progress_probe.py
Get-Content papers\falsification\DX-003\round_8_reproducers\daemon_state_progress_probe.txt
```

expected output includes:

```text
state_last_success_count=0
progress_file_count=15
progress_completed_sources=[...15 source IDs...]
progress_pending_sources=[]
progress_files_with_completed_sources_after_force_clear_count=15
last_force_refresh_clearance={"clear_all": true, "cleared_at": "2026-05-08T12:23:10Z", ...}
```

mistake_class mapping: runtime-state/progress-cache drift; honest-failure honesty.
doctrine_refs: D9, D24/D30 freshness discipline by analogy, D17.
suggested_triage: technical_repair. Force-refresh should either invalidate progress files, rewrite them as stale/degraded, or cause progress readers to compare against daemon state before displaying completion.

### R8-F2 - Fake-Passed - Progress Says No Pending Sources While Due-Source Selection Says All 17 Are Due

severity: amber
claim: With `last_success_by_source` empty, `_due_sources()` marks all 17 available source adapters due. The progress files still report no pending sources. Both views are internally derived from project artifacts, but they answer the same operational question differently.

reproducer:

```powershell
Get-Content papers\falsification\DX-003\round_8_reproducers\due_sources_after_force_clear.txt
Get-Content papers\falsification\DX-003\round_8_reproducers\daemon_state_progress_probe.txt
```

expected output includes `due_source_count=17` and `progress_pending_sources=[]`.

mistake_class mapping: fake-green / stale-cache as success.
doctrine_refs: D24, D30, D9.
suggested_triage: technical_repair. Treat progress files as advisory snapshots with freshness binding or compute pending sources live from `factory_daemon_state.json`.

### R8-F3 - Ambiguous - Progress Audit Queue Values Are Mixed Across Old Sessions

severity: yellow
claim: The progress files contain `audit_queue_at_last_check` values `[0, 109]` from different old sessions. The latest session ledger row is a force-refresh record, not a completed cycle, so there is no single current audit-queue truth attached to the cleared state. This is not a direct failure of the daemon, but it makes the operator-facing progress surface ambiguous after a control action.

reproducer:

```powershell
Get-Content papers\falsification\DX-003\round_8_reproducers\daemon_state_progress_probe.txt
```

expected output includes `progress_audit_queue_values=[0, 109]` and a latest force-refresh clearance later than all progress `written_at` values.

mistake_class mapping: UI/runtime truthfulness; stale health signal.
doctrine_refs: D9, D24/D30 by analogy.
suggested_triage: architectural_discussion. Decide whether progress files are historical snapshots or current dashboard state; then encode that distinction in schema.

### R8-F4 - Instrument Held - Due-Source Selection Correctly Honors The Cleared Daemon State

severity: informational
claim: The daemon's due-source function itself behaves consistently with the cleared `factory_daemon_state.json`: all available adapters become due. The broken surface is not source selection; it is stale progress materialization.

reproducer:

```powershell
Get-Content papers\falsification\DX-003\round_8_reproducers\due_sources_after_force_clear.txt
```

expected output includes `available_source_count=17` and `due_source_count=17`.

mistake_class mapping: via-negativa survived sub-attack.
doctrine_refs: D17.
suggested_triage: acceptable for due-source logic.

## Hypotheses

- Any Control Room or monitoring script that reads `reports/factory_daemon_progress/*.json` without checking `factory_daemon_state.json` can display stale completion after force-refresh.
- The daemon session ledger needs a post-control-action status class: `state_cleared_pending_next_cycle`, distinct from `complete` and from old progress snapshots.
- Progress schema should carry `freshness_status`, `generation_binding`, and `source_state_hash` the same way Control Room snapshots now do under D30.

## Reproducer Artifacts

- `round_8_reproducers/daemon_state_progress_probe.py`
- `round_8_reproducers/daemon_state_progress_probe.json`
- `round_8_reproducers/daemon_state_progress_probe.txt`
- `round_8_reproducers/due_sources_after_force_clear.txt`
