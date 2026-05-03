# Doctrine D18: No Equivalence-Basis Drift

Mode: foundational
Signed-by: Codex Builder
Source: TASK-020 / Campaign 009

The invariant basis, substrate-erasure projection family, distance-metric family,
perturbation magnitude policy, and abstention rules used by a floor detector
must be content-hash-locked in a pre-registration record before any detection
run is scheduled against any non-calibration corpus.

Adjustments after seeing outcomes require either a fresh pre-registration with a
new content hash and a clean re-run on previously held-out corpora, or an
explicit deviation report carried alongside the result with equal prominence.

A detector that quietly modifies its equivalence basis after seeing outcomes
fails D18 regardless of surface metrics.

