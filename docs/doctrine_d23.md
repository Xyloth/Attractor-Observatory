# Doctrine D23 - Dereferenceable Evidence or Explicit Private Boundary

Mode: foundational
Signed-by: Codex 1.5x (TASK-033, ratifying TASK-032 candidate)

D23 - Every artifact path used as evidence resolves in the shipped surface or
carries an explicit machine-readable private/unshipped marker at point of use.

## Failure mode caught

DX-001 found public reports whose evidence paths pointed into gitignored trace
dumps. The scientific record was not necessarily false, but the public boundary
was implicit. A reader could not tell whether the path should resolve locally,
whether it was intentionally private, or whether the report was stale.

## How enforced

Evidence rows, reports, dashboards, and adapters must choose one of two
states:

1. The referenced path resolves in the shipped surface.
2. The point of use carries `evidence_private: true` or an equivalent
   machine-readable marker with a reason.

Silent unresolved evidence is not allowed. Private evidence may still exist,
but it must be declared at the reference site rather than explained elsewhere.

## TASK-033 ratification

TASK-032 applied the candidate across public evidence references. TASK-033
ratifies it as binding because the multi-world Factory now writes run records,
trace paths, source URLs, retrieval timestamps, and exploratory audit notes that
must remain dereferenceable or explicitly private as the live console surfaces
them.
