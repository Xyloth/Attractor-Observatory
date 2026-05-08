# DX-003 Round 7 - Identity And Telemetry Accounting Collision

round_id: 7
attack_angle: I attacked the project's self-accounting layer: the Estimation Loop ledger, README claims about builder identities and task counts, the public telemetry contract test, BUILD_LOG mention coverage, and the Control Room AI Operations Tower. The question was whether the project can honestly answer who did what and how many calibrated task records exist, because calibration claims are part of the project's research surface, not bookkeeping trivia.
elapsed_at_round_start: approximately 00:33:38 after T_start
elapsed_at_round_end: 00:38:22.6024215 after T_start

## Surfaces Examined

- `project_telemetry/ai_builder_tasks.jsonl`
- `README.md`
- `public_tests/test_public_contracts.py`
- `control_room/adapters/builder_telemetry.py`
- `control_room/rooms/ai_operations_tower.py`
- `BUILD_LOG.md`
- `project_telemetry/TIME_CALIBRATION_REPORT.md`

## Findings

### R7-F1 - Broken - README's Estimation Ledger Counts Are Stale By 30 Tasks

severity: amber
claim: `README.md` claims the Estimation Loop ledger spans 34 tasks across three builders, with Codex 1.5x at 1 task and Claude Builder at 7 sequential UI tasks. A direct parse of `project_telemetry/ai_builder_tasks.jsonl` finds 112 rows and 64 unique `task_id` values. Using the last row per task as the current model identity, the ledger contains 30 Codex tasks, 19 Codex 1.5x tasks, and 15 Claude Builder tasks. The README is not a small stale badge; it is wrong about the dataset behind a public research claim.

reproducer:

```powershell
python papers\falsification\DX-003\round_7_reproducers\telemetry_identity_probe.py
Get-Content papers\falsification\DX-003\round_7_reproducers\telemetry_identity_probe.txt
```

expected output includes:

```text
ledger_rows=112
unique_task_count=64
task_counts_by_last_model={'Codex': 30, 'Claude (Builder)': 15, 'Codex 1.5x': 19}
readme_claims=[... 'ledger spans **34 tasks across three distinct AI builders**' ... 'Codex 1.5x** (1 task' ... 'Claude Builder** (7 sequential UI tasks' ...]
```

mistake_class mapping: documentation drift / identity accounting drift.
doctrine_refs: D9 honest reporting; D17 publishable negative record; README's own identity-bounded calibration claim.
suggested_triage: technical_repair. README task-count claims should be generated from the ledger or removed.

### R7-F2 - Fake-Passed - Public Telemetry Test Passes While Missing The Claimed Ledger Contract

severity: amber
claim: The public telemetry test passes, but it only checks `task_record_id` uniqueness, `task_id`, `record_type`, and `model_name` on estimate/actual_update rows. It does not check README count claims, does not enforce the README's claimed per-task fields, and does not fail on 17 rows missing `task_class`. The test proves the JSONL is parseable and minimally identified; it does not prove the public Estimation Loop claims are true.

reproducer:

```powershell
python -m pytest -q public_tests/test_public_contracts.py::test_telemetry_records_have_identity_and_one_active_estimate_per_task
Get-Content papers\falsification\DX-003\round_7_reproducers\telemetry_identity_probe.txt
```

expected output includes `1 passed in 0.03s` and `missing_required_count=17`.

mistake_class mapping: fake-green / test proves too little.
doctrine_refs: D9, D17, D25 public verification truthfulness.
suggested_triage: technical_repair. Add a public contract test comparing README-declared telemetry counts to the ledger or delete static counts.

### R7-F3 - Broken - AI Operations Tower Collapses Or Omits Codex 1.5x As A Top-Level Identity

severity: yellow
claim: `parse_builder_telemetry()` correctly exposes `by_model` keys for `Codex`, `Claude (Builder)`, and `Codex 1.5x`. The AI Operations Tower's top agent cards are hard-coded to `Claude Builder`, `Codex`, and `Architect Claude`. Codex 1.5x has 39 ledger rows but no top-level agent card, while Architect Claude gets a zero-task card. This contradicts the identity-bounded calibration doctrine: deployment configuration shifts are supposed to function as new identities, but the primary UI collapses/hides one of the active identities.

reproducer:

```powershell
Get-Content papers\falsification\DX-003\round_7_reproducers\ai_ops_agent_card_probe.txt
Select-String -Path control_room\rooms\ai_operations_tower.py -Pattern "Claude Builder|Codex|Architect Claude|Codex 1.5x" -Context 2,4
```

expected output includes:

```text
by_model_keys=Codex,Claude (Builder),Codex 1.5x
by_model[Codex 1.5x].record_task_count=39
codex_1_5x_agent_card_present=False
codex_agent_card_present=True
architect_claude_agent_card_present=True
```

mistake_class mapping: UI truthfulness / identity bleed.
doctrine_refs: README Estimation Loop identity-bounded claim; D9.
suggested_triage: technical_repair. Render agent cards dynamically from `by_model` or make the intentional grouping explicit.

### R7-F4 - Instrument Held - JSONL Ledger Parses And Minimal Public Identity Contract Passes

severity: informational
claim: The ledger is not corrupted at the JSONL layer. The probe found zero JSON parse errors, and the existing public identity test passes. The failure is higher-level semantic accounting, not file unreadability.

reproducer:

```powershell
Get-Content papers\falsification\DX-003\round_7_reproducers\telemetry_identity_probe.json
Get-Content papers\falsification\DX-003\round_7_reproducers\public_telemetry_contract_test.txt
```

mistake_class mapping: via-negativa survived sub-attack.
doctrine_refs: D17.
suggested_triage: acceptable as a survived substrate.

## Hypotheses

- `BUILD_LOG.md` may not be a complete join key for telemetry: the probe found 26 ledger task IDs not mentioned in BUILD_LOG by exact `TASK-*` token match. Some may be naming-shape artifacts, but the mismatch deserves a schema-aware reconciliation pass.
- `TIME_CALIBRATION_REPORT.md` is also stale (`Last updated: 2026-05-04` and task table ending at TASK-024) while README uses its claims as live framing.
- The AI Operations Tower's mistake catalog is frozen at Class 1-12 in code comments, while doctrine and README now talk about Class 13. That may be a separate UI-truthfulness finding if not covered by another room.

## Reproducer Artifacts

- `round_7_reproducers/telemetry_identity_probe.py`
- `round_7_reproducers/telemetry_identity_probe.json`
- `round_7_reproducers/telemetry_identity_probe.txt`
- `round_7_reproducers/telemetry_identity_probe_stdout.txt`
- `round_7_reproducers/public_telemetry_contract_test.txt`
- `round_7_reproducers/control_room_builder_telemetry_parse.txt`
- `round_7_reproducers/ai_operations_room_probe.txt`
- `round_7_reproducers/ai_ops_agent_card_probe.txt`
