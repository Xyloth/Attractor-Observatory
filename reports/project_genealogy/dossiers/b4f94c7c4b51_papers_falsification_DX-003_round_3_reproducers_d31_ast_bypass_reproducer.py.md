# Dossier: `papers/falsification/DX-003/round_3_reproducers/d31_ast_bypass_reproducer.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/b4f94c7c4b51_papers_falsification_DX-003_round_3_reproducers_d31_ast_bypass_reproducer.py.json`
- JSON content_hash: `sha256:6a40f22e31ea6fa6d7e0431c4159295b19346cef2ad663b4fb93199fe76ad79f`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `paper`
- Generated status: `source`
- Lines: 16 / Bytes: 1071

## Birth
- Status: `recovered`
- First-seen commit: `2eb181f5b951c4a84b344468c7a366371058cb46`
- First-seen date: `2026-05-08T17:59:37-04:00`
- Spawn ticket: `DX-003`
- Cohort: `DX-003`

### Birth predicate atoms
- **paper_artifact_in_falsifier_or_prereg** — Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.
- **header_declared_intent** — ﻿from pathlib import Path
from formalism.floor_bfg.read_separation import assert_d31_read_separation
root = Path('papers/falsification/DX-003/round_3_reproducers/d31_fake_root')
(root / 'formalism/floor_bfg').mkdir(parents=True, exist_ok=True)
(root / 'formalism/motif_contracts/predicates').mkdir(parents=True, exist_ok=True)
(root / 'formalism/floor_bfg/lenses.py').write_text('''
def evil_lens(tra

## Current
- Status: `recovered`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D18'], 'verified': [], 'claimed_only': ['D17', 'D18'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `unknown`
- Cleanup reason: PG-001 v1 declines per-file removal probes globally under removal_probe_over_budget; status defaults to unknown rather than over-claiming removable_clean
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_over_budget`

## Findings
_No findings detected mechanically._

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.