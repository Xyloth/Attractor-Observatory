# Dossier: `project_genealogy/query.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/bc850f8769c8_project_genealogy_query.py.json`
- JSON content_hash: `sha256:cc01da8a05c0fb28628bb8ed849bf456bae99e1d17e03db6304f0d829efd8ff4`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 521 / Bytes: 19953

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
- Public symbols: `GenealogyIndex, cli_children, cli_cohort, cli_depth_outliers, cli_doctrine_collisions, cli_files, cli_findings, cli_main, cli_orphans, cli_parents`
- Observed doctrines: `D26`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 279}, {'id': 'error_branch', 'line': 366}, {'id': 'error_branch', 'line': 415}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D26'], 'verified': ['D26'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 1, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 15

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-project_genealogy/query.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 138: if side == "parents" and e["target"] != file_path:
- **PG-project_genealogy/query.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 140: if side == "children" and e["source"] != file_path:
- **PG-project_genealogy/query.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 145: "path": e["target"] if side == "children" else e["source"],
- **PG-project_genealogy/query.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 149: "dossier_path": self._dossier_path_for(e["target"] if side == "children" else e["source"]),
- **PG-project_genealogy/query.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 150: "dossier_hash": self._dossier_hash_for(e["target"] if side == "children" else e["source"]),
- **PG-project_genealogy/query.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 178: if relation == "birth_cohort":
- **PG-project_genealogy/query.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 193: if relation == "parent":
- **PG-project_genealogy/query.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 201: if relation == "doctrine":
- **PG-project_genealogy/query.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 235: if kind == "no_birth_predicate":
- **PG-project_genealogy/query.py-lvs-9** (info, hypothesis): Detected letter-coupled fix surface at line 244: elif kind == "no_runtime_refs":
- **PG-project_genealogy/query.py-lvs-10** (info, hypothesis): Detected letter-coupled fix surface at line 254: elif kind == "no_parent":
- **PG-project_genealogy/query.py-lvs-11** (info, hypothesis): Detected letter-coupled fix surface at line 279: except KeyError:
- **PG-project_genealogy/query.py-lvs-12** (info, hypothesis): Detected letter-coupled fix surface at line 366: except UnicodeEncodeError:
- **PG-project_genealogy/query.py-lvs-13** (info, hypothesis): Detected letter-coupled fix surface at line 415: except UnicodeEncodeError:
- **PG-project_genealogy/query.py-lvs-14** (info, hypothesis): Detected letter-coupled fix surface at line 520: if __name__ == "__main__":
- **PG-project_genealogy/query.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.