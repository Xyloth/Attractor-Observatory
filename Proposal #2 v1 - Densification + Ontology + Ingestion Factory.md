# Proposal #2 v1 — World Densification, Substrate-Neutral Ontology, and the Research Ingestion Factory

*Architect synthesis of two PI/GPT addendums into one candidate v1.3 spec section. Status: candidate v1.3 spec addition; queued as Campaign 011 once accepted.*

---

## 0. Status, audience, lineage

**Status:** candidate v1.3 spec addition. Architectural review complete; ready for ratification + Campaign 011 build.

**Audience:**
- Claude (Architect): structural review, doctrine integration, risk register.
- Codex (Builder): schema design, ingestion pipeline implementation, calibration corpora, audit lifecycle, license enforcement, W7 first densification.
- GPT (Theorist): research strategy review, claim discipline, novelty positioning.
- Project PI: ratification, signing.

**Lineage:**
- Proposal #1 v2 (Basin-Floor Geometry) introduced floor_reachability vs floor_connectivity as separate measurements. Campaign 009 implemented the basin-floor machinery; Campaign 010 surfaced `motif.floor_connectivity.draft` as the first formal-deficit candidate.
- PI/GPT addendum #1 ("World Densification, Process Roles, Interaction Channels, Overlap Fields") proposed substrate-neutral ontology primitives.
- PI/GPT addendum #2 ("Research Ingestion Factory") proposed the sourcing mechanism.
- Architect review concluded the two addendums are one proposal: the Ingestion Factory is the *sourcing mechanism* for the Process Role / Channel / Overlap Field schemas. They share schema, share doctrine, share calibration discipline.
- This document is the merged synthesis.

---

## 1. The doctrine arc

The project's doctrine has accumulated under live pressure from observed failure modes. The arc is not random. Each rule catches an instrument-honesty failure mode at a different layer:

| Layer | Doctrine | Failure mode caught |
|---|---|---|
| Substrate honesty | D7 No toys | Stub worlds passing shape-checks |
| Substrate honesty | D8 No number-generator corpora | K-corpora that read their own answers |
| Substrate honesty | D14 No scenario-internal hardcoding | Worlds writing benchmark answers via conditional code paths |
| Measurement honesty | D9 No engineered pass criteria | Lens predictions as hand-tuned coefficients |
| Measurement honesty | D10 No hardcoded science | Schema-pressure scores via dictionary lookup |
| Measurement honesty | D12 Gates are measurements | Counts substituted for measurements |
| Measurement honesty | D13 Substance budgets honest | Width-not-depth disguised as scope expansion |
| Measurement honesty | D15 No engineered floor | Floor detectors reading labels |
| Measurement honesty | D16 Implementation-diversity is multi-scale | Single-cluster-radius entropy gameable |
| Measurement honesty | D17 Floor falsifiers are publishable | Inconvenient negatives discarded |
| Measurement honesty | D17.5 Substance floors are spec proxies | Line-floor gaming via padding |
| Analysis honesty | D11 Truth pass before new claims | Claims compounding on stale foundations |
| Analysis honesty | D18 No equivalence-basis drift | Floor detectors fitting the data after seeing it |
| **Evidence-sourcing honesty** | **D19 (proposed)** Source-bound extraction | **AI hallucination entering claim ledger** |
| **Evidence-sourcing honesty** | **D20 (proposed)** Extraction/detection separation | **Same-AI extraction contaminating subsequent detection** |
| **Substrate-discovery honesty** | **D21 (proposed)** Densification before claim-bearing | **Sparse worlds carrying claims they can't support** |

The arc completes the project's epistemic discipline. The instrument is honest at substrate, at measurement, at analysis, and now — with D19/D20/D21 — at the evidence sourcing and substrate-discovery layers. **The AI builds the instrument; the AI does not author scientific truth at any layer.**

Three canonical phrases describe the discipline:

> **The trace is the artifact.** *(substrate honesty)*
>
> **The AI is the extractor, not the source.** *(evidence-sourcing honesty)*
>
> **Sparse worlds validate the instrument; dense worlds feed the instrument.** *(substrate-discovery honesty)*

---

## 2. World Densification doctrine

### 2.1 The bottleneck Campaign 010 created

Campaign 009 surfaced W13 multiscale as a basin-floor point-attractor. Campaign 010 surfaced `motif.floor_connectivity.draft` as a formal-deficit candidate with N7 p = 0.002. Both results are real and honest. Both are *thin* — one motif, one world family, one campaign. Replication, cross-substrate confirmation, and held-out testing are the path from candidate to claim.

Replication requires more data. More data requires either more campaigns (slow, expensive in compute) or more world-internal cases per campaign (faster, but only if worlds are densified honestly). The current state of every world is "few canonical cases, validated under D7+D14." Sparse worlds have served the instrument-spine validation phase. They cannot carry L3+ claims.

The diagnosis: **the instrument spine is real; the world content is sparse; densification is the next bottleneck**.

### 2.2 The doctrine

**D21 — Densification before claim-bearing motif observations from a world family.**

A world cannot anchor a claim-bearing motif observation unless it carries a `WorldDensificationReport` showing process-role coverage, interaction-channel coverage, and overlap-field coverage above declared per-motif thresholds. Exploratory motif observations from sparse worlds remain fine; the discipline applies at the claim-bearing boundary.

This does not require all worlds to be densified before the project advances. It requires that *the worlds anchoring claim-bearing observations* have densification evidence on file. A claim-bearing motif observation citing a sparse world is a D21 violation regardless of how clean the substance audits are.

### 2.3 Density class as orthogonal property

The existing three-mode tagging (`foundational` / `exploratory` / `claim-bearing`) governs *artifact lifecycle*. Densification governs *empirical readiness of the world that produced the artifact*. They are orthogonal.

Each world carries a `density_class`:

- **`trace_valid`** — World contract honoured, traces verify, calibration corpora pass. Suitable for instrument-spine validation. Cannot anchor claim-bearing observations.
- **`exploratory_densified`** — Densification report exists; coverage above an exploratory threshold for at least one motif. Suitable for exploratory motif observations and for surfacing candidate motifs. Cannot yet anchor claim-bearing observations.
- **`claim_ready_densified`** — Densification report exists with coverage above claim-bearing threshold for the relevant motif and adversarial controls passed. Eligible for claim-bearing observations on that motif.
- **`densification_validated`** — `claim_ready_densified` plus an Architect-signed densification audit. The Substance Audit pattern applied to densification.

Mode tag and density class compose: a motif observation is `claim-bearing` only if (a) the artifact's mode tag is `claim-bearing` *and* (b) the source world's density class is `claim_ready_densified` or `densification_validated` for that motif.

### 2.4 Densification is not "add more stuff"

D21 does not authorize random feature accumulation. Densification means adding cases that are at least partially orthogonal along **process-role**, **interaction-channel**, and **overlap-field** axes (defined in §3 below). The orthogonality is measurable: pairwise distance under the per-world distance metric already declared in BFG-PR (Campaign 009), reported as a multiscale entropy curve over the type set, with declared lower bounds for "orthogonal-enough."

A world that adds twenty new ant-like species that all use chemical pheromone trails in the same process role has *not* densified — it has accumulated. A world that adds five organism types covering pheromone trail / direct contact / visual signal / vibration / no communication *has* densified, even though the count is smaller.

---

## 3. Substrate-neutral ontology

### 3.1 The four primitives

The motif registry currently has typed primitive roles (Source, Sink, Flow, Store, Boundary, Channel, Catalyst, Inhibitor, Template, Copy, Repair, Sensor, Actuator, Memory, Predictor, Selector, Reproducer, Cooperator, Parasite, Module, Controller per v1.2 §8.1). These are foundational but flat: they describe what a thing *is* without describing what it *does* in process-space.

The ontology adds four new primitive classes that supersede the v1.2 grammar primitives:

#### 3.1.1 ProcessRole

A **process role** is the function a trait or structure performs in the dynamics of a system, independent of its biological surface form.

Categories (each with sub-roles):

- **Access / Mobility** — state-space traversal, barrier bypass, range expansion, medium transition, vertical access, surface escape.
- **Sensing / Perception** — information horizon expansion, remote state detection, gradient detection, threat/resource prediction, signal discrimination.
- **Signaling / Communication** — state transmission, coordination, deception, recruitment, warning, mating, consensus formation.
- **Construction / Niche Writing** — environmental inscription, future constraint modification, externalized memory, habitat creation, overlap-field creation.
- **Energy Capture / Routing** — gradient capture, flow routing, conversion, storage, dissipation, resource concentration.
- **Boundary / Identity** — inside-outside distinction, selective exchange, self-maintenance, repair, identity persistence, nested individuality.
- **Memory / Inheritance** — state preservation, delayed causality, cross-generation transfer, environmental memory, externalized continuity.
- **Coordination / Collective Control** — distributed sensing, distributed action, task allocation, division of labor, collective repair, colony-level regulation.
- **Prediction / Control** — future-state compression, policy selection, error correction, adaptive control, planning, model-based behavior.

The categories are not exhaustive; the registry can extend.

#### 3.1.2 InteractionChannel

An **interaction channel** is the medium or pathway through which one system senses, alters, signals to, constrains, or couples with another system or environment.

Initial registry: chemical, visual, acoustic, mechanical, thermal, electrical, spatial, aerodynamic, hydrodynamic, genetic, ecological, social, symbolic, computational, environmental.

#### 3.1.3 StateSpaceEffect

A **state-space effect** is the structural transformation a trait or process imposes on the reachable, knowable, or writable state-space of the systems it touches.

Initial registry: reachable_space_expansion, long_range_adjacency, vertical_access, terrain_constraint_reduction, information_horizon_expansion, predictor_horizon_expansion, environmental_durability_extension, identity_durability_extension, externalised_continuity_creation, nested_identity_creation.

This category fills the v1.2 vocabulary gap that flight exposed: the existing motif vocabulary is dynamics-centric (closure, repair, replication, memory) without primitives for *topology of state-space*.

#### 3.1.4 OverlapField

An **overlap field** is a persistent region of shared environmental modification where multiple systems write, read, and adapt to each other's traces.

Plain definition:
> The world becomes memory.

Operational definition:
- A trace-detectable persistent environmental modification (writer system → modification);
- Persistence longer than a declared timescale;
- A trace-detectable causal coupling from the modification to a different agent's state evolution (modification → reader system);
- A counterfactual: if the modification were absent, the reader's behavior would measurably differ (causal control test).

Without all four — write, persist, read, counterfactual — an apparent overlap field is environmental coincidence, not a measured field.

Examples (each must satisfy the operational definition before entering the registry):
- pheromone trail field (ant writes; pheromone persists; ant reads; ablation experiment confirms causal coupling)
- beaver-modified watershed (writer; persistence; readers from multiple species; ablation if rare)
- coral reef ecosystem (multi-agent writing; long persistence; multi-agent reading)
- soil mycorrhizal network (fungal writing; long persistence; plant reading; ablation experiments published)
- atmospheric oxygen (cyanobacteria wrote it ~2.4 Gya; planet-scale persistence; aerobic respiration is the reader; counterfactual is the early-Earth anaerobic baseline)
- urban infrastructure (humans write; centuries of persistence; multi-species reading; ablation rare but observable in abandoned cities)

### 3.2 Operational predicate discipline

This is the rule that prevents the ontology from becoming "labeled traits at the next level of abstraction":

> **A ProcessRole, InteractionChannel, StateSpaceEffect, or OverlapField exists in the registry only if it has a trace-checkable predicate.** The predicate is a function `(trace, scope) → confidence ∈ [0, 1]` that consumes trace state, events, lineage, ledgers, or boundaries and returns a calibrated detection score. **No predicate = no registry entry.**

For a process role to be "remote state detection" rather than "has eyes," the predicate must measure *something the trace contains* that distinguishes a system that detects remote state from one that doesn't. Concretely: an event-stream signal where action choices correlate with environmental state at distance > declared threshold, with mutual information above noise floor.

This converts the ontology from a taxonomy into a measurement framework. The discipline is the same as motif registry: entries that cannot be measured cannot enter; entries that enter must pass calibration before they anchor claims.

### 3.3 TraitDecomposition schema

A `TraitDecomposition` binds a surface label (e.g., "flight," "eyes," "eusociality") to its substrate-neutral decomposition.

```
TraitDecomposition = {
  decomposition_id:        TraitDecompositionID,
  surface_label:           str,                                  # "flight"
  taxon_or_clade:          TaxonRef | None,
  process_roles:           list[ProcessRoleID],
  interaction_channels:    list[InteractionChannelID],
  state_space_effects:     list[StateSpaceEffectID],
  overlap_fields:          list[OverlapFieldID],
  preserved_invariants:    list[InvariantSpec],
  substrate_implementations: list[SubstrateImplementationRef],   # bird wings, bat wings, fixed-wing aircraft, ...
  decoy_or_confound_cases: list[DecoyRef],
  evidence_requirements:   EvidenceRequirementsSpec,
  source_provenance:       SourceProvenance,                     # which sources support this decomposition
  confidence:              float in [0,1],
  audit_status:            enum {raw_extracted, normalized_candidate, conflicted,
                                 needs_audit, audited_confirmed, audited_rejected,
                                 promoted_exploratory, promoted_claim_bearing, deprecated},
  spec_version:            ContentHash,
}
```

The `surface_label` is a UI affordance; the decomposition is the science. Surface labels are still legitimate descriptors — the rule is "no surface label can stand alone as evidence for substrate-neutrality." A `RegisteredMotif` may carry a surface name (e.g., "memory") *as long as* it carries the decomposition as evidence.

### 3.4 WorldDensificationReport schema

```
WorldDensificationReport = {
  report_id:               WorldDensificationReportID,
  world_family:            WorldFamily,
  organism_or_system_types: list[SystemTypeRef],
  process_role_coverage:   dict[ProcessRoleID, CoverageScore],
  interaction_channel_coverage: dict[InteractionChannelID, CoverageScore],
  overlap_field_coverage:  dict[OverlapFieldID, CoverageScore],
  state_space_effect_coverage: dict[StateSpaceEffectID, CoverageScore],
  orthogonality_matrix:    OrthogonalityMatrix,                  # multiscale entropy curve
  density_class:           enum {trace_valid, exploratory_densified,
                                 claim_ready_densified, densification_validated},
  per_motif_thresholds_met: dict[MotifID, bool],
  known_sparse_regions:    list[SparseRegionDescription],
  recommended_next_additions: list[WorldDensificationRecommendationRef],
  source_basis:            SourceProvenance,
  audit_status:            enum,
  spec_version:            ContentHash,
}
```

The report is required for any world that anchors claim-bearing motif observations. The audit lifecycle (raw → audited → promoted) applies the same way it applies to TraitDecomposition.

### 3.5 Migration from v1.2 motif grammar

The v1.2 §8.1 motif grammar primitives become a subset of the new ProcessRole registry. Migration:

| v1.2 grammar primitive | ProcessRole equivalent |
|---|---|
| Source | Energy Capture / gradient_capture |
| Sink | Energy Capture / dissipation |
| Flow | Energy Capture / flow_routing |
| Store | Memory / state_preservation |
| Boundary | Boundary / inside_outside_distinction |
| Channel | Energy Capture / flow_routing (when carrying flux) or InteractionChannel (when carrying signal) |
| Catalyst | Construction / future_constraint_modification |
| Memory | Memory / state_preservation_with_delayed_causality |
| Predictor | Prediction / future_state_compression |
| Selector | Prediction / policy_selection |

Old grammar primitive names are kept as aliases in the registry. Existing `RegisteredMotif` records carrying old primitives migrate via the registry's standard tombstone-and-supersede pattern.

---

## 4. The Research Ingestion Factory

### 4.1 The bottleneck and the response

The Observatory needs structured biological cases at a rate hand-curation cannot produce. A large amount of biology already exists in published research, trait databases, taxonomies, fossil databases, genome databases, and ecology datasets. The Factory ingests authoritative sources and converts them into provenance-bound candidate entries in the registries above.

> The AI is the extractor, not the source.

### 4.2 The pipeline

```
authoritative source
  → fetched via licensed adapter
  → parsed under content-hashed schema
  → extracted into BiologicalClaim records
  → normalized into ProcessRole / InteractionChannel / StateSpaceEffect / OverlapField references
  → bundled into TraitDecomposition candidates
  → confidence-scored
  → license-class-tagged
  → provenance-hashed
  → audit-status assigned (default: raw_extracted)
  → written to candidate evidence graph
  → optionally → WorldDensificationRecommendation generated
  → optionally → SimulationTemplate drafted
```

At no point in this pipeline does an AI extraction become claim-bearing without passing the audit lifecycle.

### 4.3 BiologicalClaim schema

```
BiologicalClaim = {
  claim_id:                 BiologicalClaimID,
  taxon:                    TaxonRef,                            # NCBI/OTL/GTDB ID
  taxon_rank:               enum,
  source_trait_label:       str,                                 # surface label as published
  claim_text:               str,                                 # excerpt from source, license-permitting
  normalized_claim_type:    enum {trait_presence, behavior_presence,
                                  ecological_interaction, morphological_feature,
                                  metabolic_capability, phenotype_observation, other},
  evidence_source:          SourceRef,
  evidence_location:        SourceLocation,                      # page, section, dataset row
  source_type:              enum {structured_database, peer_reviewed_article,
                                  textbook, dissertation, dataset, expert_commentary, other},
  extraction_method:        ExtractionMethodRef,                 # which adapter / which AI / which manual coder
  confidence:               float in [0,1],
  license_class:            enum LicenseClass,
  provenance_hash:          ContentHash,
  audit_status:             enum,
  conflicts:                list[BiologicalClaimID],             # claims this contradicts
  notes:                    str,
}
```

### 4.4 Candidate evidence graph

The Factory produces a graph, not a flat table.

**Nodes:** Taxon, TraitLabel, BiologicalClaim, ProcessRole, InteractionChannel, StateSpaceEffect, OverlapField, Source, EvidenceSnippet, SimulationTemplate, WorldDensificationRecommendation.

**Edges:** supports, contradicts, maps_to, decomposes_into, implemented_by, observed_in, suggests, requires_audit, derived_from, conflicts_with.

Graph queries the Factory must support:
- Which traits support the same process role?
- Which taxa share interaction channels?
- Which overlap fields recur across clades?
- Which world families are under-densified for a given motif?
- Which claims are contested?
- Which claims are well-sourced?
- Which extractions are stale?

### 4.5 Lane staging

The Factory is staged by hallucination risk:

- **Lane 1 — Structured data.** Taxonomy databases, trait databases, fossil occurrence, genome/metabolic databases, biodiversity occurrence, phylogenetic datasets. Outputs: taxon IDs, trait records, occurrence records, fossil time ranges, genome metadata, ecological associations. Lowest risk; ships first.
- **Lane 2 — Literature metadata + abstracts.** Article metadata, abstracts, indexed annotations. Outputs: candidate claim discovery, organism-trait co-occurrence, interaction-channel detection, source triage. **Exploratory only by default**; promotion requires audit.
- **Lane 3 — Legally available full text.** Mechanism extraction, trait decomposition, overlap-field evidence, interaction-channel detail. Highest risk; ships last; requires per-source license enforcement.

**Ship Lane 1 only for v0.** Lanes 2 and 3 require their own calibration corpora and explicit doctrine promotion before they enter service.

### 4.6 Audit lifecycle

```
raw_extracted
   ↓
normalized_candidate ─────→ conflicted ─────→ needs_audit
   ↓                                              ↓
needs_audit ──────────────────────────────→ audited_confirmed
   ↓                                              ↓
audited_confirmed ──→ promoted_exploratory ──→ promoted_claim_bearing
   ↓                                              ↓
audited_rejected                              deprecated
```

Discipline:
- `raw_extracted` ≠ true. The record exists; nothing depends on it.
- `normalized_candidate` ≠ true. The record has been through the schema normalizer; it is structurally valid; nothing scientific depends on it.
- `promoted_exploratory` is the *first* state where the record can flow into Observatory analysis, and only as `mode_tag: exploratory`.
- `promoted_claim_bearing` requires explicit signature (PI for biological claims; Architect for ontology decompositions).

Promotion gates are CI-enforced. The pipeline's CLI rejects any path that bypasses the audit lifecycle.

---

## 5. Doctrine D19, D20, D21

### 5.1 D19 — Source-bound extraction

> **D19 — Source-bound extraction.** No biological, ecological, or trait-derived variable may be promoted beyond exploratory status unless it is bound to a source, a provenance record, a license class, an extraction path, and an audit status. AI systems may extract, normalize, cluster, and recommend variables, but they are not evidence sources. The source remains the source.

**Failure mode caught:** AI hallucination of biology. Without D19, the project's claim ladder corrupts the moment an AI is asked "what do ants do?" and writes the answer into the registry.

**How enforced:** five layers of test, all binding from Campaign 011:
1. **Schema-level:** `claim_store.write()` rejects any record without source + provenance_hash + license_class + audit_status.
2. **Pipeline-level:** promotion CLI requires `audit_status = audited_confirmed`; rejects any path that bypasses.
3. **AST-level lint:** any code path creating a `BiologicalClaim` with `source: "ai_inferred"` (or equivalent) requires `mode_tag = exploratory`.
4. **Calibration-level:** KE1 corpus with planted false claims; pipeline must reject the planted claims at declared rate.
5. **Adversarial-level:** red-team prompts attempting to inject claims; pipeline rejects unprompted writes.

### 5.2 D20 — Extraction/detection separation

> **D20 — Extraction/detection separation.** The AI session that extracts a TraitDecomposition (or related ontology entry) from a source must not be the same AI session that detects that decomposition's process roles in a simulation trace, unless the extraction is content-hash-locked in the registry before the detection session begins and the detector explicitly declares which extraction-registry entries it consulted. Detectors that consult unlocked extractions fail D20 regardless of their measurements.

**Failure mode caught:** circular contamination. If the same AI extracts trait X from a paper and then detects trait X in a simulation, the extraction informs the detection — the detector can't help reading the trace through the lens of what it just extracted. This is a subtler version of the equivalence-basis drift D18 caught.

**How enforced:** content-hash lock on registry entries before detection runs; detector self-declarations of which entries consulted (logged and AST-checkable); session separation enforced at the AI orchestrator level.

D20 is the same pattern as D18 (basis-hash lock before detection runs) extended to the extraction layer.

### 5.3 D21 — Densification before claim-bearing

> **D21 — Densification before claim-bearing.** A world cannot anchor a claim-bearing motif observation unless it carries a `WorldDensificationReport` with declared coverage thresholds for the motif's relevant process roles, interaction channels, and overlap fields.

**Failure mode caught:** sparse-world claims. The recurrence experiment in Campaign 002 nearly happened with 8 seeds before audit caught it. D21 prevents the structural version of that risk: a world with two organism types and one interaction channel cannot anchor a claim about substrate-neutrality, regardless of how rigorous the detector is.

**How enforced:** mode-tag inheritance in provenance graph requires both (a) artifact `mode_tag = claim-bearing` and (b) source world `density_class >= claim_ready_densified` for the motif. CI lint catches violations.

---

## 6. Calibration corpora

The Factory and the ontology need calibration corpora the same way worlds and motif detectors do. Six new corpora ship in Campaign 011:

### 6.1 KP1–KP4 — process-role detection calibration

- **KP1 — Access/Mobility roles.** Synthetic worlds with planted access/mobility process roles: agents that traverse, bypass barriers, expand range. Detector reads trace; predicate accuracy measured.
- **KP2 — Construction/Niche-Writing roles.** Synthetic worlds with planted niche-construction patterns. Includes adversarial cases: agents that modify environment but the modification is environmental coincidence rather than written-and-read.
- **KP3 — Memory/Inheritance roles.** Synthetic worlds with state preservation, delayed causality, cross-generation transfer. Includes decoys: agents that *appear* to have memory but reproduce the same behavior from instantaneous state.
- **KP4 — Coordination/Collective Control roles.** Synthetic worlds with task allocation, division of labor, distributed sensing. Adversarial cases: apparent coordination from environmental coupling rather than agent-mediated control.

Each corpus has positive scenarios (planted ground truth), negative scenarios (planted absence), and adversarial decoys. Detector calibration target: ROC AUC ≥ 0.85, ECE ≤ 0.07.

### 6.2 KE1 — synthetic source corpus

A hand-authored fake taxonomy with known correct extractions plus *adversarial planted false claims*. The pipeline must extract correctly *and* reject the false claims. Reports ROC AUC and ECE for the extraction stage. This is the K-corpus discipline applied to the ingestion factory.

Example structure:
- 200 synthetic taxa with structured trait records.
- 30 of the 200 have a planted false claim ("species X has flight" when the record actually says "species X has wing scales").
- 10 have contradictory claims across two synthetic source files.
- The pipeline must extract the 200 taxa, identify the 30 false claims, and flag the 10 contradictions to the audit queue.

### 6.3 KE2 — license enforcement corpus

Synthetic restricted-source files with declared license classes. The export-guard must refuse to leak them through atlas pathways. Tests:
- Restricted-class data cannot appear in atlas exports.
- Derived statistics from restricted-class data carry the most-restrictive license class.
- A pipeline run that writes a restricted-class extraction to a public-class artifact triggers a CI failure.

---

## 7. WorldDensificationRecommendation

The Factory's primary v0 output. Not a biological claim; a recommendation for the simulation engine.

```
WorldDensificationRecommendation = {
  recommendation_id:            WorldDensificationRecommendationID,
  world_family:                 WorldFamily,
  recommended_cases:            list[OrganismOrSystemTypeRef],
  process_role_coverage_gain:   dict[ProcessRoleID, float],      # expected coverage delta
  interaction_channel_coverage_gain: dict[InteractionChannelID, float],
  overlap_field_coverage_gain:  dict[OverlapFieldID, float],
  orthogonality_rationale:      str,                             # why these cases are orthogonal
  source_basis:                 list[BiologicalClaimID],
  confidence:                   float in [0,1],
  audit_status:                 enum (defaults to raw_extracted),
  implementation_notes:         str,
  spec_version:                 ContentHash,
}
```

A recommendation is *exploratory* until audited. The simulation case it suggests is implemented under D14 and tested for trace validity; the source citation that motivated the recommendation remains exploratory until promoted.

---

## 8. W7 swarm as first densification target

W7 is the cleanest first target:
- **Well-studied taxa** (ants, bees, termites, wasps; broad literature; structured trait databases exist for major species).
- **Clear overlap fields** (pheromone trails are the canonical stigmergy example).
- **Orthogonal axes available** (communication / organization / mobility / environment-modification / memory substrate).
- **Lower-risk literature** than W6 ecosystem (definitional boundaries clearer) or W8 cognitive (less contested mechanism debate).

### 8.1 Densification axes for W7

For Campaign 011's W7 first densification, target multi-axis coverage:

| Axis | Recommended values |
|---|---|
| Communication | pheromone trail, direct contact, visual signal, vibration, no communication |
| Organization | solitary, loose aggregation, eusocial colony, caste-based colony, temporary swarm |
| Mobility | crawling, flying, burrowing, aquatic, sessile/larval-phase |
| Resource strategy | foraging, farming, parasitism, predation, scavenging, pollination |
| Environment modification | none, trail deposition, nest construction, soil modification, host manipulation |
| Memory substrate | individual, pheromone field, nest architecture, environmental damage map, collective state |

A WorldDensificationReport for W7 demonstrates coverage along these axes. **Basis coverage, not biological completeness** — the goal is orthogonal-enough, not species-rich.

### 8.2 Expected output of Campaign 011

A first densification report showing:
- ≥10 organism/system types added to W7 covering ≥4 axes orthogonally
- WorldDensificationRecommendation entries for each, with source citations
- Process-role / channel / overlap-field coverage matrix populated
- Density class for W7 advanced from `trace_valid` to `exploratory_densified`

After Campaign 011, W7 is eligible for exploratory motif observations. `claim_ready_densified` requires Campaign 012 (further densification + Architect-signed audit).

---

## 9. Background-job discipline

The Factory naturally invites long-running local jobs. This is dangerous if not gated.

Rules from Campaign 011 onwards:
- **Default mode is `dry_run`.** Background runs do not write to the registry without explicit per-session authorization.
- **Batch sizes capped per run.** No run exceeds the declared cap without authorization.
- **Audit queue depth caps.** Background ingestion stalls when the audit queue exceeds depth threshold.
- **Modes beyond `candidate_generation` require explicit user authorization per session.** No silent mode escalation.
- **CI lint flags any code path that runs the Factory without honoring the dry_run default.**

The Factory is a research-acceleration tool. Its acceleration is bounded by audit throughput, not by ingestion speed.

---

## 10. Honest novelty positioning

Three of the four ontology concepts have direct ancestors. The proposal must cite them to avoid overclaiming:

- **ProcessRoles** — niche construction theory (Odling-Smee, Laland 2003), extended phenotypes (Dawkins 1982), affordance theory (Gibson 1979), mechanism schemas in philosophy of biology (Bechtel, Craver 2005).
- **InteractionChannels** — biosemiotics (Sebeok, Hoffmeyer), signaling theory (Maynard Smith & Harper 2003), sensory ecology (Dusenbery 1992).
- **OverlapFields** — stigmergy (Grassé 1959), niche construction (Odling-Smee, Laland), scaffolded cognition (Sterelny 2010), extended phenotype (Dawkins 1982).
- **World Densification doctrine** — this might be the most genuinely novel contribution. I am not aware of an ALife or theoretical-biology project that has codified validation-vs-discovery readiness with measurable density coverage as a binding gate.
- **The Research Ingestion Factory** — provenance-preserving extraction pipelines exist (BIOTIC, GLOBI, Encyclopedia of Life, GBIF data ingestion pipelines). The novel contribution is the binding doctrine D19 + D20, the audit lifecycle as a CI-enforced state machine, and the integration with operationally-defined process-role/channel/overlap-field schemas as the extraction targets.

The novel contribution overall is the *integrated discipline*: schema + ingestion + audit lifecycle + calibration + doctrine, applied to substrate-neutral measurement under an explicit operational-predicate rule.

---

## 11. Risk register

| ID | Risk | Mitigation |
|---|---|---|
| RP1 | Process-role taxonomy becomes "labeled traits at the next level of abstraction" | Operational predicate discipline: no predicate = no registry entry. KP1–KP4 calibration corpora gate registry entries. Inter-rater agreement reporting on TraitDecomposition. |
| RP2 | Ontology bloat: too many process roles, channels, fields | Registry semantic versioning with tombstones. Coverage gain required for new entries. Architect review before registry version bump. |
| RP3 | AI extraction hallucination enters claim ledger | D19 (source-bound extraction) with five-layer enforcement (schema, pipeline, AST, calibration, adversarial). |
| RP4 | Same-AI extraction contamination of subsequent detection | D20 (extraction/detection separation) with content-hash lock on registry entries before detection runs. |
| RP5 | License contamination (restricted-class data leaking through atlas) | KE2 calibration corpus + license-class enforcement module + provenance closure checks before any real source adapter. |
| RP6 | Garbage-in variable explosion from unaudited background runs | Dry-run defaults, batch caps, audit queue depth caps, per-session authorization for non-default modes. |
| RP7 | World densification becomes random feature accumulation | Orthogonality rationale required per recommendation. Multiscale entropy curve over type set with declared lower bounds. |
| RP8 | Sparse worlds anchoring claim-bearing observations | D21 (densification before claim-bearing) with provenance-graph enforcement. |
| RP9 | OverlapField becomes vague | Operational definition with write/persist/read/counterfactual. Counterfactual is the discriminator: a "field" without ablation evidence of causal coupling is environmental coincidence. |
| RP10 | TraitDecomposition becomes subjective | Inter-rater agreement reporting. KP1–KP4 calibration. Source provenance required. |
| RP11 | Claude-as-builder self-audit collapse during this work | Outputs default to `mode_tag: exploratory` until promoted. Mechanical tests around provenance/promotion. PI as primary reviewer. Codex retro-audit when usage returns. |
| RP12 | Doctrine bloat from this addition | The doctrine-arc story (§1) constrains future additions to specific failure-mode-catching at named layers. New rules require demonstrated bypass of existing rules. |

---

## 12. Campaign sequencing

```
NOW (Campaign 010 complete):
  - This proposal accepted/ratified
  - Codex resumes for Campaign 011

CAMPAIGN 011 — Research Ingestion Factory v0 + Substrate-Neutral Ontology + W7 First Densification:
  - Ontology schemas land under motifs/ontology/
  - Factory schemas land under biology/evidence_ingestion/
  - Audit lifecycle implemented and CI-enforced
  - License-class enforcement module operational
  - KP1-KP4 + KE1 + KE2 calibration corpora built and gated
  - Synthetic Lane-1 source adapter shipped
  - First WorldDensificationRecommendation report on W7
  - Doctrine D19 + D20 + D21 ratified

CAMPAIGN 012 — W7 Densification + One Real Lane-1 Source:
  - W7 advances from exploratory_densified to claim_ready_densified
  - One real structured-source adapter (likely a small public trait database)
  - Substance Audit on W7 densification
  - Architect-signed densification audit (densification_validated)
  - Lane 2 design (abstracts) but not yet shipped

CAMPAIGN 013 — Phase 6 Biology Grounding Beachhead:
  - Real OTL/PBDB/GBIF/NCBI/GTDB adapters
  - Phylogenetic correction
  - Sampling bias models
  - Held-out clades
  - First L3 candidate claims with full provenance

CAMPAIGN 014+ — Successive densification of remaining worlds, Lane 2 ingestion enabling, Phase 6 expansion.
```

---

## 13. Spec insertion drafts

### 13.1 New section in v1.3

```
Section X — World Densification, Substrate-Neutral Ontology, and Research Ingestion Factory

The Observatory distinguishes sparse validation worlds from dense discovery
worlds. Sparse worlds are acceptable during instrument validation; they cannot
support claim-bearing motif observations by themselves. Once a world family
has trace validity, calibration, detector compatibility, and falsifier routing,
it should enter a densification phase along partially orthogonal process-role,
interaction-channel, state-space-effect, and overlap-field axes.

Major biological labels (flight, sight, eusociality, nest-building, pheromone
use, memory) do not enter the system as claim-bearing primitives. They are
decomposed into process bundles. Surface labels remain legitimate descriptors;
they cannot stand alone as evidence for substrate-neutrality.

The Observatory maintains a Research Ingestion Factory that converts
authoritative sources into provenance-bound candidate variables. The AI is the
extractor, not the source. Every extracted variable carries source identity,
evidence location, extraction method, confidence, license class, provenance
hash, conflict status, and audit status. Extracted variables remain
exploratory until promoted through the audit lifecycle.

Doctrine D19 binds source-bound extraction; D20 binds extraction/detection
separation; D21 binds densification before claim-bearing observations.
```

### 13.2 Canon phrases

```
The trace is the artifact.
Calibration is the floor.
The gates are the stopping signal.

Sparse worlds validate the instrument.
Dense worlds feed the instrument.

Surface traits label what changed.
Process roles describe what the change does.
Interaction channels explain how systems couple.
Overlap fields explain where multi-system attractors live.

The AI is the extractor, not the source.
```

---

## 14. Bottom line

The previous addendum identified that surface traits cannot anchor substrate-neutrality. The new addendum identified that hand-coding biology is the wrong scaling path. Together, they are one architectural pivot:

> The Observatory builds the *machine that ingests biology* — under doctrine that prevents AI hallucination, license drift, ontology bloat, and sparse-world claim corruption — instead of asking AI to author biology one organism at a time.

With this in place:
- Phase 6 biology grounding becomes scalable.
- The L3 unlock has a defensible substrate-neutral evidence path.
- The L5+ candidate (`motif.floor_connectivity.draft` from Campaign 010) gets the replication infrastructure it needs.
- The doctrine arc completes: substrate honesty → measurement honesty → analysis honesty → evidence-sourcing honesty → substrate-discovery honesty.

Status: candidate v1.3 spec addition. Eligible to become Campaign 011 once accepted.

— The Architect, on behalf of the project, under spec v1.2 plus binding doctrine D7–D18 with proposed D19, D20, D21.
