# Doctrine D27 - Substantive Lens Recovery

Mode: foundational  
Signed-by: James Dye (PI), Architect Claude, Codex 1.5x (TASK-MEAS-PLAN / TASK-DX-002-FIX)

D27 - A BAD motif-lens cell is not recovered by renaming a detector or moving
the same computation behind a new interface. A recovered lens must demonstrate a
substantive source-object split from the predicate, survive adversarial ablation,
and resist matched-decoy controls. New names or slightly altered fields are not
enough.

## Failure mode caught

Campaign 024 left 33 BAD motif x lens cells. Round-1 recovery planning showed
that several tempting "recoveries" would be cleaner-looking self-matches:
reaction graph / CRNT / Petri checks over the same reaction declarations used by
the autocatalytic closure predicate, and basin-geometry checks over the same BFG
summary fields used by the floor predicate.

## How enforced

Every recovered cell declares:

1. `lens_family_id`
2. `lens_variant_id`
3. `primary_recovery_class`
4. source-object map for the recovered lens
5. allowed claim role
6. source-object holdout controls
7. matched label-opposite decoys

Cells that cannot pass these gates remain `DIAG-ONLY`, `DOMAIN-DECLINE`,
`BAD-ARCH`, or `FORMALISM-REQ`. They may be useful for audit displays, but they
cannot anchor substrate-blocked evidence.
