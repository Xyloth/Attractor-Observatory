# DX-003 Round 5 - Control Room and Snapshot Truthfulness

round_id: DX-003-R5
attack_angle: I attacked the dashboard as a truth surface. The question was not whether Streamlit renders, but whether Control Room and Mission Control surfaces tell a fresh AI/human the same truth as the underlying repository state, especially for stale sidecars and PG-001's currentness.
elapsed_at_round_start: 00:22:30
elapsed_at_round_end: 00:26:44
round_end_utc: 2026-05-08T22:08:06.5186549+00:00

## Surfaces Examined

- control_room/snapshots/state_latest.json
- control_room.snapshot.build_snapshot/load_latest
- control_room/rooms/project_genealogy.py
- Streamlit AppTest render of the Project Genealogy room
- README.md, Control_Room_README.md, control_room/rooms/README.md
- eports/project_genealogy/atlas_latest.json
- eports/project_genealogy/coherence_latest.json

## Findings

### R5-F1 - RED - The canonical AI snapshot file is raw-stale while documenting itself as current

Claim: Control_Room_README.md tells a fresh AI agent to read exactly control_room/snapshots/state_latest.json as the canonical one-file state. The raw file says reshness_status=current and ctive_branch=codex/task-floor-bfg, but the current branch is DX-003 and the current commit is different. The Python helper load_latest() recomputes stale correctly, but the documented one-file artifact itself lies unless the consumer knows to import code rather than read the file.

Reproducer: Run the probe captured in ound_5_reproducers/snapshot_freshness_probe.txt. Expected output: raw state_latest binding has ranch=codex/task-floor-bfg, commit_sha=2f804f0..., reshness_status=current; load_latest() rebinding returns stale:commit_moved,branch_changed; uild_snapshot() returns the current DX branch/head.

Mistake-class mapping: sidecar freshness drift; raw-artifact truthfulness failure.
Doctrine refs: D24, D30, D9.

### R5-F2 - AMBER - Project Genealogy room renders stale PG data without a stale/degraded banner

Claim: The Project Genealogy room renders the stale PG atlas as top-row truth: udited files=920, ad drift=4, and mission atoms 8/8 covered. The only binding disclosure is a small caption with branch eature/pg-001-execute and HEAD d13d93de; AppTest output contains no stale or degraded state marker even though Round 2 proves the atlas excludes 1,870 non-DX tracked files now present on consolidated main.

Reproducer: Run the AppTest probe captured in ound_5_reproducers/project_genealogy_apptest_probe.txt and inspect element details in project_genealogy_apptest_elements.txt. Expected output: exceptions [], markdown contains udited files, ad drift, and mission atoms; booleans for stale and degraded state are False; caption shows ranch: feature/pg-001-execute | HEAD: d13d93de.

Mistake-class mapping: UI truthfulness; stale-current split.
Doctrine refs: D22, D30, D9.

### R5-F3 - AMBER - Control Room documentation still says 11 rooms while registry has 12

Claim: PG-001 added project_genealogy, so oom_registry() returns 12 rooms. README and Control Room docs still repeatedly describe an 11-room dashboard/application. This is a small but visible example of UI/documentation drift in the exact surface users are told to walk.

Reproducer: Run python - <<probe>> equivalent captured in ound_5_reproducers/room_count_doc_drift.txt. Expected output: oom_registry_count 12 with project_genealogy in the list, while README.md contains 11-room, 11 rooms, and eleven rooms, and Control_Room_README.md contains The Control Room ships **11 rooms**.

Mistake-class mapping: documentation drift; Control Room truthfulness.
Doctrine refs: D22, D30.

### R5-F4 - RED - Mission atoms claim evidence/reproducibility coverage despite live counterevidence

Claim: The PG Mission Coherence surface marks MA-evidence-discipline and MA-reproducible-research-instrument as covered. The same branch state has public tests failing (Round 1), PG manifest staleness/missing current files (Round 2), and 349 unmarked missing evidence paths (Round 4). The mission atom status is therefore too coarse to be used as a truth signal about current reproducibility/evidence discipline.

Reproducer: Inspect ound_5_reproducers/mission_atoms_covered_summary.txt: both mission atoms are covered. Compare with ound_1_reproducers/pytest_all.txt, ound_2_reproducers/pg_manifest_missing_non_dx.txt, and ound_4_reproducers/path_reference_audit_strict_summary.json.

Mistake-class mapping: claim-boundary overaggregation; mission-level false confidence.
Doctrine refs: D9, D17, D29, D30.

## Instrument-held Records

- control_room.snapshot.load_latest() correctly recomputes stale status when used as code.
- control_room.snapshot.build_snapshot() binds to the current DX branch/head and updates project-health details in memory.
- The Project Genealogy room renders deterministically without exceptions under AppTest.

## Hypotheses

- The raw snapshot should persist reshness_status=advisory or equires_rebind, not current, unless every documented consumer uses load_latest().
- Mission Control should show an explicit stale-input banner whenever tlas.run_binding.head_commit differs from current HEAD or workspace_dirty=True appears in the manifest lineage.
- Mission atom coverage needs negative evidence inputs; a mission atom should not remain simply covered when current gates directly contradict the atom text.
