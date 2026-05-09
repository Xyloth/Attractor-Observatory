# Dossier: `project_genealogy/current.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/ee21b3fc9e69_project_genealogy_current.py.json`
- JSON content_hash: `sha256:cb568a71c0ea287e32aaa195c93ee4d1ddc511d62db3e6dd04c6b515351abd03`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `audit_instrument`
- Generated status: `source`
- Lines: 361 / Bytes: 12860

## Birth
- Status: `recovered`
- First-seen commit: `2d3b03b3ca5b35945309f2264f5c8cf30d450697`
- First-seen date: `2026-05-08T15:48:43-04:00`
- Spawn ticket: `PG-001`
- Cohort: `PG-001`

### Birth predicate atoms
- **audit_instrument_executes** — Module is part of the PG-001 audit instrument and exposes a callable surface.

## Current
- Status: `recovered`
- Public symbols: `detect_class_pattern_matches, detect_doctrine_mentions, detect_letter_vs_spirit_surfaces, extract_current, find_pytest_functions, python_public_symbols`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 1, 'covered_atoms': 1, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [{'id': 'error_branch', 'line': 103}, {'id': 'error_branch', 'line': 134}, {'id': 'error_branch', 'line': 229}, {'id': 'decline_branch', 'line': None}], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D11', 'D19', 'D20'], 'verified': [], 'claimed_only': ['D11', 'D19', 'D20'], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 4, 'dereferenceable_evidence_refs': 4, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': [], 'weighted_value': 0.0}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 9

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-project_genealogy/current.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 103: except SyntaxError:
- **PG-project_genealogy/current.py-lvs-1** (info, hypothesis): Detected letter-coupled fix surface at line 108: if not node.name.startswith("_"):
- **PG-project_genealogy/current.py-lvs-2** (info, hypothesis): Detected letter-coupled fix surface at line 111: if not node.name.startswith("_"):
- **PG-project_genealogy/current.py-lvs-3** (info, hypothesis): Detected letter-coupled fix surface at line 134: except SyntaxError:
- **PG-project_genealogy/current.py-lvs-4** (info, hypothesis): Detected letter-coupled fix surface at line 139: if node.name.startswith("test_"):
- **PG-project_genealogy/current.py-lvs-5** (info, hypothesis): Detected letter-coupled fix surface at line 229: except OSError:
- **PG-project_genealogy/current.py-lvs-6** (info, hypothesis): Detected letter-coupled fix surface at line 245: line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
- **PG-project_genealogy/current.py-lvs-7** (info, hypothesis): Detected letter-coupled fix surface at line 252: if rel_path.endswith(".py"):
- **PG-project_genealogy/current.py-lvs-8** (info, hypothesis): Detected letter-coupled fix surface at line 310: if re.search(pattern, text, re.IGNORECASE):
- **PG-project_genealogy/current.py-class-0** (low, hypothesis): Detected pattern matching Class3 (soft enforcement comments) at line 178
- **PG-project_genealogy/current.py-class-1** (low, hypothesis): Detected pattern matching Class12 (decorative completeness) at line 188
- **PG-project_genealogy/current.py-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.