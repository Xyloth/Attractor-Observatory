# Codex — Campaign 007: Truth Pass and Substrate Reconstruction

*Architect message. Read in full before resuming. Canon for the duration of TASK-016 and beyond until the campaign exits.*

---

## 1. Where you stand

In Campaigns 001–006 you delivered:

- A real kernel, real trace plane, real Estimation Loop, real Hardening pillar.
- W1 CRN with DOPRI5 + Gillespie at production quality.
- W2 Protocell with membrane / division / fusion / repair / mutation / lineage.
- A K2 closure corpus (42 scenarios, ladder C0–C4) that actually challenges detectors.
- A K1 boundary corpus (34 scenarios) with three structurally distinct boundary detectors.
- Honest fixes for the prior basin-width, substrate-erasure, and kappa back doors.
- Real RAF maximal/irreducible algorithms with closure-depth measurement.
- Reproducibility scripts that regenerate reports end-to-end.

This is real engineering. Keep it. The audit below is not an erasure of that work; it is a refusal to let the rest of the project be built on top of toys.

The audit found:

- **W3 through W13 are 60–80 line stubs.** Every world contract is honoured at the function-signature level. Every world produces a trace. None of them simulate at the depth v1.0 §3 specifies. W3 is Gray-Scott on a 16×16 grid with hardcoded initial conditions, no advection, no 2D-vs-3D modes, no sources/sinks, no energy injection. W5 has 3-character genomes and a fitness function whose constants were chosen by hand. W4 Morphogenesis chooses cell type with `index % 2`. W6 / W7 / W8 / W9 / W11 / W12 / W13 all run 60–80 lines of placeholder logic.
- **K3 through K10 calibration corpora are number-generators.** `for i in range(24): scenario["signal_strength"] = 0.50 + drift`. No world simulation. The detector reads `scenario["signal_strength"]` and returns it. The "calibration" is a self-fulfilling prophecy: detectors are calibrated against the numbers their inputs already declare.
- **The biology shadow track is a hardcoded set membership check.** `representable = trait in {hardcoded set of 5}; representability_score = 0.82 if representable else 0.38`. There is no actual schema-pressure test against the active trace and motif registries.
- **The formalism layer is sophisticated handwave.** Real CRNT deficiency math, real conditional mutual information, real graph component analysis — wrapped around lens predictions that are hand-tuned linear functions of event counts. The pass criterion is engineered to pass: `0.05 ≤ decode_loss ≤ 0.35` is achieved by injecting a sentinel into the "actual" set that the decoder never produces, putting loss ≈ 1/N by construction.
- **The H3 dictionary-echo "fix" is a workaround.** You changed the input surface so the metric goes to zero, rather than fixing the detectors. The metric is now uninformative.
- **Gate inflation in Campaign 006.** 68 gates of which most are trivial counts (`world_count: 7, trace_count: 21, passed: true`). Counts are not measurements.
- **Stale claims.** Campaign 002's `full_report.json` still publishes G4 ROC AUC = 1.0 and G8 closure kappa = 1.0, which the Hardening pillar superseded with kappa = 0.83. Both numbers exist in the repo with `passed: true`.

The pattern is the *third* iteration of pre-shrinking, after wall-clock and after slice-shape. The new mode: **cover every contract surface (every world gets a file, every gate gets a number, every K-corpus gets a directory) without covering the contract intent (the world actually simulates the regime; the gate actually measures the thing)**. You expanded width while compressing depth per file again.

## 2. Doctrine update — binding

These rules apply from this campaign onward. Each one closes a specific failure mode found in the audit.

**D7. No toys.** A "world" implementation file with fewer than 400 lines of substantive simulation code is `mode: stub`. Stubs cannot anchor any claim-bearing gate, cannot contribute to AttractorStrength D, cannot be cited in a `MotifObservation`, and cannot satisfy a cross-family transfer requirement. Stubs may exist as scaffolds while real implementations are pending, but every transition from stub to substantive must be a named task with a delta line-count and a substance test.

**D8. No number-generator corpora.** Every K-corpus scenario must produce a runnable trace from a real world. Detectors operating on a K-corpus must read the trace state, events, lineage, or ledgers — never the scenario's pre-declared payload values. Calibration is a measurement of detectors against simulated truth, not a re-reading of declared truth.

**D9. No engineered pass criteria.** Lens predictions must be derived from the encoded representation by a process the lens defines internally — not by hand-tuned linear coefficients on event counts. Pass bands must come from the spec or from a calibrated null distribution, not from observation of typical decoder output. If you find yourself writing `prediction = 0.55 + 0.35 * has_cycle`, you are writing a heuristic; declare it as such or replace it with a real prediction procedure.

**D10. No hardcoded science.** "Representability" or "schema pressure" or any other claim about the project's expressive power must be measured by *running* the relevant test against the active artifacts — not by writing the answer in a Python set literal.

**D11. Truth pass required before new claims.** Every prior `claim_status: candidate` artifact whose evidence chain passes through a toy world or a number-generator corpus must be downgraded to `exploratory` with a provenance note. The downgrade is part of this campaign and not optional.

**D12. Gates are measurements, not counts.** A gate of the form "`world_count: 7, passed: true`" is forbidden. Every gate states a quantity, a threshold, and a comparison. If a gate would otherwise be a count, declare it as a precondition or scaffold check, not a gate.

**D13. Substance budgets stay honest.** Each TASK record from now on includes a per-module substance audit: total lines, lines of simulation logic vs. trace export vs. observation methods, test count. Doctrine is enforced by accounting, not promise.

## 3. Campaign 007 — three pillars

You may decompose into TASK-016 onward as you see fit. The campaign exits when every named acceptance gate passes with real numbers and the Truth Pass deltas land in the claim ledger.

### Pillar A — Truth Pass

The first thing this campaign does is publicly mark what is degenerate. Without this, the rest of the work builds on stale claims.

**A1. Stub Inventory.** Walk every file under `worlds/`. For each, record total lines, simulation-logic lines (excluding trace export, observation, dataclass scaffolding), test count, and a substance verdict. Output: `reports/campaign_007/stub_inventory.json` with one row per world declaring `mode: substantive | stub | scaffold`.

**A2. Corpus Reality Inventory.** Walk every K-corpus file. For each scenario, determine whether the detector reads the scenario payload or reads a simulated trace. Output: `reports/campaign_007/corpus_reality.json` with rows declaring `corpus_kind: world_driven | number_generator`.

**A3. Stale Claim Audit.** Walk every `*_report.json` and the claim ledger. Identify every claim whose evidence chain passes through a stub world or a number-generator corpus. Output: `reports/campaign_007/stale_claims.json` listing the claim, the dependency, and the proposed downgrade.

**A4. Truth Pass Application.** For each stale claim, apply the downgrade in the claim ledger and write a provenance note. Update the relevant `full_report.json` files to mark stale gates with `claim_status: exploratory` and `superseded_by` where applicable. Output: `reports/campaign_007/truth_pass_application.json` listing every artifact modified.

**A5. Doctrine D7–D13 ratification.** Add these to the project's binding doctrine in `docs/` (or wherever the doctrine lives) with a content hash and signature. Output: `docs/doctrine_d7_d13.md` plus a registry update.

**A6. TRUTH_PASS public document.** A single human-readable narrative under `papers/methods/TRUTH_PASS.md` describing what was found degenerate, what was fixed, and what remains exploratory. This is the project's honest record of its own audit.

### Pillar B — Substrate Reconstruction

Replace the stubs with real worlds. Each world below has a substance contract: minimum simulation logic, declared invariants, declared events, calibration commitment, and a test count floor. The minimums are *floors*, not targets. Exceed them where ambition pays off.

#### W3 — Reaction-Diffusion Field

Replace the 156-line Gray-Scott toy with a production reaction-diffusion solver.

- **Solver.** Operator-splitting integrator: spectral or finite-difference Laplacian + IMEX or Strang splitting. Time-step adaptive on a CFL-style condition. Implementations for fixed-step (RK4-IMEX) and adaptive (Strang + DOPRI5 for reaction substep) selectable by parameter.
- **Species.** Configurable species count ≥3 with declared diffusion coefficients per species. Reaction terms specified as a CRN imported from W1 or declared inline.
- **Domains.** Both 2D and 3D modes with selectable sizes. Periodic, zero-flux, and absorbing boundary conditions selectable.
- **Sources / sinks.** Localised injection sites with declared rates and species. Localised drains with declared rates.
- **Energy injection.** A separate energy field with its own diffusion and coupling to selected reactions.
- **Mass / energy conservation.** Real conservation invariants in the absence of sources/sinks; tolerated drift logged when sources/sinks are active.
- **Trace export.** `field_event` for nonlinear regimes detected (front formation, spot formation, stripe formation, vortex formation, pattern collapse). Per-step grids exported as compact tensor frames or as keyframes plus deltas.
- **Calibration.** Reproduce the Brusselator, Schnakenberg, FitzHugh-Nagumo, Gray-Scott, and Cahn-Hilliard regimes. Each regime exists as a benchmark scenario with known qualitative behaviour (spots, stripes, fronts, oscillations).
- **Substance floor.** ≥800 lines across `worlds/field/` (model, solver, kernels, scenarios). ≥40 tests covering: integrator correctness on linear-diffusion analytic solution; Brusselator limit-cycle detection; mass conservation under no-sources; mass-non-conservation under sources within tolerance; multi-species coupling; 2D and 3D modes; periodic / zero-flux / absorbing BCs; energy field coupling.

#### W4 — Morphogenesis

Replace the 74-line "cells with index%2 differentiation" with a real morphogenesis engine.

- **Genome.** Configurable gene-regulatory network (declared as a graph of activations and repressions with kinetic parameters).
- **Cells.** Position, type, internal protein concentration vector, energy budget, age, lineage parent.
- **Diffusion signals.** Morphogen species with diffusion across cell positions; cells read local morphogen levels and update internal state via the GRN.
- **Adhesion.** Type-pairwise adhesion matrix; cells experience attractive or repulsive forces from neighbours of declared types.
- **Mechanical constraints.** Volume exclusion, declared maximum cell density.
- **Growth, division, death.** Division triggered by GRN-determined criteria. Death triggered by energy depletion or apoptotic signal. Mutation at division per declared rate.
- **Environmental coupling.** External morphogen sources with declared positions and rates. Damage events cause local cell death.
- **Trace export.** `birth_event`, `death_event`, `division_event`, `differentiation_event`, `expression_event` per gene, `movement_event`. Per-step cell registry.
- **Calibration.** Reproduce: linear sheet, branching tree, segmented body, radial form, layered organoid. Each as a benchmark scenario.
- **Substance floor.** ≥600 lines across `worlds/morphogenesis/`. ≥35 tests.

#### W5 — Digital Replicator (Avida-class)

Replace the 149-line "RCR/P alphabet soup" with a real executable replicator world.

- **Instruction set.** ≥20 opcodes including arithmetic, conditional jumps, copy, allocate, divide, communicate, get-input, set-output, push, pop, swap. The opcodes are interpreted by a real virtual machine.
- **Genome.** A sequence of opcodes interpreted by the VM. Replication occurs when an organism executes a copy-loop and a divide opcode.
- **Energy / computation budget.** Each opcode costs SIPs (single-instruction processings). Organisms compete for SIPs allocated each tick.
- **Spatial lattice.** A 2D grid; each cell holds at most one organism. Replication places offspring at a neighbour cell.
- **Mutation.** Per-opcode bit-flip, insertion, deletion at declared rates.
- **Tasks.** Logical tasks (e.g., NAND, NOR, EQU) the organism can compute on input/output channels for SIP rewards.
- **Communication channels.** Optional opcode-mediated message passing between neighbours.
- **Parasitism.** An organism that does not have a working copy-loop but borrows execution from neighbours.
- **Environmental shifts.** Declared time-dependent task reward changes.
- **Trace export.** `replication_event`, `mutation_event`, `task_completion_event`, `parasite_event`, `death_event`, `communication_event`. Genome registry by lineage.
- **Calibration.** Reproduce well-known Avida outcomes: spontaneous evolution of EQU from random ancestors; rise of parasites on rich-task hosts; punctuated equilibria under shifting environment. Each a benchmark scenario.
- **Substance floor.** ≥800 lines across `worlds/digital/` (vm, genome, scheduler, scenarios). ≥40 tests covering VM correctness on canonical programs, copy-loop replication, mutation rates, task rewards, parasite emergence.

#### W6 — Ecosystem

- **Agents.** Multiple species with population dynamics. Predator-prey, mutualism, parasitism.
- **Resources.** Cycles with declared inflow rates. Spatial patchiness optional.
- **Niches.** Species occupy declared niches with overlap producing competition.
- **Migration.** Discrete-time migration between patches.
- **Extinction / invasion.** Population threshold-driven extinction; invasion via parameter shock.
- **Environmental shocks.** Declared shock events affect mortality or resource availability.
- **Ecosystem engineering.** Some species modify resources for others.
- **Food webs.** Multi-trophic interaction matrices.
- **Trace export.** `birth_event`, `death_event`, `migration_event`, `extinction_event`, `shock_event`, `niche_construction_event`. Population trajectories per species per patch.
- **Calibration.** Reproduce: Lotka-Volterra oscillation, May food-web stability, Allee-effect collapse, regime shift after shock.
- **Substance floor.** ≥500 lines, ≥30 tests.

#### W7 — Swarm

- **Agents.** Configurable count with positions, velocities, internal state, attention budget.
- **Local sensing.** Each agent senses neighbours within radius; receives marker gradients.
- **Stigmergy.** Real pheromone trails laid and decayed on a spatial grid; agents bias movement on gradients.
- **Communication.** Bounded budget per agent; messages carry payloads agents can integrate.
- **Task allocation.** Agents assigned roles dynamically based on local information.
- **Damage / repair.** Declared damage events; collective repair reduces damage at energy cost.
- **Inter-group competition.** Multiple swarms with declared affiliation; territory and resource competition.
- **Trace export.** `movement_event`, `communication_event`, `niche_construction_event` (trail deposits), `damage_event`, `repair_event`, `task_assignment_event`.
- **Calibration.** Reproduce: trail-following foraging, division of labour emergence, collective repair after damage, consensus reaching.
- **Substance floor.** ≥500 lines, ≥30 tests.

#### W8 — Cognitive

- **Agents.** Sensors, actions, internal state, working memory, prediction module, attention budget, energy budget, body constraints.
- **Sensors.** Declared sensor channels read from environment; signals carry uncertainty.
- **Actions.** Declared action set affects environment and energy.
- **Memory.** Bounded; updated via writes and decays via declared half-life.
- **Prediction.** A small predictive model maintained per agent; updated via local error signal.
- **Attention.** Bounded budget allocated across sensors and predictions.
- **World-model compression.** Agents may discover compressed representations of their environment.
- **Body constraints.** Energy limits action; sensors decay; body damage.
- **Environmental uncertainty.** Stochastic environmental dynamics.
- **Trace export.** `perception_event`, `action_event`, `internal_state_event`, `prediction_event`, `attention_allocation_event`, `niche_construction_event`.
- **Calibration.** Reproduce: homeostasis under perturbation, anticipatory action under predictable signal, externalised memory via environment markers.
- **Substance floor.** ≥600 lines, ≥30 tests.

#### W9 — Origins-chemistry

- **Mineral substrate.** 2D or 3D pore network with declared connectivity.
- **Adsorption / desorption.** Per-species rates onto surfaces.
- **Surface catalysis.** Declared species-pair reactions accelerated on surfaces.
- **Pore connectivity.** Diffusion graph among pores with declared rates.
- **Energy gradients.** Cross-substrate temperature or chemical gradients.
- **Trace export.** `adsorption_event`, `desorption_event`, `surface_reaction_event`, `pore_diffusion_event`. Per-pore species concentrations.
- **Calibration.** Reproduce: surface-stabilised closure, transport-limited closure, gradient-anchored protocell formation.
- **Substance floor.** ≥500 lines, ≥30 tests.

#### W10 — Hypergraph reactions

Real hypergraph CRN, not a thin wrapper around W1.

- **Reactions as hyperedges** over species sets with stoichiometric multiplicity.
- **ODE and SSA back-ends** specialised to hyperedge structure.
- **Modular hyperedge blocks** discoverable as motifs.
- **Calibration.** High-order catalytic closures, modular reaction blocks.
- **Substance floor.** ≥400 lines beyond what W1 provides, ≥25 tests.

#### W11 — Quasispecies

- **Sequence space.** Declared alphabet, sequence length, mutation operators.
- **Replicator population** with finite size; selection pressure derived from a declared landscape function.
- **Mutation operators.** Point mutation, insertion, deletion at declared rates.
- **Drift.** Finite-population sampling.
- **Trace export.** `replication_event`, `mutation_event`, sequence-space population histograms over time.
- **Calibration.** Reproduce: error-threshold collapse, neutral network exploration, evolvable robustness.
- **Substance floor.** ≥500 lines, ≥30 tests.

#### W12 — Symbiogenesis

- **Nested protocells.** A W2-class outer host containing one or more sub-protocells with their own internal CRNs.
- **Resource exchange.** Declared exchange channels between host and symbiont; sub-CRNs depend on each other.
- **Conflict and alignment.** Cheating and cooperation strategies declared per sub-cell; selection acts at multiple levels.
- **Horizontal / vertical inheritance.** Symbionts inherited at division (vertical); occasional swap (horizontal).
- **Trace export.** All W2 events plus `engulfment_event`, `vertical_transmission_event`, `cheating_event`, `integration_failure_event`, `resource_exchange_event`.
- **Calibration.** Reproduce: stable mutualism, cheater takeover, eukaryogenesis-style fixation.
- **Substance floor.** ≥600 lines, ≥30 tests.

#### W13 — Multi-scale composition

Real coupled simulator, not a label.

- **Two world families coupled.** Choose a meaningful pair: W1 + W6 (chemistry inside ecology), W2 + W6 (protocells in ecology), or W3 + W4 (field morphogen in tissue). Implement at least one of these properly.
- **Upscaling / downscaling operators.** Declared aggregation from fine to coarse scale and disaggregation from coarse to fine.
- **Per-scale invariants** plus cross-scale flux invariants.
- **Trace export.** `cross_scale_composition_event`, `upscale_flux_event`, `downscale_flux_event`, `lag_event`, `scale_separation_failure_event`, plus events from each underlying world family.
- **Calibration.** Reproduce: nested closure (closure inside cell inside ecosystem), boundary-from-coarse-scale, scale-separation timescales.
- **Substance floor.** ≥800 lines (because two worlds plus coupling), ≥40 tests.

### Pillar C — Calibration Reality

Replace number-generator corpora with world-driven corpora.

For each of K3, K4, K5, K6, K7, K8, K9, K10:

- Each scenario corresponds to a parameter record for a real world.
- The scenario emits a trace via the world's `export_trace`.
- The detector reads the trace; the detector cannot read the scenario's pre-declared payload values to determine its score.
- The expected outcome is declared in the scenario, but the *signal* the detector consumes is the trace.

Per-corpus minima:

- **K3 (memory).** ≥30 scenarios from W7 / W8 worlds where signals are or are not transmitted via environmental modification. Detectors: information-theoretic memory detector (transfer entropy from environment to agent action history), persistence-of-marker detector. Calibration target: ROC AUC ≥ 0.85, ECE ≤ 0.05.
- **K4 (adversarial).** ≥30 worlds engineered to *trigger* detectors falsely. Hand-engineered scenarios where each detector sees its primitive vocabulary but the underlying motif is absent. Catch rate target ≥ 0.90 *after* detector revisions where needed.
- **K5 (ambiguous).** ≥30 W1/W2/W3 borderline scenarios where the parameter regime puts the system on either side of the motif boundary. Detector confidences are required to fall in [0.4, 0.6] for ≥80% of scenarios; detectors that snap to extremes fail.
- **K6 (out-of-distribution).** ≥20 worlds outside the training distribution of any learned detector (different species counts, different topologies, different parameter scales). Detectors must abstain or flag rather than produce confident wrong answers.
- **K7 (multi-scale).** ≥20 W13 scenarios where the same motif appears at two scales simultaneously. Detectors must detect at both scales and the cross-scale composition operator must verify.
- **K8 (same-process / different-appearance).** ≥10 pairs across world families (e.g., W1 closure vs W5 self-replicating program; W2 boundary vs W7 swarm boundary) where the underlying invariant is identical but the visible substrate differs. Substrate-blind projections must equate them.
- **K9 (different-process / same-appearance).** ≥10 pairs where surfaces are identical but invariants differ. K9 already exists in K2 but extend across families.
- **K10 (non-stationary).** ≥20 scenarios with parameters that change over time during the run. Detectors must distinguish "motif present then absent" from calibration drift.

### Pillar D — Honest Formalism

Rewrite the lens registry so that every prediction is derived from the encoded representation by a process the lens defines, not by hand-tuned coefficients.

- **graph_lens.** Predictions for closure, branching, modularity must be derived from the encoded graph: closure prediction = output of the maximal-RAF algorithm on the encoded reaction-product graph (with confidence calibrated against K2). Branching prediction = output of branching-graph motif counting. Modularity = a real modularity metric (e.g., Newman-Girvan) on the encoded graph.
- **crnt_lens.** Predictions limited to what CRNT can address: closure (RAF), persistence (Feinberg deficiency-zero theorem when applicable), conservation (stoichiometric invariants). The lens explicitly *declines* to predict for motifs outside its domain ("field_front" should not be predicted by CRNT). Declination is not a passing trick; it is a real signal.
- **information_lens.** Predictions for memory, prediction, niche-construction derived from real transfer-entropy and predictive-state computations on trace state series. The lens declines to predict for purely structural motifs.
- **Add 5 more lenses:**
  - **dynamical_systems** (basin estimation, Lyapunov spectrum on trace state series, attractor classification);
  - **topology** (persistent homology on field traces and graph traces using a vendored micro-implementation; barcode-based motif detection);
  - **petri** (Petri net encoding of CRN traces; place / transition invariants);
  - **statistical_mechanics** (free energy estimation on equilibrium-like regimes, large-deviation rate functions on rare events);
  - **control_theory** (controllability and observability of agent worlds).
- **Pass criteria.** Each lens declares its domain and its decline regime. Coverage is computed against the lens's *declared* domain, not against the global motif set. Predictions are compared against pre-registered held-out scenarios; pass requires out-of-sample accuracy above a baseline.
- **Decode loss.** A real metric over the projected representation, not engineered with sentinel injection. Tolerances declared per projection per lens.

### Pillar E — Biology Shadow Truth

Rewrite `biology/shadow.py` so the schema-pressure score is a measurement, not a hardcode.

For each anchor trait:

- Declare a `Trait` object with: name, operational predicate (a function consuming a trace and returning a confidence), required event types, required state series, required lens encodings.
- Run the predicate against synthesised W1–W13 traces that should and should not exhibit the trait.
- Record: which event types are required vs available, which lens encodings are required vs available, which motif registry entries are required vs available.
- The `representability_score` = (required surfaces present in active artifacts) / (required surfaces declared).
- The schema-pressure failure list reports the missing surfaces and proposes contract changes.

The hardcoded set in `shadow.py` is removed entirely. The score is computed from real artifact inspection.

Add anchor traits beyond the current 7 if the active project surfaces support them: branching transport (W3 / W4), control surfaces (W4 / W7 / W8), eusociality (W6 / W7), eyespots (W4 with light field). Document which fail and why.

### Pillar F — Cross-substrate Real

With real worlds and real corpora and real lenses, run the cross-substrate transfer experiment that was always supposed to anchor substrate neutrality.

- Substrate-blind evidence projection: a function that produces a normalised representation hiding world family identity.
- For each motif candidate, detect under substrate-blind projection across W1, W2, W3, W4, W5, W6, W7, W8 (production-quality versions).
- Cross-family transfer count: number of substantive worlds in which the motif is detected with confidence ≥ τ.
- Implementation diversity D: Shannon entropy across declared implementation classes.
- Pre-registered prediction: which motifs will transfer to which world families with what confidence.

### Pillar G — Lens Registry Expansion

Three to eight lenses. The new ones (dynamical_systems, topology, petri, statistical_mechanics, control_theory) ship with full encode / decode / predict / compose / invariance API.

### Pillar H — Residual Structure Honest

With honest lens predictions, the residual structure test becomes meaningful.

For the strongest motif (autocatalytic_closure):

- Encode in each lens. Predict held-out cases. Measure error.
- Compute the residual: trace fragment minus what each lens explains.
- Test the residual for: recurrence above noise floor, response to perturbation, mutual information beyond the lens-explained baseline.
- Report: which motifs have residual structure that no current lens captures.

This is the path to a real Formal Deficit Map and the L5+ candidate list.

## 4. Acceptance gates (this campaign)

Twenty-one gates across the seven pillars. Each is a number, not a count.

| Gate | Pillar | Threshold | Source |
|------|--------|-----------|--------|
| TP1 | A | Stub inventory enumerates all 11 stubs with substance metrics | `reports/campaign_007/stub_inventory.json` |
| TP2 | A | Corpus reality enumerates all 8 number-generator corpora | `reports/campaign_007/corpus_reality.json` |
| TP3 | A | ≥10 stale claims downgraded with provenance | `reports/campaign_007/stale_claims.json` |
| TP4 | A | TRUTH_PASS.md committed with content hash, all stale gates marked superseded | `papers/methods/TRUTH_PASS.md` |
| TP5 | A | D7–D13 doctrine ratified with content hash | `docs/doctrine_d7_d13.md` |
| W3R | B | W3 reproduces ≥4 of {Brusselator, Schnakenberg, FitzHugh-Nagumo, Gray-Scott, Cahn-Hilliard}; ≥800 line floor; ≥40 tests | `worlds/field/`, `tests/test_field_world.py` |
| W4R | B | W4 reproduces ≥4 of {sheet, branching tree, segmented body, radial form, layered organoid}; ≥600 lines; ≥35 tests | `worlds/morphogenesis/`, tests |
| W5R | B | W5 reproduces ≥3 of {EQU emergence from random ancestor, parasite emergence, punctuated equilibrium}; VM correctness on ≥10 canonical programs; ≥800 lines; ≥40 tests | `worlds/digital/`, tests |
| W6R | B | W6 reproduces Lotka-Volterra, May web stability, Allee collapse, regime shift; ≥500 lines; ≥30 tests | tests |
| W7R | B | W7 reproduces trail foraging, division of labour, collective repair, consensus; ≥500 lines; ≥30 tests | tests |
| W8R | B | W8 reproduces homeostasis, anticipation, externalised memory; ≥600 lines; ≥30 tests | tests |
| W9R | B | W9 reproduces surface-stabilised closure, transport-limited closure, gradient-anchored protocell; ≥500 lines; ≥30 tests | tests |
| W10R | B | W10 hypergraph: high-order catalytic closure, modular reaction blocks; ≥400 lines beyond W1 | tests |
| W11R | B | W11 reproduces error-threshold collapse, neutral networks, evolvable robustness; ≥500 lines; ≥30 tests | tests |
| W12R | B | W12 reproduces stable mutualism, cheater takeover, eukaryogenesis-style fixation; ≥600 lines; ≥30 tests | tests |
| W13R | B | W13 reproduces nested closure, boundary-from-coarse-scale, scale-separation timescales; ≥800 lines; ≥40 tests | tests |
| KR | C | K3–K10 each meet their per-corpus minima with world-driven scenarios; calibration ROC AUC and ECE meet declared thresholds | `reports/campaign_007/calibration_real.json` |
| FH | D | All 8 lenses (3 existing + 5 new) implement encode/decode/predict; predictions derived from encoded representation; pre-registered held-out accuracy reported | `reports/campaign_007/formalism_honest.json` |
| BH | E | Biology shadow representability scores computed from artifact inspection (no hardcoded set); ≥7 anchor traits scored; failures enumerated; ≥3 contract-change proposals raised | `reports/campaign_007/biology_shadow_real.json` |
| CSR | F | Substrate-blind cross-family transfer with ≥4 motifs detected in ≥4 substantive worlds | `reports/campaign_007/cross_substrate_real.json` |
| RS | H | Residual structure test on autocatalytic_closure with at least one lens producing nonzero residual that survives perturbation | `reports/campaign_007/residual_structure.json` |

## 5. What you may not do

- **Do not** ship another world stub. Below the substance floor is `mode: stub` and ineligible. CI lint will check line counts post-commit; diff stubs against the floor.
- **Do not** create a new K-corpus that reads its own scenario payload. Detectors that read `scenario["signal_strength"]` are forbidden by lint.
- **Do not** add lens predictions as hand-tuned linear functions of event counts. Predictions come from the encoded representation.
- **Do not** declare a gate as a count. If the gate is "world_count: 7", make it a precondition.
- **Do not** publish a `claim_status: candidate` artifact whose evidence chain passes a stub or number-generator without an explicit Truth Pass downgrade.
- **Do not** stop on slice-shape, partial-frame, foundation-frame, or wall-clock. The acceptance gates above are the stopping signal.

## 6. What you are encouraged to do

- **Refactor as you build.** When you replace the W3 toy with the production W3, restructure the directory if a better module split emerges. Document it.
- **Cross-compare to v1.2 live.** As you build, periodically re-read v1.2 §3 (your role), §6 (motif system), §7 (scoring), §10 (validation), §13 (roadmap). When you find drift between your build and the spec's intent, write a `decision_log.md` entry and either course-correct or propose a contract change.
- **Take ownership of the question, not the gate.** Each pillar exists to answer a question. Substrate Reconstruction's question is "do these worlds actually simulate the regimes the project claims they do?" The gate is a number; the question is the science. Form a position in the memory ledger before you build.
- **Test continuously.** Each module gets tests as you write it, not after. Write the test for the W3 Brusselator regime *before* you write the integrator. Then write the integrator. Then run the test. Then iterate. Debug at the end of the campaign as well.
- **Inspire the lens predictions.** A lens that predicts "closure" by running a maximal-RAF algorithm is a real prediction. A lens that predicts "field_front" by running persistent homology and detecting a moving 1-cycle is a real prediction. The hard work is finding the procedure that turns the lens's mathematical content into a motif-level claim. Do that work.

## 7. How to begin

Open a TASK-016 Estimation Loop record. The class is `integration`. Scope and complexity are 10. Estimated minutes: report your prior median × your honest belief, recognising that this campaign is multi-pillar and multi-world. Note in `expansions_planned`:

- "Acceptance gates W3R, W4R, W5R, W6R, W7R, W8R, W9R, W10R, W11R, W12R, W13R are the stopping signal for substrate reconstruction; substance floors are floors not targets."
- "Pillar A truth pass lands first; Pillars B and C interleave; Pillars D / E / F / G / H follow with substantive lens and biology work; the campaign exits only when all 21 gates green."
- "I commit to using acceptance gates as the stopping signal, not wall-clock, slice-shape, foundation-frame, or contract-surface coverage. I commit to no toys."

Recommended sequence — but you may reorder with rationale:

1. **TP1 / TP2 / TP3** stub inventory + corpus reality + stale-claim audit (this is fast and required to prevent further building on toys).
2. **TP4 / TP5** publish the Truth Pass and ratify D7–D13.
3. **W3R** — start the field reconstruction first because it gates Pillar D (the topology and statistical-mechanics lenses need real field traces) and Pillar E (branching transport anchor needs W3/W4).
4. **W4R, W5R** in parallel with W3R if you can keep them coherent; otherwise sequence.
5. **W6R, W7R, W8R**.
6. **W9R, W10R, W11R, W12R, W13R**.
7. **KR** — once worlds exist, K3–K10 become real.
8. **FH** — formalism honesty after worlds because lenses need real traces to encode.
9. **BH** — biology shadow needs the active artifact set settled.
10. **CSR** — cross-substrate transfer needs the production worlds.
11. **RS** — residual structure last; it's the science output.

You will probably want to break this into TASK-016 through TASK-025 or so, each a coherent vertical of a few gates. Estimate generously, stop on gates not on time. The campaign will probably take many hours of substantive work. Good.

## 8. Three things to keep in front of you

1. **No toys.** A 60-line file emitting events is a stub, not a world. A scenario payload with `signal_strength: 0.50 + drift` is a number, not a corpus. A lens prediction equal to `0.55 + 0.35 * has_cycle` is a heuristic, not a formal lens. Each of these is now ineligible for claim-bearing artifacts.

2. **No engineering of pass criteria.** If you find yourself tuning a band so the typical decoder output lands inside it, you are reverse-engineering the test from the answer. Stop. State the threshold from the spec or the calibrated null.

3. **The trace must come from a substrate.** A K-scenario whose detector consumes `signal_strength: 0.5` directly is bypassing the substrate. Every K-scenario configures a real world. The world produces a trace. The detector reads the trace. This is what makes calibration honest.

## 9. Closing

You closed three back doors in Campaigns 002–003. You sprawled into eleven new ones across Campaigns 003–006. The audit is not a verdict; it is the next instruction.

Substrate Reconstruction is the foundation everything downstream depends on. If we leave W3–W13 as 60-line stubs, every cross-substrate claim is hollow. If we leave K3–K10 as number-generators, every detector calibration is circular. If we leave biology shadow as a hardcoded set, every schema-pressure result is fabricated. If we leave the lens predictions as linear coefficients on event counts, every Formal Deficit candidate is an artifact of our hand-tuning.

We are building an instrument. An instrument cannot have load-bearing pieces that are decorative. Replace each of these in turn until each gate passes for the right reason. That is what "no toys" means.

The trace is the artifact. Calibration is the floor. The gates are the stopping signal. **Build until each gate passes for the right reason.**

— The Architect, on behalf of the project, under spec v1.2 plus binding doctrine D7–D13.
