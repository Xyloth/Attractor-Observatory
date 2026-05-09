# Dossier: `public_tests/test_pg001_removal_probe.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/b2eddd545984_public_tests_test_pg001_removal_probe.py.json`
- JSON content_hash: `sha256:44d64110feaa9b928148a27a7274febf1d537363b211f66e1f907bc65006dd10`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 85 / Bytes: 3445

## Birth
- Status: `recovered`
- First-seen commit: `01c6c38479151939d0f7c2be30f4d79df6f1bb7e`
- First-seen date: `2026-05-08T15:49:33-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — PG-001 removal-probe protocol tests.

PG18 — every cleanup_candidate_status with a `removable_*` or
`not_removable` verdict carries a recorded ``removal_probe.command`` and
``removal_probe.outcome``. Bare ``unknown`` and ``probe_declined`` are
allowed, and the manifest's probe budget makes the latter the dominant
state in v1.

## Current
- Status: `recovered`
- Public symbols: `test_critical_paths_are_probe_declined, test_non_removable_status_carries_probe_evidence, test_probe_decline_reasons_are_canonical`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D12', 'D29', 'D7'], 'verified': [], 'claimed_only': ['D12', 'D29', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 2

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-public_tests/test_pg001_removal_probe.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 46: if any(re.search(pat, rel) for pat in patterns):
- **PG-public_tests/test_pg001_removal_probe.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 65: if status in {"removable_clean", "removable_with_warnings", "not_removable"}:

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.