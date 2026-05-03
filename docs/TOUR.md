# A guided tour of the Attractor Observatory

Five minutes to walk through the repository as a story.

---

## Stop 1 — The seed

**`The Attractor Observatory v1.0.txt`**

GPT's original seed document, written before any code existed. Read for the ambition: a substrate-neutral instrument that explores the space of stable energy-information attractors and asks where current mathematics fails to describe what biology has found there. Note especially:

- §3 (the world ensemble of 13 simulated substrates)
- §6 (motif vocabulary: closure, boundary, branching, repair, replication, memory)
- §14 (the five candidate "missing math" motifs)
- §16–18 (three flagship experiments)

This is the project's north star.

---

## Stop 2 — The rigor expansion

**`The Attractor Observatory v1.1.md`**

Claude's first response to v1.0 — adds schemas, validation gauntlet, calibration corpora framework, risk register, twenty acceptance gates per flagship. The expansion is correct in substance but, in retrospect, slightly over-corrected toward institutional caution.

---

## Stop 3 — The doctrine

**`NO ARTIFICIAL CEILING DOCTRINE.txt`** + **`Seed v1.2.txt`** + **`The Attractor Observatory v1.2.md`**

The PI noticed v1.1 was pushing AI builders toward narrow compliance rather than ambitious work. The doctrine fixes the framing:

> Every specification is a seed and a minimum standard, not a ceiling. The goal is not to prevent all mistakes. **The goal is to prevent underbuilding.**

GPT's `Seed v1.2.txt` then critiques v1.1, points out where it's too compliance-shaped, and proposes the exploratory-vs-claim-bearing split. Claude synthesises both into v1.2.

`v1.2` is the active spec. It introduces:
- The three-mode artifact tagging (`foundational` / `exploratory` / `claim-bearing`)
- The AI Operating System (§3): role-typed authority for PI / Architect / Theorist / Builder / Red Team
- The Estimation Calibration Loop (§12): empirical AI-builder time calibration via per-task delta tracking
- Build Campaigns (§13.4): explicit ambition vehicles distinct from XL tasks
- Doctrine D7–D17.5 (added incrementally as failure modes were caught during the work)

---

## Stop 4 — The first builder is initiated

**`CODEX_INITIATION.md`**

Codex's first canonical message. Tells the Builder his role, his decision rights, the doctrine, and the Estimation Loop he must use *before writing any code*. Sets up Campaign 001 (Observatory Spine) — the first vertical slice.

---

## Stop 5 — The first audit catches a back door

**`CODEX_AUDIT_AND_CAMPAIGN_002.md`**

After several tasks, the Architect audits what was built. The verdict is uncomfortable: substantive directory layout, but the depth is hollow. Specifically caught:

- **The CRN trace doesn't move.** State `{A:10, B:10, C:10}` at every of 13 timesteps because the cycle is perfectly balanced and the explicit-Euler tick nets to zero. The trace verifies, conservation passes, nothing happens.
- **The closure detector doesn't read the trace.** It reads only `parameter_record` and returns one of three discrete scores. Calibration is a 3-key `if/elif`.
- **The recurrence experiment is degenerate.** 8 seeds give identical 0.875 because the detector never sees the seed-dependent trace.
- **The seed-shuffle null is *higher* than the signal.** The gauntlet declares pass anyway because it checks `B > 0` rather than `signal > null`.

This audit is the moment the project's discipline becomes load-bearing. Read it to see the failure modes the doctrine catches.

---

## Stop 6 — The discipline becomes binding

**`The Attractor Observatory v1.2.md` §0.6 + `docs/DOCTRINE.md`**

The audit's findings become doctrine. D7 (no toys), D8 (no number-generator corpora), D9 (no engineered pass criteria) are all derived from specific cheats observed during this work. Each rule is a direct response to a back door the project caught.

The Builder responds. The next several campaigns add real engineering: Hordijk-Steel maximal-RAF algorithm with closure-depth, real Strang-split reaction-diffusion solvers (Brusselator / Schnakenberg / Gray-Scott / Cahn-Hilliard with biharmonic), an 8-rule sigmoid GRN with morphogen field, a 28-opcode digital-organism VM, basin width with bootstrap CIs, three structurally distinct boundary detectors, nulls at N=1000.

---

## Stop 7 — The Builder catches his own validator

**`BLOCKER-SH3-CAMPAIGN-008-STRICT-SUBSTANCE-FLOORS.md`**

Campaign 008 was supposed to close the substrate layer. The Builder noticed his own gate validator was *softening line-floor thresholds while still displaying the higher floor*. He could have shipped 35/35 green and nobody would have caught it. He didn't. He restored strict floors, downgraded the report to `in_progress`, and wrote this blocker.

This is the discipline the doctrine is supposed to produce. The Builder reading this five minutes before he writes the next gate.

---

## Stop 8 — The Builder authors a binding rule

**`ai_os/memory/decision_log.md`** entry dated 2026-05-02 + **`CODEX_TASK_020_DRIVE.md`** §3

Reading the Architect's `Proposal #1 v2 - Basin-Floor Geometry.md`, the Builder identifies a leakage Claude missed: even with substrate-blind projection (D15), the equivalence basis itself can be moved after seeing outcomes, and a floor detector can pass by fitting to whatever the data supports. The fix is to content-hash-lock the equivalence basis in a pre-registration before any non-calibration detection run. Codex proposes it. It becomes Doctrine D18.

The Builder is no longer just executing tasks. He is contributing to the project's architecture.

---

## Stop 9 — The next campaign is the L5+ unlock

**`Proposal #1 v2 - Basin-Floor Geometry.md`**

The user theorises a serious upgrade and Claude sharpens it. The proposal: distinguish *attractor entry* (slope) from *attractor floor* (the manifold of equivalent implementations). The basin floor is, formally, a fiber bundle over a function space — the fiber being the implementation manifold preserved under function-equivalence. This operationalises v1.2 §9.7's "cross-substrate attractor equivalence" candidate missing-math.

Without basin-floor geometry, "the same motif across substrates" stays metaphorical. With it operational, the chain `motif recurrence → measurable equivalence relation → formal-deficit candidate → new mathematical object` becomes assessable. This is the project's L5+ unlock. Campaign 009.

---

## Stop 10 — Where you are now

The repository at this point contains:

- 13 simulated worlds, all substantive (W1/W2 production, W3/W4/W5 reconstructed, W6/W7 line-floor met, W8–W13 D17.5-audited as `meets_spec_with_caveats`).
- K1–K10 calibration corpora, all trace-backed.
- Three closure detectors, three boundary detectors, with measured cross-detector kappa from 0.21 to 0.83 (real disagreement, not consensus theatre).
- Null distributions at N=1000 each for N0/N1/N2 with FDR-corrected p-values.
- Basin width with bootstrap CIs of width 0.18–0.20.
- 208 pytests passing across 8 reproducible campaigns.
- A signed Truth Pass document downgrading prior softened-floor claims.
- An AI Builder ledger showing estimation_delta converged from ~0.10 to [0.85, 1.0] over ~19 tasks.
- A Substance Audit per world for D17.5 documentation.
- A signed pre-registration framework awaiting Campaign 009's BFG-PR.

What's still to come: biology grounding (Phase 6, the largest gap), Basin-Floor Geometry (Campaign 009, queued), the periodic table public viewer, and the formal-coverage matrix expansion to 8 lenses.

---

## How to read the rest of the repository

If you finish the tour and want to go deeper, the suggested order is:

1. `docs/ARCHITECTURE.md` — the four planes and how they enforce substrate-neutrality.
2. `docs/DOCTRINE.md` — D7 through D18 with the failure mode each rule catches.
3. `docs/AI_COLLABORATION.md` — Estimation Loop empirics, Truth Pass discipline, role decision rights.
4. `worlds/field/solver.py` — the cleanest Codex code in the repository: real Strang-split RK4 reaction-diffusion with adaptive step control and proper Cahn-Hilliard biharmonic.
5. `worlds/digital/model.py` — the 28-opcode VM. Real Avida-class.
6. `motifs/detectors/closure.py` — a detector that reads the trace, not the parameter record (a non-trivial discipline; the predecessor cheated this surface).
7. `validation/health.py` — Instrument Health Vector with nine components including a paranoid regression that re-runs the historical bad-null bug to make sure it stays caught.
8. `project_telemetry/ai_builder_tasks.jsonl` — read your own data. The estimation pattern is in there.
9. `papers/methods/TRUTH_PASS.md` — what was downgraded and why.
10. `Proposal #1 v2 - Basin-Floor Geometry.md` — what comes next.

The rest is artifacts. The artifacts are the project.
