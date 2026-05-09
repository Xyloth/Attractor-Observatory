# DX-003 Round 1 - Executable Substrate and Worktree Reality

round_id: DX-003-R1
attack_angle: I attacked the consolidated instrument as an executable object rather than as a narrative repository: fresh branch from main, private setup script, all declared private directories, default test command, explicit public/private test commands, and targeted smoke tests for MotifContract and Control Room. The question was whether the whole project can run from the branch state it asks reviewers to trust.
elapsed_at_round_start: 00:00:00
elapsed_at_round_end: 00:05:40
round_end_utc: 2026-05-08T21:47:27.0431370+00:00

## Surfaces Examined

- scripts/setup_worktree.bat and scripts/SETUP_WORKTREE.md
- Gitignored private modules copied by setup: worlds/, motifs/, alidation/, 
ulls/, core/, 	race/, ormalism/, iology/, search/, ops/, experiments/, evidence/, 	ests/
- Default pytest.ini
- public_tests/
- copied private 	ests/
- Control Room room registry tests after PG-001
- lineage and doctrine hash gates

## Findings

### R1-F1 - RED - Public verification is red at HEAD

Claim: The consolidated main branch cannot claim a green public invariant surface. python -m pytest -q runs the configured public suite and fails 2 tests: spec lineage hashes and doctrine registry content hashes.

Reproducer: From the DX-003 worktree, run python -m pytest -q. Expected output includes 2 failed, 203 passed and failures in public_tests/test_public_contracts.py::test_spec_lineage_hashes_match_raw_bytes and public_tests/test_public_contracts.py::test_doctrine_registry_covers_all_binding_and_candidate_doctrines. Captured output: ound_1_reproducers/pytest_all.txt.

Mistake-class mapping: provenance/hash-drift; fake-green guard failure.
Doctrine refs: D9 honest failure reporting; D17 via-negativa publication; D29 private/public evidence boundary is adjacent but not the direct cause.

### R1-F2 - RED - Hash provenance gates identify 15 concrete stale hashes

Claim: The failure is not a vague test flake. spec/lineage.json has 3 stale source hashes; docs/doctrine_registry.json has 12 stale doctrine hashes. These are claim-bearing provenance records whose recorded digests no longer bind the files.

Reproducer: Run the probe embedded in ound_1_reproducers/hash_mismatches.txt recipe, or rerun:

`powershell
@'
import hashlib, json, pathlib
root=pathlib.Path('.')
lineage=json.loads((root/'spec/lineage.json').read_text(encoding='utf-8'))
for row in lineage['entries']+lineage.get('supporting_context',[]):
    actual=hashlib.sha256((root/row['source_path']).read_bytes()).hexdigest()
    if row['sha256'] != actual: print(row['source_path'], row['sha256'], actual)
reg=json.loads((root/'docs/doctrine_registry.json').read_text(encoding='utf-8'))
for row in reg['doctrines']:
    actual='sha256:'+hashlib.sha256((root/row['path']).read_bytes()).hexdigest()
    if row['content_hash'] != actual: print(row['id'], row['path'], row['content_hash'], actual)
'@ | python -
`

Expected mismatches are captured in ound_1_reproducers/hash_mismatches.txt.

Mistake-class mapping: provenance; cross-temporal drift.
Doctrine refs: D21/D22 style artifact integrity; D30 freshness semantics by analogy.

### R1-F3 - RED - The copied private test suite does not collect

Claim: The setup script copies the 13 private directories requested by the ticket, but the copied private suite still depends on gitignored Python modules that setup does not copy: tlas.db, tlas.negative_space.structured, and i_os.estimation_loop. The full-private worktree is therefore not actually whole enough to run its own private tests.

Reproducer: From the DX-003 worktree after scripts/setup_worktree.bat, run python -m pytest -q tests. Expected result: collection aborts with 5 import errors, including ModuleNotFoundError: No module named 'atlas.db' and ModuleNotFoundError: No module named 'ai_os.estimation_loop'. Captured output: ound_1_reproducers/pytest_private_tests.txt. Narrow reproducers: python -m pytest -q tests/test_estimation_loop.py and python -m pytest -q tests/test_campaign013.py, captured in the matching files.

Mistake-class mapping: dependency mirage; setup-surface incompleteness; private/public boundary leakage.
Doctrine refs: D9; D29; D30 if setup output is treated as current/full state.

### R1-F4 - AMBER - Default pytest is a fake-green surface for private tests

Claim: pytest.ini sets 	estpaths = public_tests, so python -m pytest -q never exercises the copied private suite even after setup. A developer can run the obvious full-test command and receive only the public-suite result while private collection is broken.

Reproducer: Inspect pytest.ini; it contains only 	estpaths = public_tests. Then compare python -m pytest -q with python -m pytest -q tests. The first reaches 205 public tests and fails only public hash gates; the second aborts during private collection. Captures: ound_1_reproducers/pytest_all.txt and ound_1_reproducers/pytest_private_tests.txt.

Mistake-class mapping: fake-green; audit coverage gap.
Doctrine refs: D9; Mistake Catalog Class 13 by analogy, because a surface appears decoupled from the thing it claims to exercise.

### R1-F5 - AMBER - PG-001 added a twelfth room but the private Control Room invariant still demands eleven

Claim: The README now advertises a Project Graph/Genealogy direction and PG-001 is merged, but 	ests/test_control_room_rooms.py still asserts exactly 11 rooms and canonical order without project_genealogy. The UI registry and its private invariant disagree.

Reproducer: Run python -m pytest -q tests/test_control_room_rooms.py. Expected output includes expected 11 rooms in registry, got 12 and actual order containing project_genealogy before portfolio_demo. Captured output: ound_1_reproducers/pytest_control_room_rooms.txt.

Mistake-class mapping: cross-temporal UI invariant drift.
Doctrine refs: D30 freshness/read-time truthfulness; D9.

### R1-F6 - YELLOW - Copied private __pycache__ leaks main-checkout paths into worktree tracebacks

Claim: setup_worktree.bat copies private directories recursively, including 	ests/__pycache__. The resulting Python tracebacks point at C:\Attractor Observatory\tests\... even though commands run inside the DX worktree. That weakens provenance during failure triage and can make a worktree failure look like a main-checkout failure.

Reproducer: After setup, run python -m pytest -q tests/test_estimation_loop.py in C:\Attractor Observatory DX Worktrees\dx-003-20260508T214003Z-4147aad. Expected traceback filename includes C:\Attractor Observatory\tests\test_estimation_loop.py. Captured output: ound_1_reproducers/pytest_estimation_loop.txt.

Mistake-class mapping: provenance/path leakage; dependency mirage.
Doctrine refs: D9; D30 by analogy.

## Instrument-held Records

- The required 13 private directories were present and readable after setup.
- python -c "import formalism, worlds, trace; print('ok')" returned ok.
- python -m pytest -q tests/test_motif_contracts_v2.py passed: 5 passed in 2.00s.

## Hypotheses

- The setup script likely needs a release-manifest concept rather than a hand-maintained directory allowlist; otherwise future private Python modules will continue to be invisible to worktrees.
- The public/private pytest split may need an explicit make test-public / make test-private distinction so default pytest does not look more complete than it is.
- Copied __pycache__ may also poison other provenance captures, not just tracebacks.
