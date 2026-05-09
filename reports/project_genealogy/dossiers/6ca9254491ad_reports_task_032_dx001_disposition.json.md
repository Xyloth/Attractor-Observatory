# Dossier: `reports/task_032_dx001_disposition.json`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/6ca9254491ad_reports_task_032_dx001_disposition.json.json`
- JSON content_hash: `sha256:69de66b5d4403ddadbd6aa3effcc8cb935bcd73e2decc0c9cf82b91fb902a56d`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `report`
- Generated status: `report`
- Lines: 21110 / Bytes: 1165024

## Birth
- Status: `recovered`
- First-seen commit: `ff7a2adff3a2bcf5dbddec8e613b3a17dc69edfd`
- First-seen date: `2026-05-06T14:39:23-04:00`
- Spawn ticket: `TASK-033`
- Cohort: `TASK-033`

### Birth predicate atoms
- **report_records_data** — Report serializes structured data for post-hoc analysis.

## Current
- Status: `recovered`
- Observed doctrines: `D13, D14, D18, D19, D20, D21, D22, D23, D24, D25, D7`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'value': 0.0}`
- **doctrine_binding_quality**: `{'required': ['D13', 'D14', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D7'], 'verified': ['D13', 'D14', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D7'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-reports/task_032_dx001_disposition.json-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 639
- **PG-reports/task_032_dx001_disposition.json-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 667
- **PG-reports/task_032_dx001_disposition.json-class-2** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 697
- **PG-reports/task_032_dx001_disposition.json-class-3** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 717
- **PG-reports/task_032_dx001_disposition.json-class-4** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 727
- **PG-reports/task_032_dx001_disposition.json-class-5** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 737
- **PG-reports/task_032_dx001_disposition.json-class-6** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 747
- **PG-reports/task_032_dx001_disposition.json-class-7** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 757
- **PG-reports/task_032_dx001_disposition.json-class-8** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 767
- **PG-reports/task_032_dx001_disposition.json-class-9** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 21049
- **PG-reports/task_032_dx001_disposition.json-class-10** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 21107
- **PG-reports/task_032_dx001_disposition.json-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.