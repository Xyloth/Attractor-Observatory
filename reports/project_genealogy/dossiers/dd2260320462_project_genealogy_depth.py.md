# Dossier: `project_genealogy/depth.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/dd2260320462_project_genealogy_depth.py.json`
- JSON content_hash: `sha256:f61d9e1fabca761efc031313f8885e19d81ccb29d230708736b1168cf744426b`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 178 / Bytes: 7171

## Birth
- Status: `recovered`
- First-seen commit: `76085687c8c8f33c41cb35b5af5dfadeaf23ca3d`
- First-seen date: `2026-05-08T15:48:58-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **audit_instrument_executes** — Module is part of the PG-001 audit instrument and exposes a callable surface.

## Current
- Status: `recovered`
- Public symbols: `compute_depth`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D19', 'D20'], 'verified': [], 'claimed_only': ['D11', 'D19', 'D20'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 4

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-project_genealogy/depth.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 82: if artifact_family in {"factory", "control_room", "report"}:
- **PG-project_genealogy/depth.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 90: if surf.get("pattern", "").startswith("except"):
- **PG-project_genealogy/depth.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 92: if any(s.get("snippet", "").startswith("if") for s in letter_surfaces):
- **PG-project_genealogy/depth.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 119: "present" if artifact_family in {"audit_report", "audit_instrument", "doctrine", "method"} else "absent"
- **PG-project_genealogy/depth.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.