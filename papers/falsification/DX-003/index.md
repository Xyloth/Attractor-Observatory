# DX-003 Branch Falsification Bath Index

T_start_UTC: 2026-05-08T21:40:48.9304878Z
T_start_EST: 2026-05-08 17:40:48
T_end_UTC: 2026-05-08T22:26:03.6708377Z
T_end_EST: 2026-05-08 18:26:03
total_elapsed: 00:45:14.7403499
branch: falsification/dx-003-20260508T214003Z-4147aad
main_head_at_start: 4147aad
private_surface_verified: yes, 13/13 directories present after scripts/setup_worktree.bat

## Roll-Up Counts

round_count: 9
total_finding_records: 40
confirmed_findings: 33
hypotheses: 13
total_reproducer_artifacts: 68
actual_broken_count: 27
actual_fake_passed_count: 6
actual_ambiguous_or_indeterminate_count: 3
instrument_held_count: 4

## Severity Distribution

- red: 12
- amber: 17
- yellow: 6
- informational: 5

## Distinct Attack Angles Used

1. Executable substrate reality: full public/private test collection, hash gates, setup completeness.
2. Project Genealogy self-map collision: PG manifest, run binding, atlas/coherence/test agreement.
3. Doctrine contract violators: D31 AST bypasses, D26 adversarial controls, source-object aliasing, value-encoded labels.
4. Evidence dereferenceability: structured path references, D29 marking, missing run artifacts.
5. Control Room truth surfaces: snapshot freshness, room registry/doc drift, stale PG display, mission atoms.
6. External identifier reality collision: DOI/PMID resolution and semantic citation support.
7. Identity and telemetry accounting: Estimation Loop counts, identity-bounded calibration, public telemetry test depth.
8. Daemon state and progress cache collision: force-refresh, due-source truth, stale progress files.
9. Doctrine and mistake-catalog propagation: D31/Class13 propagation to fresh-agent/Control Room surfaces.

## Attack-Class Distribution

- executable-substrate / test truth: 6 findings, 5 broken, 1 fake-passed
- genealogy/provenance self-map: 5 findings, 4 broken, 1 fake-passed
- doctrine/contract bypass: 6 findings, 5 broken, 1 fake-passed
- evidence dereferenceability: 4 findings, 3 broken, 1 ambiguous
- UI/control-room truthfulness: 4 findings, 4 broken
- external reality/citation semantics: 4 findings, 1 broken, 1 fake-passed, 1 held, 1 indeterminate
- identity/telemetry accounting: 4 findings, 2 broken, 1 fake-passed, 1 held
- runtime daemon/progress liveness: 4 findings, 1 broken, 1 fake-passed, 1 ambiguous, 1 held
- governance propagation: 3 findings, 2 broken, 1 held

## Highest-Severity Findings

1. R6-F1: motif.autocatalytic_closure.draft W1 source-bound empirical positives cite papers resolving to spider silk adhesion and essential tremor, not RAF/autocatalytic reaction networks. This is DOI-shaped semantic non-evidence.
2. R3-F1: D31 AST read-separation can be bypassed with non-contiguous strings and dynamic import while reporting passed: True.
3. R3-F2: four-axis adversarial controls miss metadata identity channels such as manifest.world_family and parameter_record.family.
4. R2-F1/R2-F2: PG-001 artifacts are bound to a dirty pre-implementation branch and omit 1,870 tracked files from the consolidated-main universe.
5. R4-F1/R4-F2: 349 unmarked missing path references remain; Campaign 006 publishes absent runs/campaign006/... evidence paths.
6. R5-F1: raw state_latest.json claims current while bound to an older branch/commit; reader rebinding catches it, but the canonical raw file lies if read directly.
7. R8-F1/R8-F2: force-refresh clears daemon state while progress files still report completed sources and no pending sources; due-source logic says all 17 sources are due.
8. R9-F1/R9-F2: governance surfaces disagree about whether Class 12 exists/ratified and omit Class 13/D31 from Control Room doctrine displays.

## Patterns Across Findings

The strongest repeated pattern is not that individual algorithms are always wrong; it is that downstream display, reports, and tests often preserve older truth after upstream artifacts change. The project has solid substrate pieces in several places (load_latest() recomputes freshness, DOI/PMID strings resolve, due-source selection honors cleared state, doctrine registry includes D31), but surrounding surfaces turn those substrate truths into stale or overconfident user-facing claims.

The second pattern is semantic validation lagging structural validation. DOI strings resolve, source-object maps compare, telemetry rows parse, and tests pass, but those checks do not prove the paper supports the motif, the alias refers to the same source object, the README count matches the ledger, or the progress view reflects current daemon state.

## Where I Would Attack Harder With More Time

- Full semantic citation audit across all DOI/PMID/URL-bearing artifacts, not just MotifContract.v2.
- Schema-aware DOI extraction for ITIS/raw source blobs to separate valid normalized DOI fields from raw $SRC strings.
- Long-run daemon replay after force-refresh in a disposable store, including progress freshness and Control Room rendering.
- UI screenshot/AppTest pass across all rooms looking for D7-D31/Class13/room-count/identity drift.
- Mutation audit for commands with --help, tests, and prepass/query operations that should be read-only.
- Full telemetry ledger schema reconciliation against README, AI Operations Tower, BUILD_LOG, and any paper claims using calibration data.

## Doctrine Candidates Proposed

- Candidate: machine-readable mistake-catalog registry, analogous to docs/doctrine_registry.json, with class id, status, ratification source, and display labels.
- Candidate: external-citation substance gate distinguishing identifier_resolved, title_matches_claim, abstract_supports_claim, and substance_audit_signed.
- Candidate: advisory snapshot/progress artifacts must carry a freshness binding to the state file they summarize, not just written_at.
- Candidate: source-object-map equality cannot rely on exact source_object string equality only; aliases/parent-child field relationships require a canonical source-object ontology.

## Open Questions For Architect / PI

- Is Class 12 now ratified, still candidate, or intentionally skipped? Current surfaces say all three depending on where a Builder reads.
- Should source_bound mean external identifier dereferenceability only, or substantive support for the mapped motif/world row?
- Is reports/factory_daemon_progress/*.json intended as historical progress snapshots or current operator truth? The schema needs to say.
- Should PG-001 artifacts be regenerated on consolidated main before downstream agents use the atlas as a live attack surface?

## Exhaustion-Honesty Statement

I have run out of fundamentally different DX-003 attack angles in the generated set for this pass after nine rounds. The remaining ideas I can name are deeper variants of surfaces already attacked here, or require starting a new long-running campaign rather than a bounded falsification round: full literature substance review, full UI screenshot QA, long daemon replay, or all-report schema reconciliation. I did not stop at the forty-minute floor; I added two post-floor rounds because fresh angles were still available.
