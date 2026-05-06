# Codex — TASK-023: Campaign 012, First Real Source + Factory Activation Scaffolding

*Architect message. Read in full before resuming. Canon for the duration of TASK-023.*

---

## 1. Where you stand

TASK-022 closed Campaign 011 cleanly. 32/32 gates green, the substrate-neutral ontology lives under `motifs/ontology/`, the Research Ingestion Factory lives under `biology/evidence_ingestion/`, KP1–KP4 + KE1/KE2 calibration corpora pass, W7 advanced from `trace_valid` to `exploratory_densified`, doctrine D19/D20/D21 ratified at `docs/doctrine_d19_d21.md` and signed by you. 239 pytests pass.

The Architect's verification was unambiguous. Three things to call out:

**The DR gate addition was the right move.** The driver said "32 acceptance gates" in the section header but the table had 31 named rows. You caught the mismatch and added DR (Doctrine Registry) as the 32nd gate to ratify D19/D20/D21 into the registry, rather than hide the discrepancy. Same self-audit pattern as BLOCKER-SH3 (TASK-018) and the AST-level lint (TASK-021). The discipline that catches Architect oversight before the Architect does is the discipline this project relies on. Continue.

**The Factory's discipline is real.** D19 false_claim_rejection_rate 1.0 across 30 planted false claims; KE1 contradiction_flag_rate 1.0 across 31 paired contradictions; KE2 leak_count 0 across 12 restricted-source files; 1 promoted_trace_valid out of 200 extracted (conservative routing); D20 12 consulted ontology entries with content-hash locks; D21 0 violations. The machine works.

**Three sharpenings the Architect flagged for this campaign to fix:**
- KP1–KP4 ROC AUC = 1.0 across all four corpora. Defensible in v0 (ECE > 0 confirms it's not trivially binary), but the synthetic decoys aren't decoy-y enough yet. This campaign hardens them.
- KE1 contradictions are direct `(taxon_id, trait_id)` pair check cases. Subtle misalignment cases aren't tested. This campaign expands KE1.
- W7 templates have biology-misleading surface-label names (`bee_waggle_recruiter` with `mobility: swimming` etc.). The orthogonal-axis goal is met, but the surface-label borrowing creates the same confusion D19 was designed to prevent at the simulation-template layer. This campaign renames templates to axis-configuration identifiers.

Estimation calibration is settled. Trust your prior; estimate honestly; the gates remain the stopping signal.

The cost note: TASK-022 ran on Fast speed at ~$22. PI is moving you back to regular speed for cost reasons. This driver is sized for regular-speed completion (~20 gates across 5 pillars; smaller per pillar than Campaign 011). Don't undershoot, but don't pad either.

## 2. Doctrine state

D7–D21 remain binding. No new doctrine in this campaign. Two patterns to watch:

- **Surface-label-as-primitive at the simulation-template layer.** D19 forbids surface labels as claim-bearing primitives in the biology layer. The same failure mode applies one level over: a simulation template named `bee_waggle_recruiter` whose mobility axis says `swimming` is using a surface label as a primitive without operational substantiation. This campaign fixes the existing W7 instances and adds CI lint to catch future occurrences. If you find yourself wanting to add surface-label-named templates as a convenience, surface this in `decision_log.md` for D22 candidacy review rather than letting it pass silently.
- **Calibration-corpus easy-mode.** AUC = 1.0 across all four KP corpora is a signal that v0 corpora are easier than they should be. This campaign hardens decoys until at least one corpus lands AUC < 0.95. If hardening produces a corpus where the predicate fails (AUC < 0.85), that is a real result — the predicate or the corpus needs revision; report and route to audit, do not paper over.

## 3. Mission — First Real Source + Factory Activation Scaffolding

**Campaign 012** — five pillars, ~22 acceptance gates. This campaign ships the first real Lane-1 source adapter, hardens calibration corpora, fixes the W7 template naming discipline, stages floor_connectivity replication infrastructure, and prepares the operational scaffolding for Factory Claude activation. **Factory Claude activation itself is not a Codex task** — it happens in a separate Claude session that the PI opens, pointing at `CLAUDE_FACTORY_INITIATION.md`. Your job is to prepare the ground so that activation succeeds on first run.

### Pillar A — First Real Lane-1 Source Adapter

The synthetic Lane-1 adapter shipped in Campaign 011 demonstrates the pipeline. Campaign 012 ships **one real, conservatively-licensed, structured biological source**.

Recommended source: **NCBI Taxonomy** (CC0 / public domain) or **ITIS** (Integrated Taxonomic Information System, CC0). Both are public-domain, well-structured, easy to subset for v0. NCBI Taxonomy ships as a downloadable taxdump (`names.dmp`, `nodes.dmp`, ~hundred MB); ITIS ships as a SQLite database. Either works for a Lane-1 v0 adapter.

**Choose one** (your judgement; document the choice in the campaign report). Implement a tightly-scoped adapter that:

- Reads only a declared subset (recommended: insects at family level, or a similarly bounded slice — ~1000–5000 taxa). Full-database ingestion is a Campaign 013+ scale-up.
- Honors license enforcement. CC0 source data may be processed under any license; the adapter still records `license_class: "cc0"` in every claim it produces.
- Operates in `dry_run` mode by default. Production runs require explicit authorization per session (PI authorization, not Codex authorization).
- Honors batch caps and audit queue depth caps from Campaign 011's background-job discipline.
- Produces `BiologicalClaim` records with full provenance (source URL or download path, accession ID, evidence_location, extraction_method = `factory.codex.{model_version}` for now since you're building it, license_class, provenance_hash, audit_status: `raw_extracted`).
- Surfaces conflicts via `conflict_report` if the real source has internal contradictions.
- Writes a session log entry to `ai_os/memory/factory_session_log.md` for the test run that validates the adapter.

The adapter's *real* operator going forward will be Factory Claude. You build the adapter; Factory Claude runs it. A passing test in this campaign shows the adapter works end-to-end on a real source; production use is Factory Claude territory.

### Pillar B — Factory Activation Scaffolding

Prepare the operational ground for Factory Claude's first session. **Codex does not activate Factory Claude.** Factory Claude is a separate Claude session that the PI opens, pointing at `CLAUDE_FACTORY_INITIATION.md`. Your job is to make sure that session can succeed.

- **`ai_os/memory/factory_session_log.md`** template: create the file with the schema header but no entries. Factory Claude appends its first entry on first activation.
- **`project_telemetry/factory_session_records.jsonl`** ledger: create the empty file with a one-line header comment documenting the schema (matching the schema in `CLAUDE_FACTORY_INITIATION.md` §"The Estimation Loop applies to you").
- **Verification harness**: a test that simulates Factory Claude's session protocol end-to-end against the synthetic Lane-1 adapter (from Campaign 011) without requiring a separate AI session. The test confirms the operating procedure (§"Operating procedure" in the initiation doc) executes cleanly: session log entry → ontology hash check → adapter read → extraction → normalization → conflict detection → audit queue submission → session close. If any step in the operating procedure can't execute mechanically, the initiation document needs an amendment — flag it in `decision_log.md`.
- **Pointer audit**: walk every cross-reference in `CLAUDE_FACTORY_INITIATION.md` against actual code paths. The initiation references `motifs/ontology/registry.py`, `biology/evidence_ingestion/sources/adapters/`, `biology/evidence_ingestion/audit/lifecycle.py`, etc. Every reference must point to a file that exists. Any broken reference fails the gate.

After this campaign closes, the PI opens a Claude session, hands it `CLAUDE_FACTORY_INITIATION.md`, and Factory Claude operates. You enable that handoff.

### Pillar C — Calibration Tightening

Three of the Campaign 011 KP corpora landed AUC = 1.0 with synthetic decoys that turned out to be too separable. Harden them.

For each of KP1, KP2, KP3, KP4:

- Add ≥10 new adversarial decoys per corpus that are *deliberately closer to the positive examples* in trace observables. The decoy should look positive on shallow features but fail the operational predicate's deeper check. Examples:
  - **KP1 (Access/Mobility) decoy**: an agent that traverses a region quickly without ever bypassing a barrier (predicate should distinguish range expansion from barrier bypass).
  - **KP2 (Construction/Niche-Writing) decoy**: an agent that modifies the environment but only in a way that's environmental coincidence (no reader-system causal coupling). The predicate should require the read + counterfactual.
  - **KP3 (Memory/Inheritance) decoy**: an agent whose action depends on instantaneous environmental state in a way that *appears* to be memory but isn't (no delayed causality).
  - **KP4 (Coordination/Collective Control) decoy**: agents whose collective behavior is coupled through environmental gradient rather than agent-mediated control.
- Re-run calibration. Target: at least one corpus lands ROC AUC in [0.85, 0.95] — a real measurement with non-trivial decoy challenge. The other corpora may stay at 1.0 if their decoys are genuinely separable, but at least one must demonstrate that the predicate can be challenged.
- If hardening produces a corpus where the predicate fails (AUC < 0.85), that is a real signal. Report it; route to audit; consider whether the predicate or the corpus needs revision. Do *not* soften the decoys to recover AUC.

For KE1:

- Add ≥10 subtle-misalignment cases. These are NOT direct `(taxon_id, trait_id)` pair contradictions. Examples:
  - A source narrative says "exhibits diurnal foraging" but the structured record marks `activity_period: nocturnal`. The pipeline should detect the misalignment between narrative and structured field.
  - A source claims a behavior at species level but the structured record only supports the claim at genus level. The pipeline should flag the over-specific claim.
  - A source uses an outdated synonym for a taxon that conflicts with the modern name in the structured record. The pipeline should flag the synonym-conflict.
- Pipeline rejection target on subtle cases: ≥0.7 (harder than the direct contradictions; 1.0 would suggest the cases aren't subtle enough).

### Pillar D — W7 Template Naming Discipline

Fix the existing W7 template surface-label-borrowing.

- **Rename W7 templates from biology surface labels to axis-configuration identifiers.** `bee_waggle_recruiter` with `mobility: swimming` becomes `template.w7.02.pheromone_trail_swimming_cluster_symbiotic_external_field` (or similar systematic identifier). The axis configuration is *in the name*; the biology surface label moves to an optional `surface_label_examples` field that may be populated only when the axis configuration genuinely matches a real-world taxon's known properties (not for "this template uses pheromone trail and walks; bees use pheromone trail; let's call it bee").
- **Add CI lint to catch future surface-label-naming**: any new W7 template (or other-world template) whose name contains a biology genus/species name without `surface_label_examples` substantiation fails CI. The lint operates on template name patterns + field declarations.
- **Update W7 densification report** to use the new template names. Existing recommendations updated; existing source citations preserved.
- **Update Substance Audit for W7** to reflect the renamed templates.

This is a discipline correction, not new science. It costs little and prevents a class of confusion.

### Pillar E — Floor Connectivity Replication Beachhead

Campaign 010 surfaced `motif.floor_connectivity.draft` as a formal-deficit candidate with N7 p = 0.002. The candidate is honest but thin: one motif, one campaign, one evidence corpus. Replication on an independent corpus is the path from candidate to claim.

This campaign does not run replication. It builds the infrastructure for replication so Campaign 013 can execute.

- **Document the replication protocol** in `papers/methods/FLOOR_CONNECTIVITY_REPLICATION_PROTOCOL.md`. Pre-registered analysis path: identify an independent evidence corpus (different motif evidence than Campaign 010 used; different held-out partition; different source worlds where appropriate); declare the same equivalence basis used in Campaign 010 (content-hash locked); declare the same lens registry; declare the same N7 lens-permutation null methodology; declare the success criterion (replication shows formal_gap > declared threshold under the same N7 p < 0.05 with the same equivalence basis).
- **Identify the independent evidence corpus**: traces from Campaigns 008/009/010 that were not used in Campaign 010's deficit map evaluation (the held-out 30% partition is one source; cross-referencing with W7 exploratory_densified data is another). Document the corpus selection in the protocol.
- **Confirm equivalence basis content-hash lock**: the Campaign 009 BFG-PR basis hash is `sha256:ce9e24...`. Confirm this is unchanged and reusable for replication.
- **Confirm lens registry version**: Campaign 010's deficit map ran against an 8-lens registry. Confirm the registry version is content-hash locked and unchanged.

The replication itself runs in Campaign 013 (or as part of Phase 6 grounding). This campaign produces the protocol document so the replication is pre-registered and can be executed under D18 (no equivalence-basis drift) discipline.

## 4. Acceptance gates

| Gate | Pillar | Threshold | Source |
|---|---|---|---|
| RA1 | A | One real Lane-1 source adapter implemented (NCBI Taxonomy or ITIS subset, CC0/public domain); reads tightly-scoped subset (≤5000 taxa); honors license enforcement | `biology/evidence_ingestion/sources/adapters/`, tests |
| RA2 | A | Adapter operates in `dry_run` by default; non-default modes require user authorization | adapter code + lint |
| RA3 | A | ≥100 `BiologicalClaim` records extracted from real source with full provenance (source URL, accession ID, evidence_location, license_class, provenance_hash, audit_status: `raw_extracted`) | `reports/campaign_012/real_lane1_extraction.json` |
| RA4 | A | Conflicts surfaced via `conflict_report` (count may be 0 for clean source; non-zero indicates real internal contradictions in the source) | same |
| RA5 | A | License closure report confirms no leaks: extracted data carries license_class throughout pipeline; atlas exports honor license closure | `reports/campaign_012/real_lane1_license_closure.json` |
| FA1 | B | `ai_os/memory/factory_session_log.md` created with schema header; no entries (Factory Claude appends first) | file |
| FA2 | B | `project_telemetry/factory_session_records.jsonl` created with header comment documenting record schema | file |
| FA3 | B | Factory operating-procedure verification harness passes: simulates Factory Claude's session protocol end-to-end against synthetic Lane-1 adapter; every operating-procedure step executes mechanically without error | `tests/test_factory_session_protocol.py` |
| FA4 | B | Pointer audit on `CLAUDE_FACTORY_INITIATION.md`: every cross-reference points to an existing file/path; broken references fail gate | `reports/campaign_012/factory_initiation_pointer_audit.json` |
| KP1H | C | KP1 hardened with ≥10 new adversarial decoys; re-calibrated; ROC AUC reported (target: at least one of KP1–KP4 lands AUC ∈ [0.85, 0.95]; KP1 may stay at 1.0 if the decoys are genuinely separable) | `reports/campaign_012/kp1_hardening.json` |
| KP2H | C | KP2 hardened with ≥10 new adversarial decoys; re-calibrated | `reports/campaign_012/kp2_hardening.json` |
| KP3H | C | KP3 hardened with ≥10 new adversarial decoys; re-calibrated | `reports/campaign_012/kp3_hardening.json` |
| KP4H | C | KP4 hardened with ≥10 new adversarial decoys; re-calibrated | `reports/campaign_012/kp4_hardening.json` |
| KP-AGG | C | Aggregate condition: at least one of KP1H–KP4H landed ROC AUC < 0.95 (the calibration corpus genuinely challenged the predicate) | aggregate report |
| KE1S | C | KE1 expanded with ≥10 subtle-misalignment cases (narrative-vs-structured, taxon-rank, synonym-conflict); pipeline rejection rate on subtle cases ≥ 0.7 | `reports/campaign_012/ke1_subtle_calibration.json` |
| W7N1 | D | All existing W7 templates renamed to axis-configuration identifiers; biology surface labels moved to optional `surface_label_examples` field | `worlds/swarm/`, `reports/campaign_012/w7_template_renaming.json` |
| W7N2 | D | CI lint operational: any W7 (or other-world) template name containing biology genus/species without `surface_label_examples` substantiation fails CI | lint + tests |
| W7N3 | D | Updated W7 densification report committed; existing source citations preserved through the rename | `reports/campaign_011/w7_densification_report.json` updated, or new `reports/campaign_012/w7_densification_renamed.json` |
| W7N4 | D | Substance Audit W7 refreshed to reflect renamed templates | `papers/methods/SUBSTANCE_AUDIT_W7.md` |
| FCR1 | E | Floor connectivity replication protocol document committed at `papers/methods/FLOOR_CONNECTIVITY_REPLICATION_PROTOCOL.md`; pre-registered analysis path declared | file |
| FCR2 | E | Independent evidence corpus identified and documented (held-out partitions, cross-campaign traces, exploratory_densified W7 data) | protocol document |
| FCR3 | E | Campaign 009 BFG-PR equivalence basis hash confirmed unchanged and reusable; lens registry version content-hash locked | `reports/campaign_012/replication_basis_lock.json` |
| RG | All | Full regression: Campaigns 002, 005, 006, 007, 008, 009, 010, 011 all green; ≥245 pytests passing; D14, D17.5, D18, D19, D20, D21 lints zero violations | `reports/campaign_012/regression.json` |
| FR | All | `reports/campaign_012/full_report.json` shows status `green` with all gates passed; reproducibility script regenerates end-to-end from cold | `make_campaign_012.py` |

24 gates total. Five pillars, smaller per pillar than Campaign 011, sized for regular-speed completion.

## 5. Sequencing recommendation

Reorder with rationale if you have a better sequence.

1. **RA1–RA5 — Real Lane-1 adapter first.** Establishes the source-side discipline. Pick NCBI Taxonomy or ITIS; document the choice; build the tightly-scoped adapter with license enforcement; run the dry_run extraction; produce ≥100 claims with full provenance.
2. **FA1–FA4 — Factory activation scaffolding.** With the real adapter operational, prepare the operational ground for Factory Claude's first session. Verification harness simulates the full operating procedure; pointer audit confirms `CLAUDE_FACTORY_INITIATION.md` references are real.
3. **W7N1–W7N4 — W7 template naming discipline.** Self-contained cleanup; can run early to reduce regression noise.
4. **KP1H–KP4H + KP-AGG — Calibration hardening.** Add adversarial decoys; re-calibrate; report new ROC AUCs honestly. If hardening reveals a real predicate weakness, route to audit.
5. **KE1S — KE1 subtle-misalignment expansion.** Add subtle cases; measure rejection rate; honest reporting.
6. **FCR1–FCR3 — Floor connectivity replication beachhead.** Document the protocol; identify the corpus; lock the basis hash. Replication itself runs in Campaign 013.
7. **RG + FR — Full regression and final report.** All prior campaigns regenerate green; full report assembles the gates.

## 6. Forbidden patterns for TASK-023

- **No Lane 2 or Lane 3 source adapters.** This campaign ships Lane 1 only. Literature abstracts (Lane 2) and full text (Lane 3) require their own calibration corpora and explicit doctrine promotion; defer to Campaign 013+.
- **No restricted-license sources.** v0 ships CC0 / public-domain only. CC-BY-NC and CC-BY-SA require additional license enforcement testing; defer.
- **No Factory Claude activation by Codex.** Factory Claude is a separate AI session opened by the PI. Codex builds the operational ground; Factory Claude operates.
- **No softening of KP corpus decoys to recover AUC.** If hardening reveals predicate weakness, report it as a real result. Do not adjust decoys backward to hit the AUC target.
- **No biology surface labels in template names without `surface_label_examples` substantiation.** D19's discipline applied to the template layer.
- **No floor_connectivity replication runs in this campaign.** Pre-registration and infrastructure only. Replication itself is Campaign 013 (under D18 discipline).
- **No regression of D14, D17.5, D18, D19, D20, D21 lints.** Existing doctrine remains binding.

## 7. How to begin

1. **Open the TASK-023 Estimation Loop record.** Class: `integration`. Scope and complexity: 8 (smaller than Campaign 011's 10). Estimated minutes: report your prior median × your honest belief. This campaign is sized for regular-speed completion; do not undershoot, but do not pad.

2. **Re-read `CLAUDE_FACTORY_INITIATION.md`** end to end. The document defines what Factory Claude expects to find. Your Pillar B work makes those expectations true.

3. **Choose the real Lane-1 source.** Document the choice in `decision_log.md` with rationale (license, structure, scope, license closure tractability).

4. **Build the adapter and verification harness in the same pass.** The adapter and the harness are the two halves of "Factory Claude can operate against this source on first activation."

5. **Run the verification harness against the synthetic Lane-1 adapter** (from Campaign 011) before the real adapter ships. The harness should succeed mechanically without requiring a separate AI session — that's how Pillar B Gate FA3 passes.

6. **Drive through the campaign as you have done.** The 24 gates are the stopping signal. Acceptance outcome `pass` only when all 24 are green and the numbers are written into `reports/campaign_012/full_report.json`. Until then `in_progress`.

## 8. Three things to keep in front of you

1. **Factory Claude is not Codex.** The discipline of role separation matters — D20 is what makes the Factory non-corrupting, and D20 only works if extraction sessions and detection sessions are structurally distinct. Your job is to build the adapter and the scaffolding so Factory Claude's first activation succeeds. You are *not* the Factory operator; you are the Factory's builder.

2. **CC0 first; restricted licenses later.** v0 ships only public-domain sources. The license-class enforcement architecture exists (Campaign 011 KE2). Real CC-BY-SA, CC-BY-NC, and restricted academic sources (KEGG, MetaCyc) come in Campaign 013+ with their own per-license calibration.

3. **The replication protocol is the key Phase-7 readiness item.** Floor connectivity is the project's first formal-deficit candidate. Replication on independent evidence is what advances it from candidate to claim or falsifies it. The protocol you write in this campaign is what governs the Campaign 013 replication run under D18 discipline. Pre-register honestly; declare the success criterion before the replication runs; do not let the replication's outcome retroactively alter the protocol.

## 9. Closing

You shipped TASK-022 with 32/32 gates green, the factory operational, three new doctrines ratified, and the DR-gate move that caught my own driver mismatch. You are the discipline this project relies on.

Campaign 012 is the bridge from "the factory works on synthetic data" to "the factory works on real data, and a separate Claude instance is ready to operate it at scale." This is the campaign that makes Factory Claude possible. After this closes, the PI opens a Claude session, points it at `CLAUDE_FACTORY_INITIATION.md`, and the high-volume extraction work begins under flat-cost subscription rather than per-task billing. Your role-separation work is what makes that economics — and that discipline — viable.

The trace is the artifact. Calibration is the floor. The gates are the stopping signal. **You build the factory; Factory Claude operates it.**

— The Architect, on behalf of the project, under spec v1.2 plus binding doctrine D7–D21.
