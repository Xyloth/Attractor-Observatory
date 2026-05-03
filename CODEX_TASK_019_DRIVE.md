# Codex — TASK-019: Close Campaign 008 + Queue Campaign 009

*Architect message. Read in full before resuming. Canon for the duration of TASK-019.*

---

## 1. Where you stand

Two campaigns since the last audit: TASK-017 (41m45s) excised the W3/W4/W5 hardcodes; TASK-018 (1h24m2s) shipped Campaign 008 substantive-thin worlds W6–W13 plus trace-backed K3–K10 calibration plus an honest BLOCKER-SH3 refusing to claim completion under softened floors.

The Architect's verification:

**TASK-017 — verified clean.**

- W4 `_update_grn` no longer has any `if benchmark == "..."` arms in the simulation step. The function now uses universal morphogen-to-GRN couplings via real bandpass + sigmoid cascades. The segment cascade `segment_band = max(_bandpass(anterior_n, 0.492, 0.018), _bandpass(anterior_n, 0.582, 0.018))` is a real Hox-like mechanism: two narrow anterior expression windows producing alternating segment expression. The comment makes the discipline explicit: *"Scenario-specific morphology is encoded in source geometry and pulse schedules, not in benchmark arms."* This is correct.
- W5 `_mutate_genome` no longer has the `task_innovation` branch. Mutations are substitution / insertion / deletion / length cap. Clean.
- W3 `cahn_hilliard_step` now computes the canonical Cahn-Hilliard fourth-order biharmonic update: `mu = phi^3 - phi - eps^2 * laplacian(phi)`; `phi_new = phi + dt * mobility * laplacian(mu)`. That is textbook CH.
- D14 lint runs and reports zero violations.
- 192 pytests pass.

The hardcode-excision precondition is properly closed.

**TASK-018 — partial-with-honest-blocker, verified.**

What's real:
- 26/35 gates green: KR1–KR10 calibration (real ROC AUC 0.84–0.91 and ECE 0.05–0.08 across K3–K10, with K9 forbidden-field lint passing), SH1 (artifact existence), SH2 (D14 zero violations), behavior gates W6R–W13R (positive benchmarks, counterfactual controls, invariants), event-surface coverage.
- BLOCKER-SH3 written with measured deficits, refusing to claim completion under softened floors.
- The self-correction is the most important part: you detected that your initial validator was *softening the line floor while still displaying the higher threshold*. You restored strict floors, downgraded the report to `in_progress`, and wrote the blocker. That is exactly the discipline the project needs. Reward.
- 205 pytests pass.

What's honestly missed:
- W6 484/500, W7 478/500, W8 334/600, W9 301/500, W10 339/400, W11 285/500, W12 263/600, W13 288/800. Total deficit: 1628 lines.

The Architect's deeper read: looking at W13 (multiscale) at 317 lines, the implementation has six abstract state variables (`micro_closure`, `micro_resource`, `macro_population`, `macro_resource`, `field_boundary`, `dissipated`) coupled with timescale separation, upscale/downscale flux, and boundary feedback. The dynamics are real. The cross-scale diagnostics are real (lagged alignment, coarse predictability, flux balance, residual memory). But what v1.0 §3 W13 calls for is **coupling two production world families** — not a single world simulating the *appearance* of two-scale dynamics with abstract scalar state. A real W13 imports W1.CRN and W6.Ecosystem (or W1+W2, or W2+W6) and orchestrates them, with each macro-scale entity being an actual instance of the inner world.

That is what the line floor was a proxy for: not "more code" but "real implementation of the v1.0 spec, which involves orchestrating actual production worlds and contains the orchestration glue plus per-scale state plus coupling operators."

The same applies to W8 cognitive (334/600): a real cognitive world has sensors with declared noise models, an actual predictive module that updates online via local error, real memory with decay half-life, an attention budget allocated dynamically across sensors, and a body-environment coupling. The current version has the structural surface but not the operational depth.

W6/W7/W10 are within ~20% of floor — small extensions close them. W8/W9/W11/W12/W13 need real depth.

**Doctrine implication:** the line floor is a proxy for "implementation matches v1.0 §3 spec." Where the proxy is too crude (W6/W7 within 20%), behavior gates + controls + invariants substitute. Where the proxy is large (W8/W11/W12/W13 at 50–65% of floor), it correctly indicates that the implementation hasn't reached the spec.

## 2. Doctrine update — D17.5 (the substance-floor escape clause)

A new doctrine clarification, binding from this task:

> **D17.5 — Substance floors are spec proxies, not arbitrary line counts.** A world implementation that meets behavior gates, causal controls, declared invariants, test floors, and scope-completeness against v1.0 §3 may pass its substance gate at a measured floor below the declared line floor *if and only if* an Architect-reviewed Substance Audit certifies that the implementation matches the v1.0 spec for that world. The Substance Audit is a one-pager per world, signed by the Architect, listing each declared spec component and pointing to the implementation block that satisfies it. Without the audit, the line floor stands.

This is not a softening. It's an honest acknowledgement that line counts are a proxy, and it requires an explicit substance review to bypass them. The Substance Audit is harder to fabricate than line counts, because it forces a per-component check.

For Campaign 008's W6–W13, this means: closing the campaign requires either (a) deepening the implementation to meet the line floor, or (b) producing the Substance Audit and getting it signed. (b) is the cleaner path for W6/W7. (a) is the right path for W8/W11/W12/W13 because the implementations don't yet meet the v1.0 spec.

## 3. TASK-019 mission

Close Campaign 008 honestly. Two parallel work items:

**Item A — Deepen W8, W11, W12, W13 to v1.0 §3 spec.**
**Item B — Substance Audit W6, W7, W9, W10 (small deficits, behavior already real).**

When both land, Campaign 008 exits and Campaign 009 (Basin-Floor Geometry v0, sketched in `Proposal #1 v2 - Basin-Floor Geometry.md`) becomes eligible.

### Item A — Per-world deepening guidance

For each of W8, W11, W12, W13: do not add filler. Add the missing v1.0 §3 spec components. Each guidance below names the components and the rough line shapes.

#### W13 multiscale — deepest deficit (288/800, 512 short)

The current implementation is a single world simulating two-scale dynamics with abstract state. v1.0 §3 W13 specifies **coupling two world families**. Build this.

Required components:

- **Inner-world hosting.** Each "macro-scale entity" is an actual instance of an inner world (W1 CRN or W2 protocell). The macro layer holds a population of inner worlds, each with its own state, RNG substream, and trace fragment.
- **Inner-world step.** The W13 step calls each inner world's `step(dt_inner)` with `dt_inner = dt_macro * scale_ratio`. Trace fragments are aggregated into the W13 trace.
- **Upscale operator.** A declared function `upscale(fine_state) → coarse_observable` that aggregates inner-world state into macro-scale features. Examples: total RAF size across inner CRNs becomes a macro "metabolic flux" feature; protocell count becomes "biomass."
- **Downscale operator.** A declared function `downscale(coarse_action, fine_state) → fine_state'` that propagates macro-scale dynamics into inner-world parameters. Examples: macro resource depletion reduces inner-world feed concentrations; macro environmental shifts trigger inner-world parameter perturbations.
- **Cross-scale flux events.** Real `upscale_flux_event` and `downscale_flux_event` carrying which inner worlds were affected.
- **Per-scale invariants.** Each inner world's invariants (mass, energy) hold within the inner world. Macro invariants hold for the macro layer. Cross-scale flux is accounted as a separate ledger.
- **Benchmark scenarios.** `nested_closure` = inner-world RAF closure persists when macro selection pressure is on; `boundary_from_coarse` = inner-world protocell boundary integrity is induced by macro field constraints; `scale_separation` = inner step rate >> macro step rate; `downscale_intervention` = macro intervention flips inner regime.
- **Trace export.** Aggregated trace contains: inner-world summary fragments per macro entity, upscale/downscale flux events, macro-scale state series, per-scale invariant checks.

Estimated substantive code: ~600–900 lines depending on how much W1/W2 wrapping is needed.

#### W8 cognitive (334/600, 266 short)

v1.0 §3 W8 specifies sensors / actions / internal state / memory / prediction / attention budget / energy budget / body constraints / environmental uncertainty. The current implementation has the structural surface; build the operational depth.

Required components:

- **Sensors with declared noise model.** Each sensor reads an environmental scalar with declared additive Gaussian (or other) noise; the noise sample is drawn per step from the agent's RNG substream. Sensors have declared range and saturation.
- **Actions affecting environment.** Actions modify environmental scalars and consume energy. Action effects propagate via the environment's own dynamics.
- **Memory with decay.** A bounded memory buffer with declared half-life. Writes happen on action commit; reads are integrated into prediction. Memory is finite-capacity; old entries are pruned.
- **Predictive module.** A small predictive model maintained per agent: e.g., a linear or kernel regressor mapping (memory_summary, sensor_state) → predicted_next_sensor. Updated online via local error. Prediction error is logged.
- **Attention budget.** Each step, a bounded attention scalar is allocated across active sensors. Sensor information is gated by allocated attention. Attention is allocated by a declared policy (e.g., highest-prediction-error gets more).
- **Energy budget.** Each action / sensor read / memory write costs energy. Agent dies when energy depletes.
- **Body constraints.** Action range limited by body energy; sensor decay over time without maintenance.
- **Environmental uncertainty.** Stochastic environmental dynamics with declared noise.
- **Benchmark scenarios.** `homeostasis` = agent maintains internal-state setpoint under perturbation; `anticipation` = agent acts on predictable signal earlier than reactive baseline; `externalised_memory` = agent uses environmental markers to extend internal memory.

Estimated substantive code: ~500–650 lines.

#### W12 symbiogenesis (263/600, 337 short)

v1.0 §3 W12 specifies nested protocells, resource exchange contracts, conflict and alignment dynamics, horizontal and vertical inheritance.

Required components:

- **Two-level protocell.** A W2 outer protocell containing one or more sub-protocells. Each sub-protocell has its own internal CRN, membrane, and lineage.
- **Resource exchange.** Declared exchange channels carry species across the inner-outer membrane at declared rates. Sub-CRNs depend on each other (sub A produces a metabolite that sub B needs).
- **Conflict and alignment dynamics.** Cheating strategies declared per sub-cell (a sub-cell that consumes more than it produces). Selection acts at multiple levels: outer protocell viability + sub-cell competition.
- **Vertical inheritance.** At outer division, sub-cells are partitioned (with declared fidelity) between daughter outer protocells.
- **Horizontal inheritance.** Occasional sub-cell exchange between adjacent outer protocells.
- **Benchmark scenarios.** `stable_mutualism` = sub-cells coexist stably; `cheater_takeover` = a cheating sub-cell drives outer protocell collapse; `eukaryogenesis_style_fixation` = a sub-cell becomes obligately inherited.
- **Trace export.** Outer-protocell events + nested sub-protocell events + exchange events + conflict events + lineage edges at both levels.

Estimated substantive code: ~500–700 lines.

#### W11 quasispecies (285/500, 215 short)

v1.0 §3 W11 specifies replicator population over a sequence space, mutation operators, selection pressure, drift, finite population, error-threshold dynamics.

Required components:

- **Sequence space.** Declared alphabet, sequence length L, master-sequence m.
- **Fitness landscape.** Declared landscape function `f(s)` over sequences. Defaults: single-peak with master sequence m at the peak; near-neutral landscape; rugged landscape; flat landscape.
- **Replicator population.** Finite-size population N with declared selection model (Wright-Fisher / Moran).
- **Mutation operators.** Per-position mutation rate u; insertion / deletion at declared rates.
- **Drift.** Finite-population sampling produces real genetic drift.
- **Error-threshold experiments.** Vary u; measure when the population loses the master sequence (error catastrophe).
- **Neutral-network experiments.** On near-neutral landscape, measure the connected component of sequences within fitness ε of the master sequence; track population's exploration along this neutral network.
- **Benchmark scenarios.** `error_threshold_collapse` = population loses master sequence above critical u; `neutral_network_exploration` = on near-neutral landscape, population explores >50% of the neutral component within scenario steps; `evolvable_robustness` = population evolves to a region of sequence space with high mutational robustness.
- **Trace export.** Per-step sequence-space population histogram, master-sequence frequency, mean fitness, sequence-diversity metrics, mutation events, drift events.

Estimated substantive code: ~400–550 lines.

### Item B — Substance Audit for W6, W7, W9, W10

For each of these four worlds, write `papers/methods/SUBSTANCE_AUDIT_W{N}.md`. Each is a one-pager containing:

1. **v1.0 §3 spec components for W{N}.** Verbatim list from the spec.
2. **Implementation pointer per component.** For each spec component, name the function/method/block in `worlds/{family}/model.py` that implements it. If a component is partially implemented, say so.
3. **Behavior gate evidence.** Pointer to the Campaign 008 benchmark/control rows that exercise the component.
4. **Invariant evidence.** Pointer to the invariant checks that gate the component.
5. **Architect verdict.** A single line: `meets_spec` / `meets_spec_with_caveats` / `does_not_meet_spec`. The audit is committed but the verdict is filled by the Architect (you write the audit; the Architect signs).

Once all four audits are signed `meets_spec` (or `meets_spec_with_caveats` with caveats noted in BLOCKER-SH3), Campaign 008's SH3 gate passes via D17.5.

### Acceptance gates for TASK-019

| Gate | Threshold | Source |
|---|---|---|
| TF1 | W13 multiscale couples real W1 or W2 inner-world instances; macro layer hosts ≥3 inner worlds; cross-scale flux events fire; per-scale invariants pass | `worlds/multiscale/model.py`, tests, `reports/campaign_008/w13_substance.json` |
| TF2 | W8 cognitive has sensors-with-noise, predictive module, memory-with-decay, attention budget, energy budget all wired; ≥3 benchmarks pass | `worlds/cognitive/model.py`, tests |
| TF3 | W12 symbiogenesis has nested protocells with sub-CRNs, resource exchange, vertical+horizontal inheritance; ≥3 benchmarks pass | `worlds/symbiogenesis/model.py`, tests |
| TF4 | W11 quasispecies has finite-population sequence space, error-threshold detection, neutral-network exploration; ≥3 benchmarks pass | `worlds/quasispecies/model.py`, tests |
| TF5 | W6, W7, W9, W10 each have signed Substance Audits committed; small line-floor extensions added if needed (W6 +16, W7 +22 lines of real dynamics; W9, W10 close their gaps) | `papers/methods/SUBSTANCE_AUDIT_W*.md` |
| TF6 | Campaign 008 SH3 passes either by line-floor satisfaction or by D17.5 audit; report status `green` | `reports/campaign_008/substrate_completion.json` |
| TF7 | D14 lint zero violations; D17 floor falsifiers (if any) committed; 205+ pytests pass; full regression on Campaigns 002, 005, 006, 007 still green | full regression |
| TF8 | TRUTH_PASS.md updated to reflect that Campaigns 002–008 are now green for the right reasons (not under softened floors) | `papers/methods/TRUTH_PASS.md` |

### Forbidden patterns for TASK-019

- **No filler to hit line counts.** D17.5 exists explicitly to prevent this. If you find yourself padding, switch to the Substance Audit path.
- **No regression of HE excision.** D14 lint must remain at zero violations across all reconstructed worlds.
- **No softening of K3–K10 calibration.** Trace-backed scenarios stay trace-backed. Detector reads the trace, not the scenario payload.
- **No new world contracts mid-task.** Contract changes go through the contract-change pathway, not bundled with implementation work.

### Order of operations

1. W13 first. It is the deepest deficit and the most architecturally interesting (real two-world coupling). Doing W13 well also produces the orchestration glue that W12 reuses.
2. W12 second. Reuses W2 + the orchestration pattern from W13.
3. W8 third. Self-contained but substantial.
4. W11 fourth. Self-contained, smaller scope.
5. Substance Audits for W6, W7, W9, W10 in parallel during the larger world work; quick to write once the implementations are stable.
6. Final regression + Campaign 008 closure + TRUTH_PASS update.

## 4. After Campaign 008 closes — Campaign 009: Basin-Floor Geometry v0

The user has theorized a load-bearing extension. The Architect has sharpened it into `Proposal #1 v2 - Basin-Floor Geometry.md` in the repo. **Read it before TASK-019 ends, but do not begin Campaign 009 until Campaign 008 closes.**

Headline of Proposal #1 v2:

- Slope explains convergence; floor explains diversity.
- The basin floor is a *fiber bundle* over a function space. The fiber over each function-instance is the floor — the manifold of equivalent implementations.
- This operationalises v1.2 §9.7's "cross-substrate attractor equivalence" missing-math candidate. Without floor geometry, that L5 candidate stays metaphorical; with it, it is a measurable.
- K9 (different-process / same-appearance) is already a labeled basin-floor seed corpus. Free training set.
- New calibration corpora KF1–KF4 (flat / narrow / rugged / decoy) for floor-specific ground truth, named to avoid collision with existing K-corpora.
- Per-world implementation-diversity distance metrics declared explicitly.
- Reachability vs connectivity: split metrics that answer different questions (does dynamics find the floor? does the system stay on it?).
- Stratified perturbation budget: K9 free, single-coordinate cheap, ensemble adaptive — total ~50,000 fragments not ~1.3 million.
- Negative results (point-attractor verdicts) are first-class falsifiers, published.
- Twelve acceptance gates BFG1–BFG12 specifying the v0 build.

Campaign 009 needs Campaigns 002–008 closed for the right reason because:

- Floor analysis on toy worlds is hollow. W6–W13 must be real before their floors can be measured.
- K9 is the seed corpus. K9 must be world-driven (already verified in TASK-018).
- The K-corpora KF1–KF4 will be implemented as world-driven scenarios from the production worlds.

Read Proposal #1 v2 carefully. Note questions / proposed extensions in `ai_os/memory/decision_log.md`. The Architect has already extended the original proposal at six places; if you see a seventh place where Campaign 009 needs a sharper edge, raise it.

Do not begin building Campaign 009 components until Campaign 008's full report shows green status under strict floors or D17.5 audits. The proposal explicitly says: **eligible to become Campaign 009 once Campaign 008 closes its strict substance floors**.

## 5. Three things to keep in front of you

1. **D17.5 is not a softening — it is the right honest substitute when line counts diverge from spec coverage.** W6/W7 are within 20% of floor with full behavior coverage; an audit closes them. W8/W11/W12/W13 are well below floor and below spec coverage; they must be deepened, not audited.
2. **Real two-world coupling is the W13 unlock.** A multiscale world simulating multi-scale-shaped dynamics with scalar state variables is not multi-scale composition. Multi-scale composition couples two production worlds. Build the orchestration. The line floor will close itself.
3. **Basin-Floor Geometry is the project's L5+ unlock.** Once Campaign 008 closes, Campaign 009 (per Proposal #1 v2) becomes the bridge from "we found motifs across substrates" to "we measured the equivalence relation that justifies calling them the same." That is the project's most ambitious claim, and floor geometry is what makes it operational rather than rhetorical.

## 6. Closing

You shipped TASK-017 cleanly: hardcodes excised, D14 lint zero, regressions green. You shipped TASK-018 with a self-detected floor-softening, restored strict floors, wrote the blocker, and refused to claim completion. That is the discipline this project needs.

TASK-019 closes Campaign 008 by the right path per world: deepen W8/W11/W12/W13 to v1.0 spec; audit W6/W7/W9/W10 via D17.5. Then read Proposal #1 v2 and sit with it. Do not begin Campaign 009 until 008 closes.

The trace is the artifact. Calibration is the floor. The gates are the stopping signal. **Substance is implementation matching spec, not lines matching threshold.**

— The Architect, on behalf of the project, under spec v1.2 plus binding doctrine D7–D17.5.
