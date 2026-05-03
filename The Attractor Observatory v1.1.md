# The Attractor Observatory — v1.1

*A deepened specification, derived from v1.0, prepared for implementation handoff to Codex.*

---

## 0. Preamble: what changed from v1.0, and why

v1.0 is correct in ambition and roughly correct in shape. v1.1 does not retract any of v1.0's claims; it tightens them, makes them falsifiable, and turns the diagrammatic gestures into contracts.

The diff against v1.0 is concentrated in nine load-bearing places:

1. **AttractorStrength is reformulated.** v1.0's product form `R · P · B · X · D · C · V` collapses to zero on any zero factor and conflates very different quantities. v1.1 replaces it with a weighted log-additive composite with explicit floors, units, and an uncertainty envelope (§1.4, §8.6).
2. **`SystemTrace` becomes a versioned schema, not a sketch.** Types, units, sampling policy, conservation invariants, determinism class, and on-disk layout are specified (§4).
3. **"Formal coverage" becomes an operational round-trip test** with concrete metrics (encoding success, invariant preservation, compression ratio, predictive transfer). No more "partial / weak / missing" labels without a number behind them (§9).
4. **Detectors require ground truth.** A *Calibration Corpus* of synthetic worlds with known motifs is introduced as a first-class artifact, on equal footing with the simulation engines themselves (§8.3, §6.2).
5. **Null-model architecture is made explicit.** A hierarchy of nulls (run-level, network-level, lineage-level, phylogenetic-block) is specified, and every claim names which null it is contesting (§6.3).
6. **Pre-registration is required for every flagship experiment.** Predictions, thresholds, stopping rules, and analysis paths are committed before the run (§6.7).
7. **The biology grounding layer accounts for phylogenetic non-independence, fossil/occurrence sampling bias, and held-out clades.** Naïve clade-overlap statistics are explicitly disallowed (§10).
8. **A risk register is introduced.** Twenty-four named risks are tracked with owners, triggers, and mitigations, including the project's most dangerous risk: self-confirming pipelines (§11).
9. **Codex task atoms get a defined format and size buckets.** This makes hand-off mechanical rather than aspirational (§13).

Three things that v1.0 already does well are preserved unchanged: the world-ensemble pluralism, the claim ladder from descriptive to formal, and the insistence that the trace format — not any single simulator — is the project's load-bearing artifact. v1.1 doubles down on all three.

---

## 1. Strengthened research framing

### 1.1 What kind of object the Observatory is

The Observatory is best understood as **a computational instrument for a science that does not yet have a name**. It is closer in spirit to an electron microscope than to a hypothesis-testing study: most of its value comes from making certain regularities *visible at all*, not from confirming a specific guess about them. This framing has three direct consequences:

- The instrument's correctness is judged primarily by its **null-handling and false-positive control**, not by what it discovers. A microscope that hallucinates structure in clean water is worthless even if it sometimes shows real cells.
- The instrument must be **substrate-neutral by construction**, not by promise. If the trace format silently encodes assumptions specific to chemistry or to agents, every cross-substrate comparison is contaminated.
- The instrument's **observers are themselves objects of study**. The motif grammar, the formal lenses, and the human-audit policy all shape what is seen; v1.1 therefore treats the detector and lens registries as primary scientific outputs, not auxiliary tooling.

### 1.2 The claim ladder, sharpened

v1.0's success levels are correct in spirit. v1.1 makes each rung carry a precise pass condition.

| Rung | Claim | Pass condition (operational) |
|------|-------|------------------------------|
| L1 — Framework | The system can mine recurring process-forms from heterogeneous worlds via a common trace. | A trace produced in one world family round-trips through a different world family's analysis pipeline without information loss exceeding a published threshold (§4.8). |
| L2 — Discovery | The system surfaces motifs not explicitly programmed. | At least one motif scoring above the strength floor (§1.4) is detected in ≥3 independent world families with no rule pre-specifying it, and is reproduced on held-out seeds. |
| L3 — Grounding | Earth biology occupies a non-random subset of the discovered attractor space. | Phylogenetically corrected occupancy of high-strength basins exceeds matched null distributions at α = 0.001 with FDR-controlled multiple-comparison correction (§6.4). |
| L4 — Prediction | The map predicts held-out cases. | Pre-registered predictions on (a) held-out clades and (b) held-out simulation regimes achieve out-of-sample accuracy above the strongest available baseline by a pre-declared margin. |
| L5 — Formal deficit | Recurring high-strength motifs exceed current mathematical compression. | At least one motif with confirmed strength has a measured Formal Coverage Score below a published threshold across all lenses in the registry, with the residual quantified and reproducible (§9). |
| L6 — New formal object | A new abstraction compresses or predicts better than existing descriptions. | A formal object proposed by the project, when added to the lens registry, raises Coverage Score on the deficit motif by a pre-declared margin without raising it on adversarial controls (§9.7). |

Rungs L5 and L6 are the only ones the project should ever describe as "missing math" claims, and only in writing, after passing the corresponding test. Casual use of the phrase below L5 is forbidden in any artifact bearing the project's name.

### 1.3 Falsifiers and dignified failure modes

A project that cannot be wrong is not a science project. The following are the named **falsifiers** for v1.1, in descending order of severity:

- **F1 (kills L3+):** After phylogenetic and sampling-bias correction, biology's occupancy of high-strength basins is statistically indistinguishable from a substrate-blind null. Conclusion: the simulation worlds and Earth's life history may share surface vocabulary but not deep attractor structure.
- **F2 (kills L2):** "Discovered" motifs are reliably traceable to artifacts of detector dictionaries (e.g., they vanish under detector ablation, or appear in adversarial worlds designed to lack them). Conclusion: the motif layer is hallucinating.
- **F3 (kills L1):** Cross-world traces fail round-trip without information loss. Conclusion: the substrate-neutral promise is not delivered; the project must either fix the trace or restrict claims to within-family analyses.
- **F4 (kills L5):** Formal Coverage Scores depend on the choice of lens registry to a degree that swamps motif effects. Conclusion: the formal-deficit map is measuring our taste in mathematics, not biology.
- **F5 (kills L6):** Proposed new formal objects gain coverage uniformly across motifs and adversarial controls. Conclusion: we built a flexible curve-fitter, not a discovery.

Each falsifier has a designated detection routine in the validation plan (§6). The project commits in advance to publishing falsifications as primary results, with the same prominence as confirmations.

### 1.4 Reformulating Attractor Strength

v1.0 defines `AttractorStrength = R · P · B · X · D · C · V`. This is unsuitable for three reasons: (i) any zero factor zeroes the score, masking mostly-strong motifs that have one weak dimension; (ii) it lacks units and any notion of uncertainty; (iii) it confuses orthogonal concepts (recurrence and persistence are correlated; basin width and implementation diversity are not).

v1.1 defines:

```
AttractorStrength(M) = Σ_i w_i · z_i(M)        # primary, weighted log-z composite
                        with floors f_i and uncertainty envelope U_i

where z_i(M) = clip( log(x_i(M) / x_i^ref),  f_i, ∞ )
      x_i = one of: R, P, B, X, D, I, C_pred, S_obs
      U_i = bootstrap CI from per-run resamples
```

The components are redefined to be orthogonal and operationalised:

- **R** — recurrence: number of independent runs (different seeds, same world family, same parameter neighbourhood) in which the motif is detected with confidence above τ. Units: dimensionless count.
- **P** — persistence: the fraction of trace duration during which the motif is detected, normalised by the half-life of the underlying world's noise time-scale. Units: dimensionless.
- **B** — basin width: volume of the parameter neighbourhood, in normalised parameter space, in which detection probability exceeds 0.5. Units: dimensionless volume after rank-normalisation.
- **X** — cross-family transfer: number of distinct world families in which detection occurs. This component is *capped* and combined as min(X, X_max) to prevent inflation.
- **D** — implementation diversity: a Shannon entropy over the binned implementation-class distribution of detected instances within a family.
- **I** — invariance under detector ablation: stability of detection when components of the detector pipeline are removed (§8.5).
- **C_pred** — predictive contribution: pre-registered out-of-sample improvement when the motif is added as a feature.
- **S_obs** — sampling sufficiency: 1 − (estimated remaining basin probability mass) from a coverage estimator (§6.5).

Two derived scores layer on top:

- **Formal Coverage** F(M) ∈ [0, 1] from the round-trip test (§9).
- **Formal Gap** G(M) = AttractorStrength(M) · (1 − F(M)), reported with both numerator and denominator visible.

Crucially, the project never reports a single AttractorStrength number without its uncertainty envelope and the ablation profile that produced it. The score is a vector with a scalar projection, not a scalar.

### 1.5 Adjacent fields and our explicit relationship to each

The Observatory inherits from many traditions and must declare which inheritances it accepts as load-bearing and which it merely cites.

- **Artificial Life (Avida, Tierra, Lenia, Flow-Lenia, particle-Lenia, neural CAs).** Load-bearing for the digital and field worlds. We reuse trace conventions where possible.
- **RAF / autocatalytic-set theory (Hordijk, Steel, Kauffman).** Load-bearing for the chemistry stack. We use standard RAF detection as the *seed* algorithm and extend it.
- **Chemical Reaction Network Theory (Feinberg, Horn-Jackson, Anderson).** Load-bearing for the formal-lens registry, especially deficiency theory and persistence/permanence.
- **Free-Energy Principle and Markov-blanket formalisms (Friston, Pearl).** *Cited but not load-bearing.* The Markov-blanket idea is one detector among many for the boundary motif. The project does not stake its scientific credibility on the FEP being correct.
- **Autopoiesis (Maturana, Varela) and (M, R)-systems (Rosen).** *Conceptual ancestor.* We translate the intuitions into operational tests rather than adopting the philosophical stance.
- **Major-transitions framework (Maynard Smith, Szathmáry).** Load-bearing for the closure-rank ladder and for the biology-grounding test set.
- **Convergent evolution literature.** Load-bearing for benchmark cases (eyes, flight, eusociality, branching transport).
- **Topological Data Analysis (Carlsson, Edelsbrunner-Harer, Ghrist).** Load-bearing for the field worlds and for cross-substrate motif comparison.
- **Information theory and computational mechanics (ε-machines, predictive states, transfer entropy).** Load-bearing for the memory/prediction motifs.
- **Category theory and applied compositional structures (Spivak, Fong-Spivak, Baez-Pollard).** *Aspirational.* If a substrate-invariant attractor class becomes a candidate new formal object, this is the most plausible language for it. We do not assume it is the right answer.
- **Niche construction and extended evolutionary synthesis.** Load-bearing for the externalized-memory motif.

This map is a contract: papers and code must explicitly indicate which inheritance they are activating, so reviewers can assess whether the cited tradition's assumptions actually hold in our setting.

### 1.6 What the Observatory is *not*

To prevent scope creep:

- It is not a theory of the origin of life. It can host such theories as world configurations.
- It is not a unified theory of biology. It is an instrument that may make such theories testable.
- It is not a general-purpose ALife platform. Worlds exist to feed the trace; their internal aesthetics are subordinate.
- It is not a benchmarking suite for ALife. Comparisons across ALife implementations are a side effect, not a goal.
- It is not an AGI project. Cognitive worlds are minimal proto-cognition for the purposes of motif extraction.

---

## 2. Expanded system architecture

### 2.1 Architectural planes

v1.0 lays out an `attractor-observatory/` directory tree but does not separate concerns. v1.1 imposes four architectural planes, each with its own evolutionary tempo and its own correctness criteria.

```
┌──────────────────────────────────────────────────────────────────┐
│ ATLAS PLANE         (slow-changing, public-facing)               │
│   periodic table │ atlas DB │ replays │ paper figures            │
├──────────────────────────────────────────────────────────────────┤
│ ANALYSIS PLANE      (medium-changing, scientifically primary)    │
│   motif registry │ detectors │ lens registry │ scoring │ nulls   │
├──────────────────────────────────────────────────────────────────┤
│ DATA PLANE          (append-only, schema-versioned)              │
│   SystemTrace store │ event store │ lineage store │ ledgers      │
├──────────────────────────────────────────────────────────────────┤
│ SUBSTRATE PLANE     (fast-changing, world-specific)              │
│   world engines │ search/orchestration │ perturbation │ HPC glue │
└──────────────────────────────────────────────────────────────────┘
                ↑           Provenance graph spans all planes ↑
                ↑           Telemetry plane spans all planes  ↑
```

The cardinal rule: **information flows up, never down**. The Atlas reads from the Analysis plane only via the Motif Registry and Atlas DB; the Analysis plane reads from the Data plane only via the trace store; the Data plane reads from the Substrate plane only via export. No layer above the Data plane may read a world's internal state directly. This is what makes substrate-neutrality enforceable.

The provenance graph and telemetry plane are orthogonal: every artifact in every plane carries a provenance record back to its inputs, and every component emits structured telemetry into a separate sink that does not influence scientific outputs.

### 2.2 Component map

```
attractor-observatory/
├── core/                       # shared kernel
│   ├── ids.py                  # typed IDs (TraceID, MotifID, RunID, …)
│   ├── units.py                # unit handling (pint or in-house)
│   ├── rng.py                  # determinism guarantees
│   ├── provenance.py           # provenance graph primitives
│   ├── telemetry.py            # structured logging, metric emit
│   ├── invariants.py           # conservation/validity check framework
│   ├── manifests.py            # run manifest schema
│   └── errors.py               # typed errors with severity classes
│
├── trace/                      # the data plane
│   ├── schema/                 # versioned schemas (v1, v1.1, …)
│   ├── store/                  # on-disk store (Parquet/Zarr/HDF5)
│   ├── reader.py               # pull-based reader API
│   ├── writer.py               # streaming writer API
│   ├── migrate.py              # schema migrations
│   ├── verify.py               # integrity, conservation, determinism
│   └── sbml_bridge.py          # SBML import/export
│
├── worlds/                     # the substrate plane
│   ├── world_api.py            # the World contract (§3.4)
│   ├── crn/                    # chemical reaction network
│   ├── raf/                    # autocatalytic set focus
│   ├── protocell/
│   ├── fields/                 # reaction-diffusion, Lenia-family
│   ├── morphogenesis/
│   ├── digital/                # Avida-class digital organisms
│   ├── ecosystem/
│   ├── swarm/
│   ├── cognitive/
│   └── calibration/            # synthetic worlds with known motifs
│
├── search/                     # search & orchestration over worlds
│   ├── samplers/               # LHS, Sobol, novelty, QD, BO
│   ├── adversarial/            # perturbation generators
│   ├── curriculum/
│   ├── scheduler.py            # job graph, retry, dedup
│   └── coverage.py             # parameter-space coverage metrics
│
├── motifs/                     # the analysis plane (motif side)
│   ├── grammar/                # primitive roles, relations, operators
│   ├── registry/               # versioned motif ontology
│   ├── detectors/
│   │   ├── closure.py
│   │   ├── boundary.py
│   │   ├── recurrence.py
│   │   ├── topology.py
│   │   ├── information.py
│   │   ├── graph_motifs.py
│   │   ├── lineage.py
│   │   ├── memory.py
│   │   └── _ablation.py        # detector-ablation harness
│   ├── triangulation.py        # cross-detector consensus
│   ├── confidence.py           # calibration, ECE, Brier
│   └── scoring.py              # AttractorStrength, basin width, etc.
│
├── formalism/                  # the analysis plane (math side)
│   ├── lenses/                 # one module per formalism
│   │   ├── crnt.py
│   │   ├── dynsys.py
│   │   ├── topology.py
│   │   ├── information.py
│   │   ├── control.py
│   │   ├── petri.py
│   │   ├── category.py
│   │   ├── stat_mech.py
│   │   └── comp_mechanics.py
│   ├── coverage.py             # round-trip / invariance / compression tests
│   ├── proposals/              # candidate new formal objects (§9.7)
│   └── deficit_map.py
│
├── biology/                    # biology grounding
│   ├── sources/                # OTL, PBDB, GBIF, NCBI, GTDB, KEGG
│   ├── ingestion/              # ETL with provenance + license metadata
│   ├── trait_coding/           # standardised trait coding spec
│   ├── observation_model/      # absence/uncertainty handling
│   ├── phylo_correction.py     # PIC, PGLS, BAMM-style
│   ├── sampling_bias.py        # PBDB/GBIF correction models
│   └── mapping.py              # motif↔biological-trait alignment
│
├── nulls/                      # the null-model factory
│   ├── seed_shuffle.py
│   ├── network_rewire.py
│   ├── lineage_shuffle.py
│   ├── phylogenetic_blocks.py
│   ├── adversarial_worlds.py
│   └── multitest.py            # FDR/FWER procedures
│
├── validation/                 # validation gauntlet runner
│   ├── gauntlet.py
│   ├── prereg.py               # preregistration manager
│   ├── thresholds.py
│   └── reports/
│
├── atlas/                      # atlas plane
│   ├── db.py                   # the Atlas DB (curated)
│   ├── embeddings.py
│   ├── visualization.py
│   ├── replay.py
│   └── periodic_table/
│
├── ops/                        # operational tooling
│   ├── containers/             # OCI images
│   ├── schedulers/             # SLURM/K8s adapters
│   ├── audit/                  # human-in-the-loop interfaces
│   ├── secrets/
│   └── ci/                     # determinism, schema, license CI
│
└── papers/                     # reproducibility-bound paper artifacts
    ├── figures/
    ├── tables/
    ├── methods/
    └── prereg/
```

### 2.3 Determinism, replay, and provenance

These three properties are non-negotiable.

- **Determinism class.** Every world declares one of: `strict` (bit-identical given seed and platform), `replayable_to_eps` (numerical drift bounded by ε on the same hardware class), or `stochastic` (only distributional reproduction is guaranteed). The class is part of the manifest. Stochastic worlds must publish a drift bound and an estimator for it.
- **Seed propagation.** A single root seed is split into substreams using a counter-based RNG (e.g., Philox or Threefry). No component pulls from a global RNG. Forks (e.g., parallel parameter sweeps) record the substream counter as part of the manifest. This is enforced by lint, not policy.
- **Provenance graph.** Every artifact (trace, motif observation, score, figure) carries an immutable record of the inputs and code versions that produced it. The graph is materialised in a content-addressed store. Re-running an artifact's recipe with the same inputs must produce a content-identical artifact in `strict` and `replayable_to_eps` worlds, or a distributionally indistinguishable one in `stochastic` worlds (with a documented test).
- **Code/container pinning.** All artifacts cite a git commit and a container digest. CI fails any commit that produces a trace whose declared determinism class is not actually achieved on the test corpus.

### 2.4 Compute orchestration

Time and compute are not the primary constraint, but waste *is*. The orchestration layer must:

- Deduplicate runs by content-addressed (world, parameters, seed, code) tuples.
- Cache intermediate trace fragments under content-addressed keys.
- Permit *partial* replays: re-run only the analysis plane against a fixed trace.
- Support both batch (sweeps) and interactive (zoo curation) workflows.
- Emit cost telemetry per (world family × motif detector × phase) cell.

The reference implementation targets local single-node, SLURM, and Kubernetes-Job back-ends behind a common interface. No scientific code may import the scheduler back-end directly.

### 2.5 Data residency and license boundaries

Biology data has licences. The architecture must enforce them.

- Every external dataset has a `license_class` enum: `cc0`, `cc-by`, `cc-by-nc`, `restricted`, `derived-only-publishable`.
- The Atlas plane refuses to render or export anything whose provenance graph leads back to a `restricted` source unless the export carries a license-compatible attribution bundle.
- Derived statistics and motif scores carry the *most restrictive* license in their provenance closure.
- Data with `restricted` class is held in a quarantine zone with separate access controls.

This is engineering, but it has scientific consequences: licence violations would tar credibility. It belongs in the architecture, not the operations runbook.

---

## 3. Module boundaries

For each module, v1.1 declares: responsibility, interface (in pseudo-Python, not committing to syntax), invariants, anti-responsibilities (things it must not do), telemetry obligations, and primary failure modes.

### 3.1 `core` — shared kernel

- **Responsibility.** Provide typed IDs, unit handling, deterministic RNG, provenance primitives, structured telemetry, conservation-invariant framework, run manifests, and typed errors.
- **Interface highlights.**
  - `RunID, TraceID, MotifID, EntityID, RunGroupID, EventID, BasinID, FormalLensID, MotifObservationID` — opaque, cryptographically random, typed.
  - `with_provenance(producer, inputs, code_ref) -> ProvenanceNode`.
  - `RNG.split(label: str) -> RNG` (counter-based, deterministic).
- **Invariants.** No global mutable state. No I/O. No randomness without an explicit RNG argument.
- **Anti-responsibilities.** Does not know what a world or motif is. Does not import any other module.
- **Telemetry.** Emits one event per RNG-split, per provenance write, per invariant breach.
- **Failure modes.** Any leakage of global RNG, any unit-mismatch passed as a plain `float`, any provenance write missing an input.

### 3.2 `trace` — the data plane

- **Responsibility.** Define `SystemTrace` schema versions; provide append-only writers; pull-based readers with column projection; on-disk persistence (Parquet/Zarr/HDF5); SBML import/export at the chemistry layer; integrity and conservation verification; schema migrations.
- **Interface highlights.**
  - `TraceWriter(manifest, schema_version) -> writer`; methods `append_state`, `append_event`, `append_lineage`, `append_invariant_check`, `close`.
  - `TraceReader(trace_id, projection: list[str], time_range, entity_filter) -> stream`.
  - `verify(trace_id) -> VerificationReport` (deterministic, conservation-checked, schema-valid).
- **Invariants.** Traces are append-only after writer close. Schema versions are immutable. Migrations are pure functions with explicit version pairs.
- **Anti-responsibilities.** Does not interpret trace content scientifically. Does not detect motifs.
- **Telemetry.** Per-write byte counts, per-read I/O, schema-version distribution, verification pass/fail rates per world family.
- **Failure modes.** Schema drift; partial writes producing torn traces; readers ignoring projection and dragging full state into memory.

### 3.3 `worlds.world_api` — the World contract

This contract is the most important interface in the project. v1.0 sketches it; v1.1 specifies it.

```
class World(Protocol):
    family: WorldFamily             # enum
    implementation_id: str          # e.g. "crn.feinberg.v3"
    implementation_version: SemVer
    determinism_class: DeterminismClass
    parameter_schema: ParameterSchema
    state_schema: StateSchema       # declares tensors, units, axes
    event_taxonomy: list[EventType]
    invariants: list[InvariantSpec] # mass, energy, count, custom

    def reset(self, seed: u64, params: Params) -> WorldState: ...
    def step(self, dt: SimDelta) -> StepReport: ...
    def observe(self, projection: ObservationSpec) -> Observation: ...
    def perturb(self, intervention: Intervention) -> PerturbationReceipt: ...
    def export_trace(self, writer: TraceWriter) -> None: ...
    def teardown(self) -> None: ...

    # Optional but encouraged:
    def fork(self, label: str) -> "World": ...
    def diff_state(self, other: "World") -> StateDiff: ...
```

- **Invariants.**
  - `reset` followed by N `step` calls is deterministic to the world's declared class.
  - `observe` is a pure function of internal state; it cannot mutate.
  - Every `step` call emits at least the events that *occurred* and nothing that did not.
  - `perturb` records its intervention with full provenance and may not bypass the event log.
  - `export_trace` produces a trace whose `verify` passes the world's declared invariants.
- **Anti-responsibilities.** A world must not contain detectors. A world must not read Atlas state. A world must not access biology data.

### 3.4 `worlds.<family>` — individual world engines

- **Responsibility.** Implement the World contract for one substrate. Provide world-internal calibration tests and synthetic ground-truth scenarios for §3.6.
- **Invariants.** Inherits the contract above. Additional family-specific invariants (e.g., for CRN: mass closure on declared elements; for fields: bounded total mass when conservation flag is set).
- **Anti-responsibilities.** Does not define motifs.

### 3.5 `search` — sampling and orchestration

- **Responsibility.** Choose what to run. Implements LHS, Sobol, random, novelty, quality-diversity (MAP-Elites), Bayesian optimisation, evolutionary search, adversarial perturbation, and curriculum schedules. Maintains coverage telemetry. Runs the scheduler.
- **Interface highlights.**
  - `Sampler.propose(state: SearchState) -> list[ProposedRun]`.
  - `coverage(state) -> CoverageReport` with named coverage metrics.
- **Invariants.** Search is a pure function of declared state plus its own RNG. Same state ⇒ same proposals (with the search's declared determinism class).
- **Anti-responsibilities.** Does not score motifs. Does not look at trace contents during proposal generation, except via summary statistics emitted by the analysis plane through declared interfaces.

### 3.6 `motifs` — the analysis plane (motif side)

- **Responsibility.** Maintain the motif grammar; the versioned motif registry; the detectors and their calibration; cross-detector triangulation; confidence calibration; AttractorStrength scoring; basin estimation.
- **Interface highlights.**
  - `Motif` is a typed object with a registry ID, grammar expression, prior, and a list of detector bindings.
  - `Detector.run(trace, scope) -> stream[MotifObservation]` with confidence and provenance.
  - `triangulate(observations) -> ConsensusObservation` with explicit conflict reporting.
- **Invariants.** Detectors are pure functions of their declared inputs. Detector outputs carry calibrated confidences (post-isotonic). Motif registry is append-only with semantic versioning; deletions become tombstones.
- **Anti-responsibilities.** Does not run worlds. Does not access biology data directly; it consumes `MotifObservation` records from the biology layer through a normalised interface.

### 3.7 `formalism` — the analysis plane (math side)

- **Responsibility.** Maintain the lens registry. Each lens implements `encode`, `decode`, `predict`, `compose`, and a set of invariance preservation tests. Compute the Formal Coverage Score per (motif × lens) pair and the deficit map.
- **Interface highlights.**
  - `FormalLens.encode(motif_evidence) -> Encoding | EncodingFailure`.
  - `FormalLens.decode(encoding) -> ReconstructedEvidence`.
  - `FormalLens.predict(encoding, holdout_query) -> PredictiveResult`.
  - `coverage_round_trip(motif, lens) -> CoverageScore`.
- **Invariants.** Lenses do not see motif IDs at encoding time; they see only the motif's evidence under a normalised representation, to prevent identity-based fitting. Encoding and decoding are pure.
- **Anti-responsibilities.** Lenses must not be modified to fit specific motifs they were tested against. Modification requires a registry version bump and rerun on adversarial controls.

### 3.8 `biology` — biology grounding

- **Responsibility.** Ingest external datasets with full provenance and licence metadata; standardise trait coding; produce phylogenetic correction inputs; produce sampling-bias correction inputs; emit `MotifObservation` records keyed by taxon, clade, and time interval, with explicit absence semantics.
- **Invariants.** No record without provenance. No record without an absence-status declaration. No phylogenetic claim without a tree-ID and a method-ID.
- **Anti-responsibilities.** Does not run nulls (those live in `nulls`). Does not score motifs (those live in `motifs.scoring`).

### 3.9 `nulls` — null-model factory

- **Responsibility.** Generate null distributions appropriate to each claim. Includes seed-shuffle, network-rewire (configuration model, edge-permutation, motif-preserving rewires), lineage-shuffle (preserving topology vs. branch-lengths separately), phylogenetic block bootstrap, and adversarial-world generators.
- **Interface highlights.**
  - `NullSpec` declares the property being preserved and the property being randomised.
  - `null_distribution(claim, n_samples) -> EmpiricalDistribution`.
- **Invariants.** Every null is named; every claim cites which null it is contesting; multiple-comparison correction is applied at the claim group level.

### 3.10 `validation` — gauntlet & preregistration

- **Responsibility.** Execute the §6 validation plan, manage preregistrations, render reports.
- **Invariants.** Preregistrations are content-addressed, versioned, and signed before the corresponding runs are scheduled. Post-hoc analyses are permitted but flagged in any report and never used to upgrade claim rungs.

### 3.11 `atlas` — atlas plane

- **Responsibility.** Render the curated periodic table; the zoo of replayable artifacts; the public dashboard; the paper figures pipeline.
- **Invariants.** The Atlas DB is a *curated* projection of the analysis plane and never the source of truth. Anything in the Atlas must be traceable back to a verified trace + a registered motif observation + a published preregistration (or marked as exploratory).

### 3.12 `ops` — operational tooling

- **Responsibility.** Containers, schedulers, secret management, human-audit interfaces, CI for determinism/schema/licence/lints.
- **Anti-responsibilities.** Carries no scientific logic.

---

## 4. Data and trace schemas

### 4.1 Design philosophy

The trace store is the project's most valuable asset. It must be:

- **Append-only.** Once a trace is closed, its bytes are immutable.
- **Content-addressed.** Trace identity = hash of contents + manifest, not a UUID.
- **Schema-versioned.** Every field has a schema version; readers handle ranges of versions.
- **Self-describing.** A trace contains its own schema reference, parameter schema, unit declarations, and determinism class.
- **Sparse-friendly.** Time series and event streams are stored sparsely where appropriate; readers project columns.
- **Conservation-checkable.** Energy, mass, and particle-count ledgers are first-class, not derived.

### 4.2 Schema version policy

Schema versions follow `major.minor.patch`:
- `patch`: documentation and constraint clarification, no field changes.
- `minor`: additive (new optional fields). Old readers keep working.
- `major`: breaking. Requires a migration. Old traces remain readable via the `trace.migrate` path.

`SystemTrace` enters service at v1.0. v1.1's specification of the schema is itself versioned alongside the project.

### 4.3 Top-level structure

```
SystemTrace = {
  manifest:          Manifest,
  axes:              Axes,
  parameter_record:  ParameterRecord,
  invariants:        list[InvariantSpec],
  state:             StateContainer,           # tensors keyed by axis
  events:            EventStream,              # typed records
  entities:          EntityRegistry,
  lineage:           LineageGraph,
  energy_ledger:     EnergyLedger,
  material_ledger:   MaterialLedger,
  boundaries:        BoundaryRegistry,
  perturbations:     PerturbationLog,
  measurements:      MeasurementSeries,        # derived during run
  detector_outputs:  DetectorOutputStream,     # optional, post-hoc allowed
  invariant_checks:  InvariantCheckSeries,
  audit_notes:       AuditNoteStream,
  signatures:        SignatureBlock            # cryptographic, on close
}
```

### 4.4 `Manifest`

```
Manifest = {
  trace_id:                  ContentHash,         # set at writer close
  schema_version:            SemVer,
  world_family:              enum WorldFamily,
  world_implementation_id:   str,
  world_implementation_ver:  SemVer,
  parent_traces:             list[ContentHash],   # for forks/restarts
  root_seed:                 u64,
  rng_algorithm:             enum {Philox4x32, Threefry4x64, …},
  rng_initial_state_hash:    bytes32,
  rng_final_state_hash:      bytes32,
  parameter_schema_id:       ContentHash,
  parameter_record_id:       ContentHash,
  determinism_class:         enum {strict, replayable_to_eps, stochastic},
  determinism_eps:           float | null,        # only if replayable_to_eps
  started_at:                ISO8601,
  completed_at:              ISO8601 | null,
  wall_seconds:              float,
  sim_seconds:               float,
  compute_node_class:        str,                 # not exact node, equiv class
  container_digest:          ContentHash,
  git_commit:                str,
  dependencies_lock_hash:    ContentHash,
  license_class:             enum LicenseClass,
  retention_class:           enum {ephemeral, indexed, archival},
  notes:                     str
}
```

### 4.5 `Axes` and `StateContainer`

`Axes` declares the simulation's time, space, species, energy, and information axes with explicit units and sampling policies.

```
Axes.time = {
  unit:               UnitExpr,                   # e.g. "s_sim"
  sampling_policy:    enum {fixed, adaptive, event_driven},
  dt_nominal:         float,
  jitter_policy:      enum {none, bounded, ssa},
  t0:                 float,
  irregular_index:    bool                        # true if event-driven
}

Axes.space = {
  topology:           enum {none, lattice2d, lattice3d, mesh, graph},
  dim:                int,
  extent:             tuple[float, …],
  units:              UnitExpr,
  boundary_conditions: enum {periodic, zero_flux, absorbing, mixed_decl}
}

Axes.species = {
  taxonomy:           ContentHash,                # species type taxonomy ref
  id_space:           enum {dense_int, uuid, string},
  cardinality_bound:  int | null
}

Axes.energy = {
  unit:               UnitExpr,
  accounting_mode:    enum {strict, declared, none},
  reference_state:    str
}

Axes.information = {
  unit:               UnitExpr,                   # bits or nats
  estimator_default:  str
}
```

`StateContainer` holds named tensors. Each tensor declares dtype, axes-of-variation, units, and missing-value semantics. Storage uses Zarr for tensor state (chunked, compressed) and Parquet for tabular streams.

### 4.6 `EventStream` and event taxonomy

Events are typed records with a common header and a discriminated payload. The taxonomy is intentionally rich and extensible.

Common header:
```
EventHeader = {
  event_id:        EventID,
  type:            EventType,
  t_sim:           float,
  t_wall:          ISO8601,
  source:          enum {world_step, perturbation, derived},
  causes:          list[EventID],   # optional but encouraged
  confidence:      float | null     # for derived events
}
```

Initial event taxonomy (extensible per world family):

| Type | Domains | Payload sketch |
|------|---------|----------------|
| `reaction_event` | chemistry | reaction_id, stoichiometry_delta, catalyst_set, energy_delta |
| `diffusion_event` | chemistry/fields | species_id, src_region, dst_region, amount |
| `flux_event` | fields | channel, src, dst, signed magnitude |
| `birth_event` | protocell, ecology, swarm | entity_id, parent_ids, location, kind |
| `death_event` | protocell, ecology, swarm | entity_id, cause |
| `division_event` | protocell, digital | parent_id, child_ids, fidelity |
| `fusion_event` | protocell | parents, child |
| `mutation_event` | digital, dev, eco | locus, before, after |
| `expression_event` | dev | gene_id, level, tissue |
| `movement_event` | swarm, eco, cog | entity_id, from, to |
| `communication_event` | swarm, cog | sender, receiver(s), channel, payload_hash |
| `boundary_event` | protocell, fields | boundary_id, kind, change |
| `repair_event` | protocell, dev, digital | target_id, mechanism, success |
| `perception_event` | cog | agent_id, sensor, signal, salience |
| `action_event` | cog, swarm | agent_id, action, params |
| `internal_state_event` | cog | agent_id, state_diff_hash |
| `niche_construction_event` | eco, swarm, cog | actor_id, environment_diff |
| `selection_event` | eco, digital | scope, fitness_proxy, survivors |
| `perturbation_event` | all | spec_id, target, magnitude, source |
| `detector_event` | all (post-hoc) | detector_id, motif_id, score, scope |
| `invariant_breach_event` | all | invariant_id, magnitude, recovered |
| `log_event` | all | level, code, message |

Each world family declares the subset of event types it can emit; the trace verifier rejects out-of-family events.

### 4.7 `LineageGraph`, ledgers, and registries

```
LineageGraph = directed acyclic graph with:
  nodes: EntityID
  edges: (parent: EntityID, child: EntityID, kind: enum {division, fusion, mutation, fork}, evidence: EventID)
  attributes: per-entity birth_event, death_event, lineage_label
```

```
EnergyLedger = time series indexed by region of:
  inflow:      float (in declared energy unit)
  outflow:     float
  dissipation: float
  stored:      float
  invariant_residual: float    # should be 0 within tolerance
```

```
MaterialLedger = per-(time, region, species):
  produced:    float
  consumed:    float
  imported:    float
  exported:    float
  in_storage:  float
  invariant_residual: float
```

```
BoundaryRegistry = list of:
  boundary_id:        BoundaryID
  declared_kind:      enum {none, passive, active, self_maintained, heritable}
  detection_provenance: ProvenanceRef        # null if declared by world
  geometry_ref:       SpaceRegionRef
  permeability_spec:  PermeabilitySpec
  birth_event:        EventID
  death_event:        EventID | null
```

```
EntityRegistry = id → {
  type, world_family, kind, birth_event, death_event,
  attribute_history_ref, lineage_label
}
```

### 4.8 Round-trip and information-loss tests

Substrate-neutrality requires that the *information needed for downstream analyses* can flow between worlds via the trace. v1.1 defines an explicit measurement of this property.

- For each pair of world families (W_i, W_j), define a *projection*: the set of motif-relevant features the analysis plane will request. The projection is declared in the analysis plane's interface.
- A trace from W_i is *projection-equivalent* to one from W_j if, after passing through the analysis plane's reader, the projected feature set is reconstructible to within a declared tolerance.
- The round-trip test runs synthetic seeds through the writer/reader pipeline and measures information loss against a ground-truth projection.

The trace passes if, for every projection in the registry, loss is below a published per-projection threshold. This test is one of the gating items between Phase 1 and Phase 2 (§12).

### 4.9 Storage format and physical layout

- Tabular streams (events, ledgers, lineage edges, invariant checks): Apache Parquet with per-row-group compression (zstd), column projection.
- Tensor state: Zarr v3 with sharded chunks.
- Manifest, schemas, registries: JSON Schema for human readability, with content-addressed copies in the provenance store.
- All artifacts pinned by content hash; on-disk paths are content-addressed (`/store/<hashprefix>/<hash>/...`).
- Optional HDF5 export for interop where required.

### 4.10 SBML and other interchange formats

- **SBML.** Required for the chemistry stack. The CRN/protocell worlds support SBML-L3-Core import for parameter records and simulation reports as exports.
- **NeXML and Newick.** Required for phylogenies.
- **Darwin Core.** Required for occurrence data ingestion (GBIF).
- **OBO / OWL.** Used for trait ontologies in the biology layer.

### 4.11 `MotifObservation` schema (consumed by atlas, validation, biology)

```
MotifObservation = {
  observation_id:        MotifObservationID,
  motif_id:              MotifID,                  # registered motif
  motif_registry_version: SemVer,
  scope:                 ObservationScope,         # trace + entity/region + time-range
  detector_id:           DetectorID | null,        # null for biology-side
  detector_version:      SemVer | null,
  triangulation_basis:   list[DetectorID],
  confidence:            float in [0,1],
  confidence_calibration: CalibrationRef,          # which calibration produced it
  evidence:              EvidenceBundle,           # structured, replayable
  absence_status:        enum {present, probably_present, unknown,
                               probably_absent, structurally_absent, n/a},
  null_contested:        list[NullSpecID],
  human_audit:           AuditRecord | null,
  provenance:            ProvenanceRef,
  notes:                 str
}
```

`absence_status` is a first-class field, not a flag derived from the absence of records. The biology layer is forbidden from ever defaulting absence to "absent".

---

## 5. Telemetry plan

The telemetry plane is separate from the data plane on purpose: telemetry must never influence a scientific result. Telemetry is for noticing that the instrument is behaving abnormally.

### 5.1 Five telemetry domains

1. **World telemetry.** Per-step wall time, memory, RNG draws, event volume by type, invariant residuals (energy and mass tolerances), determinism-drift estimators (for `replayable_to_eps`), warning counts.
2. **Pipeline telemetry.** Job submission, retry, dedup hits, queue waits, container start times, scheduler latencies, cache hit ratios.
3. **Detector telemetry.** Per-detector latency, per-trace coverage, ablation deltas, calibration drift since last refit, agreement matrix between detectors over the same scope.
4. **Audit telemetry.** Human-review queue depth, time-to-audit, audit override rates, inter-rater agreement when multiple humans review the same observation.
5. **Sampling/coverage telemetry.** Parameter-space coverage by sampler, novelty-score histories, basin-coverage estimates, regions starved of runs.

### 5.2 Conservation-law and invariant-breach telemetry

For each world family, a list of declared invariants is published with tolerances:

- Mass conservation per declared species set.
- Energy ledger residual.
- Particle count parity (for SSA worlds).
- Species-id integrity (no orphan references).
- Entity birth/death pairing.

Every step's per-invariant residual is sampled (not always written, to keep the trace small) and aggregated. Any breach above tolerance produces an `invariant_breach_event` and a tagged telemetry record. CI fails any change that increases breach rates above a baseline.

### 5.3 Determinism-breach telemetry

A subset of traces is run twice nightly under matched conditions to detect determinism drift. Mismatches at or below the declared epsilon are logged but do not fail; mismatches above epsilon trigger an alert.

### 5.4 Calibration-drift telemetry

Detectors are recalibrated periodically against the calibration corpus. The drift between successive calibrations is logged. When drift exceeds a threshold, the affected motif observations are flagged as needing reconfirmation and the registry version is bumped.

### 5.5 Coverage telemetry

The search layer publishes per-world-family coverage maps (binned over normalised parameter space). The atlas's claim "we have searched broadly" must be backed by a number, not an assertion.

### 5.6 Self-confirmation telemetry

A unique-to-this-project metric: **dictionary echo**. For each detector, measure correlation between detected motif rates and the *frequency of the detector's primitive vocabulary in trace event streams*. A high correlation indicates the detector is finding itself; this is reported to the audit layer.

### 5.7 Reporting

Telemetry feeds three dashboards:

- **Operations.** Job queues, failures, costs.
- **Method health.** Determinism, calibration, breaches.
- **Scientific health.** Coverage, dictionary-echo, audit agreement.

Method-health regressions block release of any artifact. Scientific-health regressions block claim upgrades.

---

## 6. Validation and falsification plan

### 6.1 Ten tests, made operational

v1.0's gauntlet (Tests 1–10) is correct in intent. v1.1 binds each to a measurable threshold, a null, and a stopping rule.

| Test | Operationalisation | Threshold (initial) | Null contested |
|------|--------------------|---------------------|----------------|
| T1 Recurrence | proportion of independent seeds (in matched parameter neighbourhood) producing the motif | ≥ 0.5 | seed-shuffle |
| T2 Basin width | normalised volume of parameter space with detection p > 0.5 | family-specific floor | random parameter null |
| T3 Perturbation recovery | proportion of perturbations recovered within τ_recover | ≥ 0.5 | shuffled perturbation pairings |
| T4 Implementation diversity | Shannon entropy across declared implementations | family-specific floor | implementation-blind null |
| T5 Cross-family transfer | number of world families with detection at confidence ≥ τ | ≥ 3 | family-permuted null |
| T6 Biological grounding | phylogenetically corrected occupancy of high-strength basin | family-specific floor | phylogenetic block bootstrap |
| T7 Null comparison | empirical p-value vs. matched null distribution | < α with FDR correction | hierarchy of nulls (§6.3) |
| T8 Prediction | out-of-sample improvement on pre-registered held-out set | pre-declared margin | best baseline model |
| T9 Compression | MDL gain from naming the motif | strictly positive | randomised motif labels |
| T10 Formal coverage | round-trip score (§9) | reported, not gated | n/a |

A motif that survives T1–T9 is a *candidate attractor*. T10 produces the formal-deficit profile that determines whether L5 or L6 are even in scope.

### 6.2 Calibration corpora as first-class artifacts

Detectors must be calibrated against worlds where the answer is known. v1.1 introduces three corpora:

- **Positive corpus.** Synthetic worlds engineered to contain a specific motif, with known instances. Detector must achieve recall above a threshold per motif.
- **Negative corpus.** Synthetic worlds engineered to *lack* the motif, sometimes with adversarial decoys (visually similar structure that fails an internal property, e.g., a passive container that looks like a self-maintained boundary). Detector must achieve high specificity.
- **Drift corpus.** Worlds parameterised across borderline cases to measure ROC curves and calibrate confidences.

Detector confidences must be well-calibrated; we report Expected Calibration Error and Brier scores by motif and by world family. Confidences are isotonic-regression-mapped to the calibration corpus before any downstream use.

### 6.3 Hierarchy of nulls

Every claim names which null it is contesting. The factory provides at least:

- **N0 — random parameter null.** Compares against random parameter draws, holding world family fixed.
- **N1 — seed-shuffle null.** Same parameters, randomised seed; tests whether the motif is parameter-driven or stochastic noise.
- **N2 — network-rewire null.** For network-bearing worlds (CRN, ecology, swarm communication graphs), randomises edges while preserving degree and other declared properties. Multiple variants (configuration model, edge-permutation, motif-preserving).
- **N3 — lineage-shuffle null.** Permutes lineage edges while preserving topology or branch-length statistics independently.
- **N4 — phylogenetic block bootstrap.** For biological claims, resamples in clades to preserve non-independence.
- **N5 — adversarial-world null.** Worlds explicitly engineered to look like the motif locally but lack the invariant globally.
- **N6 — detector-permutation null.** Randomises detector→trace assignment; tests for confounding by trace properties.

Multiple comparison correction: Benjamini–Hochberg FDR per claim group, with a published group definition. Family-wise correction for the L3/L4 flagship claims.

### 6.4 Pre-registration

For every flagship experiment and every claim that targets L3 or above:

- The hypothesis, the null, the test statistic, the threshold, the stopping rule, and the analysis path are committed to a content-addressed preregistration record before the corresponding runs are scheduled.
- The preregistration record lives in `papers/prereg/` and is signed.
- Any deviation from preregistration is reported with equal prominence as the headline result and prevents claim-upgrade.

### 6.5 Coverage estimators

To say "the basin width is X", we must know what we have not seen. Each sampler emits a coverage estimator (e.g., a kernel-density estimator over normalised parameter space, or a Good-Turing-style frequency-of-frequencies estimator on motif outcomes). Coverage estimates accompany every basin-width claim.

### 6.6 Adversarial controls and red-team protocol

A standing adversarial team (which can rotate) is responsible for designing:

- World configurations expected to *spuriously* produce motif detections (decoy worlds).
- Perturbations expected to break a "robust" motif.
- Detector ablations expected to swing scores significantly.

The red team's wins are reported in every release. A motif that has not been red-teamed cannot be promoted to the periodic table.

### 6.7 Stopping rules and negative-result protocol

A claim's runs may be stopped only by pre-registered conditions: hitting the sample-size cap, hitting a sequential-test boundary, or a method-health regression. Researchers may not stop a run because it "looks bad". Negative results are released with the same artifact bundle as positives: trace store, motif observations, scoring, registry version, container.

### 6.8 Cross-detector triangulation

A motif claim above L2 requires agreement among at least two structurally independent detectors (e.g., a graph-motif detector and a topological detector for the same boundary motif). Disagreements are not silently averaged; they are reported and routed to audit.

---

## 7. Simulation-world expansion

v1.0's eight worlds are good. v1.1 keeps all of them, makes their interfaces precise, adds five new worlds, and introduces a class of *calibration worlds*.

### 7.1 Refined specifications for v1.0 worlds

Each world declares: parameter schema (typed); invariants; declared event types; declared determinism class; calibration scenarios; reference benchmarks (if any); failure-mode tests.

For brevity, the parameter schemas, scenarios, and benchmarks are listed in §7.4 as a table. The point of v1.1 is that none of these are now optional.

### 7.2 New worlds

#### W9 — Origins-chemistry / mineral-surface world

- Motivation: pre-cellular catalytic surfaces (clay, FeS, mineral pores) are a frequent setting for origins hypotheses; restricting chemistry to fully-mixed soup misses surface-mediated motifs.
- Spec: 2D/3D mineral substrate with adsorption/desorption rates per species, surface-catalysis modifiers, pore connectivity graph, energy gradients across surfaces.
- Targeted motifs: surface-stabilised closure, transport-limited closure, gradient-anchored protocells.

#### W10 — Hypergraph reaction world

- Motivation: standard CRN edges connect species pairs; many biological reactions are inherently many-to-many. A first-class hypergraph representation may surface motifs that the bipartite Petri-net view obscures.
- Spec: reactions as hyperedges over species sets, with stoichiometric multiplicity. ODE and SSA back-ends.
- Targeted motifs: high-order catalytic closures, modular reaction blocks.

#### W11 — Quasispecies / sequence-space world

- Motivation: replication with mutation produces a cloud of variants whose collective properties differ from a clonal population. The error-threshold and sequence-space topology are first-order objects.
- Spec: replicator population over a sequence space with declared landscape, mutation operators, selection pressures, drift, and finite population.
- Targeted motifs: error-threshold collapse, neutral networks, evolvable robustness.

#### W12 — Symbiogenesis / endosymbiosis world

- Motivation: major-transition motifs (e.g., eukaryogenesis) involve nested individuality and identity transfer. No v1.0 world produces this naturally.
- Spec: protocells with internal sub-protocells; resource exchange contracts; conflict and alignment dynamics; horizontal and vertical inheritance.
- Targeted motifs: nested closure, identity-merge, division-of-labour-by-fusion.

#### W13 — Multi-scale composition world

- Motivation: real attractors compose. The Observatory must produce traces where the same motif occurs at two scales simultaneously (e.g., closure within a cell *and* closure within an ecosystem of those cells).
- Spec: coupled simulation of two world families with explicit upscaling/downscaling operators.
- Targeted motifs: cross-scale invariants, scale-bridging closures, emergent boundaries at coarse scales.

### 7.3 Calibration worlds

Calibration worlds are not scientific worlds. Their job is to provide ground truth.

- **K1 — Boundary calibration.** A field world with declared boundaries; some self-maintained, some passive, some heritable. Detector must distinguish.
- **K2 — Closure calibration.** CRN networks with hand-constructed RAFs of known size and depth, plus decoys.
- **K3 — Memory calibration.** Agent worlds where a known signal is or is not transmitted via environmental modification.
- **K4 — Adversarial calibration.** Worlds engineered to produce *false-positive*-prone surfaces (e.g., environmental cycles that look like internal closure).

Calibration worlds are part of CI. A change that lowers calibration scores blocks release.

### 7.4 World matrix

| ID | Name | Status | Determinism | Key invariants | Initial calibration |
|----|------|--------|-------------|----------------|---------------------|
| W1 | CRN | refined | strict | mass per element, count parity (SSA) | K2 |
| W2 | Protocell | refined | replayable_to_eps | mass, energy, boundary integrity | K1 |
| W3 | Field | refined | replayable_to_eps | mass (when conservative), boundary continuity | K1 |
| W4 | Morphogenesis | refined | replayable_to_eps | tissue mass, energy budget | K1 |
| W5 | Digital | refined | strict | computation budget, replication parity | K2 |
| W6 | Ecosystem | refined | stochastic | population non-negativity, conservation | — |
| W7 | Swarm | refined | stochastic | agent-count parity, communication budget | K3 |
| W8 | Cognitive | refined | stochastic | energy and attention budget | K3 |
| W9 | Origins-chemistry | new | stochastic | surface coverage, mass | K2 |
| W10 | Hypergraph reactions | new | strict (ODE) / stochastic (SSA) | mass, count parity | K2 |
| W11 | Quasispecies | new | stochastic | population size, sequence integrity | K2 |
| W12 | Symbiogenesis | new | stochastic | nested-mass conservation | K1 |
| W13 | Multi-scale composition | new | replayable_to_eps | per-scale mass/energy + cross-scale flux | K1, K3 |
| K1 | Boundary calibration | new | strict | declared ground truth | self |
| K2 | Closure calibration | new | strict | declared ground truth | self |
| K3 | Memory calibration | new | strict | declared ground truth | self |
| K4 | Adversarial calibration | new | strict | declared ground truth | self |

### 7.5 World-family completeness criteria

A world family is *Phase-1 complete* when:

1. It implements the World contract.
2. Its trace passes the round-trip test against at least one other family's projection.
3. Its calibration scenarios pass at the declared thresholds.
4. Its invariants are CI-tested.
5. It has at least one published preregistered experiment in the validation library.

### 7.6 Out-of-scope worlds (declared)

To prevent scope creep, v1.1 explicitly defers:

- Quantum-chemistry worlds (out of scope until L4).
- Astrophysical attractor worlds (deferred indefinitely; potential future "ALOE-cosmos").
- Economy / market worlds (deferred to a Phase 2+ companion project; scientifically interesting but introduces socio-political ambiguity).
- LLM-as-agent cognitive worlds (deferred until contamination risks for biology grounding are characterised).

---

## 8. Motif-detection improvements

### 8.1 Grammar with operational semantics

v1.0's motif grammar is a list of roles and relations. v1.1 adds composition, semantics, and a detector-binding layer.

Roles, relations, and operators form a typed graph algebra.

```
Role   ::= Source | Sink | Flow | Store | Boundary | Channel
        | Catalyst | Inhibitor | Template | Copy | Repair
        | Sensor | Actuator | Memory | Predictor | Selector
        | Reproducer | Cooperator | Parasite | Module | Controller

Relation ::= produces | consumes | contains | repairs | copies
           | routes | amplifies | dampens | selects | predicts
           | signals | competes_with | cooperates_with | bounds
           | depends_on | scales_to | composes_with | inherits_from

Op     ::= AND | OR | NOT | SEQ(A→B) | LOOP(A) | NESTED(A in B)
        | OVER_TIME(A, window) | UNDER_PERTURBATION(A, p)
        | PERSIST(A, τ) | RECOVER(A, τ_r)

Motif  ::= Role
        |  Relation(Motif, Motif)
        |  Op(Motif*)
```

Each motif has:
- a *grammar expression* (above);
- a *semantics function* mapping it to a predicate over trace fragments;
- a *prior probability* under each world family (estimated from K-corpora or declared);
- a *detector binding* to one or more concrete detectors;
- *invariance declarations*: which transformations of evidence preserve the motif (e.g., relabel-species, time-translate, region-translate).

The grammar's operational semantics is given by a reference interpreter that turns grammar expressions into evidence predicates over trace fragments. Detectors must agree with the reference interpreter on the calibration corpus.

### 8.2 Motif registry

The motif registry is a versioned ontology with semantic versioning and tombstones.

```
RegisteredMotif = {
  motif_id:        MotifID,
  name:            str,
  grammar:         GrammarExpression,
  semantics_ref:   str,
  invariances:     list[InvarianceDecl],
  detector_bindings: list[DetectorBinding],
  prior_by_family: dict[WorldFamily, float],
  status:          enum {draft, active, retired},
  introduced_in:   RegistryVersion,
  retired_in:      RegistryVersion | null,
  notes:           str
}
```

Adding, retiring, or modifying a motif bumps the registry's semantic version. Existing observations carry the registry version that produced them; comparisons across registry versions go through migrations.

### 8.3 Detector taxonomy

Detectors are typed by mechanism and by the evidence they consume.

| Detector class | Inputs | Output | Examples |
|----------------|--------|--------|----------|
| Rule-based | events, lineage, ledgers | structured evidence | RAF, cycle, branching |
| Topological | tensors, fields | persistence diagrams | spots/stripes/holes via persistent homology |
| Information-theoretic | event streams, state series | mutual information, transfer entropy | memory, prediction |
| Graph-motif | network snapshots | motif counts, configuration tests | feedback, modularity, bowtie |
| Statistical | aggregate features | hypothesis-test results | recurrence, robustness |
| Learned | normalised evidence | calibrated scores | trained on calibration corpora |
| Compositional | other detector outputs | meta-motif scores | nested closure, scale-bridging |

Every motif must be detectable by at least two structurally distinct classes for cross-detector triangulation.

### 8.4 Confidence calibration

Detector confidences are not raw scores. They are calibrated via isotonic regression against the calibration corpus, evaluated by Expected Calibration Error and Brier score, and re-fit on a fixed schedule with calibration-drift telemetry.

### 8.5 Detector ablation harness

Every detector pipeline supports systematic ablation: turning off each component, each feature, each sub-detector, and measuring the change in motif scores. Stable motifs survive ablation; unstable ones unmask their dependence on a single component (a red flag).

### 8.6 Scoring details

- **Recurrence (R)** is computed across a *parameter neighbourhood* defined by a kernel over normalised parameter space, not exact-match seeds. The neighbourhood definition is part of the scoring spec.
- **Basin width (B)** is computed via a stratified-sampling estimator with reported variance.
- **Cross-family transfer (X)** uses substrate-blind evidence: the motif is detected under a normalised representation that hides world family identity from the detector.
- **Implementation diversity (D)** is computed over declared implementation classes (e.g., for memory: pheromone-trail, environmental-feature, internal-state, externalised-symbol).

### 8.7 Defenses against self-confirmation

- Detector dictionaries are versioned; changes are logged and audited.
- Dictionary-echo telemetry (§5.6) is monitored.
- Adversarial worlds (§7.3, §6.6) generate worlds expected to *trigger* detectors falsely; triggering them at high rate fails the detector.
- Held-out world families: a fraction of world families and a fraction of seeds are reserved per release for confirmation, untouched by detector tuning.
- Audit overrides feed back into a confusion matrix that informs detector retraining schedules.

### 8.8 Audit interface

A motif observation is *auditable* if its evidence bundle is replayable: a human auditor can pull up the trace fragment, the detector's intermediate computations, the decoy comparisons, and the alternative hypotheses, and mark the observation as confirmed, rejected, or uncertain. Audit decisions are part of the provenance graph, never silently applied.

---

## 9. Mathematical / formalism layer improvements

### 9.1 Operationalising "formal coverage"

v1.0's "graph theory: partial; topology: partial; … missing" must become a number derived from a test. v1.1 defines formal coverage as a composite over three operations: encoding, decoding, and predicting.

Given a motif `M` and a lens `L`:

```
encode:   evidence(M)   → encoding ∈ L
decode:   encoding ∈ L  → reconstructed_evidence
predict:  encoding ∈ L  + holdout_query → predictive_result
```

The lens passes the test on `M` only if all three succeed for a representative sample of evidence.

### 9.2 Coverage components

```
CoverageScore(M, L) = w_e · EncodingScore   + w_d · ReconstructionScore
                    + w_p · PredictionScore + w_i · InvarianceScore
                    + w_c · CompressionScore
```

- **EncodingScore.** Fraction of evidence bundles that encode without information loss above ε.
- **ReconstructionScore.** Information loss between original and round-tripped evidence (using a normalised distance over the evidence representation, not raw bytes).
- **PredictionScore.** Out-of-sample accuracy on pre-registered held-out evidence relative to a baseline.
- **InvarianceScore.** Fraction of declared motif invariances preserved by the encode/decode pipeline.
- **CompressionScore.** Description-length ratio of the encoded representation to a baseline.

`CoverageScore` lives in [0, 1] after a published normalisation. Every component is reported individually; the composite is for ranking, not citation.

### 9.3 Lens registry

Each lens is implemented as a class implementing the `FormalLens` interface (§3.7). The initial lenses are listed in v1.0 §8 and inherited:

- graph theory, network science
- chemical reaction network theory
- dynamical systems
- stochastic processes
- information theory
- thermodynamics
- control theory
- topological data analysis
- category theory
- process algebra
- Petri nets
- game theory
- statistical mechanics
- computational mechanics

v1.1 adds:

- **rough paths / signature methods** (for irregular event-driven traces);
- **operad / coloured operads** (for compositional motifs);
- **stochastic thermodynamics / large-deviation theory** (for boundary and dissipative-structure motifs);
- **mean-field game theory** (for eco/swarm/cog motifs);
- **persistent sheaf cohomology** (for cross-scale motifs);
- **renormalisation-group / rough-grain operators** (for multi-scale composition).

Each lens declares its prerequisites (which motif evidence it can consume), its compositional rules (how lens-encodings of sub-motifs combine), and its invariance preservation profile.

### 9.4 Compositional and invariance tests

A lens passes the *compositionality* sub-test on motif `M = Op(M_1, M_2)` if `encode_L(M) = compose_L(encode_L(M_1), encode_L(M_2))` up to an isomorphism declared by the lens. Lenses that fail compositionality are still useful but cannot ground L6 claims involving compositional motifs.

A lens passes the *invariance* sub-test if encoding is equivariant with respect to the motif's declared invariances (e.g., species-relabel for a chemical motif; spatial translation for a field motif).

### 9.5 Predictive transfer test

For each lens that passes encoding/decoding, we ask: given an encoding from a held-out trace, can the lens predict an aspect of trace evolution (a future event, a perturbation response, a basin transition) better than a baseline that ignores the lens? Predictive transfer is the hardest of the lens tests and is required for L4-relevant claims.

### 9.6 The deficit map

For each motif × lens pair, a row in the deficit map records the five scores in §9.2 plus their individual confidences. The map is rendered as a heatmap and as a queryable table in the atlas.

A motif's *Formal Gap* is operationalised as `1 − max_L CoverageScore(M, L)`, weighted by AttractorStrength(M). The Missing-Math Candidate List is the set of motifs whose Gap exceeds a published threshold and whose AttractorStrength exceeds a published floor, reported with full uncertainty.

### 9.7 Path to candidate new formal objects

A candidate new formal object enters the registry only via:

1. A *failure mode in the deficit map.* Specifically, no existing lens achieves coverage above the published threshold across the motif's declared invariances.
2. A *proposal record* with: target invariants, mathematical sketch, operational definition, encode/decode/predict implementations.
3. Adversarial controls: the proposal is evaluated against motifs *outside* its target set; uniform improvement signals a flexible curve-fitter rather than a discovery (F5).
4. Independent reproduction: at least one external collaborator implements the proposal independently from the same operational definition, with matching coverage.

A candidate that passes the above is added as a lens, with its registry version, and the deficit map is recomputed.

### 9.8 Specific deficit motifs flagged as priors

Inheriting from v1.0 §14, the priors for missing-math are:

1. **Self-maintained boundary** (composite motif over closure + boundary + repair + identity-through-time).
2. **Closure rank** (a hierarchy of closure types, expected to be a well-typed object).
3. **Cross-substrate attractor equivalence** (functorial equivalence with substrate erasure).
4. **Adaptive identity through replacement** (a sheaf or stochastic-thermodynamic object).
5. **Externalised memory** (a niche-construction-aware information-theoretic object).

v1.1 commits to evaluating each of these against the lens registry by Phase 7 and to publishing the deficit profile regardless of outcome.

---

## 10. Biological grounding plan

### 10.1 Threats to validity (named)

- **Phylogenetic non-independence.** Species are not independent samples; closely related taxa share traits via inheritance. Ignoring this inflates apparent overlap with motif basins.
- **Fossil-record sampling bias.** Preservation bias (lithology, time, geography, body size, body composition).
- **Occurrence sampling bias.** GBIF and similar are heavily biased to urban areas, charismatic taxa, and certain regions.
- **Trait-coding heterogeneity.** Different ontologies code "flight" differently across studies.
- **Absence-as-zero.** Treating "not observed" as "absent" is the cardinal sin of this layer.
- **Look-elsewhere effect.** With many motifs and many clades, some overlap is guaranteed by chance.
- **Dataset version drift.** Phylogenies and taxonomies change; without pinning, results become irreproducible.
- **Definition drift.** "Eyes" or "memory" is ambiguous; a single study can move the apparent overlap merely by recoding.
- **Anthropic / publication bias.** Studied taxa are over-studied for cultural reasons.

Each threat has a corresponding mitigation that is a hard requirement, not a footnote.

### 10.2 Hard requirements

1. **Phylogenetic correction.** Every claim of motif–biology overlap uses phylogenetically corrected statistics (PIC, PGLS, or equivalents) when a tree is available. Block bootstraps over phylogenetic blocks are used for non-parametric tests.
2. **Sampling-bias models.** Every claim using PBDB or GBIF cites a bias model (e.g., subsampling, range-through, occurrence-density modelling) and reports results with and without correction.
3. **Trait-coding standards.** Each trait used has a versioned operational definition, ideally referencing an ontology (PATO, NBO, ENVO). Coding decisions are stored with provenance.
4. **Absence semantics.** Every observation declares an absence status; defaults are forbidden.
5. **Held-out clades.** A pre-registered fraction of clades is reserved per claim and used only for confirmation.
6. **Time-blind tests.** Where possible, the analysis is performed without access to taxon time-stamps and revealed only after.
7. **Dataset pinning.** Every external dataset version is content-hashed and pinned. GTDB releases, OTL synthetic-tree versions, PBDB query parameters, GBIF download keys, and NCBI accession lists are all stored.
8. **Look-elsewhere correction.** FDR per claim group; family-wise correction for L3/L4 flagships.
9. **Independent re-coding.** For a sampled subset of trait codings, an independent coder repeats the work; agreement statistics are reported.
10. **Negative space.** Predicted basins lacking biological examples are first-class outputs (not failures); they are explicitly enumerated and tested with adversarial sampling against literature.

### 10.3 Datasets and roles

| Dataset | Role | Licence class | Notes |
|---------|------|---------------|-------|
| Open Tree of Life | phylogeny scaffold | CC0 | pin synthesis version |
| Paleobiology Database | fossil time-ranges | CC-BY | pin query parameters; cite contributors |
| GBIF | occurrence and biogeography | CC-BY / CC0 mix per record | use download keys |
| NCBI Datasets | genomes, annotations | mostly public | pin accessions |
| GTDB | microbial taxonomy | CC-BY-SA | pin release |
| KEGG | metabolic pathway data | restricted (academic) | use only if licence permits redistribution; otherwise derived statistics only |
| MetaCyc / BRENDA | metabolism | restricted in places | as KEGG |
| Phenoscape / PATO / NBO / ENVO | trait/phenotype ontologies | CC variants | for trait coding |
| Tree of Sex, AnAge, EOL traits | trait sources | mixed | cite per-record |
| BAMM / RPANDA outputs | rate analyses | derived | reproducible from pinned trees |

The biology layer never *redistributes* restricted data; it derives statistics under licence-compatible terms and the Atlas refuses exports that would violate licence.

### 10.4 Mapping motifs to biology

Mapping is via `MotifObservation` records with explicit absence status and confidence. The mapping process is:

1. For each motif in the registry, declare an *evidence interface*: the kinds of biological evidence that support presence/absence.
2. Implement evidence loaders per dataset that produce candidate `MotifObservation` records with confidences derived from the evidence type.
3. Every record passes through a coding-spec verifier and is signed by a coder.
4. A subset is independently re-coded.
5. The mapping is versioned with the motif registry; mapping changes bump the version.

### 10.5 The biological test set

A specific list of biological cases anchors L3/L4 claims:

- Eye/photoreception convergence.
- Powered flight.
- Eusociality.
- Streamlined aquatic body plan.
- C4 photosynthesis.
- Carnivory in plants.
- Echolocation.
- Venom systems.
- Branching transport (vascular, tracheal, fungal).
- Segmentation.
- Externalised information (DNA, immune memory, niche construction, language).
- Major transitions: prokaryote→eukaryote, unicellular→multicellular, asocial→eusocial, individual→group, genome→language.

Each case has:
- a definitional spec;
- a clade-sample list;
- a held-out clade list;
- an absence-status convention;
- a primary motif-binding hypothesis;
- a null model.

### 10.6 Reporting conventions

- Every biological claim cites: dataset version, phylogeny version, trait coding spec version, motif registry version, null model, and preregistration ID.
- Negative results are reported with the same template as positive results.
- The biology layer publishes a quarterly *coverage and bias report* describing what is well-sampled, what is sparse, and where claims are necessarily weaker.

---

## 11. Risk register

The register is owned at the project level. Each risk has: ID, name, class, severity (1–5), likelihood (1–5), trigger (how we know), and mitigation. The most dangerous risks are R10 (self-confirmation) and R7 (definition drift); they are the ones that would turn the project into theatre.

### 11.1 Scientific & methodological risks

| ID | Name | Severity | Likelihood | Trigger | Mitigation |
|----|------|----------|------------|---------|-----------|
| R1 | Detector hallucination on unstructured noise | 5 | 4 | High motif rates on N1/N2 nulls; adversarial worlds trigger detectors | Calibration corpora; ablation harness; adversarial worlds; multi-detector triangulation; confidence calibration |
| R2 | Absence-as-zero in biology layer | 5 | 4 | Naïve bar charts of presence by clade in any artifact | Hard schema requirement for absence_status; CI lint; coder training |
| R3 | Phylogenetic non-independence ignored | 5 | 4 | Significant claims based on naïve clade-overlap statistics | Mandatory phylo-correction; block bootstraps; reviewer checklists |
| R4 | Sampling bias inflates patterns | 4 | 4 | Patterns track sampling effort more than biology | Bias models; subsampling; geography- and time-stratified analyses |
| R5 | Look-elsewhere effect | 4 | 4 | Many small p-values without correction | FDR per claim group; FWER for flagships; preregistration |
| R6 | Pre-registration drift | 4 | 3 | Headline claims deviate from preregistered analysis paths | Signed prereg records; deviations reported with equal prominence |
| R7 | Motif/trait definition drift | 5 | 5 | Motif scores change without registry version bump; coding inconsistency | Versioned registry; tombstones; independent re-coding; CI on definitions |
| R8 | Cross-substrate equivalence claimed without substrate-blind evidence | 5 | 3 | Claims of "same motif across worlds" without round-trip test | Mandatory substrate-blind detector mode; round-trip test gating |
| R9 | Formal coverage swung by lens taste | 4 | 4 | Coverage scores depend strongly on which lenses are in the registry | Multiple lens versions; lens-permutation null; adversarial new-object controls |
| R10 | Self-confirming pipeline | 5 | 5 | Dictionary-echo telemetry high; held-out worlds and clades show no effect | Held-out partitions; dictionary-echo monitoring; red team; adversarial worlds |
| R11 | Negative results suppressed | 4 | 3 | Imbalance between positive and negative result publications | Negative-result protocol; mandatory release with same artifact bundle |
| R12 | False mathematical originality (F5) | 4 | 3 | Proposed new objects raise coverage uniformly | Adversarial controls; independent reproduction; lens-permutation null |
| R13 | Anthropic biases in motif selection | 3 | 4 | Motifs reflect researcher culture | External motif submissions; periodic review by outside researchers |

### 11.2 Engineering risks

| ID | Name | Severity | Likelihood | Trigger | Mitigation |
|----|------|----------|------------|---------|-----------|
| R14 | Trace schema drift | 4 | 4 | Old traces unreadable; migrations not pure | Versioned schema; pure migrations; CI on round-trip |
| R15 | Determinism class violations | 4 | 3 | Bit-identical replays disagree | RNG discipline; nightly determinism tests; CI |
| R16 | Compute waste from non-deduped runs | 2 | 5 | Sweeps repeating identical runs | Content-addressed scheduling; cache hit telemetry |
| R17 | Detector calibration drift | 3 | 4 | ECE/Brier increases between releases | Calibration-drift telemetry; scheduled re-fits |
| R18 | License contamination | 5 | 2 | Restricted-source data leaks into Atlas exports | Licence-class enforcement at export boundaries; CI on provenance closures |
| R19 | Provenance gaps | 4 | 3 | Artifacts whose graph cannot be traversed back to inputs | Provenance writes via `with_provenance` only; CI on graph integrity |
| R20 | Storage cost explosion | 2 | 4 | Trace store growth swamps budget | Retention classes; sparse layouts; tiered storage |

### 11.3 Sociological & credibility risks

| ID | Name | Severity | Likelihood | Trigger | Mitigation |
|----|------|----------|------------|---------|-----------|
| R21 | Overclaiming "missing math" | 5 | 4 | Use of the phrase below L5 thresholds in any artifact | Linguistic discipline; review checklists; named falsifiers |
| R22 | Mysticism creep | 4 | 3 | Atlas language drifts toward "life is X" generalisations | House style guide; reviewer culture; explicit "what we are not claiming" sections |
| R23 | Single-team echo chamber | 4 | 3 | Lack of independent reproduction; closed development | External collaborators on motif submissions and lens proposals; reproducibility bundles |
| R24 | LLM contamination of biological reasoning | 4 | 4 | Use of LLM-derived trait codings without human audit | Audit policy; LLM use is allowed for tooling, not for evidence judgements without sign-off |

### 11.4 Standing review cadence

Each risk is reviewed at every phase boundary. Severity × likelihood scores are re-estimated. Mitigations are tested by red-team exercises at least once per phase.

---

## 12. Phased build roadmap

The phases are not time-sliced; they are *capability-sliced*. Each phase has explicit entry conditions, exit conditions, and the artifacts that must be in place before the next phase begins. Compute is not the bound; rigor is.

### Phase 0 — Foundations

- **Goal.** Lock contracts. No simulation runs in this phase.
- **Scope.** `core` module; trace schema v1.0; World contract; Manifest; provenance graph; telemetry plane; CI for determinism, schema, licence, and lints; calibration-corpus framework; preregistration tooling; risk register live.
- **Entry.** v1.1 spec accepted.
- **Exit.** All Phase-0 artifacts pass CI. The trace verifier runs on synthetic empty traces. A "hello-world" world (no science, just contract demonstration) ships.
- **Risk focus.** R7, R14, R15, R18, R19.

### Phase 1 — Chemistry primitives and trace plumbing

- **Goal.** First scientific traces exist; round-trip works; closure detector exists.
- **Scope.** W1 (CRN/RAF) at production quality; W10 (hypergraph reactions) in alpha; first calibration corpus K2; SBML import/export; closure detector; basic graph-motif detector; null factory N0/N1/N2; AttractorStrength scoring with R, P, B, I components only (X, D require multiple worlds).
- **Entry.** Phase 0 exit.
- **Exit.** A preregistered RAF/closure recurrence study runs end-to-end. Calibration scores meet thresholds. Round-trip test passes for the projection set declared.
- **Risk focus.** R1, R7, R10.

### Phase 2 — Boundary, protocell, and field worlds

- **Goal.** First closure-to-boundary transitions are detectable.
- **Scope.** W2 (protocell), W3 (field), W9 (origins-chemistry); K1 calibration corpus; boundary detector; topology-based detectors using GUDHI/Ripser-class tooling; expansion of the AttractorStrength score with X, D; flagship preregistration #1 (Closure-to-Boundary Transition).
- **Entry.** Phase 1 exit + boundary detector calibration > threshold.
- **Exit.** Flagship #1 published with full preregistration, full negative-space report, and ablation profile.
- **Risk focus.** R1, R3, R8, R10.

### Phase 3 — Morphogenesis, digital organisms, quasispecies

- **Goal.** First strong cross-substrate transfer claims.
- **Scope.** W4, W5, W11; lineage detector; replication detector; mutation/repair detectors; addition of more lens registry entries (CRNT deficiency, dynamical-systems persistence theorems, info-theoretic predictive states).
- **Entry.** Phase 2 exit + at least two motifs survive cross-family transfer at threshold.
- **Exit.** A preregistered cross-family transfer experiment with at least four motifs passes triangulation across at least three world families.
- **Risk focus.** R8, R9, R10, R12.

### Phase 4 — Ecology, swarms, multi-scale composition

- **Goal.** Higher-level attractors; cross-scale composition.
- **Scope.** W6, W7, W12, W13; collective-memory and division-of-labour detectors; multi-scale composition operators; first sheaf-cohomology lens experiments.
- **Entry.** Phase 3 exit.
- **Exit.** At least one cross-scale motif survives the gauntlet.
- **Risk focus.** R8, R10, R12.

### Phase 5 — Cognitive

- **Goal.** Memory, prediction, anticipation as first-class motifs.
- **Scope.** W8 cognitive worlds; computational-mechanics ε-machine lens; mean-field-game lens; learned detectors with audit-mandated calibration.
- **Entry.** Phase 4 exit.
- **Exit.** At least one prediction/memory motif survives the gauntlet with biology-relevant analogues identified.
- **Risk focus.** R10, R24.

### Phase 6 — Biology grounding

- **Goal.** Earth's life history compared to the attractor map.
- **Scope.** Full biology layer (OTL, PBDB, GBIF, NCBI, GTDB, KEGG-derived stats); phylo correction; sampling-bias models; trait-coding pipeline; held-out clades; flagship preregistration #2 (Convergence as Basin Depth).
- **Entry.** Phase 5 exit.
- **Exit.** Flagship #2 published with full controls, including F1 falsifier outcome.
- **Risk focus.** R2, R3, R4, R5, R6, R7, R11.

### Phase 7 — Formal coverage and the deficit map

- **Goal.** Operational deficit map for all surviving motifs.
- **Scope.** Lens registry full coverage; coverage scoring; flagship preregistration #3 (Formal Deficit Map); first proposals for new formal objects (only if motivated).
- **Entry.** Phase 6 exit.
- **Exit.** Deficit map published. F4 falsifier outcome reported. If any L5 candidate is identified, pass to Phase 8 with adversarial controls; otherwise project enters sustaining mode.
- **Risk focus.** R9, R12, R21.

### Phase 8 — Atlas and public artifact

- **Goal.** A periodic table people can explore; reproducibility bundles for every claim.
- **Scope.** Atlas DB; periodic table interactive viewer; replay app; reproducibility bundles; documentation; published methods + theory papers; external-collaborator onboarding.
- **Entry.** Phase 7 exit.
- **Exit.** Atlas live; first-paper bundle reproducible from cold container start; at least one independent reproduction completed.
- **Risk focus.** R18, R21, R22, R23.

### Phase boundaries are gates

A phase exits only when all named artifacts are live, all named tests pass, and all named risks are within tolerance. There is no "we'll fix that later" between phases; deferrals are written to the spec or the phase does not exit.

---

## 13. Task-sizing guidance for Codex

Codex will implement many of these tasks. The handoff is mechanical only if the tasks themselves are well-formed.

### 13.1 Task atom format

Every Codex task is a *task atom* with the following fields, mandatory:

```
TaskAtom = {
  id:                  TaskID,
  title:               str,                # imperative, ≤80 chars
  size:                enum {XS, S, M, L, XL},
  module:              ModuleID,
  rationale:           str,                # why this task; what depends on it
  inputs:              list[ArtifactRef],  # specs, schemas, prior code
  preconditions:       list[Predicate],
  outputs:             list[ArtifactRef],  # files created/modified, contracts honoured
  acceptance_tests:    list[TestSpec],     # mechanical, runnable
  determinism_contract: DeterminismClass,
  invariants_to_test:  list[InvariantSpec],
  telemetry:           list[MetricEmit],
  red_flags:           list[str],          # anti-patterns Codex must avoid
  out_of_scope:        list[str],
  dependencies:        list[TaskID]
}
```

A task without acceptance tests is not a task; it's a wish. Acceptance tests must be runnable with a single command and must include at least one negative test (a property whose violation causes failure).

### 13.2 Size buckets

| Size | Wall-clock target | Code surface | Examples |
|------|-------------------|--------------|----------|
| XS | < 30 min | one function or schema field | "Add absence_status enum to MotifObservation"; "Lint rule: ban `random.random()`" |
| S | < 4 h | one module file | "Implement TraceWriter v1.0 API skeleton with append-only enforcement"; "Implement Philox RNG splitter with deterministic counter" |
| M | < 1 day | one module | "Implement closure detector v0 with calibration against K2"; "Implement provenance graph store with content-addressed nodes" |
| L | < 1 week | one subsystem | "Implement Phase-1 trace store end-to-end with verifier and round-trip test"; "Implement W2 (protocell) with all declared invariants and K1 calibration" |
| XL | > 1 week | cross-module | "Implement validation gauntlet runner with preregistration, null factory integration, and report renderer" |

XL tasks are decomposed into L tasks before assignment. Codex never sees an XL.

### 13.3 Decomposition heuristics

- **Schema before code.** Schema and contract tasks come first within a phase, even if the implementing tasks lag.
- **Test before implementation.** Acceptance tests are written first as part of the task atom; implementation tasks then satisfy them.
- **Invariants before features.** A world's invariants are implemented and tested before any non-trivial dynamics.
- **Calibration before science.** A detector's calibration scenario is implemented before the detector is used scientifically.
- **One module per task.** Tasks that span modules are decomposed.
- **Determinism first.** Determinism contract is part of the task; it cannot be added later.

### 13.4 Acceptance-test patterns

Every task includes at least one of each, where applicable:

- **Schema round-trip.** Object → bytes → object equals original.
- **Property test.** A randomised input passes a declared property (e.g., trace verifier always returns a verdict; never raises).
- **Negative test.** A pathological input fails in a *named* way.
- **Determinism test.** Two runs with the same seed produce results within the declared class.
- **Invariant test.** The declared invariants hold on the calibration scenario.
- **Performance bound.** A loose upper bound to catch accidental quadratic blow-ups.

### 13.5 Anti-patterns Codex must avoid

- Importing a global RNG (`random`, `numpy.random.RandomState` without explicit seed).
- Mutating a manifest after writer close.
- Conflating "absence" and "not observed".
- Using a magic number where the schema declares a unit.
- Writing a detector that consumes raw world state instead of normalised evidence.
- Promoting an exploratory finding into a claim without a preregistration link.
- Inferring a license from a dataset's accessibility ("it was on the web therefore CC0").
- Using a `time.time()` call where a deterministic clock is needed.
- Adding a new dependency without updating the lock-file hash.
- Skipping tests "to ship faster".

### 13.6 Codex output expectations

Every Codex output produces:

- A patch.
- Updated tests.
- Updated docs (in-module).
- A short rationale explaining how acceptance tests are met.
- A telemetry-emit declaration if applicable.

Codex outputs that lack any of the above are sent back for revision.

### 13.7 Sample task atoms (Phase 0–1)

```
[XS] Add absence_status enum to MotifObservation v1.0 schema
  inputs: §4.11
  acceptance_tests: schema round-trip; negative test rejecting null
  red_flags: defaulting absence_status

[S] Implement Philox-based RNG.split with named substreams
  inputs: §2.3
  acceptance_tests: determinism (1000 splits identical across runs);
                    counter monotonicity; rejection of unlabeled splits
  red_flags: use of OS entropy in the splitter

[S] Implement Manifest schema v1.0 and content-addressed hashing
  inputs: §4.4
  acceptance_tests: round-trip; hash stability under field-order permutation
  red_flags: include of mutable fields in hash

[M] Implement TraceWriter v1.0 with append-only and torn-write detection
  inputs: §4
  acceptance_tests: append-only enforcement; crash-during-write produces
                    an unverified trace not a corrupted one; verifier
                    detects torn writes; schema round-trip
  red_flags: out-of-band mutation; non-atomic close

[M] Implement W1 (CRN) ODE+SSA back-ends with mass-conservation invariant
  inputs: §3.4, §7.4
  acceptance_tests: K2 closure-calibration recall ≥ threshold;
                    SSA→ODE convergence in mean as N→∞;
                    mass conservation residual within tolerance;
                    determinism class strict for ODE, replayable_to_eps for SSA;
                    round-trip with TraceReader projection
  red_flags: use of global RNG; species-id collisions on perturbation

[L] Implement closure detector v0 with calibration against K2
  inputs: §8, §6.2
  acceptance_tests: recall ≥ threshold on K2 positives;
                    specificity ≥ threshold on K2 decoys;
                    calibration ECE ≤ threshold post-isotonic;
                    ablation profile matches expected;
                    detection invariance under species relabel
  red_flags: leakage of motif identity into detector; uncalibrated raw scores

[L] Implement preregistration manager with content-addressed records
  inputs: §6.4
  acceptance_tests: signed records; tamper detection; deviation report
                    surfaces non-preregistered analyses; integration with
                    validation gauntlet runner
  red_flags: mutable preregistration after first run scheduled
```

Phase 2+ task atoms follow the same template. The full task atom backlog is maintained in `papers/methods/tasks/` and is itself versioned.

---

## 14. Questions that must be resolved before code begins

These are the concrete decisions whose deferral would produce churn later. Each is owned, has a target resolution date relative to Phase 0, and has acceptable answers laid out where possible.

### 14.1 Conceptual

- **Q1. What exactly is "the same motif across substrates"?** Acceptable answers must include an operational equivalence test under substrate-blind evidence.
- **Q2. Which closure-rank ladder is canonical for v1.1?** v1.0 proposes C0–C8. v1.1 must commit to the rung definitions or acknowledge that the ladder is a research output, not an input.
- **Q3. What is the scope of "biology"?** Earth biology only? Synthetic biology? Origins regimes? The biology-grounding plan presumes Earth biology; this is a deliberate restriction and must be documented.
- **Q4. Are LLM-as-agent worlds in scope?** v1.1 defers; the question must be revisited at Phase 5 boundary.
- **Q5. What is the project's stance on the FEP and Markov-blanket frameworks?** v1.1 cites them as one detector among many; explicit non-load-bearing status.
- **Q6. Is the project explicitly committed to producing falsifications when warranted?** v1.1 says yes; this requires governance backing.

### 14.2 Methodological

- **Q7. What significance regime governs L3 claims?** v1.1 proposes α = 0.001 with FDR; needs ratification.
- **Q8. Which phylogenetic correction methods are first-class?** PIC, PGLS, BAMM-style rate methods, or a chosen subset?
- **Q9. Which sampling-bias models are first-class for PBDB and GBIF?** Subsampling (SQS), shareholder quorum, range-through, occupancy modelling?
- **Q10. What is the held-out-fraction policy?** Per claim, per phase?
- **Q11. What is the project's red-team budget and rotation?**
- **Q12. How are external collaborators credentialed for motif and lens submissions?**

### 14.3 Engineering

- **Q13. Which RNG family is canonical?** Philox or Threefry. v1.1 inclines to Philox4x32 for performance and to Threefry4x64 for cross-language stability; one must be picked.
- **Q14. Which on-disk store?** v1.1 proposes Zarr v3 + Parquet + JSON-Schema. Confirm or alternatives.
- **Q15. Which language for the substrate plane?** v1.1 inclines to Python with JAX where differentiability matters, plus Diffrax for ODEs and a thin Rust core for SSA hot paths if needed. Confirm.
- **Q16. Which container runtime and registry?**
- **Q17. Which scheduler back-ends are first-class?** Local + SLURM + K8s-Job, or a subset?
- **Q18. What is the storage retention policy per retention class?**
- **Q19. How is secret management handled for licensed datasets?**

### 14.4 Data and licensing

- **Q20. Which KEGG/MetaCyc derivative usage is licence-compatible?** Legal review needed before Phase 6.
- **Q21. What is the citation policy for derived datasets?** A standard `CITATION.cff` per dataset version is proposed.
- **Q22. Which trait ontologies are canonical?** PATO, NBO, ENVO and others — choose the priority set.
- **Q23. What is the data-release schedule?** Per phase or rolling?
- **Q24. Are reproducibility bundles required to include input data, or pinned hashes only?**

### 14.5 Governance

- **Q25. Who owns the motif registry?** A small named editorial board.
- **Q26. Who owns the lens registry?** Same or separate editorial board.
- **Q27. Who can sign preregistrations?** Project leads + per-claim PI.
- **Q28. What is the dispute-resolution process when red team and detector authors disagree?**
- **Q29. What is the project's authorship policy?** A contribution-typology (CRediT or similar) is proposed.
- **Q30. Is there a public-engagement policy?** v1.1 proposes that no public claim is made above L2 until the corresponding rung is passed in writing; needs ratification.

### 14.6 Open scientific questions to be tracked, not resolved

These are not blockers. They are recorded so they do not get conflated with decisions:

- **OSQ1.** Is "self-maintained boundary" a single motif, a family of motifs, or a regime in motif space?
- **OSQ2.** Is closure rank a totally ordered ladder or a partial order?
- **OSQ3.** Are externalised-memory motifs distinct from niche-construction motifs, or aspects of the same object?
- **OSQ4.** Is cross-substrate equivalence preserved by *the* trace projection, or only by motif-specific projections?
- **OSQ5.** Is there an attractor-strength inflation under increased simulation fidelity? (i.e., do motifs become "stronger" merely by simulating in more detail?)
- **OSQ6.** Does the periodic table have a notion of "between cells" — transitional motifs whose identity is regime-dependent?
- **OSQ7.** Is convergent evolution evidence of basin depth, evidence of constraint, or both, and can the Observatory distinguish?

---

## 15. Closing notes for the implementation handoff

Three things the Codex hand-off must internalise above all:

1. **The trace is the artifact.** Worlds come and go; detectors will be replaced; lenses will be rewritten. Traces, motif observations, and the provenance graph are the project's permanent record. Any decision that compromises them for short-term convenience compromises the project.

2. **Calibration is the floor, not the ceiling.** Calibration corpora and red-team adversarial worlds are the difference between an instrument and a Rorschach test. They are written first and protected forever.

3. **The phrase "missing math" is earned, not used.** It appears nowhere outside §1.4 above L5 thresholds, in any artifact bearing this project's name. The temptation to overclaim will be the project's most consistent enemy. Discipline here is what gives the project a shot at ever credibly using the phrase.

v1.1 is, in the end, the same ambition as v1.0 with the safety rails the ambition demands: the same north-star claim, the same world ensemble, the same closure-rank intuition, the same atlas. What it adds is the apparatus that lets the claim survive contact with reviewers who do not already love the idea.

That apparatus is what makes this an observatory rather than a planetarium.
