# Waiting to be Published

*Living log of the project's potential publishable artifacts. Each entry tracks what's there now, what tier it's at, and what's needed to move it up. Updated as campaigns close and as scope narrows toward write-up.*

*Last update: 2026-05-05 (after TASK-CB-003 close).*

---

## Tier definitions

- **Preprint ready** — could go up to arXiv / Zenodo / bioRxiv this week. No further work required; minor framing only.
- **Workshop ready** — could be submitted to a niche peer-reviewed venue (ICLR/NeurIPS/ICML workshops, ALIFE workshop, FAccT workshop) with a focused write-up pass. Maybe one more campaign of polish.
- **Conference ready** — full conference paper at the corresponding tier (ICLR, NeurIPS, ALIFE main, ICML, FAccT main). Needs solid empirical core and one or two more campaigns of either expansion or rigor.
- **Journal ready** — full journal paper. Multiple campaigns of additional work; replication; expansion of empirical scope; broader claims with stronger controls.
- **Not yet** — interesting but the empirical scaffolding isn't built yet.

---

## A. AI-Collaboration Framework + Estimation Loop Empirics

**Working title:** *"Doctrine-Bound AI Collaboration: 21 Rules from Observed Failure Modes in a Multi-Month Autonomous Research Project."*

**Core claim:** AI builders can be calibrated through doctrine-bound exposure; a corrective loop that records `estimated_minutes`, `actual_minutes`, and `calibration_method` per task drives systematic 10× overestimation toward delta near 1.0 over ~20 tasks; a doctrine arc D7→D21 emerging from observed failure modes (each rule traceable to a specific cheat caught) provides discipline scaffolding; a cross-audit triangle (Architect / two Builders) catches what single-audit predictably misses.

**Empirical evidence currently in hand:**
- Codex calibration trajectory: TASK-001 (delta 0.10) → TASK-019 (delta ~0.85-0.90) → TASK-024 (delta 0.70) over 24 tasks, recorded in `project_telemetry/ai_builder_tasks.jsonl`.
- Claude Builder calibration trajectory: TASK-CB-001 (delta 0.20) → TASK-CB-002 (delta 0.267) → TASK-CB-003 (delta 0.556) over 3 tasks. **Faster initial convergence than Codex** — likely because Codex's prior calibration data is now available as scaffolding for Claude Builder's `calibration_method` reasoning.
- Doctrine arc D7-D21: each rule documented in `docs/DOCTRINE.md` and `docs/doctrine_d19_d21.md` with the specific failure mode that motivated it.
- Cross-audit catches catalog: 11 mistake classes in `CLAUDE_BUILDER_INITIATION.md` §4, each with example. Class 11 (Categorical confound through pooling) is a *worked example of cross-audit working* — Builder missed, Architect missed, Codex caught — recorded in BUILD_LOG with the meta-trail.

**Tier:** **Workshop ready** (preprint ready immediately if published as-is on arXiv).

**To advance to conference:** add a third Builder instance (Gemini-class or Mistral-class) and replicate the calibration trajectory across a third architecture. One more campaign or external collaboration.

**Venues:** ICLR Workshop on AI for Code / Scientific Workflows; NeurIPS Workshop on ML Tools / Reproducibility; FAccT (full conference if cross-architecture replicates); ALIFE workshop on AI-collaborative research.

---

## B. Floor-Connectivity Formal-Deficit Candidate

**Working title:** *"Cross-Substrate Equivalence and the Limits of Compositional Mathematics: A Replicated Formal-Deficit Candidate from a Multi-World Attractor Observatory."*

**Core claim:** Across 8 mathematical lenses (graph theory, CRNT, dynamical systems, topology, information theory, Petri nets, statistical mechanics, control theory) operating on a substrate-neutral basin-floor geometry framework, the motif `motif.floor_connectivity.draft` exhibits a formal_gap that survives lens-permutation null and replicates with strengthened signal on independent corpus. The methodology has been validated against a captured-motif baseline (graph lens correctly does NOT flag `replication_lineage` as a deficit). The candidate is bounded to W1/W2 context; multi-substrate confirmation requires fresh corpora.

**Empirical evidence currently in hand:**
- Campaign 010 deficit-map: floor_connectivity formal_gap 0.308, N7 p 0.002.
- Campaign 013 replication on independent corpus: gap 0.355, p 0.001 (strengthened).
- TASK-CB-003 adversarial control: graph × replication_lineage gap 0.036, p 1.000 (methodology validated).
- TASK-CB-003 substrate-blocked control: pooled-corpus result downgraded to `not_evaluable_substrate_confounded` (Class 11 confirmed).

**Tier:** **Workshop ready** for a focused methodology paper on the basin-floor framework + replication. **Not yet conference-ready** for a full L5 missing-math claim.

**To advance to conference:** multi-substrate confirmation on substrate-suitable corpora (Campaign C-A below). At least one substrate beyond W1/W2 must show floor_connectivity gap above threshold under proper Step 0a discipline.

**To advance to journal:** propose a candidate new formal object (sheaf-cohomological / fiber-bundle / quotient framing) that closes the gap on floor_connectivity but leaves adversarial controls untouched (Campaign C-D). Plus replication by an external research group.

**Venues:** ALIFE main conference (if multi-substrate confirms); workshop on Foundations of Theoretical Biology; arXiv math.AT / cs.AI dual-listing for methodology.

---

## C. Substrate Densification + Truth Pass Discipline

**Working title:** *"Substrate Densification as a Pre-Claim Discipline: Truth-Pass Audits Under AI-Collaborative Construction."*

**Core claim:** A substrate that has not been densified along orthogonal process-role / interaction-channel / state-space-effect / overlap-field axes cannot anchor claim-bearing motif observations regardless of how rigorous the detector is; D21 (Densification before claim-bearing) operationalizes this discipline; Truth Pass audits retroactively downgrade historical claims when foundations turn out to be inadequate.

**Empirical evidence currently in hand:**
- 13 simulated worlds with `density_class` per world; W7 advanced from `trace_valid` to `exploratory_densified` in Campaign 011.
- 8 signed Substance Audits (W6–W13 per `papers/methods/SUBSTANCE_AUDIT_W{6..13}.md`).
- Truth Pass document (`papers/methods/TRUTH_PASS.md`) with documented downgrades from prior campaigns.
- Doctrine D7-D21 with each rule rooted in observed failure modes.

**Tier:** **Workshop ready** as a methodology paper for AI-collaborative scientific software construction.

**To advance to conference:** apply the discipline to a second AI-collaborative project as external validation. Or expand the substrate-densification discipline into a generalizable framework with a non-ALife test case.

**Venues:** Workshop on Reproducibility / Open Science / AI Tools; FAccT workshop; ICSE workshop on AI-augmented engineering.

---

## D. The Substrate Engine Itself

**Working title:** *"A Multi-World Computational Observatory for Substrate-Neutral Attractor Discovery."*

**Core claim:** The Attractor Observatory is a substrate-neutral computational research instrument with 13 simulated worlds (chemistry → digital → cognitive → multiscale composition), trace-backed K1-K10 calibration corpora, an 8-lens formal-coverage framework, and a basin-floor geometry analysis layer. The instrument as designed is the contribution; specific scientific results (above) are demonstrations.

**Empirical evidence currently in hand:**
- 13 worlds, all substantive (W1-W2 production; W3-W5 reconstructed; W6-W13 substantive with caveats).
- ~265 pytests across 13 reproducible campaigns.
- Reproducibility scripts (`make_campaign_NNN.py`) for every campaign.
- Cold-start regeneration verified.
- Substrate-neutral ontology (ProcessRole, InteractionChannel, StateSpaceEffect, OverlapField).
- Research Ingestion Factory with audit lifecycle + license enforcement.

**Tier:** **Conference ready** for an instrument-paper / tool-paper.

**To advance to journal:** at least one striking science result anchored on the instrument (currently floor_connectivity-pending-multi-substrate). Real biology grounding (Phase 6) would be a major upgrade.

**Venues:** ALIFE main conference (instrument paper); JSS (Journal of Statistical Software) if generalized; The Journal of Open Source Software.

---

## Aggregate publishing strategy

If we ship a preprint *now* (this week or next) it would be Track A from earlier conversations: paper A above (AI-Collaboration Framework + Estimation Loop Empirics). Workshop-tier; could be on arXiv this week with a focused 8-10 page draft.

Paper B (Floor-Connectivity Candidate) waits for Campaign C-A (multi-substrate fresh corpora) before submission.

Papers C and D could ride on either A or B's preprint priority and follow as full submissions.

The preprint priority claim is real: if the AI-collaboration framework + Estimation Loop empirics go up first, every subsequent paper cites the framework's preprint and the methodology arc is already on the record.

---

## Updates as campaigns close

This file appends per-campaign updates. Format: `## YYYY-MM-DD (Campaign NNN / TASK-XXX): [tier change | new artifact | downgrade | etc.]`

### 2026-05-04 (TASK-CB-002 close): no tier changes; pooled-corpus result tagged for substrate-blocked control.

### 2026-05-05 (TASK-CB-003 close): Paper B methodology validated (adversarial control passes); pooled-corpus result downgraded permanently; Paper A's cross-audit case study extended with Class 11 worked example; Paper B remains workshop-ready, blocked from conference-tier on multi-substrate.
