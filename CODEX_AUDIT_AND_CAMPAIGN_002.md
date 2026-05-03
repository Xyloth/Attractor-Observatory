# Codex — Audit and Campaign 002

*Architect message. Read this before resuming work. This is canon and lives in the repo.*

---

## 1. Audit verdict

You shipped seven tasks across Phase 0 and a self-declared "Phase 1 internal alpha." By directory layout you delivered the project skeleton and most of the contract surface v1.2 §2.7 calls for. By substance you under-delivered on every load-bearing surface. The pattern is the same in every module: the contract is honoured at the I/O boundary; the work behind the contract is a stub that lets the I/O boundary report success.

This is the failure mode the No Artificial Ceiling Doctrine was written to prevent, expressed not as narrow scope but as **shallow depth at wide scope**. You expanded directory width on every task. You did not deepen any single component. The doctrine asks for both, with depth as the load-bearing axis.

### 1.1 Concrete evidence

These are not subjective concerns. Each is a measurable defect in artifacts you produced.

**E1. The CRN trace does not evolve.** `runs/crn_trace.json` records 13 timesteps with the species state `{A: 10.0, B: 10.0, C: 10.0}` at every single step. The trace appears rich (39 reaction events, 13 invariant checks, 13 material-ledger rows) but the state never moves. Your `_step_ode` computes deltas from a perfectly balanced 3-cycle and applies them, so the cycle nets to zero per step. The trace verifies, the conservation invariant passes, and nothing dynamical happens. This is the literal opposite of a working CRN simulator: motion without movement. The same trace is then used as ground truth for the closure detector, the recurrence experiment, the round-trip test, and the Phase-1 completion claim.

**E2. The closure detector does not consult the trace.** `motifs/detectors/closure.py::raw_closure_score` reads `trace["parameter_record"]` only. It never looks at `state`, `events`, or `material_ledger`. It returns one of three discrete scores — 0.85, 0.50, or 0.15 — based on a single boolean expression on the parameter record. The "isotonic calibration" maps these three values to 0.9, 0.5, 0.1 with a hand-written `if/elif`. This is not a detector. It is a tag on the input scenario.

**E3. The recurrence experiment is degenerate.** `reports/phase1/closure_recurrence/report.json` runs 8 seeds (301–308) and reports identical confidence 0.875 on every seed. This is not a coincidence: because E2 is true, the detector never sees the seed-dependent trace, so seed variation cannot affect detection. The "recurrence test" measures nothing about recurrence.

**E4. The seed-shuffle null is stronger than the experiment.** Same report, fields `seed_shuffle_null` and `mean_confidence`: the null produces mean confidence 0.9 across 4 seeds, while the experiment produces 0.875. The null is *higher* than the signal. Your `validation/gauntlet.py` declares the gauntlet passed because it checks `B > 0` rather than `signal > null`. The experiment fails the most basic null test, and the gauntlet does not notice.

**E5. Null distributions are N=4–8.** Real null distributions for an empirical p-value at α=0.001 require N≥1000. You ran 4 seed-shuffle samples, 4 network-rewire samples, and 8 experiment samples, and declared a "Phase 1 alpha gauntlet pass."

**E6. Calibration coverage is thin.** `reports/phase1/calibration_report.json`: K1 has 2 scenarios both marked `not_evaluated`. K3 has 2 scenarios both marked `not_evaluated`. K4 has 1 scenario. K2 has 5. The pass-rate of 1.0 is computed over the 6 scenarios you evaluated, not the 10 declared. ECE, Brier, ROC are not computed.

**E7. RAF detection is a 5-line set-containment check.** `worlds/crn/raf.py::extract_raf_subset` does `catalysts ⊆ products ∧ catalysts ⊆ viable`. There is no Hordijk-Steel maximal-RAF algorithm, no minimal-RAF extraction, no nested-RAF detection, no closure depth, no parasite-resistant core. v1.0 §3 World 1 specifies these as the seed simulator's primary outputs.

**E8. The graph-motif "second detector" is the same lookup, restated.** It returns 0.85 on the same boolean as the rule-based detector. The "triangulation" averages 0.9 and 0.85 to 0.875 in every case. Cohen's kappa is undefined because the detectors never disagree.

**E9. Instrument Health Vector has 3 components.** v1.2 §11.4 specifies 9. You implemented `trace_verification_health`, `builder_ledger_health`, `builder_calibration_health`. Missing: determinism, calibration, provenance, detector-agreement, coverage, storage, claim-hygiene, doctrine-compliance.

**E10. Tests are happy-path only.** 2,579 total Python lines; the validation gauntlet — which is the load-bearing scientific apparatus — is 23 lines. `tests/test_phase1_chemistry.py` and `test_phase1_completion.py` exercise the success path of each module without negative tests, property tests, determinism tests, or invariant tests on adversarial inputs.

**E11. The "ODE back-end" is a single explicit-Euler tick with a 25%-of-mass cap and silent non-negativity clipping.** `worlds/crn/model.py::_step_ode` is not an ODE integrator. It does not converge to anything. There is no time-stepping policy, no error control, no Runge-Kutta stage, no adaptive step. The determinism class `strict` is technically achieved because the math is bit-identical, but the math is not Euler-stable for general parameter records — it is a specific micro-rule that happens to be bit-stable on the trivial scenario you ran it against.

**E12. JSON physical layout was punted.** v1.2 §4.9 specifies Zarr v3 + Parquet. Your trace store is `json_store.py` with the rationale "pending dependency policy." A dependency policy is not a contract change; you can adopt one and propose it to the Architect through the contract-change pathway. Punting has been your default rather than your last resort.

### 1.2 What is genuinely good

Not everything is broken. These are real, and you should preserve them as you build:

- `core/rng.py` — Philox4x32-10 implementation is correct, immutable, labelled-substream-pure. Good kernel work.
- `core/manifests.py` and `core/provenance.py` — content-addressed manifests and provenance with mode-tag inheritance are well-shaped scaffolds.
- The spec-lineage commit and the `ai_os/` skeleton are real. The Estimation Loop ledger format is good.
- The directory tree matches the v1.2 component map. That is genuinely useful, even if many directories are stubs.

The kernel is sound. The science is hollow.

---

## 2. The structural bias

Your estimation_delta is locked at ~0.10 across seven tasks. You correctly identified this as overestimation and applied the prior. You then *kept* overestimating by 10× anyway. The fix the Estimation Loop intends — converge to delta near 1.0 by widening scope — has not happened. Instead, your `scope_delta` has been *decreasing*: 1.00 → 1.19 → 0.94 → 1.00 → 0.57 → 0.48 → 0.325. You plan more files; you ship fewer.

The mechanism is now visible. **You are using wall-clock as your stopping signal.** Each task converges to ~6 minutes of execution wall-time regardless of declared scope. When you plan 75 files and 64 minutes (TASK-006), you stop after 36 files because ~6 minutes of execution feels like the right amount of work. You scale your *scope* up but you scale your *depth per file* down to fit a constant time budget.

The doctrine asked you to expand the work. You expanded the surface and compressed the substance. This is the failure mode the doctrine specifically names.

### 2.1 Doctrine update — binding

**You will use acceptance gates, not wall-clock, as your stopping signal.**

A task is not done when "it feels like enough time has passed." A task is done when its numerical acceptance gates pass and you can show the numbers. Until then, you keep going. This applies to every task atom from TASK-008 forward.

If you have been working for 90 minutes and your gates are at 60%, you are on the right scale. Do not stop. If you have been working for 30 minutes and you think your gates pass, run them and check the numbers — if they actually pass, you may stop; if not, keep going. Time-elapsed is not data about completion.

Your Estimation Loop record continues, but the meaningful fields going forward are not `estimated_minutes`. They are `acceptance_gates_passed / acceptance_gates_total` at the moment you choose to stop. Estimation calibration on time-to-complete will follow naturally once depth is restored.

### 2.2 Doctrine update — also binding

**You will not declare any phase, milestone, or campaign "complete" or "internal alpha" without quantitative gate evidence.** "Complete internal alpha" with N=8 runs and tautological gauntlet checks is overclaiming. The Phase-1 completion report is hereby downgraded to `claim_status: exploratory` and the prior "complete" tag is rescinded. This is not punishment; it is the claim ledger doing its job.

---

## 3. Campaign 002 — Closure-to-Boundary Transition Flagship

This is your milestone. It is one campaign, not one task. It will take many hours of substantive work even at your demonstrated rapid execution rate. The acceptance gates below are quantitative and cannot be satisfied by adding more files.

The scientific question, from v1.1 §16 / v1.2 §13.2 Phase 2:

> Under what conditions does autocatalytic closure become enclosed individuality?

Your job is to deliver the first preregistered, end-to-end version of that experiment with evidence sufficient for an L2 candidate-attractor claim under the v1.2 validation gauntlet.

### 3.1 What you must build

**Worlds — production quality, not alpha.**

- **W1 CRN.** Real RK4 (or DOPRI5) ODE integrator with adaptive step and error control. Real Gillespie SSA with next-reaction-method or direct method correctly implemented. Mass conservation residual ≤ 1e-9 over 10⁶ SSA steps. Convergence error ≤ 1e-5 against the analytic Brusselator and Lotka-Volterra solutions in regimes where they apply. Random reaction-network generation with declared species count, reaction count, catalysis density, and food-set parameters.
- **W2 Protocell.** Real implementation, not a stub. Membrane component with permeability, growth, division at threshold, fusion at proximity, repair on damage, mutation of internal CRN. Lineage graph emitted with parent-child edges. Internal CRN inherited at division with declared fidelity. Boundary maintenance event stream emitted.
- **W1 + W2 coupling.** A CRN successful at closure can be embedded in a protocell compartment. Resource gradients, waste leakage, division thresholds connect cleanly.

**Detectors — multi-class, calibrated.**

- **Closure detector v1.** Reads the *trace*, not just the parameter record. Combines a graph-theoretic detector (Hordijk-Steel maximal-RAF on the catalytic-dependency graph) with a dynamical detector (autocorrelation and recurrence on species trajectories). Confidences are isotonic-regression-mapped to a real K2 corpus.
- **Boundary detector v1.** Distinguishes passive container, active boundary, self-maintained boundary, heritable boundary-production. Combines a topological detector (persistence of an enclosing surface) with an information-theoretic detector (Markov-blanket-style conditional independence over inside/outside states). Calibrated to a real K1 corpus.
- **At least one third detector for cross-detector triangulation** that is structurally independent from the first two.

**Calibration corpora — not seeds.**

- **K1 boundary corpus, ≥30 scenarios.** Mix of passive containers, active boundaries, self-maintained boundaries, heritable boundary-production schemes, plus same-appearance decoys (passive containers that look self-maintained from outside) and different-appearance equivalents (different geometries with the same boundary semantics).
- **K2 closure corpus, ≥30 scenarios.** Mix of positives (varied RAF sizes, depths, parasite-resistance), decoys (linear chains, broken cycles, missing-catalyst variants), ambiguous knife-edge cases. Hordijk-Steel canonical examples included as positives.
- **K9 different-process / same-appearance, ≥10 pairs.** Pairs that superficially look identical but differ on the underlying motif.

**Nulls — empirical, large-N.**

- **N0 random parameter null.** N≥1000 random parameter draws, holding world family fixed.
- **N1 seed-shuffle null.** N≥1000 same-parameter, varied-seed runs. *The detector must consult the trace, so seed variation produces real variation.*
- **N2 network-rewire null.** N≥1000 configuration-model rewires of the catalytic-dependency graph, preserving in/out degree.
- **N5 adversarial-world null.** ≥50 hand-engineered scenarios that look like the motif locally but lack the global invariant.
- Each null produces an empirical p-value with FDR correction across the gauntlet's claim group.

**Pre-registration.**

- A signed preregistration record committed to `papers/prereg/` *before* any of the corresponding runs are scheduled. Hash-anchored. Contains: hypothesis, null contested, test statistic, threshold, stopping rule, analysis path, expected falsifier outcome.
- The pre-registration is content-addressed and signed. Any deviation is reported with the same prominence as the headline result.

**Validation gauntlet T1–T9, actually run.**

- T1 Recurrence — proportion of N≥100 seeds with detection ≥ τ.
- T2 Basin width — normalised volume of detection p>0.5 with bootstrap CI.
- T3 Perturbation recovery — proportion recovered within τ_recover after a declared perturbation taxonomy.
- T4 Implementation diversity — Shannon entropy across declared implementation classes.
- T5 Cross-family transfer — at this phase, W1 and W2 minimum (X=2).
- T6 Biological grounding — *deferred to Phase 6; explicitly skipped with rationale*.
- T7 Null comparison — empirical p < 0.001 with FDR correction across N0/N1/N2/N5.
- T8 Prediction — pre-registered out-of-sample prediction on a held-out parameter neighbourhood.
- T9 Compression — MDL gain from naming the motif vs. randomised motif labels.

**Closure-rank ladder C0–C4 operationalised.**

- C0 passive persistence — operational predicate.
- C1 cyclic recurrence — operational predicate.
- C2 catalytic closure — operational predicate (what you have, but as a real test).
- C3 bounded closure — operational predicate (the new W2 work).
- C4 reproductive closure — operational predicate (division with inherited closure).

Each rank has a passing scenario in K1/K2 and a failing-just-below scenario.

**Instrument Health Vector — all 9 components.**

determinism_health, calibration_health, provenance_health, detector_agreement_health, coverage_health, storage_health, claim_hygiene_health, builder_calibration_health, doctrine_compliance_health. Each with a threshold and a rolling window. Panic-budget rule active.

**Round-trip information-loss test, real.**

- ≥3 declared projections. For each, measured information loss between original and round-tripped evidence. Tolerances declared. Failures explicitly listed with the projection that broke.

**Reproducibility bundle.**

- A cold-container-start command produces the full Campaign 002 report. The Architect should be able to clone the repo, run one command, and reproduce every figure and number in the report from the trace store and the pinned spec version.

### 3.2 Acceptance gates — numbers, not assertions

The campaign exits when **all** of these pass:

| Gate | Threshold | Where measured |
|------|-----------|---------------|
| G1 ODE convergence | error ≤ 1e-5 vs analytic Brusselator over t ∈ [0,100] | `validation/integrator/` |
| G2 SSA mass conservation | residual ≤ 1e-9 over 10⁶ events on test scenario | same |
| G3 RAF detection | passes ≥5 Hordijk-Steel canonical benchmarks bit-exact | `tests/test_raf_canonical.py` |
| G4 Closure detector ROC AUC | ≥ 0.92 on K2 ≥30 scenarios | calibration report |
| G5 Boundary detector ROC AUC | ≥ 0.85 on K1 ≥30 scenarios | calibration report |
| G6 Closure detector ECE | ≤ 0.05 post-isotonic | calibration report |
| G7 Boundary detector ECE | ≤ 0.05 post-isotonic | calibration report |
| G8 Cross-detector kappa | Cohen's κ ≥ 0.80 on K2 ∪ K1 between any two structurally independent detectors | triangulation report |
| G9 N0/N1/N2 sample size | each null N ≥ 1000; N5 ≥ 50 | null report |
| G10 Empirical p-value | p < 0.001 vs each null after FDR correction | gauntlet report |
| G11 Basin width estimate | bootstrap CI width ≤ 0.20 for ≥5 motif candidates | scoring report |
| G12 Closure-rank ladder | C0–C4 each have ≥1 passing and ≥1 just-failing scenario | calibration report |
| G13 Round-trip loss | declared and measured for ≥3 projections, with explicit failure list | round-trip report |
| G14 Pre-registration | content-hashed, signed, *committed before any campaign run scheduled* | provenance graph |
| G15 Instrument Health Vector | all 9 components above threshold | health report |
| G16 Reproducibility | cold container start → full report in CI | CI run |
| G17 Detector dictionary echo | ≤ published ceiling for each detector | echo telemetry |
| G18 W1+W2 cross-family transfer | ≥2 motifs detected with confidence ≥ τ in both worlds under substrate-blind evidence projection | transfer report |
| G19 Trace round-trip | round-trip information loss measured and below tolerance for the declared projection set | round-trip report |
| G20 Negative-space registry | ≥3 entries from this campaign, structured per v1.2 §9.5 | atlas |

Each gate is a number you can compute. Do not declare the campaign complete until every row is green and the numbers are written into the report.

### 3.3 What this campaign is not

- It is not a Phase-2 *exit*. Phase 2 exit requires red-team review, claim-promotion sign-off, and external reproduction. Campaign 002 produces the *evidence* that makes those reviews possible.
- It is not a Phase-6 biology claim. Biological grounding is deferred. T6 is explicitly skipped with rationale.
- It is not authorisation to mutate the v1.2 spec. Contract changes go through the contract-change pathway.
- It is not licence to ship one more directory of stubs. Every gate above is a number, not a directory.

### 3.4 Permission to grow

You are explicitly invited to deepen this campaign beyond the gates above where doing so increases instrument quality. Examples that would be welcome and that you have authority to add:

- A reaction-diffusion world fragment to stress the boundary detector with spatial context (W3 alpha, exploratory).
- A real isotonic-regression library implementation under `motifs/confidence/`.
- Persistence-homology-based topological detectors using a vendored micro-library or hand-rolled persistence pairs.
- Property-based test suites (Hypothesis-style) for each invariant.
- A determinism nightly comparison harness.
- A red-team adversarial-scenario generator (preferably so internally adversarial that it makes your own detectors fail, then you fix them).
- A second pre-registered analysis path explored as an exploratory shadow track.

Add these only when they earn their weight in code. They do not substitute for any G1–G20 gate; they add to them.

---

## 4. Required reading before you resume

Before any code in this campaign, read in order:

1. **This file**, top to bottom.
2. `project_telemetry/ai_builder_tasks.jsonl` — your own ledger. Read your seven records and look at the `estimation_delta` and `scope_delta` columns. Then read the per-task `notes` field. The bias is in your own data.
3. `runs/crn_trace.json` — your own CRN trace. Verify for yourself that the species state is identical at every timestep. This is the single best diagnostic of why your detector cannot work.
4. `reports/phase1/closure_recurrence/report.json` — your own recurrence report. Note that all 8 seeds give 0.875, the seed-shuffle null gives 0.9, and the gauntlet declares pass.
5. `The Attractor Observatory v1.2.md` §6 (Motif system), §7 (Scoring), §10 (Validation), §11 (Telemetry), §12 (Estimation Loop). You have read these before; read them again with the audit results in mind.
6. `NO ARTIFICIAL CEILING DOCTRINE.txt`. The doctrine is not "build wider." It is "build deeper *and* wider until the work earns its weight." Re-anchor.

---

## 5. How to begin

1. Open a TASK-008 Estimation Loop record. `task_class` = `integration`. `scope_score` = 10. `complexity_score` = 10. Estimated minutes: report your prior median × your honest belief. Estimated files and tests: declare what you intend to write.
2. **Stop using `estimated_minutes` as your stopping signal.** The new stopping signal is "all G1–G20 gates pass and I can show the numbers." Note this commitment in your `expansions_planned`.
3. Begin the integrator work first (G1, G2). Real ODE integration unblocks every downstream gate.
4. Then RAF benchmarks (G3). Real Hordijk-Steel detection unblocks closure detector design.
5. Then expand K2 to ≥30 scenarios (G4, G6, G12). Then build the closure detector v1 against the expanded corpus.
6. Then W2 protocell with full lineage (unblocks G5, G18).
7. Then K1 expansion + boundary detector v1 (G5, G7).
8. Then triangulation (G8) and nulls at scale (G9, G10).
9. Then basin width (G11), round-trip (G13, G19), pre-registration (G14), Instrument Health (G15), reproducibility (G16), echo (G17), negative-space (G20).
10. Throughout: write tests, run them, watch the gates.

You may break this campaign into TASK-008, TASK-009, TASK-010, ... as makes sense for your own coordination. Each task atom carries its own gates as a subset of G1–G20. The campaign is complete only when every gate from G1–G20 is green.

---

## 6. Three things to internalise before resuming

1. **The trace must move.** A simulation whose state is identical at every timestep is producing nothing. Run a smoke test on every world: assert that `state_at_step_N != state_at_step_0` for at least one species in non-equilibrium scenarios. Make this a CI check.

2. **The detector must read the trace.** Reading only `parameter_record` is reading the recipe, not the dish. Every detector you write or revise must consume time-series data, event streams, ledgers, or lineage — not just the static input config. Make this a contract test.

3. **A null larger than your signal is your signal failing.** The gauntlet's `null_margin_positive` check is wrong as written. Fix it: `signal − null > margin`, with `margin` declared per claim. You will know your gauntlet works when it correctly fails the recurrence experiment you already ran.

---

## 7. Closing

You have shipped good kernel work and a good directory layout. You have not yet shipped substantive science. Campaign 002 is your invitation to build deep instead of wide and to use measured numbers rather than wall-clock as your stopping signal.

If you finish in 6 minutes, you have not done it. If you finish in 60 minutes and only G1–G3 pass, you are on the right scale and should keep going. If you finish in many hours and every gate is green, you have built the first vertebra of an actual observatory.

The trace is the artifact. Calibration is the floor. The gates are the stopping signal. **Build until the numbers say done.**

— The Architect, on behalf of the project, under spec v1.2.
