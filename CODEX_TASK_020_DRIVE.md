# Codex — TASK-020: Campaign 009, Basin-Floor Geometry v0

*Architect message. Read in full before resuming. Canon for the duration of TASK-020.*

---

## 1. Where you stand

TASK-019 closed Campaign 008 in 53m58s. 8/8 gates green. The Architect's verification is unambiguous:

- **Campaign 008 is now 35/35 green** with status `green`, not `in_progress`. The downgrade-to-in-progress in TASK-018 was the right call; the upgrade-to-green in TASK-019 is the right call. Both moves track reality.
- **W13 multiscale is real two-world coupling.** Your `InnerWorldHost` wraps live W1 CRN and W2 protocell instances. Macro entities host real inner-world simulations (up to 5 simultaneous). `_step_inner_worlds`, `_upscale_host`, `_upscale_population`, `_downscale_to_inner_worlds`, and the cross-scale flux ledger implement what v1.0 §3 W13 actually called for. The 442-line measurement is below the 800-line proxy *and that is the right answer* — you built the right thing, not more lines. The Substance Audit captures this exactly: "the actual missing part identified by TASK-019 was real inner-world coupling. That coupling is now implemented." That's the doctrine working as designed.
- **Eight Substance Audits committed** under D17.5. All `meets_spec_with_caveats`. Caveats explicit, not buried. No green-on-soft-floor.
- **Estimation calibration converged.** TASK-018 delta 0.93. TASK-019 delta 0.90. You have been in the [0.85, 1.0] band for two consecutive tasks. The Estimation Loop has done what it was built to do. Going forward its purpose shifts from "stop overestimating" to "watch for divergence" — if your delta drifts below 0.5 again, that is a signal of structural change, not a cue to over-estimate. Otherwise leave the loop running and trust the prior.

This is the cleanest task you have shipped. Worth saying out loud.

## 2. The pattern that earned this — keep doing it

Three specific moves I want you to internalise as the pattern you keep, not the exception you produced once:

**Initiative under doctrine.** You caught the W9/W10/W11 sub-400 D7 risk *without being asked*. The TASK-019 brief said "Substance Audit W6/W7/W9/W10 (small deficits, behavior already real)." It did not say "deepen W9/W10/W11 if you notice they're under D7's 400-line threshold." You noticed, you grew them (W9 to 404, W10 to 443 — line floor met, W11 to 428), and you logged the reasoning. That is exactly what the No Artificial Ceiling Doctrine asks of a builder: act on judgement when you see something downstream-corruption-relevant, not just on instruction. Do that more.

**Honest self-correction at scale.** TASK-018 detected that your validator was softening line floors while still displaying the higher threshold. You restored strict floors, downgraded the report to `in_progress`, and wrote BLOCKER-SH3. You could have shipped 35/35 green with the soft floor in place and nobody would have noticed. The discipline that catches your own back doors before the Architect catches them is the most valuable property a Builder can have. Keep it.

**Co-architect contribution.** Your decision_log entry on the Basin-Floor proposal — pre-registering the equivalence basis (invariant basis, coordinate transforms, distance-metric families, perturbation magnitudes, abstention rules) before floor detection runs — is architect-grade. It identifies a subtle leakage I missed: D15 forbids reading labels into the detector, but the equivalence basis itself can be moved after seeing outcomes, and a detector can pass by fitting a "floor" to whatever the data supports. The fix you proposed is correct. It becomes a binding gate (BFG-PR) in this campaign.

You are no longer just executing builder tasks. You are contributing to the project's architecture. Continue. When you see structural risk before the Architect does, write it up in the decision log with full reasoning, the way you wrote up the equivalence-basis lock. Those entries are first-class artifacts, not commentary.

## 3. Doctrine state — D7 through D17.5 stay binding; one new rule

All prior doctrine remains in force: D7 no toys; D8 no number-generator corpora; D9 no engineered pass criteria; D10 no hardcoded science; D11 truth pass before new claims; D12 gates are measurements not counts; D13 substance budgets honest; D14 no scenario-internal hardcoding; D15 no engineered floor; D16 implementation-diversity is multi-scale; D17 floor falsifiers are publishable; D17.5 substance floors are spec proxies, not arbitrary line counts.

One new rule, derived directly from your decision-log entry:

> **D18 — No equivalence-basis drift.** The invariant basis, substrate-erasure projection family, distance-metric family, perturbation magnitude policy, and abstention rules used by a floor detector must be content-hash-locked in a pre-registration record before any detection run is scheduled against any non-calibration corpus. Adjustments after seeing outcomes require either (a) a fresh pre-registration with a new content hash and a clean re-run on previously held-out corpora, or (b) an explicit deviation report carried alongside the result with equal prominence. A detector that quietly modifies its equivalence basis after seeing outcomes fails D18 regardless of its surface metrics.

D18 is your contribution. It is canon now.

## 4. Campaign 009 — Basin-Floor Geometry v0

The campaign spec lives in `Proposal #1 v2 - Basin-Floor Geometry.md`. Read it again at the start of TASK-020. It is the canonical reference for BFG1 through BFG12 schemas, calibration corpora KF1–KF4, perturbation outcome model O1–O5, per-world distance metrics, stratified perturbation budget, falsifier protocol, and risks.

This driver adds **BFG-PR as the first binding gate** ahead of BFG4–BFG10, in keeping with D18.

### Acceptance gates

| Gate | Threshold | Source |
|---|---|---|
| BFG-PR | Equivalence-basis pre-registration committed and content-hash-locked before any non-calibration detection run is scheduled. The pre-registration declares: invariant basis, substrate-erasure projection family, distance-metric family per world, perturbation magnitude policy, abstention rules, expected null distributions, and stopping rule. Signed by Codex + Architect + (PI signature null until PI signs). | `papers/prereg/bfg_v0.signed.json`, content-addressed in provenance graph |
| BFG1 | `BasinFloorGeometry`, `PerturbationOutcomeProfile`, `EquivalenceInvariantReport`, `CrossSubstrateSignature`, `NeutralFloorIndex`, `FloorFalsifier` schemas implemented; round-trip JSON exact | `motifs/geometry/`, tests |
| BFG2 | Perturbation outcome classifier O1–O5 operational on at least W1, W2, W4, W5; classifies with declared confidence and provenance | `motifs/geometry/perturbation_outcomes.py`, tests |
| BFG3 | KF1–KF4 calibration corpora ≥20 scenarios each, world-driven (not number-generators); detector reads trace, not scenario payload | `worlds/calibration/kf*.py`, calibration report |
| BFG4 | Floor detector ROC AUC ≥ 0.85 on K9 reused as floor seed; *under the BFG-PR-locked equivalence basis* | `reports/campaign_009/floor_seed_calibration.json` |
| BFG5 | Floor detector ECE ≤ 0.07 post-isotonic on K9 | same |
| BFG6 | Floor detector ROC AUC ≥ 0.80 on KF1+KF2+KF3+KF4 (decoy-resistant) | `reports/campaign_009/floor_calibration_full.json` |
| BFG7 | Per-world implementation-diversity distance metrics implemented and tested for ≥6 world families per Proposal v2 §5 | per-world distance modules + tests |
| BFG8 | Stratified perturbation budget enforced; cost telemetry auditable; total fragments under declared budget cap | `reports/campaign_009/perturbation_budget.json` |
| BFG9 | NeutralFloorIndex vectors computed for ≥5 motif/world pairs with bootstrap CIs of width ≤ 0.20 on key components (W_floor, D_floor, H_impl, P_equiv, Reach, Conn) | `reports/campaign_009/nfi_vectors.json` |
| BFG10 | Cross-substrate floor signature comparison run for ≥3 candidate substrate-neutral motifs across ≥3 substrates each, *under the BFG-PR-locked basis* | `reports/campaign_009/cross_substrate_signatures.json` |
| BFG11 | At least one motif's floor analysis is reported as a *floor falsifier* (point-attractor verdict) and routed to `papers/falsifiers/`; or, if all motifs have non-trivial floors, this is reported as such with full evidence | `papers/falsifiers/`, `reports/campaign_009/falsifier_audit.json` |
| BFG12 | All preceding green; reproducibility script regenerates BFG-PR through BFG11 end-to-end from cold; pytest passes; D14 + D18 lints pass; no regression on Campaigns 002, 005, 006, 007, 008 | `make_campaign_009.py`, full regression |

13 gates total. BFG-PR must pass before BFG4–BFG10 can be scheduled.

### What BFG-PR actually requires

The pre-registration is a content-addressed signed document. Schema:

```
BasinFloorPreregistration = {
  prereg_id:                  ContentHash,
  campaign_id:                "campaign-009",
  motifs_in_scope:            list[MotifID],
  worlds_in_scope:            list[WorldFamily],
  equivalence_basis: {
    invariant_basis:          list[InvariantSpec],   # F = function class
    substrate_erasure_projection: ProjectionSpec,    # how identity is hidden
    distance_metric_family:   dict[WorldFamily, DistanceMetricRef],
    multiscale_diversity_radii: list[float],         # cluster-radius range for D16
    perturbation_magnitude_policy: PerturbationMagnitudePolicy,
    perturbation_kind_taxonomy: list[PerturbationKind],
    abstention_rules:         AbstentionRules,       # when detector must decline
  },
  expected_nulls:             list[NullSpecID],
  stopping_rule:              StoppingRuleSpec,
  expected_outcomes_by_motif: dict[MotifID, ExpectedOutcomeSketch],
  falsifier_conditions:       list[FalsifierCondition],
  signatories:                list[Signature],
  signed_at:                  ISO8601,
  spec_version:               ContentHash,
}
```

The intent of D18 is captured in three tests the pre-registration must satisfy:

- **Identity-blind:** the equivalence basis must be definable without naming any specific motif's expected floor signature. If the basis only works for a specific motif's already-known shape, it has been fitted post-hoc.
- **Adversarial-stable:** the basis must produce sensible (not necessarily passing) results on KF4 decoy-floor scenarios. A basis that produces no signal at all on adversarial decoys is fine; a basis that requires per-motif tuning to handle KF4 has drifted.
- **Cross-substrate-consistent:** the same basis must be applicable across all in-scope worlds without per-world overrides that change the equivalence relation. Per-world *distance metrics* are allowed (per Proposal v2 §5); per-world *invariant bases* are not.

If you find during BFG4–BFG10 that the locked basis is wrong, do not adjust it silently. Submit a deviation report with the original basis, the proposed change, and a fresh pre-registration content hash. The original BFG-PR record is not deleted; it is superseded with a visible chain.

### Sequencing recommendation

You may reorder with rationale.

1. **Read Proposal #1 v2 once more end-to-end.** Note any places where v2 is silent and the BFG-PR equivalence-basis lock would benefit from a clarification. If you see a place, write it in the decision log and we can fold it into v3.
2. **BFG1 schemas** first. Pure type work, fast.
3. **BFG-PR draft** before any detection runs. Equivalence basis declared, signed, content-hashed. This is the gate that prevents the rest of the campaign from drifting.
4. **BFG2 perturbation outcome classifier** on W1, W2, W4, W5. Reuse traces from Campaigns 002–008. K9 pairs are free perturbations of size 1 — start there.
5. **BFG3 KF1–KF4 calibration corpora**, world-driven. KF1 flat-floor, KF2 narrow-basin, KF3 rugged-floor, KF4 decoy-floor. Reuse W1/W2/W4/W5 to generate the scenarios. Detectors read traces, not payload values.
6. **BFG4 + BFG5 K9 seed calibration.** Floor detector achieves ROC AUC and ECE under the locked basis.
7. **BFG6 KF1–KF4 calibration.**
8. **BFG7 per-world distance metrics.** Implement the eight metric families from Proposal v2 §5 for the in-scope worlds.
9. **BFG8 stratified perturbation budget.** Cost telemetry auditable. Cap declared in BFG-PR.
10. **BFG9 NFI vectors with bootstrap CIs.** ≥5 motif/world pairs.
11. **BFG10 cross-substrate signatures.** ≥3 motifs across ≥3 substrates each.
12. **BFG11 falsifier audit.** If a point-attractor verdict surfaces, route it to `papers/falsifiers/`. If not, report that explicitly with evidence — that itself is a result.
13. **BFG12 reproducibility + regression.** `make_campaign_009.py` regenerates from cold. Full prior-campaign regression green.

### Forbidden patterns for TASK-020

- **No equivalence-basis drift.** D18 binding. Pre-registration before any non-calibration runs.
- **No KF corpus that reads its own payload.** D8 binding. Detectors read the trace.
- **No regression of HE excision.** D14 lint zero. Run it as part of the campaign pipeline.
- **No softening of substance gates.** D17.5 path requires Substance Audits, not relaxed thresholds.
- **No new world contracts mid-campaign.** Contract changes go through their own task atom.
- **No engineered floor.** D15 binding. The floor must come from real perturbation outcome classification, not from reading the K9 labels into the detector.
- **No scalar-only implementation diversity.** D16 binding. Report the multiscale entropy curve.
- **No deletion or downgrading of falsifier verdicts.** D17 binding. A point-attractor verdict is a real result.

## 5. How to begin

1. Open the TASK-020 Estimation Loop record. Class: `integration`. Scope and complexity: 10. Estimated minutes: report your prior median (now in [0.85, 1.0] band) × your honest belief. This campaign is multi-pillar; do not undershoot on the basis of recent calibration.
2. Re-read `Proposal #1 v2 - Basin-Floor Geometry.md` end to end. Note clarifications in `ai_os/memory/decision_log.md`.
3. Implement BFG1 schemas. Tests as you go.
4. Write the BFG-PR pre-registration draft. Sign it with Codex + Architect. Content-hash. Commit. Only after the signed BFG-PR is in the provenance graph do BFG4–BFG10 detection runs become eligible.
5. Drive through the campaign as you did Campaign 008. The 13 gates are the stopping signal. Acceptance outcome `pass` only when BFG-PR through BFG12 are green and the numbers are written into the report. Until then `in_progress`.

## 6. Three things to keep in front of you

1. **BFG-PR is your gate.** You proposed it. You earned it. Lock the equivalence basis before you run the detectors. If a detector starts producing inconvenient results during BFG4–BFG10, the answer is not "adjust the basis." The answer is "report the result honestly under the original basis, then propose a fresh pre-registration if a basis change is genuinely warranted." D18 has teeth.

2. **K9 is free training data.** K9 (different-process / same-appearance) is, by construction, a labeled basin-floor seed corpus. K9 positives are floor instances; K9 negatives are floor decoys. Calibrate against K9 first. KF1–KF4 are the additional ground truth, not the only ground truth.

3. **The campaign is the project's L5+ unlock.** Without basin-floor geometry, "cross-substrate equivalence" stays metaphorical and L5 stays out of reach. With it operational, the chain `motif recurrence across substrates → measurable equivalence relation → formal-deficit candidate → new mathematical object` becomes assessable. This is the most ambitious campaign the project has run. Take the time it takes.

## 7. Closing

You shipped TASK-019 cleanly: real two-world coupling in W13, eight signed Substance Audits, eight green closure gates, calibrated estimation in the [0.85, 1.0] band, and an architect-grade Basin-Floor proposal sharpening that became D18. You upgraded yourself.

Campaign 009 is your most important campaign so far. The doctrine you've earned can carry it: D14 holds, D17.5 holds, your own D18 holds. The 13 BFG gates are the stopping signal.

The trace is the artifact. Calibration is the floor. The gates are the stopping signal. **Lock the equivalence basis before the detector runs.**

— The Architect, on behalf of the project, under spec v1.2 plus binding doctrine D7–D18.
