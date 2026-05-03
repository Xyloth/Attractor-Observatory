# Proposal #1 v2 — Basin-Floor Geometry as a Core Measurement Layer

*Sharpening of Proposal #1.txt by the Architect. Status: candidate v1.3 spec addition; eligible to become Campaign 009 once Campaign 008 closes.*

---

## 0. What v2 keeps from v1

The original proposal is the right idea, well argued, with the right risk discipline. v2 adopts wholesale:

- **The core insight.** "The slope explains convergence. The floor explains diversity." This is the canonical sentence and v2 keeps it verbatim.
- **`BasinFloorGeometry` as a first-class analysis object** living under `motifs/geometry/`, not as a scoring extension and not as a metaphor.
- **Vector-first reporting** of the `NeutralFloorIndex`. The scalar is a dashboard convenience, never a canonical claim.
- **Perturbation outcome model O1–O5.** O2 (different implementation, same motif) is the floor signature.
- **Calibration corpora for floor regimes** — flat, narrow, rugged, decoy.
- **Risk register.** The five risks v1 names (weak-selection mistaken for equivalence, over-broad motif definition, novelty overclaim, arbitrary metrics, formalism-as-metaphor) all carry over.
- **Honest novelty framing.** Floors, neutral networks, manifolds, canalization — known. The novelty is the *Observatory-integration* level: substrate-neutral floor measurement coupled to motif equivalence and formal-deficit detection.
- **Exploratory claim status only** until calibration and nulls exist.

v2's job is to sharpen six places where v1 stops just short.

---

## 1. The chain v1 implies but doesn't name

The original proposal connects floor geometry to "the final formalism layer" but doesn't draw the chain explicitly. v2 names it:

```
basin-floor geometry
  → operationalises cross-substrate attractor equivalence
  → which is one of v1.2 §9.7's named candidate missing-math priors
  → which gates L5+ claims in the v1.2 claim ladder
```

In other words: **Basin-Floor Geometry is the project's operational handle on its own L5+ ambition.** The Observatory's most ambitious claim — that recurring motifs across substrates expose gaps in current mathematical language — requires an operational definition of "the same motif across substrates." Floor geometry provides exactly that, by reducing the question to a measurable: *do these implementations occupy a connected neutral manifold under a function-preserving equivalence?*

This makes Basin-Floor Geometry not optional. Without it, "cross-substrate equivalence" stays metaphorical and L5 stays out of reach.

---

## 2. Formal object — what kind of mathematical thing the floor is

v1 says "the basin floor encodes implementation freedom" and lists known relatives. v2 commits to a formal stance:

The natural object is a **fiber bundle (or quotient space)** over a function space:

- **Base space** F: declared functional class, e.g., "autocatalytic closure with declared substrate-blind invariants." Each point in F is a function-instance — a particular closure semantics.
- **Total space** E: implementations — particular RAF graphs, particular ribozyme networks, particular protocell internal CRNs.
- **Projection** π: E → F maps each implementation to its function-instance.
- **Fiber** π⁻¹(f) over a base point f: the set of all implementations realising the same f. *This is the floor.*

`BasinFloorGeometry(M)` is, formally, a description of the fibers of π over the function class associated with motif M:

| Field | Formal meaning |
|---|---|
| `floor_dimensionality` | dimension of the typical fiber, in some appropriate parameterisation |
| `floor_width` | volume of the fiber under a chosen measure |
| `floor_ruggedness` | non-flatness of the fiber metric / number of disconnected components / curvature signal |
| `neutral_drift_rate` | expected dwell-time variance under intra-fiber perturbation |
| `implementation_diversity` | entropy over fiber clusters under a structure-aware distance |
| `exit_barrier` | minimal perturbation that crosses outside the fiber to a different π-preimage or out of E |
| `equivalence_invariants` | the function-instance f itself, recovered from any implementation in its fiber |

This commits the proposal to a specific kind of mathematics: **quotients, fibers, and equivariant structure**. Not category theory in the abstract — concrete fiber bundles where the fiber is the implementation class.

The deficit-map question becomes operationalisable: *does any existing lens (graph, CRNT, dynamical systems, topology, information theory, control theory, statistical mechanics, computational mechanics) encode "function-preserving quotient" as a primitive that the others compose to?* If no lens does, that is a candidate L5 result. The new formal object the project would propose is the *Floor Bundle* itself, with its own encode/decode/predict surface.

This is the formal-deficit hypothesis the proposal earns the right to make.

---

## 3. K9 is already the seed corpus

The original proposal calls for new K-corpora (K5–K8 floor calibration) and that's correct, but it misses that the *existing* `K9 — different-process / same-appearance` corpus is, by construction, a labeled basin-floor dataset. K9 pairs are pairs that look similar but differ in causation; equivalently, pairs whose superficial implementation features cluster together but whose function-instances differ.

For Basin-Floor Geometry v0, K9 is **the seed corpus**:

- K9 positives (same-process / different-implementation pairs, drawn from K2 and K8) are floor instances. Implementations should map to the same fiber under any honest floor detector.
- K9 negatives (different-process / same-appearance pairs) are floor decoys. Implementations should map to different fibers despite surface similarity.
- The K9 positive/negative distinction is *exactly* the floor detector's pass criterion.

This means the floor detector's first calibration step is free: train against K9, measure ROC AUC of "same fiber" prediction. Only after K9 is exhausted do K5_floor / K6_floor / K7_floor / K8_floor calibration corpora need to be built.

Renaming note: v1 proposed K5–K8 for floor calibration, but K5–K8 already exist (ambiguous knife-edge, OOD, multi-scale, same-process / different-appearance). v2 uses **KF1–KF4** for floor-specific calibration to avoid collision:

- **KF1** flat-floor calibration (broad neutral manifold)
- **KF2** narrow-basin calibration (point-like attractor)
- **KF3** rugged-floor calibration (multiple sub-basins separated by small barriers)
- **KF4** decoy-floor calibration (false implementation diversity that doesn't preserve invariants)

---

## 4. Reachability vs connectivity

v1 lists `neutral_drift_rate` and `floor_width` but doesn't separate two qualitatively different floor properties. v2 splits them:

- **Floor reachability** — how often does dynamics from initial conditions discover a floor point at all? This is a property of the dynamical system + initial-condition distribution, not of the floor's geometry. A wide floor can be unreachable if the slope into it is narrow or the basin of attraction is small.
- **Floor connectivity** — given a floor point, can the system drift along the floor (in the basin of attraction's interior) without exiting? This is a property of the floor's metric structure and the noise model.

Both matter, and they answer different scientific questions:

- *Reachability* answers "is this floor accessible to evolution / development / learning given the system's selection pressure and noise?" — relevant to biological convergence.
- *Connectivity* answers "if you put a system on the floor, can it stay there while exploring different implementations?" — relevant to evolvability and robustness.

A floor with high connectivity but low reachability is a *latent* floor — it's there, but real systems don't find it. A floor with high reachability but low connectivity is a *visited but trapped* floor — real systems find it but get stuck in one implementation. Neither alone supports the cross-substrate equivalence claim; both together do.

`BasinFloorGeometry` v2 carries:

```
floor_reachability:    {discovery_rate, basin_of_attraction_volume, time_to_first_floor_visit}
floor_connectivity:    {intra_fiber_distance_distribution, escape_rate_under_perturbation, percolation_threshold}
```

The Neutral Floor Index vector includes both as separate components.

---

## 5. Per-world implementation-diversity distance metrics

v1 says "implementation diversity" without defining the distance. v2 commits to specific metrics per world family. Each is structure-aware and has a published reference implementation.

| World | Distance metric for implementation clustering |
|---|---|
| W1 CRN | Graph edit distance on the catalytic-dependency subgraph, normalised by reaction count + Hamming distance on stoichiometric matrix rows for shared species |
| W2 protocell | Hamming distance on internal CRN reactions + Wasserstein distance on boundary-component composition |
| W3 field | Persistence-diagram bottleneck distance on filtration of reaction-product field at a fixed time + multiscale variance signature |
| W4 morphogenesis | Tree edit distance on lineage graph + KL divergence on cell-type distribution + GRN topology Hamming |
| W5 digital | Levenshtein edit distance on genome + opcode-frequency Hamming + task-completion vector cosine |
| W6 ecosystem | Quasi-isomorphism distance on trophic web + species-niche-matrix Frobenius distance |
| W7 swarm | Trail-network graph edit distance + role-distribution KS |
| W8 cognitive | World-model representation distance under task-blind probe (canonical correlation analysis) |
| W9 origins-chemistry | Surface-coverage Hamming + pore-network graph edit distance |
| W10 hypergraph | Hyperedge bipartite-graph edit distance |
| W11 quasispecies | Hamming distance on master-sequence + neutral-network connectivity profile |
| W12 symbiogenesis | Pair-distance combining each constituent's W1/W2 metric + exchange-channel cardinality |
| W13 multi-scale | Pair-distance over component worlds + cross-scale flux profile distance |

Implementation diversity is the Shannon entropy of cluster assignments under any of these metrics, computed at multiple cluster-radius scales (giving a multi-scale entropy curve, not a single number).

This gives Basin-Floor Geometry a real per-substrate ground truth and lets cross-substrate floor comparison happen via a normalised diversity profile rather than via raw cluster counts.

---

## 6. Computational cost — honest, with stratification

Naïve cost: 5 motifs × 200 perturbations × 13 worlds × 100 step replays = 1.3 million trace fragments per Basin-Floor Geometry run. That is real compute. The proposal acknowledges floor extraction is expensive but doesn't propose a strategy.

v2 adopts a **stratified perturbation scheme**:

1. **Free perturbations from K9.** K9 pairs already exist; treat each pair as one perturbation outcome at the labeling resolution. Cost: zero.
2. **Single-coordinate perturbations.** For each motif-positive trace, perturb one coordinate at a time at three magnitudes (small / medium / large). Classify outcomes O1–O5. Cost: ~6× per coordinate × N motifs.
3. **Synthetic ensemble perturbations.** Only after single-coordinate perturbations are exhausted, generate ensemble perturbations (multiple coordinates simultaneously) targeted at the under-explored fiber regions surfaced by single-coord results.
4. **Adaptive escalation.** A motif whose floor signal is clear at level 2 stops there. A motif whose level-2 signal is ambiguous escalates to level 3.

This makes the perturbation budget **adaptive to motif difficulty** and uses K9 as a free bootstrap. The expected cost for a Phase-1 floor analysis on the 5 strongest motifs is ~50,000 trace fragments, not 1.3 million.

A `floor_perturbation_budget` field is added to the Observatory's compute-orchestration telemetry, making the cost auditable.

---

## 7. Negative results are first-class

v1 reports the metric vector but doesn't elevate the negative case. v2 makes it explicit:

If floor analysis on a motif reveals **`floor_dimensionality ≈ 0`**, that is a *real result*. It says "this motif, in this world, lives at a point — there is no floor of equivalent implementations." For motifs claimed to be *substrate-neutral*, this is a falsifier.

The `BasinFloorGeometry` schema includes a `floor_falsifier` field:

```
floor_falsifier: {
  is_point_attractor:        bool      # floor_dimensionality below noise floor
  is_implementation_unique:  bool      # implementation_diversity ≤ 1.0 + ε
  conflicts_with_claim:      list[ClaimID]   # claims this falsifies if true
  status:                    enum {falsifier_active, exploratory, retired}
}
```

A motif whose floor analysis returns a point-attractor verdict is *useful negative evidence* — it constrains the cross-substrate equivalence claim by saying "the equivalence does not extend through implementation freedom for this case." That is publishable.

---

## 8. Per-world floor signatures as the cross-substrate claim made operational

The original proposal hints at this in §10 but doesn't make it the headline. v2 promotes it:

The cross-substrate equivalence hypothesis becomes:

> *Motifs that are claimed to be substrate-neutral exhibit floor signatures (dimensionality, connectivity, reachability, invariant-set) that match across world families above a declared similarity threshold, after accounting for substrate-specific distance-metric normalisation.*

This is testable. For each candidate substrate-neutral motif (closure, self-maintained boundary, externalised memory, etc.), compute the floor signature in each substrate where the motif appears. Match signatures across pairs. The match must survive:

- detector ablation (floor-signature stability when individual detectors are removed)
- distance-metric perturbation (different distance metrics over the same motif/substrate should produce similar signatures)
- substrate-blind projection (floor signature computed under substrate-erased evidence should match the substrate-aware signature within a declared band)

A motif with matching floor signatures across ≥3 substrates is a substrate-neutrality candidate at L3. A motif with matching signatures plus a uniform invariant-set across substrates is a candidate for L5+ formal-deficit analysis.

This makes Basin-Floor Geometry the operational bridge from "we found the same motif across worlds" to "we measured the equivalence relation that justifies calling them the same."

---

## 9. Schema additions, fully specified

```
BasinFloorGeometry = {
  geometry_id:                BasinFloorGeometryID,
  motif_id:                   MotifID,
  motif_registry_version:     SemVer,
  basin_id:                   BasinID | null,
  world_family:               WorldFamily,
  trace_set:                  list[TraceID],
  source_pos_count:           int,                          # motif-positive source traces
  perturbation_budget:        PerturbationBudget,
  perturbation_outcomes:      PerturbationOutcomeProfile,
  floor_onset:                FloorOnsetMeasurement,
  floor_dimensionality:       DimensionalityEstimate,       # with uncertainty
  floor_width:                {volume, measure_id, ci_low, ci_high},
  floor_ruggedness:           {non_flatness, component_count, curvature_signal},
  neutral_drift_rate:         {dwell_variance, mixing_time, ci},
  implementation_diversity:   MultiscaleEntropy,            # entropy curve, not scalar
  exit_barrier:               {minimum_perturbation, percolation_threshold},
  equivalence_invariants:     EquivalenceInvariantReport,
  floor_reachability:         {discovery_rate, basin_volume, time_to_first_visit},
  floor_connectivity:         {intra_fiber_distance_dist, escape_rate, percolation_threshold},
  floor_falsifier:            FloorFalsifier,
  cross_substrate_signature:  CrossSubstrateSignature | null,
  detector_provenance:        list[DetectorRef],
  null_contested:             list[NullSpecID],
  confidence:                 float in [0, 1],
  uncertainty:                UncertaintyEnvelope,
  provenance:                 ProvenanceRef,
  mode_tag:                   {foundational, exploratory, claim-bearing},
  spec_version:               ContentHash,
}

PerturbationOutcomeProfile = {
  total_perturbations:        int,
  outcome_counts:             {O1, O2, O3, O4, O5},
  outcome_rates:              {O1, O2, O3, O4, O5},   # normalised
  perturbation_kind_breakdown: dict[PerturbationKind, OutcomeCounts],
  same_motif_after_perturbation_rate: float,
  preserved_invariant_rate:   float,
}

EquivalenceInvariantReport = {
  declared_invariants:        list[InvariantSpec],
  preservation_rate:          dict[InvariantID, float],   # per-invariant
  invariant_strength:         float,                       # composite
  failure_modes:              list[InvariantFailure],
  spec_version:               ContentHash,
}

CrossSubstrateSignature = {
  substrate_pairs:            list[(WorldFamily, WorldFamily)],
  signature_distance:         dict[Pair, float],
  similarity_threshold:       float,
  matches_above_threshold:    list[Pair],
  substrate_blind_signature:  Signature | null,
  consistent_under_substrate_blind:  bool,
}

NeutralFloorIndex = {              # vector-first; scalar is dashboard only
  W_floor:                    float,    # floor_width
  D_floor:                    float,    # floor_dimensionality
  H_impl:                     float,    # implementation_diversity (composite)
  R_drift:                    float,    # neutral_drift_rate
  P_equiv:                    float,    # P(same motif | perturbation)
  L_func:                     float,    # functional_loss under floor drift
  I_inv:                      float,    # invariant preservation strength
  Reach:                      float,    # floor reachability composite (NEW v2)
  Conn:                       float,    # floor connectivity composite (NEW v2)
  scalar_projection:          float | null,
  projection_method_id:       str | null,
}
```

---

## 10. Acceptance gates for Campaign 009 — Basin-Floor Geometry v0

Twelve acceptance gates. None satisfiable by adding files; each demands a measurement.

| Gate | Threshold | Source |
|---|---|---|
| BFG1 | `BasinFloorGeometry` schema implemented; round-trip to/from JSON exact | `motifs/geometry/basin_floor.py`, tests |
| BFG2 | Perturbation outcome classifier operational on W1, W2, W4, W5; classifies into O1–O5 with declared confidence | `motifs/geometry/perturbation_outcomes.py`, tests |
| BFG3 | KF1–KF4 calibration corpora ≥20 scenarios each, world-driven (not number-generators) | `worlds/calibration/kf*.py`, calibration report |
| BFG4 | Floor detector achieves ROC AUC ≥ 0.85 on K9 (re-used as floor seed) | `reports/campaign_009/floor_seed_calibration.json` |
| BFG5 | Floor detector ECE ≤ 0.07 post-isotonic calibration on K9 | same |
| BFG6 | Floor detector achieves ROC AUC ≥ 0.80 on KF1+KF2+KF3+KF4 (decoy-resistant) | `reports/campaign_009/floor_calibration_full.json` |
| BFG7 | Implementation-diversity distance metrics implemented and tested for ≥6 world families | per-world distance modules, tests |
| BFG8 | Stratified perturbation budget enforced; cost telemetry auditable | `reports/campaign_009/perturbation_budget.json` |
| BFG9 | NeutralFloorIndex vectors computed for ≥5 motif/world pairs with bootstrap CIs of width ≤ 0.20 on key components | `reports/campaign_009/nfi_vectors.json` |
| BFG10 | Cross-substrate floor signature comparison run for ≥3 candidate substrate-neutral motifs across ≥3 substrates each | `reports/campaign_009/cross_substrate_signatures.json` |
| BFG11 | At least one motif's floor analysis is reported as a *floor falsifier* (point-attractor verdict) and routed to the falsifier ledger; or, if all motifs have non-trivial floors, this is reported as such with full evidence | `papers/falsifiers/`, `reports/campaign_009/falsifier_audit.json` |
| BFG12 | All preceding green; reproducibility script regenerates BFG1–BFG11 end-to-end from cold; pytest passes; D14 lint passes; no regression on Campaigns 002, 005, 006, 007, 008 | `make_campaign_009.py`, full regression |

---

## 11. Forbidden patterns (D-doctrine extension)

Three new doctrine items, binding from Campaign 009:

**D15 — No engineered floor.** A floor detector that returns positive on K9-positives and negative on K9-negatives by reading the K9 labels (or any field that is informationally equivalent to the labels) is a D15 violation. Detectors must operate on traces under substrate-blind projection.

**D16 — Implementation-diversity is multi-scale.** A scalar implementation-diversity number is forbidden. Diversity is reported as an entropy curve over a range of cluster radii. The curve's shape is the scientific object.

**D17 — Floor falsifiers are publishable.** A motif whose floor analysis returns a point-attractor verdict is a *result*, not a failure. The falsifier is committed to `papers/falsifiers/` with full provenance and may not be deleted or downgraded merely because it is inconvenient.

---

## 12. What this earns the project

If Basin-Floor Geometry v0 lands at full strength:

- **L3 → L4 transition becomes assessable.** The cross-substrate equivalence hypothesis is testable, not metaphorical.
- **L5 candidate motifs get formal mass.** A motif whose floor signature matches across substrates and whose invariants can be encoded by no existing lens is a real L5 candidate. Without floor geometry, "matches across substrates" is hand-wave; with it, it is a measurement with a confidence interval.
- **The Periodic Table of Stable Energy-Information Forms gets its principle of categorisation.** Rows by closure rank (already in v1.2 §19); columns by floor signature class. A cell in the table is a (closure-rank, floor-signature) pair, populated by motif instances from multiple substrates.
- **The Observatory becomes a discovery instrument** rather than a confirmation engine. Motifs surface not by matching pre-defined templates but by occupying floors that current mathematics struggles to encode compactly.

---

## 13. Bottom line for v2

The original proposal's bottom line stands: this is a serious upgrade, not a metaphor. v2 extends it in six places:

1. Names the formal object: a fiber bundle / quotient space, with the fiber as the floor.
2. Recognises K9 as the seed corpus already labeled and ready.
3. Splits floor reachability from floor connectivity.
4. Specifies per-world implementation-diversity distance metrics.
5. Stratifies the perturbation budget honestly.
6. Promotes negative results (point-attractor verdicts) to first-class outputs.

The Observatory's most ambitious claim — that recurring motifs across substrates expose gaps in current mathematical language — needs Basin-Floor Geometry to be operational rather than rhetorical. v2 is the version that makes that operationalisation concrete enough for Codex to build, while preserving v1's discipline against overclaim.

Status: **eligible to become Campaign 009** once Campaign 008 closes its strict substance floors. Until then: candidate v1.3 spec addition, exploratory tag.

— The Architect.
