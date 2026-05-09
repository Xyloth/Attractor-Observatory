# Dossier: `public_tests/test_cb015_adapter_expansion.py`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/cd648c50dcac_public_tests_test_cb015_adapter_expansion.py.json`
- JSON content_hash: `sha256:06d44c310a12bbcbf279b8210fcae95998c15ee5b6a250f1a6bd18a43f382b85`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `test`
- Generated status: `source`
- Lines: 323 / Bytes: 13615

## Birth
- Status: `recovered`
- First-seen commit: `0f5947c275a05c6cfc48e149ca4e3cd1733039bd`
- First-seen date: `2026-05-07T12:23:48-04:00`
- Spawn ticket: `TASK-CB-015`
- Cohort: `TASK-CB-015`

### Birth predicate atoms
- **behavior_assertion_present** — Module exposes at least one assert-bearing pytest function.
- **header_declared_intent** — Tests for CB-015 Phase-A adapter expansion.

Coverage (T5 brief: ≥4 tests per adapter × 4 adapters = ≥16):

  NIST atomic spectra (T1):
    * happy-path bundled seed produces ≥1 record
    * spectra cardinality is full periodic table × 5 ionization stages
    * provenance completeness on every record
    * source-limited honest decline produces audit-queue items
    * license_class is metadata_onl

## Current
- Status: `recovered`
- Public symbols: `test_kegg_offline_emits_eco_with_pathways_and_others_source_limited, test_kegg_organism_adapter_has_50_organisms, test_kegg_organism_adapter_in_registry, test_kegg_records_carry_full_provenance, test_kegg_source_license_is_metadata_only, test_math_catalog_canonical_names_are_unique, test_math_catalog_every_entry_has_doi_and_citation, test_math_catalog_has_exactly_200_entries, test_math_catalog_offline_fetch_emits_200_records, test_math_catalog_taxonomy_covers_canonical_classes`
- Observed doctrines: `D17, D19, D26`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D17', 'D19', 'D26'], 'verified': ['D17', 'D19', 'D26'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 5, 'dereferenceable_evidence_refs': 5, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'absent'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['BUILD_LOG.md'], 'weighted_value': 1.5}`

## Drift
- Status: `positive_deepening`
- Doctrine boundary crossings: 3
- Letter-vs-spirit surfaces: 1

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-public_tests/test_cb015_adapter_expansion.py-lvs-0** (info, hypothesis): Detected letter-coupled fix surface at line 206: assert entry["source_url"].startswith("https://doi.org/"), (

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.