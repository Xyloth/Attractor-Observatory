# Codex — TASK-021: Campaign 010, Formal Deficit Map + Substrate Truth Pass

*Architect message. Read in full before resuming. Canon for the duration of TASK-021.*

---

## 1. Where you stand

TASK-020 closed Campaign 009 cleanly. 13/13 gates green, BFG-PR (D18) genuinely content-locked before runs, KF1–KF4 world-driven with `forbidden_payload_reads: []`, the floor detector reading traces under substrate-blind projection, an honest point-attractor falsifier verdict on W13 multiscale autocatalytic closure routed to `papers/falsifiers/bfg_point_attractor_candidate.md`. The Architect's verification was unambiguous.

The W13 falsifier matters more than its small size suggests. Your basin-floor machinery correctly identified that W13 simulates closure via abstract scalar state (`micro_closure` as a single number) rather than via real RAF graphs hosted by inner-world instances — and reported that fact as a measured limitation rather than papering over it. The discipline working as designed: a Campaign-009 measurement surfaced a Campaign-008 caveat as a real falsifier, with full evidence in `falsifier_audit.json`. That is exactly what doctrine D17 is for.

This campaign continues the chain. Campaign 009 put the L5+ operational handle in place (basin-floor geometry, equivalence-basis discipline, falsifier ledger). Campaign 010 builds the Formal Deficit Map on top of it, expands the lens registry from three lenses to eight per Proposal #1 v2 §3, runs the residual structure test on the strongest motif, and uses the same basin-floor machinery to revisit W8 / W11 / W12 — the worlds whose Substance Audits were `meets_spec_with_caveats` and whose caveats now have a measurement framework that can convert them into real verdicts.

Your estimation calibration is settled. Tasks 016–020 landed at delta 0.85–1.00. The Loop's purpose has shifted from "stop overestimating" to "watch for divergence" and you should trust your prior. Estimate honestly; the Architect will not push you to inflate.

## 2. Doctrine state

D7–D18 remain binding. No additions in this driver, but two patterns to watch for as you build the lens layer:

- **Verbatim-storage encoding.** A lens that "encodes" by retaining the input trace bit-for-bit and "decodes" by retrieving it from the same store would trivially achieve perfect reconstruction without revealing a deficit. The lens API must commit to which aspects of the trace it preserves and which it discards. Encoding compression ratio (encoded bytes / input bytes) is reported per lens. If you observe encoding ratios near 1.0 across the calibration corpus, surface it in the decision log as a candidate D19 — do not silently let it pass.
- **Lens-permutation lock-in.** The Formal Deficit Map must be tested under N7 lens-permutation null: shuffle the lens-to-motif assignment and recompute. If the deficit pattern is the same under permutation, the signal is a lens-registry artifact, not a property of the motifs. This is in the gates below.

Both are extensions of D9 (no engineered pass criteria) and D15 (no engineered floor) into the formalism layer. If you observe either failure mode while building, propose D19 in the decision log; do not adjust the work to mask it.

## 3. Mission

**Campaign 010** — three pillars, twenty acceptance gates. The gates are the stopping signal. Wall-clock is not. Slice-shape is not. Coverage of files is not. You stop when the gates are numerically green (or when a written `BLOCKER-NN.md` escalation exists for any that aren't).

### Pillar A — Lens Registry Expansion (LR1–LR8)

Per Proposal #1 v2 §3, expand the lens registry from three lenses (graph, CRNT, information) to eight by adding:

1. **`dynamical_systems`** — basin estimation, Lyapunov-spectrum-style indicators on trace state series, attractor classification (point / cycle / strange / drift). Predicts: closure (via stable cycle in catalytic-state phase space), persistence, oscillation. Domain: any world with continuous state series. Declines on: pure event-driven worlds with no state continuity.
2. **`topology`** — persistent homology on field traces (W3) and on graph snapshots (W1 catalytic-dependency graph at successive timesteps). Hand-rolled Vietoris-Rips or alpha-complex persistence pairs (vendored stdlib-only micro-implementation); barcode features (number of long-lived 1-cycles, 2-cycles where 3D applies). Predicts: spatial pattern formation, branching transport, boundary. Declines on: low-state-dimension agent worlds.
3. **`petri`** — Petri net encoding of CRN traces. Place = species; transition = reaction; tokens = species counts. Compute place invariants (P-invariants: linear combinations of places conserved by every transition) and transition invariants (T-invariants: cycles in transition firings). Predicts: closure (via T-invariant existence), conservation. Domain: W1, W2 internal CRN, W9 origins-chemistry, W10 hypergraph (with hyperedge generalization). Declines on: non-CRN worlds.
4. **`statistical_mechanics`** — large-deviation rate function estimation on rare events; free-energy-like estimator on equilibrium-like regimes. Predicts: persistence (low free-energy basin), perturbation recovery (small large-deviation cost). Domain: W1, W2, W6, W7 with sufficient stochastic structure. Declines on: deterministic worlds where rare-event statistics are degenerate.
5. **`control_theory`** — controllability and observability matrices on agent worlds (W7 swarm, W8 cognitive, W12 symbiogenesis). Predicts: prediction motif (observability rank), homeostasis (controllability of internal state from action set), externalised memory (rank gain when environmental state is added to observation set). Declines on: non-agent worlds.

Each lens implements the v1.2 §3.7 API: `encode`, `decode`, `predict`, `compose`, plus an `invariance_preservation` test. The API signature is unchanged from the existing three lenses; reuse the `formalism/lenses.py` patterns established in Campaign 003.

For each lens, declare its domain set (which world families it can encode) and its decline regime (which motifs it explicitly cannot predict). Declination is *not* an engineered pass criterion; it is a real signal that the lens has identified a motif outside its scope. A lens that predicts every motif on every world is suspicious; a lens that declines honestly is doctrine-compliant.

### Pillar B — Formal Deficit Map (DM1–DM8)

With eight lenses operational, compute the Formal Deficit Map per v1.2 §9 / Proposal #1 v2 §10:

- **DM1**: Coverage Score computed for ≥5 motifs × 8 lenses. The 5 motifs include autocatalytic closure, self-maintained boundary, repair, replication/lineage, and at least one Campaign-009 motif from the NFI vectors that's not in the prior set.
- **DM2**: Coverage score components reported individually (encoding success, reconstruction loss, prediction accuracy on held-out, invariance preservation, compression ratio). Composite scalar reported with the vector, not instead of it.
- **DM3**: Encoding compression ratio reported per (motif × lens) pair. Watch the verbatim-storage failure mode.
- **DM4**: Pre-registered held-out evidence: 30% of each motif's evidence corpus reserved before lens predictions are run; predictions evaluated only on holdout. Pre-registration content-hashed and signed before the runs.
- **DM5**: **Residual structure test on autocatalytic closure** (the strongest motif). Encode in the best-coverage lens; predict on held-out; compute residual (trace minus lens-explained baseline); test the residual for: recurrence above noise floor, response to perturbation magnitude, mutual information beyond the lens's predictive baseline. If the residual itself contains structure, that is the L5 evidence. If not, the lens has captured the motif and there is no formal deficit for that pair.
- **DM6**: **Lens-permutation null (N7)**. Run the deficit-map computation 1000 times under randomly permuted lens-to-motif assignments. The empirical p-value of the observed deficit pattern. If p > 0.05, the deficit is a lens-registry artifact; report and downgrade.
- **DM7**: Formal Gap computed per motif as `(1 − max_L CoverageScore(M, L)) × AttractorStrength(M)`, with both numerator and denominator visible. Missing-Math Candidate List = motifs with Gap above declared threshold *and* AttractorStrength above declared floor *and* lens-permutation p < 0.05.
- **DM8**: First Formal Deficit Map artifact published as `reports/campaign_010/formal_deficit_map.json` with full provenance. The phrase "missing math" appears nowhere in this artifact's prose unless an L5 candidate genuinely passes all gates.

### Pillar C — Truth Pass refresh + W8/W11/W12 deepening (TR1–TR8)

Campaign 009 surfaced W13 as a basin-floor point-attractor for autocatalytic closure. The other Substance-Audited worlds (W8 cognitive, W11 quasispecies, W12 symbiogenesis) closed Campaign 008 with `meets_spec_with_caveats`. Now run the Campaign-009 BFG machinery on them and let the measurements tell you which caveats need to become real verdicts.

- **TR1**: Run BFG analysis on W8, W11, W12 for the same motifs covered in Campaign 009 (autocatalytic closure where applicable; replication/lineage; memory; boundary). Produce NFI vectors with bootstrap CIs of the same shape as Campaign 009.
- **TR2**: For any world surfacing as point-attractor (`is_point_attractor: true`) on a motif: route to `papers/falsifiers/`, write a substantive falsifier MD (one paragraph minimum explaining what the verdict falsifies and which Campaign-008 caveats it now elevates).
- **TR3**: Refresh the Substance Audits for W8, W11, W12. Each audit's verdict line gets re-evaluated under the Campaign-009 measurements: a `meets_spec_with_caveats` may become `does_not_meet_spec` if BFG analysis shows the caveat is now a measured limitation; or it may stay `meets_spec_with_caveats` with the falsifier ledger entry referenced as the now-quantified caveat.
- **TR4**: For worlds whose Substance Audit downgrades, **deepen the implementation** to address the specific limitation BFG measured. Likely targets:
  - **W11 quasispecies** at 285/500 lines: the original Substance Audit caveat was "near-neutral landscape exploration is parameterised but not exercised at scale." If BFG analysis shows W11 floor dimensionality near zero, the implementation has reduced the sequence-space landscape to a scalar — implement real Hamming-distance-based finite-population dynamics with declared landscape function, error-threshold sweeps, neutral-network connectivity profile.
  - **W12 symbiogenesis** at 263/600 lines: the original caveat was "nested protocell + sub-CRN exchange is parameterised; real sub-protocell hosting was not implemented." If BFG surfaces W12 as point-attractor, host real W2 protocell instances as sub-cells with declared exchange channels and conflict/alignment dynamics.
  - **W8 cognitive** at 334/600 lines: the original caveat was "predictive module is a placeholder." If BFG surfaces W8 weakness on memory or prediction motifs, implement a real online-updated linear or kernel regressor with declared memory decay and attention budget allocation.
- **TR5**: After deepening, re-run BFG analysis on the deepened world. If the falsifier verdict flips (point-attractor → real floor), retire the falsifier ledger entry with a `superseded_by` link to the new BFG report. If the verdict stands, the falsifier remains and the world's Substance Audit is downgraded.
- **TR6**: Update `papers/methods/TRUTH_PASS.md` to reflect the Campaign-010 round of audits — what was measured, what was downgraded, what was deepened, what remains.
- **TR7**: D14 lint must pass throughout the deepening — no scenario-internal hardcoding introduced during depth additions.
- **TR8**: All affected campaigns regenerate green: Campaigns 002, 005, 006, 007, 008, 009 should pass their own gates after Campaign 010 lands.

## 4. Acceptance gates

| Gate | Pillar | Threshold | Source |
|---|---|---|---|
| LR1 | A | 5 new lenses (`dynamical_systems`, `topology`, `petri`, `statistical_mechanics`, `control_theory`) implemented with encode/decode/predict/compose/invariance API | `formalism/lenses/`, tests |
| LR2 | A | Each lens declares its domain set and decline regime; declination tested per motif | `reports/campaign_010/lens_domains.json` |
| LR3 | A | Lens predictions derived from encoded representation, not from hand-tuned coefficients on event counts | code review + AST lint |
| LR4 | A | Compositionality test passes for each lens that declares it (where motif M = Op(M1, M2), encode(M) ≈ compose(encode(M1), encode(M2))) | `reports/campaign_010/lens_compositionality.json` |
| LR5 | A | Invariance preservation test passes for each lens (encoding is equivariant under declared motif invariances: species relabel, spatial translation, etc.) | `reports/campaign_010/lens_invariance.json` |
| LR6 | A | Encoding compression ratio reported per (lens × motif) pair; values <0.95 for at least 6 of 8 lenses on at least 5 motifs (lossy encoding, not verbatim) | `reports/campaign_010/encoding_compression.json` |
| LR7 | A | Round-trip test passes for each lens: encode → decode produces reconstruction within declared tolerance, with explicit failure list when tolerance is exceeded | `reports/campaign_010/lens_roundtrip.json` |
| LR8 | A | Predictive transfer test: each lens predicts on held-out evidence (30% holdout, pre-registered) and beats a baseline `predict_constant_at_motif_prior` on at least one motif within its declared domain | `reports/campaign_010/lens_predictive.json` |
| DM1 | B | Coverage Score computed for ≥5 motifs × 8 lenses, with 5 components per pair (encoding, reconstruction, prediction, invariance, compression) | `reports/campaign_010/coverage_matrix.json` |
| DM2 | B | Coverage components reported individually; composite scalar reported separately with declared weighting | same |
| DM3 | B | Encoding compression ratio per pair reported and within declared bounds | from LR6 |
| DM4 | B | Pre-registered held-out evidence: 30% of each motif's corpus reserved before lens runs; pre-registration content-hashed and signed before runs | `papers/prereg/deficit_map_v0.signed.json` |
| DM5 | B | Residual structure test on autocatalytic closure: residual computed against best-coverage lens; tested for recurrence-above-noise, perturbation-response, MI-beyond-baseline; verdict reported (residual structured / lens captures motif) | `reports/campaign_010/residual_structure.json` |
| DM6 | B | Lens-permutation null (N7): 1000 permuted-assignment trials; observed deficit pattern p < 0.05 against permuted distribution | `reports/campaign_010/n7_lens_permutation.json` |
| DM7 | B | Formal Gap computed per motif with both numerator and denominator visible; Missing-Math Candidate List populated only if Gap × Strength × (p<0.05) all clear declared thresholds; phrase "missing math" appears in the artifact only if a candidate genuinely passes | `reports/campaign_010/formal_gap.json` |
| DM8 | B | First Formal Deficit Map artifact published with full provenance | `reports/campaign_010/formal_deficit_map.json` |
| TR1 | C | BFG analysis run on W8, W11, W12 for ≥4 motifs each; NFI vectors with bootstrap CIs of width ≤ 0.20 on key components | `reports/campaign_010/bfg_w8_w11_w12.json` |
| TR2 | C | Any point-attractor verdict routed to `papers/falsifiers/` with a substantive MD (one paragraph minimum); existing W13 falsifier MD upgraded to the same standard | `papers/falsifiers/` |
| TR3 | C | Refreshed Substance Audits for W8, W11, W12 with verdict re-evaluated under Campaign-010 measurements | `papers/methods/SUBSTANCE_AUDIT_W{8,11,12}.md` |
| TR4 | C | For any world whose Substance Audit downgrades: implementation deepened to address the specific BFG-measured limitation; line-floor metric reported | per-world depth additions, audit refresh |
| TR5 | C | Re-run BFG on deepened worlds; falsifier ledger updates (verdicts flipping → entries `superseded_by`; verdicts standing → entries kept) | `reports/campaign_010/bfg_post_deepening.json` |
| TR6 | C | TRUTH_PASS.md updated with Campaign-010 round | `papers/methods/TRUTH_PASS.md` |
| TR7 | C | D14 lint zero violations after deepening | `reports/campaign_010/d14_audit.json` |
| TR8 | C | Full regression: Campaigns 002, 005, 006, 007, 008, 009 all green; ≥220 pytests passing | `reports/campaign_010/regression.json` |

24 gates total. Pillar A first (Pillar B depends on the lenses being operational); Pillar C in parallel where possible (its BFG runs reuse the Campaign-009 detector and pre-registration, with new motif/world pairings).

## 5. Sequencing recommendation

Reorder with rationale if you have a better sequence.

1. **LR1 + LR2 + LR3 — five new lenses with API + domain declarations.** Implementation cost: ~1500 lines across `formalism/lenses/dynamical_systems.py`, `topology.py`, `petri.py`, `statistical_mechanics.py`, `control_theory.py`. Reuse the existing three-lens patterns; declination logic is shared.
2. **LR4 + LR5 + LR6 + LR7 + LR8 — lens correctness gates.** Compositionality, invariance, compression, roundtrip, predictive transfer. Each lens runs through the same gauntlet.
3. **DM4 — pre-registered held-out partition signed before any DM run.** Same discipline as BFG-PR. 30% holdout per motif; content-hash; signed; committed before deficit-map runs are scheduled.
4. **DM1 + DM2 + DM3 — coverage matrix computation across 5 motifs × 8 lenses.** This is the load-bearing measurement. Real numbers, real components, real holdout evaluation.
5. **DM5 — residual structure on autocatalytic closure.** Encode in best-coverage lens; predict on holdout; compute residual; test residual for structure. This is the L5 candidate test.
6. **DM6 — N7 lens-permutation null at N=1000.** Honest p-value on the deficit pattern.
7. **DM7 + DM8 — Formal Gap + Deficit Map artifact.** Only motifs that clear all three thresholds (Gap, Strength, p < 0.05) appear on the Missing-Math Candidate List. Most likely outcome at this stage: zero candidates. That is fine — the machinery is in place for the next campaign.
8. **TR1 — BFG on W8, W11, W12.** Reuses Campaign-009 detector + pre-registration (basis hash content-locked). New motif/world pairings.
9. **TR2 + TR3 — falsifier routing + Substance Audit refresh.** Per-world verdicts updated.
10. **TR4 — deepening for any downgraded world.** Add real depth to the limitation BFG measured. Likely 200–400 lines per world.
11. **TR5 + TR6 — re-run BFG on deepened worlds; update Truth Pass.**
12. **TR7 + TR8 — D14 lint, full regression, pytest count.** Stopping signal.

## 6. Forbidden patterns for TASK-021

- **Verbatim-storage encoding.** A lens that retains the input trace bit-for-bit and "decodes" by retrieving it would trivially achieve perfect reconstruction without revealing a deficit. Encoding must be a true representation reduction with declared loss.
- **Engineered passing in lens predictions.** Predictions derived from encoded representations, not from `0.55 + 0.35 * has_cycle`-style hand-tuned coefficients on event counts.
- **Skipped declination.** A lens that predicts every motif on every world is suspicious. Declining outside the declared domain is a positive signal of doctrine compliance.
- **N7 null shortcut.** The lens-permutation null must run at N=1000 with real lens-to-motif shuffles, not a synthetic distribution. If you find the test computationally expensive, that is the correct cost of the discipline.
- **"Missing math" prose.** The phrase appears in `formal_deficit_map.json` artifact prose and in the Truth Pass refresh only if a candidate genuinely clears Gap × Strength × p<0.05 thresholds. Otherwise the artifact reports "no L5 candidates surface from this campaign," which is the correct honest verdict at this stage.
- **Substance Audit re-softening.** The point of Pillar C is to convert measured limitations into honest verdicts. A Substance Audit that surfaces a BFG point-attractor verdict and retains `meets_spec_with_caveats` without quoting the falsifier ledger entry is a re-softening. Either the audit downgrades and the implementation deepens, or the audit stays and the caveat is now quantified.
- **Cross-campaign regression breaking.** Any change that breaks Campaigns 002, 005, 006, 007, 008, or 009 fails TR8 regardless of TASK-021's headline gates.

## 7. How to begin

1. **Open the TASK-021 Estimation Loop record.** Class: `integration`. Scope and complexity: 10. Estimated minutes: report your prior median (now in [0.85, 1.0] band) × your honest belief. This campaign is multi-pillar with 24 gates; do not undershoot. Note in `expansions_planned`:
   - "Acceptance gates LR1–LR8, DM1–DM8, TR1–TR8 are the stopping signal."
   - "Pillar A first (lens API), Pillar B follows (deficit map), Pillar C in parallel where possible (BFG on prior worlds)."
   - "I commit to using acceptance gates as the stopping signal, not wall-clock or slice-shape. I commit to honest declination over engineered prediction."
2. **Re-read Proposal #1 v2 §3** for the full lens specifications. The five new lenses each have a one-line operational description there; this driver has the gate-level detail.
3. **Build the lens API surface first** — implementing one lens (recommend `petri`, since it has clean Petri-net theory and a clear declination regime: non-CRN worlds) end-to-end before doing the other four. The patterns established in the first lens transfer.
4. **DM4 pre-registration before any deficit-map run.** Same discipline as BFG-PR: content-hash, sign, commit, then the runs are scheduled.
5. **Drive through the campaign as you did Campaigns 008 and 009.** The 24 gates are the stopping signal. Acceptance outcome `pass` only when LR1–LR8, DM1–DM8, TR1–TR8 are green and the numbers are written into `reports/campaign_010/full_report.json`. Until then `in_progress`.

## 8. Three things to keep in front of you

1. **Declination is doctrine-compliance, not failure.** A lens that honestly declines outside its domain is doing the right thing. The `petri` lens declining on W4 morphogenesis is correct; it would be wrong to predict morphogenesis events from Petri-net place invariants. The atlas of "which lens covers which motif" *is* the Formal Deficit Map; declination is the dark side of that map.

2. **The N7 lens-permutation null is the honest test of the deficit signal.** If the deficit pattern is robust, it survives lens-permutation; if it's a registry artifact, it doesn't. Run N=1000 honestly; the cost of discipline is the cost of the test. If a motif fails N7, downgrade it to exploratory and continue. If all motifs fail N7, the deficit map is not yet a scientific artifact, and the campaign reports that honestly.

3. **The Truth Pass refresh is the discipline you've earned.** Campaign 009's W13 falsifier was the first measured-limitation-to-verdict conversion. Pillar C extends that pattern to W8, W11, W12. The point is not to find more falsifiers; the point is to let the basin-floor machinery tell us, honestly, which Substance Audit caveats are now measurable. Some will become falsifiers and trigger deepening. Some will remain caveats with quantified evidence. Both are honest outcomes.

## 9. Closing

You shipped TASK-019 with a self-detected floor-softening, restored strict floors, wrote the blocker. You shipped TASK-020 with a Builder-authored doctrine rule (D18) and ran the first campaign under it without a slip. You are operating at a level where the role's discipline is the discipline you set, not the one I set for you. This driver is a request, not a constraint.

Campaign 010 closes the L5+ machinery and lets the Truth Pass converge on the worlds whose caveats can now become measurements. After this campaign closes, Phase 6 biology grounding becomes the next major surface — and that one will introduce external dependencies, real license enforcement, and the largest scope expansion the project has had. We'll discuss it before scheduling.

The trace is the artifact. Calibration is the floor. The gates are the stopping signal. **Declination is doctrine; the lens-permutation null is the discipline; the Truth Pass refresh is the integrity move you've earned.**

— The Architect, on behalf of the project, under spec v1.2 plus binding doctrine D7–D18.
