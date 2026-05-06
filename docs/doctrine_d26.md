# Doctrine D26 - Predicate-Lens Independence

Mode: foundational
Signed-by: James Dye (PI), Architect Claude, Codex 1.5x (TASK-MOTIF-IMPL)

D26 - A motif predicate and the detector/lens used to evaluate it must declare
their source-object maps before a claim-bearing run. The pair is classified by
source-object comparison:

- CLEAN: predicate and lens read disjoint source objects.
- PARTIAL: predicate and lens read the same source object but disjoint fields;
  the shared object must pass an ablation check before use.
- BAD: predicate and lens read at least one identical source-object field; the
  lens is excluded from claim-bearing evidence for that motif.

## Failure mode caught

Campaign 020 produced five motif survivors under substrate-blocked permutation,
but the locked label function and the graph-lens detector shared event-token and
state-key surfaces. The control blocked substrate identity, not predicate-detector
surface coupling. D26 makes that coupling explicit before the run rather than
discovering it after a suspicious survivor count.

## How enforced

Every MotifContract.v2 record carries:

1. `predicate_source_object_map`
2. per-lens `source_object_map`
3. `derive_independence_verdict(predicate_som, lens_som)`
4. ablation results for every PARTIAL cell

Claim-bearing promotion is forbidden if the primary evidence path is BAD, if a
PARTIAL cell collapses after ablation, or if the predicate verdict changes under
event-token/state-key/payload-key/generator-ID adversarial transforms.

## TASK-MOTIF-IMPL ratification

TASK-MOTIF-IMPL implements the v2 contract schema, semantic predicates for all
six motifs, adversarial controls, D26 source-object-map audits, and a new
substrate-blocked rerun. The rerun remains exploratory: surviving motifs queue a
Destroyer pass and do not promote while detector independence is still being
stress-tested.
