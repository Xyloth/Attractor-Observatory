# Dossier: `project_genealogy/manifest.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/58d9d06d967d_project_genealogy_manifest.py.json`
- JSON content_hash: `sha256:69c8955357793421a74dd8373328da285479575bd100644fcb9d15646ee210f0`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 822 / Bytes: 29690

## Birth
- Status: `recovered`
- First-seen commit: `b37c7b68e73883b45ef91df2e9d2bb5d799bdff6`
- First-seen date: `2026-05-08T15:48:24-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **audit_instrument_executes** — Module is part of the PG-001 audit instrument and exposes a callable surface.

## Current
- Status: `recovered`
- Public symbols: `build_manifest, cli_main, determine_artifact_family, is_cohort_only, is_critical_path, write_manifest`
- Observed doctrines: `D11, D12, D15, D17.5, D18, D19, D20, D22, D23, D24, D25, D26, D29, D30, D31, D7, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 687}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D12', 'D15', 'D17.5', 'D18', 'D19', 'D20', 'D22', 'D23', 'D24', 'D25', 'D26', 'D29', 'D30', 'D31', 'D7', 'D9'], 'verified': ['D11', 'D12', 'D15', 'D17.5', 'D18', 'D19', 'D20', 'D22', 'D23', 'D24', 'D25', 'D26', 'D29', 'D30', 'D31', 'D7', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 2, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 1.0}`

## Drift
- Status: `review_required`
- Letter-vs-spirit surfaces: 5

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-project_genealogy/manifest.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 127: if re.search(pattern, rel_path):
- **PG-project_genealogy/manifest.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 141: if name.endswith("_signed.json") or name.endswith(".signed.json"):
- **PG-project_genealogy/manifest.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 640: return any(re.search(p, rel_path) for p in CRITICAL_PATH_PATTERNS)
- **PG-project_genealogy/manifest.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 687: except OSError:
- **PG-project_genealogy/manifest.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 821: if __name__ == "__main__":
- **PG-project_genealogy/manifest.py-class-0** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 355
- **PG-project_genealogy/manifest.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.