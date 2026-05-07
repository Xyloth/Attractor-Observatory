# Floor Connectivity Predicate Split

> **DX-002 public runtime boundary:** References to `formalism/*`, `trace/*`, `worlds/*`, `motifs/*`, or `validation/*` in this document are narrative or private-runtime evidence unless a shipped public file is explicitly linked. The executable implementation is held outside the public branch; citations to private paths are governed by D29 and should be read as `evidence_private: true` / `private_unshipped`, not as public-runnable verification.


Task: TASK-MOTIF-IMPL
Mode: exploratory; no claim-bearing promotion

## Summary

`motif.floor_connectivity.draft` now has two distinct historical objects:

1. **BFG predicate** - the clean Basin-Floor Geometry predicate. It reads
   perturbation-equivalence fiber evidence: `neutral_floor_index`,
   `perturbation_outcome`, and `projection_basis`.
2. **C020/C014 label function** - the deprecated surface-key predicate. It read
   `neutral_component_fraction`, `nested_lineage_edges`, `attention_entropy`, and
   `neutral_percolation_event` through `formalism.lens_registry._process_flags`.

The BFG predicate is the active MotifContract.v2 predicate. The C020/C014 label
function is no longer an active floor-connectivity predicate; it can only be used
as a historical candidate-tier detector surface.

## BFG Predicate

The BFG predicate asks whether implementation perturbations remain connected
inside equivalence fibers that preserve function and declared invariants. The
implemented fields are:

- `W_floor`
- `P_equiv`
- `L_func`
- `I_inv`
- `Reach`
- `Conn`

Rows can arrive as a direct `neutral_floor_index` object or as older Campaign 009
calibration rows carrying `outcome` plus `projection_basis`. In both cases, the
predicate reads quotient/fiber evidence and never event tokens.

## Deprecated C020/C014 Label Function

The deprecated function was:

```text
formalism.lens_registry._label_feature_for_motif("motif.floor_connectivity.draft", trace)
```

For floor connectivity, that function called `_process_flags` and returned true
when it saw any of these surface features:

- state key `neutral_component_fraction`
- state key `nested_lineage_edges`
- state key `attention_entropy`
- event token `neutral_percolation_event`

Those features are surface vocabulary, not BFG quotient/fiber evidence. They are
now forbidden evidence for the active motif predicate.

## Historical Campaign Check

The p = 0.9075092490750925 substrate-blocked death is recorded in:

- `reports/campaign_014/floor_corpus_foundry.json`
- `papers/methods/FLOOR_CORPUS_FOUNDRY_C014.md`

That report's `label_audit.label_source` is:

```text
locked _label_feature_for_motif; scenario expected label is audit-only
```

Therefore the historical p = 0.9075 result did **not** evaluate the BFG predicate.
It evaluated the deprecated C014/C020-style surface-key label function. The
result remains a valid falsification of that surface-key detector path, but it
does **not** stand as a death of the BFG floor-connectivity predicate.

Some public/project prose later described this as a Campaign 016 death. The
artifact with the p-value is Campaign 014. Campaign 016 carried the low-level
Factory and detector-coverage audit; it did not supply the p = 0.9075
substrate-blocked floor predicate test.

## TASK-MOTIF-IMPL Status

TASK-MOTIF-IMPL implements `evaluate_floor_connectivity` as the BFG predicate and
adds an adversarial control proving C020-style surface keys alone return
`insufficient_evidence`. The new Campaign 023 rerun uses Campaign 009 BFG
calibration rows for floor connectivity and marks the result exploratory.

Because the Campaign 014 p = 0.9075 death was run against the deprecated label
function, the active BFG floor predicate must be treated as re-opened at
operational exploratory tier, not claim-bearing. It requires detector-side
Destroyer controls before any promotion.
