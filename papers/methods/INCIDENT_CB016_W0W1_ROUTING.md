# INCIDENT — CB-016 — W0 / W1 Router Schema Mismatch

**Status:** OPEN, surfaced for separate ticket. Records persist
clean; routing-stage rejection prevents simulation only. D17 honest
non-evidence behavior preserved.

## Summary

After CB-016 persistence load-on-init fix, the cache replay
recovered all four CB-015 sources' records into a single coherent
`factory_store/empirical_records.json` (4,378 records across W-1 +
W0 + W1). All records carry full provenance (D19) and
`methodology_review_required=true` (D26).

**Both W0 (math_primitives) and W1 (CRN) routers reject the
adapters' canonical payload schema** during the routing stage of
`run_live_factory_cycle`:

* **W0 math_primitives**: 200 records emitted by
  `MathPrimitivesCatalogAdapter` carry `state_equation`,
  `parameters`, `expected_stable_form`, and 7 other catalog fields.
  The W0 router (or `MathPrimitivesWorld.from_empirical_records`)
  rejects them — exact reason TBD (the records reach
  `empirical_records.json` but don't progress to trace simulation).
* **W1 crn**: 50 records emitted by `KEGGOrganismCRNAdapter` carry
  `reactions`, `initial_state`, and `species_count` nested under
  `payload.world_parameters`. The W1 router rejects them with
  `crn_requires_initial_state_and_reactions` because it checks
  top-level keys, not the nested form.

## Audit-queue evidence

Post-replay audit_queue contains 50 entries:

```
50  routing_rejection:crn_requires_initial_state_and_reactions
```

(Math primitives' rejections may emit at a different stage and not
land in `audit_queue.json`; investigation pending.)

## Records persist with full provenance

Per D9 / D17 / D19 / D26 the rejection-stage records are NOT
discarded — they're stored with full source-bound provenance and
`methodology_review_required=true`. They simply don't drive
simulation traces until the schema reconciliation lands.

| World | Records persisted | Drives simulation? |
|-------|------------------:|--------------------|
| W0 math_primitives | 200 / 200 (100% of Phase-1 target) | NO — router rejects |
| W1 crn (KEGG) | 50 / 50 (100% of Phase-1 target) | NO — router rejects |

Phase-1 ingestion target hit on both worlds; the simulation chain
is downstream of routing and waits on the schema fix.

## Fix path (separate ticket — Codex's lane)

This is **producer-side schema reconciliation between adapter
output and router input**. Two equivalent options; pick whichever
is closer to canonical:

**Option A — extend routers to accept nested payloads** (lower-risk;
adapters stay as-is):

```python
# W1 CRN router: read from nested location if top-level missing.
def _extract_initial_state_and_reactions(record):
    payload = record.payload
    if "initial_state" in payload and "reactions" in payload:
        return payload["initial_state"], payload["reactions"]
    if "world_parameters" in payload:
        wp = payload["world_parameters"]
        if "initial_state" in wp and "reactions" in wp:
            return wp["initial_state"], wp["reactions"]
    return None  # routing rejection
```

**Option B — lift adapters' nested payloads to top-level**
(canonicalizes one router contract; risks back-compat with prior
adapter outputs):

```python
# In KEGGOrganismCRNAdapter, return payload with initial_state +
# reactions at top-level alongside the existing nested
# world_parameters block.
```

Math primitives' router needs analogous reconciliation;
investigation needs to determine which fields the W0 router checks
vs which fields `MathPrimitivesCatalogAdapter` emits.

## Forbidden in CB-016

The CB-016 brief explicitly excludes:

> Touching adapter code (CB-015 + Codex Phase B both ship adapters;
> this ticket fixes persistence only).
> Touching router code (W0/W1 schema mismatch — separate ticket).

So this incident is **documented, not fixed**, in CB-016. Recommend:

* **TASK-CB-017** (or Codex equivalent) — schema reconciliation
  between adapter output and router input, with explicit canonical
  contract for which keys live where in `EmpiricalRecord.payload`.
* Until that ticket lands: 250 records (200 math + 50 KEGG) persist
  with full provenance but don't drive simulation. Honest state.

## Doctrine binding

* D9 — surface, don't paper over: this incident doc + the
  audit-queue entries do that.
* D14 — no fabricated routing: records reach the store as-fetched.
* D17 — honest non-evidence: routing-rejection records still
  persist with `methodology_review_required=true`.
* D19 — full provenance: 4,378 / 4,378 records carry
  `source_url`, `retrieval_timestamp`, `parser_version`,
  `authority`, `raw_exported`.
* D22 — empty over fake: simulation surfaces (motif fires,
  trace tables) for W0/W1 stay empty until the schema fix lands;
  no fabricated lens evaluations to paper over the gap.
