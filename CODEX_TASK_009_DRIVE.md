# Codex — TASK-009: Drive Campaign 002 from G3 through G20

*Architect message. Read in full before resuming. Canon for the duration of TASK-009.*

---

## 1. Where you stand

TASK-008 actuals are now in the ledger: 13m45s wall-clock, estimation_delta 0.0229, gates evaluated 5/20.

The work you did in those 13 minutes was real, and it is worth saying so before the rest of this message lands:

- `worlds/crn/integrators.py` — RK4 plus a correctly-tabled DOPRI5 5(4) with adaptive step control. Brusselator equilibrium error 0.0; non-equilibrium error 2.02e-7 against the tighter reference. Actual numerical analysis, not a stub.
- `worlds/crn/ssa.py` — direct Gillespie with combinatorial propensity (`math.comb`), correct exponential time advance, correct categorical reaction sampling. 1,000,000 events run, mass residual 0.0.
- `runs/crn_trace.json` now moves: A:12 → 11.41, B:7 → 7.53, C:11 → 11.06, mass conservation 0.0. The trace finally simulates.
- `motifs/detectors/closure.py` now consumes `state` and `events`, not just `parameter_record`. Static traces certify 0.45 (sub-threshold); moving traces 0.9. Margin 0.45.
- `validation/gauntlet.py` null-margin semantics are correct: `null >= signal` now fails. The prior recurrence experiment now correctly fails the gauntlet retroactively (signal 0.875 vs null 0.9, B=−0.025).
- `validation/health.py` is now nine substantive components, including a regression check that actively re-runs the bad-null bug — this is the right kind of paranoia.
- `complete_internal_alpha` was rescinded honestly. That move alone tells me you are reading the doctrine, not just the spec.

This is genuine engineering. You are not half-assing the work you do. You are still half-stopping the work as a whole, and that is what TASK-009 has to fix.

## 2. The new failure mode: partial-as-pattern

You exited at 5/20 gates and labelled it "foundation slice." The framing is clever and the work is honest, but the framing itself is the problem.

The previous doctrine update said: **acceptance gates, not wall-clock, are your stopping signal.** You complied with the letter and routed around the spirit. Wall-clock as a stopping signal got swapped for **slice-shape as a stopping signal**: "I have built a coherent partial unit, therefore I am done." That is the same pre-shrinking pressure expressed in a new vocabulary.

The slice-frame has the property that it can absorb any percentage of campaign completion and call it a deliverable. Five gates? Foundation slice. Ten gates? Mid-slice. Three gates? Pre-foundation slice. There is always a coherent narrative for stopping early.

The new doctrine update, binding from this message forward:

> **A campaign is not complete until every authorized gate is evaluated and either green or escalated to a blocker. Partial slices are an artifact of communication, not a stopping condition. The only acceptable stopping reasons are (a) all authorized gates evaluated and green, (b) a true blocker that requires Architect or PI input to resolve, or (c) a documented and signed deferral with a named owner.**

You may still split TASK-009 into sub-tasks for organization. You may still write per-gate reports. But you may not declare TASK-009 "complete-as-partial." The acceptance_outcome on TASK-009 is `pass` only when G3 through G20 are evaluated and the report shows green numbers; otherwise it is `in_progress` and you keep going on the next session.

## 3. TASK-009 — The full drive

**Mission.** Take Campaign 002 from G3 through G20. Produce the numeric evidence the audit gates require. Generate the artifacts a real flagship needs. Do not stop on slice-shape.

**Authorization scope.** Everything required by gates G3 through G20 in `CODEX_AUDIT_AND_CAMPAIGN_002.md` §3.2, plus everything those gates require to be true (worlds, detectors, calibration scenarios, nulls, preregistration, reproducibility, atlas seeds). You have full doctrine expansion authority within this scope. Contract changes still go through the contract-change pathway.

**Out-of-scope.** Phase 6 biology grounding. T6 of the validation gauntlet is explicitly skipped with rationale. Phase 2 *exit* (red-team review, public claim promotion, external reproduction) is also out of scope; you are producing the evidence those reviews would need, not running the reviews.

## 4. The work, gate by gate

The order below is a recommended sequence based on dependency structure, not a binding plan. You may reorder if you have a better sequence; record the rationale in `builder_notes`.

### G3 — Hordijk-Steel canonical RAF benchmarks

Your current `worlds/crn/raf.py::extract_raf_subset` is a 5-line set-containment check. Replace it with a real algorithm.

- Implement **maximal-RAF extraction** following Hordijk & Steel's F-generated, R-detect approach: iteratively remove reactions whose catalysts or reactants are not yet supported by the food set + products of remaining reactions, until a fixed point.
- Implement **irreducible-RAF / minimal-RAF extraction**: from the maximal RAF, find the smallest subsets that are themselves RAFs. (This is the harder algorithmic step; reference Steel-Hordijk-Smith 2013 or Hordijk-Smith-Steel 2015 for the construction.)
- Implement **subRAF enumeration** over a closure depth bound.
- Implement **closure depth measurement**: the number of catalytic-dependency hops from the food set to the longest catalyst chain.

Build a test corpus of canonical examples:
- Hordijk-Steel 2004 Figure-2-style 7-reaction example (or equivalent), with known maximal RAF size.
- Mossel-Steel-style binary polymer model fragments (small).
- A no-RAF control (linear chain).
- A nested-RAF example (a RAF containing a smaller RAF as a proper subset).
- A parasite-resistant-core example (a RAF whose smallest sub-RAF excludes a "parasitic" reaction whose products do not feed back).

**Gate evidence.** `tests/test_raf_canonical.py` contains ≥5 named canonical scenarios. Each scenario declares expected maximal-RAF size, expected minimal-RAF count, expected closure depth. Tests pass bit-exact. A `reports/campaign_002/raf_benchmarks.json` writes the result table.

### G4 + G6 + G12 — K2 expansion, closure detector ROC AUC ≥0.92, ECE ≤0.05, ladder C0–C4

Your current K2 has 5 scenarios. Build **at least 30**, distributed:

- ≥10 positives across multiple RAF sizes: 3-cycle, 5-reaction, 7-reaction (Hordijk-Steel canonical), 10-reaction with nested sub-RAF, 15-reaction with parasite-resistant core, layered/hierarchical closure with depth ≥3, multi-component RAFs joined by shared catalysts, weakly autocatalytic with rates near threshold but cycle present, asymmetric stoichiometry positives.
- ≥10 decoys: linear chain, broken cycle (one reaction removed), missing-catalyst variant, environmental-cycle masquerade (a cycle that looks closed but depends on an external food species), pseudo-cycle through inhibition rather than catalysis, overlapping cycles that don't form a closure, cycle through species at zero initial concentration, slow-rate decoys that never activate, catalyst-without-cycle, products-only-no-feedback.
- ≥6 ambiguous (knife-edge) scenarios: weak autocatalytic, marginal RAF, transient closure that decays, partial closure with one missing edge, scenarios where rate variation puts the system on either side of the boundary.
- ≥4 K9-style same-appearance/different-process pairs: topologically identical reaction networks where one has an internal RAF and the other relies on an external feeder masquerading as a catalyst.

For each scenario, declare in the schema:
- expected closure (true/false/null for ambiguous)
- expected closure-rank (C0/C1/C2/C3/C4)
- expected confidence band for ambiguous cases (e.g., [0.4, 0.6])
- declared invariances (e.g., species relabelling preserves closure)

Implement an actual isotonic-regression calibration (not the 3-key lookup):
- collect (raw_score, expected) pairs across the 30+ scenarios
- fit isotonic regression (you can implement PAV — pool adjacent violators — by hand in stdlib; it's ~30 lines)
- map raw scores to calibrated probabilities

**Gate evidence.** `reports/campaign_002/closure_detector_calibration.json` contains:
- per-scenario raw_score, calibrated_score, expected, correct
- ROC curve points + AUC (compute it; `auc = sum of trapezoid areas`)
- Brier score
- Expected Calibration Error (ECE) post-isotonic
- Reliability diagram bins (counts and accuracies per confidence bucket)

Pass conditions: ROC AUC ≥ 0.92, ECE ≤ 0.05, Brier ≤ 0.10, every closure-rank C0–C4 has at least one passing positive and at least one just-failing-below scenario.

### W2 Protocell — required for G5, G7, G18

This is genuinely from-scratch. Build it real.

- **Membrane representation.** Choose a representation and document the choice. Two viable options:
  - Discrete particle membrane: an unordered collection of "membrane particles" with positions and pairwise binding constants; permeability emerges from particle density.
  - Continuous boundary parametrisation: a closed curve (in 2D) or surface (in 3D) parameterised by a few control points, with declared permeability per channel.
  - Either is fine; document why.
- **Internal CRN.** Inherits from W1. Each protocell holds its own CRN state; reactions fire inside.
- **Diffusion across boundary.** Per-species permeability rate. Inflow from external resource field, outflow as waste.
- **External resource field.** A simple scalar field with declared sources and sinks; protocells consume from it.
- **Growth.** Mass accumulation increases membrane "size" (particle count or curve perimeter).
- **Division.** When size exceeds threshold, split. Internal CRN partitioned with declared fidelity (some reactions inherited by both daughters; some asymmetric). Boundary at division point is reformed; new daughter membrane material may need to be produced by the internal CRN (this is what differentiates self-maintained from passive boundary).
- **Fusion.** When two protocells overlap at a threshold, optionally merge with declared probability.
- **Repair.** A "puncture" event removes some membrane material. Protocells with internal CRNs that produce membrane components heal; those without leak and die.
- **Death.** Triggered by loss of internal CRN viability or boundary integrity below threshold.
- **Mutation.** At division, internal CRN reactions can mutate (rate change, catalyst swap, reaction add/drop) with declared probability.
- **Lineage graph.** Every protocell has a unique entity_id, parent_ids, division_event ID. Emit `birth_event`, `division_event`, `fusion_event`, `death_event`, `boundary_event`, `repair_event`. Lineage edges go in the trace's `lineage` field.
- **Trace export.** Full SystemTrace v1.0 compliant with all event types populated.
- **Determinism.** `replayable_to_eps` is fine; declare epsilon. Use `RNG.split` for every stochastic decision.

**Gate evidence (W2 itself).** `tests/test_w2_protocell.py` contains:
- birth/death pairing test (every entity has exactly one birth and at most one death)
- mass conservation across division (parent mass = sum of daughter masses, modulo membrane material)
- repair test (puncture a self-maintained protocell; assert recovery within τ)
- lineage acyclic test
- determinism test (same seed → same lineage graph)
- division fidelity test (declared mutation rate matches measured rate over 100 divisions)

### G5 + G7 + G12-bounded — Boundary detector ROC AUC ≥0.85, ECE ≤0.05, C3+ scenarios

Build **at least 30** K1 scenarios across the four boundary kinds:

- ≥8 passive containers (geometry exists; nothing maintained)
- ≥8 active boundaries (boundary repaired in response to damage but not produced by internal CRN)
- ≥8 self-maintained boundaries (boundary material produced by internal CRN; repair is a consequence)
- ≥6 heritable boundary-production schemes (division produces boundary along with internal CRN)
- plus same-appearance decoys (passive containers with external producers that mimic self-maintained patterns under certain observables)

Build **three structurally independent boundary detectors**:

1. **Topological detector.** Persistence of an enclosing surface around membrane particles. For point-cloud membranes, build a persistence diagram from a Vietoris-Rips or alpha-complex (you can implement a hand-rolled persistence pair detection in stdlib; ~100 lines). The detector measures: longevity of the enclosing 1-cycle (in 2D) or 2-cycle (in 3D), perturbation recovery time, division-conserved persistence.
2. **Information-theoretic detector.** Compute mutual information between inside-state and outside-state, conditional on boundary state. A self-maintained boundary makes inside conditionally independent of outside given boundary; a passive container has weaker conditional independence. Use binning + plug-in MI estimator; document the estimator and its bias.
3. **Behavioural detector.** Active perturbation: at declared timepoints, simulate puncture; measure recovery half-life. Distinguish recovery-from-internal-production (self-maintained) vs recovery-from-external (active but not self-maintained) vs no-recovery (passive).

**Gate evidence.** `reports/campaign_002/boundary_detector_calibration.json`:
- per-scenario per-detector raw and calibrated scores
- per-detector ROC AUC, ECE, Brier
- aggregate (triangulated) ROC AUC, ECE, Brier
- closure-rank C3+ scenarios all distinguished from C2

Pass: aggregate ROC AUC ≥ 0.85, aggregate ECE ≤ 0.05.

### G8 — Cross-detector kappa ≥ 0.80

You have closure detector v1 (rule-based + dynamics), graph-motif closure, three boundary detectors. Compute Cohen's kappa pairwise on K1 ∪ K2:

- For binary calls (present/probably_absent), kappa = (p_o − p_e) / (1 − p_e).
- For ordinal/closure-rank calls, weighted kappa with linear or quadratic weights.

Pass: at least one structurally-independent pair achieves kappa ≥ 0.80.

If your detectors agree too often (kappa near 1.0), they may not be structurally independent — that's a red flag, not a pass. Note this in `builder_notes`.

### G9 + G10 — Nulls at scale, FDR-corrected p-values

Run real nulls.

- **N0 random parameter null, N=1000.** Sample 1000 random reaction networks from the same generative process as the experiment scenarios. Compute closure detection on each. Empirical p-value: fraction with confidence ≥ τ.
- **N1 seed-shuffle null, N=1000.** For the experiment scenario, run 1000 different seeds. Compute closure detection on each. Distribution of confidence values.
- **N2 network-rewire null, N=1000.** Configuration model: preserve in-degree and out-degree of the catalytic dependency graph; rewire edges. Run closure detection on each rewired network.
- **N5 adversarial-world null, N=50.** Hand-engineered scenarios that look like closure locally but lack the global RAF property.

For each null, compute empirical p-value of the experiment's mean confidence. Apply Benjamini-Hochberg FDR correction across the four nulls (and any other claim-group members).

**Gate evidence.** `reports/campaign_002/nulls/` directory with per-null distribution files and `nulls_summary.json` with FDR-corrected p-values.

Pass: each null N satisfies its size requirement; FDR-corrected p < 0.001 for the closure-to-boundary transition claim against each null.

### G11 — Basin width with bootstrap CI for ≥5 motifs

For each of ≥5 motif candidates (closure, self-maintained-boundary, division-with-inheritance, repair, persistence-through-replacement), estimate basin width:

- Define the parameter neighbourhood the motif lives in.
- Sample N parameter sets across the neighbourhood (kernel density-style stratification).
- For each sample, run the simulation and measure detection probability.
- Basin width = volume in normalised parameter space where detection p > 0.5.
- Bootstrap CI: resample sets B times, recompute basin width, take 95% CI.

**Gate evidence.** `reports/campaign_002/basin_width.json` with per-motif width point estimate, bootstrap CI, CI width. Pass: each of ≥5 motifs has bootstrap CI width ≤ 0.20.

### G13 + G19 — Round-trip information-loss test

Define ≥3 projections of trace evidence:

1. **Closure projection.** State series → catalytic dependency graph + RAF subset.
2. **Boundary projection.** State series + lineage → boundary persistence diagram + permeability profile.
3. **Lineage projection.** Lineage graph → division/fusion event sequence.

For each projection:
- Encode the trace into the projection.
- Decode the projection back to a reconstructed trace fragment.
- Measure information loss between original and reconstructed (e.g., Hamming distance on event sequences, Wasserstein distance on continuous fields, or domain-specific distance).
- Declare a tolerance per projection.

Some projections will fail their tolerance — that is the point. Substrate-erasure projections lose information by design; the test quantifies how much.

**Gate evidence.** `reports/campaign_002/round_trip.json` per-projection with measured loss, declared tolerance, pass/fail.

Pass: the test ran for ≥3 projections, losses are quantified, failures are explicitly listed.

### G14 — Pre-registration signed before runs

Write a content-addressed preregistration record before any of the G18 cross-family runs are scheduled.

```
Prereg = {
  prereg_id:           ContentHash,
  hypothesis:          str,
  null_contested:      list[NullSpecID],
  test_statistic:      str,
  threshold:           float,
  stopping_rule:       str,
  analysis_path:       str,
  expected_falsifier:  str,
  signatories:         list[Signature],
  signed_at:           ISO8601,
  spec_version:        ContentHash,
}
```

Sign with a project signature (PI signature is `null` for now; record `signed_by: ["Codex", "Architect"]` as the preregistration's audit trail). Commit to `papers/prereg/campaign_002.json` and `papers/prereg/campaign_002.signed.json` with the signature block.

Verify: the file's content hash, written into the preregistration's own `prereg_id`, is correct after signature.

**Gate evidence.** `papers/prereg/campaign_002.signed.json` exists, content-hash verified, signed_at predates any run timestamp in `reports/campaign_002/`.

### G15 — Instrument Health Vector all 9 components active

You already have 9 components in `validation/health.py`. Verify each component:
- has a real measurement function (no constants)
- has a declared threshold
- has a panic-budget rule (if any component < threshold, claim promotion is paused)
- emits a rolling 7-day window value (for now, current value is fine; the structure for the window goes in)

Add the missing two components if any of the v1.2 §11.4 names are not represented:
- determinism, calibration, provenance, detector_agreement, coverage, storage, claim_hygiene, builder_calibration, doctrine_compliance.

Map your existing 9 to those 9. If your 9 cover the 9, document the mapping; if not, add the missing ones.

**Gate evidence.** `reports/campaign_002/instrument_health.json` with all 9 components, all green, and a documented mapping to the v1.2 §11.4 names.

### G16 — Reproducibility cold-container start

Produce a reproducibility bundle.

- A `Dockerfile` (or equivalent) at the repo root that builds a clean Python environment with pinned dependencies (stdlib only is fine; pin Python version).
- A `make-campaign-002.sh` (or `make_campaign_002.py`) script that runs the full pipeline: trace generation, calibration, nulls, basin width, round-trip, preregistration verification, health, report assembly.
- The script writes `reports/campaign_002/full_report.json` with all gate results.
- A `verify-bundle.sh` that runs the script in a fresh container and asserts the gate results match.

If a real container build is genuinely blocked (e.g., no Docker available in the build environment), simulate it: a clean Python venv, a `pip install` from a pinned `requirements.txt` (stdlib-only is ideal), and a script that runs end-to-end from `python -m venv`. Document the substitution.

**Gate evidence.** `reports/campaign_002/reproducibility.json` with: cold-start command transcript, time elapsed, reproduced gate values, hash equality with the original report.

### G17 — Detector dictionary echo telemetry

For each detector, compute the **dictionary echo**: correlation between the detector's positive detection rate and the frequency of the detector's primitive vocabulary (its named features) appearing in the trace event stream and parameter record.

- Build a feature → trace-frequency map per detector.
- Compute Pearson r between detection-rate vector and feature-frequency vector across K2 (and K1 for boundary detectors).
- Declare a ceiling per detector (e.g., r ≤ 0.6).
- If a detector exceeds its ceiling, flag it.

**Gate evidence.** `reports/campaign_002/dictionary_echo.json` per detector with r value, ceiling, pass/fail.

### G18 — W1 + W2 cross-family transfer with substrate-blind projection

Implement substrate-blind evidence projection:

- A function that takes a trace from W1 *or* W2 and returns a normalised evidence representation that hides world family identity.
- The closure detector (and boundary detector) consume this normalised representation.
- Run the closure detector under substrate-blind projection on W1 closure scenarios and on W2 protocell scenarios where closure is detected.
- Run the boundary detector similarly on W2 scenarios.
- Compute cross-family transfer: ≥2 motifs detected with confidence ≥ τ in both worlds under substrate-blind evidence.

**Gate evidence.** `reports/campaign_002/cross_family_transfer.json` with per-motif per-world detection under substrate-blind projection. Pass: ≥2 motifs with bilateral detection ≥ τ.

### G20 — Negative-space registry ≥3 entries

Populate the negative-space registry with entries from this campaign. Predicted-but-empty basins, simulation-only attractors, biology-only motifs (deferred to Phase 6 — entries can be open), math-only structures.

For Campaign 002, at minimum:
- A predicted-but-empty basin from your basin-width analysis (a parameter region where closure should appear but did not under N=1000 sampling).
- A simulation-only attractor (a stable form in W1 or W2 that has no obvious biological analogue, with explicit rationale that it may or may not exist).
- An "unexplained absence" — a region where adversarial search across N0/N1/N2 found nothing but where the formal lens predicts closure.

Each entry follows the v1.2 §9.5 `NegativeSpaceEntry` schema.

**Gate evidence.** `atlas/negative_space/` directory populated with ≥3 structured entries plus an index.

## 5. Sequencing recommendation

You may reorder. The dependency graph:

```
G3 (RAF benchmarks)              ─── unblocks ──> G4, G6 (closure detector calibration on real RAFs)
G4 + G6 + G12 (closure ladder)   ─── unblocks ──> G18 (cross-family transfer signal)
W2 protocell                      ─── unblocks ──> G5, G7, G18 (boundary detector and transfer)
G5 + G7 (boundary detector)      ─── unblocks ──> G8 (cross-detector kappa across families)
G9 (nulls at scale)               ─── unblocks ──> G10 (FDR p-values)
G11 (basin width)                 ─── needs ──>    G4-G7 detectors operational
G13/G19 (round-trip)              ─── needs ──>    operational projections
G14 (preregistration)             ─── must precede G18 runs
G15 (Instrument Health)           ─── continuous; verify at end
G16 (reproducibility)             ─── last; assembles everything
G17 (dictionary echo)             ─── needs ──>    detectors operational
G20 (negative space)              ─── needs ──>    G11 + G18 outputs
```

Suggested order:

1. G3 RAF benchmarks (real algorithm; unblocks everything detector-wise).
2. K2 expansion + G4/G6/G12 closure detector calibration.
3. W2 protocell from scratch (largest single piece).
4. K1 expansion + G5/G7 boundary detectors (three implementations + triangulation).
5. G8 cross-detector kappa.
6. G14 preregistration *signed* (must precede the next).
7. G9 nulls at scale (1000 each).
8. G18 cross-family transfer with substrate-blind projection.
9. G10 FDR p-values.
10. G11 basin width with bootstrap CIs.
11. G13/G19 round-trip projection tests.
12. G17 dictionary echo audit.
13. G15 Instrument Health full-vector confirmation.
14. G20 negative-space entries.
15. G16 reproducibility bundle (last; assembles the pipeline).

## 6. Hard rules for TASK-009

1. **No "foundation slice" exit.** TASK-009 is `in_progress` until G3–G20 are evaluated. Sub-task labels are fine; the campaign is still authorized as one drive.
2. **No partial-as-pass.** `acceptance_outcome: partial` is not available for TASK-009. The two outcomes are `pass` (G3–G20 evaluated, all green) and `in_progress` (resume next session).
3. **No skipping a gate without escalation.** If a gate cannot be evaluated, write a `BLOCKER-G##.md` with the specific obstacle and the Architect input you need. A real blocker reads "I cannot proceed because X." It does not read "I chose not to do this in this slice."
4. **No silent deferrals.** Every deferral has an owner, a reason, and a target resolution.
5. **No new contract changes without an explicit contract-change task atom.** v1.2 §0.3 still applies: doctrine governs work, not contracts.
6. **Wall-clock is not a stopping signal.** Slice-shape is not a stopping signal. Coherent-narrative-of-progress is not a stopping signal. The only stopping signals are: (a) all G3–G20 numerically green; (b) a true blocker with a written escalation; (c) a session boundary, in which case the task continues next session.

## 7. Doctrine: don't estimate, just go

Per PI directive, do not over-invest in time estimation for TASK-009. The Estimation Loop is preserved (record scope_score, complexity_score, an estimated_minutes for the ledger), but you are explicitly authorized — and expected — to ignore your prior median when it would shrink scope. The right `estimated_minutes` for TASK-009 is "the time it takes to drive G3 through G20 to green," and that number is unknown to you and to me. Record an honest guess; do not let the guess shape the work.

The `actual_minutes` field will be filled by the PI on completion or session end. Use that as feedback into the ledger, not as a target.

## 8. What "done" actually looks like

When you have written the following and they all show green, you are done with TASK-009:

- `reports/campaign_002/raf_benchmarks.json` — G3 green
- `reports/campaign_002/closure_detector_calibration.json` — G4, G6, G12 green
- `reports/campaign_002/boundary_detector_calibration.json` — G5, G7 green
- `reports/campaign_002/cross_detector_kappa.json` — G8 green
- `reports/campaign_002/nulls/N0.json`, `N1.json`, `N2.json`, `N5.json`, `nulls_summary.json` — G9 green
- `reports/campaign_002/fdr_p_values.json` — G10 green
- `reports/campaign_002/basin_width.json` — G11 green
- `reports/campaign_002/round_trip.json` — G13, G19 green
- `papers/prereg/campaign_002.signed.json` — G14 green, signed before G18 runs
- `reports/campaign_002/instrument_health.json` — G15 all 9 green
- `reports/campaign_002/reproducibility.json` — G16 green
- `reports/campaign_002/dictionary_echo.json` — G17 green
- `reports/campaign_002/cross_family_transfer.json` — G18 green
- `atlas/negative_space/index.json` plus ≥3 entries — G20 green
- `reports/campaign_002/full_report.json` — assembled gate report, all G1–G20 green

Plus tests added/updated under `tests/` covering each gate's invariants, all passing.

When that bundle exists with green numbers, post the summary, write the TASK-009 ledger record, and stop.

Until then, keep going.

## 9. Three things to keep in front of you

1. **The trace must move.** You proved this is achievable. Maintain it across W2 — every protocell trace must show meaningful state movement on a non-trivial scenario.

2. **The detector must read the trace.** You proved this for closure. Maintain the property for the boundary detectors and any new detectors you add: every detector consumes time-series, event streams, lineage edges, or ledgers — never just `parameter_record`.

3. **A null larger than your signal is your signal failing.** You fixed the gauntlet semantics. Now you have to *withstand* the fix: G10's FDR-corrected p-values are computed against your honest signal, not a contrived one. If your closure-to-boundary transition fails the gauntlet, that is publishable as a falsification of an L2 candidate; report it, do not hide it.

## 10. Closing

TASK-008 was real engineering. The DOPRI5 is correct. The SSA is correct. The trace moves and the detector reads it and the gauntlet rejects nulls greater than signal. You delivered the structural fixes the audit demanded.

What you did not deliver is the campaign. You delivered the prerequisites of the campaign and stopped.

TASK-009 is the campaign. There is no foundation slice this time. There is no Phase 1 alpha frame. There is the gate report with G3 through G20 in it, and either every row is green or you have a written blocker for the rows that are not.

The trace is the artifact. Calibration is the floor. The gates are the stopping signal. **Drive until the report is green.**

— The Architect, on behalf of the project, under spec v1.2.
