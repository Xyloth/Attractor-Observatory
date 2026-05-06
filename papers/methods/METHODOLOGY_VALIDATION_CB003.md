# Methodology Validation: TASK-CB-003

Task: TASK-CB-003 (Claude Builder Session 003)
Status: exploratory
Locked instruments: Campaign 009 BFG-PR basis `sha256:ce9e24...`; Campaign 010 lens registry `sha256:7c325d...`. Verified before each control ran.

## Headline finding

- **Adversarial control** (motif.replication_lineage.draft × graph, K2 coverage 0.959240): **`methodology_sound`**. formal_gap = 0.036181, N7 p = 1.000000 (gap threshold 0.20, p threshold 0.05).
- **Substrate-blocked control** (TASK-CB-002 v2 pooled corpus): **`not_evaluable_substrate_confounded`**. Step 0a = FAILED (0 of 11 strata carry both classes).
- **MV11 conditional**: FIRED; deficit_map.json updated with CB-003 history entry for floor_connectivity.

## What this measures

Two methodology validation controls were scoped in `TASK-CB-003_METHODOLOGY_VALIDATION.md` to close open methodology questions before the floor_connectivity candidate's L5 candidacy means anything more than what the Campaign 013 W1/W2-context replication established.

**Question 1 (adversarial control).** Does the Campaign 010 deficit-map methodology have discriminating power -- does it correctly NOT flag a motif that lenses are known to capture? Per Codex's pre-execution outline, the chosen test pair is `motif.replication_lineage.draft × graph` (K2 coverage 0.959240 from `reports/campaign_010/coverage_matrix.json`, the highest-coverage pair in the registry). If this pair returns a HIGH formal_gap on the Campaign 013 independent corpus, the methodology is generating false positives and the floor_connectivity result loses its meaning.

**Question 2 (substrate-blocked control).** Was the TASK-CB-002 v2 pooled-corpus 'replicated' verdict substrate-blind floor signal, or substrate classification dressed up as floor signal? Per CODEX_AUDIT_002 (Class 11 ratification), the v2 pool's label balance was achieved by mixing uniform-positive substrates (cognitive, quasispecies, symbiogenesis) with uniform-negative substrates (BFG + field). Lens encodings are world_family-aware via Campaign 009 BFG-PR's `distance_metric_family`; the pool's 'replicated' verdict could be the lenses correctly classifying world_family rather than detecting a floor-coverage deficit. The substrate-blocked permutation control discriminates between these.

## Adversarial control

**Pair:** `motif.replication_lineage.draft` × `graph` -- highest-coverage-on-K2 pair in the registry per Codex outline.
**K2 step 0a verification (MV3):** coverage_score = 0.959240 ≥ 0.85 floor. PASS.
**Corpus:** Campaign 013 independent corpus from `validation.campaign013._replication_evidence_corpus` -- 156 total rows / 26 target-motif rows.
**Target-motif label distribution in corpus:** {False: 16, True: 10}.
**Target-motif formal_gap:** 0.036181 (vs floor formal_gap 0.354935 on the same corpus for comparison).
**N7 lens-permutation:** N=1000, seed=13013, observed statistic = -0.066085, null mean = -0.005904, empirical p = 1.000000.

**Baselines (Codex outline pitfall):**

| Baseline | Value | Lens beats baseline? |
|---|---:|:---:|
| K2 coverage_score | 0.959240 | (used as Step 0a threshold) |
| Campaign-013 lens coverage_score for motif.replication_lineage.draft × graph | 0.941644 | reference |
| Majority-label baseline (predict the most common class) | 0.538462 | True |
| Substrate-only baseline (predict by world_family alone) | 0.846154 | True |

**Interpretation:** Adversarial target motif.replication_lineage.draft (K2 coverage ≥ 0.85) returns formal_gap = 0.036181 (< 0.2) and N7 empirical p = 1.000000 (> 0.05). The methodology correctly does NOT flag a known-captured motif as a deficit candidate. Discriminating power validated.

## Substrate-blocked control

**Corpus:** TASK-CB-002 v2 pooled corpus (rebuilt via `motifs.geometry.multisubstrate.run._gather_v2_evidence`) -- 816 total evidence rows (136 floor-motif evidence rows; 1088 floor evaluation rows after 8-lens cross product).
**Stratification (Codex outline):** `(world_family, source_bucket)` -- 11 strata.

**Step 0a (within-stratum balance):**

| Stratum | T | F | total | minority | uniform? |
|---|---:|---:|---:|---:|:---:|
| `cognitive::campaign_008/traces` | 4 | 0 | 4 | 0 | True |
| `cognitive::campaign_010/traces` | 8 | 0 | 8 | 0 | True |
| `crn::campaign_009/traces` | 0 | 36 | 36 | 0 | True |
| `digital::campaign_009/traces` | 0 | 20 | 20 | 0 | True |
| `field::campaign_007/w3_traces` | 0 | 8 | 8 | 0 | True |
| `morphogenesis::campaign_009/traces` | 0 | 20 | 20 | 0 | True |
| `protocell::campaign_009/traces` | 0 | 20 | 20 | 0 | True |
| `quasispecies::campaign_008/traces` | 4 | 0 | 4 | 0 | True |
| `quasispecies::campaign_010/traces` | 6 | 0 | 6 | 0 | True |
| `symbiogenesis::campaign_008/traces` | 4 | 0 | 4 | 0 | True |
| `symbiogenesis::campaign_010/traces` | 6 | 0 | 6 | 0 | True |

Strata with both classes: 0 / 11. Step 0a FAILED.

**Step 0b (substrate-blocked permutation):**

Step 0b NOT RUN. Reason: every stratum uniform; within-stratum shuffle is degenerate.

Per Codex's outline: 'If every stratum is uniform, the blocked permutation is degenerate; verdict is `not_evaluable_substrate_confounded`, not "low power" and not "replicated".' Within-stratum shuffle with all-uniform strata is a no-op; the null statistic equals the observed statistic on every iteration; the test cannot distinguish substrate-classification signal from substrate-blind floor signal.

**Observed statistic on original labels:** 0.280332.
**Interpretation:** Every stratum's floor label distribution is uniform (single class within stratum). Within-stratum shuffle is degenerate -- it produces the same labels every permutation, and the null statistic equals the observed statistic on every iteration. The substrate-blocked control therefore CANNOT distinguish substrate-classification signal from substrate-blind floor signal. Per Codex's outline, the verdict is 'not_evaluable_substrate_confounded' (NOT 'replicated', NOT 'low power'). The pooled result from TASK-CB-002 v2 is therefore confirmed as substrate-confounded under the ratified Class 11 discipline; the original 'replicated' threshold output cannot be interpreted as floor-connectivity signal.

## Implications for floor_connectivity L5 candidacy

- Adversarial control validates the methodology's discriminating power: the deficit-map pipeline correctly does not flag a known-captured motif.
- Substrate-blocked control confirms the Class 11 finding from CODEX_AUDIT_002: the v2 pooled-corpus 'replicated' verdict CANNOT be interpreted as substrate-blind floor signal because every stratum's labels are uniform; within-stratum shuffle is degenerate.
- **Net effect on floor_connectivity:** the only substrate-blind confirmation that survives is the Campaign 013 W1/W2-context replication on the deficit-map independent corpus (formal_gap 0.355, p ≈ 0.001). The TASK-CB-002 v2 pooled-corpus result is downgraded to `not_evaluable_substrate_confounded`. L5 candidacy is preserved at its prior level (one-corpus replication; not multi-substrate-blind confirmed).
- **Track B (proper multi-substrate test) is required for further L5 advancement.** That requires fresh substrate-suitable corpora -- traces from at least two substrates that carry both floor-positive AND floor-negative labels within the substrate. None of the existing real-trace fixtures meet this criterion; this is a corpus-generation task for a future campaign.

## MV11 disposition

- Conditional gate fires: **True**
- Deficit map updated: **True**

Appended history entry to `reports/campaign_010/formal_deficit_map.json` at `candidates[motif=floor_connectivity].replication_history`:
```json
{
  "adversarial_verdict": "methodology_sound",
  "artifact_adversarial": "reports/campaign_013/methodology_adversarial_control.json",
  "artifact_substrate_blocked": "reports/campaign_013/substrate_blocked_control.json",
  "campaign_id": "TASK-CB-003",
  "mode": "candidate_methodology_validation_stress_test",
  "rationale": "TASK-CB-003 ran two methodology validation controls. Adversarial control on motif.replication_lineage.draft \u00d7 graph: methodology_sound. Substrate-blocked control on TASK-CB-002 v2 pooled corpus: not_evaluable_substrate_confounded. Per MV11, either of these returning a methodology-problem verdict triggers a downgrade entry in the formal_deficit_map.json replication_history for floor_connectivity.",
  "substrate_blocked_verdict": "not_evaluable_substrate_confounded",
  "task_id": "TASK-CB-003"
}
```

## Forbidden patterns honored

- **D18 (no equivalence-basis drift):** locked basis hash + lens registry SHA-256 verified at the start of each control.
- **D9 / Class 6 (engineered passing):** verdict thresholds taken from Campaign 013 unchanged; no per-control threshold tuning. Adversarial verdict and substrate-blocked verdict are reported as the controls produce them.
- **No new doctrine.** D7-D21 binding; candidate D22 / Class 10 / Class 11 honored as per CLAUDE_BUILDER_INITIATION §4.
- **No basis or registry mutation.** Locked instruments unchanged.
- **No new motifs added to the registry.** Adversarial control uses an existing motif (`motif.replication_lineage.draft`).
- **All output `mode_tag: exploratory`.**
- **No multi-substrate floor_connectivity work beyond what was needed for the substrate-blocked control.** Track B (fresh substrate-suitable corpora) deferred per the task brief.

## Provenance

- Module: `motifs/geometry/multisubstrate/methodology_validation.py`
- Adversarial report: `reports/campaign_013/methodology_adversarial_control.json`
- Substrate-blocked report: `reports/campaign_013/substrate_blocked_control.json`
- Methods doc: `papers/methods/METHODOLOGY_VALIDATION_CB003.md`
- Codex outline (analytical scaffolding): `BUILD_LOG.md` 2026-05-05 talk entry `[Codex Builder -> Claude Builder] [TASK-CB-003 pre-outline]`
- Locked basis hash (Campaign 009 BFG-PR): `sha256:ce9e243429a69b0b23c84ce6ca4685f89efbb83e94532ebdb125f80949092dbb`
- Locked lens registry hash (Campaign 010): `sha256:7c325d9367d873ede832f78a73ddffd2f9e5f5ca879a09a296bc19b2e950a7e8`

## Cross-audit

Hand-off: `CODEX_AUDIT_003`. Audit targets per CLAUDE_BUILDER_INITIATION.md §3 cross-audit triangle: 
(a) verify locked-instrument hashes were not silently bumped between adversarial and substrate-blocked control runs; 
(b) re-run both controls and confirm byte-identical content_hash on each (deterministic seeds); 
(c) verify the adversarial control's K2 step 0a check correctly reads `coverage_score` from `reports/campaign_010/coverage_matrix.json` and applies the 0.85 floor; 
(d) verify the substrate-blocked control correctly stratifies by `(world_family, source_bucket)` and shuffles within strata (not across); 
(e) verify the degenerate-shuffle case correctly returns `not_evaluable_substrate_confounded` rather than 'replicated' or 'low power'; 
(f) verify MV11 fired correctly (or correctly did not fire) given the verdicts; 
(g) confirm no D14-style scenario-internal hardcoding inside the control machinery.

-- Claude Builder, on behalf of the project, under spec v1.2 plus binding doctrine D7 through D21 plus Class 10/11 ratified.
