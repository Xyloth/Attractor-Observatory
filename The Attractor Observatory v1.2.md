# The Attractor Observatory — v1.2

*A synthesis of v1.0 (GPT seed), v1.1 (Claude rigor expansion), and Seed v1.2 (GPT critique), under the No Artificial Ceiling Doctrine, with the Codex Estimation Calibration Loop as canon.*

---

## 0. Preamble

### 0.1 Spec lineage and how to read this document

| Version | Authored by | Role | Hash policy |
|---------|-------------|------|-------------|
| v1.0 | GPT (seed) | the original ambition; sets north-star claim, world ensemble, atlas concept | content-addressed, immutable |
| v1.1 | Claude | rigor substrate: schemas, validation gauntlet, calibration corpora, risk register, task atoms | content-addressed, immutable |
| Seed v1.2 | GPT (critique) | sharpening pass: doctrine, exploratory mode, AI-builder telemetry, emergent motifs, biology shadow track | content-addressed, immutable |
| **v1.2** | Claude (this document) | synthesis: keep v1.1 rigor, install the doctrine, accept most Seed-v1.2 amendments, push back where the seed flattens distinctions that matter | content-addressed, this version |
| v1.3 (anticipated) | Codex | first build-reality correction; adjusts spec where contact with implementation reveals friction | content-addressed |

`spec/lineage.json` records the hash, parent hash, author model, and rationale of each version. `spec/CHANGELOG.md` carries a human-readable diff. Both are tamper-evident: any change without a hash bump is a violation.

When this document conflicts with an earlier version, **v1.2 wins**. When this document is silent, defer to v1.1 (rigor substrate). When v1.1 is silent, defer to v1.0 (ambition substrate).

### 0.2 The No Artificial Ceiling Doctrine — canonical text

This is the project's load-bearing operating principle for builders. Reproduced verbatim from `NO ARTIFICIAL CEILING DOCTRINE.txt` and elevated to canon:

> Every specification, task description, architecture note, and implementation request given to a coding model is a **seed and a minimum standard, not a ceiling**.
>
> Do not constrain the coder to the narrowest interpretation of the task. Do not ask for the smallest useful implementation unless explicitly required for compatibility or recovery. Do not over-prescribe structure, file boundaries, abstractions, or scope when the coder can reasonably infer, improve, or extend them.
>
> Assume the coding model is a capable research engineer with strong architectural judgment. Trust it to add worthwhile complexity, nuance, instrumentation, tests, and design improvements when those additions strengthen the project.
>
> The instruction pattern is:
>
> > "This is the minimum success condition. You are encouraged to exceed it where doing so increases rigor, extensibility, observability, correctness, or scientific value. Add complexity only when it earns its weight in code. Do not treat the task boundary as a creativity boundary."
>
> Creativity, experimentation, and ambitious implementation are encouraged, even when they require later review, refactor, or pruning.
>
> The goal is not to prevent all mistakes. **The goal is to prevent underbuilding.**
>
> We would rather review and refine an ambitious implementation than repeatedly receive safe, narrow, prematurely minimized work.
>
> **Seed, not ceiling. Minimum, not maximum. Trust the builder.**

The doctrine is binding on every coder-facing artifact in the repository. Every task atom, every code-review checklist, every CI message, and every README that addresses an AI builder must preserve it.

### 0.3 The doctrine's scope and limits (the part the seed didn't say out loud)

The doctrine governs **the work**. It does not govern **the contracts**.

- **Work** = implementation: code, tests, docs, instrumentation, dashboards, additional benchmarks, additional calibration scenarios, performance tooling, developer ergonomics, architectural cleanups, additional acceptance tests beyond those listed.
- **Contracts** = schemas, registries, determinism classes, units, conservation invariants, manifest fields, motif IDs, lens IDs, license classes, retention classes, claim status labels, the trace's on-disk encoding.

A builder following the doctrine on **work** is encouraged to expand and improve. A builder modifying **contracts** without a registry version bump and an audit record is violating the project, not living up to it. Ambition on contracts goes through a controlled channel — *propose* a contract change with rationale, evidence, and migration plan; the change is reviewed and either accepted (with a version bump) or deferred.

This distinction is what prevents "trust the builder" from collapsing into "the builder rewrote the schema mid-task and contaminated three weeks of traces." The doctrine is for the engine room; the contracts are the hull.

### 0.4 Three modes, not two

Seed v1.2 proposes a binary split between Exploratory and Claim-Bearing. v1.2 keeps that split but adds a third mode that the seed implicitly assumes without naming:

| Mode | Purpose | Gates | Doctrine applies as |
|------|---------|-------|---------------------|
| **Foundational** | substrate everyone depends on: schemas, contracts, determinism, provenance, units, conservation invariants | **strictest gates**; any breach contaminates downstream work; deferrals on data-plane invariants are not allowed | Doctrine still applies *to the implementation* of foundational artifacts (instrumentation, tests, docs); contract surface is fixed and changes only via registry bump |
| **Exploratory** | discover, prototype, stress-test, invent, overbuild, surface unknowns | label-only; no public claims; tagged `exploratory`; trace bytes welcome | Full doctrine — encourage scope expansion, ambitious extensions, additional calibration scenarios |
| **Claim-Bearing** | publish, validate, upgrade rung level, release atlas entries | preregistration, calibration, nulls, provenance, determinism, bias correction, audit | Doctrine applies to implementation craft (more tests, better instrumentation), but not to scope of claims (claims are scope-bounded by preregistration) |

Every artifact carries a `mode` tag, inherited downstream. A motif observation produced from an exploratory trace is exploratory; an exploratory motif observation cannot support a claim-bearing artifact. Promotion across modes is explicit and auditable (§4.6).

A foundational artifact is not "exploratory" even when first written; the contract is the contract from day one. The project simply chooses which contracts are foundational at any given phase, with the option to *promote* a contract from exploratory-helper to foundational once it has earned the gates.

### 0.5 Where v1.2 accepts Seed v1.2

I accept the substance of the following Seed-v1.2 amendments, often with refinements:

1. **No Artificial Ceiling Doctrine as top-level principle.** Adopted as §0.2. Binding.
2. **Exploratory vs Claim-Bearing modes.** Adopted, expanded into a three-mode system (§0.4).
3. **AI-builder telemetry is first-class.** Adopted, formalised into the Estimation Calibration Loop (§12) and the AI Operating System (§3).
4. **Research Memory Ledger.** Adopted (§4.4). Idea provenance is now as binding as artifact provenance.
5. **Two motif pipelines** (hypothesis-driven + emergent candidate). Adopted (§6). The emergent pipeline gets its own promotion path with named gates.
6. **Biology shadow track from Phase 0.** Adopted (§9.1), with a discipline rule: shadow artifacts cannot become claim-bearing without explicit promotion.
7. **Negative-space registry as first-class output.** Adopted (§8.3, §9.5). Predicted-but-empty basins, simulation-only attractors, biology-only motifs, math-only structures are first-class artifacts.
8. **AttractorStrength reported as vector first, scalar second; Pareto ranking.** Adopted (§7.1, §7.2). The vector is the canonical object; scalar projections are reporting conveniences, declared per claim context.
9. **Residual structure test for formal deficits.** Adopted (§7.5). After the best lens explains what it can, the residual must itself be examined for recurring structure before "missing math" is invoked.
10. **Expanded calibration corpora.** Adopted (§10.1) with K5–K10. The added cases (ambiguous, OOD, multi-scale, semantic-equivalence pairs, non-stationary) sharpen substrate-neutrality testing.
11. **Exploratory and Quarantined worlds rather than hard deferrals.** Adopted (§5.3). LLM-agent worlds, market worlds, etc., become exploratory or quarantined, not banned.
12. **Revised Codex task atoms with `minimum_success` and `builder_expansion_authority`.** Adopted (§14.2). Replaces the v1.1 "out-of-scope / red flags" framing with claim-safety invariants and review triggers.
13. **Campaign 001 — Observatory Spine as the first build.** Adopted (§13.3). The first build is a serious vertical slice, not a hello-world.
14. **Spec lineage and changelog.** Adopted (§0.1).
15. **Model-to-model debate logs and conflict resolution.** Adopted (§3.6). Debate logs are content-addressed and arbitrated by the human PI.
16. **Failure artifacts.** Adopted (§4.5) with a triage taxonomy (structural/informative/boundary).
17. **World usefulness scoring.** Adopted (§5.5). Worlds are scored on the contributions that justify their compute and storage.
18. **Claim ledger.** Adopted (§4.3). Every claim is an object with explicit evidence, nulls, falsifiers, and public-allowed status.

### 0.6 Where v1.2 pushes back on Seed v1.2

I accept the seed's spirit on every point, but flatten distinctions that matter would weaken the project. The following pushbacks are deliberate.

**P1 — XL tasks: pushback (partial).** Seed v1.2 reads "Codex never sees an XL" as a violation of the doctrine. It is not. The doctrine governs **scope of work within a task**; task atomicity is a separate concern about *reviewability and rollback*. v1.2's resolution: XL tasks become **Build Campaigns** — explicit, multi-task ambition vehicles with their own coordination structure (§13.4). Codex sees campaigns and is encouraged to expand them; campaigns are composed of L-sized tasks for review. Doctrine preserved (each task has expansion authority); reviewability preserved (each task atomic enough to revert). This is not capitulation to the seed; it is sharpening it.

**P2 — Phase 0 simulation runs: accept with refinement.** Seed v1.2 wants Phase 0 to allow exploratory simulation runs. Agreed. But foundational work (schemas, manifests, determinism contracts, provenance graph) must still pass strict gates before claim-bearing simulation begins. v1.2's resolution: Phase 0 has two tracks — Foundations (strictly gated) and Spine Demonstration (exploratory). Campaign 001 is the Spine Demonstration. Both must complete to leave Phase 0; Foundations gate claim-bearing readiness, Spine Demonstration gates "we know how to make all of this work end-to-end."

**P3 — "No 'fix it later' between phases": accept with carve-out.** Seed v1.2 wants logged deferrals throughout. Agreed for most things. Carve-out: data-plane invariants (trace schema, manifest, provenance, determinism, conservation) cannot be deferred — they contaminate every downstream artifact retroactively. v1.2's rule: deferrals are allowed and tracked, except where the deferral is to a foundational data-plane invariant, in which case the phase does not exit. This protects the trace as the project's permanent record.

**P4 — "Missing math" language: accept GPT's relaxation, with one tightening.** Seed v1.2 allows "missing math" as a hypothesis label in internal exploratory notes. Accepted. The tightening: every internal use must be prefixed `[speculative]` or `[hypothesis]` and must carry a one-line acknowledgement of which L5 criteria are not yet met. This makes leakage into draft public artifacts auditable. The rule "L5+ for any artifact bearing the project's identity" stays.

**P5 — Single InstrumentHealth aggregate: pushback.** Seed v1.2 proposes one aggregate "is the observatory itself behaving?" score. v1.2 rejects scalar aggregates here for the same reason it rejected the v1.0 product-form AttractorStrength: scalars hide the dimensions that matter. v1.2's resolution: **Instrument Health Vector** with a panic budget (§11.4). Each component (determinism, calibration, provenance, detector agreement, coverage, storage, claim hygiene) carries a threshold. If any component dips below threshold, the project pauses claim promotion until the component recovers. Scalar projections are for dashboards only; never for decisions.

**P6 — Failure artifacts: accept with triage taxonomy.** Seed v1.2 says "a failed detector is a training signal." Sometimes; sometimes it is a bug. v1.2's resolution: failures are typed (§4.5) — *structural* (deletable after lesson logged), *informative* (kept and studied), *boundary* (kept and used as adversarial fodder). Without typing, the failure store becomes garbage. With typing, it becomes a corpus.

**P7 — Doctrine scope: extend the seed.** Seed v1.2 stops short of saying which surfaces the doctrine governs. v1.2 names this explicitly (§0.3): the doctrine governs **work**, not **contracts**. This is not a rejection of the seed; it is the missing fence that prevents "trust the builder" from being read as "the builder rewrites the trace schema in a Tuesday afternoon refactor."

**P8 — Multi-objective AttractorStrength → Pareto: accept and structure.** Seed v1.2 proposes Pareto ranking. Adopted, with the addition that the Pareto front is computed over a **declared subset of components** that depends on claim context (§7.2). A motif's Pareto status under a "biology grounding" context differs from its status under a "formal deficit" context. The vector is canonical; Pareto is contextual.

**P9 — Exploratory worlds with a tag is good; quarantine needs structure.** Seed v1.2 allows quarantined worlds. Agreed. v1.2 adds: a quarantined world cannot share storage paths or detector ablation pipelines with claim-bearing worlds. Quarantine is enforced by the architecture, not just the policy (§5.3.4). LLM-agent worlds, in particular, must not feed motif observations into the registry until contamination tests pass.

**P10 — Estimation Calibration Loop is the heart of the AI Operating System.** Seed v1.2 lists `estimated_time` and `actual_time` as task-atom fields. v1.2 promotes the loop to a top-level section (§12) with a documented ledger format, calibration analysis, and feedback into priors. The user has named this the project's most important AI-collaboration mechanism; v1.2 treats it as such. The loop's *purpose* is doctrinal: to systematically disabuse builders of the overestimation bias that drives premature minimisation.

### 0.7 What v1.2 adds beyond either prior version

- **Three modes (Foundational / Exploratory / Claim-Bearing).** §0.4.
- **Explicit doctrine scope** (work vs. contracts). §0.3.
- **AI Operating System** with role-typed authority and decision rights. §3.
- **Estimation Calibration Loop** as a first-class section. §12.
- **Build Campaigns** as the framing for ambition vehicles, distinct from XL tasks. §13.4, §14.4.
- **Foundations vs. Spine Demonstration tracks in Phase 0.** §13.1.
- **Instrument Health Vector with panic budget.** §11.4.
- **Failure typology.** §4.5.
- **Substrate-erasure round-trip discipline** for cross-substrate motif claims. §6.6.
- **Calibration corpus K10 (non-stationary).** §10.1.

---

## 1. Research framing

### 1.1 The north-star claim, restated

Life is one observed trajectory through a larger space of stable energy-information attractors. The Observatory is the instrument that makes the rest of that space visible — and where it cannot be made visible by existing math, the residual is the project's most valuable output.

### 1.2 The claim ladder

Inheriting v1.1 §1.2 unchanged. L1 framework, L2 discovery, L3 grounding, L4 prediction, L5 formal deficit, L6 new formal object. Each rung carries an operational pass condition; rungs L5 and L6 are the only ones whose claims may use the phrase "missing math" in public artifacts.

### 1.3 Falsifiers

Inheriting v1.1 §1.3 unchanged. F1 (kills L3+), F2 (kills L2), F3 (kills L1), F4 (kills L5), F5 (kills L6). The project commits to publishing falsifications with the same prominence as confirmations.

### 1.4 Dignified failure modes

Beyond the falsifiers, v1.2 names three **dignified failure modes** — outcomes that would not falsify the project but would mark the limits of its useful claims:

- **D1 — Substrate-bound success.** Strong motifs and strong biology grounding within a restricted substrate set, but no successful cross-substrate transfer. The Observatory becomes a high-quality intra-substrate attractor map; the substrate-neutrality ambition is parked.
- **D2 — Descriptive but not predictive.** Strong recurrence and strong overlap with biology, but no out-of-sample predictive value. The atlas is a map of correlations; predictive use awaits future work.
- **D3 — Formal coverage saturated.** Existing math captures every high-strength motif under round-trip. No "missing math" candidate emerges. The project becomes a successful taxonomy; new formal objects await different motifs.

D1–D3 are publishable outcomes. None of them is failure; all of them are honest results worth releasing.

### 1.5 Adjacent fields and inheritance disclosure

Inheriting v1.1 §1.5 unchanged. The adjacency table is binding: every paper and code module declares which inheritance it activates so reviewers can assess whether the cited tradition's assumptions actually hold.

### 1.6 What the Observatory is not

Inheriting v1.1 §1.6, with one update: **LLM-as-agent cognitive worlds** are not out of scope; they are quarantined (§5.3.4). The seed was right that hard deferral is too strong.

---

## 2. Architecture

### 2.1 Architectural planes

Inheriting v1.1 §2.1 unchanged. Atlas / Analysis / Data / Substrate, with provenance and telemetry as orthogonal cross-cutting planes. Information flows up only.

### 2.2 Trace-first design (canon)

> The trace is the artifact.

Worlds will evolve. Detectors will be replaced. Lenses will mutate. The trace store, the motif observation registry, the claim ledger, and the provenance graph are the project's permanent record. Any decision that compromises them for short-term convenience compromises the project. This is non-negotiable.

### 2.3 Provenance graph

Inheriting v1.1 §2.3, with one extension. Every artifact carries:

- inputs (content-addressed)
- producer (model, version, container, git commit)
- mode tag (foundational | exploratory | claim-bearing)
- license closure (most-restrictive license in the input set)
- registry versions consulted
- audit decisions (if any)

The mode tag is **inheritable downstream**: any artifact derived from an exploratory artifact inherits the exploratory tag. Promotion across modes requires an explicit promotion record (§4.6), signed.

### 2.4 Artifact status labels

Every output carries a `claim_status`:

```
exploratory | candidate | validated | claim-bearing | published | deprecated | retired
```

Applied to: worlds, detectors, motifs, traces, scores, formal lenses, biology mappings, atlas entries, figures, papers, ledgers, dashboards.

The status drives downstream eligibility. An exploratory detector cannot produce a claim-bearing motif observation. A candidate motif cannot anchor an L3 claim. The atlas viewer renders status visibly.

### 2.5 Compute orchestration

Inheriting v1.1 §2.4. Content-addressed scheduling, deduplication, partial replay, and per-cell cost telemetry. Time and compute are not the primary constraint, but waste is.

### 2.6 License and residency boundaries

Inheriting v1.1 §2.5. The Atlas refuses to render or export anything whose provenance closure would violate licensing.

### 2.7 Component map (updated)

```
attractor-observatory/
├── core/                       # shared kernel
│   ├── ids.py
│   ├── units.py
│   ├── rng.py
│   ├── provenance.py
│   ├── telemetry.py
│   ├── invariants.py
│   ├── manifests.py
│   ├── status.py               # NEW: claim_status, mode tag enforcement
│   ├── doctrine.py             # NEW: seed-not-ceiling helpers, expansion-authority lints
│   └── errors.py
│
├── trace/                      # data plane
│   ├── schema/
│   ├── store/
│   ├── reader.py
│   ├── writer.py
│   ├── migrate.py
│   ├── verify.py
│   └── sbml_bridge.py
│
├── ai_os/                      # NEW: human-AI operating system
│   ├── roles.py                # role registry: PI, architect, theorist, builder, red-team
│   ├── debate_log.py           # content-addressed debate records
│   ├── decision_log.py         # arbitration outcomes
│   ├── estimation_loop.py      # estimation/actuals/calibration
│   ├── builder_telemetry.py    # AI builder events
│   └── memory/
│       ├── decision_log.md
│       ├── hypothesis_ledger.md
│       ├── rejected_ideas.md
│       ├── open_questions.md
│       ├── concept_glossary.md
│       ├── motif_candidate_journal.md
│       └── formal_gap_journal.md
│
├── worlds/                     # substrate plane
│   ├── world_api.py
│   ├── crn/
│   ├── raf/
│   ├── protocell/
│   ├── fields/
│   ├── morphogenesis/
│   ├── digital/
│   ├── ecosystem/
│   ├── swarm/
│   ├── cognitive/
│   ├── origins_chemistry/
│   ├── hypergraph_reactions/
│   ├── quasispecies/
│   ├── symbiogenesis/
│   ├── multi_scale/
│   ├── calibration/            # K1..K10
│   ├── exploratory/            # NEW: tagged-only worlds for stress and inspiration
│   └── quarantined/            # NEW: contained worlds with separate paths
│
├── search/
│   ├── samplers/
│   ├── adversarial/
│   ├── curriculum/
│   ├── novelty/
│   ├── quality_diversity/
│   ├── negative_space/         # NEW: target predicted-but-unseen basins
│   ├── scheduler.py
│   └── coverage.py
│
├── motifs/                     # analysis plane (motif side)
│   ├── grammar/
│   ├── registry/               # registered motifs (versioned)
│   ├── candidates/             # NEW: emergent candidate motifs
│   ├── promotion/              # NEW: candidate -> registered pathway
│   ├── detectors/
│   ├── triangulation.py
│   ├── confidence.py
│   ├── scoring.py
│   └── pareto.py               # NEW: per-context Pareto ranking
│
├── formalism/
│   ├── lenses/
│   ├── coverage.py
│   ├── residual.py             # NEW: residual structure test
│   ├── proposals/
│   └── deficit_map.py
│
├── biology/
│   ├── shadow/                 # NEW: biology shadow anchor set, Phase 0+
│   ├── sources/
│   ├── ingestion/
│   ├── trait_coding/
│   ├── observation_model/
│   ├── phylo_correction.py
│   ├── sampling_bias.py
│   └── mapping.py
│
├── nulls/
│   ├── seed_shuffle.py
│   ├── network_rewire.py
│   ├── lineage_shuffle.py
│   ├── phylogenetic_blocks.py
│   ├── adversarial_worlds.py
│   ├── lens_permutation.py     # NEW: address R9 in v1.1
│   └── multitest.py
│
├── validation/
│   ├── gauntlet.py
│   ├── prereg.py
│   ├── thresholds.py
│   ├── claim_ledger.py         # NEW: claim objects, evidence, falsifiers
│   ├── failure_store/          # NEW: typed failure artifacts
│   └── reports/
│
├── atlas/
│   ├── db.py
│   ├── embeddings.py
│   ├── visualization.py
│   ├── replay.py
│   ├── periodic_table/
│   ├── negative_space/         # NEW: empty basins, simulation-only attractors
│   └── status_viewer/          # NEW: claim-status-aware rendering
│
├── ops/
│   ├── containers/
│   ├── schedulers/
│   ├── audit/
│   ├── secrets/
│   └── ci/
│
└── papers/
    ├── figures/
    ├── tables/
    ├── methods/
    ├── prereg/
    └── lineage/                # NEW: spec lineage + changelog
```

---

## 3. Human-AI Operating System

This is the section v1.1 implied but did not name. The Observatory is a research program executed by a heterogeneous team of one human PI and several AI collaborators with different strengths. The collaboration itself needs an operating system.

### 3.1 Roles

| Role | Responsibility | Decision rights | Telemetry |
|------|----------------|------------------|-----------|
| **Human PI** | sets ambition envelope; final arbiter on disagreements; signs preregistrations and claim promotions; provides actuals for Estimation Loop | unconditional override; sole authority on claim promotion to public artifacts | calibration outcomes, override patterns |
| **Architect (Claude-class)** | structural design, contract review, cross-cutting concerns, schema design, risk register, validation plans | proposes contracts; gates schema PRs; flags doctrine drift | architecture-review records, constraint-vs-doctrine balance |
| **Theorist (GPT-class)** | research strategy, claim review, methodological pushback, biology grounding plans, formalism choice | proposes scientific directions; gates claim wording; reviews preregistrations | theory-review records, falsifier proposals |
| **Builder (Codex-class)** | implementation, testing, calibration runs, dashboards, instrumentation, builder telemetry generation | proposes implementations; expands within doctrine; commits work | estimation/actuals, scope deltas, expansion notes |
| **Red Team** | adversarial perturbation, decoy worlds, detector ablation campaigns, dictionary-echo audits; can be a rotating subset of any of the above plus external collaborators | proposes red-team scenarios; gates motif promotion to claim-bearing | red-team scoreboards, rejected-promotion records |
| **External Reviewers** | independent reproduction, motif/lens submissions, periodic audit | submit candidates and audits; cannot bypass project's own gates | reproduction outcomes, submission lineage |

Roles are not exclusive: a model may rotate. What matters is that **every action carries a role tag** and the role's authority is enforced by the architecture, not policy.

### 3.2 Decision-rights enforcement

A claim promotion that requires PI signature cannot be promoted without a signed record. A schema change that requires Architect review cannot be merged without an architecture review record. A motif promotion that requires Red Team sign-off cannot proceed without a red-team scoreboard entry. These are not best practices; they are CI rules.

### 3.3 Debate log

`ai_os/debate_log/` contains content-addressed records of substantive disagreements. Each record:

```
DebateRecord = {
  debate_id:        ContentHash,
  topic:            str,
  positions:        list[ {role, model, version, position, evidence} ],
  arbitration:      {arbiter_role, decision, rationale, signed_at},
  follow_ups:       list[TaskID],
  revisit_trigger:  RevisitTriggerSpec,
  spec_impact:      list[SpecChangeRef] | null,
}
```

Recording a debate is not optional once the topic crosses a threshold (e.g., affects a contract, changes a phase boundary, challenges a falsifier). Silent drift between models is the failure mode debate logs prevent.

### 3.4 Decision log

`ai_os/decision_log.md` is the human-readable index of arbitrated decisions, each linked back to a debate record. Decisions have:

- date
- arbiter
- decision text
- rationale
- spec-version impact
- revisit trigger

### 3.5 Research Memory Ledger

Idea provenance is as binding as artifact provenance. `ai_os/memory/` carries:

| File | Purpose |
|------|---------|
| `decision_log.md` | arbitrated decisions, indexed |
| `hypothesis_ledger.md` | live and retired hypotheses, with status, evidence, counter-evidence |
| `rejected_ideas.md` | ideas considered and rejected, with reason and revisit trigger |
| `open_questions.md` | tracked questions, owner, target resolution |
| `concept_glossary.md` | versioned definitions of project-specific terms |
| `motif_candidate_journal.md` | informal notes on emergent candidates before registry promotion |
| `formal_gap_journal.md` | informal notes on lens gaps before deficit-map entry |
| `model_calibration_report.md` | running summary of Estimation Loop outcomes |

Every entry carries: date, author/model, spec version, idea, why it matters, status, evidence, counterargument, next action, linked artifacts.

### 3.6 Conflict resolution

Disagreements between models follow a fixed protocol:

1. **Position recording.** Each model logs its position in the debate record with evidence.
2. **Evidence cross-walk.** A neutral model (typically the Architect or an external reviewer) summarises the points of agreement and disagreement.
3. **Pre-decision red-team.** The Red Team is invited to argue against the current leading position.
4. **PI arbitration.** If the disagreement crosses the threshold (contract, claim, phase, falsifier), the PI arbitrates with a signed decision.
5. **Revisit trigger.** Every decision records what new evidence would justify reopening it.

This is what prevents "two LLMs converged on a confident wrong answer because they trained on similar text" from being how the project's hardest decisions are made.

### 3.7 AI builder telemetry

Every builder task emits:

```
BuilderTaskRecord = {
  task_id, task_atom_hash,
  model_name, model_version, container_digest,
  spec_version_read,
  scope_score:           int 1..10,
  complexity_score:      int 1..10,
  estimated_minutes:     float,
  estimated_files:       int,
  estimated_tests:       int,
  actual_minutes:        float | null,    # filled by orchestrator
  actual_files:          int,
  actual_tests:          int,
  failure_count:         int,
  revision_count:        int,
  initiative_extensions: list[ExtensionDescription],
  acceptance_outcome:    enum,
  underbuild_score:      float | null,    # PI-assigned
  initiative_score:      float | null,    # PI-assigned
  rework_index:          float,
  notes:                 str,
}
```

Records are written to `project_telemetry/ai_builder_tasks.jsonl` (append-only). The Estimation Calibration Loop (§12) reads from this file.

---

## 4. Data plane

### 4.1 SystemTrace (v1.0 of the schema)

Inheriting v1.1 §4. The schema, manifest, axes, event taxonomy, ledgers, and registries are unchanged. v1.2 adds three top-level fields:

```
SystemTrace.mode_tag:         enum {foundational, exploratory, claim-bearing}
SystemTrace.campaign_id:      CampaignID | null
SystemTrace.lineage_pointer:  ContentHash         # spec version under which produced
```

`mode_tag` propagates to every downstream artifact. `campaign_id` lets a build campaign group its traces. `lineage_pointer` records which spec version was active.

### 4.2 MotifObservation

Inheriting v1.1 §4.11, with one addition:

```
MotifObservation.candidate_origin: MotifCandidateID | null
```

If the observation was produced via the emergent candidate pipeline (§6.2), it carries the candidate ID it was promoted from. Direct registered-motif detections leave it null.

### 4.3 Claim objects

Every claim is an object in the claim ledger. This prevents accidental overclaiming.

```
Claim = {
  claim_id:          ClaimID,
  text:              str,                       # the wording
  rung:              enum {L1, L2, L3, L4, L5, L6},
  status:            enum {drafted, preregistered, evidence-collected,
                            validated, claim-bearing, published, retracted},
  preregistration:   PreregID | null,
  evidence:          list[ArtifactRef],
  nulls_contested:   list[NullSpecID],
  supporting_traces: list[TraceID],
  supporting_motifs: list[MotifID],
  falsifiers:        list[FalsifierSpec],
  known_weaknesses:  list[str],
  public_allowed:    bool,                      # signed by PI
  signed_by:         list[Signature],
  spec_version:      ContentHash,
}
```

The atlas viewer never renders a claim without showing its rung and status.

### 4.4 Research Memory Ledger

Files listed in §3.5. The ledger is itself versioned (Markdown plus a JSON index for tooling).

### 4.5 Failure store and failure typology

Failures are first-class. They live in `validation/failure_store/`. Three types:

| Type | Definition | Disposition |
|------|------------|-------------|
| **Structural** | the failure is due to an implementation bug or contract drift; the lesson is local and corrigible | logged, lesson recorded in the relevant journal, artifact deletable after the lesson is committed |
| **Informative** | the failure reveals a property of the substrate or method that is worth keeping (e.g., a detector that hallucinates closure on environmental cycles) | kept; tagged with the regime that produces it; used as future calibration material |
| **Boundary** | the failure occurs at the edge of a method's competence and is consistent across runs (e.g., persistent homology missing a topology with a specific noise profile) | kept; surfaced in the methods documentation as a known boundary; informs lens proposals |

The failure store is part of the project's permanent record. Without typing, it would silt up; with typing, it becomes a corpus the Red Team can mine.

### 4.6 Mode promotion records

A promotion record is required to lift an artifact from one mode to another:

```
PromotionRecord = {
  artifact_ref:          ContentHash,
  from_mode:             Mode,
  to_mode:               Mode,
  evidence:              list[ArtifactRef],
  gates_passed:          list[GateID],
  signatories:           list[Signature],
  spec_version:          ContentHash,
  notes:                 str,
}
```

Foundational → Exploratory promotions are not allowed (foundational artifacts are stricter, not looser). Exploratory → Claim-Bearing requires the validation gauntlet (§10). Claim-Bearing → Foundational is allowed when a claim-bearing artifact has stabilised enough to anchor schemas (rare).

### 4.7 Storage formats

Inheriting v1.1 §4.9 unchanged. Zarr v3 + Parquet + JSON-Schema + content-addressed paths.

---

## 5. World ensemble

### 5.1 World classes

Worlds are typed by intent:

| Class | Purpose | Mode eligibility | Notes |
|-------|---------|------------------|-------|
| **Core** | claim-bearing science across rungs L2–L6 | exploratory or claim-bearing | passes Phase-1 completeness criteria (v1.1 §7.5) |
| **Calibration** | ground-truth scenarios for detectors and lenses | foundational | K1..K10 (§10.1) |
| **Exploratory** | stress-test schemas, generate candidate motifs, inspire new architecture | exploratory only | tagged at trace level; cannot anchor claims |
| **Quarantined** | substrate types with unresolved contamination concerns | quarantined; physical separation | cannot share storage paths or detector ablation pipelines with claim-bearing worlds |
| **Retired** | deprecated worlds kept for replay only | retired | read-only |

### 5.2 Core worlds

Inheriting v1.1 §7.4:

W1 CRN, W2 Protocell, W3 Field, W4 Morphogenesis, W5 Digital, W6 Ecosystem, W7 Swarm, W8 Cognitive, W9 Origins-chemistry, W10 Hypergraph reactions, W11 Quasispecies, W12 Symbiogenesis, W13 Multi-scale composition.

Each world declares: parameter schema, invariants, event types, determinism class, calibration scenarios, and a Phase-1 completeness checklist.

### 5.3 Exploratory and quarantined worlds

#### 5.3.1 Exploratory market/economy worlds

Permitted as exploratory. May surface motifs (e.g., institutional repair, externalised memory) that inform the registry. Cannot anchor claims about Earth biology without an explicit promotion record and red-team review.

#### 5.3.2 Exploratory astrophysical attractor worlds

Permitted as exploratory. Useful for stressing the cross-substrate transfer test. Anchored claims would be a separate project ("ALOE-cosmos").

#### 5.3.3 Exploratory cultural/social worlds

Permitted with explicit caution. The risk is anthropocentric motif inflation; the mitigation is heavy ablation discipline and red-team adversarial scenarios.

#### 5.3.4 Quarantined LLM-as-agent cognitive worlds

Quarantined. Architectural separation:

- separate storage namespace (`/quarantine/llm_agents/`)
- separate detector pipeline (cannot share the production motif registry)
- separate provenance subgraph (any artifact whose provenance touches quarantine is itself quarantined and cannot be promoted to claim-bearing without contamination tests)
- explicit unblocking required to submit observations to the registry

The contamination concerns are: (a) LLM agents may import biological vocabulary as priors; (b) trace events may carry LLM-generated narrative that biases motif detection; (c) motif observations risk circularity if the same kind of model that generated the events is later used to interpret them.

When and if these concerns are resolved by a red-team-approved test, quarantine can be lifted.

### 5.4 Calibration worlds

Listed in §10.1.

### 5.5 World usefulness scoring

Each world is scored periodically on:

| Component | Description |
|-----------|-------------|
| trace_quality | invariant breach rate, determinism stability, schema completeness |
| motif_yield | unique motif candidates per compute hour |
| calibration_value | calibration-corpus contributions per phase |
| cross_family_value | how often the world's motifs transfer to other families |
| biological_relevance | how often the world's motifs map to shadow-track or full biology |
| formal_lens_stress | how often the world's motifs surface lens-coverage failures |
| compute_cost | actual cost per useful artifact |
| failure_insight_value | informative/boundary failures generated |

The score is a vector. A world that scores low on every component for two consecutive phase reviews is a candidate for deprecation. The doctrine applies: ambition expansion is encouraged, but worlds must justify their compute budget over time.

---

## 6. Motif system

### 6.1 Two pipelines

v1.2 makes explicit a distinction v1.1 elided. The Observatory must support both:

- **Hypothesis-driven pipeline.** Registered motifs with declared grammar, semantics, detector bindings, and invariances. This is what v1.1 specified.
- **Emergent candidate pipeline.** Unsupervised or weakly supervised discovery, producing `MotifCandidate` records that may be promoted to registered motifs through a named pathway.

Both are first-class. The registry is for known things. The candidate pipeline is for discovery the registry would otherwise prevent.

### 6.2 Emergent candidate pipeline

Candidates are produced by:

- unsupervised clustering on substrate-blind evidence projections
- topological persistence on field traces and graph traces
- recurrence mining on event streams
- compression-gain mining (a candidate is interesting when naming it shrinks descriptions)
- novelty-search outputs from the search layer

```
MotifCandidate = {
  candidate_id:               MotifCandidateID,
  discovered_by:              DiscoveryMethodID,
  evidence_clusters:          list[EvidenceClusterRef],
  recurrence_profile:         RecurrenceProfile,
  worlds_present:             list[WorldFamily],
  possible_interpretations:   list[InterpretationSketch],
  nearest_registered_motifs:  list[ {motif_id, similarity_metric, score} ],
  novelty_score:              float,
  compression_gain:           float,
  human_notes:                list[NoteRef],
  promotion_status:           enum {raw, audited, draft_motif, active_motif, retired},
  promotion_history:          list[PromotionEvent],
}
```

### 6.3 Promotion pathway

Candidates do not become registered motifs by accident. The pathway is:

1. **raw** → **audited candidate.** Independent re-detection on held-out seeds; novelty above floor; compression gain above floor; not a duplicate of an existing motif under similarity test.
2. **audited candidate** → **draft registered motif.** Grammar expression authored; detector binding implemented; calibration scenarios designed; prior estimates declared. Architect review.
3. **draft registered motif** → **active registered motif.** Calibration scenarios pass; cross-detector triangulation passes; red-team scenarios pass; registry version bump. PI signature.

A candidate may be retired at any stage with a recorded reason. Retirement is not deletion; the candidate remains in the journal.

### 6.4 Detector calibration (inheriting and extending v1.1 §8)

Detectors are calibrated against K1..K10 corpora. Confidence outputs are isotonic-regression-mapped. ECE and Brier scores reported.

v1.2 adds: **dictionary echo budgets.** Every detector has a published ceiling on dictionary echo (the correlation between detection rates and the detector's primitive vocabulary appearing in trace events). Above the ceiling, the detector's claims are downgraded automatically (claim-bearing → candidate) until echo is reduced.

### 6.5 Cross-detector triangulation

Inheriting v1.1 §8. A motif claim above L2 requires agreement among at least two structurally independent detectors. Disagreements are reported and audited, never silently averaged.

### 6.6 Substrate-erasure round-trip discipline

Cross-substrate motif claims require a substrate-erasure round-trip:

1. Take an evidence bundle from world family A.
2. Project to a substrate-blind representation.
3. Detect via the registered motif's detector under the substrate-blind representation.
4. Compare detections to a parallel pipeline that retains substrate identity.

A claim of "the same motif" across families requires consistent detection under substrate erasure, not merely co-occurrence. This operationalises v1.1's "substrate-neutrality must be enforceable, not promised."

### 6.7 Ambiguity handling

Detectors must output well-calibrated confidence. The K5 ambiguous corpus measures ambiguity competence: detectors must place borderline cases in the [0.4, 0.6] confidence band, not bistabilise on noise.

---

## 7. Scoring

### 7.1 AttractorStrength as vector

Inheriting v1.1 §1.4. The vector components are:

R recurrence, P persistence, B basin width, X cross-family transfer, D implementation diversity, I detector-ablation invariance, C_pred predictive contribution, S_obs sampling sufficiency.

The vector is canonical. Scalar projections are reporting conveniences and must be declared per claim context.

### 7.2 Pareto ranking (per claim context)

For each claim context, a subset of components is declared as the "objective set." The Pareto front is computed over that subset.

Example contexts and subsets:

| Claim context | Pareto subset |
|---------------|---------------|
| Cross-substrate transfer claim | {X, D, I, S_obs} |
| Biological grounding claim | {R, P, B, biological-overlap-score} |
| Formal deficit candidate | {R, X, D, C_pred} (and high formal gap) |
| Predictive value claim | {C_pred, S_obs} |
| Robustness claim | {P, B, I} |

Pareto status (dominant / on-front / dominated) is a property of the claim context, not the motif alone. The atlas viewer renders Pareto status in context.

### 7.3 Formal coverage

Inheriting v1.1 §9 with one extension. Coverage components stay: encoding, reconstruction, prediction, invariance, compression. Lens registry stays. Compositionality and invariance sub-tests stay.

### 7.4 Compression discipline

Adopted from Seed v1.2: a lens does not get full credit if it succeeds only by encoding the whole trace. The compression component of CoverageScore is computed against a baseline that allows the lens to "store everything"; if the lens does only marginally better than the baseline, compression credit is near zero.

### 7.5 Residual structure test

Adopted from Seed v1.2 (§9 in seed). After the best existing lens explains what it can, the residual is itself examined:

- Does the residual contain recurring structure (recurrence above noise floor, across runs and across world families)?
- Does the residual respond systematically to perturbations?
- Does the residual carry information that the lens did not capture (mutual information above baseline)?

If yes → strengthens the formal-deficit case for that motif × lens pair. If no → the gap was likely bad lens implementation, not missing math.

### 7.6 Negative-space scoring

Predicted-but-empty basins are scored on:

- prediction strength (basin coordinates and stability prediction)
- search effort spent
- biological coverage of the corresponding region
- adversarial-search outcome (did targeted search find an example?)
- alternative explanation strength (sampling gap vs. physical impossibility vs. historical contingency)

A high-strength negative-space entry that survives adversarial search is a research output, not a failure.

---

## 8. Search and simulation

### 8.1 Sampling strategies

Inheriting v1.1 §11. Random, LHS, Sobol, novelty, quality-diversity (MAP-Elites), Bayesian optimisation, evolutionary search, adversarial perturbation, curriculum schedules.

### 8.2 Coverage telemetry

Per-world-family coverage maps (binned over normalised parameter space). Every basin-width claim is accompanied by a coverage estimate.

### 8.3 Negative-space mining

A first-class search mode. The negative-space miner targets:

- predicted basins where the search has not yet found an instance
- regions of motif space where biology has examples but simulation has none
- regions where simulation is rich but biology is sparse
- regions where one substrate has examples but another consistently does not

Mining produces structured `NegativeSpaceEntry` records (§9.5).

### 8.4 Perturbation campaigns

Inheriting v1.1 §6. Perturbations are systematic and pre-registered for claim-bearing work.

### 8.5 Coverage estimators

Inheriting v1.1 §6.5. Kernel density, Good-Turing-style, basin-coverage. Every claim about "we have searched broadly" cites a coverage number.

---

## 9. Biology grounding

### 9.1 Biology shadow track (Phase 0+)

Adopted from Seed v1.2. From Phase 0 onwards, the project maintains a tiny biological anchor set:

- photoreception
- powered flight
- branching transport
- eusociality
- segmentation
- autocatalytic metabolic closure
- externalised memory

Purpose: **schema pressure**. At every phase boundary the team asks:

- Can the trace/motif schema represent the anchor set without hacks?
- Does absence semantics handle the cases where biology has no examples?
- Can confidence representations capture the uncertainty of paleobiological evidence?
- Can formal lenses encode the relevant aspects?
- Can the atlas display the anchor set with proper status labels?

Shadow-track artifacts are tagged `mode: shadow` and inherit the tag; they cannot be promoted to claim-bearing without explicit promotion records and the gates of §10.

### 9.2 Full biology grounding (Phase 6)

Inheriting v1.1 §10. OTL, PBDB, GBIF, NCBI, GTDB, KEGG-derived statistics. Phylogenetic non-independence corrected. Sampling bias modelled. Held-out clades reserved. Trait coding standardised. Absence-as-zero forbidden at the schema level.

### 9.3 Bias corrections

Inheriting v1.1 §10.2 unchanged.

### 9.4 Held-out clades

Inheriting v1.1 §10.2. A pre-registered fraction of clades is reserved per claim. Adversarial cross-checking is used to confirm hold-out integrity.

### 9.5 Negative biological space

A registered output. Files:

```
atlas/negative_space/
  predicted_empty_basins.md
  simulation_only_attractors.md
  biology_only_motifs.md
  math_only_structures.md
  unexplained_absences.md
```

Each entry has structured fields:

```
NegativeSpaceEntry = {
  entry_id:               NegativeSpaceID,
  category:               enum {predicted_empty, sim_only, bio_only,
                                 math_only, unexplained_absence},
  coordinates:             MotifSpaceCoords,
  prediction_strength:     float,
  search_effort:           CoverageReport,
  biology_coverage:        BiologyCoverageReport,
  adversarial_outcome:     enum {confirmed_absent, found, inconclusive},
  candidate_explanations:  list[ExplanationRef],
  status:                  enum {open, retired, resolved},
}
```

Categories of unexplained absence (from Seed v1.2):

- sampling gap
- physical impossibility
- historical contingency
- bad simulator
- bad motif definition
- undiscovered life-form class

Each unexplained absence is research fuel.

---

## 10. Validation

### 10.1 Calibration corpora (K1–K10)

| ID | Name | Role |
|----|------|------|
| K1 | Boundary calibration | declared-truth boundaries, passive vs. active vs. self-maintained vs. heritable |
| K2 | Closure calibration | hand-constructed RAFs of known size and depth + decoys |
| K3 | Memory calibration | known-signal-via-environment vs. agent-internal |
| K4 | Adversarial calibration | engineered false-positive surfaces |
| K5 | Ambiguous / knife-edge | borderline cases where the correct answer is graded uncertainty; detectors must produce confidences in [0.4, 0.6], not bistabilise |
| K6 | Out-of-distribution | scenarios outside the training distribution of any learned detector; detectors must abstain or flag |
| K7 | Multi-scale | the same motif at two scales simultaneously; tests cross-scale composition operators |
| K8 | Same-process / different-appearance | structurally identical processes implemented in visibly different substrates; detectors must equate |
| K9 | Different-process / same-appearance | superficially similar surfaces with different underlying invariants; detectors must distinguish |
| K10 | Non-stationary | the answer changes over time; detectors must distinguish "motif present then absent" from calibration drift |

Calibration scores feed CI. A change that lowers any K-corpus score below threshold blocks merge.

### 10.2 Null hierarchy

Inheriting v1.1 §6.3. N0–N6. Every claim names the null it contests. v1.2 adds:

- **N7 — Lens-permutation null.** For formal coverage claims: the deficit map is recomputed with lenses randomly assigned to motifs to test whether the gap structure is a property of motifs or of the lens registry.

### 10.3 Pre-registration

Inheriting v1.1 §6.4. Content-addressed, signed, before runs scheduled.

### 10.4 Red-team protocol

Inheriting v1.1 §6.6, with two strengthenings:

- The red team has standing budget (compute and time) declared per phase.
- The red team's wins are reported in every release as a named section.

### 10.5 Stopping rules and negative-result protocol

Inheriting v1.1 §6.7. Stopping by preregistered conditions only. Negative results released with full bundle.

### 10.6 Cross-detector triangulation

Inheriting v1.1 §6.8.

---

## 11. Telemetry

### 11.1 Five domains (carried over from v1.1)

- World telemetry
- Pipeline telemetry
- Detector telemetry
- Audit telemetry
- Sampling/coverage telemetry

### 11.2 AI-builder telemetry

New top-level domain. Source records: `project_telemetry/ai_builder_tasks.jsonl` (§3.7).

Derived metrics:

```
estimation_delta      = actual_minutes / estimated_minutes
scope_delta           = actual_files_changed / estimated_files
underbuild_index      = human_requested_expansions_after_completion
initiative_index      = useful_unrequested_improvements / task_size
rework_index          = revisions_needed / task_size
calibration_drift     = rolling_mean(estimation_delta) − 1.0
```

Aggregations:

- per-model, per-task-class, per-phase
- per-builder-session
- per-spec-version

### 11.3 Method-health dashboard

Determinism, calibration, breaches, dictionary-echo, audit agreement, coverage, schema integrity. Method-health regressions block release of any artifact (inherited from v1.1).

### 11.4 Instrument Health Vector with panic budget

Replacing Seed v1.2's single aggregate. Components:

```
InstrumentHealthVector = {
  determinism_health,
  calibration_health,
  provenance_health,
  detector_agreement_health,
  coverage_health,
  storage_health,
  claim_hygiene_health,
  builder_calibration_health,    # NEW: derived from §11.2
  doctrine_compliance_health,    # NEW: derived from underbuild/initiative ratios
}
```

Each component carries a threshold and a rolling 7-day window. **Panic budget rule**: if any component dips below threshold, claim promotion across the project pauses until the component recovers. Scalar projections of the vector are for dashboards only; never for decisions.

### 11.5 Reporting cadence

Daily for engineering metrics. Weekly for scientific health. Per-phase for builder calibration and doctrine compliance.

---

## 12. The Estimation Calibration Loop (canonical)

This section is the project's central AI-collaboration mechanism. It is canon.

### 12.1 Why this exists

Current AI builders, including Claude, GPT-class models, and Codex-class models, systematically misestimate task duration and scope. The dominant bias is *overestimation* of time and *underestimation* of capability — a builder will quote 90 minutes for a task that completes in 12, or scope a task narrowly because the broader version "feels" too large. The mechanism by which this happens is anchoring on token count and plan complexity rather than on prior actuals.

The downstream effect is **systematic underbuilding**: builders pre-shrink their work, the doctrine is silently violated, and the project receives narrow, prematurely minimised implementations.

The Estimation Calibration Loop is the corrective. It does not punish bad estimates; it makes the bias visible and uses repeated exposure to reduce it.

### 12.2 The loop

```
[1] Builder reads task atom (treated as a seed, expanded by builder judgment).
[2] Builder commits scope_score (1..10) and complexity_score (1..10) given the
    expanded scope it intends to execute.
[3] Builder commits estimated_minutes and a brief rationale.
[4] Builder executes the task, including any expansions consistent with the
    No Artificial Ceiling Doctrine.
[5] Orchestrator (typically the human PI) provides actual_minutes upon completion.
[6] Builder computes estimation_delta = actual_minutes / estimated_minutes
    and records it.
[7] Builder reads the last N records (default N = 20) of similar task class
    before its next estimate, and adjusts its prior accordingly.
[8] Calibration trends are reported in the AI-builder telemetry dashboard
    and in `model_calibration_report.md`.
```

### 12.3 Task class taxonomy for calibration purposes

To keep N-record windows meaningful, tasks are bucketed:

| Class | Definition |
|-------|------------|
| schema | schema design or modification |
| contract | contract or API design |
| primitive_impl | single-function or single-class implementation |
| module_impl | module-level implementation |
| integration | integration across modules |
| detector | detector implementation or calibration |
| world | world implementation |
| test_suite | test scaffolding or expansion |
| docs | documentation (in-tree) |
| analysis | analysis pipeline implementation |
| tooling | dashboards, CLIs, dev ergonomics |

A builder reads the last N records *of its own model class* in the same task class.

### 12.4 The estimation record schema

Stored in `project_telemetry/ai_builder_tasks.jsonl`, one JSON object per line:

```
{
  "task_id":               TaskID,
  "task_atom_hash":        ContentHash,
  "task_class":            TaskClass,
  "model_name":            str,
  "model_version":         str,
  "spec_version":          ContentHash,
  "scope_score":           int,         // 1..10
  "complexity_score":      int,         // 1..10
  "estimated_minutes":     float,
  "estimated_files":       int,
  "estimated_tests":       int,
  "expansions_planned":    [ExpansionDescription],
  "actual_minutes":        float | null,    // filled by PI
  "actual_files":          int,
  "actual_tests":          int,
  "expansions_realised":   [ExpansionDescription],
  "estimation_delta":      float | null,
  "scope_delta":           float | null,
  "initiative_score":      float | null,
  "underbuild_score":      float | null,
  "rework_index":          float,
  "acceptance_outcome":    enum,
  "spec_versions_consulted": [ContentHash],
  "notes":                 str
}
```

### 12.5 Calibration analysis

`ai_os/estimation_loop.py` computes:

- per-model × per-task-class **systematic bias**: median(estimation_delta) over a rolling window.
- per-model × per-task-class **scope timidity**: median(scope_delta − 1.0) over a rolling window. Negative values indicate the builder reliably under-scopes.
- **calibration trajectory**: change in bias across spec versions.

A builder's prior, going into a new task, is the rolling median of estimation_delta in its class. If the rolling median is 0.4, the builder's next estimate should be roughly 40% of what its naïve estimate would have been — and, equivalently, the builder is authorised to expand scope until its expanded estimate matches a realistic time-on-task.

### 12.6 What the loop is for, doctrinally

The loop's purpose is to grow the builder's confidence in **scope-expansion decisions** under the No Artificial Ceiling Doctrine. It is not a productivity dashboard. It is not a punishment system. It is the mechanism by which the doctrine is actually delivered: instead of telling builders to "trust themselves more," the project shows them, through their own data, that they have been systematically wrong in the same direction, and gives them a corrected prior.

The expected outcome over time: builders pick larger task classes, expand more aggressively within them, and converge to estimation_delta near 1.0 with smaller variance.

### 12.7 Honest counter-bias

The loop must report when the builder is *under*estimating, not just *over*estimating. A model that has learned to "say 12 minutes when the truth is 12" is calibrated; a model that has learned to "say 1 minute because the loop rewards small numbers" is broken.

The loop is ungameable in proportion to the honesty of the actuals. The PI's role here is to provide actuals without flinching.

### 12.8 Doctrine integration

Every task atom (§14.2) carries fields the loop needs (`scope_score`, `complexity_score`, `estimated_minutes`, `estimated_files`, `estimated_tests`, `expansions_planned`). Every completed task writes a record. Every model reads its prior before its next estimate. The loop is not opt-in.

### 12.9 Edge cases

- **Failures.** A failed task records `actual_minutes` up to abort and `acceptance_outcome: failed`. Failures count toward calibration with full weight.
- **Revisions.** A task that is revised carries an incremented `revision_count` and the cumulative `actual_minutes`.
- **Scope expansion mid-task.** If the builder expands scope after starting (a legitimate doctrine move), the expansion is recorded and the estimate updated; both the original and the updated estimate enter the calibration record.
- **Cross-spec drift.** If the spec version changes mid-task, the task is forked and both halves are recorded.

### 12.10 The first 50 records

The first 50 records establish the project's calibration baseline. Until 50 records exist for a (model × task class) pair, the loop reports "calibration uncertain" and the builder is encouraged to be deliberately ambitious. After 50, the rolling window stabilises and calibration trajectories become meaningful.

---

## 13. Roadmap

### 13.1 Two roadmaps, not one

Following the three-mode split, the project runs two roadmaps in parallel:

- **Foundations roadmap**: gated, claim-bearing-readiness, cannot be skipped, deferral on data-plane invariants forbidden.
- **Spine demonstration roadmap**: campaign-driven, exploratory, demonstrates end-to-end working substrate from day one.

Both must complete to leave a phase. They are not redundant: foundations gate scientific credibility; spine demonstrations gate engineering reality.

### 13.2 Phase outline

| Phase | Foundations focus | Spine demonstration focus |
|-------|-------------------|---------------------------|
| 0 | core kernel; trace schema; manifest; provenance; telemetry plane; CI | Campaign 001 — Observatory Spine |
| 1 | calibration corpus K1–K4 framework; null factory N0–N2; preregistration | first preregistered chemistry/closure exploration |
| 2 | boundary detector calibration; topology pipeline; null factory expansion | flagship #1 — Closure-to-Boundary Transition |
| 3 | morphogenesis + digital + quasispecies world contracts; lens registry expansion | first cross-substrate transfer experiments |
| 4 | ecosystem + swarm + symbiogenesis + multi-scale contracts; sheaf-cohomology lens | first cross-scale motif experiments |
| 5 | cognitive world contracts; computational-mechanics + mean-field-game lenses | first prediction/memory motif experiments |
| 6 | full biology layer; phylogenetic correction; sampling-bias models; full hold-out | flagship #2 — Convergence as Basin Depth |
| 7 | full lens registry; coverage scoring; deficit map; new-formal-object proposals | flagship #3 — Formal Deficit Map |
| 8 | atlas; reproducibility bundles; external collaborator onboarding | first paper bundle reproducible from cold start |

### 13.3 Campaign 001 — Observatory Spine

Adopted from Seed v1.2 with refinement.

**Minimum success conditions:**

- project skeleton matching the §2.7 component map
- spec loader (reads `lineage.json` + `CHANGELOG.md`, surfaces active spec version)
- trace schema v1.0 implemented (manifest, axes, state, events, lineage, ledgers, registries, signatures)
- manifest schema with content-addressed hashing
- provenance graph primitives
- RNG discipline (Philox-based splitter; CI lint forbidding global RNG)
- telemetry sink (structured logs + metrics emit; AI-builder ledger)
- "hello-world" world (no science, demonstrates the World contract)
- CRN mini-world (W1 alpha) with mass-conservation invariant and SSA + ODE back-ends
- K2 closure-calibration seed (small-scale ground-truth scenarios)
- closure detector v0 with isotonic confidence calibration
- trace writer + reader + verifier (round-trip + integrity)
- task telemetry logger (estimation loop ledger)
- one command per:
  - reproducible CRN trace
  - trace verification
  - closure detection
  - MotifObservation emission
  - task telemetry record write

**Builder expansion authority:**

The Codex builder may add architecture, tests, dashboards, richer schemas, CLI tooling, developer docs, visualizations, additional calibration scenarios beyond K2-seed, or improved module boundaries — provided each expansion is:

- consistent with §0.2 (the doctrine);
- restricted to **work**, not **contracts**, unless an Architect review is requested;
- accompanied by an updated estimation record (§12.4);
- captured in `builder_notes` of the relevant task atoms.

Suggested stretch additions (none required, all welcomed if scope allows):

- second world (a scoped W3 field or W2 protocell) wired to the same trace
- second detector (a graph-motif detector) for triangulation experience
- atlas seed page for closure motif observations
- Atlas DB schema draft
- replay tooling for a recorded CRN trace
- container build with reproducibility bundle
- determinism nightly test scaffolding

**Definition of done (claim-status: spine demonstrated, foundations passing):**

- The minimum-success commands all run from a cold container start in CI.
- The trace verifier passes on the demonstration runs.
- Schema round-trip passes.
- Determinism class declared and confirmed for the CRN ODE back-end (`strict`) and SSA back-end (`replayable_to_eps`).
- At least one MotifObservation has been audited and signed.
- At least one estimation record has been written, actuals received, and the resulting calibration entry recorded.
- Spec lineage v1.2 is the active spec; debate logs and decision logs exist with at least their initial entries (the v1.0 → v1.1 → Seed v1.2 → v1.2 lineage).

This is the first vertebra. It is not a toy. It is a working observatory in miniature.

### 13.4 Build Campaigns

A Build Campaign is the v1.2 framing for what would otherwise be an XL task. Campaigns:

- name a coherent multi-task ambition vehicle (e.g., "Phase 2 Boundary Capability");
- declare the minimum-success conditions, builder expansion authority, and stretch list;
- decompose into L-sized tasks with dependencies;
- carry their own calibration record and review cadence;
- are first-class artifacts, not informal groupings.

The Codex builder sees campaigns. Within a campaign, tasks remain L-sized for review and rollback. The doctrine is preserved (each task has expansion authority); reviewability is preserved (each task is atomic). This is v1.2's resolution to the v1.1-vs-Seed-v1.2 disagreement on XL task assignments.

### 13.5 Phase exit criteria

A phase exits only when:

- all foundations artifacts pass their gates;
- the spine demonstration for that phase reaches its definition of done;
- all named risks for the phase are within tolerance;
- the relevant flagship preregistration (if any) has produced a published outcome;
- the Instrument Health Vector has no component below threshold.

Deferrals are allowed except on data-plane invariants. Each deferral is logged with severity, owner, and prevention-from-claims status until resolved.

---

## 14. Codex task doctrine

### 14.1 Principles

- **Seed, not ceiling.** The doctrine governs every task atom.
- **Minimum, not maximum.** The acceptance criteria are the floor, not the cap.
- **Work, not contracts.** Builders expand work freely; contract changes go through registry bumps and Architect review.
- **Estimation is part of the task.** Every task carries the calibration loop's metadata.

### 14.2 Task atom (v1.2 schema)

```
TaskAtom = {
  id:                          TaskID,
  title:                       str,                    # imperative, ≤80 chars
  ambition_class:              enum {foundation, expansion, exploratory, claim-bearing},
  module:                      ModuleID,
  campaign:                    CampaignID | null,
  rationale:                   str,
  inputs:                      list[ArtifactRef],

  minimum_success:             list[Predicate],
  builder_expansion_authority: list[str],              # explicitly invited extensions
  suggested_extensions:        list[str],              # optional, non-binding

  expected_outputs:            list[ArtifactRef],
  acceptance_tests:            list[TestSpec],
  optional_stretch_tests:      list[TestSpec],

  invariants_to_preserve:      list[InvariantSpec],    # the substrate of doctrine
  claim_safety_invariants:     list[InvariantSpec],    # what cannot be relaxed for ambition
  review_triggers:             list[str],              # events that call for review,
                                                        # not prohibitions

  determinism_contract:        DeterminismClass,
  telemetry_to_emit:           list[MetricEmit],

  scope_score:                 int 1..10,              # filled at task start
  complexity_score:            int 1..10,
  estimated_minutes:           float,
  estimated_files:             int,
  estimated_tests:             int,

  actual_minutes:              float | null,           # filled at completion by orchestrator
  actual_files:                int,
  actual_tests:                int,
  estimation_delta:            float | null,
  scope_delta:                 float | null,

  expansions_planned:          list[ExpansionDescription],
  expansions_realised:         list[ExpansionDescription],

  initiative_score:            float | null,
  underbuild_score:            float | null,
  rework_index:                float,

  builder_notes:               str,
  acceptance_outcome:          enum {pass, fail, partial, deferred},

  dependencies:                list[TaskID],
  spec_version:                ContentHash,
}
```

The fields `out_of_scope` and `red_flags` from v1.1 are removed in v1.2 and replaced by `claim_safety_invariants` and `review_triggers`. The framing change is deliberate: the v1.1 fields shrunk ambition by listing prohibitions; the v1.2 fields name what cannot be compromised (so ambition can be applied freely elsewhere) and what calls for review (so initiative is invited to surface itself).

### 14.3 Acceptance test patterns

Inheriting v1.1 §13.4 with one addition: every task atom in the foundational class includes a **schema-stability test** ensuring no contract field was changed without a registry bump.

### 14.4 Build Campaigns vs. tasks

A campaign is composed of tasks. The campaign carries its own minimum-success and expansion authority; tasks within it inherit the campaign's ambition class and contribute to its definition of done. Codex sees campaigns as a unit *and* as a graph of tasks.

### 14.5 What Codex must internalise

Three rules above all (carrying over from v1.1 §15 with v1.2 framing):

1. **The trace is the artifact.** Worlds, detectors, lenses come and go; the trace store, the motif observation registry, and the provenance graph are the project's permanent record. Doctrine governs how you build them, not whether they have contracts.

2. **Calibration is the floor.** Calibration corpora and red-team adversarial worlds protect the project from becoming a Rorschach test. They are written first and protected forever.

3. **"Missing math" is earned, not used.** The phrase appears in public artifacts only above L5 thresholds. Internal exploratory notes may use `[speculative]` prefixed labels; every appearance is auditable.

And one more, new in v1.2:

4. **Estimate, then expand.** Every task atom is a seed. Commit a scope and a time, then expand the work where ambition earns its weight — and let the calibration loop confirm, over time, that you have been systematically wrong in the same direction.

### 14.6 Anti-patterns Codex must avoid

Inheriting v1.1 §13.5, with v1.2 reframing:

- Importing a global RNG. Use `core.rng.RNG.split(label)`.
- Mutating a manifest after writer close.
- Conflating "absence" and "not observed" in any biology-adjacent code.
- Using a magic number where the schema declares a unit.
- Writing a detector that consumes raw world state instead of normalised evidence.
- Promoting an exploratory finding into a claim without a preregistration link.
- Inferring a license from a dataset's accessibility.
- Using `time.time()` where a deterministic clock is required.
- Adding a new dependency without updating the lock-file hash.
- **Treating a task atom as a ceiling.**
- **Skipping estimation/actuals reporting because it feels like overhead.**
- **Modifying contracts in the same patch as work.** Contract changes are their own task atoms.

---

## 15. Risk register

Inheriting v1.1 §11. Twenty-four risks across scientific/methodological, engineering, sociological/credibility classes. v1.2 adds three doctrine-related risks:

| ID | Name | Severity | Likelihood | Trigger | Mitigation |
|----|------|----------|------------|---------|-----------|
| R25 | Builder over-expansion contaminates contracts | 4 | 3 | unauthorised contract changes appear in work-class patches | Doctrine scope (§0.3) enforced by CI lint that flags contract-touching diffs in tasks not declared as contract tasks |
| R26 | Estimation loop weaponised against ambition | 3 | 3 | builder's rolling delta drives the model to under-scope to "look calibrated" | Honest actuals; loop reports both over- and under-estimation; PI flags "scope timidity" trends |
| R27 | Mode tag drift | 4 | 3 | exploratory artifacts silently used as evidence in claim-bearing artifacts | Mode tag inheritance enforced at the provenance graph layer; promotion records required and signed |

Severity × likelihood is reviewed at every phase boundary. Mitigations are red-teamed at least once per phase.

---

## 16. Open questions

Inheriting v1.1 §14, with the following resolutions and updates.

### 16.1 Resolved by v1.2

- **Q4.** LLM-as-agent worlds — *quarantined*, not banned (§5.3.4).
- **Q21.** Citation policy — `CITATION.cff` per dataset version, plus `papers/lineage/` for spec lineage.
- **Q29.** Authorship policy — CRediT-style typology, with model authorship recorded but humans accountable for claim wording.

### 16.2 Still open, raised in priority

- **Q13.** RNG family — Philox4x32 default, Threefry4x64 fallback for cross-language stability. Decision needed before Phase 0 exit.
- **Q14.** On-disk store — Zarr v3 + Parquet + JSON Schema as default (per v1.1). Confirm.
- **Q15.** Language for the substrate plane — Python primary, JAX where differentiability matters, Diffrax for ODEs, optional Rust core for SSA hot paths. Confirm.
- **Q25–Q27.** Registry and preregistration ownership — proposed: motif registry under Architect; lens registry under Theorist; preregistrations co-signed by PI + per-claim PI.
- **Q30.** Public-engagement policy — proposed: no public claim above L2 until the corresponding rung is passed in writing.

### 16.3 New questions raised by v1.2

- **Q31.** What is the rolling-window size N for the Estimation Loop?  Default proposed: 20. Must be tuned per task class once 50 records exist.
- **Q32.** How is the Instrument Health Vector "panic budget" tuned? Initial thresholds need defaults and a process for adjustment.
- **Q33.** Who sits on the Red Team? Standing rotation vs. ad-hoc, internal vs. external.
- **Q34.** What is the protocol for promoting exploratory worlds (W-exploratory) to core worlds?
- **Q35.** What is the contamination test for lifting LLM-agent quarantine?
- **Q36.** How are emergent motif candidates surfaced for human review without overwhelming the audit queue? Proposed: novelty + compression-gain priority, with a daily ceiling.

### 16.4 Open scientific questions (untouched)

OSQ1–OSQ7 from v1.1 §14.6 are carried over unchanged.

---

## 17. Immediate next actions

These are the first few steps after v1.2 is accepted as canon. They are themselves task atoms (§14.2) at the M/L size, all in the **foundational** ambition class, with the Estimation Loop active from the first record.

1. **Spec lineage commit.** Materialise `spec/lineage.json` and `spec/CHANGELOG.md`; content-address v1.0, v1.1, Seed v1.2, and v1.2; sign.
2. **Doctrine canonisation.** Place the No Artificial Ceiling Doctrine at the top of every coder-facing artifact template (task atom template, README, CONTRIBUTING).
3. **AI Operating System scaffold.** Create `ai_os/` skeleton: roles, debate log schema, decision log schema, estimation loop ledger, builder telemetry sink, memory ledger files.
4. **Estimation loop bootstrap.** Implement `ai_os/estimation_loop.py` with the record schema, ledger writer, calibration analysis, and prior reader. The very first task atom Codex writes records into the ledger.
5. **Trace schema v1.0 freeze.** Land the schema, manifest, axes, event taxonomy, ledgers, registries, signatures. CI for round-trip and integrity.
6. **Determinism RNG.** Implement Philox-based splitter. CI lint banning global RNG.
7. **Provenance graph store.** Content-addressed nodes, mode tag inheritance.
8. **Mode tag enforcement.** `core/status.py`. CI checks downstream artifact tag inheritance.
9. **Calibration corpus framework.** K1–K10 directory layout, scenario schema, harness for confidence calibration and ECE/Brier reporting.
10. **Campaign 001 — Observatory Spine.** Open the campaign with its task graph; assign first three tasks to Codex; let the Estimation Loop start collecting records.

---

## 18. Closing

v1.2 is the synthesis the project needed: it keeps the rigor that v1.1 added without the institutional caution that the seed correctly diagnosed as overcorrection. It installs the No Artificial Ceiling Doctrine where it belongs — at the top, governing implementation, but bounded by the contracts that make claim-bearing science possible. It accepts the bulk of GPT-5.5's amendments because they are correct. It pushes back where the seed's framing flattened distinctions that matter: XL tasks are real but become Build Campaigns; Phase 0 has both Foundations and Spine Demonstration; data-plane invariants cannot be deferred; "missing math" stays earned in public.

It also bakes in the mechanism the user asked for as canon: the **Estimation Calibration Loop**. The loop is how the doctrine actually delivers. Telling builders to "trust themselves" does not work; showing them, through their own data, that they have been systematically wrong in the same direction does. The loop is the project's permanent corrective for AI-builder timidity.

The v1.2 merge principle is what the seed proposed and what v1.2 affirms:

> Keep Claude's rigor.
> Add the builder doctrine.
> Separate exploratory freedom from claim-bearing discipline.
> Make the trace permanent.
> Make the AI-collaboration telemetry first-class.
> Create room for discoveries outside the registered grammar.
> Bake in the estimation loop so the doctrine is delivered, not preached.

That is the v1.2 the project should hand to Codex.

The first vertebra is Campaign 001. The first record is the first estimate. The first calibration entry will land before the first detector does.

Build it.
