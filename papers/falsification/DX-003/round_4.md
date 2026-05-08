# DX-003 Round 4 - Evidence Dereferenceability and Private-Boundary Marking

round_id: DX-003-R4
attack_angle: I attacked evidence as dereferenceable substrate. Instead of asking whether reports parse or tests pass, I scanned structured artifacts for path-bearing fields and checked whether the referenced files actually exist from the consolidated branch state, distinguishing private-marked absences from unmarked evidence-shaped holes.
elapsed_at_round_start: 00:17:43
elapsed_at_round_end: 00:22:30
round_end_utc: 2026-05-08T22:04:35.2517131+00:00

## Surfaces Examined

- JSON artifacts under eports/, papers/, tlas/, docs/, spec/, and control_room/snapshots/
- eports/campaign_006/*
- eports/campaign_019/*
- eports/campaign_023/full_report.json
- eports/campaign_024/full_report.json
- o-crate-metadata.json

## Findings

### R4-F1 - RED - 349 unmarked missing path references remain in structured artifacts

Claim: A strict path-key scan found 37,291 path-bearing values. 3,742 were missing; 3,393 of those were marked private/unshipped, but 349 missing path references had no private/unshipped marker. That is the exact D29 failure shape: evidence-like paths that cannot be dereferenced and are not honestly labeled as private or unshipped.

Reproducer: Run the strict scanner recipe captured in ound_4_reproducers/path_reference_audit_strict_summary.json / path_reference_audit_strict.txt. Expected summary: path_key_values_checked=37291, missing_paths=3742, missing_marked_private=3393, missing_unmarked=349.

Mistake-class mapping: provenance/dereferenceability; private-evidence boundary leak.
Doctrine refs: D29, D9, D17.

### R4-F2 - RED - Campaign 006 publishes evidence paths into absent uns/ traces without private markers

Claim: Campaign 006 is the largest unmarked dereferenceability failure. It has 210 missing paths in eports/campaign_006/perturbation_maps.json, 42 in evidence_atlas.json, 21 in eta_worlds.json, and 21 in evidence_bundles/campaign_006_bundle.json. The missing values point to uns/campaign006/..., but no uns/ directory exists in the worktree and these rows are not private-marked.

Reproducer: From the DX worktree, run Test-Path runs (expected False) and inspect ound_4_reproducers/path_reference_audit_strict_summary.json. The examples begin with eports/campaign_006/beta_worlds.json rows.0.trace_path = runs\\campaign006\\W4_positive_6060_base.json and many uns\\campaign006\\perturbations\\... paths.

Mistake-class mapping: missing source trace provenance; report-to-artifact split.
Doctrine refs: D11, D17, D29.

### R4-F3 - AMBER - Campaign 019 hardening fixtures cite missing lock artifacts

Claim: Campaign 019's hardening and fixture reports cite lock files such as eports/campaign_019/fixtures/required_key_contract/factory.lock, but those files are absent and unmarked. That weakens the replayability of fixture gates and stop/start locking claims.

Reproducer: Inspect ound_4_reproducers/campaign_019_missing_paths.txt. Expected rows include eports\\campaign_019\\full_report.json fixture_gates.4.evidence.lock.path, hardening_fixtures.json scenarios.*.lock.path, and ixture_gates.json gates.*.evidence.lock.path, all pointing to missing actory.lock files with marked_private=false.

Mistake-class mapping: hardening-fixture provenance gap; honest-failure honesty.
Doctrine refs: D17, D29, D30.

### R4-F4 - YELLOW - The project is partially applying D29 correctly, but unevenly

Claim: The same strict scan found 3,393 missing paths that are marked private/unshipped. That is good doctrine behavior. The bug is uneven adoption: Campaign 023/024 traces and many private runtime paths are now honestly marked or shipped, while older Campaign 006/019 paths still look public-dereferenceable.

Reproducer: Compare ound_4_reproducers/path_reference_audit_strict_summary.json with ound_4_reproducers/campaign_023_024_trace_private_check.txt. Campaign 023 and 024 each have 	otal_path_refs 180 missing 0, while Campaign 006/019 account for most unmarked missing references.

Mistake-class mapping: partial doctrine migration; cross-temporal artifact hygiene.
Doctrine refs: D29, D30.

## Instrument-held Records

- Campaign 023 and Campaign 024 full reports no longer reproduce the DX-002 missing-trace failure: each has 180 path refs and 0 missing in this full-private worktree.
- o-crate-metadata.json has 4 graph items, 2 file-like IDs checked, and 0 missing file-like IDs.
- 33,549 checked path values resolved successfully.

## Hypotheses

- Older campaigns need a D29 migration sweep: either ship the trace/fixture artifacts, mark them private/unshipped, or replace raw paths with content-addressed public summaries.
- The path-reference scanner should become a public invariant with an allowlist for intentional private paths.
- Campaign 006's uns/ references may be historical/regenerable, but the current artifact does not encode the regeneration command or private-boundary reason at point of use.
