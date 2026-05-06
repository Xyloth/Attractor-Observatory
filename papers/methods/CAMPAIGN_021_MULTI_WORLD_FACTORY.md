# Campaign 021 - Multi-World Factory Pilot

Task: TASK-033
Mode: exploratory
Claim promotion: closed pending C020 ontology/methodology repair

## Scope

Campaign 021 extends the autonomous Factory from the W-1/W0 floor into five
higher worlds:

- W1 CRN from KEGG E. coli K-12 MG1655 metabolic-network metadata
- W3 Field from peer-reviewed reaction-diffusion benchmark parameters
- W6 Ecosystem from GBIF occurrence-count summaries around the Jornada Basin
  LTER vicinity
- W9 Origins Chemistry from peer-reviewed prebiotic chemistry benchmarks
- W11 Quasispecies from NCBI HIV-1 HXB2 reference sequence metadata plus
  peer-reviewed mutation-rate metadata

The Campaign 016 low-level runner is left unchanged. TASK-033 adds a separate
multi-world runner so older W-1/W0 reports do not silently change.

## Source discipline

All runtime ingestion remains daemon code. AI is not used in the ingestion
path. Each adapter emits `EmpiricalRecord` rows with source URL, retrieval
timestamp, parser version through `SourceCacheEntry`, authority, license class,
and raw-export policy.

Live network fetches are supported where the source offers a stable endpoint.
Offline verification uses bundled authoritative seeds with source provenance.
Bundled seeds are compact derived summaries, not redistributed raw corpora.

## Routing and rejection

`factory_lowlevel/router.py` now validates target-world fit before simulation.
For W1/W3/W6/W9/W11, records must carry deterministic `world_parameters`.
Underdetermined records are rejected and surfaced as audit items rather than
filled with plausible defaults.

## World construction

Each wired world exposes `from_empirical_records()`:

- `CRNWorld.from_empirical_records()`
- `FieldWorld.from_empirical_records()`
- `OriginsChemistryWorld.from_empirical_records()`
- `QuasispeciesWorld.from_empirical_records()`

The constructors accept only structurally matching records and return
rejections for nonmatching or underdetermined input.

## Live console

Room 9, Factory Intake Dock, now renders:

- target-world selector
- source-adapter selector
- fixed source-bound parameter inputs for the pilot sources
- FIRE button backed by `factory_lowlevel.daemon.run_multi_world_factory_cycle`
- live stage state from `control_room/cache/factory_runs/latest_state.json`
- life-form trace rows from `latest_run.json`
- per-trace drilldown into lens evaluations
- per-world motif fire rates
- run history from the Factory session ledger

Honest absence is preserved under D22. Empty motif fires render as no-fire
results, not as failure-to-fill UI.

## Verification command

```
python make_campaign_021.py
pytest public_tests/test_task033_multiworld_factory.py
```

## Disclosure

The formal lens registry currently contains six draft motifs. TASK-033 reports
those six. It does not fabricate additional motif IDs to satisfy older UI copy
that referred to eight motifs.

The C020 methodology leak remains out of scope. All outputs stay
`mode_tag: exploratory`.
