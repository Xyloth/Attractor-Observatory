# Dossier: `public_tests/test_pg001_acceptance_gates.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/4f7100ab98e1_public_tests_test_pg001_acceptance_gates.py.json`
- JSON content_hash: `sha256:80ae520ce9b4b47795779d88ee80ca1120e2f3deef4c31b3b39ab1bfdd888061`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 352 / Bytes: 14209

## Birth
- Status: `recovered`
- First-seen commit: `01c6c38479151939d0f7c2be30f4d79df6f1bb7e`
- First-seen date: `2026-05-08T15:49:33-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — PG-001 acceptance gates — single test per gate.

The twenty acceptance gates from spec §"Acceptance Gates" are reported
here as individual pytest assertions so a fresh auditor can run

    python -m pytest public_tests/test_pg001_acceptance_gates.py -v

and see one PASS line per gate, mapping directly to the spec.

Each test references the underlying public_tests/test_pg001_*.py module
that exerci

## Current
- Status: `recovered`
- Public symbols: `test_PG001_coherence_and_atlas_findings_are_partitioned, test_PG001_help_is_inert, test_PG10_query_api_examples_execute, test_PG11_cohort_consistency, test_PG12_cross_doctrine_collision_pass, test_PG13_mistake_class_mapping, test_PG14_public_verification_honesty, test_PG15_versioned_atlas, test_PG16_mission_atoms_locked, test_PG17_mission_coverage_complete`
- Observed doctrines: `D26`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 44}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D26'], 'verified': ['D26'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 5

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-public_tests/test_pg001_acceptance_gates.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 44: except (OSError, json.JSONDecodeError):
- **PG-public_tests/test_pg001_acceptance_gates.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 51: assert manifest["content_hash"].startswith("sha256:")
- **PG-public_tests/test_pg001_acceptance_gates.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 215: if first_seg in {"worlds", "motifs", "validation", "nulls", "core", "trace", "formalism", "biology", "search", "ops", "e
- **PG-public_tests/test_pg001_acceptance_gates.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 265: if status in {"removable_clean", "removable_with_warnings", "not_removable"}:
- **PG-public_tests/test_pg001_acceptance_gates.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 267: elif status == "probe_declined":

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.