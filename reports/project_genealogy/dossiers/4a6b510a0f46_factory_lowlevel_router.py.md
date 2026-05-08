# Dossier: `factory_lowlevel/router.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/4a6b510a0f46_factory_lowlevel_router.py.json`
- JSON content_hash: `sha256:a09ef10405366215c0f141ce2a2e2048588122836053c554400b874be78d14da`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `factory`
- Generated status: `source`
- Lines: 186 / Bytes: 8437

## Birth
- Status: `recovered`
- First-seen commit: `f31fabef27b7618506d78bc49dae735b8c9cb3d4`
- First-seen date: `2026-05-05T20:37:55-04:00`
- Spawn ticket: `TASK-CB-001`
- Cohort: `TASK-CB-001`

### Birth predicate atoms
- **factory_module_exposes_callable** — Module exposes runnable factory components consumed by the daemon/pipeline.

## Current
- Status: `recovered`
- Public symbols: `RoutedWorldBundle, RoutingRejection, route_records, routing_rejections, validate_record_for_world`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}, {'id': 'decline_branch', 'kind': 'letter_pattern'}], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [{'id': 'error_branch', 'kind': 'letter_pattern'}], 'value': 0.5}`
- **doctrine_binding_quality**: `{'required': ['D14', 'D17.5', 'D7'], 'verified': [], 'claimed_only': ['D14', 'D17.5', 'D7'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['papers/methods/CAMPAIGN_021_MULTI_WORLD_FACTORY.md'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 5

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-factory_lowlevel/router.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 121: if target_world == "crn":
- **PG-factory_lowlevel/router.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 124: if target_world == "field" and not world_params.get("benchmark"):
- **PG-factory_lowlevel/router.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 126: if target_world == "origins_chemistry" and not world_params.get("benchmark"):
- **PG-factory_lowlevel/router.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 128: if target_world == "ecosystem":
- **PG-factory_lowlevel/router.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 132: if target_world == "quasispecies":
- **PG-factory_lowlevel/router.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.