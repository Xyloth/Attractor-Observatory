# Multi-Substrate Floor Connectivity Test (v2: substrate-suitability-gated)

Task: TASK-CB-002 (Claude Builder Session 002)
Status: exploratory
Schema: `MultisubstrateFloorConnectivity.v2`
Content hash: `sha256:1dbe5ed2ee1ca02f71850a04f0c537de234e57b53c5e61d736d8e91f742a24fc`
Supersedes: TASK-CB-001 v1 report (`reports/campaign_013/multisubstrate_floor_connectivity.json`); v1 record preserved.

## Step 0 corpus overview (binding gate)

Candidate substrates surveyed: **8** (['cognitive', 'crn', 'digital', 'field', 'morphogenesis', 'protocell', 'quasispecies', 'symbiogenesis']).
Substrates **passing** Step 0 (threshold logic applicable): **0** ([]).
Substrates **failing** Step 0 (threshold logic skipped): **8** (['cognitive', 'crn', 'digital', 'field', 'morphogenesis', 'protocell', 'quasispecies', 'symbiogenesis']).

Step 0 status per substrate:

| Substrate | Step 0 status | Source bucket | Purpose |
|---|---|---|---|
| `cognitive` | `motif_present_uniform_positive` | campaign_008/traces/W8=4, campaign_010/traces/W8=8 | floor_positive_candidate |
| `crn` | `motif_absent_in_corpus` | campaign_009/k9=16, campaign_009/kf/KF1=0, campaign_009/kf/KF2=0, campaign_009/kf/KF3=10, campaign_009/kf/KF4=10 | BFG_specified |
| `digital` | `motif_absent_in_corpus` | campaign_009/kf/KF1=0, campaign_009/kf/KF2=0, campaign_009/kf/KF3=10, campaign_009/kf/KF4=10 | BFG_specified |
| `field` | `motif_absent_in_corpus` | campaign_007/w3_traces=8 | deliberate_negative_control |
| `morphogenesis` | `motif_absent_in_corpus` | campaign_009/kf/KF1=0, campaign_009/kf/KF2=0, campaign_009/kf/KF3=10, campaign_009/kf/KF4=10 | BFG_specified |
| `protocell` | `motif_absent_in_corpus` | campaign_009/kf/KF1=0, campaign_009/kf/KF2=0, campaign_009/kf/KF3=10, campaign_009/kf/KF4=10 | BFG_specified |
| `quasispecies` | `motif_present_uniform_positive` | campaign_008/traces/W11=4, campaign_010/traces/W11=6 | floor_positive_candidate |
| `symbiogenesis` | `motif_present_uniform_positive` | campaign_008/traces/W12=4, campaign_010/traces/W12=6 | floor_positive_candidate |

**Binding discipline:** Class 10 / candidate D22 (presence-gated replication): a replication verdict is claim-bearing only if the target motif is present in the corpus AND label distribution has enough variation to make the threshold test falsifiable. Step 0 routes ineligible substrates to the threshold_mechanical / not_evaluable_* lane; threshold logic does not run on them.

## Aggregate verdict

- **threshold_verdict** (locked Campaign 013 logic, D18-protected): `no_threshold_logic_ran`
- **scientific_verdict** (applicability-gated read): `not_evaluable_no_substrate_suitable`
- **claim_eligible:** `False`
- **l5_candidacy_advancement:** `False`

Step 0 substrate-suitability check failed on every substrate evaluated (8 of 8). Threshold logic was not applicable to any corpus. Per binding Class 10 discipline (and candidate D22), the aggregate scientific verdict is not_evaluable. No L5 candidacy advancement. claim_eligible is structurally False until both (a) at least two Step-0-eligible substrates produce replicated verdicts and (b) the source worlds advance to claim_ready_densified under D21. Step 0 failure breakdown: cognitive=motif_present_uniform_positive, crn=motif_absent_in_corpus, digital=motif_absent_in_corpus, field=motif_absent_in_corpus, morphogenesis=motif_absent_in_corpus, protocell=motif_absent_in_corpus, quasispecies=motif_present_uniform_positive, symbiogenesis=motif_present_uniform_positive

## What this measures

TASK-CB-001 returned threshold-mechanical `uniform_replication` on W3/W4/W5 corpora where the floor motif was absent from every substrate's labels (CODEX_AUDIT_001 confirmed; Class 10 ratified by Architect Claude with candidate doctrine D22 'presence-gated replication'). TASK-CB-002 replaces the W3/W4/W5 corpus with:

- Architect-specified Campaign 009 BFG perturbation corpus (crn / digital / morphogenesis / protocell)
- Floor-positive candidates surfaced by an extended Step 0 survey across `reports/` (cognitive / quasispecies / symbiogenesis)
- A deliberate negative-control substrate (W3 field) so the Step 0 plumbing self-tests on a known-absent corpus

Step 0 substrate-suitability runs *before* any threshold logic. The threshold output (locked under D18) is preserved as `threshold_verdict`; the scientifically-meaningful read (gated on Step 0 and on D21 densification) is `scientific_verdict`. CODEX_AUDIT_001 P2 fix is implemented: threshold and scientific verdicts are sibling fields, not nested, so machine parsers cannot accidentally read one without the other.

## Locked instruments (verified before analysis)

- Equivalence basis hash: `sha256:ce9e243429a69b0b23c84ce6ca4685f89efbb83e94532ebdb125f80949092dbb` (basis_unchanged: True)
- Lens registry file SHA-256: `sha256:7c325d9367d873ede832f78a73ddffd2f9e5f5ca879a09a296bc19b2e950a7e8` (matches expected `sha256:7c325d9367d873ede832f78a73ddffd2f9e5f5ca879a09a296bc19b2e950a7e8`: True)
- N7 lens-permutation: N=1000, seed=13013
- Verdict thresholds: formal_gap > 0.20 AND empirical_p < 0.05 = replicated. Locked under D18.

## Held-out evidence audit

Checked **136** trace paths against the Campaign 010 deficit-map preregistration 
(`papers\prereg\deficit_map_v0.signed.json`, 141 training rows). 
Overlap count: **0**. Held-out clean: **True**.

## Per-substrate results

| Substrate | Step 0 status | threshold_verdict | scientific_verdict | claim_eligible | l5_advancement |
|---|---|---|---|:---:|:---:|
| `cognitive` | `motif_present_uniform_positive` | `skipped` | `not_evaluable_label_uniform` | False | False |
| `crn` | `motif_absent_in_corpus` | `skipped` | `not_evaluable_motif_absent` | False | False |
| `digital` | `motif_absent_in_corpus` | `skipped` | `not_evaluable_motif_absent` | False | False |
| `field` | `motif_absent_in_corpus` | `skipped` | `not_evaluable_motif_absent` | False | False |
| `morphogenesis` | `motif_absent_in_corpus` | `skipped` | `not_evaluable_motif_absent` | False | False |
| `protocell` | `motif_absent_in_corpus` | `skipped` | `not_evaluable_motif_absent` | False | False |
| `quasispecies` | `motif_present_uniform_positive` | `skipped` | `not_evaluable_label_uniform` | False | False |
| `symbiogenesis` | `motif_present_uniform_positive` | `skipped` | `not_evaluable_label_uniform` | False | False |
| **pooled_all_substrates** | `motif_present_balanced` | `replicated` | `replicated` | False | True |

## Per-substrate Step 0 detail

| Substrate | floor=T | floor=F | minority | balance | Step 0 verdict |
|---|---:|---:|---:|---:|---|
| `cognitive` | 12 | 0 | 0 | 0.000 | `motif_present_uniform_positive` |
| `crn` | 0 | 36 | 0 | 0.000 | `motif_absent_in_corpus` |
| `digital` | 0 | 20 | 0 | 0.000 | `motif_absent_in_corpus` |
| `field` | 0 | 8 | 0 | 0.000 | `motif_absent_in_corpus` |
| `morphogenesis` | 0 | 20 | 0 | 0.000 | `motif_absent_in_corpus` |
| `protocell` | 0 | 20 | 0 | 0.000 | `motif_absent_in_corpus` |
| `quasispecies` | 10 | 0 | 0 | 0.000 | `motif_present_uniform_positive` |
| `symbiogenesis` | 10 | 0 | 0 | 0.000 | `motif_present_uniform_positive` |

## Negative-control self-test

Per Codex audit precondition #3, a deliberate motif-absent substrate (W3 `field` from `reports/campaign_007/w3_traces/`) is included in the candidate set. It must produce `scientific_verdict: not_evaluable_motif_absent` with `threshold_verdict: skipped` (not `replicated`). This self-tests the Step 0 plumbing.

- `field` step_0_status: `motif_absent_in_corpus`
- `field` threshold_verdict: `skipped`
- `field` scientific_verdict: `not_evaluable_motif_absent`
- **Self-test passed:** True

## Implications for L5 candidacy

- Aggregate scientific_verdict: `not_evaluable_no_substrate_suitable`
- Aggregate l5_candidacy_advancement: `False`

Step 0 substrate-suitability check failed on every substrate evaluated (8 of 8). Threshold logic was not applicable to any corpus. Per binding Class 10 discipline (and candidate D22), the aggregate scientific verdict is not_evaluable. No L5 candidacy advancement. claim_eligible is structurally False until both (a) at least two Step-0-eligible substrates produce replicated verdicts and (b) the source worlds advance to claim_ready_densified under D21. Step 0 failure breakdown: cognitive=motif_present_uniform_positive, crn=motif_absent_in_corpus, digital=motif_absent_in_corpus, field=motif_absent_in_corpus, morphogenesis=motif_absent_in_corpus, protocell=motif_absent_in_corpus, quasispecies=motif_present_uniform_positive, symbiogenesis=motif_present_uniform_positive

## Codex mentoring instructions internalized

Per CODEX_AUDIT_001 §"Mentoring Instructions For Claude Builder" (12 instructions), this build implements:

1. Applicability gates before threshold gates — Step 0 substrate-suitability runs first (binding).
2. `threshold_verdict` separated from `scientific_verdict` at every level (per-substrate, pooled, aggregate).
3. Caveats encoded as machine-readable JSON fields (`scientific_verdict`, `claim_eligible`, `l5_candidacy_advancement`), not just prose.
4. Uniform labels treated as a stop sign — both `motif_absent_in_corpus` and `motif_present_uniform_*` Step 0 statuses skip threshold logic.
5. Caveats made hard to over-claim by elevating them to first-class report fields.
6. Negative-control self-test included (W3 `field`).
7. Borrowed private helpers documented with assumed-set docstring at the top of `floor_connectivity.py`.
8. Skipped-vs-passed gates explicit per substrate.
9. BUILD_LOG entries record next-substrate recommendations precisely.
10. Default to `exploratory_not_claim_bearing` — `claim_eligible: False` everywhere; promotion requires D21 densification audit.
11. Three outcomes pre-registered: replicated, falsified, not-applicable (`scientific_verdict` taxonomy includes `replicated` / `falsified` / `weakened` / `different_result` / `not_evaluable_*`).
12. Self-audit step happened before declaring complete — Step 0 survey ran before refactor began.

## Forbidden patterns honored

- **D18 (no equivalence-basis drift):** locked basis hash + lens registry SHA-256 verified before analysis ran.
- **D9 / Class 6 (engineered passing):** thresholds taken from Campaign 013 unchanged; no per-substrate threshold tuning.
- **D15 / Class 1 (static-input contamination):** lens evaluations consume trace state and events; no lens reads substrate label or benchmark name.
- **D21 (densification before claim-bearing):** all output `mode_tag: exploratory`; `claim_eligible: False` everywhere structurally.
- **Class 10 / candidate D22 (presence-gated replication):** Step 0 substrate-suitability gate runs before threshold logic; substrates failing Step 0 produce `not_evaluable_*` scientific verdicts.
- **No new lenses, no new motifs, no ontology registry mutation.**

## Provenance

- Module: `motifs/geometry/multisubstrate/floor_connectivity.py` (v1 + v2 helpers); `motifs/geometry/multisubstrate/run.py` (v1 `build()` + v2 `build_v2()`)
- Report v2: `reports/campaign_013/multisubstrate_floor_connectivity_v2.json`
- Report v1 (preserved as TASK-CB-001 record): `reports/campaign_013/multisubstrate_floor_connectivity.json`
- Methods doc: `papers/methods/MULTISUBSTRATE_FLOOR_CONNECTIVITY.md`
- Locked basis hash (Campaign 009 BFG-PR): `sha256:ce9e243429a69b0b23c84ce6ca4685f89efbb83e94532ebdb125f80949092dbb`
- Locked lens registry hash (Campaign 010): `sha256:7c325d9367d873ede832f78a73ddffd2f9e5f5ca879a09a296bc19b2e950a7e8`
- Spec version: `sha256:492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729`
- Mode tag: `exploratory`

## Cross-audit

Hand-off: CODEX_AUDIT_002. Audit targets per CLAUDE_BUILDER_INITIATION.md §3 cross-audit triangle: 
(a) Verify Step 0 implementation matches the binding Class 10 / D22 wording; 
(b) Re-run `python -m motifs.geometry.multisubstrate.run` (v1, unchanged) AND `python -c "from motifs.geometry.multisubstrate.run import build_v2; build_v2()"` (v2) and confirm byte-identical content_hash on both; 
(c) Verify `claim_eligible: True` is structurally impossible without D21 densification (it should be False on every substrate even if scientific_verdict is replicated); 
(d) Verify the W3 field negative-control self-test passes (Step 0 routes to `motif_absent_in_corpus`, threshold_verdict is `skipped`, scientific_verdict is `not_evaluable_motif_absent`); 
(e) Confirm no D14-style scenario-internal hardcoding inside the analysis path; 
(f) Sanity-check the borrowed-private-helper docstring at the top of `floor_connectivity.py` matches the actual assumptions imported from `validation.campaign013`.

-- Claude Builder, on behalf of the project, under spec v1.2 plus binding doctrine D7 through D21 plus candidate D22.
