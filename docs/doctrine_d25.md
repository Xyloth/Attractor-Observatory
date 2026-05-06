# Doctrine D25 - Public Verification Honesty

Mode: foundational
Signed-by: Codex 1.5x (TASK-033, ratifying TASK-032 candidate)

D25 - Public docs may not claim public tests, screenshots, reproducibility
scripts, or shipped evidence unless those files are present in the public
branch or explicitly scoped private.

## Failure mode caught

DX-001 found public documentation claiming verification surfaces that were not
actually present in the shipped branch. That is a documentation-level false
positive: the project can have private tests, but the public docs must name
them as private rather than implying the reader can run them.

## How enforced

Any public-facing claim about verification must match repository reality:

1. If a test exists publicly, name the path.
2. If a screenshot exists publicly, name the path.
3. If a script is private, say it is private.
4. If a report depends on private traces, mark that boundary under D23.

## TASK-033 ratification

TASK-032 corrected public verification claims. TASK-033 ratifies D25 because
the live Factory console creates new public-facing UX and run-history surfaces:
every visible result must be backed by a persisted run record, trace, or honest
empty state.
