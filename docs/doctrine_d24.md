# Doctrine D24 - Freshness-Bound Sidecars

Mode: foundational
Signed-by: Codex 1.5x (TASK-033, ratifying TASK-032 candidate)

D24 - Snapshot and cache artifacts used for AI handoff bind to branch, commit,
generation command, generation timestamp, and freshness status.

## Failure mode caught

DX-001 found `state_latest.json` could look current while the underlying branch
or commit had moved. That made a sidecar handoff artifact easy to over-trust.

## How enforced

Sidecars that summarize project state must include generation metadata:

1. branch name
2. commit SHA
3. generation command
4. generation timestamp
5. freshness status

When the underlying state moves, the sidecar reports stale status instead of
claiming `ok`. Consumers may still read stale sidecars, but the staleness must
be visible and machine-readable.

## TASK-033 ratification

TASK-032 made Control Room snapshots freshness-bound. TASK-033 extends the
same rule to live Factory run sidecars: `latest_state.json`, `latest_run.json`,
and content-hashed run records are explicit generated artifacts, not evidence
by themselves.
