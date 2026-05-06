# Doctrine D22 — Empty rooms beat stocked rooms with mock data

Mode: foundational
Spec version: sha256:492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729
Signed-by: Architect Claude (TASK-CB-004 / Campaign 015 Phase 0)
Class watch: Class 12 candidate — Decorative Completeness

D22 — Honest absence over decorative completeness. When a Control Room view
(or any read-only project surface) has no real artifact to display, the
view shows the absence honestly — labelled "no data" with the campaign,
artifact, or condition that would populate it — rather than a synthetic
placeholder, fabricated example, or styled mock that could be mistaken for
real signal.

## Failure mode caught

The Observatory Control Room is a sidecar visualization layer. The pull
toward "make the empty room look fuller" — placeholder rows, lorem-ipsum
narrative, plausible-looking but fabricated charts, screenshot-friendly
mock data — creates a class of mistake the project has not yet observed
in scientific code but is structurally invited by visual UI work. Class
12 candidate (Decorative Completeness) is on watch: a UI surface that
appears full-of-content when the underlying artifacts are missing,
exploratory, or contradicted, eroding D11 (truth pass), D17 (honest
falsifiers), and D21 (densification before claim-bearing) at the
presentation layer.

## How enforced

D22 is enforced by **mechanism, not policy**:

1. **Single empty-state component.** Every Control Room room renders
   missing/empty data via exactly one component (`control_room/components/empty_state.py`).
   No room may render a fallback view, a "demo" panel, a placeholder
   table, or a stylised mock without going through this component. The
   component renders a labelled absence (`"no data — campaign needed: X"`,
   `"artifact missing — file: Y"`, `"adapter degraded — reason: Z"`).
2. **Adapter status discipline.** Every adapter under
   `control_room/adapters/` returns a structured payload with `status` in
   `{ok, missing, malformed}`. Rooms route directly: `status == "ok"` →
   render real content; otherwise → empty-state component. There is no
   "fill in plausible defaults" pathway.
3. **No mock data in code unless explicitly labelled `EXAMPLE — NOT REAL`
   on the rendered surface itself.** Code comments are insufficient; the
   user-visible label must carry the disclaimer.
4. **CI / test suite verifies** the empty-state component exists and is
   the unique render path for absent data.

## Operationalization

* Component: `control_room/components/empty_state.py` —
  `render_empty_state(reason, expected_artifact)`.
* Adapter contract: `control_room/adapters/*.py` —
  every adapter returns `{"status": "ok"|"missing"|"malformed", "data":
  ..., "rationale": "..."}`.
* Rooms call the adapter, branch on `status`, and on non-`ok` call
  `render_empty_state(reason=payload["rationale"], expected_artifact=...)`.
  No alternative path is permitted.

## Class 12 — Decorative Completeness (candidate)

A UI surface displays content that *looks* like real project data — populated
tables, plotted charts, narrative text — when the underlying artifact is
missing, malformed, or exploratory. The pattern is structurally similar to
Class 6 (Engineered passing) but at the presentation layer rather than the
verdict layer: the surface produces an impression of completeness that
the data does not warrant.

Sub-patterns to watch for:

* fabricated rows added to a table to fill out an empty section
* lorem-ipsum or placeholder narrative styled to look authored
* synthetic chart data plotted with the same visual language as real data
* "demo mode" toggles that show fake data without a clear `NOT REAL` label
* screenshot-friendly arrangements that depend on data the campaign has
  not produced

Trigger: if a builder catches themselves wanting to "make the empty room
look fuller," that is the trigger to stop and check D22. Add the missing
artifact, document the absence, or render via the empty-state component —
do not paper over the absence.

Class 12 is currently a *candidate* (not ratified). Ratification follows
observed bypass of D22, per the same evolution path Class 10 (TASK-CB-001
→ ratified) and Class 11 (TASK-CB-002 → ratified) followed.

## How D22 evolves

D22 binds the Control Room (Campaign 015) and any subsequent project surface
that displays read-only project state. Future surfaces (e.g., the Atlas
public viewer, paper bundle generators, README screenshot rigs) inherit
D22 by default. Repeal would require demonstrating that the Decorative
Completeness failure mode does not occur in the project — which has not
happened to any doctrine since D7.

## Lineage

* Proposed: `Control Room v0.txt` §10 ("Read-only first principle"), §12
  ("Data adapters" — graceful missing-file handling), §22 ("Builder
  expansion authority" forbidding fabricated visual completeness).
* Ratified: TASK-CB-004 (Campaign 015 Phase 0). Architect Claude binds
  D22 as the new doctrine for the Control Room foundation; Class 12 is
  added to the mistake catalog watch list.
