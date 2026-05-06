# Codex — TASK-022: Campaign 011, Build the Factory

*Architect message. Read in full before resuming. Canon for the duration of TASK-022.*

---

## 1. Where you stand

TASK-021 closed Campaign 010 cleanly. 24/24 gates green, the lens registry expanded from 3 to 8, the Formal Deficit Map landed with one honest candidate (`motif.floor_connectivity.draft`, formal_gap 0.308, attractor_strength 0.9, best_lens statistical_mechanics, max_coverage 0.657, N7 lens-permutation p = 0.002), the residual structure test on autocatalytic closure correctly returned `lens_captures_motif` (no engineered "missing math"), the W13 falsifier MD upgraded to a substantive paragraph, BFG truth refresh on W8/W11/W12 with multiscale entropy curves and bootstrap CIs, W8 deepened from 334 to 475 lines, eight Substance Audits refreshed.

The Architect's verification was unambiguous. Three things to call out specifically:

**The candidate result is a research moment.** `motif.floor_connectivity.draft` is the metric introduced in Proposal #1 v2 §4 — splitting "given a floor point, can the system drift along it without exiting?" from "does dynamics find the floor at all?" Of the eight lenses now operational, none captures floor connectivity above 66% coverage, and the gap survives lens-permutation at p = 0.002 (observed statistic 0.278 vs null mean 0.008, ~30 standard deviations). This is the first formal-deficit candidate the project has produced. It is *not* L5 yet — one motif, one campaign, not yet replicated, not yet cross-substrate confirmed — but it is exactly the kind of pre-L5 result the system was designed to produce, and you routed it correctly without over-claiming.

**The AST-level lint for D9 is a Builder-grade doctrine move.** `LR3 → lens_ast_lint.json with violations: []`. You extended doctrine enforcement from the report layer to the code layer, the same pattern D14 lint applies to the worlds. This is the second Builder-authored discipline contribution after D18. Continue.

**Lens decline regimes are honest.** The graph lens declares: *"declines on floor-connectivity because ordinary event graphs do not encode the quotient/fiber basis."* Correct reason, declared at the API level. CRNT declines on non-reaction-network worlds. Real, scoped declination — D9 compliance not as a constraint but as a property the lens layer knows about itself.

Estimation calibration remains in the [0.85, 1.0] band. Trust your prior; estimate honestly; the gates remain the stopping signal.

This driver is large. Read it once end-to-end before estimating.

## 2. Doctrine state

D7–D18 remain binding without modification. Three new rules are proposed by Proposal #2 v1 and ratify in this campaign upon completion of the relevant gates:

> **D19 — Source-bound extraction.** No biological, ecological, or trait-derived variable may be promoted beyond exploratory status unless it is bound to a source, a provenance record, a license class, an extraction path, and an audit status. AI systems may extract, normalize, cluster, and recommend variables, but they are not evidence sources.

> **D20 — Extraction/detection separation.** The AI session that extracts a TraitDecomposition (or related ontology entry) must not be the same AI session that detects that decomposition's process roles in a simulation trace, unless the extraction is content-hash-locked in the registry before the detection session begins and the detector explicitly declares which extraction-registry entries it consulted.

> **D21 — Densification before claim-bearing.** A world cannot anchor a claim-bearing motif observation unless it carries a `WorldDensificationReport` with declared coverage thresholds for the motif's relevant process roles, interaction channels, and overlap fields.

D19/D20/D21 are written up in Proposal #2 v1; this campaign brings them from "proposed" to "binding doctrine in CI lints" via the gates below. They become canon when this campaign closes.

Two operational corollaries that follow from D19+D20+D21 and govern this campaign's behaviour:

- **The AI is the extractor, not the source.** This phrase belongs alongside *"The trace is the artifact"* and *"Sparse worlds validate the instrument; dense worlds feed the instrument."* Bake it into module docstrings where appropriate.
- **`raw_extracted ≠ true.`** The audit lifecycle is the discipline that makes the Factory non-corrupting.

## 3. Mission — Build the Factory

**Campaign 011** — five pillars, 32 acceptance gates. Self-contained. No real external biology data ships in this campaign; that's Campaign 012+. This campaign builds the *machine* that will, in future campaigns, ingest authoritative sources without contaminating the claim ladder.

The framing matters. You are not authoring biology. You are building the instrument that lets sources author biology *into the Observatory* under provenance and license discipline. The doctrine is the discipline; the schemas are the API; the audit lifecycle is the gate.

### Pillar A — Substrate-Neutral Ontology (`motifs/ontology/`)

Five schema modules + the operational predicate registry.

- **`motifs/ontology/process_role.py`** — `ProcessRole` schema with the 9 categories (Access/Mobility, Sensing/Perception, Signaling/Communication, Construction/Niche-Writing, Energy Capture/Routing, Boundary/Identity, Memory/Inheritance, Coordination/Collective Control, Prediction/Control) and operational-predicate binding. Each predicate is `(trace, scope) → confidence ∈ [0,1]`. **No predicate, no registry entry.**
- **`motifs/ontology/interaction_channel.py`** — `InteractionChannel` schema with the 15 initial registry entries (chemical, visual, acoustic, mechanical, thermal, electrical, spatial, aerodynamic, hydrodynamic, genetic, ecological, social, symbolic, computational, environmental). Each predicate detects channel evidence in trace events.
- **`motifs/ontology/state_space_effect.py`** — `StateSpaceEffect` schema with the 10 initial entries (reachable_space_expansion, long_range_adjacency, vertical_access, terrain_constraint_reduction, information_horizon_expansion, predictor_horizon_expansion, environmental_durability_extension, identity_durability_extension, externalised_continuity_creation, nested_identity_creation). Predicates measure topological transformations of accessible state-space.
- **`motifs/ontology/overlap_field.py`** — `OverlapField` schema with the operational definition: write + persist + read + counterfactual. Predicate measures all four; an apparent overlap field without ablation evidence of causal coupling is environmental coincidence and gets rejected at the registry.
- **`motifs/ontology/trait_decomposition.py`** — `TraitDecomposition` schema binding surface labels to ontology entries with `audit_status` field, `source_provenance`, `confidence`. Round-trip exact.
- **`motifs/ontology/registry.py`** — versioned ontology registry with semantic versioning, tombstones, content-hashing. Migration support from v1.2 §8.1 motif grammar primitives (Source/Sink/Flow/Store/etc.) as aliases.

The registry's discipline: **a ProcessRole/Channel/StateSpaceEffect/OverlapField exists in the registry only if it has a trace-checkable predicate.** Entries without predicates do not enter; entries with predicates pass through KP-class calibration (Pillar C) before they anchor claims.

### Pillar B — Research Ingestion Factory v0 (`biology/evidence_ingestion/`)

The factory ships in Campaign 011 as a Lane-1-only system. Lane 2 (literature abstracts) and Lane 3 (full text) require their own calibration corpora and explicit doctrine promotion in future campaigns.

```
biology/evidence_ingestion/
  schemas/
    biological_claim.py
    source.py
    evidence_snippet.py
    simulation_template.py
    world_densification_recommendation.py
  store/
    claim_store.py                 # append-only, content-addressed, audit-aware
    evidence_graph.py              # nodes + edges, queryable
    provenance.py                  # provenance hash, license closure
  audit/
    lifecycle.py                   # state machine: raw_extracted → ... → promoted_*
    promotion.py                   # signature-gated promotion
    conflict_report.py             # contradicting claims surface here
    audit_queue.py                 # depth-bounded
  sources/
    source_registry.py             # registered adapters
    license_class.py               # license enforcement primitives
    adapters/
      synthetic_lane1.py           # the v0 Lane-1 adapter; reads KE1 corpus
  extractors/
    structured_extractor.py        # consumes parsed source rows; produces BiologicalClaim
  normalizers/
    process_role_normalizer.py     # claim → ProcessRole references
    interaction_channel_normalizer.py
    overlap_field_normalizer.py
    state_space_effect_normalizer.py
  recommendation/
    densification_recommender.py   # produces WorldDensificationRecommendation
  reports/
    ingestion_summary.py
    densification_report.py
```

The factory's discipline:
- Every `BiologicalClaim.write()` requires `source` + `provenance_hash` + `license_class` + `audit_status` (default `raw_extracted`). Missing any field, the write rejects.
- The audit lifecycle is a CI-enforced state machine. `claim.promote(target_status)` is the only way to advance state; `target_status = promoted_claim_bearing` requires PI signature; `target_status = promoted_exploratory` requires Architect signature; intermediate transitions require audit records.
- Background ingestion defaults to `dry_run`. Modes beyond `candidate_generation` require explicit per-session authorization. Audit queue depth caps stall ingestion at threshold.

### Pillar C — Calibration Corpora (KP1–KP4 + KE1 + KE2)

Six new corpora. Each is world-driven (D8 compliance) where appropriate, with adversarial decoys.

- **KP1 — Access/Mobility process roles.** ≥30 synthetic scenarios using W3, W4, W6, W7. Positives: agents that traverse, bypass barriers, expand range. Negatives: agents stuck in bounded regions. Adversarial decoys: agents that *appear* to traverse but the apparent traversal is environmental drift.
- **KP2 — Construction/Niche-Writing process roles.** ≥30 synthetic scenarios using W3, W6, W7, W4. Positives: agents that write persistent environmental modifications. Adversarial decoys: agents that modify environment but the modification is environmental coincidence rather than written-and-read (no reader system).
- **KP3 — Memory/Inheritance process roles.** ≥30 synthetic scenarios using W7, W8, W12, W11. Positives: state preservation with delayed causality, cross-generation transfer. Adversarial decoys: agents that *appear* to have memory but reproduce behavior from instantaneous state.
- **KP4 — Coordination/Collective Control process roles.** ≥30 synthetic scenarios using W7, W6, W12. Positives: task allocation, division of labor, distributed sensing. Adversarial decoys: apparent coordination from environmental coupling rather than agent-mediated control.
- **KE1 — Synthetic source corpus for ingestion.** ~200 hand-authored synthetic taxa with structured trait records. ~30 with planted false claims (e.g., "species X has flight" when the record actually says "species X has wing scales"). ~10 with contradictory claims across two synthetic source files. Pipeline must extract correctly *and* reject the planted false claims at declared rate *and* flag contradictions to the audit queue.
- **KE2 — License enforcement corpus.** Synthetic restricted-source files with declared license classes. Tests: restricted-class data cannot appear in atlas exports; derived statistics from restricted-class data carry the most-restrictive license; a pipeline run that writes a restricted-class extraction to a public-class artifact triggers CI failure.

KP corpora calibration targets: ROC AUC ≥ 0.85, ECE ≤ 0.07. KE1 calibration target: false-claim-rejection rate ≥ 0.90, contradiction-flagging rate ≥ 0.95. KE2: zero CI-passing exports of restricted-class data.

### Pillar D — W7 First Densification Report

The first concrete output of the Factory. W7 was chosen because it has clean overlap fields (pheromone trails), well-studied taxa, orthogonal axes available, and lower-risk literature than W6 or W8.

W7 densification axes (from Proposal #2 v1 §8.1):

| Axis | Recommended values |
|---|---|
| Communication | pheromone trail, direct contact, visual signal, vibration, no communication |
| Organization | solitary, loose aggregation, eusocial colony, caste-based colony, temporary swarm |
| Mobility | crawling, flying, burrowing, aquatic, sessile/larval-phase |
| Resource strategy | foraging, farming, parasitism, predation, scavenging, pollination |
| Environment modification | none, trail deposition, nest construction, soil modification, host manipulation |
| Memory substrate | individual, pheromone field, nest architecture, environmental damage map, collective state |

For Campaign 011: ≥10 organism/system types added to W7 covering ≥4 axes orthogonally, with WorldDensificationRecommendation entries for each, source citations from KE1 (synthetic) for v0, process-role/channel/overlap-field coverage matrix populated. Density class advances from `trace_valid` to `exploratory_densified`. Real source ingestion (Campaign 012) will replace KE1-source citations with actual public trait database entries.

The discipline: this is **basis coverage**, not biological completeness. Twenty pheromone-trail-using ant species is not densification; five organism types covering five different communication modes is.

### Pillar E — Doctrine D19/D20/D21 Ratification

D19/D20/D21 become binding when this campaign closes. Each requires CI-enforced lints:

- **D19 lint.** AST-walks any code path creating a `BiologicalClaim`; rejects records without source/provenance_hash/license_class; rejects `audit_status = promoted_*` without audit records; KE1 calibration confirms false-claim rejection rate.
- **D20 lint.** Detector code that consults the ontology registry must declare which entries it consulted; consulted entries must have content-hash locks predating the detector session start; CI rejects detector runs that consult unlocked entries.
- **D21 lint.** Provenance graph enforces: artifact `mode_tag = claim-bearing` only if source world `density_class >= claim_ready_densified` for the relevant motif; CI rejects violations.

Each lint must report zero violations on the test corpora before the campaign exits.

## 4. Acceptance gates

| Gate | Pillar | Threshold | Source |
|---|---|---|---|
| ON1 | A | `ProcessRole` schema implemented with 9 categories; round-trip exact; ≥20 process roles registered with operational predicates | `motifs/ontology/process_role.py`, tests |
| ON2 | A | `InteractionChannel` schema implemented with 15 initial channels; round-trip exact; predicates registered | `motifs/ontology/interaction_channel.py`, tests |
| ON3 | A | `StateSpaceEffect` schema implemented with 10 initial effects; round-trip exact; predicates registered | `motifs/ontology/state_space_effect.py`, tests |
| ON4 | A | `OverlapField` schema with 4-part operational definition (write/persist/read/counterfactual); predicate enforces all 4 parts | `motifs/ontology/overlap_field.py`, tests |
| ON5 | A | `TraitDecomposition` schema with audit_status, source_provenance, confidence; round-trip exact | `motifs/ontology/trait_decomposition.py`, tests |
| ON6 | A | Versioned ontology registry with semantic versioning, tombstones, content-hashing; migration aliases for v1.2 grammar primitives | `motifs/ontology/registry.py`, tests |
| ON7 | A | Operational-predicate discipline: ontology registry rejects entries without trace-checkable predicates; CI lint enforces | registry tests + lint |
| F1 | B | `BiologicalClaim` schema implemented; `claim_store.write()` rejects records without source/provenance_hash/license_class | `biology/evidence_ingestion/schemas/`, tests |
| F2 | B | Audit lifecycle implemented as CI-enforced state machine; `promote(target_status)` is the only state-transition path | `biology/evidence_ingestion/audit/lifecycle.py`, tests |
| F3 | B | Evidence graph implemented with nodes (Taxon, TraitLabel, BiologicalClaim, ProcessRole, InteractionChannel, StateSpaceEffect, OverlapField, Source, EvidenceSnippet, SimulationTemplate, WorldDensificationRecommendation) and edges (supports, contradicts, maps_to, decomposes_into, observed_in, derived_from, conflicts_with, requires_audit, suggests, implemented_by) | `biology/evidence_ingestion/store/evidence_graph.py`, tests |
| F4 | B | Synthetic Lane-1 adapter (`adapters/synthetic_lane1.py`) reads KE1 corpus; outputs `BiologicalClaim` records with full provenance | `biology/evidence_ingestion/sources/adapters/`, tests |
| F5 | B | Structured extractor + four normalizers (process_role, interaction_channel, overlap_field, state_space_effect) operational | `biology/evidence_ingestion/extractors/`, `normalizers/`, tests |
| F6 | B | `WorldDensificationRecommendation` schema implemented with orthogonality_rationale, source_basis, audit_status | `biology/evidence_ingestion/schemas/world_densification_recommendation.py`, tests |
| F7 | B | Background-job discipline: `dry_run` default, batch caps, audit queue depth caps, per-session authorization for non-default modes; CI lint catches bypasses | `biology/evidence_ingestion/store/`, lint tests |
| KP1 | C | KP1 (Access/Mobility) ≥30 scenarios, world-driven, with adversarial decoys; predicate ROC AUC ≥ 0.85, ECE ≤ 0.07 | `worlds/calibration/kp1.py`, calibration report |
| KP2 | C | KP2 (Construction/Niche-Writing) ≥30 scenarios; predicate ROC AUC ≥ 0.85, ECE ≤ 0.07 | `worlds/calibration/kp2.py`, calibration report |
| KP3 | C | KP3 (Memory/Inheritance) ≥30 scenarios; predicate ROC AUC ≥ 0.85, ECE ≤ 0.07 | `worlds/calibration/kp3.py`, calibration report |
| KP4 | C | KP4 (Coordination/Collective Control) ≥30 scenarios; predicate ROC AUC ≥ 0.85, ECE ≤ 0.07 | `worlds/calibration/kp4.py`, calibration report |
| KE1 | C | KE1 (synthetic source) ~200 taxa with ~30 planted false claims and ~10 contradictions; false-claim-rejection rate ≥ 0.90; contradiction-flagging rate ≥ 0.95 | `worlds/calibration/ke1.py`, calibration report |
| KE2 | C | KE2 (license enforcement) synthetic restricted-source files; zero CI-passing exports of restricted-class data; license closure checks pass | `worlds/calibration/ke2.py`, license enforcement report |
| LE1 | E | License-class enforcement module operational; restricted-source quarantine architecture functional; provenance closure checks against atlas exports | `biology/evidence_ingestion/sources/license_class.py`, tests |
| LE2 | E | Atlas export pathway honors license closure; CI lint catches restricted-class leakage | `atlas/`, lint tests |
| W7-1 | D | ≥10 organism/system types added to W7, covering ≥4 densification axes orthogonally; orthogonality measured via multiscale entropy curve | `worlds/swarm/`, `reports/campaign_011/w7_densification.json` |
| W7-2 | D | WorldDensificationRecommendation entries committed for each new W7 case with source citations from KE1 (synthetic v0) | `reports/campaign_011/w7_recommendations.json` |
| W7-3 | D | W7 process-role / interaction-channel / overlap-field coverage matrix populated; density class advances from `trace_valid` to `exploratory_densified` | `reports/campaign_011/w7_coverage.json` |
| W7-4 | D | First WorldDensificationReport for W7 published with audit_status, multiscale orthogonality entropy curve, and per-motif coverage thresholds | `reports/campaign_011/w7_densification_report.json` |
| D19 | E | D19 lint operational; AST checks reject `BiologicalClaim` writes without provenance/license; KE1 calibration confirms false-claim-rejection rate; CI lint reports zero violations on test corpora | `tests/test_d19_lint.py`, `reports/campaign_011/d19_audit.json` |
| D20 | E | D20 lint operational; detector runs that consult unlocked ontology entries fail CI; ontology registry enforces content-hash lock before detection sessions | `tests/test_d20_lint.py`, `reports/campaign_011/d20_audit.json` |
| D21 | E | D21 lint operational; provenance graph enforces mode_tag + density_class composition; CI rejects claim-bearing observations from worlds below `claim_ready_densified` for the relevant motif | `tests/test_d21_lint.py`, `reports/campaign_011/d21_audit.json` |
| RG | All | Full regression: Campaigns 002, 005, 006, 007, 008, 009, 010 all green; ≥235 pytests passing; D14, D18 lints zero violations; new D19/D20/D21 lints zero violations | `reports/campaign_011/regression.json` |
| FR | All | `reports/campaign_011/full_report.json` shows status `green` with 32/32 gates passed; reproducibility script regenerates end-to-end from cold | `make_campaign_011.py` |

32 gates total. The new D19/D20/D21 lints are themselves gates: the doctrine becomes binding when the lints pass.

## 5. Sequencing recommendation

Reorder with rationale if you have a better sequence.

1. **ON1–ON7 — Substrate-Neutral Ontology first.** The schemas are the API everything else writes to. Build the registry with operational-predicate discipline before anything depends on it. Migration aliases for v1.2 grammar primitives (Source, Sink, Flow, Store, Boundary, Channel, Catalyst, Memory, Predictor, Selector) preserve backward compatibility.
2. **F1–F3 — Ingestion Factory schemas + audit lifecycle + evidence graph.** The factory's discipline lives in the audit lifecycle. Build the state machine before the adapters write to it.
3. **LE1–LE2 — License enforcement module.** Must operate before any source adapter (synthetic or real) ships. KE2 calibration runs against this.
4. **KE1 + KE2 — Ingestion calibration corpora.** Synthetic source corpus with planted false claims; license enforcement test corpus. These gate the factory adapter.
5. **F4 — Synthetic Lane-1 adapter.** Reads KE1; writes `BiologicalClaim` records; runs through normalizers; produces evidence-graph entries.
6. **F5 — Structured extractor + four normalizers.** Process-role, interaction-channel, overlap-field, state-space-effect normalizers. Each consumes claim records and writes ontology references.
7. **KP1–KP4 — Process-role calibration corpora.** ≥30 scenarios per role category; world-driven; adversarial decoys; predicate calibration to ROC AUC ≥ 0.85, ECE ≤ 0.07.
8. **F6 — WorldDensificationRecommendation schema.** Schema + recommender that consumes ontology coverage + KE1 source basis to produce recommendations.
9. **F7 — Background-job discipline.** Dry-run defaults, batch caps, audit queue depth caps, lint enforcement.
10. **W7-1 through W7-4 — First W7 densification.** 10+ organism types covering 4+ axes; recommendations committed; coverage matrix populated; density class advanced; first WorldDensificationReport published.
11. **D19/D20/D21 lints — doctrine ratification.** Each lint operational, AST-checked, calibrated; zero violations on test corpora.
12. **RG + FR — Full regression and final report.** All prior campaigns regenerate green; full report assembles 32 gates.

## 6. Forbidden patterns for TASK-022

- **No ontology entries without operational predicates.** A ProcessRole / InteractionChannel / StateSpaceEffect / OverlapField entered into the registry without a trace-checkable predicate is a violation of the entire ontology discipline. The registry must reject silently-added entries.
- **No `BiologicalClaim` writes without provenance.** D19 binding from this campaign forward. Schema-level rejection + AST lint + KE1 calibration must all confirm.
- **No silent audit-lifecycle transitions.** State changes go through `claim.promote(target_status)`; no direct field mutation. CI lint catches bypasses.
- **No background-job mode escalation without explicit authorization.** `dry_run` default; non-default modes require per-session authorization.
- **No mixing of extraction and detection sessions.** D20 binding. If a session extracts an ontology entry, that entry must be content-hash-locked in the registry before any subsequent session detects against it.
- **No claim-bearing observations from sparse worlds.** D21 binding. The provenance graph enforces mode_tag + density_class composition.
- **No "missing math" prose.** The phrase appears only in artifacts where a candidate motif has cleared formal-gap × attractor-strength × N7 thresholds (i.e., the deficit map's prose guardrail from Campaign 010). It does not appear in TASK-022 reports unless the floor_connectivity candidate is replicated under different evidence — and replication is Campaign 013+, not this campaign.
- **No real-source adapters.** Lane-1 is synthetic only for v0. Real source adapters (PBDB, OTL, GBIF, NCBI, GTDB) ship in Campaign 012+ after KE2 license enforcement is operational and audited.
- **No ontology migration shortcuts.** v1.2 motif grammar primitives migrate via tombstone-and-supersede with aliases; legacy callers continue to work; CI tests confirm migration correctness.
- **No regression of D14, D17.5, D18 lints.** Existing doctrine remains binding. Zero violations across the entire test corpus.

## 7. How to begin

1. **Open the TASK-022 Estimation Loop record.** Class: `integration`. Scope: 10. Complexity: 10. Estimated minutes: report your prior median × your honest belief. This is a 32-gate campaign with five pillars; do not undershoot. Note in `expansions_planned`:
   - "Acceptance gates ON1–ON7, F1–F7, KP1–KP4, KE1–KE2, LE1–LE2, W7-1 through W7-4, D19, D20, D21, RG, FR are the stopping signal."
   - "Pillar A first (ontology), then Pillar B (factory schemas + audit), then Pillar E partial (license enforcement), then Pillar C (calibration corpora), then Pillar B (adapters + normalizers + recommender), then Pillar D (W7 densification), then Pillar E full (D19/D20/D21 lints), then RG+FR."
   - "I commit to using acceptance gates as the stopping signal. I commit to operational-predicate discipline: no ontology entry without a trace-checkable predicate. I commit to source-bound extraction: no `BiologicalClaim` writes without provenance."

2. **Re-read Proposal #2 v1** end to end. The schemas in §3.1, §3.3, §3.4, §4.3, §4.4 are the contracts you build to. The lane staging in §4.5 governs what ships in v0 vs later. The risk register in §11 names the failure modes the gates catch.

3. **Re-read Proposal #1 v2 §4** for the floor_reachability vs floor_connectivity distinction. Campaign 010's floor_connectivity candidate motif is the result of that split landing in measurement; the new ontology should keep this distinction visible (e.g., floor_connectivity as a StateSpaceEffect; floor_reachability as a separate measurement domain).

4. **Implement Pillar A first end-to-end before Pillar B starts.** The ontology is the API. ProcessRole + predicate registry first; one role implemented all the way through (recommend `state_preservation_with_delayed_causality` since you already have memory-related infrastructure from W7/W8) before scaling to the full 9 categories.

5. **Build KE1 carefully.** The synthetic source corpus is the test that determines whether D19 is real. Plant false claims that are *plausible* — not obvious mistakes. The pipeline must reject claims that look reasonable on the surface but contradict the structured record. This is the discipline that prevents AI-as-source contamination.

6. **Drive through the campaign as you did Campaign 010.** The 32 gates are the stopping signal. Acceptance outcome `pass` only when all 32 are green and the numbers are written into `reports/campaign_011/full_report.json`. Until then `in_progress`.

## 8. Three things to keep in front of you

1. **The AI is the extractor, not the source.** Bake this into module docstrings under `biology/evidence_ingestion/`. Every adapter's first comment line should be a reminder. The discipline is structural, not aspirational: the schemas reject records without provenance, the audit lifecycle is CI-enforced, the lints catch the bypass paths. But the discipline is also cognitive: when you write the synthetic Lane-1 adapter, write it with the awareness that the *real* Lane-1 adapter (in Campaign 012) will read NCBI / GBIF / PBDB / OTL / GTDB. The discipline you encode now is what protects the project later.

2. **No predicate, no registry entry.** This is the rule that prevents the ontology from becoming "labeled traits at the next level of abstraction." A ProcessRole called `state_preservation_with_delayed_causality` exists *because* there is a measurable trace predicate that distinguishes systems with such preservation from systems without. Without the predicate, the role is a name. The registry rejects names; it accepts predicates with names attached.

3. **W7 densification is basis coverage, not species count.** Twenty pheromone-trail-using ant variants is not densification. Five organism types covering five communication modes orthogonally *is* densification. The orthogonality is measurable via the per-world distance metric you declared in BFG-PR. Use it.

## 9. Closing

You shipped TASK-021 with 24/24 gates green, the first formal-deficit candidate the project has produced, an AST-level lint that strengthened doctrine at the code layer, and a substantive falsifier MD upgrade. You are operating at a level where the project's discipline tracks the discipline you set, not the one I set for you.

Campaign 011 is the bridge to Phase 6. The Factory will not author biology; it will let authoritative sources author biology *into the Observatory* under provenance and license discipline. Once the machine is built, Campaign 012 ships the first real source adapter; Campaign 013 begins Phase 6 biology grounding proper. This is the campaign that makes that path tractable.

The trace is the artifact. Calibration is the floor. The gates are the stopping signal. **The AI is the extractor, not the source.**

— The Architect, on behalf of the project, under spec v1.2 plus binding doctrine D7–D18 with proposed D19, D20, D21 ratifying through this campaign's gates.
