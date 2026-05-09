# DX-003 Round 2 - Project Genealogy Self-Map Collision

round_id: DX-003-R2
attack_angle: I attacked PG-001 as a self-map of the project rather than as another report. The core question was whether the genealogy atlas and coherence report are actually bound to consolidated main and whether they audit the surfaces introduced by PG-001/CB-020/CB-021, or whether the self-map excludes the newest terrain while still presenting itself as the current atlas.
elapsed_at_round_start: 00:05:40
elapsed_at_round_end: 00:13:35
round_end_utc: 2026-05-08T21:55:02.7238191+00:00

## Surfaces Examined

- papers/methods/PROJECT_GENEALOGY_PG001_SPEC.md
- project_genealogy/ runner/query/hash modules
- eports/project_genealogy/input_manifest.json
- eports/project_genealogy/atlas_latest.json
- eports/project_genealogy/coherence_latest.json
- eports/project_genealogy/dossiers/
- PG-001 public tests in public_tests/test_pg001_*.py
- Git tracked-file set at the DX-003 branch state

## Findings

### R2-F1 - RED - PG-001's shipped manifest is not a manifest of consolidated main

Claim: eports/project_genealogy/input_manifest.json says 	racked_total=5075, but the branch contains 6955 tracked files after Round 1 and 6945 at the frozen main base. Excluding DX-003's own new files, 1870 non-DX tracked files are absent from the manifest's audited+excluded universe. Missing examples include project_genealogy/*.py, control_room/rooms/project_genealogy.py, actory_lowlevel/memory_guard.py, CB-020/CB-021/PG-001 public tests, and the PG reports/dossiers themselves.

Reproducer: Run the script captured in ound_2_reproducers/pg_manifest_missing_non_dx.txt, or rerun:

`powershell
@'
import json, subprocess
from pathlib import Path
m=json.loads(Path('reports/project_genealogy/input_manifest.json').read_text(encoding='utf-8'))
git_files=subprocess.check_output(['git','ls-files'], text=True).splitlines()
known={e['path'] for e in m['audited_files']} | {e['path'] for e in m['excluded_files']}
missing=sorted(set(git_files)-known)
print(len([p for p in missing if not p.startswith('papers/falsification/DX-003/')]))
print('\n'.join([p for p in missing if not p.startswith('papers/falsification/DX-003/')][:25]))
'@ | python -
`

Expected result: 1870 non-DX tracked files absent from the manifest, including the genealogy implementation itself.

Mistake-class mapping: self-observation blind spot; cross-temporal manifest drift; fake completeness.
Doctrine refs: D9, D17, D30, D31-adjacent if the genealogy is used as a claim boundary.

### R2-F2 - RED - The current PG artifacts are bound to a dirty pre-PG implementation branch, not to main

Claim: The PG manifest, atlas, and coherence report all record ranch=feature/pg-001-execute and head_commit=d13d93d..., while consolidated main is 4147aad and the DX branch is after that. d13d93d is the PG spec merge, before the PG implementation commits. The manifest also records workspace_dirty=True and lists the PG implementation/report files as dirty inputs.

Reproducer: Run the probe captured in ound_2_reproducers/pg_binding_vs_head.txt. Expected output shows current branch alsification/dx-003-..., current HEAD 42118fd... at the time of this round, and all PG artifact bindings at eature/pg-001-execute / d13d93de... with dirty workspace state. ound_2_reproducers/git_recent_for_pg_binding.txt shows d13d93d precedes the PG implementation commits.

Mistake-class mapping: cross-temporal provenance drift; dirty-workspace evidence laundering.
Doctrine refs: D29, D30, D9.

### R2-F3 - AMBER - PG-001 public tests pass while the atlas excludes PG-001/CB-020/CB-021 surfaces

Claim: The PG acceptance tests do not catch R2-F1 or R2-F2. The explicit PG public test set passes 49 passed, even though the current atlas is not bound to current main and excludes the newly merged PG/CB-020/CB-021 files.

Reproducer: Run python -m pytest -q public_tests/test_pg001_acceptance_gates.py public_tests/test_pg001_control_room_tab.py public_tests/test_pg001_query.py public_tests/test_pg001_removal_probe.py public_tests/test_pg001_schema.py. Expected result: 49 passed. Then run the manifest probe from R2-F1 and observe the 1870-file gap. Captured output: ound_2_reproducers/pytest_pg001_public_explicit.txt and ound_2_reproducers/pg_manifest_missing_non_dx.txt.

Mistake-class mapping: fake-green; acceptance gate missing current-HEAD binding.
Doctrine refs: D9, D30.

### R2-F4 - AMBER - Coherence report says mission fully covered while confirmed bad drift lives elsewhere

Claim: coherence_latest.json has indings=[] and mission coverage covered=8, while tlas_latest.json reports confirmed_finding_count=4 and ad_drift_count=4; python -m project_genealogy.query findings returns 964 records, including 4 confirmed high-severity bad-drift findings. A reviewer reading only the coherence report sees a cleaner project than the query/atlas surfaces admit.

Reproducer: Run the script captured in ound_2_reproducers/pg_count_contradiction.txt and python -m project_genealogy.query findings. Expected output: atlas summary confirmed_finding_count 4, ad_drift_count 4, coherence indings.len 0, and query counts {'hypothesis': 960, 'confirmed': 4} in ound_2_reproducers/pg_query_findings_counts.txt.

Mistake-class mapping: UI/report truthfulness split; claim-boundary drift.
Doctrine refs: D9, D17, D30.

### R2-F5 - YELLOW - PG CLI help can mutate the audit manifest

Claim: python -m project_genealogy run-prepass --help does not display help. It executes the prepass, rewrites eports/project_genealogy/input_manifest.json, and exits 0. A help/introspection command is therefore a state-changing command.

Reproducer: Run python -m project_genealogy run-prepass --help, then git status --short -- reports/project_genealogy/input_manifest.json. Expected output: prepass log lines and a modified manifest. Captured output: ound_2_reproducers/pg_run_prepass_help_side_effect.txt. I restored the side effect before committing this round.

Mistake-class mapping: CLI contract violation; hidden mutation.
Doctrine refs: D9; D17.5-adjacent because a reviewer asking for help mutates evidence state.

## Instrument-held Records

- PG artifact content_hash fields verify under the project's stated canonical JSON hash rule; see ound_2_reproducers/pg_content_hash_self_check.txt.
- python -m project_genealogy.query findings, orphans, depth-outliers, and doctrine-collisions returned JSON and exited 0.

## Hypotheses

- PG-001 may need an explicit self-exclusion doctrine: either it declares it cannot audit its own generation wave, or it must run a second pass after PG artifacts are committed.
- Coherence/Mission Control should probably surface confirmed bad drift counts even if mission atoms are all covered.
- The query command named indings mixes 960 not-run hypotheses with 4 confirmed findings; future UIs may need a default confirmed-only mode to avoid evidence inflation.
