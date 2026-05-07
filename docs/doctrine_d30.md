# Doctrine D30 - Freshness Computed At Read

Mode: foundational  
Signed-by: Codex 1.5x (TASK-DX-002-FIX), under PI/Architect ratification

D30 - Stored freshness fields such as `freshness_status: current` are advisory
only. Any consumer that depends on freshness must recompute it at read time
against the current HEAD and current branch. Persistence layers may cache
freshness for performance, but read paths must surface staleness when the
underlying state has changed.

## Failure mode caught

DX-002 found `control_room/snapshots/state_latest.json` claiming
`freshness_status: current` while its generation binding pointed at a different
branch/commit than the audited HEAD. A cached sidecar status hid real staleness.

## How enforced

`control_room.snapshot.load_latest()` and `load_prior()` bind snapshot freshness
at read time. Consumers should call the freshness-binding path instead of
trusting persisted freshness fields. Persisted snapshots may retain advisory
freshness metadata, but display and AI-handoff surfaces must recompute.
