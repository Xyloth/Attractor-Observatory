# Dossier: `BUILDER_INGESTION_MONITORING_PLAYBOOK.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/71d91606d5af_BUILDER_INGESTION_MONITORING_PLAYBOOK.md.json`
- JSON content_hash: `sha256:ef7e2e03209d47e462dfcf859f8666a770f41e2db614bfbac03a19fb01496dd6`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `driver_or_root_doc`
- Generated status: `source`
- Lines: 238 / Bytes: 10738

## Birth
- Status: `recovered`
- First-seen commit: `f1d7305d60c15c1177908245f22443d22cf86bf5`
- First-seen date: `2026-05-07T08:59:39-04:00`
- Spawn ticket: `CB-013`
- Cohort: `CB-013`

### Birth predicate atoms
- **driver_states_intent** — Driver/root doc declares a task or campaign intent that other artifacts can cite.
- **header_declared_intent** — # Builder Ingestion Monitoring Playbook
**Audience:** Claude Builder (any session — fresh or continuing) supervising the unattended Factory daemon.
**Goal:** detect anomalies in the running daemon, decide warn vs stop, execute the right shutdown / triage / resume sequence without ambiguity.
**Doctrine:** D7–D31. **D9 hard** — fail closed on doubt. **D17 hard** — stale data flagged stale. **D22 har

## Current
- Status: `recovered`
- Observed doctrines: `D11, D17, D19, D22, D24, D31, D7, D9`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D17', 'D19', 'D22', 'D24', 'D31', 'D7', 'D9'], 'verified': ['D11', 'D17', 'D19', 'D22', 'D24', 'D31', 'D7', 'D9'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Letter-vs-spirit surfaces: 1

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-BUILDER_INGESTION_MONITORING_PLAYBOOK.md-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 197: | `stale_cache_artifact`              | `reason.startswith("stale_cache:")`                | `D17_stale_cache_artifact` 

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.