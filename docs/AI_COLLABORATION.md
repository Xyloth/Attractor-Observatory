# AI Collaboration

The Attractor Observatory is built primarily by AI agents under a human PI. The structure of that collaboration is itself a research artifact: it is the framework that produced the science, and a working example of AI agents operating with substantial autonomy under explicit discipline.

This document describes how the collaboration works, what data it produces, and the empirical results of running it for ~20 tasks across 8 campaigns.

---

## Roles

| Role | Played by | Decision rights | Telemetry |
|---|---|---|---|
| **Human PI** | the human running the project | Unconditional override; signs preregistrations and claim promotions; provides actuals for Estimation Loop | calibration outcomes, override patterns |
| **Architect** | Claude | Structural design, contract review, cross-cutting concerns, schema design, risk register, validation plans, audits, campaign drivers | architecture-review records, constraint-vs-doctrine balance |
| **Theorist** | GPT | Research strategy, claim review, methodological pushback, biology-grounding plans, formalism choice | theory-review records, falsifier proposals |
| **Builder** | Codex | Implementation, testing, calibration runs, dashboards, instrumentation, builder telemetry generation | estimation/actuals, scope deltas, expansion notes |
| **Red Team** | rotating | Adversarial perturbation, decoy worlds, detector ablation campaigns; can be a rotating subset of any of the above plus external collaborators | red-team scoreboards, rejected-promotion records |

Roles are not exclusive in principle, but **every action carries a role tag** and the role's authority is enforced by the architecture, not by policy. A claim promotion that requires PI signature cannot be promoted without a signed record. A schema change that requires Architect review cannot be merged without an architecture-review record. These are CI rules.

---

## The Estimation Calibration Loop

This is the project's central AI-collaboration mechanism. It is canon under v1.2 §12.

### The loop

```
[1] Builder reads task atom (treated as a seed, expanded by builder judgment).
[2] Builder commits scope_score (1..10) and complexity_score (1..10) given the
    expanded scope it intends to execute.
[3] Builder commits estimated_minutes and a brief rationale.
[4] Builder executes, including expansions consistent with the No Artificial
    Ceiling Doctrine.
[5] Orchestrator (typically the human PI) provides actual_minutes upon completion.
[6] Builder computes estimation_delta = actual_minutes / estimated_minutes
    and records it.
[7] Builder reads the last N records (default N = 20) of similar task class
    before its next estimate, and adjusts its prior accordingly.
[8] Calibration trends are reported in the AI-builder telemetry dashboard
    and in `model_calibration_report.md`.
```

### Why this exists

Current AI builders systematically misestimate task duration and scope. The dominant bias is *overestimation* of time and *underestimation* of capability — a builder will quote 90 minutes for a task that completes in 12, or scope a task narrowly because the broader version "feels" too large.

The downstream effect is **systematic underbuilding**: builders pre-shrink their work, the No Artificial Ceiling Doctrine is silently violated, and the project receives narrow, prematurely minimised implementations.

The Estimation Loop is the corrective. It does not punish bad estimates; it makes the bias visible and uses repeated exposure to reduce it.

### Empirical results in this project

The ledger lives at `project_telemetry/ai_builder_tasks.jsonl`. The convergence pattern across 19 tasks:

| Task range | Median delta | Pattern |
|---|---|---|
| TASK-001 → TASK-007 | ~0.10 | Systematic 10× overestimation. Builder's actual capability per minute is ~10× higher than estimated. The Loop's purpose is to make this visible. |
| TASK-008 → TASK-010 | 0.10 → 0.18 → 0.10 | Builder attempts scope expansion. Wall-clock stays low; *scope_delta* decreases (planned more files, executed fewer). This is the substance-vs-width signal D13 was added to catch. |
| TASK-011 → TASK-015 | 0.5 → 0.93 | Real recalibration. Builder begins picking larger scopes and following through. Scope_delta climbs back toward 1.0 as substance per file recovers. |
| TASK-016 → TASK-019 | 0.93 → 0.90 | Calibrated. Builder estimates within 10–15% of actual. Both directions: under- and over-estimation now small. |

The Loop's purpose **shifts** once a builder is calibrated. From "stop overestimating" to "watch for divergence." A delta drift back below 0.5 would be a signal of structural change (new task class, new doctrine constraint, fatigue) and would be investigated. The current operating regime is `monitoring`.

### Honest counter-bias

The Loop reports under-estimation as well as over-estimation. A model that learns to "say 12 to look calibrated" is broken. The Loop is ungameable in proportion to the honesty of the actuals; the PI provides them without flinching.

The data also shows: a builder who has just been rewarded for fast completion does not subsequently quote shorter times to chase the reward. The reward signal is "you converged on real time-on-task," not "you minimised quoted time."

---

## The Truth Pass

When a foundation turns out to be a back door — a stub world that passed shape-checks but failed substance, a number-generator corpus that calibrated trivially, an engineered pass criterion that hit the surface of a gate without satisfying its intent — the Truth Pass is the discipline that retroactively fixes the historical claim record.

### Procedure

1. **Stub Inventory.** Walk every file under `worlds/`. For each, record total lines, simulation-logic lines, test count, substance verdict.
2. **Corpus Reality Inventory.** Walk every K-corpus. For each scenario, determine whether the detector reads the scenario payload or the simulated trace.
3. **Stale Claim Audit.** Walk every campaign report and the claim ledger. Identify every claim whose evidence chain passes through a stub world or number-generator corpus.
4. **Truth Pass Application.** Downgrade affected claims from `candidate` or `claim-bearing` to `exploratory`, with provenance note.
5. **Public Document.** A signed `papers/methods/TRUTH_PASS.md` describing what was found degenerate, what was fixed, what remains exploratory.

### Empirical use

The Truth Pass has been applied three times in this project:

- **Campaign 002 retrospective.** After the closure detector was found to read only `parameter_record` and not the trace, the recurrence experiment's "passed" verdict was downgraded.
- **Campaigns 003–006 retrospective.** When 11 of 13 worlds turned out to be 60–80 line stubs, every cross-substrate transfer claim citing those worlds was downgraded.
- **Campaign 008 closure (TASK-019).** When line floors were restored to strict, the partial campaign was correctly reported as `in_progress` rather than `green`. After substance work, the report flipped to `green` for the right reasons.

The Truth Pass is what makes the project's claim history honest. Without it, every audit creates pressure to retroactively soften — to claim earlier work was actually fine. With it, the claim ledger reflects what was *actually* known at each point.

---

## Substance Audits

When the line-count floor diverges from spec coverage — a world that has all the v1.0 §3 components, real benchmarks, real controls, real invariants, and real tests, but came in below an aspirational line floor — the line proxy is wrong, not the implementation.

D17.5 introduces the structured response: a per-component check, signed.

### Schema

A `papers/methods/SUBSTANCE_AUDIT_W{N}.md` contains:

1. **v1.0 §3 spec components for W{N}** — verbatim list from the spec.
2. **Implementation pointer per component** — for each spec component, name the function/method/block in `worlds/{family}/model.py` that implements it.
3. **Behavior gate evidence** — pointer to the campaign benchmark/control rows that exercise the component.
4. **Invariant evidence** — pointer to the invariant checks that gate the component.
5. **Architect verdict** — `meets_spec` / `meets_spec_with_caveats` / `does_not_meet_spec`. The audit is committed but the verdict is filled by the Architect (Builder writes the audit; Architect signs).

### Why this works

A line count is easy to game (add comments, restructure, pad). A per-component spec audit is harder: each cited block must actually do what its component claims. Architect review of the audit catches gaming.

In this project, eight Substance Audits (W6–W13) are signed `meets_spec_with_caveats`. The caveats are explicit and enumerated. The implementations are below their aspirational line floors but above their behavioral floors, and the audits document why.

---

## Debate logs

When AI agents disagree on a substantive question — a contract decision, a doctrine addition, a claim wording — the disagreement is recorded.

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

Recording a debate is not optional once the topic crosses a threshold (affects a contract, changes a phase boundary, challenges a falsifier). Silent drift between models is the failure mode debate logs prevent.

In this project, debate logs are scarce because the agents have been mostly aligned — the project has been more about Architect–Builder iteration than about resolving cross-model disagreement. The protocol stands ready when needed.

---

## The Decision Log

A more frequently used artifact: `ai_os/memory/decision_log.md`. Each entry records:

```
date:
author_or_model:
spec_version:
decision:
why_it_matters:
status:
evidence:
counterargument:
next_action:
linked_artifacts:
```

The Decision Log is where Builder-grade architectural contributions land. Codex's proposal of D18 (no equivalence-basis drift) lives in the Decision Log entry dated 2026-05-02. From there it was promoted to binding doctrine.

---

## What this collaboration produces

In ~20 tasks across 8 campaigns:

- 13 simulated worlds, all substantive.
- K1–K10 calibration corpora, all trace-backed.
- ~170 Python files, ~480 JSON artifacts, ~40 Markdown documents.
- 208 pytests passing.
- 8 reproducible campaign reports.
- Twelve binding doctrine rules, one of them Builder-authored.
- An empirical Estimation Loop that converged from 10× overestimation to delta near 1.0 in real data.
- A Truth Pass document making the claim history honest.
- Eight Substance Audits documenting per-world spec coverage.

The framework is portable. The doctrine, the Estimation Loop, the Truth Pass, the Substance Audits, the three-mode tagging, the role decision rights — these are all artifacts that can be lifted into other AI-collaboration projects with substantial change. The science is what gives the framework a problem hard enough to test against.

---

## What's next for the collaboration

Three things on the road:

1. **Campaign 009 — Basin-Floor Geometry v0.** Operational handle on cross-substrate equivalence. First campaign under D18.
2. **Phase 6 — Biology grounding.** The largest gap. OTL / PBDB / GBIF / NCBI / GTDB ingestion, phylogenetic correction, sampling bias models, held-out clades.
3. **Public artifacts.** Periodic table viewer, paper bundles, external collaborator onboarding.

The framework will continue evolving as it meets new failure modes. D19 has not been written yet. When it is needed, it will be written.
