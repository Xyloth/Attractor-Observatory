# Campaign 014: Floor Corpus Foundry v0

> **DX-002 public runtime boundary:** References to `formalism/*`, `trace/*`, `worlds/*`, `motifs/*`, or `validation/*` in this document are narrative or private-runtime evidence unless a shipped public file is explicitly linked. The executable implementation is held outside the public branch; citations to private paths are governed by D29 and should be read as `evidence_private: true` / `private_unshipped`, not as public-runnable verification.


Task: TASK-025 / Campaign 014
Status: exploratory
Content hash: `sha256:0525d9a35c4b3018fc997eb50565f3bd9abae6589d9b20bc5fbc20bbdc5906d3`

## Headline

Campaign 014 builds the evidence surface CB-003 proved was missing: W8 cognitive, W11 quasispecies, and W12 symbiogenesis now each have both floor-positive and floor-negative real traces under the locked lens-registry predicate.

- Traces generated: 48
- Step-0-eligible substrates: ['cognitive', 'quasispecies', 'symbiogenesis']
- Substrate-blocked control: `signal_not_distinguishable_after_substrate_blocking` (N_run=10000, p=0.9075092490750925)
- Negative uniform control: `not_evaluable_substrate_confounded`
- L5 candidacy advancement from this corpus: `False`

## Why this exists

TASK-CB-003 showed that pooled floor-connectivity replication can be substrate-confounded when all positive labels live in some substrates and all negative labels live in others. This foundry fixes the corpus, not the statistic: the basis and lens registry remain locked, while the worlds generate within-substrate positive and negative traces.

## Label discipline

Scenario records include `floor_foundry_expected_label` for audit only. The evidence labels are computed solely by `formalism.lens_registry._label_feature_for_motif` on the exported trace. The expected label is checked after the fact and never read by verdict code.

| Substrate | floor=True | floor=False | minority | Step 0 balanced? |
|---|---:|---:|---:|:---:|
| cognitive | 8 | 8 | 8 | True |
| quasispecies | 8 | 8 | 8 | True |
| symbiogenesis | 8 | 8 | 8 | True |

## Substrate-blocked result

Observed statistic: 0.228957
Null mean: 0.24715796352268896
Empirical p: 0.9075092490750925

The observed floor gap does not clear the within-stratum shuffled null; no L5 advancement from this corpus.

## Negative control

The all-negative trace subset intentionally removes every floor-positive trace before running the same blocked-control path. It must stay `not_evaluable_substrate_confounded`; otherwise the control machinery is over-claiming.

All strata are label-uniform; the blocked shuffle is degenerate and cannot evaluate substrate-blind floor signal.

## Gates

| Gate | Passed | Description |
|---|:---:|---|
| C14-1 | True | 48 real W8/W11/W12 traces generated; locked predicate labels match audit-only mechanism expectation. |
| C14-2 | True | Each substrate has both floor labels with minority count >= 8. |
| C14-3 | True | Substrate-blocked control is nondegenerate and ran N=10000. |
| C14-4 | True | All-uniform negative control remains not_evaluable. |
| C14-5 | True | CB-003 adversarial baseline remains methodology_sound. |
| C14-6 | True | Campaign 014 report round-trips and has a content hash. |
| C14-7 | True | Locked basis and lens registry unchanged. |
| C14-8 | True | Blocked-control scientific verdict is machine-readable and aggregate L5 surface matches it. |
| C14-9 | True | All outputs remain exploratory; no claim-bearing promotion attempted. |

## Doctrine notes

- D18 honored: basis and lens registry hashes are checked and unchanged.
- D14 honored: no benchmark-specific answer stamping; floor channel presence is gated by mechanism parameters, not benchmark names.
- Class 11 honored: multi-substrate interpretation uses within-stratum shuffling rather than pooled label balance.
- D21 honored: all outputs are exploratory; no claim-bearing promotion occurs.

## Artifacts

- Report: `reports/campaign_014/floor_corpus_foundry.json`
- Trace root: `reports/campaign_014/traces/`
- Module: `motifs/geometry/multisubstrate/floor_corpus_foundry.py`
- Regenerator: `make_campaign_014.py`
