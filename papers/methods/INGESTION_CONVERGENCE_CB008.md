# Ingestion Convergence Loop — CB-008 Methods

**Task ID:** TASK-CB-008
**Class:** ingestion_convergence_self_paced
**Branch:** `feature/cb-008-ingestion-convergence`
**Builder:** Claude (Builder), claude-sonnet-4.7-20260501
**Start EST:** 2026-05-06 05:46:44
**Stop EST:** 2026-05-06 (see `reports/campaign_022/convergence_session.json`)
**Timer cap:** 60 minutes
**Outcome:** **CONVERGED** — three consecutive clean cycles with no fixes needed.

## What this method does

Pressure-tests the live Factory ingestion pipeline (`factory_lowlevel/`)
against the seven-component cleanliness contract from the CB-008 brief:

1. Empirical records — full provenance (source_url, retrieval_timestamp,
   parser_version, license_class, authority).
2. Normalized references — ontology axes populated where the world
   model needs them (process_roles / interaction_channels /
   state_space_effects / overlap_fields).
3. Evidence graph — no orphan edges; every edge's `evidence_record_ids`
   resolve to known records.
4. World traces — every routed world_family produces a trace file with
   a recompute-able `trace_content_hash`.
5. Audit queue — every item has `reason` + `recommended_action`; no
   silent drops.
6. Motif evaluations — out of CB-008 scope (separate stage).
7. Idempotence — record_ids / normalized_ids / edge_ids / trace_ids
   stable across reruns.

## How the loop works

```
loop:
    cycle = run_factory_cycle(allow_network=True)
    audit = audit_seven_components(cycle.store)
    if audit.all_pass:
        clean_streak += 1
        if clean_streak >= 3:
            break
    else:
        fix_producer_side(audit.failures)   # adapter / persistence / pipeline
        wipe_contaminated_store(reason=...) # log every deletion
        clean_streak = 0
report(cycles_run, fixes_shipped, garbage_deleted, final_audit)
```

The contract is producer-side: when output is malformed, the **adapter**
or **persistence** layer is wrong, never the audit. We never patch the
Factory to accept malformed data and we never engineer the audit to
pass on contaminated input (D9 / D14 / D17 binding).

## Bug catalog (cycle 1 audit findings)

### Bug A — PubChem SMILES schema drift (CRITICAL)

**Symptom:** 5/5 PubChem records had `payload.canonical_smiles == ""`;
`bond_topology_proxy` was all zeros; downstream normalized
references had `predicate.observed = ""` for the SMILES gate. This is
the "PubChem topology bug pattern" the brief explicitly named.

**Root cause:** PubChem PUG-REST renamed `CanonicalSMILES` →
`SMILES` and `IsomericSMILES` → `SMILES` around 2024-2025; the
canonical-without-stereo form moved to `ConnectivitySMILES`. The
adapter still requested the deprecated property names AND read the
deprecated keys from the response, so live fetches returned no SMILES
field and the parser produced empty strings.

**Fix:** `factory_lowlevel/adapters.py`
- `PubChemSmallMoleculeAdapter._query_url`: request
  `MolecularFormula,SMILES,ConnectivitySMILES,MolecularWeight,HeavyAtomCount,Complexity`.
- `PubChemSmallMoleculeAdapter._record_from_row`: read `SMILES` first,
  then `ConnectivitySMILES`, then fall back to legacy
  `CanonicalSMILES` / `IsomericSMILES` for any pre-migration cached
  responses still on disk.

### Bug B — Provenance schema mismatch (HIGH)

**Symptom:** 16/16 records used `provenance.retrieved_at` instead of
the brief-mandated `provenance.retrieval_timestamp`. `parser_version`
was absent from `provenance` entirely (only carried on the cache
entry, which downstream consumers don't see per record).

**Root cause:** Adapters were written against an earlier schema that
predates the CB-008 contract.

**Fix:** `factory_lowlevel/adapters.py` — three `provenance` dicts
(NIST atomic, math primitives, PubChem) now include both
`retrieval_timestamp` (canonical) and `retrieved_at` (legacy alias,
retained for back-compat) plus `parser_version`. The legacy alias
prevents quietly breaking anything that already reads `retrieved_at`.

### Bug C — Silent acceptance of empty critical fields (HIGH)

**Symptom:** With Bug A in place, 5 PubChem records persisted with
empty SMILES → empty topology proxy → meaningless normalized
references. The audit queue had 0 items. This is the canonical D9
violation pattern: garbage data masquerading as complete records.

**Root cause:** No post-parse validation in the adapter; no audit
ingestion path in the persistence layer; no audit wiring in the
pipeline.

**Fix (three layers):**
1. `factory_lowlevel/adapters.py`: new `AdapterAudit` dataclass and
   `AdapterResult.audits` field. PubChem adapter post-validates each
   record after parse; emits an `AdapterAudit` with severity `high`
   and reason `pubchem_smiles_empty_after_parse` when SMILES survives
   empty.
2. `factory_lowlevel/persistence.py`: new
   `LowLevelFactoryStore.ingest_adapter_audits` method converts each
   `AdapterAudit` into a real `AuditQueueItem` with the required
   `reason` + `recommended_action`.
3. `factory_lowlevel/pipeline.py`: pipeline now passes
   `result.audits` into the store so adapter-level honest negatives
   land in the persisted audit queue.

This makes the bug **publishable as an honest negative (D17)** rather
than silently accepted as data.

### Bug E — Routed records produced no trace files (HIGH)

**Symptom:** The CB-008 brief explicitly required "100% of routed
records produced verified traces (content_hash matches)." Cycle 1
produced **zero traces** because `route_records()` returned
`RoutedWorldBundle` objects in-memory only and the pipeline never
persisted them.

**Fix:** `factory_lowlevel/persistence.py`
- New `LowLevelFactoryStore.world_traces` dict and
  `ingest_world_traces` method. Each routed bundle becomes a
  `LowLevelWorldTrace.v1` record with:
  - `trace_id` — sha256 of `{world, body, salt}`
  - `trace_content_hash` — sha256 of canonical `body` JSON
  - `body` — sorted record_ids + normalized_ref_ids + counts +
    run_id_seed
  - `verifier` — predicate `sha256_of_canonical_json(body) ==
    trace_content_hash` marked `trace_checkable: true` and
    `deterministic: true`.
- New top-level `verify_world_traces(store_root)` function that
  re-derives every trace's content_hash from its persisted body and
  compares. Returns `{present, verified: {family: bool}, all_pass}`.
- `LowLevelFactoryStore.write` now persists `world_traces.json` and
  includes `world_traces` in the snapshot counts.
- `factory_lowlevel/pipeline.py`: pipeline now calls
  `store.ingest_world_traces(routed, run_id_seed=store.content_hash())`
  after the evidence graph is rebuilt and before the snapshot is
  written. Run-id-seed binding makes trace IDs reproducible.

## Garbage deleted (cycle 1 → cycle 2 wipe)

| Category               | Count | Files                       | Reason for total wipe                              |
|------------------------|-------|-----------------------------|----------------------------------------------------|
| baseline records       |    16 | empirical_records.json      | Bug A + Bug B touched ALL records                  |
| baseline normalized    |    16 | normalized_refs.json        | derived from contaminated records                  |
| baseline edges         |    19 | evidence_graph.json         | derived from contaminated normalized refs          |
| baseline cache index   |     3 | source_cache_index.json     | inconsistent with new parser_version contract       |
| baseline snapshot      |     1 | snapshot.json               | content_hash referenced contaminated payloads      |

A partial purge would have left inconsistent provenance dicts and
stale empty-SMILES records side-by-side with fresh ones; a clean
rebuild was the correct call. The wipe is logged in
`reports/campaign_022/convergence_wipe_log.jsonl` with timestamp,
counts, and reason.

## Per-cycle log

| Cycle | Trigger          | Records | Refs | Edges | Audit | Traces | Outcome                         |
|-------|------------------|--------:|-----:|------:|------:|-------:|---------------------------------|
|   1   | cb008_baseline   |    16   |   16 |   19  |    0  |    0   | FAIL — 4 bugs found             |
|   2   | cb008_cycle_2    |    16   |   16 |   19  |    0  |    2   | PASS (first clean after fixes)  |
|   3   | cb008_cycle_3    |    16   |   16 |   19  |    0  |    2   | PASS — no fixes needed          |
|   4   | cb008_cycle_4    |    16   |   16 |   19  |    0  |    2   | PASS — fully idempotent         |

Cycle 4's `idempotent_duplicate_run_id` was True (cycles 3 and 4 ran
within the same wall-clock second; `utc_now()` is second-precision so
the snapshot content_hash matched).

## Final audit

| Component                          | Status                          |
|------------------------------------|---------------------------------|
| 1. empirical records               | PASS — 16 records, 0 prov fails |
| 2. normalized references           | PASS — 0 all-empty refs         |
| 3. evidence graph                  | PASS — 0 orphan evidence ids    |
| 4. world traces                    | PASS — 2/2 verify; 0 missing    |
| 5. audit queue                     | PASS — 0 items, none silent     |
| 6. motif evaluations               | N/A (separate stage)            |
| 7. idempotence                     | PASS — 0 dup ids of any kind    |

## Tests

`tests/test_factory_lowlevel_cb008.py` — 8 deterministic-seed tests
pass in 0.18 s. Coverage:

- Bug A — `test_pubchem_reads_live_smiles_property_name`
- Bug A backward-compat — `test_pubchem_falls_back_to_legacy_smiles_keys`
- Bug B — `test_provenance_carries_retrieval_timestamp_and_parser_version_all_adapters`
- Bug C — `test_pubchem_audit_fires_when_smiles_empty`
- Bug C — `test_pubchem_audit_silent_when_smiles_populated`
- Bug E — `test_world_traces_persist_and_verify`
- Bug E — `test_world_traces_have_recomputable_content_hash`
- Idempotence — `test_pipeline_idempotent_record_ids_on_rerun`

All tests use `allow_network=False` and inject deterministic seed
JSON into the cache directory (per the CB-008 forbidden-pattern rule
"Network calls in tests").

## Brief discrepancies (open questions for Architect)

1. **Snapshot hash drift across cycles.** `LowLevelFactoryStore.write`
   computes `snapshot.content_hash` over all persisted payloads,
   including provenance dicts whose `retrieval_timestamp` refreshes
   per cycle. Result: identical input produces drifting snapshot
   hashes when cycles run in different wall-clock seconds. Record
   IDs / normalized IDs / edge IDs / trace IDs are stable, so the
   brief's idempotence criterion ("No duplicate IDs across runs")
   holds. Should the snapshot hash explicitly exclude
   `retrieval_timestamp` so the digest is fully content-addressable
   independent of clock?

2. **`live_pipeline.py` referenced but does not exist.** The brief
   said to use `live_pipeline.run_live_factory_cycle()`. On
   `codex/task-033-multi-world-factory` only `factory_lowlevel.daemon
   .run_factory_cycle()` and `factory_lowlevel.pipeline
   .run_low_level_factory()` exist. Was `live_pipeline.py` a planned
   surface that hasn't been merged yet, or should it have been
   created as part of this task?

3. **`reports/campaign_021/factory_store/` referenced but does not
   exist.** The daemon defaults to
   `reports/campaign_016/daemon_store/`. Are 017–021 future campaigns
   not yet started on this branch?

4. **`worlds/*/model.py` `from_empirical_records()` does not exist.**
   The brief mentions fixing world adapters when records aren't
   routing into worlds correctly. The world model layer hasn't been
   created here, so the "world model rejections" sub-component of
   the audit could not be exercised.

## Doctrine binding

D7 — measured against contracted output, not engineered to pass.
D9 — no engineered passes; bugs were producer-side, not test-side.
D14 — no fabricated values; SMILES come from the live API, not
synthesized.
D17 — empty-SMILES post-parse is published as an honest negative via
the new `AdapterAudit` path, not silently dropped.
D19 — every record carries source-bound provenance with both
`retrieval_timestamp` and `parser_version`.
D22 — when an adapter declines to populate a field (returns ""), the
audit queue declares the absence rather than papering over it.
