# Dossier: `make_source_object_generation.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/320728a98684_make_source_object_generation.py.json`
- JSON content_hash: `sha256:7dedb5da12323c801c29ad0b0164352ef7566955d8df0680b507968836a28c46`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `root_artifact`
- Generated status: `source`
- Lines: 6 / Bytes: 266

## Birth
- Status: `recovered`
- First-seen commit: `8b88da40e8ec798dfd3b49389e91ec980d9add21`
- First-seen date: `2026-05-07T07:51:11-04:00`
- Spawn ticket: `TASK-SOURCE-OBJ-GEN`
- Cohort: `TASK-SOURCE-OBJ-GEN`

### Birth predicate atoms
- **root_artifact_serves_repo** — Top-level artifact serves a repo-wide convention (license, citation, ignore, requirements, container).
- **header_declared_intent** — from factory_lowlevel.source_object_generation import build_source_object_generation_report
if __name__ == "__main__":
report = build_source_object_generation_report()
print(f"TASK-SOURCE-OBJ-GEN -> {report['status']} ({report['total_records']} records)")

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': [], 'verified': [], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Letter-vs-spirit surfaces: 1

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-make_source_object_generation.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 4: if __name__ == "__main__":

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.