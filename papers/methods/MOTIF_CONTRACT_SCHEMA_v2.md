# Motif Contract — Schema v2 (RATIFIED)

**Status:** Three-way consensus locked. PI ratified, Architect Claude ratified, Codex 1.5x co-authored. Ready for implementation.
**Predecessors:** `MOTIF_CONTRACT_SCHEMA_DRAFT.md` (v1, Architect first draft) → `MOTIF_CONTRACTS_v1_DRAFT.md` (Codex co-author with amendments) → this document.
**Doctrine binding:** D26 (Predicate-Lens Independence) ratifies on this campaign's worked example. Class 13 (Predicate-Detector Surface Coupling) ratifies from candidate to active.

---

## What changed from v1

Two additions from PI ratification:

1. **`source_object_map`** is a required field on both predicate and per-lens entries. Independence verdict (CLEAN / PARTIAL / BAD) is now **mechanically derived from source-object comparison**, not interpretive.
2. **Four-state predicate verdict** replaces binary positive/negative. `insufficient_evidence` and `invalid_malformed` are first-class states that exclude a trace from the substrate-blocked corpus rather than silently collapse to negative.

Plus all of Codex's v1 amendments accepted: type fix on semantic definition (X_S species support), promotion-gate direction fix (original gap > shuffled CI upper bound), four-axis adversarial controls (event-token + state-key + payload-key + generator-id), W6/W11 marked EXPLORATORY via `mapping_status`, floor-connectivity historical split (BFG predicate vs C020 label function).

---

## The schema

### `MotifContract.v2`

```yaml
motif_id: string
contract_version: "2"
signed_at: ISO_UTC
signed_by: list[agent_id]    # PI, Architect Claude, Codex 1.5x
content_hash: sha256

# 1. Semantic definition
# What the motif IS, abstractly. NO event-token vocabulary. NO surface-string
# matching. Operates one layer above event tokens — set theory, topology,
# graph reachability, information channel, behavioral recovery, phylogenetic
# descent, etc. Type-safe (predecessor v1 had a type bug — Codex caught it).
semantic_definition: prose

# 2. Allowed evidence
# Specific structural / behavioral features the predicate may read. Each item
# names the feature AND the trace component it's computed from. Source MUST
# be a structural object (reaction graph, perturbation outcomes, state-space
# trajectory, etc.), NOT the event stream surface.
allowed_evidence: list[feature_with_source]

# 3. Forbidden evidence
# Specific shortcuts the predicate must NOT use. Anti-patterns named
# operationally with the actual leaking surface (event-token names, state-key
# patterns, generator IDs, scenario labels, frequency proxies). Must include
# every feature any of the 8 lenses uses, with substantive-difference
# justification.
forbidden_evidence: list[anti_pattern_with_reason]

# 4. Predicate abstraction layer
# Where the predicate operates. Concrete declaration matched to source_object_map (§5).
predicate_abstraction_layer: layer_declaration

# 5. source_object_map (NEW IN v2)
# REQUIRED. Per-predicate AND per-lens declaration of source objects read +
# fields read from each. Independence verdict CLEAN / PARTIAL / BAD derives
# mechanically from set-comparison.
predicate_source_object_map:
  - source_object: string       # "trace.reaction_declarations" / "trace.events" / etc.
    type: string                # "list[ReactionDecl]" / "list[Event]" / etc.
    fields_read: list[string]   # ["reactants", "products", "stoichiometry"]

# Lens abstraction layer with mandatory source_object_map per lens.
# Independence verdict is COMPUTED, not asserted:
#   CLEAN   if predicate.source_object set ∩ lens.source_object set == ∅
#   PARTIAL if predicate.source_object set ∩ lens.source_object set ≠ ∅
#           AND predicate.fields_read ∩ lens.fields_read == ∅ for every shared object
#   BAD     if predicate.source_object set ∩ lens.source_object set ≠ ∅
#           AND any shared source_object has predicate.fields_read ∩ lens.fields_read ≠ ∅
#
# Disposition:
#   CLEAN   → lens included in this motif's substrate-blocked control by default.
#   PARTIAL → lens included ONLY after ablation harness passes (feature-removal
#             test where the shared source_object is denied to the lens; lens
#             must still produce meaningful evaluation; if it collapses, the
#             cell reclassifies as BAD).
#   BAD     → lens excluded from this motif's substrate-blocked control.
#             Cell documented; future refactor may upgrade to PARTIAL or CLEAN.
lens_abstraction_layer:
  graph:
    features: list[string]
    source_object_map: list[source_object_entry]   # same shape as predicate_source_object_map
    shares_input_with_predicate: CLEAN | PARTIAL | BAD   # COMPUTED, not asserted
    justification: prose
  crnt: { same shape }
  dynamical_systems: { ... }
  topology: { ... }
  petri: { ... }
  statistical_mechanics: { ... }
  control_theory: { ... }
  information: { ... }

# 6. Invariance requirements
# Specific invariances; each gets a fixture in §7.
invariance_requirements: list[invariance_declaration]

# 7. Decoy controls (FOUR-AXIS, expanded from v1)
# At minimum:
#   - event_token_rename:    consistent rename of every event token to distinct synonyms
#   - state_key_rename:      consistent rename of every state-dict key
#   - payload_key_rename:    consistent rename of every payload-dict key
#   - generator_id_erasure:  strip generator IDs / benchmark-strings from metadata
# Plus motif-specific adversarial pairs (e.g., autocatalytic_closure adds
# "two networks with same event counts but opposite closure verdicts").
# Predicate verdict must be identical across all axes; any divergence = contract failure.
decoy_controls: list[control_with_fixture]

# 8. Promotion requirements
# Direction-correct gate (Codex caught v1 inversion).
promotion_requirements:
  - "All decoy controls pass on ≥30 traces per substrate"
  - "Original decoupled-predicate gap > shuffled CI upper bound under
     within-substrate permutation at N=10,000"
  - "≥3 substrates show predicate-positive results from independently-sourced
     corpora WITH mapping_status: source_bound (EXPLORATORY substrates do not
     count toward this gate)"
  - "Content-hash-signed contract; AI Operations Tower displays contract hash"
  - "Substance audit signed per substrate"

# 9. Known failure modes
known_failure_modes: list[class_with_guard]

# 10. Empirically-positive worlds (NEW: mapping_status field)
# DOI/PMID proves substrate phenomenon exists, NOT that the project's predicate
# captures it. mapping_status separates the two.
empirically_positive_worlds:
  - world_family: string
    instances: list[instance_description]
    citations: list[doi_or_pmid]
    mapping_status: source_bound | EXPLORATORY
    substance_audit_signed: bool

# 11. Verdict states (NEW IN v2)
# Four-state, not binary. Substrate-blocked control EXCLUDES the bottom two
# from the corpus rather than silently treating them as negative.
verdict_states:
  positive:               # semantic conditions met
  negative:               # semantic conditions evaluated AND not met
  insufficient_evidence:  # required source objects missing/under-populated
  invalid_malformed:      # source objects present but structurally invalid
```

---

## Independence verdict — operational rule

Given a predicate's `source_object_map` and a lens's `source_object_map`:

```python
def derive_independence_verdict(pred_som, lens_som) -> Literal["CLEAN", "PARTIAL", "BAD"]:
    pred_objects = {entry["source_object"] for entry in pred_som}
    lens_objects = {entry["source_object"] for entry in lens_som}
    shared_objects = pred_objects & lens_objects

    if not shared_objects:
        return "CLEAN"

    for obj in shared_objects:
        pred_fields = set(_fields_for(pred_som, obj))
        lens_fields = set(_fields_for(lens_som, obj))
        if pred_fields & lens_fields:
            return "BAD"
    return "PARTIAL"
```

Codex implements this in `formalism/motif_contracts/independence.py` as part of TASK-MOTIF-IMPL.

**Disposition by verdict:**
- **CLEAN** → lens evaluated in substrate-blocked control by default.
- **PARTIAL** → lens evaluated ONLY after the ablation harness proves it doesn't degenerate when the shared source object is denied (feature-removal test). If it degenerates, reclassify to BAD.
- **BAD** → lens excluded from this motif's substrate-blocked control. Documented in the contract. Cell becomes a candidate for refactor in a future campaign.

This is the operational form of D26.

---

## Doctrine ratification (this campaign closes both)

### D26 — Predicate-Lens Independence (binding)

> Every claim-bearing motif evaluation must be backed by a `MotifContract.v2` whose `source_object_map` analysis confirms predicate independence from the lenses used in its substrate-blocked control. Lenses with shared source objects + shared fields_read (BAD) are excluded; lenses with shared source objects but disjoint fields_read (PARTIAL) require ablation-harness verification. The independence verdict is mechanical (set comparison), not interpretive.

### Class 13 — Predicate-Detector Surface Coupling (active mistake class)

> A failure mode where the function defining a motif's labels and the function computing a lens's features both read the same surface-level features of a trace (typically event-token vocabulary, state-key names, generator IDs, or scenario labels). The substrate-blocked control then validates correlation between two views of the same encoding, not independent detection of the motif. Worked example: C020 sweep returned 5/5 motif survival under within-substrate shuffle at N=10,000 — arithmetically correct, methodologically circular. Cross-link: Class 7 (Surface-labels-as-primitives) is the same failure at the ontology layer; Class 13 is its expression at the methodology layer.

---

## The autocatalytic_closure exemplar (Codex's amended version preserved)

For brevity, the autocatalytic_closure exemplar at full depth lives in `MOTIF_CONTRACTS_v1_DRAFT.md` lines 196–338 — accepted verbatim with the v2 schema additions applied during implementation:

- Add `predicate_source_object_map` populated as: `[{source_object: "trace.reaction_declarations", type: "list[ReactionDecl]", fields_read: ["reactants", "products", "stoichiometry"]}, {source_object: "trace.parameters.food_set", type: "list[species_id]", fields_read: ["species_ids"]}, {source_object: "trace.parameters.catalysis_relation", type: "Mapping[reaction_id, list[species_id]]", fields_read: ["catalyst_species"]}]`
- Add per-lens `source_object_map` for each of the 8 lenses; let `derive_independence_verdict()` compute CLEAN/PARTIAL/BAD mechanically. Codex's existing PARTIAL flags on graph / CRNT / Petri should fall out of the rule (they share `trace.reaction_declarations` and read overlapping fields like reactant/product/stoichiometry).
- Add `verdict_states` block with the four states.

The other five contracts (self_maintained_boundary, repair, externalized_memory, replication_lineage, floor_connectivity-BFG) Codex drafted in `MOTIF_CONTRACTS_v1_DRAFT.md` and are accepted; same v2 additions apply during implementation.

---

## Floor connectivity — historical split (binding for implementation)

There are two distinct predicates calling themselves "floor_connectivity" in the project's history:

- **BFG predicate** (older, Campaign 009/010 era): perturbation equivalence fibers; basin-floor reachability geometry. Codex's v1 review classifies this as **structurally clean** — its source objects are perturbation-outcome distributions, not reaction declarations or event streams. This is the canonical floor_connectivity predicate.
- **C020 label function** (later): uses `neutral_component_fraction`, `nested_lineage_edges`, `attention_entropy`, `neutral_percolation_event` — surface-key coupled. **Deprecated in this campaign.** Routed to candidate-tier or removed from the active registry.

The floor_connectivity contract under v2 ratifies the BFG predicate, NOT the C020 label function. The Campaign 016 floor_connectivity death (p = 0.9075) **stands ONLY if it was evaluated against the BFG predicate**. Codex verifies this in TASK-MOTIF-IMPL T5 and reports honestly; if C016 used the C020-style label function, the death is methodologically contaminated and re-runs under the BFG predicate.

---

## What's locked, what's open

**Locked:** Schema v2, the 6 contracts as drafted in v1 with v2 additions applied at implementation time, D26 + Class 13 ratification, four-axis adversarial controls, mapping_status field, four-state verdicts, BFG-vs-C020-label split for floor_connectivity.

**Open:** Implementation. Codex's TASK-MOTIF-IMPL ticket builds the predicates, adversarial harness, ablation harness, runs substrate-blocked re-runs, updates `formal_deficit_map.json`, ratifies D26 + Class 13 in the registry.

After TASK-MOTIF-IMPL lands and the Destroyer pass-2 validates, the project has methodologically defensible substrate-blocked verdicts for the first time.

---

*— Schema v2 ratified by James Dye (PI), Architect Claude, Codex 1.5x. May 2026.*
