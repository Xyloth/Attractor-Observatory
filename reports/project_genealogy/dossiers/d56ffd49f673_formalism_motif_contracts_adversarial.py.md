# Dossier: `formalism/motif_contracts/adversarial.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/d56ffd49f673_formalism_motif_contracts_adversarial.py.json`
- JSON content_hash: `sha256:535f6d4207f8ffc3e68d13b4b880e0b69df659f2ddbf95a15fee6b90fdd32dba`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `other`
- Generated status: `source`
- Lines: 323 / Bytes: 10548

## Birth
- Status: `recovered`
- First-seen commit: `20c8c938e8f7e7abf1af4a8348c0983ddae455de`
- First-seen date: `2026-05-09T07:11:04-04:00`
- Spawn ticket: `TASK-CB-022`
- Cohort: `TASK-CB-022`

### Birth predicate atoms
- **tracked_artifact_present** — File is tracked under git but does not match a higher-priority family.

## Current
- Status: `recovered`
- Public symbols: `event_token_rename, generator_id_erasure, metadata_identity_erasure, payload_key_rename, run_adversarial_controls, run_controls_for_corpus, run_lens_adversarial_controls, run_lens_controls_for_corpus, state_key_rename, value_label_erasure`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': [], 'verified': [], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Letter-vs-spirit surfaces: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-formalism/motif_contracts/adversarial.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 107: if key == "t_sim":
- **PG-formalism/motif_contracts/adversarial.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 128: if key_text in GENERATOR_ID_KEYS or key_text.endswith("_generator_id"):

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.