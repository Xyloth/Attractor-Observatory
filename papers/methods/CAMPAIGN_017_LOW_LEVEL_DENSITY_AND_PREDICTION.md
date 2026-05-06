# Campaign 017 - Low-Level Density Falsifiers and Upward Prediction

Campaign 017 tests whether the W-1 and W0 density-ready label survives falsifier pressure before it is used for next-level bridge planning.

## Inputs

- Source report: `reports/campaign_016/full_report.json`.
- Preserved signal: Campaign 016 raw formal-lens result remains 96/96 declined and 0/96 nondeclined.
- Output mode: all Campaign 017 artifacts are `exploratory`; `claim_eligible` is false.

## Density Falsifiers

- W-1 `atomic_molecular_primitives`: ready_after_falsifiers=True (5/5 tests passed).
- W0 `math_primitives`: ready_after_falsifiers=True (5/5 tests passed).

Cross-world controls:
- raw_96_of_96_decline_preserved: passed=True.
- source_native_adversarial_controls_still_green: passed=True.
- projection_bridge_not_finding: passed=True.

## Upward Predictions

These are bridge-evaluability predictions, not motif-positive predictions. Projection counts are kept separate from finding fields.

- W-1 `atomic_molecular_primitives` -> W1 `crn`: threshold=30 bridge nondeclines; ready_for_next_campaign=True.
- W0 `math_primitives` -> W1 `crn`: threshold=30 bridge nondeclines; ready_for_next_campaign=True.

## Factory Recovery

- Atomic write path exercised: `reports\campaign_017\recovery_fixture\valid_artifact.json`.
- Recovery checked 2 JSON artifacts; quarantined 1 corrupt artifact.
- Recovery passed: True.

## Doctrine Candidates Proposed

- Bridge diagnostics should have a mandatory sibling `claim_eligible=false` field until a ratified promotion doctrine exists.
- Density-ready substrate labels should require explicit negative controls for missing axes, missing source provenance, and restricted licenses before they feed upward predictions.
- Factory persistence should treat corrupt partial JSON as quarantine-and-audit, never best-effort parse or overwrite.

## Parked

- No live source refresh was performed.
- No W1/W9/W10 target-world traces were generated; Campaign 017 only selects the next bridge target and falsifiers.
- No biology-level adapters or claim-bearing promotions were added.
