# Architecture

The Attractor Observatory is structured as four architectural planes plus two cross-cutting planes. The structural rule is that **information flows up only**: each higher plane reads from the plane below via declared interfaces, never directly into a lower plane's internals. This is what makes substrate-neutrality enforceable rather than promised.

---

## The four planes

```
┌──────────────────────────────────────────────────────────────────┐
│ ATLAS PLANE         (slow-changing, public-facing)               │
│   periodic table │ atlas DB │ replays │ negative-space registry  │
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

### Substrate plane

Thirteen simulated worlds plus calibration scaffolding plus a `hello-world` reference world that demonstrates the World contract end-to-end:

- **W1 CRN** — chemical reaction networks. ODE backend (Strang-split RK4 + DOPRI5 adaptive) and SSA backend (direct Gillespie with combinatorial propensity). Hordijk-Steel maximal-RAF and minimal-subRAF extraction with closure-depth measurement.
- **W2 Protocell** — internal CRN inside a particle membrane. Real growth, division, fusion, repair, mutation, lineage.
- **W3 Field** — reaction-diffusion solver. Configurable 2D and 3D grids; periodic / zero-flux / absorbing boundaries; sources and sinks; energy field with coupling. Five reaction families: Brusselator, Schnakenberg, FitzHugh-Nagumo, Gray-Scott, Cahn-Hilliard (real fourth-order biharmonic).
- **W4 Morphogenesis** — 8-rule sigmoid gene-regulatory network with morphogen field, type-pair adhesion matrix, mechanical constraints. Five benchmark regimes (linear sheet, branching tree, segmented body, radial form, layered organoid) all driven by morphogen schedules and bandpass GRN cascades, **not** by benchmark-conditional code paths (D14).
- **W5 Digital** — 28-opcode virtual machine, executable genomes, copy-loop replication via allocate/copy/divide, mutation operators (substitution / insertion / deletion / length cap), task evaluation (NAND / NOR / EQU), parasitism, environment shifts. Avida-class.
- **W6 Ecosystem** — multi-trophic interaction matrix, predator-prey, mutualism, parasitism, resource cycles, niches, migration, extinction.
- **W7 Swarm** — pheromone trails, communication budget, role differentiation, collective repair, stigmergy.
- **W8 Cognitive** — sensors with noise, predictive module updated online, memory with decay, attention budget allocation, energy budget.
- **W9 Origins-chemistry** — mineral pore network with adsorption / desorption, surface catalysis, gradient-anchored protocell formation.
- **W10 Hypergraph reactions** — first-class hyperedge representation; modular reaction blocks.
- **W11 Quasispecies** — finite-population sequence space, error-threshold experiments, neutral-network exploration.
- **W12 Symbiogenesis** — nested protocells with sub-CRNs, resource exchange channels, vertical and horizontal inheritance.
- **W13 Multi-scale composition** — hosts live W1 and W2 inner-world instances at the macro layer; real upscale and downscale operators with cross-scale flux ledger.

Plus calibration worlds **K1–K10** and adversarial corpora.

The **World contract** in `worlds/world_api.py` defines the minimum surface every world honours: `reset`, `step`, `observe`, `perturb`, `export_trace`, `teardown`. All worlds must declare `family`, `implementation_id`, `implementation_version`, `determinism_class`, and a list of declared `invariants`. Determinism class is one of `strict`, `replayable_to_eps`, or `stochastic` with declared epsilon.

### Data plane

The trace store is the project's permanent record. Every world exports into a content-addressed `SystemTrace` v1 with:

- **Manifest** — content hash, schema version, world implementation ID and version, root seed, RNG algorithm, determinism class, license class, retention class, container digest.
- **Axes** — time / space / species / energy / information with explicit units.
- **Parameter record** — content-hashed, immutable.
- **State** — per-time-sample tensors keyed by axis.
- **Events** — typed, with cause links and confidence where appropriate. Taxonomy includes reaction events, division events, mutation events, perturbation events, niche-construction events, etc.
- **Lineage graph** — directed acyclic for parent-child relations.
- **Energy and material ledgers** — per-region inflow / outflow / dissipation / stored, with invariant residuals.
- **Boundary registry** — declared kind (passive / active / self-maintained / heritable) with detection provenance.
- **Invariant checks** — per-step residuals against declared invariants with tolerances.
- **Mode tag** — `foundational` / `exploratory` / `claim-bearing` (inheritable downstream).
- **Signatures** — content hash signatures on close.

The trace store is append-only. Schema versions are immutable. Migrations are pure functions with explicit version pairs.

### Analysis plane

Two pipelines run side by side:

- **Hypothesis-driven motif pipeline** — registered motifs with declared grammar, semantics, detector bindings, invariances, prior estimates per world family. Registry is versioned with semantic versioning and tombstones; deletions become tombstones, not erasures.
- **Emergent candidate motif pipeline** — unsupervised / weakly supervised discovery producing `MotifCandidate` records that may be promoted to `RegisteredMotif` through a named pathway (raw → audited candidate → draft motif → active motif).

Detectors are typed by mechanism (rule-based, topological, information-theoretic, graph-motif, statistical, learned, compositional). Confidence is calibrated via isotonic regression against the calibration corpus; ECE and Brier scores reported; dictionary-echo telemetry monitored.

Cross-detector triangulation is required for L2+ claims: a motif claim must be agreed on by at least two structurally independent detectors, and disagreements are not silently averaged.

The lens registry holds formal-mathematics surfaces (graph theory, CRNT, dynamical systems, information theory, topology, control theory, Petri nets, statistical mechanics, computational mechanics). Each lens implements `encode`, `decode`, `predict`, `compose`, plus invariance preservation tests. Coverage scores are computed from round-trip tests, not from descriptive labels. Three lenses are operational; five are queued for Campaign 009.

The null factory provides matched-randomisation distributions: N0 random parameter, N1 seed-shuffle, N2 network-rewire (configuration model), N3 lineage-shuffle, N4 phylogenetic block bootstrap, N5 adversarial worlds, N6 detector-permutation, N7 lens-permutation. Multiple-comparison correction at the claim group level via Benjamini-Hochberg FDR.

### Atlas plane

Curated public-facing surface: atlas DB, motif observation index, replays, periodic table viewer (queued), negative-space registry (24+ entries from Campaigns 002–008). The Atlas is a curated *projection* of the Analysis plane and never the source of truth.

---

## Cross-cutting planes

### Provenance graph

Every artifact carries an immutable record of inputs and code versions that produced it:

- inputs (content-addressed)
- producer (model, version, container, git commit)
- mode tag (inherited downstream)
- license closure (most-restrictive license in the input set)
- registry versions consulted
- audit decisions

Mode tag inheritance is enforced at the provenance graph layer: any artifact derived from an exploratory artifact is itself exploratory until an explicit promotion record (`PromotionRecord`, signed) lifts it.

### Telemetry plane

Five telemetry domains feed three dashboards (operations / method-health / scientific-health) plus the AI builder ledger:

- **World telemetry** — per-step wall time, memory, RNG draws, event volume, invariant residuals, determinism-drift estimators.
- **Pipeline telemetry** — job submission, retry, dedup, queue waits, container starts, scheduler latencies, cache hit ratios.
- **Detector telemetry** — per-detector latency, calibration drift, cross-detector agreement, dictionary-echo correlation.
- **Audit telemetry** — review queue depth, audit override rates, inter-rater agreement.
- **AI builder telemetry** — per-task estimation/actual, scope deltas, initiative scores, underbuild scores, rework indices.

The Instrument Health Vector aggregates nine components (determinism, calibration, provenance, detector agreement, coverage, storage, claim hygiene, builder calibration, doctrine compliance) with a panic budget rule: if any component dips below threshold, claim promotion across the project pauses until it recovers.

---

## Three modes

Every artifact carries a `mode_tag`:

| Mode | Purpose | Doctrine |
|---|---|---|
| **Foundational** | substrate everyone depends on: schemas, contracts, determinism, provenance, conservation invariants | strictest gates; deferrals on data-plane invariants forbidden; doctrine governs implementation, not contract surface |
| **Exploratory** | discover, prototype, stress-test, invent, surface unknowns | label-only; no public claims; tagged at provenance level; full No Artificial Ceiling Doctrine applies |
| **Claim-Bearing** | publish, validate, upgrade rung level, release atlas entries | preregistration, calibration, nulls, provenance, determinism, bias correction, audit |

Mode promotion requires a signed `PromotionRecord`. Foundational → Exploratory promotions are not allowed (foundational artifacts are stricter, not looser). Exploratory → Claim-Bearing requires the validation gauntlet.

---

## Build campaigns

A Build Campaign is the unit of multi-task ambition. Codex sees campaigns and is encouraged to expand them; campaigns decompose into L-sized tasks for review and rollback. Each campaign carries minimum-success conditions, builder expansion authority, suggested stretch list, acceptance gates with numeric thresholds, and a definition-of-done. Each campaign has a `make_campaign_NNN.py` that regenerates its full report from cold.

Eight campaigns live in this repository (002 through 008 + 007's two sub-campaigns + 009 queued).

---

## The cardinal rules

1. **Information flows up only.** Atlas reads Analysis through Motif Registry. Analysis reads Data through trace store. Data reads Substrate via export. No layer above Data may read a world's internal state directly.
2. **The trace is the artifact.** Worlds, detectors, lenses come and go. The trace store, motif observation registry, provenance graph, and claim ledger are the project's permanent record.
3. **Doctrine governs work; not contracts.** Builders expand work freely under the No Artificial Ceiling Doctrine. Schema, registry, unit, determinism-class changes go through registry version bumps and Architect review.
4. **Calibration is the floor, not the ceiling.** Calibration corpora and red-team adversarial worlds protect the project from becoming a Rorschach test. They are written first and protected forever.
5. **Falsifiers are publishable.** A point-attractor verdict on a motif (D17), a null larger than the signal, a basin-width failure — these are real results that go in the published record.

The full v1.2 specification — including the AI Operating System, the Estimation Loop, the doctrine, the campaign roadmap, the risk register — is in `The Attractor Observatory v1.2.md`.
