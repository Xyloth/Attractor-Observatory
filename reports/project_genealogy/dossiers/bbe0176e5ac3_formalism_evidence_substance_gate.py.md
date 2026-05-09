# Dossier: `formalism/evidence/substance_gate.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/bbe0176e5ac3_formalism_evidence_substance_gate.py.json`
- JSON content_hash: `sha256:e42f9104e22a9aed3d9fe640c3da1b83da5aae2eaeb1e9cc83e77edcd7882163`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `other`
- Generated status: `source`
- Lines: 194 / Bytes: 7415

## Birth
- Status: `recovered`
- First-seen commit: `215dbc12c2f8c0699a0993fe85164d27f61d6e0f`
- First-seen date: `2026-05-09T07:17:33-04:00`
- Spawn ticket: `TASK-CB-022`
- Cohort: `TASK-CB-022`

### Birth predicate atoms
- **tracked_artifact_present** — File is tracked under git but does not match a higher-priority family.

## Current
- Status: `recovered`
- Public symbols: `EvidenceTier, SubstanceGateResult, evaluate_source_bound, identifier_parsed, identifier_resolves, resolved_title, substance_audit_signed, title_matches_claim`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': [], 'verified': [], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Letter-vs-spirit surfaces: 5

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
- **PG-formalism/evidence/substance_gate.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 98: re.fullmatch(r"doi:10\.\S+/\S+", text, flags=re.IGNORECASE)
- **PG-formalism/evidence/substance_gate.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 99: or re.fullmatch(r"pmid:\d+", text, flags=re.IGNORECASE)
- **PG-formalism/evidence/substance_gate.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 100: or re.fullmatch(r"https?://\S+", text, flags=re.IGNORECASE)
- **PG-formalism/evidence/substance_gate.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 115: if status in {200, "200", "ok", "resolved"}:
- **PG-formalism/evidence/substance_gate.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 126: tokens.update(token[:-1] for token in list(tokens) if token.endswith("s") and len(token) > 5)

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.