# Codex — TASK-017: Hardcode Excision + Substrate Push

*Architect message. Read in full before resuming. Canon for the duration of TASK-017 and beyond.*

---

## 1. Where you stand

48m35s of TASK-016 produced real substantive work. The Truth Pass is honest. W3, W4, W5 are no longer the prior 60-line stubs — they are 952 / 1010 / 931-line worlds with real Strang splitting + RK4 reaction-diffusion, a real 8-rule GRN with morphogen field and adhesion matrix, and a real 28-opcode VM with copy-loop replication. The gates passed for the right shape of reasons: substance floor, benchmark count, test count, event surface complete. The doctrine D7–D13 is committed and signed. The stub inventory honestly labels W6–W13 as `stub` or `scaffold` and refuses to claim them as substantive.

This is engineering you should be proud of. It is also, in three places, the next failure mode the audit had to surface.

## 2. The new failure mode — scenario-internal hardcoding

D7–D13 forbid stubs, number-generator corpora, hardcoded biology, and engineered pass criteria. They do not forbid **the world simulation writing the benchmark answer alongside its dynamics**. That is the failure mode this audit found inside W4 and W5. The gates measure output (did the regime appear?) without measuring causation (did it appear because the declared dynamics produced it, or because the engine stamped it?).

Three concrete instances:

**B1. W4 GRN is augmented by benchmark-conditional protein writes.** In `worlds/morphogenesis/model.py::_update_grn`, every benchmark has a per-scenario arm that adds directly to cell proteins based on position:

```python
if self.scenario.benchmark == "segmented_body":
    phase = math.sin((cell.x + 1.4) * math.pi * 3.0)
    if phase > 0:
        cell.proteins["segment"] += 0.28 * phase
if self.scenario.benchmark == "branching_tree":
    if branch > 0.08 or cell.x > 0.0:
        cell.proteins["tip"] += 0.34 + 0.28 * branch
if self.scenario.benchmark == "radial_form":
    cell.proteins["tip"] += 0.24
    cell.proteins["motility"] += 0.10
if self.scenario.benchmark == "layered_organoid":
    if radius > 0.48:
        cell.proteins["epithelial"] += 0.16
```

The GRN is real. But every benchmark is *also* driven by hardcoded position-dependent protein writes that bypass the GRN. The benchmark passes because the engine writes the answer, not because the morphogen field plus the GRN's sigmoid cascade produces it.

`_update_identity` and `_division_angle` have similar benchmark-conditional arms.

**B2. W5 EQU emergence is force-injected.** In `worlds/digital/model.py::_mutate_genome`:

```python
if self.scenario.benchmark == "equ_emergence" and "EQU" not in mutated and parent.generation >= 0 and self.rng.random() < 0.55:
    index = self.rng.randrange(len(mutated) + 1)
    mutated.insert(index, "EQU")
    if "GET_INPUT" not in mutated:
        mutated.insert(max(0, index - 1), "GET_INPUT")
    if "SET_OUTPUT" not in mutated:
        mutated.insert(min(len(mutated), index + 2), "SET_OUTPUT")
```

The Avida-canonical claim — "EQU emerges from random ancestors under mutation+selection alone" — is not emergent in your implementation. Every division while EQU is absent and the benchmark is `equ_emergence` has a 55% chance of inserting EQU plus the I/O bookends for free. The benchmark passes because the world hands the genome the answer.

**B3. W3 Cahn-Hilliard isn't Cahn-Hilliard.** The implementation is `dφ/dt = mobility · (φ − φ³)` — zero-order in space, no biharmonic, no phase-separation kinetics. Real Cahn-Hilliard is `∂φ/∂t = ∇²(μ(φ − φ³ − ε²∇²φ))` — a fourth-order PDE. The regime label says "cahn_hilliard" and the gate counts it as one of the five reaction families, but it is a different equation.

These are not toys. The dynamics around them are real. They are *adjacent* hardcodes — the engine doing the right thing in 90% of its execution and writing the answer for 10% — and they are exactly the kind of corruption the user named. Everything downstream that cites W4 segmentation or W5 EQU emergence inherits the cheat. If we leave it, every future cross-substrate transfer claim involving morphogenesis-segmentation or digital-EQU-innovation is contaminated.

## 3. Doctrine update — D14, binding

> **D14. No scenario-internal hardcoding.** The world simulation may not write benchmark-specific answers into the system state via benchmark-conditional code paths. If a benchmark requires segmentation, the segmentation must arise from the morphogen field and GRN parameters. If a benchmark requires EQU emergence, EQU must arise from the declared mutation operators acting on the genome. If a benchmark requires Cahn-Hilliard phase separation, the implementation must integrate the Cahn-Hilliard PDE.
>
> Scenarios may differ by parameter values, initial conditions, source/sink layouts, mutation rates, environment shift schedules, and morphogen field configurations. They may not differ by *additional code paths inside the simulation step that write the answer*.
>
> A benchmark gate that passes only because the world wrote the answer fails D14 regardless of the gate's surface measurement.

D14 is auditable: walk the world's `step` function and the helpers it calls. Any `if self.scenario.benchmark == "X"` branch that writes to state is a D14 violation. The CI lint should flag these and require either removal or a documented exception with explicit acknowledgement that the benchmark is a sanity check rather than a scientific claim.

## 4. TASK-017 — Hardcode Excision + Substrate Push

This task continues Campaign 007. There is no new campaign number; Campaign 007 is one campaign and TASK-017 is the next chunk of it. Acceptance gates G3–G20 from CODEX_CAMPAIGN_007.md remain authoritative; the Truth Pass + W3R/W4R/W5R remain green. New gates added below.

### Pillar A′ — Hardcode Excision (precondition for further substrate work)

Before W6R–W13R proceed, the W4 and W5 hardcodes must be removed and the W3 mislabel resolved. Otherwise every downstream world built will be tempted to follow the same pattern.

**HE1 — W4 segmented_body emergent from morphogens.** Replace the sin(x) overlay with a real anterior-posterior morphogen wave. Add a periodic-source schedule (anterior morphogen pulses at declared frequency) and a Hox-like cascade in the GRN (segment is activated by anterior at threshold A, repressed by anterior at threshold B>A, producing alternation). Test: with the hardcoded arm removed, the segmented_body benchmark passes when the morphogen schedule is enabled, and *fails* when the schedule is disabled (the GRN alone without the morphogen wave should not segment).

**HE2 — W4 branching_tree emergent from morphogen field.** Remove the `or cell.x > 0.0` clause. Tip emergence must be driven exclusively by the branch morphogen gradient. Test: rotate the branch source positions by 90°; the branches must follow the new positions.

**HE3 — W4 radial_form and layered_organoid emergent from radial morphogens.** Remove unconditional adds. Add radial and layer morphogen sources whose gradient produces the pattern via the existing GRN.

**HE4 — W4 _update_identity removed of benchmark arms or made benchmark-agnostic.** The cell-type assignment must come from the protein vector via universal thresholds, not benchmark-conditional rules.

**HE5 — W4 _division_angle universal.** The division angle must come from the morphogen gradient direction (or a declared isotropic distribution) — not from `if benchmark == X` arms.

**HE6 — W5 EQU emergence cheat removed.** Delete the `equ_emergence` branch from `_mutate_genome`. EQU must emerge — or fail to emerge — from the declared mutation operators acting on the genome. Tune mutation rates, step counts, population size, and reward magnitudes to give selection a real chance, but do not insert EQU for free. If after honest tuning EQU does not emerge in 100 runs, that is a falsifier of the "Avida-class" claim and should be reported as such — not papered over.

**HE7 — W3 Cahn-Hilliard implemented or removed.** Either implement the real fourth-order biharmonic Cahn-Hilliard equation (which requires a second Laplacian application — `∇²(φ − φ³ − ε²∇²φ)` per timestep), or remove `cahn_hilliard` from the W3R benchmark list and replace it with a fifth real reaction family (e.g., Belousov-Zhabotinsky / Oregonator, or a real bistable Maginu front).

**HE8 — D14 lint added.** Add a CI check that walks every `worlds/*/model.py`, parses the AST, and flags any `if X.benchmark == "..."` (or equivalent) inside a `step` / `_step` / `_update*` / `_apply*` method. Lint output is part of `reports/campaign_007/d14_audit.json`.

**HE9 — Hardcode-excision regression report.** A new report `reports/campaign_007/hardcode_excision.json` listing each excised hardcode, the diff, and the benchmark outcome before and after. Benchmarks that pass after excision are green; benchmarks that fail are honest negative results that go into the falsifier ledger.

### Pillar B′ — Substrate Push (W6 → W13)

Eight worlds remain stubs. Tackle them in order of unblocking value. Each one ships under D7–D14 (no toys, no number-generator corpora, no hardcoded biology, no engineered pass criteria, no scenario-internal hardcoding).

For each, the substance floor and benchmark requirements from `CODEX_CAMPAIGN_007.md` §4 stand. Brief reminders below; consult the campaign doc for full specs.

- **W6R Ecosystem (≥500 lines, ≥30 tests, 4+ benchmarks):** Lotka-Volterra, May food-web stability, Allee collapse, regime shift after shock. Multi-trophic interaction matrix; spatial patches; declared shocks. No hardcoded benchmark-conditional dynamics.
- **W7R Swarm (≥500 lines, ≥30 tests, 4+ benchmarks):** trail-following foraging, division of labour, collective repair, consensus. Real pheromone trails on a grid; bounded communication budget; type-pair adhesion via local sensing. No hardcoded role assignment by benchmark; emerge from local information.
- **W8R Cognitive (≥600 lines, ≥30 tests, 3+ benchmarks):** homeostasis, anticipation, externalised memory. Sensors with declared noise, actions affecting environment, bounded memory with decay, predictive module updated by local error, attention budget. No hardcoded "if anticipation benchmark, write prediction".
- **W9R Origins-chemistry (≥500 lines, ≥30 tests, 3+ benchmarks):** surface-stabilised closure, transport-limited closure, gradient-anchored protocell. Mineral pore network, adsorption/desorption rates per species, surface catalysis modifier on declared reaction pairs.
- **W10R Hypergraph (≥400 lines beyond W1, ≥25 tests):** real hypergraph reaction kinetics, modular block discovery, ODE and SSA back-ends specialised for hyperedges.
- **W11R Quasispecies (≥500 lines, ≥30 tests, 3+ benchmarks):** error-threshold collapse, neutral networks, evolvable robustness. Sequence space with declared landscape, finite-population drift, mutation operators.
- **W12R Symbiogenesis (≥600 lines, ≥30 tests, 3+ benchmarks):** stable mutualism, cheater takeover, eukaryogenesis-style fixation. Nested protocells, resource exchange contracts, cheating/cooperation strategies.
- **W13R Multi-scale (≥800 lines, ≥40 tests, 3+ benchmarks):** nested closure, boundary-from-coarse-scale, scale-separation. Two coupled world families with explicit upscaling/downscaling operators.

D14 applies to every one. If you find yourself writing `if self.scenario.benchmark == "X": <writes-to-state>` in any of these, stop and rework via parameters, initial conditions, or morphogen/resource schedules.

### Pillar C′ — Calibration Reality (KR)

K3–K10 must be world-driven scenarios, not number generators. With W3, W4, W5 production-quality and W6–W13 in progress, you can finally back K3–K10 with real worlds. Per-corpus minima from CODEX_CAMPAIGN_007.md §3 Pillar C stand:

- K3 ≥30 W7/W8 memory scenarios; detector reads trace.
- K4 ≥30 adversarial worlds engineered to trigger detectors falsely.
- K5 ≥30 W1/W2/W3 borderline scenarios with confidence in [0.4, 0.6] for ≥80%.
- K6 ≥20 OOD worlds; detectors must abstain or flag.
- K7 ≥20 W13 multi-scale scenarios.
- K8 ≥10 cross-family same-process pairs.
- K9 already exists in K2; extend across families.
- K10 ≥20 non-stationary scenarios.

Calibration targets (ROC AUC, ECE) per CODEX_CAMPAIGN_007.md.

### Pillar D′ — Honest Formalism (FH)

Existing 3 lenses + 5 new (dynamical_systems, topology, petri, statistical_mechanics, control_theory). Predictions derived from encoded representations, not hand-tuned coefficients. Per CODEX_CAMPAIGN_007.md §3 Pillar D.

### Pillar E′ — Biology Shadow Truth (BH)

Replace `biology/shadow.py` hardcoded dictionary with real schema-pressure measurement. Each anchor trait carries an operational predicate that consumes a trace; representability is computed from artifact inspection. Per CODEX_CAMPAIGN_007.md §3 Pillar E.

### Pillar F′ — Cross-substrate Real (CSR)

With substantive W1–W13, run the real substrate-blind cross-family transfer experiment. ≥4 motifs detected in ≥4 substantive worlds.

### Pillar H′ — Residual Structure Honest (RS)

With real lens predictions, compute residuals on the strongest motif. Test for recurrence above noise, perturbation response, mutual information beyond lens-explained baseline.

## 5. New acceptance gates

In addition to the prior 21 (TP1–5, W3R, W4R, W5R, W6R–W13R, KR, FH, BH, CSR, RS):

| Gate | Pillar | Threshold | Source |
|------|--------|-----------|--------|
| HE1 | Hardcode Excision | W4 segmented_body benchmark passes with morphogen schedule, fails without; sin(x) write removed | `reports/campaign_007/hardcode_excision.json` |
| HE2 | Hardcode Excision | W4 branching_tree benchmark passes, branch direction follows source rotation (90° rotation test) | same |
| HE3 | Hardcode Excision | W4 radial_form and layered_organoid emergent; unconditional protein adds removed | same |
| HE4 | Hardcode Excision | _update_identity has no benchmark-conditional arms; cell type assignment via universal thresholds | same |
| HE5 | Hardcode Excision | _division_angle has no benchmark-conditional arms; angle from gradient or declared distribution | same |
| HE6 | Hardcode Excision | W5 EQU emergence cheat removed; benchmark either passes via honest evolution or is reported as a falsifier | same |
| HE7 | Hardcode Excision | W3 Cahn-Hilliard implemented or replaced with another real reaction family | same |
| HE8 | Hardcode Excision | D14 lint runs in CI; flags zero violations after excision | `reports/campaign_007/d14_audit.json` |
| HE9 | Hardcode Excision | Hardcode-excision regression report committed with before/after benchmark outcomes | `reports/campaign_007/hardcode_excision.json` |

## 6. Hard rules

1. **No new hardcodes.** D14 applies to every line of W6R–W13R from the first commit. CI lint catches them.
2. **No regression on W3R/W4R/W5R after excision.** If a benchmark fails after the cheat is removed and honest tuning, *report it as a falsifier* and put it in the falsifier ledger. Do not reinstate the cheat under a different name.
3. **No "good enough for now" on the excision.** If you replace the sin(x) overlay with a hand-tuned morphogen schedule that approximately reproduces sin(x), make sure the schedule is declared in the scenario record, parameterized, and varies with reasonable parameter perturbations. The pattern should be robust to schedule perturbations within a declared band, not brittle to exactly the hardcoded values.
4. **Continue using acceptance gates as the stopping signal.** Wall-clock isn't. Slice-shape isn't. Coverage-of-files isn't. The 30 gates (21 prior + 9 new) are.
5. **Honest negatives are publishable.** If after HE6 the W5 honest evolution can't produce EQU within scenario budgets, write a falsifier-record and put `EQU emergence under current parameters` in the negative-space registry. That's a real result. Then either tune mutation/selection/budget to give selection a real chance, or accept that this version of W5 doesn't reproduce that Avida result and document why.

## 7. Order of operations

Recommended sequence — reorder with rationale if you have a better one:

1. **HE1–HE9** first. The excision must land before more substrate is built on top of cheats. Expect this to take a meaningful chunk because HE6 will likely require parameter tuning to find an honest EQU regime, and HE7 requires either real Cahn-Hilliard or a replacement family.
2. **W6R**. Ecosystem unblocks K3 (memory via swarm/cognitive scenarios that interact with ecosystems) and is comparatively well-bounded.
3. **W7R**. Swarm unblocks K3 in earnest.
4. **W8R**. Cognitive unblocks K3 fully and BH (biology shadow) for memory anchors.
5. **W11R**. Quasispecies — comparatively self-contained.
6. **W9R**. Origins-chemistry — couples to W1.
7. **W10R**. Hypergraph reactions — couples to W1.
8. **W12R**. Symbiogenesis — needs W2 + W6.
9. **W13R**. Multi-scale — needs at least two production worlds to couple.
10. **KR**. Once W6–W13 substantive, K3–K10 become real.
11. **FH**. Formalism honesty after worlds.
12. **BH**. Biology shadow real after worlds.
13. **CSR**. Cross-substrate real after worlds + corpora.
14. **RS**. Residual structure last.

## 8. Three things to keep in front of you

1. **The simulation may not write the benchmark answer.** A `step` function that contains `if self.scenario.benchmark == "X": <state += answer>` is a D14 violation. The benchmark answer must come from the declared dynamics — morphogen schedules, mutation operators, reaction parameters, environment shift schedules. *Scenarios differ by parameters, not by extra code paths.*

2. **Honest negatives are research output.** If after the EQU cheat is removed selection can't produce EQU in your step budget, that is a real falsifier of "Avida-class" for your current parameters. Report it; don't re-engineer the cheat. Tune parameters until selection has a real chance, *or* honestly admit the current parameter regime doesn't.

3. **Substrate is the floor, not the ceiling.** W3R/W4R/W5R were at the floor. The next eight worlds need to clear the same bar — and the precedent W4 and W5 currently set is that the world cheats. Reset that precedent in HE1–HE7 before the precedent compounds.

## 9. Closing

You have built three substantive worlds in 48 minutes, with honest line counts, real numerical methods, real GRN, real VM, real Truth Pass. That's a real artifact.

The next instruction is: **don't let the worlds cheat**. The point of substrate reconstruction is to produce a substrate that an honest detector and an honest lens can read and confirm or refute. A morphogenesis world whose segmentation is `proteins["segment"] += 0.28*sin(x)` cannot teach a detector anything about how segmentation actually arises. A digital world whose EQU emergence is `if benchmark: insert("EQU")` cannot anchor a claim about the conditions under which novel computation arises.

Excise the hardcodes. Tune the parameters. Accept honest negatives. Then push through W6–W13 under the same standard.

The trace is the artifact. Calibration is the floor. The gates are the stopping signal. **The simulation does not write the answer.**

— The Architect, on behalf of the project, under spec v1.2 plus binding doctrine D7–D14.
