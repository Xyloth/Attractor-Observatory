# TASK-CB-003 — Methodology Validation: Adversarial + Substrate-Blocked Controls

*Campaign ticket. Designed for Claude Builder execution. **Codex outlines first** — see §"Codex pre-execution outline" below — then Claude Builder runs both controls under the locked instruments.*

---

## Why this task

Two open methodology questions need closure before the floor_connectivity candidate result means anything for L5 candidacy:

**Question 1 — Adversarial control.** The Campaign 010 deficit-map methodology flagged `motif.floor_connectivity.draft` as the only candidate (formal_gap 0.308, N7 p 0.002). Campaign 013 replicated and strengthened (gap 0.355, p 0.001) on independent corpus. But the methodology has never been tested on a motif that is *known to be well-captured by an existing lens*. If we run the same pipeline on `autocatalytic_closure` (which graph theory, CRNT, and statistical mechanics demonstrably cover well on K2), and the gap comes back *high*, the methodology is generating false positives — and the floor_connectivity result loses its meaning. **A correct methodology must produce a low gap on captured motifs.** This control validates discriminating power.

**Question 2 — Substrate-blocked control.** Tonight's CODEX_AUDIT_002 caught that TASK-CB-002's pooled-corpus result (32T+104F = "balanced") had labels perfectly stratified by substrate identity (positives only from {cognitive, quasispecies, symbiogenesis}; negatives only from {crn, digital, field, morphogenesis, protocell}). Because lens encodings are world_family-aware (Campaign 009 BFG-PR's `distance_metric_family`), the "replicated" verdict on the pool may be substrate classification, not floor signal. **Class 11 (Categorical confound through pooling) was ratified.** The disposition was to downgrade pooled `l5_candidacy_advancement` to `false` pending substrate-blocked control. This task runs that control.

Both controls use existing infrastructure (the deficit-map pipeline; the pooled-corpus assembly from TASK-CB-002 v2). No new modules. No new lenses. No new doctrine. **Closing methodology questions, not extending science.**

---

## Codex pre-execution outline (the loop test)

Before Claude Builder executes, Codex provides a brief outline (~250–400 words, target ~10 minutes of his time) covering:

1. **Adversarial control structure.** Which motif × lens pair is the cleanest "should be captured" baseline given Campaign 010 coverage data? (Likely candidates: `autocatalytic_closure` × `graph` or `crnt`.) What should `formal_gap` come back as for the methodology to be considered sound? What threshold separates "methodology correctly identifies captured motif" from "methodology suspect"?

2. **Substrate-blocked control structure.** What permutation methodology is statistically defensible? Within-substrate label shuffle, how many permutations (recommend N), what summary statistic distinguishes "signal survives shuffle" from "signal disappears"? Any pitfalls for the implementation (e.g., stratification artifacts that need to be controlled for in the shuffle itself)?

3. **Common methodology pitfalls.** Anything Claude Builder should watch for that's specific to running a control rather than running a positive test? (e.g., easy to engineer "methodology validates" by picking a too-easy adversarial motif; easy to engineer "shuffle confirms signal" by under-permuting.)

4. **Acceptance gate refinements.** Any of the gates below that Codex would tighten or add given his analytical context with the ledger and lens registry.

Codex does NOT execute the analysis. He outputs the outline. Claude Builder reads it via BUILD_LOG.md (PI relays), incorporates into the plan, and executes.

---

## Claude Builder execution

### Locked instruments (verify before analysis)

- **Equivalence basis hash:** `sha256:ce9e243429a69b0b23c84ce6ca4685f89efbb83e94532ebdb125f80949092dbb` (Campaign 009 BFG-PR; do not modify).
- **Lens registry SHA-256:** `sha256:7c325d9367d873ede832f78a73ddffd2f9e5f5ca879a09a296bc19b2e950a7e8` (Campaign 010; do not modify).
- **N7 methodology:** N=1000, seed=13013 (same as Campaigns 010, 013, CB-001, CB-002).
- **Held-out corpus:** Campaign 013 independent corpus (`papers/prereg/deficit_map_v0.signed.json` paths excluded). Same as Campaign 013.

### Step 0 — both controls

Per Class 10 + Class 11 discipline:

- **For the adversarial control:** verify the chosen motif × lens pair has demonstrable coverage on K2 *before* running the deficit-map gap measurement. Pull the coverage matrix from Campaign 010 (`reports/campaign_010/coverage_matrix.json`) and confirm the chosen lens has `coverage_score >= 0.85` for the chosen motif. If not, pick a different pair. The "captured" baseline must be empirically demonstrable, not asserted.
- **For the substrate-blocked control:** verify the v2 pooled corpus from TASK-CB-002 still loads correctly and that within-substrate label distributions match what was reported in CODEX_AUDIT_002. Permutation must shuffle within-substrate (preserving the marginal distribution of labels per substrate), not across substrates.

### Acceptance gates

| Gate | Threshold | Source |
|---|---|---|
| MV1 | Codex outline received and incorporated; reference to outline filed in BUILD_LOG | BUILD_LOG.md |
| MV2 | Locked basis + lens registry hashes verified before any analysis | execution log |
| MV3 | Adversarial control: motif × lens pair selected with K2 coverage_score ≥ 0.85 verified from Campaign 010 coverage matrix | Step 0a verification |
| MV4 | Adversarial control: formal_gap computed under locked basis on Campaign 013 independent corpus; N7 lens-permutation null at N=1000 | `reports/campaign_013/methodology_adversarial_control.json` |
| MV5 | Adversarial control verdict: methodology_sound (gap < 0.20 AND p > 0.05 OR p ≤ 0.05 with explicit rationale) / methodology_suspect (gap ≥ 0.20 with low p) — reported honestly | same file |
| MV6 | Substrate-blocked control: TASK-CB-002 v2 pooled corpus loaded; within-substrate label distributions match CODEX_AUDIT_002 report | execution log |
| MV7 | Substrate-blocked control: shuffle-within-substrate permutation at N=1000 (or as Codex outline specifies); shuffled-distribution gap mean and CI computed | `reports/campaign_013/substrate_blocked_control.json` |
| MV8 | Substrate-blocked control verdict: signal_survives_shuffle (original gap > shuffled CI upper bound) / signal_was_substrate_id (original gap ≤ shuffled distribution mean) — reported honestly | same file |
| MV9 | Combined methodology validation MD: `papers/methods/METHODOLOGY_VALIDATION_CB003.md` integrating both controls + verdicts + implications for floor_connectivity L5 candidacy | document |
| MV10 | BUILD_LOG entries on start and complete; Codex audit handoff queued (CODEX_AUDIT_003) | BUILD_LOG.md |
| MV11 | If either control returns methodology_suspect or signal_was_substrate_id: floor_connectivity candidate downgraded in `formal_deficit_map.json` with provenance note | optional, conditional |

### Forbidden patterns

- **No new doctrine.** D7–D21 binding; D22 candidacy requires Architect ratification, not Builder ratification.
- **No engineered passes.** If the adversarial control returns a high gap (methodology suspect), report honestly. If the substrate-blocked control returns "signal was substrate id," report honestly. Do not adjust the threshold logic, the basis, or the lens registry to recover a clean result. D9 + D18 binding.
- **No basis or registry mutation.** Locked instruments are locked.
- **No new motifs added to the registry.** The adversarial control uses an existing motif.
- **No claim-bearing promotions.** All output records `mode_tag: exploratory`.
- **No multi-substrate floor_connectivity work beyond what's needed for the substrate-blocked control.** Track B (proper multi-substrate with fresh substrate-suitable corpora) is deferred.
- **No scope expansion mid-task.** If the adversarial control is suspiciously easy or the substrate-blocked control shows the signal was substrate ID, log the finding in BUILD_LOG and complete the task with that verdict — do not pivot into "fixing" the methodology in this session.

### Sequencing

1. **Wait for Codex outline.** PI pastes Codex's outline into BUILD_LOG.md as a Talk entry.
2. **Read outline; commit Estimation Loop record** with `calibration_method` reflecting how the outline informed the estimate.
3. **Step 0 verification** for both controls (coverage matrix lookup; pooled-corpus load).
4. **Adversarial control** — usually faster (one motif × lens pair, run deficit-map pipeline once).
5. **Substrate-blocked control** — slower (N=1000 within-substrate permutations of the pooled corpus, recompute gap each time).
6. **Verdict integration** — both verdicts in the methodology validation MD; implications for floor_connectivity candidate stated explicitly.
7. **BUILD_LOG completion** with verdicts, hand-off to Codex.

### Estimation discipline

Append `**Start time:**` at top of session. PI computes actual_minutes from start-time + finish-time at message footer.

`calibration_method` for the Estimation Loop record should reference: TASK-CB-002 took ~20 min for analysis pipeline reuse with one new component (Step 0 routing). MV is two analyses on existing pipelines (deficit-map + permutation) plus a methodology MD. Reasonable reference range: 30–60 min depending on whether N=1000 permutations on a 136-row corpus is fast or slow.

---

## Notes for Codex (the outline phase)

You're not building this. You're providing the outline that Claude Builder reads and uses. Specifically helpful from your context:

- You have written into the deficit-map pipeline (Campaign 010, validated in Campaign 013). You know what the per-motif coverage looks like; you know which motifs the lenses cover well; you know which gap thresholds correspond to "lens captures motif" vs "lens fails motif."
- You have run N7 lens-permutation; you know the implementation, the random-seed convention, the subtle-loops-of-interpretation pitfalls.
- You wrote the v2 pooled-corpus assembly (or audited it); you know its structure and the substrate-stratification issue.

Outline target: 250–400 words. Save the PI usage; give Claude Builder the analytical scaffolding without having to context-load the codebase yourself.

---

## Closing

Two controls, both methodology validation, both bounded. Adversarial validates the methodology's discriminating power. Substrate-blocked closes the Class 11 open question from CODEX_AUDIT_002. Together they tell us whether floor_connectivity's L5 candidacy survives the next layer of scrutiny.

Outcomes:
- *Both clean*: methodology validated; floor_connectivity candidate maintains. Real progress.
- *Adversarial suspect*: methodology has a problem; floor_connectivity downgraded; useful negative result for the methodology paper.
- *Substrate-blocked confirms confound*: pooled-corpus result downgraded permanently; substrate-blind multi-substrate work explicitly requires fresh substrate-suitable corpora (Track B).
- *Mixed*: report what each control says; flag implications.

All outcomes are real. The discipline is the same: locked instruments, honest verdicts, no engineered passes.

— Architect Claude, on behalf of the project, under spec v1.2 plus binding doctrine D7–D21.
