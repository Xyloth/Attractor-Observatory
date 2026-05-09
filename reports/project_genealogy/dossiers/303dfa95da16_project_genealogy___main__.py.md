# Dossier: `project_genealogy/__main__.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/303dfa95da16_project_genealogy___main__.py.json`
- JSON content_hash: `sha256:034893ce533f8e60fded83e6d2460314eff896cf5980e14544d8f58c21a0eb29`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 122 / Bytes: 3952

## Birth
- Status: `recovered`
- First-seen commit: `2896e0e1027b545c467428fe13baa4e13b019772`
- First-seen date: `2026-05-08T15:49:14-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **audit_instrument_executes** — Module is part of the PG-001 audit instrument and exposes a callable surface.

## Current
- Status: `recovered`
- Public symbols: `main`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D19', 'D20'], 'verified': [], 'claimed_only': ['D11', 'D19', 'D20'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 1, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 2

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-project_genealogy/__main__.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 115: if cmd == "query":
- **PG-project_genealogy/__main__.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 121: if __name__ == "__main__":
- **PG-project_genealogy/__main__.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.