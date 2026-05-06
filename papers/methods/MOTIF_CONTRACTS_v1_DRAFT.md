# Motif Contracts v1 Draft

Status: Codex 1.5x coauthor draft, pending PI + Architect consensus.
Mode: contract authoring only. No implementation in this task.
Origin: C020 methodology leak, where labels and lens features both depended on
`formalism.lens_registry._label_feature_for_motif`.

## Blind Spots Architect Missed

- Same source object is still shared input space. In the autocatalytic-closure
  exemplar, graph, CRNT, and Petri lenses are marked mostly independent even
  though they read the same reaction declarations as the predicate. Different
  computations on the same reaction graph reduce but do not remove Class 13
  risk. Contracts should mark these cells PARTIAL unless the promotion harness
  proves independence by feature ablation and adversarial graph pairs.
- The product-closure definition mixes reaction-set and species-set notation.
  "products in S union F" is type-invalid if S is a set of reactions. It should
  declare a species support set X_S induced by reactions in S.
- The schema's substrate-blocked promotion sentence says "gap < CI lower
  bound." That is directionally wrong for the established C014/C016/C020
  convention. The gate should be: original gap > shuffled CI upper bound.
- "Token rename" is necessary but too weak. C020 also leaked through process
  flags derived from event names and state-key names. Contracts must require
  event-token rename, state-key rename, payload-key rename, and
  generator-id/benchmark-string erasure.
- The autocatalytic exemplar overclaims W6 and W11 empirical positives. Plant
  mutualistic networks and quasispecies are plausible generalized-RAF analogues,
  but they are not automatically Hordijk-Steel RAFs. They must be marked
  EXPLORATORY until a substrate-specific formalization maps food set,
  catalysts, and closure semantics.
- Trace-length invariance is misphrased for structural predicates. If reaction
  declarations live in the trace header, event truncation should not change the
  verdict. If declarations are absent, truncation can delete evidence and should
  produce "insufficient evidence," not forced agreement.
- Empirical-positive-worlds needs a "mapping status" field. A DOI proves the
  substrate phenomenon exists; it does not prove the project's predicate captures
  it. I add `mapping_status: source_bound | EXPLORATORY` to each entry below.
- Floor connectivity is not "dead" in the same sense as token-surface motifs.
  The older Basin-Floor Geometry predicate can be structurally clean because it
  operates on perturbation equivalence fibers. The later C020 floor label,
  however, used `neutral_component_fraction`, `nested_lineage_edges`,
  `attention_entropy`, and `neutral_percolation_event`; that version is still a
  surface-key predicate and must not be confused with the BFG contract.

## Architect Schema Preserved

The verbatim Architect schema excerpt from
papers/methods/MOTIF_CONTRACT_SCHEMA_DRAFT.md is preserved below. Codex
comments and amendments appear only in the exemplar/contracts, marked
// CODEX:.

``text
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
# matching. The definition operates at the LAYER ABOVE event tokens â€” set
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
# must be substantively different from every lens's layer (declared in Â§5).
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
# Each invariance gets a specific test fixture in Â§7.
invariance_requirements: list[invariance_declaration]

# 7. Decoy controls
# Specific adversarial fixtures the predicate must pass before any
# operational-tier promotion. At minimum: token-rename (every event token
# consistently renamed; verdict identical), decoy-injection (â‰¥10% spurious
# events; verdict identical), permutation (reorder predicate inputs; verdict
# identical), synonym-replacement (replace strings with synonymous distinct
# strings; verdict identical). Any control failure â†’ predicate fails the
# contract; not promotable.
decoy_controls: list[control_with_fixture]

# 8. Promotion requirements
# What evidence threshold gates claim-bearing. At minimum: all decoy controls
# pass on a corpus of â‰¥30 traces per substrate; substrate-blocked permutation
# at N=10,000 with the decoupled predicate yields shuffle-distribution gap <
# CI lower bound; â‰¥3 substrates show predicate-positive results from
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
# are NOT acceptable here â€” this field is the entry point for operational-tier
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
``

Codex operational addition for these drafts: mapping_status: source_bound |
EXPLORATORY is added under empirically_positive_worlds so a DOI/PMID proves
substrate reality without pretending the project predicate is already validated.
The compact field inventory below includes that addition.

```yaml
motif_id: string
contract_version: string
signed_at: ISO_UTC
signed_by: list[agent_id]
content_hash: sha256

semantic_definition: prose
allowed_evidence: list[feature_with_source]
forbidden_evidence: list[anti_pattern_with_reason]
predicate_abstraction_layer: layer_declaration

lens_abstraction_layer:
  graph: { features: [...], shares_input_with_predicate: bool_or_PARTIAL, justification: prose }
  crnt: { features: [...], shares_input_with_predicate: bool_or_PARTIAL, justification: prose }
  dynamical_systems: { features: [...], shares_input_with_predicate: bool_or_PARTIAL, justification: prose }
  topology: { features: [...], shares_input_with_predicate: bool_or_PARTIAL, justification: prose }
  petri: { features: [...], shares_input_with_predicate: bool_or_PARTIAL, justification: prose }
  statistical_mechanics: { features: [...], shares_input_with_predicate: bool_or_PARTIAL, justification: prose }
  control_theory: { features: [...], shares_input_with_predicate: bool_or_PARTIAL, justification: prose }
  information: { features: [...], shares_input_with_predicate: bool_or_PARTIAL, justification: prose }

invariance_requirements: list[invariance_declaration]
decoy_controls: list[control_with_fixture]
promotion_requirements: list[gate_with_threshold]
known_failure_modes: list[class_with_guard]

empirically_positive_worlds:
  - world_family: string
    instances: list[instance_description]
    citations: list[doi_or_pmid]
    mapping_status: source_bound | EXPLORATORY
    substance_audit_signed: bool
```

## Architect Exemplar With Codex Amendments

```yaml
motif_id: motif.autocatalytic_closure.draft
contract_version: "1-architect-draft-with-codex-amendments"
signed_at: <pending three-way consensus>
signed_by: <pending: PI, Architect Claude, Codex 1.5x>
content_hash: <computed at finalization>

semantic_definition: |
  A set of reactions S with induced species support X_S such that:
  (a) every species consumed by a reaction in S is either in food set F or is
      produced by at least one reaction in S;
  (b) every reaction in S is reachable from F by repeated application of
      reactions in S under declared stoichiometry/catalysis constraints;
  (c) every product species of every reaction in S is in X_S union F.
  // CODEX: Architect's original "products in S union F" was type-invalid
  // because S is a reaction set. This amendment introduces X_S.

  This is RAF-compatible only where the substrate declares a chemical reaction
  system with food set, reaction set, and catalysis relation. Generalized
  non-chemical closures are EXPLORATORY until they define these analogues.
  // CODEX: Prevents W6/W11 analogy from silently inheriting RAF validity.

allowed_evidence:
  - feature: "Bipartite reaction graph: species, reactions, reactants, products"
    source: "reaction declaration block, not event stream"
  - feature: "Food set F and initial species availability"
    source: "trace parameter declarations"
  - feature: "Catalysis relation when RAF rather than mere closure is claimed"
    source: "reaction declarations or source-bound adapter metadata"
  - feature: "Stoichiometric support for each reaction"
    source: "reaction declarations"

forbidden_evidence:
  - anti_pattern: "event types: reaction_event, closure_event, surface_catalysis_event, hyperedge_reaction_event"
    reason: "These are exactly the current `_process_flags(...).closure` token surfaces."
  - anti_pattern: "generator ids such as w1_crn_mass_action_closure or scenario_class positive/negative"
    reason: "C020 labels and scenarios carried answer-bearing names."
  - anti_pattern: "process_flags.closure or any decoded visible_processes.closure"
    reason: "Current lenses read this flag; predicate must not."
  - anti_pattern: "trace length, event_type_count, event_entropy, reaction_event frequency"
    reason: "Frequency proxies were C020-compatible leaks."
  - anti_pattern: "graph-lens cycle_proxy when defined from closure flags"
    reason: "Graph lens currently computes cycle_proxy partly from closure token flags."

predicate_abstraction_layer: |
  Set theory on declared reaction hypergraphs. The predicate may compute maxRAF
  or closed reachable reaction subsets from declarations. It may not read
  event streams, process flags, generator IDs, or scenario labels.

lens_abstraction_layer:
  graph:
    features: ["actor graph", "cycle_proxy", "branching_proxy", "process_flags"]
    shares_input_with_predicate: PARTIAL
    justification: "Reads event graph and process flags; current graph lens is not admissible for closure until process_flags are removed."
  crnt:
    features: ["species_count", "reaction_count", "stoichiometric_rank", "t_invariant_proxy"]
    shares_input_with_predicate: PARTIAL
    justification: "Reads the same reaction declarations. Use only as separate lens after adversarial pairs prove CRNT invariants do not predict closure by shared declaration artifacts."
  dynamical_systems:
    features: ["state trajectory recurrence", "terminal drift", "stability"]
    shares_input_with_predicate: false
    justification: "Reads simulated state trajectories, not closure declarations, but process_flags must be disabled for this motif."
  topology:
    features: ["persistent homology over state point clouds"]
    shares_input_with_predicate: false
    justification: "Reads trajectory geometry, not reaction-set membership; current process_flags.closure feature must be removed."
  petri:
    features: ["incidence matrix", "p/t invariants", "process_flags"]
    shares_input_with_predicate: PARTIAL
    justification: "Incidence matrix shares reaction declarations with predicate; process_flags.closure is disallowed."
  statistical_mechanics:
    features: ["free_energy_proxy", "large_deviation_rate", "energy_variance"]
    shares_input_with_predicate: false
    justification: "Reads ensemble/trajectory statistics; must not include process_flags."
  control_theory:
    features: ["controllability_proxy", "observability_proxy"]
    shares_input_with_predicate: false
    justification: "Control lens generally out-of-domain for closure; if used, it reads state/control channels, not reaction closure."
  information:
    features: ["event_entropy", "delta_entropy_proxy", "predictive_state_count"]
    shares_input_with_predicate: false
    justification: "Reads statistical information channels; must not include process_flags."

invariance_requirements:
  - "Event-token rename invariance"
  - "State-key rename invariance for non-declaration keys"
  - "Reaction-id and species-id permutation invariance"
  - "Event-stream decoy invariance when reaction declarations are unchanged"
  - "Insufficient-evidence verdict when reaction declarations are removed"

decoy_controls:
  - name: "event-token rename"
    fixture: "Rename all event types; verdict identical."
  - name: "state-key decoy"
    fixture: "Inject state keys named closure_like, raf_like, catalytic_memory; verdict unchanged."
  - name: "reaction declaration adversarial pair"
    fixture: "Two networks with same event counts but one closed reachable S and one non-closed S."
  - name: "CRNT collision"
    fixture: "Networks matched on deficiency/rank but opposite closure verdicts."

promotion_requirements:
  - "All decoy controls pass on >=30 traces per substrate."
  - "Original decoupled-predicate gap > substrate-blocked shuffled CI upper bound at N=10000."
  - ">=3 substrates with both positive and negative labels within substrate."
  - "Graph/CRNT/Petri closure lenses either refactored to remove shared features or excluded."
  - "Content hash displayed by AI Operations Tower; substance audit signed per substrate."

known_failure_modes:
  - class: "Class 1 Static-input contamination"
    guard: "Forbids scenario labels, generator ids, and expected_closure fields."
  - class: "Class 2 Direction inversion"
    guard: "Promotion gate explicitly uses original gap > shuffled CI upper bound."
  - class: "Class 7 Surface-labels-as-primitives"
    guard: "Forbids closure event names and process flags."
  - class: "Class 11 Categorical confound through pooling"
    guard: "Requires within-substrate positive and negative labels."
  - class: "Class 13 Predicate-Detector Surface Coupling"
    guard: "Marks graph/CRNT/Petri as PARTIAL until decoupled."

empirically_positive_worlds:
  - world_family: "W1 CRN"
    instances: ["RAF/autocatalytic reaction networks"]
    citations: ["doi:10.1098/rsif.2017.0228", "doi:10.1371/journal.pone.0084054"]
    mapping_status: source_bound
    substance_audit_signed: false
  - world_family: "W9 Origins-Chemistry"
    instances: ["prebiotic RAF and autocatalytic-set chemistry"]
    citations: ["doi:10.1016/j.jtbi.2003.10.001", "doi:10.1016/j.jtbi.2012.04.015"]
    mapping_status: source_bound
    substance_audit_signed: false
  - world_family: "W6 Ecosystem"
    instances: ["mutualistic interaction networks as generalized closure candidates"]
    citations: ["doi:10.1038/nature07950", "doi:10.1146/annurev.ecolsys.38.091206.095818"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
  - world_family: "W11 Quasispecies"
    instances: ["replicator networks as generalized autocatalytic populations"]
    citations: ["doi:10.1007/BF00623322"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
```

## Contract: Self-Maintained Boundary

```yaml
motif_id: motif.self_maintained_boundary.draft
contract_version: "1-codex-draft"
signed_at: <pending>
signed_by: <pending>
content_hash: <computed at finalization>

semantic_definition: |
  A subsystem B maintains a persistent inside/outside distinction by using
  internal or coupled processes to rebuild, regulate, or preserve the boundary
  that constrains exchange with its environment. The boundary may be chemical,
  spatial, membrane-like, ecological, organizational, or informational, but the
  predicate must observe persistence plus maintenance coupling, not merely the
  presence of a component named "boundary."

allowed_evidence:
  - feature: "Boundary state variable with exchange constraint effect"
    source: "state trajectory plus declared environment/internal partition"
  - feature: "Maintenance flux from internal process to boundary integrity"
    source: "causal dependency graph or perturbation-response profile"
  - feature: "Boundary-loss perturbation followed by recovery without external reset"
    source: "paired baseline/perturbed traces"
  - feature: "Exchange selectivity across boundary"
    source: "flux ledger or state transition matrix"

forbidden_evidence:
  - anti_pattern: "event types: boundary_event, engulfment_event"
    reason: "These directly trigger current `_process_flags(...).boundary`."
  - anti_pattern: "state keys: membrane_integrity, nested_fraction when used only as names"
    reason: "Current predicate reads their presence, not maintenance dynamics."
  - anti_pattern: "payload keys: outer_id, subcell_id, boundary_kind, internal_produces_boundary"
    reason: "Graph lens counts actor edges from these keys and adapters may declare the answer."
  - anti_pattern: "process_flags.boundary or visible_processes.boundary"
    reason: "Current lenses share this derived flag with labels."
  - anti_pattern: "world_family in {protocell, symbiogenesis} as a boundary proxy"
    reason: "Substrate identity is a categorical confound."

predicate_abstraction_layer: |
  Perturbation-response and causal maintenance on partitioned state spaces.
  The predicate reads the effect of boundary perturbation on exchange and the
  endogenous recovery trajectory. It does not read boundary-named tokens.

lens_abstraction_layer:
  graph:
    features: ["actor_node_count", "actor_edge_count", "cycle_proxy", "process_flags.boundary"]
    shares_input_with_predicate: PARTIAL
    justification: "Actor graph can read boundary payload keys; current process_flags must be removed."
  crnt:
    features: ["p_invariant_proxy", "species persistence", "process_flags.boundary"]
    shares_input_with_predicate: PARTIAL
    justification: "Potentially useful for membrane chemistry but shares state/reaction support; remove flags."
  dynamical_systems:
    features: ["stability", "terminal drift", "recurrence"]
    shares_input_with_predicate: PARTIAL
    justification: "Predicate also reads recovery dynamics; admissible only if DS lens excludes boundary perturbation labels."
  topology:
    features: ["long_h1_cycles", "state-cloud holes"]
    shares_input_with_predicate: false
    justification: "Topological enclosure is separate from maintenance coupling, but process_flags.boundary must be removed."
  petri:
    features: ["p_invariant_count", "place_count", "process_flags.boundary"]
    shares_input_with_predicate: PARTIAL
    justification: "Shares conservation structure in reaction substrates and currently shares flags."
  statistical_mechanics:
    features: ["energy_variance", "low_energy_basin", "process_flags.boundary"]
    shares_input_with_predicate: PARTIAL
    justification: "Energy basin can correlate with recovery; flags must be removed."
  control_theory:
    features: ["controllability_proxy", "observability_proxy", "process_flags.boundary"]
    shares_input_with_predicate: PARTIAL
    justification: "Control lens and predicate both read recovery/control; require independent input partition."
  information:
    features: ["event_entropy", "delta_entropy_proxy", "process_flags"]
    shares_input_with_predicate: false
    justification: "Information statistics are separate after process_flags removal."

invariance_requirements:
  - "Rename boundary/membrane tokens without verdict change."
  - "Scale boundary state units without verdict change when dynamics are equivalent."
  - "Swap entity IDs inside/outside while preserving partition relation."
  - "Add passive boundary component with no maintenance flux -> negative remains negative."

decoy_controls:
  - name: "boundary-token decoy"
    fixture: "Inject boundary_event and membrane_integrity into a no-recovery trace; verdict must remain false."
  - name: "maintenance ablation"
    fixture: "Keep boundary present but remove internal repair flux; verdict false."
  - name: "external reset trap"
    fixture: "Boundary recovers only through exogenous reset; verdict false."
  - name: "matched-stability pair"
    fixture: "Two traces matched on terminal stability; only one has boundary-specific recovery coupling."

promotion_requirements:
  - "All decoys pass on >=30 traces per substrate."
  - "Within-substrate positive and negative corpora for each promoted substrate."
  - "Original gap > substrate-blocked shuffled CI upper bound at N=10000."
  - "Control/DS lenses using recovery features must run ablation controls."
  - "Substance audit verifies boundary source and maintenance source are distinct."

known_failure_modes:
  - class: "Class 1 Static-input contamination"
    guard: "Forbids boundary_kind and internal_produces_boundary config fields."
  - class: "Class 4 Scenario-internal hardcoding"
    guard: "Requires perturbation evidence, not benchmark branch."
  - class: "Class 7 Surface-labels-as-primitives"
    guard: "Forbids boundary_event and membrane_integrity name-only checks."
  - class: "Class 11 Categorical confound through pooling"
    guard: "Requires within-substrate label balance."
  - class: "Class 13 Predicate-Detector Surface Coupling"
    guard: "Flags graph/control/DS overlap explicitly."

empirically_positive_worlds:
  - world_family: "W2 Protocell"
    instances: ["fatty-acid vesicle growth/division with membrane boundary"]
    citations: ["doi:10.1021/ja900919c", "pmid:19323552"]
    mapping_status: source_bound
    substance_audit_signed: false
  - world_family: "W6 Ecosystem"
    instances: ["mutualistic networks with persistence constraints on community boundary"]
    citations: ["doi:10.1038/nature07950"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
  - world_family: "W12 Symbiogenesis"
    instances: ["endosymbiotic compartmentalization and organelle-origin boundary maintenance"]
    citations: ["doi:10.1186/gb-2001-2-6-reviews1018", "pmid:11423013"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
```

## Contract: Repair

```yaml
motif_id: motif.repair.draft
contract_version: "1-codex-draft"
signed_at: <pending>
signed_by: <pending>
content_hash: <computed at finalization>

semantic_definition: |
  A system detects or is perturbed into functional degradation and then executes
  an endogenous process that restores a specified invariant or function above a
  predeclared threshold. Repair requires damage, endogenous intervention, and
  measurable recovery. Mere stability, low variance, or a token named "repair"
  is insufficient.

allowed_evidence:
  - feature: "Pre-damage baseline invariant/function value"
    source: "trace state or declared invariant report"
  - feature: "Damage or perturbation event with measurable functional drop"
    source: "perturbation ledger or paired source/perturbed traces"
  - feature: "Endogenous intervention path"
    source: "causal event/state transition graph excluding exogenous reset"
  - feature: "Recovery to threshold"
    source: "post-perturbation trajectory"

forbidden_evidence:
  - anti_pattern: "event types: repair_event, sanction_event, homeostasis_event, mutual_stabilisation_event"
    reason: "These directly trigger current `_process_flags(...).repair`."
  - anti_pattern: "process_flags.repair or visible_processes.repair"
    reason: "Shared label/lens feature."
  - anti_pattern: "energy_variance or terminal stability alone"
    reason: "Low variance can mean no damage occurred."
  - anti_pattern: "benchmark fields: membrane_repair, homeostasis, mutualism, repair_rate"
    reason: "Parameter/config fields can contain the answer."
  - anti_pattern: "external reset, source reload, cache refresh, or daemon retry as biological repair"
    reason: "Operational recovery is not substrate repair."

predicate_abstraction_layer: |
  Intervention/counterfactual recovery over perturbation-outcome trajectories.
  The predicate compares baseline, damaged, and recovered states and checks that
  recovery is mediated by endogenous system dynamics.

lens_abstraction_layer:
  graph:
    features: ["actor paths", "branching_proxy", "process_flags.repair"]
    shares_input_with_predicate: PARTIAL
    justification: "Can read intervention paths; current repair flag must be removed."
  crnt:
    features: ["p_invariant_proxy", "persistence_indicator", "process_flags.repair"]
    shares_input_with_predicate: PARTIAL
    justification: "Useful for conserved repair chemistry but overlaps invariant recovery."
  dynamical_systems:
    features: ["stability", "terminal drift", "recovery dynamics"]
    shares_input_with_predicate: PARTIAL
    justification: "Both read recovery shape; DS lens must be trained on recovery-independent features or excluded."
  topology:
    features: ["trajectory topology after perturbation"]
    shares_input_with_predicate: false
    justification: "Topology may see basin return but not repair causality; no process_flags."
  petri:
    features: ["p_invariant_count", "place_count", "process_flags.repair"]
    shares_input_with_predicate: PARTIAL
    justification: "Conservation invariants overlap with repaired invariant; require ablation."
  statistical_mechanics:
    features: ["energy_variance", "large_deviation_rate", "process_flags.repair"]
    shares_input_with_predicate: PARTIAL
    justification: "Rare-event recovery may correlate; remove repair flags."
  control_theory:
    features: ["controllability_proxy", "intervention/control channels", "process_flags.repair"]
    shares_input_with_predicate: PARTIAL
    justification: "Control and predicate both read intervention; require causal independence control."
  information:
    features: ["event entropy", "delta entropy", "predictive state count"]
    shares_input_with_predicate: false
    justification: "Information features are admissible after process_flags removal."

invariance_requirements:
  - "Rename repair/homeostasis/sanction/mutual-stabilisation tokens."
  - "Damage magnitude monotonicity: larger damage cannot be easier unless repair effort changes."
  - "No-damage control returns negative or insufficient evidence."
  - "External reset control returns negative."

decoy_controls:
  - name: "repair-token decoy"
    fixture: "Inject repair_event into trace with no damage/recovery; verdict false."
  - name: "passive relaxation"
    fixture: "State relaxes without endogenous intervention path; verdict false unless passive self-repair is predeclared."
  - name: "exogenous reset"
    fixture: "External controller resets state; verdict false."
  - name: "matched-stability"
    fixture: "Positive and negative traces matched on final stability; only positive has damage plus endogenous recovery."

promotion_requirements:
  - "Damage, intervention, recovery all source-bound and independently logged."
  - "All decoys pass on >=30 traces per substrate."
  - "Original gap > substrate-blocked shuffled CI upper bound at N=10000."
  - "At least one adversarial no-damage and one exogenous-reset corpus per substrate."

known_failure_modes:
  - class: "Class 1 Static-input contamination"
    guard: "Forbids repair_rate and expected_recovery parameters."
  - class: "Class 4 Scenario-internal hardcoding"
    guard: "Requires perturbation ledger and endogenous recovery path."
  - class: "Class 6 Engineered passing"
    guard: "Recovery threshold predeclared from source invariant."
  - class: "Class 13 Predicate-Detector Surface Coupling"
    guard: "Marks DS/control/Petri/stat-mech overlap."

empirically_positive_worlds:
  - world_family: "W11 Quasispecies / Molecular"
    instances: ["DNA damage and enzymatic repair systems"]
    citations: ["doi:10.1038/362709a0", "pmid:8469282"]
    mapping_status: source_bound
    substance_audit_signed: false
  - world_family: "W2 Protocell / Cellular Boundary"
    instances: ["plasma membrane disruption and repair"]
    citations: ["doi:10.1146/annurev.cellbio.19.111301.140101", "pmid:14570567"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
  - world_family: "W6 Ecosystem"
    instances: ["ecological resilience and recovery after perturbation"]
    citations: ["doi:10.1146/annurev.es.04.110173.000245"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
```

// CODEX: Schema amendment required before ratification: replace the promotion
// text "gap < CI lower bound" with "original gap > shuffled CI upper bound."
// Otherwise this contract encodes Class 2 direction inversion.

## Contract: Externalized Memory

```yaml
motif_id: motif.externalized_memory.draft
contract_version: "1-codex-draft"
signed_at: <pending>
signed_by: <pending>
content_hash: <computed at finalization>

semantic_definition: |
  A system writes information into a persistent medium outside the acting
  subsystem and later reads that medium so future behavior depends on the stored
  external state. The motif requires write, persistence, read, and behavioral
  dependence. Internal state recurrence or a token named "memory" is not enough.

allowed_evidence:
  - feature: "External medium identity distinct from actor state"
    source: "entity graph or declared storage substrate"
  - feature: "Write operation from actor to medium"
    source: "causal event/state transition with payload target"
  - feature: "Persistence of written state across actor updates"
    source: "time-indexed medium state"
  - feature: "Read operation changing later policy/trajectory"
    source: "counterfactual or ablation trace with medium removed"

forbidden_evidence:
  - anti_pattern: "event types: memory_write_event, external_mark_event, learning_gain_event"
    reason: "These directly trigger current `_process_flags(...).memory`."
  - anti_pattern: "event-name substrings: memory, mark, prediction"
    reason: "Control lens currently counts these as memory_channel_count."
  - anti_pattern: "process_flags.memory or visible_processes.memory"
    reason: "Shared label/lens feature."
  - anti_pattern: "state recurrence alone"
    reason: "Internal recurrence is not externalized storage."
  - anti_pattern: "attention_entropy or predictive_state_count as a memory verdict"
    reason: "These can be lens features, not predicate evidence."

predicate_abstraction_layer: |
  Information-channel intervention analysis over actor-medium bipartitions. The
  predicate asks whether an externalized write/read channel causally changes
  later behavior relative to a storage-erasure control.

lens_abstraction_layer:
  graph:
    features: ["actor nodes/edges", "process_flags.memory"]
    shares_input_with_predicate: PARTIAL
    justification: "Actor-medium graph overlaps with predicate; current flag must be removed."
  crnt:
    features: ["reaction invariants"]
    shares_input_with_predicate: false
    justification: "Normally out-of-domain; chemical storage analogues need separate contract."
  dynamical_systems:
    features: ["recurrence_rate", "process_flags.memory"]
    shares_input_with_predicate: PARTIAL
    justification: "Recurrence can proxy memory; must be tested against storage-erasure controls."
  topology:
    features: ["connectivity of state point cloud", "process_flags.memory"]
    shares_input_with_predicate: false
    justification: "Point-cloud topology is separate after flag removal."
  petri:
    features: ["declines for memory"]
    shares_input_with_predicate: false
    justification: "Current Petri lens declines; no coupling if it continues to decline."
  statistical_mechanics:
    features: ["declines unless custom memory lens added"]
    shares_input_with_predicate: false
    justification: "No current prediction surface for memory."
  control_theory:
    features: ["memory_channel_count", "observability_proxy", "process_flags.memory"]
    shares_input_with_predicate: PARTIAL
    justification: "memory_channel_count reads memory/mark/prediction tokens; not admissible without refactor."
  information:
    features: ["event_entropy", "delta_entropy_proxy", "predictive_state_count", "process_flags"]
    shares_input_with_predicate: PARTIAL
    justification: "Information lens is conceptually adjacent; require storage-erasure and transfer-control tests."

invariance_requirements:
  - "Rename memory/mark/prediction tokens."
  - "Rename medium entity IDs while preserving actor-medium partition."
  - "Storage-erasure control must flip positive to negative."
  - "Internal-memory-only trace remains negative."

decoy_controls:
  - name: "memory-token decoy"
    fixture: "Inject memory_write_event labels without persistent medium; verdict false."
  - name: "write-without-read"
    fixture: "External mark persists but is never read; verdict false."
  - name: "read-without-write"
    fixture: "Actor reads preloaded environment not written by system; verdict false unless source declares inherited external memory."
  - name: "medium-erasure"
    fixture: "Erase external medium after write; positive trace must lose memory-dependent behavior."

promotion_requirements:
  - "External medium boundary and actor boundary source-bound."
  - "Write/read/persistence/behavioral-dependence all present."
  - "All decoys pass on >=30 traces per substrate."
  - "Original gap > substrate-blocked shuffled CI upper bound at N=10000."

known_failure_modes:
  - class: "Class 1 Static-input contamination"
    guard: "Forbids scenario memory labels and process flags."
  - class: "Class 7 Surface-labels-as-primitives"
    guard: "Forbids memory/mark/prediction substrings."
  - class: "Class 8 Abstract-scalar-standing-in"
    guard: "Requires explicit medium state, not scalar memory score."
  - class: "Class 13 Predicate-Detector Surface Coupling"
    guard: "Marks graph/control/information overlap."

empirically_positive_worlds:
  - world_family: "W8 Cognitive"
    instances: ["external cognitive storage and extended mind"]
    citations: ["doi:10.1093/analys/58.1.7"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
  - world_family: "W7 Swarm"
    instances: ["pheromone trails and collective external memory"]
    citations: ["doi:10.1007/BF01417909", "pmid:32546115"]
    mapping_status: source_bound
    substance_audit_signed: false
  - world_family: "W6 Ecosystem"
    instances: ["ecological memory in ecosystem response"]
    citations: ["doi:10.1002/fee.1311"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
```

## Contract: Replication Lineage

```yaml
motif_id: motif.replication_lineage.draft
contract_version: "1-codex-draft"
signed_at: <pending>
signed_by: <pending>
content_hash: <computed at finalization>

semantic_definition: |
  A lineage exists when entities produce descendants through a copy/division
  process that preserves identifiable heritable state across parent-child edges.
  The motif requires parent-child relation, inherited state, and at least one
  nontrivial descent path. Population growth without inheritance, or inheritance
  labels without descendants, is insufficient.

allowed_evidence:
  - feature: "Parent-child edge list with timestamps"
    source: "lineage ledger, not event names"
  - feature: "Heritable state comparison between parent and child"
    source: "sequence/genome/morphology/state vector"
  - feature: "Replication/division operation that creates child entity"
    source: "entity graph transition"
  - feature: "Lineage depth and branching"
    source: "ancestry graph computed from parent-child edges"

forbidden_evidence:
  - anti_pattern: "event types: replication_event, division_event, vertical_inheritance_event, nested_division_event"
    reason: "These directly trigger current `_process_flags(...).lineage`."
  - anti_pattern: "payload keys: parent_id, child, child_ids, parent_sequence, child_sequence used only as counts"
    reason: "Graph lens counts these actor edges without verifying heritable similarity."
  - anti_pattern: "process_flags.lineage or visible_processes.lineage"
    reason: "Shared current label/lens feature."
  - anti_pattern: "population size increase alone"
    reason: "Growth is not inheritance."
  - anti_pattern: "world_family in {digital, quasispecies, symbiogenesis}"
    reason: "Substrate identity can perfectly predict lineage in pooled corpora."

predicate_abstraction_layer: |
  Genealogical graph plus heritable-state similarity. The predicate reads
  parent-child edges and computes descent paths with inherited state preservation
  above a predeclared similarity threshold.

lens_abstraction_layer:
  graph:
    features: ["actor_edge_count", "branching_proxy", "process_flags.lineage"]
    shares_input_with_predicate: PARTIAL
    justification: "Reads the same parent/child payload surface; not admissible without heritability-blind ablation."
  crnt:
    features: ["declines for lineage"]
    shares_input_with_predicate: false
    justification: "Current CRNT lens does not predict lineage."
  dynamical_systems:
    features: ["declines unless lineage embedded in continuous state"]
    shares_input_with_predicate: false
    justification: "No current direct prediction for lineage."
  topology:
    features: ["declines for lineage"]
    shares_input_with_predicate: false
    justification: "Current topology lens does not predict lineage."
  petri:
    features: ["t_invariant_count", "process_flags.lineage"]
    shares_input_with_predicate: PARTIAL
    justification: "Vertical inheritance event pseudo-transition overlaps; process flag disallowed."
  statistical_mechanics:
    features: ["large_deviation_rate", "process_flags.lineage"]
    shares_input_with_predicate: PARTIAL
    justification: "Rare branching can correlate; lineage flag must be removed."
  control_theory:
    features: ["declines for lineage"]
    shares_input_with_predicate: false
    justification: "No current direct prediction."
  information:
    features: ["event_entropy", "predictive_state_count", "process_flags"]
    shares_input_with_predicate: PARTIAL
    justification: "Heritable-state information is adjacent; require label-free feature separation."

invariance_requirements:
  - "Rename replication/division/inheritance tokens."
  - "Permute entity IDs preserving parent-child edges."
  - "Reverse-time lineage control must fail."
  - "Child without inherited-state similarity fails."

decoy_controls:
  - name: "lineage-token decoy"
    fixture: "Inject replication_event names without child entity creation; verdict false."
  - name: "growth-without-inheritance"
    fixture: "Entity count grows but child states are random; verdict false."
  - name: "inheritance-without-child"
    fixture: "State copied but no new entity edge; verdict false."
  - name: "substrate-pool trap"
    fixture: "Pool uniform-positive lineage substrates with uniform-negative others; substrate-blocked shuffle must kill signal."

promotion_requirements:
  - "Lineage graph and heritable state are both source-bound."
  - "Within-substrate positive and negative corpora."
  - "All decoys pass on >=30 traces per substrate."
  - "Original gap > substrate-blocked shuffled CI upper bound at N=10000."

known_failure_modes:
  - class: "Class 1 Static-input contamination"
    guard: "Forbids scenario lineage labels."
  - class: "Class 7 Surface-labels-as-primitives"
    guard: "Forbids replication/division token shortcuts."
  - class: "Class 10 Substrate-presence mismatch"
    guard: "Requires both positive and negative lineage traces in substrate."
  - class: "Class 11 Categorical confound through pooling"
    guard: "Requires substrate-blocked controls."
  - class: "Class 13 Predicate-Detector Surface Coupling"
    guard: "Marks graph/Petri/stat-mech/information overlap."

empirically_positive_worlds:
  - world_family: "W11 Quasispecies"
    instances: ["viral/RNA replicator lineage under mutation-selection dynamics"]
    citations: ["doi:10.1007/BF00623322"]
    mapping_status: source_bound
    substance_audit_signed: false
  - world_family: "W5 Digital"
    instances: ["Avida digital organisms with executable-genome descent"]
    citations: ["doi:10.1038/nature01568", "pmid:12736677"]
    mapping_status: source_bound
    substance_audit_signed: false
  - world_family: "W12 Symbiogenesis"
    instances: ["organelle/endosymbiont descent and genome reduction"]
    citations: ["doi:10.1186/gb-2001-2-6-reviews1018", "pmid:11423013"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
  - world_family: "W2 Protocell"
    instances: ["vesicle growth/division as protocell lineage precursor"]
    citations: ["doi:10.1021/ja900919c"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
```

## Contract: Floor Connectivity

```yaml
motif_id: motif.floor_connectivity.draft
contract_version: "1-codex-retroactive-draft"
signed_at: <pending>
signed_by: <pending>
content_hash: <computed at finalization>

semantic_definition: |
  For a target function or motif-equivalence class E, a floor exists when there
  is a connected set of implementation states reachable under bounded neutral
  perturbations such that the declared invariant/function remains preserved.
  Connectivity is measured in implementation space after quotienting by the
  declared equivalence basis. The motif is structural only when it reads
  perturbation outcomes, invariant preservation, implementation distance, and
  quotient/fiber connectivity. It is not structural when it reads state-key names
  such as `neutral_component_fraction`.

allowed_evidence:
  - feature: "Equivalence basis and declared invariants"
    source: "Basin-Floor Geometry preregistration / invariant report"
  - feature: "Perturbation outcome profile with same-fiber scores"
    source: "paired source/perturbed traces"
  - feature: "Implementation-distance graph under locked metric"
    source: "distance_metrics plus perturbation outcomes"
  - feature: "Neutral-floor index fields W_floor, D_floor, H_impl, R_drift, P_equiv, L_func, I_inv, Reach, Conn"
    source: "BasinFloorGeometry object"
  - feature: "Point-attractor/implementation-unique falsifier"
    source: "FloorFalsifier"

forbidden_evidence:
  - anti_pattern: "state keys: neutral_component_fraction, nested_lineage_edges, attention_entropy"
    reason: "These are the C020 `_process_flags(...).floor` key surfaces."
  - anti_pattern: "event type: neutral_percolation_event"
    reason: "Direct current floor token shortcut."
  - anti_pattern: "motif id itself, attractor_strength floor=0.88, or formal_gap asymmetry"
    reason: "Campaign floor candidate can mechanically pass from registry asymmetry."
  - anti_pattern: "world_family in {cognitive, quasispecies, symbiogenesis}"
    reason: "Prior floor positives clustered by substrate in Class 11 failure."
  - anti_pattern: "coverage_score or lens prediction score as predicate input"
    reason: "Would make predicate read detector output."

predicate_abstraction_layer: |
  Quotient-topological graph connectivity over implementation fibers. The clean
  predicate is the BFG version: compute connected neutral implementation
  components preserving declared invariants under a locked equivalence basis.
  // CODEX: The current C020 `_label_feature_for_motif` floor predicate is not
  // this clean predicate; it is a state-key/event-token proxy. The contract
  // ratifies only the BFG predicate shape, not the C020 label function.

lens_abstraction_layer:
  graph:
    features: ["declines currently for floor"]
    shares_input_with_predicate: false
    justification: "Graph lens declines on floor; keep it excluded unless quotient/fiber graph lens is separately contracted."
  crnt:
    features: ["declines currently for floor"]
    shares_input_with_predicate: false
    justification: "No current CRNT prediction for floor."
  dynamical_systems:
    features: ["recurrence_rate", "stability"]
    shares_input_with_predicate: PARTIAL
    justification: "Can confuse basin recurrence with neutral floor; require perturbation-equivalence ablation."
  topology:
    features: ["connectivity", "cycle_persistence_proxy"]
    shares_input_with_predicate: PARTIAL
    justification: "Topology reads connectivity too, but on state point clouds rather than quotient implementation fibers; high coupling risk."
  petri:
    features: ["declines currently for floor"]
    shares_input_with_predicate: false
    justification: "Current Petri lens declines."
  statistical_mechanics:
    features: ["large_deviation_rate", "energy_variance"]
    shares_input_with_predicate: false
    justification: "Can evaluate rare neutral drift statistics but not quotient connectivity directly."
  control_theory:
    features: ["controllability_proxy", "observability_proxy"]
    shares_input_with_predicate: PARTIAL
    justification: "Control reachability can overlap with floor reachability; require locked quotient-basis separation."
  information:
    features: ["declines currently for floor"]
    shares_input_with_predicate: false
    justification: "Information lens declines on floor under current registry."

invariance_requirements:
  - "Implementation-ID rename invariance."
  - "Trace-token rename invariance."
  - "Equivalent metric representation invariance under locked basis."
  - "Point-attractor falsifier: implementation-unique surfaces fail."
  - "Substrate erasure: verdict unchanged when world_family removed and evidence retained."

decoy_controls:
  - name: "floor-token decoy"
    fixture: "Inject neutral_component_fraction or neutral_percolation_event into non-neutral traces; BFG verdict false."
  - name: "point-attractor falsifier"
    fixture: "Single implementation preserves function but no neutral neighborhood; verdict false."
  - name: "same-reachability-different-fiber"
    fixture: "Two traces matched on reachability; only one has connected invariant-preserving fiber."
  - name: "substrate-label shuffle"
    fixture: "Labels shuffled within substrate at N=10000; original must exceed shuffled CI upper bound."
  - name: "basis drift"
    fixture: "Change equivalence basis hash; predicate refuses to evaluate."

promotion_requirements:
  - "Use BFG predicate only; C020 state-key floor label is non-promotable."
  - "Locked equivalence basis content hash displayed in report."
  - "Within-substrate positive and negative examples for each substrate."
  - "Original gap > substrate-blocked shuffled CI upper bound at N=10000."
  - "Point-attractor and implementation-unique falsifiers pass."
  - "Topology/control lenses marked PARTIAL must pass ablation controls or be excluded."

known_failure_modes:
  - class: "Class 1 Static-input contamination"
    guard: "Forbids K labels, coverage scores, and lens outputs."
  - class: "Class 2 Direction inversion"
    guard: "Explicit CI upper-bound direction."
  - class: "Class 8 Abstract-scalar-standing-in"
    guard: "Requires connected implementation set, not scalar floor score."
  - class: "Class 10 Substrate-presence mismatch"
    guard: "Requires motif presence and label variation before threshold logic."
  - class: "Class 11 Categorical confound through pooling"
    guard: "Requires within-substrate balance and substrate-blocked shuffle."
  - class: "Class 13 Predicate-Detector Surface Coupling"
    guard: "Separates BFG quotient predicate from topology/control lenses."

empirically_positive_worlds:
  - world_family: "W11 Quasispecies"
    instances: ["RNA/genotype neutral networks preserving phenotype/function"]
    citations: ["doi:10.1073/pnas.96.17.9716", "pmid:10449760"]
    mapping_status: source_bound
    substance_audit_signed: false
  - world_family: "W5 Digital"
    instances: ["digital organisms where robustness enables neutral variation"]
    citations: ["doi:10.1186/1471-2148-8-284", "doi:10.1038/nature01568"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
  - world_family: "W4 Morphogenesis"
    instances: ["developmental canalization as phenotype-preserving implementation variation"]
    citations: ["doi:10.1038/150563a0"]
    mapping_status: EXPLORATORY
    substance_audit_signed: false
```

## Per-Lens Substrate-Coupling Audit Appendix

Legend: OK means no direct input-space sharing after process_flags are removed.
PARTIAL means same source object or adjacent abstraction; needs ablation,
feature removal, or exclusion. BAD means current implementation reads the same
surface as the predicate and is not admissible for claim-bearing controls.

| motif | graph | CRNT | dynamical systems | topology | Petri | stat mech | control | information |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| autocatalytic_closure | BAD: process_flags.closure; PARTIAL: reaction graph | PARTIAL: same reaction declarations | PARTIAL until flags removed | PARTIAL until flags removed | BAD: process_flags.closure; PARTIAL: incidence graph | PARTIAL until flags removed | OK/out-of-domain | PARTIAL until flags removed |
| self_maintained_boundary | BAD: process_flags.boundary and boundary payload keys | PARTIAL: conservation/reaction support | PARTIAL: recovery dynamics | PARTIAL until flags removed | BAD: process_flags.boundary | PARTIAL: energy basin plus flags | PARTIAL: recovery/control overlap | PARTIAL until flags removed |
| repair | BAD: process_flags.repair | PARTIAL: invariant restoration | PARTIAL: recovery dynamics | OK after flags removed | BAD: process_flags.repair | PARTIAL: rare recovery plus flags | PARTIAL: intervention channels | OK after flags removed |
| externalized_memory | PARTIAL: actor-medium graph; BAD flags | OK/out-of-domain | PARTIAL: recurrence can proxy memory | OK after flags removed | OK/declines | OK/declines | BAD: memory_channel_count reads memory/mark/prediction tokens | PARTIAL: same information-channel concept |
| replication_lineage | BAD: parent/child payload counts and flags | OK/declines | OK/declines | OK/declines | PARTIAL: vertical inheritance pseudo-transition | PARTIAL: rare branching plus flags | OK/declines | PARTIAL: heritable information adjacent |
| floor_connectivity | OK if graph continues to decline | OK/declines | PARTIAL: basin recurrence can proxy floor | PARTIAL: connectivity on nearby but different space | OK/declines | OK | PARTIAL: reachability overlap | OK/declines |

Required implementation consequence for D26 candidate:

- Any BAD cell is excluded from substrate-blocked controls until refactored.
- Any PARTIAL cell must pass an ablation suite where the predicate-positive
  property is destroyed while the lens feature is preserved, and vice versa.
- Any lens that uses `process_flags.*` for the same motif as the predicate is
  automatically BAD for that motif under the contract.
- The C020 result is not promotion evidence for any of these five motifs because
  every label was produced by `_label_feature_for_motif`, and several lenses
  used `process_flags` derived from the same function.

## Citation Notes

The DOI/PMID entries above are evidence anchors, not automatic mappings. Entries
marked EXPLORATORY need a substrate-specific substance audit before they can
count toward promotion. In particular:

- W6 mutualism is not automatically autocatalytic closure.
- W12 endosymbiosis is not automatically self-maintained boundary or lineage.
- W4 canalization supports phenotype-preserving variation but does not by itself
  prove the BFG floor predicate.
- W8 extended cognition supports external storage as a philosophical/cognitive
  construct; operational source data still needs a substrate-specific audit.