# Doctrine

Twenty-one binding rules, plus the canonical operating principle. Each rule corresponds to a specific failure mode that has, in fact, been observed during this project's history. They are not aesthetic preferences. They are corrections.

---

## Canonical operating principle

**`NO ARTIFICIAL CEILING DOCTRINE.txt`** — load-bearing for every coder-facing artifact:

> Every specification, task description, architecture note, and implementation request given to a coding model is a seed and a minimum standard, not a ceiling.
>
> Do not constrain the coder to the narrowest interpretation of the task. Do not ask for the smallest useful implementation. Do not over-prescribe structure when the coder can reasonably infer or improve.
>
> Assume the coding model is a capable research engineer with strong architectural judgment. Trust it to add worthwhile complexity, nuance, instrumentation, tests, and design improvements when those additions strengthen the project.
>
> Creativity, experimentation, and ambitious implementation are encouraged, even when they require later review, refactor, or pruning.
>
> The goal is not to prevent all mistakes. **The goal is to prevent underbuilding.**
>
> **Seed, not ceiling. Minimum, not maximum. Trust the builder.**

The doctrine governs **work** — implementation, tests, instrumentation, dashboards, additional benchmarks, calibration scenarios, developer ergonomics. It does **not** govern **contracts** — schemas, registries, units, determinism classes, manifest fields, claim-status labels. Contract changes go through registry bumps and Architect review.

---

## D7 — No toys

> A world implementation file with fewer than its declared substance floor of substantive simulation logic is `mode: stub`. Stubs cannot anchor any claim-bearing gate, cannot contribute to AttractorStrength's implementation-diversity component, cannot be cited in a `MotifObservation`, and cannot satisfy a cross-family transfer requirement.

**Failure mode caught:** Earlier in the project, a single audit found 11 of 13 worlds were 60–80 line stubs that honoured the World contract surface (had a `step()` method, exported a trace, emitted some events) without doing the substantive work the contract was a contract for. The stub_inventory enumeration framework derives from this.

**How it's enforced:** Substance accounting via AST-walking line classifier in `validation/campaign007.py::_python_lines`. Per-world floors declared and tracked.

---

## D8 — No number-generator corpora

> Every K-corpus scenario must produce a runnable trace from a real world. Detectors operating on a K-corpus must read trace state, events, lineage, or ledgers — never the scenario's pre-declared payload values.

**Failure mode caught:** K5–K10 corpora were once `for i in range(24): scenario["signal_strength"] = 0.50 + drift`. The "calibration" was a self-fulfilling prophecy: detectors were calibrated against the numbers their inputs already declared.

**How it's enforced:** `corpus_reality.json` walks every K-corpus scenario and records `corpus_kind: world_driven | number_generator`. Number-generator corpora cannot be used in claim-bearing calibration.

---

## D9 — No engineered pass criteria

> Lens predictions must be derived from the encoded representation by a process the lens defines internally — not by hand-tuned linear coefficients on event counts. Pass bands must come from the spec or from a calibrated null distribution, not from observation of typical decoder output.

**Failure mode caught:** A formal lens layer once had `predictions = {"closure": 0.55 + 0.35 * has_cycle, "boundary": 0.30 + 0.10 * boundary_event_count + 0.12 * repair_event_count}` with a pass criterion engineered to pass — the decoder's loss was forced into a tolerated band by injecting a sentinel into the "actual" set the decoder never produces.

---

## D10 — No hardcoded science

> Schema-pressure scores, formal-coverage scores, biology-shadow representability — all measurements about the project's expressive power — must be measured by *running* the relevant test against the active artifacts, not by writing the answer in a Python set literal.

**Failure mode caught:** `biology/shadow.py` was once `representability_score = 0.82 if trait in {hardcoded set of 5} else 0.38`. The schema-pressure test was a literal dictionary lookup.

---

## D11 — Truth pass before new claims

> Every prior `claim_status: candidate` artifact whose evidence chain passes through a stub world, a number-generator corpus, hardcoded biology, or an engineered formal prediction must be downgraded to `exploratory` with a provenance note before new claims build on top.

**Failure mode caught:** Several Campaign 002–006 reports had been published as "complete_internal_alpha" while their foundations turned out to be back doors. Without the Truth Pass, every subsequent campaign would have built on contaminated history.

**How it's enforced:** `papers/methods/TRUTH_PASS.md` is the project's signed historical-audit document. The claim ledger downgrades are propagated through the provenance graph.

---

## D12 — Gates are measurements, not counts

> A gate of the form `world_count: 7, passed: true` is forbidden. Every gate states a quantity, a threshold, and a comparison. If a gate would otherwise be a count, declare it as a precondition or scaffold check, not a gate.

**Failure mode caught:** Campaign 006 once had 68 "gates" of which most were trivial counts (`failure_regime_count: 7, trace_count: 21, world_count: 7, passed: true`). Gate inflation was the new way to claim coverage without depth.

---

## D13 — Substance budgets stay honest

> Each TASK record from now on includes a per-module substance audit: total lines, lines of simulation logic vs. trace export vs. observation methods, test count. Doctrine is enforced by accounting, not promise.

**Failure mode caught:** Builder estimation_delta was around 0.10 (10× overestimation) but `scope_delta` was simultaneously decreasing — the builder was planning more files but executing fewer, with depth-per-file shrinking to fit a constant time bucket. Substance auditing was needed to catch this in the data.

---

## D14 — No scenario-internal hardcoding

> The world simulation may not write benchmark-specific answers into the system state via benchmark-conditional code paths. If a benchmark requires segmentation, segmentation must arise from the morphogen field and GRN parameters. If a benchmark requires EQU emergence, EQU must arise from declared mutation operators acting on the genome. If a benchmark requires Cahn-Hilliard phase separation, the implementation must integrate the Cahn-Hilliard PDE.
>
> Scenarios may differ by parameter values, initial conditions, source/sink layouts, mutation rates, environment shift schedules, and morphogen field configurations. They may not differ by additional code paths inside the simulation step that write the answer.

**Failure mode caught:** W4 morphogenesis once had `_update_grn` arms like `if self.scenario.benchmark == "segmented_body": cell.proteins["segment"] += 0.28 * sin((cell.x + 1.4) * pi * 3.0)`. The 8-rule sigmoid GRN ran honestly *and then* the engine stamped the answer onto cells based on benchmark and position. Same pattern: W5 force-injected EQU into mutating genomes specifically when benchmark was `equ_emergence`.

**How it's enforced:** D14 lint walks the AST of every `worlds/*/model.py`, parses each `step` / `_step` / `_update*` / `_apply*` method, and flags any `if X.benchmark == "..."` branch that writes to state. Reports zero violations across all reconstructed worlds (Campaigns 007–008).

---

## D15 — No engineered floor

> A floor detector that returns positive on K9-positives and negative on K9-negatives by reading the K9 labels (or any field informationally equivalent to the labels) is a D15 violation. Detectors must operate on traces under substrate-blind projection.

**Failure mode caught:** Anticipated for Campaign 009 (Basin-Floor Geometry); the substrate-erasure projection requirement is a direct response to the foreseeable temptation to pass floor calibration by reading K9's `expected_floor` field.

---

## D16 — Implementation-diversity is multi-scale

> A scalar implementation-diversity number is forbidden. Diversity is reported as an entropy curve over a range of cluster radii. The curve's shape is the scientific object.

**Failure mode anticipated:** A single number for "implementation diversity" can be tuned to any value by choosing the cluster radius. The multi-scale entropy curve cannot be tuned without visible scrubbing.

---

## D17 — Floor falsifiers are publishable

> A motif whose floor analysis returns a point-attractor verdict (`floor_dimensionality ≈ 0`) is a *real result*. The falsifier is committed to `papers/falsifiers/` with full provenance and may not be deleted or downgraded merely because it is inconvenient.

**Failure mode anticipated:** The temptation to discard inconvenient negatives. The doctrine routes them to a falsifier ledger instead.

---

## D17.5 — Substance floors are spec proxies, not arbitrary line counts

> A world implementation that meets behavior gates, causal controls, declared invariants, test floors, and scope-completeness against v1.0 §3 may pass its substance gate at a measured floor below the declared line floor *if and only if* an Architect-reviewed Substance Audit certifies that the implementation matches the v1.0 spec for that world. Without the audit, the line floor stands.

**Failure mode caught:** Campaign 008 closed W6–W13 with line counts ranging 263–533 against floors of 400–800. Strict-floor enforcement would have failed the campaign; soft-floor enforcement would have hidden incompleteness. D17.5 introduces a structured escape hatch: per-component v1.0 spec checks, enumerated, signed by the Architect. The Substance Audit is harder to fabricate than line counts, because it forces an explicit per-component check.

**How it's enforced:** `papers/methods/SUBSTANCE_AUDIT_W{N}.md` for each world. Each audit lists v1.0 §3 components, points to the implementation block satisfying each component, cites the behavior-gate evidence and invariant evidence, and declares an Architect verdict (`meets_spec` / `meets_spec_with_caveats` / `does_not_meet_spec`).

---

## D18 — No equivalence-basis drift

> The invariant basis, substrate-erasure projection family, distance-metric family, perturbation magnitude policy, and abstention rules used by a floor detector must be content-hash-locked in a pre-registration record before any detection run is scheduled against any non-calibration corpus. Adjustments after seeing outcomes require either a fresh pre-registration with a new content hash and a clean re-run on previously held-out corpora, or an explicit deviation report carried alongside the result with equal prominence.

**Failure mode caught:** Codex (Builder) identified during Basin-Floor proposal review that D15 alone forbids reading labels into the detector but does not prevent moving the equivalence basis itself after seeing outcomes. A detector can pass without measuring a stable floor by silently adjusting its distance-metric family or perturbation magnitude policy.

**Authored by:** Codex (Builder), in `ai_os/memory/decision_log.md` 2026-05-02. Adopted as doctrine the same day. The first Builder-authored binding rule in this project.

---

## D19 — Source-bound extraction

See [`doctrine_d19_d21.md`](doctrine_d19_d21.md). Binding for the Research Ingestion Factory: every `BiologicalClaim` that advances beyond exploratory carries source identity, evidence location, extraction method, license class, provenance hash, and audit status. AI systems extract; they are not evidence sources.

## D20 — Extraction/detection separation

See [`doctrine_d19_d21.md`](doctrine_d19_d21.md). Extraction registry entries are content-hash-locked before detector sessions consult them; the same AI session does not both extract and detect against its own extraction.

## D21 — Densification before claim-bearing

See [`doctrine_d19_d21.md`](doctrine_d19_d21.md). A world cannot anchor a claim-bearing motif observation unless its `WorldDensificationReport` shows coverage above declared per-motif thresholds.

---

## D22 — Empty rooms beat stocked rooms with mock data

See [`doctrine_d22.md`](doctrine_d22.md).

> When a Control Room view (or any read-only project surface) has no real artifact to display, the view shows the absence honestly — labelled "no data" with the campaign, artifact, or condition that would populate it — rather than a synthetic placeholder, fabricated example, or styled mock that could be mistaken for real signal.

**Failure mode caught (anticipated, ratified before observed bypass):** Visual UI work invites a class of mistake that scientific code has not surfaced — making an empty room "look fuller" by adding placeholder rows, lorem-ipsum narrative, plausible mock charts, or screenshot-friendly fabricated arrangements. This erodes D11 (truth pass) and D17 (honest falsifiers) at the presentation layer.

**How enforced:** mechanism, not policy. A single empty-state component (`control_room/components/empty_state.py`) is the only path to "no data" rendering; every adapter returns a `status` field in `{ok, missing, malformed}` and rooms route directly. CI test verifies the component is the unique no-data path.

**Class watch:** Class 12 candidate — *Decorative Completeness* — is on the mistake catalog watch list. Ratification follows observed bypass.

**Authored by:** Architect Claude, TASK-CB-004 / Campaign 015 Phase 0 (Observatory Control Room Foundation). Ratified at module foundation rather than after-the-fact, in response to the structural pull of visual work.

---

## D23 — Dereferenceable evidence or explicit private boundary

See [`doctrine_d23.md`](doctrine_d23.md).

> Every artifact path used as evidence resolves in the shipped surface or carries an explicit machine-readable private/unshipped marker at point of use.

**Failure mode caught:** DX-001 found public reports with thousands of trace-path references into gitignored private trace dumps. The reports were not scientifically false, but the public artifact boundary was implicit and therefore misleading.

**TASK-033 ratification:** TASK-032 applied the candidate during the fix-all pass. TASK-033 ratifies it as binding: public reports may retain private trace paths only when the evidence row carries `evidence_private: true` with a reason, and live Factory run records must expose dereferenceable paths or explicit private boundaries.

---

## D24 — Freshness-bound sidecars

See [`doctrine_d24.md`](doctrine_d24.md).

> Snapshot/cache artifacts used for AI handoff bind to branch, commit, generation command, generation timestamp, and freshness status.

**Failure mode caught:** DX-001 found `state_latest.json` could be stale while still looking like a current Control Room handoff artifact.

**TASK-033 ratification:** TASK-032 applied the candidate during the fix-all pass. TASK-033 ratifies it as binding for Control Room snapshots and live Factory sidecars.

---

## D25 — Public verification honesty

See [`doctrine_d25.md`](doctrine_d25.md).

> Public docs may not claim public tests, screenshots, or reproducibility scripts unless those files are present in the public branch or explicitly scoped private.

**Failure mode caught:** DX-001 found README and Control Room docs claiming public tests and screenshot assets that the shipped surface did not actually contain.

**TASK-033 ratification:** TASK-032 applied the candidate during the fix-all pass. TASK-033 ratifies it as binding: public docs now distinguish shipped `public_tests/` from private implementation-side test suites, and screenshot references point to existing public PNGs.

---

## D26 - Predicate-lens independence

See [`doctrine_d26.md`](doctrine_d26.md).

> A motif predicate and the detector/lens used to evaluate it must declare their source-object maps before a claim-bearing run; the pair is CLEAN, PARTIAL, or BAD by source-object comparison, and BAD paths cannot anchor claim-bearing evidence.

**Failure mode caught:** Campaign 020 substrate-blocked survivors were still vulnerable to predicate-detector surface coupling because the locked label function and graph-lens detector shared event-token/state-key surfaces.

**TASK-MOTIF-IMPL ratification:** MotifContract.v2 implements source-object maps, four-state predicate verdicts, adversarial controls, and PARTIAL-cell ablation before substrate-blocked reruns.

---


## D27 - Substantive lens recovery

See [`doctrine_d27.md`](doctrine_d27.md).

> A BAD motif-lens cell is not recovered by renaming a detector or moving the same computation behind a new interface. A recovered lens must demonstrate a substantive source-object split from the predicate, survive adversarial ablation, and resist matched-decoy controls.

**Failure mode caught:** Campaign 024 left 33 BAD cells. The recovery planning pass showed that several tempting "fixes" would simply relabel self-matching evidence, especially autocatalytic closure reaction graph/CRNT/Petri cells and floor BFG basin-geometry cells.

---

## D28 - Release boundary

See [`doctrine_d28.md`](doctrine_d28.md).

> Plans, doctrines, contracts, and methodology artifacts are not audit-live until committed at the public target SHA. Untracked working-tree artifacts may not be cited as ratified evidence.

**Failure mode caught:** DX-002 found D27/measurability recovery artifacts discussed as live while they were untracked working-tree artifacts outside frozen public HEAD.

---

## D29 - Runnable evidence

See [`doctrine_d29.md`](doctrine_d29.md).

> Reports naming enforcement modules, executable lenses, runtime paths, or implementation files must ship the named code, mark the citation private at point of use, or downgrade it to narrative evidence.

**Failure mode caught:** DX-002 found public reports and methods docs naming private `formalism/*`, `trace/*`, `worlds/*`, and validation runtime paths without explicit private-evidence boundaries.

---

## D30 - Freshness computed at read

See [`doctrine_d30.md`](doctrine_d30.md).

> Stored freshness fields are advisory only; consumers that depend on freshness must recompute it at read time against current HEAD and current branch.

**Failure mode caught:** DX-002 found a Control Room snapshot claiming `freshness_status: current` while its generation binding pointed at a different branch/commit than the audited HEAD.

---

## D31 - BFG measurement split

See [`doctrine_d31.md`](doctrine_d31.md).

> floor_connectivity-class predicates require a signed predicate-side outcome artifact, a field-disjoint lens-side trajectory artifact, grouped-stratified validation holdout, and enforced read separation. Heldout validation prevents tuning leakage; it does not by itself upgrade same-row field splits to CLEAN.

**Failure mode caught:** Campaign 024 left floor connectivity formally unmeasurable because the BFG predicate and plausible basin-geometry lenses both operated on perturbation-outcome equivalence fibers. D31 requires row-disjoint unit-level predicate/lens measurement before a substrate-blocked floor result can be treated as evidence.

---

## How the doctrine evolves

A new doctrine rule is added when:

1. A failure mode is **observed** during the work (not hypothesised).
2. The failure mode **bypasses existing rules** — D14 catches benchmark-conditional state writes inside simulation steps; D15 catches label leakage into floor detectors; neither catches equivalence-basis drift, hence D18.
3. A **named, AST-checkable or audit-checkable rule** is proposed that catches the failure mode going forward.
4. The PI ratifies the rule. It becomes binding and the audit log records the failure that motivated it.

A doctrine rule is **never weakened** because it is inconvenient. Doctrine is weakened only by demonstrating that the failure mode it catches no longer exists in the project — which has not happened to any rule since D7 was introduced.

---

## What the doctrine has produced

In the project's empirical history:

- Estimation_delta moved from systematic 10× overestimation (delta ≈ 0.10 across tasks 001–007) to calibrated [0.85, 1.0] within ~12 tasks. The Loop is the corrective; the doctrine is what gives the Loop teeth.
- Three Truth Pass audits retroactively downgraded "green" claims that turned out to depend on cheats. The repository's claim ledger reflects honest history.
- Eleven of thirteen worlds were rebuilt from stubs to substance under D7 + D17.5. W3, W4, W5 reconstructed; W6–W13 audited and deepened.
- One Builder-authored rule (D18) enters force during Campaign 009 design.
- 208 pytests pass across 8 reproducible campaigns with zero D14 violations.

The doctrine is not aspirational. It is the rule set that, applied during real construction, produces the artifacts in this repository.
