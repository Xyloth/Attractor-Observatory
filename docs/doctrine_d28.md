# Doctrine D28 - Release Boundary

Mode: foundational  
Signed-by: Codex 1.5x (TASK-DX-002-FIX), under PI/Architect ratification

D28 - Plans, doctrines, contracts, and methodology artifacts are not audit-live
until committed at the public target SHA. Untracked working-tree artifacts may
not be cited as ratified evidence. Pre-ratification artifacts must declare an
`audit_live_at` or equivalent public-SHA boundary; before that SHA, they are
exploratory drafts and not fail-closed enforcement inputs.

## Failure mode caught

DX-002 found D27 and the measurability recovery plan discussed as if live while
they were dirty working-tree artifacts outside frozen public HEAD `a35aab1`.
The artifact content was real, but not part of the audited release boundary.

## How enforced

Release-facing reports distinguish:

- draft artifacts in the working tree
- committed artifacts in the public branch
- private artifacts outside the public branch

Control and falsification passes evaluate committed release surfaces. Drafts may
guide work, but they do not satisfy public doctrine, plan, or evidence claims
until committed at the target SHA.
