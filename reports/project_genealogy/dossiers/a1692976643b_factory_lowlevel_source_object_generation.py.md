# Dossier: `factory_lowlevel/source_object_generation.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/a1692976643b_factory_lowlevel_source_object_generation.py.json`
- JSON content_hash: `sha256:654a060358fd81113dd7042392f7cdd7e02d409bd8c4fca2591e37f4cb8d05cb`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 184 / Bytes: 8128

## Birth
- Status: `recovered`
- First-seen commit: `8b88da40e8ec798dfd3b49389e91ec980d9add21`
- First-seen date: `2026-05-07T07:51:11-04:00`
- Spawn ticket: `TASK-SOURCE-OBJ-GEN`
- Cohort: `TASK-SOURCE-OBJ-GEN`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.
- **header_declared_intent** — Validation harness for TASK-SOURCE-OBJ-GEN.

This is intentionally network-free by default. The adapters may validate live
source homes when explicitly requested, but the acceptance tests use bundled
authoritative source-object seeds so CI does not depend on external uptime.

## Current
- Status: `recovered`
- Public symbols: `build_source_object_generation_report`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}], 'value': 0.5}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5', 'D7'], 'verified': [], 'claimed_only': ['D14', 'D17.5', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 1

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-factory_lowlevel/source_object_generation.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 182: if __name__ == "__main__":
- **PG-factory_lowlevel/source_object_generation.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.