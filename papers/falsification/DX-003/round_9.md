# DX-003 Round 9 - Doctrine And Mistake-Catalog Propagation Collision

round_id: 9
attack_angle: I attacked the governance propagation layer: the doctrine registry, README claims, Claude Builder initiation mistake catalog, Control Room doctrine displays, AI Operations Tower, and portfolio demo copy. The question was whether new doctrine/class ratifications propagate to the surfaces that teach future agents what failures exist.
elapsed_at_round_start: approximately 00:41:00 after T_start
elapsed_at_round_end: 00:42:47.3854622 after T_start

## Surfaces Examined

- `README.md`
- `CLAUDE_BUILDER_INITIATION.md`
- `docs/DOCTRINE.md`
- `docs/doctrine_registry.json`
- `docs/doctrine_d22.md`
- `docs/doctrine_d31.md`
- `control_room/rooms/ai_operations_tower.py`
- `control_room/rooms/doctrine_console.py`
- `control_room/rooms/portfolio_demo.py`
- `control_room/rooms/README.md`

## Findings

### R9-F1 - Broken - Mistake Catalog Claims Thirteen Ratified Classes, But The Canonical Initiation Catalog Skips Class 12

severity: amber
claim: `README.md` says the Mistake Catalog has thirteen ratified classes and points to `CLAUDE_BUILDER_INITIATION.md` section 4 as the worked example catalog. The initiation file has class headings for 1 through 11 and 13, but no `### Class 12` heading. Meanwhile `docs/doctrine_d22.md` still describes Class 12 as a candidate/watch-list item. The governance surface simultaneously presents Class 12 as candidate/missing and presents thirteen ratified classes as accumulated project fact.

reproducer:

```powershell
python papers\falsification\DX-003\round_9_reproducers\doctrine_catalog_drift_probe.py
Get-Content papers\falsification\DX-003\round_9_reproducers\doctrine_catalog_drift_probe.txt
```

expected output includes:

```text
claude_builder_initiation_class_count=12
claude_builder_initiation_class_ids=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13]
readme_mentions_class_13=True
```

secondary reproducer:

```powershell
Select-String -Path README.md,CLAUDE_BUILDER_INITIATION.md,docs\doctrine_d22.md -Pattern "13 ratified|Class 12|Class 13|mistake catalog" -Context 1,2
```

mistake_class mapping: governance/catalog drift.
doctrine_refs: D9 honest reporting; D17 via-negativa; D22 candidate status.
suggested_triage: architectural_discussion plus technical_repair. Either ratify/document Class 12 and make the count true, or state that there are 12 catalog headings plus one candidate watch class.

### R9-F2 - Broken - Control Room Doctrine Surfaces Are Frozen At Class 1-12 And D7-D22/D25 While README Says D7-D31 And Class 13

severity: amber
claim: `control_room/rooms/ai_operations_tower.py` and `control_room/rooms/doctrine_console.py` hard-code a Class 1-12 catalog and omit Class 13. The Doctrine Console markdown says `doctrine registry · D7 — D22`; `control_room/rooms/README.md` says Doctrine arc D7-D25; `portfolio_demo.py` still says D7-D22 and Class 1-12. The underlying doctrine registry has 26 entries through D31, but multiple Control Room surfaces teach older governance state.

reproducer:

```powershell
Get-Content papers\falsification\DX-003\round_9_reproducers\doctrine_catalog_drift_probe.txt
Select-String -Path control_room\rooms\ai_operations_tower.py,control_room\rooms\doctrine_console.py,control_room\rooms\README.md,control_room\rooms\portfolio_demo.py -Pattern "Class 1-12|class 1 — 12|D7-D22|D7-D25|D7 — D22|Class 13|D31" -CaseSensitive:$false -Context 1,2
```

expected output includes:

```text
ai_operations_catalog_count=12
ai_operations_catalog_ids=['1', ..., '12']
ai_operations_class_13_present=False
doctrine_console_catalog_count=12
doctrine_console_class_13_present=False
doctrine_registry_count=26
doctrine_registry_ids_tail=['D24', 'D25', 'D26', 'D27', 'D28', 'D29', 'D30', 'D31']
```

mistake_class mapping: UI truthfulness / doctrine propagation drift.
doctrine_refs: D25 public verification honesty; D30 read-time truth; D31 ratified doctrine.
suggested_triage: technical_repair. Doctrine and mistake-catalog displays should be generated from registry/catalog artifacts or marked as historical snapshots.

### R9-F3 - Instrument Held - Doctrine Registry Itself Includes D31

severity: informational
claim: The registry substrate is current enough to know about D31. The drift is in rendered/control-room surfaces and catalog prose, not in the doctrine registry JSON.

reproducer:

```powershell
Get-Content docs\doctrine_registry.json | Select-String -Pattern '"id": "D31"|"updated_by"'
```

expected output includes `"id": "D31"` and `"updated_by": "Codex 1.5x TASK-FLOOR-BFG"`.

mistake_class mapping: via-negativa survived sub-attack.
doctrine_refs: D17.
suggested_triage: acceptable for registry substrate.

## Hypotheses

- Any fresh Builder using Control Room instead of README/registry directly may miss Class 13 and D26-D31 doctrine pressure.
- The mistake catalog needs its own machine-readable registry, just like doctrine has `doctrine_registry.json`.
- Portfolio/demo surfaces should be treated as claim-bearing summaries if they are used for external review; otherwise stale governance claims will survive inside polished UI copy.

## Reproducer Artifacts

- `round_9_reproducers/doctrine_catalog_drift_probe.py`
- `round_9_reproducers/doctrine_catalog_drift_probe.json`
- `round_9_reproducers/doctrine_catalog_drift_probe.txt`
