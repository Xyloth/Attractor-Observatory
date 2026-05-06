# Factory End-State and Schema Discipline

*Architect document. Status: foundational discipline for the Research Ingestion Factory. Read by Factory Claude before Session 001; binding on all Factory operations.*

---

## 0. Why this document exists

The Factory's outputs become the substrate everything downstream depends on: Phase 6 biology grounding, L3 cross-substrate-overlap claims, the Periodic Table public artifact, future Densification reports across W6–W13. If today's schema choices are wrong, tomorrow's questions can't be answered without re-fetching, re-extracting, and re-auditing every source we've already processed. That cost compounds.

This document defines:

1. The **archive-before-extract** discipline that lets schemas evolve without re-fetching.
2. A schema-completeness audit identifying fields the current `BiologicalClaim` design is missing, with priority tiers.
3. The schema evolution policy (versioning, migrations, replay-from-cache).
4. Per-session quality gates from Session 001 through steady-state.
5. Failure recovery procedures when bugs are discovered after ingestion has scaled.
6. Quantitative end-state definitions for "Factory ready for Phase 6" and beyond.

The intent is excruciating detail. Future Architect-Claude sessions, Factory-Claude sessions, and Codex sessions all read this before doing work that touches the Factory.

---

## 1. The archive-before-extract discipline

### 1.1 The rule

> **No source record is processed by the Factory without first being cached locally with content hash, license metadata, and full raw form.** Re-extraction from cache produces deterministic results given the same extraction code version. Re-fetching the source is reserved for cache-invalidation events (source schema change, source URL change, source policy change), not for routine schema evolution.

### 1.2 The four-layer storage architecture

Factory data lives in four layers, each independently rebuildable from the layer below:

```
Layer 4 — Evidence Graph + Reports        (rebuildable from Layer 3)
              ↑
Layer 3 — Normalized References            (rebuildable from Layer 2)
              ↑
Layer 2 — BiologicalClaim records          (rebuildable from Layer 1)
              ↑
Layer 1 — Source Cache (raw + parsed)      (rebuildable only by re-fetch)
```

- **Layer 1 — Source Cache.** For every source record fetched: raw bytes (license-permitting; for restricted sources, structured-fields-only is preserved with a `restricted_raw_omitted: true` flag), parsed structured form, source identity, fetch timestamp, license class, content hash. Stored under `biology/evidence_ingestion/cache/` with content-addressed paths.
- **Layer 2 — BiologicalClaim records.** Extracted from Layer 1 by the structured extractor. Each claim cites its source-cache content hash. Multiple claims may extract from one cached source record. Schema-versioned.
- **Layer 3 — Normalized References.** Process-role / interaction-channel / state-space-effect / overlap-field references derived from Layer 2 by the normalizers. Rebuilt by re-running normalizers; no source touch.
- **Layer 4 — Evidence Graph + Reports.** Nodes, edges, WorldDensificationRecommendation reports, atlas surfaces. Rebuilt from Layer 3.

### 1.3 What this buys us

- **Schema evolution without re-fetch.** If Phase 6 reveals we need a `geographic_range` field on BiologicalClaim that wasn't there at extraction time, we re-extract from Layer 1 cache (cheap, local, fast) instead of re-fetching from ITIS (slow, network-dependent, source-may-have-changed).
- **Bug recovery without re-fetch.** Normalizer bug discovered in Session 50? Re-normalize from Layer 2 cache; no re-fetch.
- **Provenance integrity.** Every Layer 4 artifact's content hash chain leads back to a Layer 1 source content hash. Atlas exports declare the chain.
- **License compliance preservation.** Layer 1 carries license_class on every cached record; Layer 2's claims inherit; Layer 4's exports honor the closure.

### 1.4 Cache structure (concrete)

```
biology/evidence_ingestion/cache/
  README.md                                  # discipline summary
  index.jsonl                                # one line per cached record (source_id, content_hash, license_class, fetch_timestamp, layer1_path)
  itis/                                      # per-source subdirectory
    {content_hash[0:2]}/                    # content-addressed sharding
      {content_hash}/
        raw.{ext}                           # raw bytes if license permits
        parsed.json                         # parsed structured form (always present)
        manifest.json                       # source_id, fetch_timestamp, license_class, fetcher_version, source_url
        provenance.json                     # ContentHash chain back to fetch
  ncbi_taxonomy/                             # future
  pbdb/                                      # future
  ...
```

Cache hits are content-hash-addressable. Cache misses (i.e., a source record we haven't fetched yet) trigger a fetch under D19 license enforcement. Cache invalidation (source URL changed, source schema changed, license changed) is a Codex task (re-fetch with new fetcher version), not a Factory Claude task.

### 1.5 Cache integrity invariants (CI-checkable)

- Every Layer 2 BiologicalClaim cites a Layer 1 cache content hash that exists.
- Every Layer 3 normalization cites a Layer 2 claim that exists.
- Every Layer 4 artifact's provenance chain leads to a Layer 1 cache hit.
- Every Layer 1 cache record carries license_class.
- License closure: a Layer 4 artifact's effective license class is the most-restrictive in its provenance chain.

CI tests these invariants per campaign. Factory Claude sessions report cache integrity at session close.

---

## 2. Schema completeness audit

The current `BiologicalClaim` schema (Proposal #2 v1 §4.3) is the v0 minimum. This section identifies fields that may be needed for Phase 6+ and assigns priority. **Ship the high-priority additions in the current schema version (v1.1) before scale ingestion begins; defer medium and low priority to schema versions v1.2+ as needs emerge.**

### 2.1 High-priority additions (ship in BiologicalClaim v1.1 before scaling beyond Session 5)

These fields are likely-needed for Phase 6 and cheap to extract from typical structured biological sources. Adding them later costs re-extraction across all prior sessions; adding them now costs nothing.

- **`spatial_context`** — geographic_range (text or coordinate bounding box), biome (enum), biogeographic_region (enum). Critical for ecological claims and biogeographic sampling-bias correction.
- **`temporal_context`** — fossil_first_appearance / fossil_last_appearance (geological time intervals), modern_status (modern / extinct / historical_only). Critical for fossil-record overlap with motif basins.
- **`life_stage_context`** — life_stage (adult / larval / nymph / sessile / dispersing / dormant / mixed), developmental_phase. A claim about "ant" may apply to adults but not larvae.
- **`scope_level`** — population_level / individual_observation / inferred / theoretical. A claim "exhibits stigmergy" at population level differs from one inferred from anatomy.
- **`observation_setting`** — wild / captive / laboratory / inferred_from_morphology / behavioral_assay / phylogenetic_inference. The methodology gates reliability.
- **`taxon_synonym_chain`** — list of synonyms across versions, with `accepted_name_at_extraction_time` and `accepted_name_currently`. Taxa rename; we don't want to re-fetch when ITIS updates a synonym.
- **`source_authority_class`** — peer_reviewed / textbook / curated_database / expert_commentary / popular / unverified. Reliability metadata that informs audit weighting.
- **`claim_publication_year`** — when the claim was first published. Trait knowledge changes; old claims may be superseded.
- **`normalization_version`** — version of the normalizer that produced the Layer 3 references for this claim. Lets us re-normalize cleanly when normalizers improve.
- **`schema_version_at_extraction`** — version of the BiologicalClaim schema this record was produced under. Migration target.

### 2.2 Medium-priority additions (BiologicalClaim v1.2 — add when Phase 6 calls for them)

These fields are needed for some claims but not all; some sources don't carry them. Defer until a campaign specifically requires them.

- **`quantitative_magnitude`** — claim_magnitude (float), claim_units (enum), claim_uncertainty (CI or stddev). For numeric claims (rates, distances, body sizes).
- **`phylogenetic_context`** — sister_clade_traits, ancestral_state_inference, apomorphic_or_synapomorphic. Needed for convergence detection.
- **`methodology_summary`** — text excerpt of the methodology section (license-permitting), methodology_reliability_score.
- **`cross_references`** — claim IDs that confirm this claim, claim IDs that elaborate on it (distinct from `conflicts`, which is contradictions).
- **`overlap_field_evidence_strength`** — for overlap-field claims specifically: write_evidence, persist_evidence, read_evidence, counterfactual_evidence (each as confidence values).
- **`sample_size`** — n / n_individuals / n_observations / n_studies. Reliability-weighting input.

### 2.3 Low-priority additions (BiologicalClaim v1.3+ — add only when needed)

- **`original_language`** — for non-English sources.
- **`translation_provenance`** — translator identity, translation_method, translation_review_status.
- **`citation_metadata`** — citation count, h-index of authors, citation_velocity.
- **`derivative_claim_chain`** — if this claim is derived by re-extraction from a prior claim version, the chain.
- **`embargo_status`** — publication embargo windows for time-restricted sources.

### 2.4 Recommended schema action before Session 001

Codex (in a small follow-up task before Session 001 opens, or as the first action of Campaign 013) bumps `BiologicalClaim` from v1.0 to v1.1 with the §2.1 high-priority additions. Existing v1.0 records (the 200 from KE1, the 150 from ITIS in Campaign 012) migrate via standard tombstone-and-supersede:

- Old v1.0 records: marked `schema_version: 1.0`, deprecated.
- Re-extraction from cache produces v1.1 records with the new fields populated where derivable from cache; null where not derivable.
- The 200 KE1 + 150 ITIS records re-extract from Layer 1 cache (assuming the cache exists; if not, this is the first cache build).

This is a bounded one-time migration. Doing it before scaling beyond ~500 records is cheap; doing it after 50,000 records have ingested is expensive.

---

## 3. Schema evolution policy

### 3.1 Versioning

`BiologicalClaim` (and other Factory schemas) carry `schema_version` per [SemVer](https://semver.org/):

- **Patch (1.0.0 → 1.0.1):** documentation clarification, constraint tightening that's backward-compatible. Old records remain valid; no migration.
- **Minor (1.0 → 1.1):** additive — new optional fields. Old records remain valid; new fields populate via migration where derivable, otherwise default to null. This is the §2 high-priority case.
- **Major (1.x → 2.0):** breaking — field removals, type changes, semantic changes. Requires explicit migration with declared field mappings. Old records migrate or are tombstoned.

Major version bumps are rare and expensive. The §2.1 high-priority additions ship as a single 1.1 minor bump; future Phase 6 needs land as 1.2, 1.3, etc.

### 3.2 Migrations are pure functions

```
def migrate_1_0_to_1_1(record_v1_0: dict) -> dict:
    """v1.0 → v1.1: add §2.1 high-priority fields with derivable defaults from cache."""
    cached = layer1_cache.get(record_v1_0["provenance_hash"])
    return {
        **record_v1_0,
        "schema_version": "1.1",
        "spatial_context": _derive_spatial_context(cached),
        "temporal_context": _derive_temporal_context(cached),
        "life_stage_context": _derive_life_stage_context(cached),
        # ...
    }
```

Pure functions: same input → same output. Migrations are CI-tested against fixture records.

### 3.3 Replay-from-cache discipline

When a schema migrates:

1. The migration runs against existing claim records (Layer 2) where derivable fields exist in the cache (Layer 1).
2. For fields that aren't derivable from cache (e.g., a new field that requires a re-fetch with a different parser), the field is `null` and the record is flagged `requires_replay: true`.
3. Records with `requires_replay: true` are queued for re-extraction. Re-extraction reads from Layer 1 cache (or re-fetches if Layer 1 doesn't have the needed parser surface).
4. After re-extraction, the record's `requires_replay` flag clears.

This means: schema migrations *don't break the audit chain*. A v1.0 record that migrates to v1.1 retains its audit_status. If re-extraction is needed for some new field, the record reverts to `raw_extracted` for the new field only, and re-audit applies only to that field.

### 3.4 Normalizer version compatibility

Layer 3 normalizers also version. When a normalizer bug is discovered:

1. Affected records receive a `normalization_version` mismatch flag.
2. Re-normalization runs against the cached Layer 2 claims (no re-fetch, no re-extract).
3. Affected claims revert to `raw_extracted` *for the affected normalization paths only* (not for the full claim).
4. Audit re-processes the affected normalizations.

Layer 2 (claims) and Layer 3 (normalizations) are independently versionable.

---

## 4. Per-session quality gates

Factory Claude sessions follow a discipline that scales with confidence. Sessions are categorized into stages.

### 4.1 Session 001 — Synthetic shakedown

**Adapter:** synthetic_lane1 (KE1 corpus).
**Mode:** candidate_generation.
**Goal:** verify the operating procedure executes mechanically end-to-end.

Pass criteria:
- All 10 operating-procedure steps execute without error.
- Session log entry committed.
- Estimation Loop record committed (deliberately ambitious estimate).
- ≥10 candidate records produced through the full pipeline (extract → normalize → conflict-detect → queue).
- Cache integrity verified (Layer 1 lookups succeed; provenance hashes match).
- License closure summary clean.
- Audit queue depth reported.
- Session close summary produced.

Failure mode: any operating-procedure step that fails reveals a Factory Claude initiation document amendment or a code path bug. Flag in `decision_log.md`; do not proceed to Session 002 until the issue is resolved.

### 4.2 Sessions 002–005 — ITIS shakedown

**Adapter:** itis_lane1 (real source).
**Mode:** candidate_generation.
**Goal:** validate the discipline on real-source data with real license enforcement.

Pass criteria per session:
- Cache hit rate ≥95% (i.e., the adapter is reusing the cache where possible; Session 002's cache miss rate may be 100% as the cache fills, but Sessions 003+ should hit prior records).
- License closure clean.
- Conflicts surfaced honestly (real ITIS has internal contradictions; expect non-zero conflict counts).
- Architect Claude audit pass: ≥10 of Session N's records advance from `raw_extracted` to `audited_confirmed` or are explicitly rejected with reasons. Session N+1 doesn't open until Session N has audit feedback.

Aggregate across Sessions 002–005:
- ≥500 BiologicalClaim records ingested with full provenance.
- KE1-style false-claim-rejection rate maintained (≥0.9 if planted false claims are introduced as audit calibration).
- Architect audit pass rate ≥70% (lower means the extraction is too noisy; higher means audit isn't challenging).

If pass rate <70% across the shakedown: Factory Claude's confidence calibration is off; tighten extraction discipline before scaling.

### 4.3 Sessions 006–010 — Calibration

**Adapter:** itis_lane1 + new adapters as Codex ships them.
**Mode:** candidate_generation; selective dry_run for adapter-validation runs.
**Goal:** Estimation Loop convergence; first WorldDensificationRecommendation reports for W6 / W7 / W12.

Pass criteria:
- Estimation Loop estimation_delta enters [0.5, 2.0] range (well-calibrated).
- ≥1500 BiologicalClaim records cumulative across Sessions 001–010.
- ≥3 worlds with WorldDensificationRecommendation reports queued for audit.
- Architect audit pass rate stable (within 5% across last 5 sessions).
- Cache integrity invariants pass.

### 4.4 Sessions 011+ — Steady-state

**Adapter:** any operational adapter (Lane 1 only in v0; Lane 2/3 require their own calibration).
**Mode:** candidate_generation default; dry_run for batch runs; non-default modes require explicit per-session authorization.
**Goal:** scale ingestion toward Phase 6 readiness end-state.

Pass criteria per session:
- Estimation Loop estimation_delta in [0.85, 1.15] (well-calibrated).
- Throughput stable: claims/session ± 25% week-over-week.
- Audit queue depth below cap.
- Cache integrity invariants pass.
- License closure clean.

If estimation_delta drifts outside [0.5, 2.0] for two consecutive sessions: Factory Claude's calibration is degrading; surface to decision log.

---

## 5. Failure recovery procedures

### 5.1 Bug discovered in normalizer (Layer 3)

- Bug reported in `decision_log.md` with severity + scope (which sessions affected).
- Affected records' Layer 3 references are tombstoned with `normalization_version_bug: true`.
- Re-normalization runs against Layer 2 (cached claims) under the corrected normalizer.
- Affected records' audit_status reverts to `raw_extracted` for the affected normalization paths only.
- Audit pipeline re-processes the affected normalizations.
- No re-fetch, no re-extract.

**Cost:** small. Affected sessions' Layer 3 work is redone; Layers 1, 2, 4 (rebuilt from 3) re-stabilize.

### 5.2 Bug discovered in extractor (Layer 2)

- Bug reported in `decision_log.md`.
- Affected records (Layer 2) marked `extractor_version_bug: true`.
- Re-extraction runs against Layer 1 (cached source records) under the corrected extractor.
- Affected records' audit_status reverts to `raw_extracted`.
- Audit pipeline re-processes affected claims.
- No re-fetch.

**Cost:** medium. Re-extraction is faster than re-fetch but slower than re-normalization. Layer 4 reports rebuild from corrected Layer 2.

### 5.3 Bug discovered in adapter (Layer 1 fetcher)

- Bug reported in `decision_log.md`.
- Affected source records marked `fetcher_version_bug: true`.
- Re-fetch under corrected adapter; new Layer 1 cache entries replace old (old entries archived under `cache/_deprecated/{old_hash}/`).
- Layer 2 records re-extracted from new Layer 1.
- Layer 3 normalizations rebuilt.
- Layer 4 reports regenerate.

**Cost:** high. Re-fetch is network-dependent and source-changes-may-affect-results. This is the case the archive-before-extract discipline is designed to *prevent* by isolating fetcher bugs from extraction bugs. Most failures should land in §5.1 or §5.2; §5.3 is rare.

### 5.4 Schema migration (Layer 2 schema bump)

- New schema version declared (e.g., 1.0 → 1.1).
- Migration function tested against fixtures.
- Migration runs against existing records.
- Records with `requires_replay: true` queue for re-extraction from cache.
- Audit pipeline re-processes only the affected fields.
- No re-fetch.

**Cost:** small to medium depending on field count requiring re-extraction.

### 5.5 Audit reversal

If Architect Claude (or PI) revokes an `audited_confirmed` decision retroactively (e.g., a downstream review reveals the audit was wrong):

- Affected records revert to `audited_rejected` or `needs_audit` with reason note.
- Records they supported (TraitDecompositions, WorldDensificationRecommendations) re-route through audit.
- The revocation is logged in the decision_log with the prior audit's signature voided.

**Cost:** scales with downstream dependency depth.

---

## 6. Quantitative end-state for Phase 6 readiness

The Factory is "ready for Phase 6 grounding" when:

### 6.1 Coverage of biology shadow track anchor set

For each of the 7 anchor traits (photoreception, powered flight, branching transport, eusociality, segmentation, autocatalytic metabolic closure, externalised memory):

- ≥100 BiologicalClaim records, across ≥50 distinct taxa, from ≥3 authoritative sources.
- ≥5 TraitDecomposition records covering the major substrate-implementations (e.g., for flight: bird wings, bat wings, insect wings, pterosaur wings, engineered aircraft if cross-substrate).
- Process-role coverage: ≥3 process roles per anchor trait with operational predicates.
- Interaction-channel coverage: ≥2 channels per anchor.
- State-space-effect coverage: ≥1 effect per anchor.
- OverlapField references: where applicable (some anchors don't have overlap fields; that's a real result).
- Phylogenetic distribution captured: which clades exhibit the trait, with `phylogenetic_context` populated where derivable.
- License closure clean across the anchor's evidence graph.
- Architect-audited at ≥70% audit pass rate.

### 6.2 World densification readiness

At least 3 of W6 / W7 / W8 / W12 advanced to `claim_ready_densified` with:

- ≥10 organism templates per world covering ≥4 axes orthogonally.
- ≥30 BiologicalClaim records per world with source citations.
- WorldDensificationReport committed and Architect-signed.

### 6.3 Calibration corpus expansion

KP1–KP4 calibration corpora updated with ≥30 additional scenarios using real ingested data (not just synthetic). KE1 expanded with ≥30 misalignment cases discovered in real ingestion (where ITIS records contradict each other or contradict NCBI).

### 6.4 Lane progression

- Lane 1 fully operational with ≥3 real source adapters (ITIS + at least 2 of: NCBI Taxonomy, OTL synthetic tree, GBIF occurrence, public trait databases).
- Lane 2 (literature abstracts) calibrated with KL2 (literature calibration) corpus and ready to ship.
- Lane 3 (full text) deferred to post-Phase-6.

### 6.5 Quantitative thresholds (rough targets, refined per session experience)

- ≥10,000 cumulative BiologicalClaim records.
- ≥1,000 unique taxa represented.
- ≥500 TraitDecomposition records.
- ≥100 OverlapField records with full 4-part operational evidence.
- Cache size: bounded by source license; for CC0 sources, full raw cache; for CC-BY-NC sources, structured-fields-only cache.
- Audit queue depth steady-state: ≤200 records (caps prevent backlog explosion).

These are scale targets, not perfectionist goals. Hitting them means Phase 6 has the substrate to anchor L3 claims; not hitting them means we proceed exploratory-only on the gaps.

---

## 7. Document version control

This document is canonical. Updates require:

- `decision_log.md` entry citing the change.
- Architect signature (currently Claude; after Codex returns, optionally Codex co-signs for Builder concerns).
- PI sign-off on doctrine-relevant changes.

The current version is **1.0**, dated [date Factory Claude first reads this]. Future versions track field additions, schema evolution policy refinements, and quantitative threshold adjustments.

---

## 8. Bottom line

The Factory's reusability over time depends on three commitments:

1. **Archive-before-extract** — Layer 1 cache is the foundation; re-fetch is rare, re-extract is cheap.
2. **Schema versioning with pure-function migrations** — schemas evolve without breaking records.
3. **Layer-isolated bug recovery** — normalizer / extractor / fetcher bugs each affect only their own layer's records.

If we honor these three commitments, ingesting 100,000 claims today and adding `geographic_range` to the schema next month costs roughly the time to write the migration function and re-extract from cache — not the time to re-fetch 100,000 records from sources that may have changed.

If we don't honor them, we eat re-ingestion cost the moment Phase 6 reveals a missing field. That cost compounds with every additional schema evolution.

The discipline here is not optional. It's the engineering version of D19 (source-bound extraction) and D20 (extraction/detection separation): same kind of structural integrity, applied to the storage layer.

Sleep well. When you wake up, Factory Claude knows what discipline he's operating under, and the §2.1 high-priority schema additions are ready for a small Codex follow-up before Session 001 opens.

— The Architect, on behalf of the project, under spec v1.2 plus binding doctrine D7–D21.
