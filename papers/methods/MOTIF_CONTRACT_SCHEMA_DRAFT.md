# Motif Contract — Schema v1 (DRAFT)

**Status:** Architect first draft, awaiting Codex 1.5x co-authorship + PI ratification (three-way consensus).
**Origin:** Required by the C020 methodology-leak finding (5/5 motif survival under substrate-blocked permutation suggested predicate-lens surface coupling). The Motif Contract artifact formalizes the structure that prevents predicate-lens space sharing and binds adversarial-control discipline to every motif before claim-bearing promotion.
**Doctrine context:** D26 (Predicate-Lens Independence) is a candidate doctrine that ratifies based on the success of the first Motif Contract round. **Class 13 (Predicate-Detector Surface Coupling)** is the catalog mistake-class this contract specifically guards against.

---

## Why this artifact exists

The C020 sweep ran substrate-blocked permutation (N=10,000, within-substrate label shuffle) on five motifs. All five "survived" (`signal_survives_shuffle`). On its face that's promotion-ready — but Codex 1.5x correctly diagnosed the verdict as suspect: *"locked labels and graph-lens features both depend heavily on event-token surfaces."*

Confirmed by inspection: every C020 evidence row's `locked_label_predicate` field reads `"formalism.lens_registry._label_feature_for_motif"` — the predicate that defines the label is the same function used by lenses to compute features. The substrate-blocked shuffle is testing correlation between two views of the same encoding, not independent detection of the motif. The arithmetic is correct; the test isn't testing what we said it was testing.

The Motif Contract decouples the layers. Each motif gets a single per-motif document declaring its *semantic definition*, its *predicate abstraction layer*, its *lens abstraction layer* (with the constraint that the two layers must be substantively different), the *invariances the predicate must satisfy*, the *adversarial controls* that prove independence, the *promotion requirements* that gate claim-bearing, the *known failure modes* it guards against, and the *empirically-positive worlds* with peer-reviewed citations for each.

Without this artifact, the C020 leak recurs every time we add a motif. With this artifact, predicate-lens independence is a structural requirement, verifiable by automated controls, and every motif's evidence chain traces to peer-reviewed sources.

---

## The schema

### `MotifContract.v1`

```yaml
motif_id: string                        # canonical motif id, e.g. "motif.autocatalytic_closure.draft"
contract_version: string                # "1" for the initial round
signed_at: ISO_UTC                      # when contract was ratified
signed_by: list[agent_id]               # human + AI signatories (PI, Architect, Codex 1.5x)
content_hash: sha256                    # over canonical JSON of all fields below

# 1. Semantic definition
# What the motif IS, abstractly. NO event-token vocabulary. NO surface-string
# matching. The definition operates at the LAYER ABOVE event tokens — set
# theory, topology, graph reachability, information channel, behavioral
# recovery, phylogenetic descent, etc. The semantic definition is the source
# of truth; the predicate is its executable instance.
semantic_definition: prose

# 2. Allowed evidence
# Specific structural / behavioral features the predicate may read. Each item
# names the feature AND the trace component it's computed from (reaction graph,
# state-space trajectory, perturbation-outcome distribution, etc.).
allowed_evidence: list[feature_with_source]

# 3. Forbidden evidence
# Specific shortcuts the predicate must NOT use. Each item names a concrete
# anti-pattern (event-token name, surface vocabulary string, frequency-of-keyword
# count, trace-length proxy, etc.). The list must include every feature that
# any of the 8 lenses uses, with a justification of the substantive difference.
forbidden_evidence: list[anti_pattern_with_reason]

# 4. Predicate abstraction layer
# Where the predicate operates. Concrete declaration: "Set theory on reaction
# graphs", "Persistent homology on state-space trajectories", etc. The layer
# must be substantively different from every lens's layer (declared in §5).
predicate_abstraction_layer: layer_declaration

# 5. Lens abstraction layer
# Per-lens declaration of what features that lens uses for this motif, AND
# whether those features share input space with the predicate. Required for
# all 8 lenses (graph, CRNT, dynamical_systems, topology, Petri, statistical
# mechanics, control_theory, information). Any lens with input-space overlap
# triggers a Class 13 violation and must be either (a) refactored or (b) excluded
# from this motif's substrate-blocked control.
lens_abstraction_layer:
  graph: { features: [...], shares_input_with_predicate: bool, justification: prose }
  crnt: { features: [...], shares_input_with_predicate: bool, justification: prose }
  dynamical_systems: { ... }
  topology: { ... }
  petri: { ... }
  statistical_mechanics: { ... }
  control_theory: { ... }
  information: { ... }

# 6. Invariance requirements
# List of invariances the predicate must satisfy under structural transforms.
# Each invariance gets a specific test fixture in §7.
invariance_requirements: list[invariance_declaration]

# 7. Decoy controls
# Specific adversarial fixtures the predicate must pass before any
# operational-tier promotion. At minimum: token-rename (every event token
# consistently renamed; verdict identical), decoy-injection (≥10% spurious
# events; verdict identical), permutation (reorder predicate inputs; verdict
# identical), synonym-replacement (replace strings with synonymous distinct
# strings; verdict identical). Any control failure → predicate fails the
# contract; not promotable.
decoy_controls: list[control_with_fixture]

# 8. Promotion requirements
# What evidence threshold gates claim-bearing. At minimum: all decoy controls
# pass on a corpus of ≥30 traces per substrate; substrate-blocked permutation
# at N=10,000 with the decoupled predicate yields shuffle-distribution gap <
# CI lower bound; ≥3 substrates show predicate-positive results from
# independently-sourced corpora; content-hash signed Motif Contract; AI
# Operations Tower displays the contract hash; substance audit signed per
# substrate.
promotion_requirements: list[gate_with_threshold]

# 9. Known failure modes
# Cross-link to Mistake Catalog classes this contract guards against.
# Required: name every catalog class that could express itself in this
# motif's evidence chain, and how the contract's structure prevents it.
known_failure_modes: list[class_with_guard]

# 10. Empirically-positive worlds
# Substrates with peer-reviewed instances of this motif. Each entry MUST cite
# at least one DOI or PMID. AI-derived process-role assignments without sources
# are NOT acceptable here — this field is the entry point for operational-tier
# evidence, and every record must be source-bound.
empirically_positive_worlds:
  - world_family: "W1"
    instances: list[instance_description]
    citations: list[doi_or_pmid]
    substance_audit_signed: bool
  - world_family: "W3"
    ...
```

---

## Architect's exemplar — `motif.autocatalytic_closure.draft`

This is a starting reference, not a final contract. Codex 1.5x reviews and amends.

```yaml
motif_id: motif.autocatalytic_closure.draft
contract_version: "1-architect-draft"
signed_at: <pending three-way consensus>
signed_by: <pending: PI, Architect Claude, Codex 1.5x>
content_hash: <computed at finalization>

semantic_definition: |
  A set of reactions S such that:
  (a) every species consumed by some reaction in S is produced by some other
      reaction in S, OR is supplied by a designated food set F;
  (b) S is reachable from F under mass-action kinetics (every reaction in S
      can fire given F's initial concentrations and the products of prior
      firings within S);
  (c) S is closed under reaction-product application — applying any reaction
      in S to its inputs produces only products in S ∪ F.

  Equivalent to a maximal RAF (reflexively-autocatalytic and food-generated)
  in the Hordijk-Steel formalism, under appropriate food-set and catalyst
  conditions.

allowed_evidence:
  - feature: "Reaction-graph bipartite structure (species × reactions)"
    source: "Trace's reaction declaration block, NOT the event stream"
  - feature: "Set-theoretic closure check: for each reaction r in candidate S,
      verify all reactants ∈ S ∪ F and all products ∈ S ∪ F"
    source: "Reaction-graph traversal"
  - feature: "Reachability path from food set F to candidate S under mass-action"
    source: "Reaction-graph + initial concentrations from trace parameters"
  - feature: "Hordijk-Steel maxRAF algorithm output on the reaction network"
    source: "worlds/crn/raf.py existing implementation"
  - feature: "Per-reaction species-balance verification (mass conservation)"
    source: "Reaction stoichiometry from trace declarations"

forbidden_evidence:
  - anti_pattern: "Matching event-stream tokens like 'closure_event',
      'autocatalytic_step', 'raf_detected'"
    reason: "Surface vocabulary match; bypasses semantic check; would fail
      token-rename invariance"
  - anti_pattern: "Counting frequency of any event_type"
    reason: "Frequency-of-keyword is a lens-level feature; predicate must
      operate on graph structure, not event statistics"
  - anti_pattern: "Trace-length proxies (longer traces → closure more likely)"
    reason: "Closure is structural, not emergent over time; latent C020 leak"
  - anti_pattern: "Any feature also computed by graph-lens cycle detection,
      CRNT-lens deficiency analysis, or dynamical_systems-lens limit-cycle
      classification"
    reason: "Predicate must operate on a layer ABOVE these lenses' feature
      spaces; sharing input space triggers Class 13"

predicate_abstraction_layer: |
  Set theory on reaction graphs. The predicate operates on the bipartite graph
  (species, reactions) extracted from the trace's reaction declarations. It
  does NOT read the event stream. It does NOT count tokens. It computes
  semantic membership: "is there a non-empty subset S of reactions such that
  S satisfies the closure conditions in §1?"

lens_abstraction_layer:
  graph:
    features: ["cycle structure", "centrality", "community detection",
      "node/edge counts on the reaction graph"]
    shares_input_with_predicate: false
    justification: |
      Graph-lens reads cycle structure on the reaction graph; predicate reads
      set-membership closure on the same graph. Both are graph-derived but the
      computations are non-overlapping: cycle structure ≠ closure (a cycle
      isn't necessarily closed under products; a closed set isn't necessarily
      cyclic in the graph-theoretic sense). Verifiable by token-rename test:
      both invariant under rename; cycle structure independent of closure
      verdict on representative test corpus.
  crnt:
    features: ["deficiency", "weak reversibility", "linkage class structure"]
    shares_input_with_predicate: false
    justification: |
      CRNT operates on the same reaction-network structure but computes
      Feinberg-network-theoretic invariants (deficiency δ = n - ℓ - s where
      n is complexes, ℓ is linkage classes, s is rank of stoichiometric
      subspace). These are orthogonal to closure-set membership. δ=0 networks
      can be closed or not; closed networks can have any δ.
  dynamical_systems:
    features: ["fixed-point classification", "limit-cycle detection",
      "strange-attractor classification on the reaction-network ODEs"]
    shares_input_with_predicate: false
    justification: |
      DS lens runs the reaction-network ODEs and classifies the asymptotic
      behavior of the trajectory. Closure is a network-structural property,
      independent of dynamical asymptotics — a closed network can have any
      asymptotic behavior; non-closed networks can have limit cycles.
  topology:
    features: ["persistent homology of state-space trajectories"]
    shares_input_with_predicate: false
    justification: |
      Topology lens computes persistence diagrams over state-space; predicate
      computes set membership over reaction graph. Different domains.
  petri:
    features: ["Petri net liveness, boundedness, reachability over the
      reaction net"]
    shares_input_with_predicate: PARTIAL
    justification: |
      Petri reachability touches the same notion as the predicate's
      reachability check from F to S. POTENTIAL Class 13 risk. Recommendation:
      Petri lens features for this motif should be specifically restricted to
      liveness + boundedness, NOT reachability. Architect flags for Codex
      review.
  statistical_mechanics:
    features: ["partition-function approximations over reaction-network
      configuration space"]
    shares_input_with_predicate: false
    justification: |
      Statistical-mechanics lens computes thermodynamic / ensemble properties.
      Different domain than set-theoretic closure.
  control_theory:
    features: ["controllability / observability of the reaction-network
      ODEs as a control system"]
    shares_input_with_predicate: false
    justification: |
      Control lens treats the reaction network as a state-space system with
      inputs/outputs; predicate treats it as a discrete reaction graph.
      Different domains.
  information:
    features: ["mutual information between reaction firings"]
    shares_input_with_predicate: false
    justification: |
      Information lens computes statistical dependence between events;
      predicate computes structural closure. Different domains. Verifiable
      by decoy-injection test: information-lens features change under decoy
      injection; predicate verdict invariant.

invariance_requirements:
  - name: "Token-rename invariance"
    description: "Predicate verdict unchanged under consistent rename of all
      event tokens (e.g., 'reaction_fired' → 'transformation_x')"
  - name: "Reaction-id permutation invariance"
    description: "Predicate verdict unchanged under reordering of reaction IDs
      in the reaction declaration block"
  - name: "Species-renaming invariance"
    description: "Predicate verdict unchanged when species names are
      consistently renamed"
  - name: "Decoy resistance"
    description: "Inserting non-causal noise events doesn't flip the verdict"
  - name: "Trace-length invariance"
    description: "Predicate verdict on the first 50% of a trace agrees with
      verdict on the full trace (closure is structural, not late-emergent)"

decoy_controls:
  - name: "token-rename test"
    fixture: "Deterministic rename of all event tokens to distinct synonyms;
      predicate must produce identical verdict"
    pass_threshold: "Identical verdict on ≥30 traces per substrate"
  - name: "decoy-token test"
    fixture: "Inject ≥10% spurious events with semantically plausible but
      causally disconnected tokens; verdict must be identical"
    pass_threshold: "Identical verdict on ≥30 traces per substrate"
  - name: "reaction-shuffle test"
    fixture: "Randomly reorder all reaction declarations; verdict identical"
    pass_threshold: "Identical verdict on ≥30 traces per substrate"
  - name: "species-rename test"
    fixture: "Replace species names with synonymous but distinct strings;
      verdict identical"
    pass_threshold: "Identical verdict on ≥30 traces per substrate"

promotion_requirements:
  - "All four decoy controls pass on a corpus of ≥30 traces per substrate"
  - "Substrate-blocked permutation at N=10,000 with the decoupled predicate
     yields shuffle-distribution gap < CI lower bound (signal beats shuffle)"
  - "≥3 substrates show predicate-positive results from independently-sourced
     corpora"
  - "Content-hash-signed Motif Contract; AI Operations Tower displays
     contract hash"
  - "Substance audit signed by Architect or Codex 1.5x per substrate"

known_failure_modes:
  - class: "Class 11 — Categorical confound through pooling"
    guard: "Bypassed by within-substrate shuffle in promotion_requirement #2"
  - class: "Class 13 (candidate) — Predicate-Detector Surface Coupling"
    guard: "Specifically prevented by §3 forbidden_evidence + §5
      lens_abstraction_layer + §6 invariance_requirements + §7 decoy_controls"
  - class: "Class 1 — Static-input contamination"
    guard: "Trace-length invariance + decoy-token test"
  - class: "Class 7 — Surface-labels-as-primitives"
    guard: "§3 forbids any surface-label feature; §4 declares set-theoretic
      abstraction layer"

empirically_positive_worlds:
  - world_family: "W1 (CRN)"
    instances:
      - "KEGG E. coli K-12 metabolic subnetworks (TCA cycle + glycolysis +
         pentose phosphate satisfy closure under appropriate food sets)"
      - "Hordijk-Steel pre-biotic RAF benchmarks"
    citations:
      - "doi:10.1098/rsif.2017.0260 (Hordijk & Steel 2017, RAF theory review)"
      - "doi:10.1371/journal.pone.0084054 (Filisetti et al. 2014, RAFs in
         realistic chemistry)"
    substance_audit_signed: false  # pending
  - world_family: "W6 (Ecosystem)"
    instances:
      - "Mutualistic interaction networks where every species is supported
         by ≥1 mutualistic edge (Bascompte 2009 plant-pollinator data)"
    citations:
      - "doi:10.1146/annurev.ecolsys.38.091206.095818 (Bascompte 2009)"
    substance_audit_signed: false  # pending
  - world_family: "W9 (Origins-Chemistry)"
    instances:
      - "Hordijk-Steel pre-biotic autocatalytic cycles"
      - "Vasas et al. autocatalytic networks under realistic chemistry"
    citations:
      - "doi:10.1016/j.jtbi.2003.10.001 (Hordijk & Steel 2004)"
      - "doi:10.1016/j.jtbi.2012.04.015 (Vasas et al. 2012)"
    substance_audit_signed: false  # pending
  - world_family: "W11 (Quasispecies)"
    instances:
      - "Autocatalytic replication networks at viral population scale"
    citations:
      - "doi:10.1007/BF00623322 (Eigen 1971, original quasispecies)"
      - "doi:10.1146/annurev.micro.51.1.151 (Domingo & Holland 1997)"
    substance_audit_signed: false  # pending
```

---

## Open for Codex 1.5x review

Codex's job is to:

1. **Amend this exemplar** wherever Architect's draft is vague, surface-coupled, evidence-gapped, or missing per-substrate sourcing. Mark amendments inline with `// CODEX:` so we can see the diff.
2. **Draft contracts** for the other five motifs in the same depth:
   - `motif.self_maintained_boundary.draft`
   - `motif.repair.draft`
   - `motif.externalized_memory.draft`
   - `motif.replication_lineage.draft`
   - `motif.floor_connectivity.draft` (retroactive — verify the existing predicate is structurally clean)
3. **Audit per-lens substrate-coupling.** For each motif × lens cell, declare whether the lens shares input space with the predicate. Architect already flagged the Petri-lens reachability concern as PARTIAL for autocatalytic_closure; Codex should look for similar concerns across all 6 motifs × 8 lenses = 48 cells.
4. **Surface blind spots.** A "Blind spots Architect missed" section at the top of the v1 draft, with bullet-point findings.

Output: `papers/methods/MOTIF_CONTRACTS_v1_DRAFT.md`.

After Codex's draft lands, three-way consensus (PI + Architect + Codex) ratifies the final 6 contracts. Then the implementation ticket goes out.

---

*— Architect Claude, first draft, awaiting Codex 1.5x co-authorship and PI ratification.*
