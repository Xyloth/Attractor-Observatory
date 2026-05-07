# Lens Recovery v1 Draft

> **DX-002 public runtime boundary:** References to `formalism/*`, `trace/*`, `worlds/*`, `motifs/*`, or `validation/*` in this document are narrative or private-runtime evidence unless a shipped public file is explicitly linked. The executable implementation is held outside the public branch; citations to private paths are governed by D29 and should be read as `evidence_private: true` / `private_unshipped`, not as public-runnable verification.


Task: TASK-LENS-RECOVERY-R1  
Author: Codex 1.5x, co-authorship review pass  
Status: Round 1 design draft only; no implementation; no claim-bearing promotion.

## Blind Spots Architect Missed

- "Probably most BAD cells are refactorable" is false under the Campaign 024 audit. Most BAD cells are not dirty implementations of otherwise clean measurements; they are missing-source, same-object, or domain-inapplicable failures.
- The graph lens should not be recovered as one generic lens. "Graph" is a lens family. The scientifically meaningful units are reaction bipartite graph, external-channel graph, perturbation-response graph, phylogenetic graph, boundary-region graph, and BFG quotient/fiber graph. These have different source objects and different D26 risk.
- A pure reaction graph is not independent evidence for autocatalytic_closure when the predicate is RAF/maxRAF on the same reaction declarations. It can be a diagnostic or predicate-internal sanity check, but not a substrate-blocked detector unless the source object is independently split.
- Repair cannot be recovered by renaming state-stream lenses. The repair predicate already uses the drop/recovery state or boundary trajectory. A recovery lens must operate on an independent perturbation-outcome ensemble, not the same trajectory.
- Replication_lineage cannot be recovered by reading the declared lineage ledger. A clean phylogenetic lens needs independent sequence/entity observations and reconstructs descent without using declared parent/child edges as features.
- Floor_connectivity is the highest self-match risk. A basin-geometry lens that reads `neutral_floor_index` is just the BFG predicate wearing a detector label. Floor recovery needs held-out perturbation graphs or a split BFG formalism.
- C024's "BAD" overloaded at least four states: historical token leak, no nondeclined source, D26 same-field overlap, and PARTIAL-cell ablation collapse. Round 2 should split these states in the schema/report so we stop treating domain decline as an engineering bug.
- C025 should not select "first clean lens" as the primary detector. That rule hid scientific distinctions between lens families. C025 should preregister each recovered cell and report per-cell evidence before any per-motif aggregate.

## Improved Recovery Taxonomy

Architect's four classes are directionally useful but too coarse. I recommend seven operational classes:

| Code | Name | Definition | Round 2 action |
|---|---|---|---|
| REF-STRUCT | Structural refactor | Dirty implementation can be rewritten over an already-present independent source object. | Implement clean variant and four-axis lens controls. |
| NEW-ABST | New abstraction layer | The right measurement exists, but it is a different scientific object than the v1 lens used. | Add `lens_variant_id`, source-object map, and tests before including in C025. |
| SCHEMA-SPLIT | Upstream source-object split | The measurement is plausible only if traces expose predicate evidence and lens evidence as separate objects or folds. | Build/ratify trace schema first; no detector until source split exists. |
| BAD-ARCH | Architecturally unrecoverable for claim evidence | Predicate and lens must read the same fundamental object/fields; independence is impossible for substrate-blocked evidence. | Keep excluded. It may remain diagnostic-only. |
| DOMAIN-DECLINE | Lens family not applicable to motif/substrate | The lens has no meaningful source object for this motif in this substrate. | Record as honest decline, not a RED engineering failure. |
| DIAG-ONLY | Useful diagnostic, not independent evidence | The lens checks internal consistency of the predicate object. | Allowed for QA/audit reports; forbidden as promotion evidence. |
| FORMALISM-REQ | Requires Phase 7 formalism | The project lacks the formal object needed to define a clean lens. | Route to Architect + PI before code. |

Schema implication: `lens_id` should become a family name, and every recovered cell should declare:

```yaml
lens_family_id: graph | crnt | dynamical_systems | topology | petri | statistical_mechanics | control_theory | information
lens_variant_id: string
recovery_class: REF-STRUCT | NEW-ABST | SCHEMA-SPLIT | BAD-ARCH | DOMAIN-DECLINE | DIAG-ONLY | FORMALISM-REQ
allowed_claim_role: substrate_blocked_evidence | diagnostic_only | honest_decline
source_object_map: list[source_object_entry]
source_object_split_required: bool
```

## Classification of the 33 BAD Cells

The table below classifies every Campaign 024 BAD cell. "Recover?" means recoverable as substrate-blocked evidence, not merely as a diagnostic plot.

| Motif | Lens | C024 failure mode | Class | Recover? | Round 2 recommendation |
|---|---|---|---|---|---|
| autocatalytic_closure | graph | Historical event/process leak; pure reaction graph would read predicate reaction declarations. | BAD-ARCH / DIAG-ONLY | No, for evidence | Keep as diagnostic-only unless reaction graph source is independently split from RAF predicate source. |
| autocatalytic_closure | crnt | Clean CRNT overlaps predicate reaction fields. | BAD-ARCH / DIAG-ONLY | No, for evidence | CRNT invariants are useful chemistry diagnostics, not independent RAF evidence on the same declaration object. |
| autocatalytic_closure | petri | Historical event leak plus reaction-field overlap. | BAD-ARCH / DIAG-ONLY | No, for evidence | Same as CRNT: incidence-matrix checks can audit the RAF object but cannot validate it independently. |
| repair | graph | No clean generic graph source; old graph was event/process-driven. | NEW-ABST + SCHEMA-SPLIT | Yes, after schema | Build perturbation-response graph from independent perturbation trials, not event streams or predicate trajectory. |
| repair | crnt | No reactions in current corpus; process-flag historical leak. | DOMAIN-DECLINE or SCHEMA-SPLIT | Conditional | Only recover for biochemical repair substrates with explicit repair chemistry; otherwise honest decline. |
| repair | dynamical_systems | PARTIAL state lens collapses when predicate state object denied. | SCHEMA-SPLIT | Yes | Use perturbation-outcome ensemble or held-out intervention fold, not the same drop/recovery series. |
| repair | topology | PARTIAL state lens collapses when predicate state object denied. | SCHEMA-SPLIT | Yes | Topology should operate on basin-of-recovery samples across perturbations, not the predicate trajectory. |
| repair | petri | No transitions/reactions in current corpus; event/process historical leak. | DOMAIN-DECLINE or SCHEMA-SPLIT | Conditional | Recover only if repair process is encoded as an independent transition system. |
| repair | statistical_mechanics | PARTIAL state lens collapses when predicate state object denied. | SCHEMA-SPLIT | Yes | Use recovery-time distribution, noise response, or restoration probability from independent perturbation ensemble. |
| repair | control_theory | PARTIAL state lens collapses when predicate state object denied. | SCHEMA-SPLIT | Yes | Use controllability/observability of intervention-response model fitted on held-out perturbations. |
| repair | information | PARTIAL state lens collapses when predicate state object denied. | SCHEMA-SPLIT | Yes | Use information flow from perturbation input to restored state on held-out trials; not state-key recovery itself. |
| externalized_memory | graph | Historical event/process/token leak; no channel graph variant implemented. | NEW-ABST | Yes | External-channel graph: nodes are external medium variables and internal readback variables; edges from lagged dependence, not event labels. |
| externalized_memory | crnt | No reaction network source. | DOMAIN-DECLINE | No | Honest decline for memory unless a chemical memory substrate supplies reaction declarations independently. |
| externalized_memory | petri | No transition-network source; historical event-transition proxy. | DOMAIN-DECLINE or NEW-ABST | Conditional | Petri channel model could exist for symbolic memory systems, but current corpus lacks it. |
| replication_lineage | graph | Historical event/process/token leak; clean graph battery had no lineage source. | NEW-ABST + SCHEMA-SPLIT | Yes | Phylogenetic graph variant must reconstruct graph from entity observations, not read declared lineage edges. |
| replication_lineage | crnt | No reaction source. | DOMAIN-DECLINE | No | Decline for lineage unless studying biochemical replicator reaction networks as a different motif bridge. |
| replication_lineage | dynamical_systems | No numeric state source for clean lens. | DOMAIN-DECLINE or NEW-ABST | Conditional | Recover only with population-frequency trajectory independent of declared lineage predicate. |
| replication_lineage | topology | No point-cloud/source object. | NEW-ABST + SCHEMA-SPLIT | Yes | Tree-space topology over reconstructed sequence/entity distances; requires sequence observations separate from lineage ledger. |
| replication_lineage | petri | No transition source; historical event/process leak. | DOMAIN-DECLINE or NEW-ABST | Conditional | Recover only for explicit reproduction transition systems independent of predicate ledger. |
| replication_lineage | statistical_mechanics | No state/statistical source; historical event/process leak. | NEW-ABST | Conditional | Population diversity/branching distribution lens if entity observations exist independent of parent labels. |
| replication_lineage | control_theory | No control source; historical token leak. | DOMAIN-DECLINE | No | Not a natural lineage lens under current formalism. |
| replication_lineage | information | No information source; historical event entropy. | NEW-ABST + SCHEMA-SPLIT | Yes | Heritable-information lens from parent/child sequences, but only if predicate does not read the same sequence fields. |
| self_maintained_boundary | graph | Historical event/process/token leak; no boundary graph variant implemented. | NEW-ABST + SCHEMA-SPLIT | Yes | Boundary-region adjacency graph from spatial/compartment geometry, not boundary tokens. |
| self_maintained_boundary | crnt | No reaction source; historical process flag. | DOMAIN-DECLINE or SCHEMA-SPLIT | Conditional | Recover if boundary maintenance chemistry is present as source object distinct from boundary predicate fields. |
| self_maintained_boundary | petri | No transition source; historical event/process leak. | DOMAIN-DECLINE or SCHEMA-SPLIT | Conditional | Recover if membrane maintenance is represented as a transition system independent of boundary object fields. |
| floor_connectivity | graph | No clean graph source; old graph out of domain. | FORMALISM-REQ | Conditional | Need quotient/fiber graph formalism over held-out perturbation outcomes. |
| floor_connectivity | crnt | No reaction source. | DOMAIN-DECLINE | No | Decline for BFG unless the substrate is specifically a reaction-network floor study, still likely diagnostic-only. |
| floor_connectivity | dynamical_systems | No clean state source; BFG score excluded. | FORMALISM-REQ | Conditional | Need basin-return lens from held-out perturbation trajectories, not neutral_floor_index fields. |
| floor_connectivity | topology | No clean topology source; BFG score excluded. | FORMALISM-REQ | Conditional | Need topology of equivalence fibers from raw perturbation graph, not predicate threshold summary. |
| floor_connectivity | petri | No transition source; historical event proxy. | DOMAIN-DECLINE | No | Decline unless floor object is explicitly a transition-system perturbation graph. |
| floor_connectivity | statistical_mechanics | No clean distribution source; event-stat historical leak. | FORMALISM-REQ | Conditional | Could measure perturbation energy/barrier distribution, but source object must be separate from predicate summary. |
| floor_connectivity | control_theory | No clean reachability source; token historical leak. | FORMALISM-REQ | Conditional | Reachability overlaps BFG Reach; only recover with held-out reachability experiment or keep BAD-ARCH. |
| floor_connectivity | information | No clean information source; event entropy historical leak. | DOMAIN-DECLINE or FORMALISM-REQ | Low | Only meaningful if BFG formalism defines information over equivalence fibers; not current v1 formalism. |

## Amendments to Architect's Lens-Variant Proposals

### Graph-pure variant

Architect draft: Use only reaction-graph topology, spectral properties, persistent homology, percolation thresholds, and graph-Laplacian spectrum on bipartite species/reaction graph.

// CODEX: This is not one graph lens. It is a graph lens family. Reaction graph topology is clean only for motifs whose predicate does not read reaction declarations. For autocatalytic_closure, reaction graph topology shares the predicate object and fields, so it is DIAG-ONLY or BAD-ARCH for substrate-blocked evidence.

// CODEX: Required variants:
- `graph.reaction_bipartite_topology`: reaction/species graph; diagnostic-only for RAF closure unless source split exists.
- `graph.perturbation_response`: nodes are perturbation trials/outcomes; candidate repair lens.
- `graph.external_channel`: nodes are external medium and internal readback variables; candidate memory lens.
- `graph.phylogenetic_reconstruction`: nodes are entities/sequences; edges inferred from distance, not declared parent labels.
- `graph.boundary_region`: nodes are compartments/boundary regions; edges from spatial adjacency/exchange.
- `graph.bfg_quotient_fiber`: nodes are perturbation equivalence classes; requires Phase 7 BFG formalism split.

### CRNT-pure

Architect draft: Use only stoichiometric-matrix invariants, deficiency, linkage classes, and weak reversibility.

// CODEX: Correct as a CRNT implementation, but not independent evidence for autocatalytic_closure when closure predicate reads the same reaction declarations. For closure it is diagnostic-only. It can be evidence for boundary/repair only if the predicate reads boundary/perturbation objects and CRNT reads a separate chemistry object.

### Petri-pure

Architect draft: Incidence matrix only, no process flags.

// CODEX: Same caution as CRNT. Petri-pure is not automatically independent. It is admissible only when the transition declarations are not the predicate source object, or when a source-object split makes predicate and Petri features disjoint under D26 plus ablation.

### Behavioral-recovery lens

Architect draft: Operate on perturbation-outcome distributions: recovery time, basin radius, equivalence-class restoration probability.

// CODEX: This is the right direction. It should be the primary repair recovery path. But it cannot read the single trajectory used by the repair predicate. C025 needs a new source object: `perturbation_response_ensemble`, with repeated perturbations, perturbation magnitudes, restoration outcomes, and recovery times. Predicate may read a separate held-out event/trajectory or a signed high-level verdict; lens reads the ensemble distribution.

### Phylogenetic lens

Architect draft: Operate on parent-child structure graphs of replicating entities, lineage edges, mutation distance, tree topology, branching rate, descent reconstructability.

// CODEX: If this reads declared `lineage.edges.parent` and `lineage.edges.child`, it self-matches the predicate. The clean version reconstructs descent from `entity_observations` or `sequence_observations` while blinded to declared lineage edges. Source split: predicate can read declared lineage ledger; lens reads sequence/entity distances and reconstructs a tree. Or invert it: predicate reads sequence-inheritance semantics, lens reads declared graph topology. It cannot read both.

### Basin-geometry lens

Architect draft: Operate on perturbation-outcome equivalence fibers; computes floor connectivity scores, fiber dimension, equivalence-class boundary geometry. Might be BFG predicate itself promoted to lens status.

// CODEX: Do not promote the BFG predicate itself to lens status. That is Class 13 self-match. The minimum clean design is a BFG split:
- Predicate source: signed `neutral_floor_index` or declared equivalence-fiber criterion.
- Lens source: held-out raw perturbation graph, boundary samples, or independent reachability experiment.
- Forbidden: lens reading `W_floor`, `P_equiv`, `L_func`, `I_inv`, `Reach`, or `Conn` if those are predicate threshold fields.

// CODEX: This is probably FORMALISM-REQ before Round 2 code. Floor needs a BFG measurement formalism, not a quick detector patch.

### Information-pure

Architect draft: Use mutual information between external state channels and future internal state; external qualifier is key.

// CODEX: Good for externalized_memory only if source objects are split. The predicate currently reads external medium and readback histories. An information lens can read lagged mutual information over external/internal channels, but C025 should use time-window or channel holdouts so the predicate and lens are not both reading the same evidence rows. For repair/lineage/floor, information-pure needs motif-specific source objects; generic event entropy is permanently forbidden.

## Per-Motif Current Formalism Assessment

### repair

Repair is not unmeasurable in principle. It is unmeasurable under the current v1 lens battery because all viable clean lenses collapse onto the same state/boundary trajectory that the predicate reads.

Sufficient Round 2 source object:

```yaml
perturbation_response_ensemble:
  trials:
    - perturbation_id
      perturbation_magnitude
      pre_state_summary
      post_damage_summary
      recovery_time
      restoration_fraction
      outcome_class
  fields_for_predicate: optional signed perturbation occurred + separate semantic recovery verdict
  fields_for_lens: distributional response features across trials
```

If that object exists with a holdout split, repair gets measurable through behavioral-recovery, topology-of-basins, statistical mechanics of recovery times, control-theory response, and information flow from perturbation to restoration. Without it, repair remains not evaluable under D26.

### replication_lineage

Replication_lineage needs a source-object split between declared lineage and independent entity observations. The current predicate reads lineage edges and may read inherited boundary/sequence fields. A phylogenetic lens that also reads those fields is self-match.

Sufficient Round 2 source objects:

```yaml
declared_lineage_ledger:
  nodes
  edges.parent
  edges.child

entity_observations:
  entity_id
  birth_time
  phenotype_vector
  genotype_or_sequence
  boundary_marker
```

Clean lens options:
- Graph/topology: reconstruct tree from entity observations, then measure branching/tree-likeness without parent labels.
- Information: heritable information across inferred parent-child pairs, but only if predicate did not use the same sequence fields.
- Statistical mechanics: lineage diversity/branching distribution from observations, not event counts.

This is schema work, but not necessarily Phase 7 formalism if the trace schema can expose entity observations cleanly.

### floor_connectivity

Floor is different. It likely needs Phase 7 formalism before honest recovery. The BFG predicate and the proposed basin-geometry lens are too close unless the source objects are split at the BFG level.

Sufficient Round 2 object is not just "more fields"; it is a formal separation:

```yaml
bfg_predicate_summary:
  neutral_floor_index fields used by predicate

heldout_perturbation_fiber_graph:
  perturbation nodes
  equivalence-class assignments blinded to predicate thresholds
  reachability observations
  boundary samples
  raw outcome profiles
```

Until this split is ratified, floor lens recovery should be parked as FORMALISM-REQ. A quick basin-geometry lens would create a cleaner-looking but still circular result.

## Substrate-Blocked Sweep Methodology Revision for C025

C024's method was useful as a falsifier, but C025 should revise four points:

1. Preregister per cell, not only per motif. Each recovered motif x lens variant gets its own signed source-object map, recovery class, adversarial controls, and expected decline conditions.
2. Replace "first admissible lens" with a per-cell result table plus a preregistered motif aggregate rule. Suggested aggregate: a motif survives only if at least two non-isomorphic lens variants survive, or one variant survives across at least two independent substrates. Do not aggregate DIAG-ONLY cells.
3. Add source-object holdout controls. For SCHEMA-SPLIT cells, deny the predicate source object to the lens and deny the lens source object to the predicate. If either side collapses, the cell is BAD.
4. Add matched-decoy generators. Event/payload/generator erasure is necessary but not sufficient; clean numeric summaries can still act as generator-family proxies. C025 should include label-opposite traces matched on trace length, source-object count, state dimensionality, and basic magnitude distributions.
5. Treat `DOMAIN-DECLINE` separately from `BAD`. A lens that correctly declines because no source exists is not a broken lens; it is a scoped instrument.
6. Preserve four-state predicate verdicts and exclude insufficient/malformed traces. No silent conversion to negative.
7. For floor, require a BFG formalism preregistration before any permutation run. If the BFG split is not ratified, floor remains not evaluable rather than patched.

## Recommended Round 2 Sequence

1. Extend the contract/report schema with `lens_variant_id`, `recovery_class`, and `allowed_claim_role`.
2. Reclassify C024 cells using the seven-state taxonomy above, while preserving the original CLEAN/PARTIAL/BAD D26 field.
3. Implement only the recovery paths that do not need unresolved formalism:
   - externalized_memory external-channel graph/info variants if source split can be made from existing histories.
   - self_boundary boundary-region graph only if boundary adjacency/source fields exist.
   - repair behavioral-recovery only after a perturbation-response ensemble fixture exists.
   - lineage phylogenetic reconstruction only after entity observations exist independent of declared lineage.
4. Park autocatalytic_closure CRNT/Petri/graph as DIAG-ONLY unless PI/Architect ratify a reaction-source split.
5. Park floor as FORMALISM-REQ unless BFG source-object split is ratified first.
6. Run four-axis controls plus source-object holdout controls on recovered cells.
7. Preregister and run Campaign 025 with per-cell reporting, then produce per-motif verdicts.

## Minimum Source-Object Contracts for Round 2

These are not implementation specs yet. They are the minimum scientific objects that must exist before a recovered lens can be trusted.

### perturbation_response_ensemble

Purpose: repair lenses.

Predicate-safe split:

- Predicate may read one signed semantic recovery verdict or one held-out trajectory per trial.
- Lens reads the distribution over trials: response curve, recovery time, restoration fraction, basin radius, and failure modes.
- Neither side reads event labels such as `repair_event`, scenario names, or generator IDs.

Required decoys:

- Same perturbation magnitude, no endogenous recovery.
- Exogenous reset that restores state but should fail repair semantics.
- Passive stability/no-damage control.
- Matched trace-length and state-dimensionality controls.

### external_channel_samples

Purpose: externalized_memory graph/information variants.

Predicate-safe split:

- Predicate tests causal effect of removing/scrambling external medium.
- Lens estimates lagged dependence from external channel at time `t` to internal state/readback at time `t + k`.
- C025 should use time-window holdouts: predicate and lens do not consume the same rows.

Required decoys:

- Internal recurrence with no external channel.
- External noise channel with same entropy but no future predictive value.
- Renamed channel keys and payload keys.

### entity_observations

Purpose: replication_lineage graph/topology/information/statistical variants.

Predicate-safe split:

- Predicate reads declared lineage ledger or signed descent relation.
- Lens reconstructs descent from entity observations while blinded to declared parent/child edges.
- Sequence or phenotype fields used by the lens must be withheld from the predicate if the predicate otherwise uses them.

Required decoys:

- Declared parent/child edges with randomized sequences.
- Similar sequences without parent-child temporal ordering.
- Growth/population increase without heritable descent.

### boundary_region_samples

Purpose: self_maintained_boundary graph/CRNT/Petri variants.

Predicate-safe split:

- Predicate reads operational boundary persistence and internal maintenance fields.
- Lens reads independent region adjacency, exchange graph, reaction/transition declarations for boundary production, or compartment topology.
- Static shells and externally reset shells are negative controls.

Required decoys:

- Closed shell with no internal maintenance.
- Boundary material restored only by external reset.
- Same boundary count and trace length with randomized region adjacency.

### heldout_perturbation_fiber_graph

Purpose: floor_connectivity BFG recovery.

Predicate-safe split:

- Predicate reads `bfg_predicate_summary` or a signed `neutral_floor_index`.
- Lens reads raw held-out perturbation graph, equivalence-class samples, boundary crossings, and reachability observations.
- The lens cannot read the predicate threshold fields `W_floor`, `P_equiv`, `L_func`, `I_inv`, `Reach`, or `Conn` unless those fields are explicitly withheld from the predicate.

Required decoys:

- Point-attractor/implementation-unique falsifier.
- Same function similarity but disconnected perturbation graph.
- Same connectivity score but invariant not preserved.
- Randomized equivalence-class assignments preserving class sizes.

## C025 Acceptance Gates

- Every recovered cell has `lens_variant_id`, `recovery_class`, `allowed_claim_role`, and signed source-object map.
- Every recovered evidence cell passes four-axis controls and source-object holdout controls.
- Every SCHEMA-SPLIT cell includes a fixture proving the predicate can run without the lens object and the lens can run without the predicate object.
- Every DOMAIN-DECLINE cell is counted separately from BAD and does not depress readiness.
- No DIAG-ONLY cell enters substrate-blocked promotion evidence.
- Floor connectivity does not run unless the BFG split is ratified before preregistration.
- C025 report exposes both per-cell and per-motif results; motif aggregate cannot hide a single-cell self-match.

## D27 Candidate

Candidate doctrine name: D27 - Substantive Lens Recovery.

Candidate text:

> A BAD motif-lens cell is not recovered by renaming a detector or moving the same computation behind a new interface. A recovered lens variant must declare a new or repaired source_object_map, a substantive measurement operation distinct from the predicate, an allowed claim role, and adversarial plus source-object holdout controls. If the recovered variant reads the same fundamental object and fields as the predicate, it remains BAD or DIAG-ONLY regardless of implementation cleanliness.

Operational tests:

- Cosmetic rename test: if replacing the variant name with the old lens name leaves the source_object_map and features unchanged, recovery fails.
- Source denial test: if the lens collapses when denied the predicate source object, it is BAD unless it is explicitly DIAG-ONLY.
- Claim-role test: every variant declares `substrate_blocked_evidence`, `diagnostic_only`, or `honest_decline`. Unlabeled variants cannot enter promotion evidence.
- Matched-decoy test: recovered lens must decline or lose signal on label-opposite decoys matched for generator family, trace length, source-object counts, and coarse numeric distributions.

Recommendation: Ratify D27 after Round 2 experience if it prevents at least one attempted cosmetic recovery.

## Bottom Line

The next move is not "recover 33 cells." The next move is to separate the cells into: permanently diagnostic, honestly inapplicable, schema-recoverable, and formalism-required. The cells most worth implementing in Round 2 are repair via perturbation-response ensembles, lineage via blinded phylogenetic reconstruction, and externalized_memory via external-channel graph/information variants. The cells most dangerous to implement prematurely are autocatalytic_closure reaction graph/CRNT/Petri and floor basin-geometry, because both can become mathematically polished self-matches.
