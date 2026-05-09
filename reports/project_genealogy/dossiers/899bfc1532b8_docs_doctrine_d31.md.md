# Dossier: `docs/doctrine_d31.md`

> JSON is authoritative. This file is a rendering of the JSON dossier.

- JSON: `reports/project_genealogy/dossiers/899bfc1532b8_docs_doctrine_d31.md.json`
- JSON content_hash: `sha256:82e8450ee740c0db4c4fe39f6e23f21b52e037399123de7a54b9e99fcdaf17be`
- Schema: `ProjectGenealogyDossier.v1`
- Artifact family: `doctrine`
- Generated status: `source`
- Lines: 39 / Bytes: 2572

## Birth
- Status: `recovered`
- First-seen commit: `60d3171a987fb3de940669461c63d084a8e3dd32`
- First-seen date: `2026-05-07T07:50:30-04:00`
- Spawn ticket: `TASK-FLOOR-BFG`
- Cohort: `TASK-FLOOR-BFG`

### Birth predicate atoms
- **binding_rule_named** — Document declares a binding doctrine rule with a numbered ID and ratification.
- **header_declared_intent** — # D31 - BFG Measurement Split
**Status:** ratified during TASK-FLOOR-BFG / Campaign 026.
**Mode:** foundational.
**Failure mode caught:** Basin-Floor Geometry self-match, where a floor-connectivity predicate and a basin-geometry lens both read perturbation-outcome equivalence fibers and then substrate-blocked control validates circular evidence.
## Binding Text
> floor_connectivity-class predicate

## Current
- Status: `recovered`
- Observed doctrines: `D21, D26, D27, D31`

## DepthVector.v1
- **predicate_atom_coverage**: `{'claimable_atoms': 2, 'covered_atoms': 2, 'missing_atoms': [], 'value': 1.0}`
- **adversarial_surface_coverage**: `{'required_bad_cases': [], 'covered_bad_cases': [], 'missing_bad_cases': [], 'value': None}`
- **doctrine_binding_quality**: `{'required': ['D21', 'D26', 'D27', 'D31'], 'verified': ['D21', 'D26', 'D27', 'D31'], 'claimed_only': [], 'missing': [], 'contradicted': [], 'not_applicable': []}`
- **evidence_integration**: `{'source_bound_claims': 3, 'dereferenceable_evidence_refs': 3, 'private_evidence_refs': 0, 'unresolved_evidence_refs': 0, 'audit_queue_or_falsifier_route': 'present'}`
- **operational_load_bearingness**: `{'imports_in': 0, 'imports_out': 0, 'generates_artifacts': [], 'validated_by': [], 'cited_by_reports': ['docs/doctrine_registry.json'], 'weighted_value': 1.5}`

## Drift
- Status: `review_required`
- Doctrine boundary crossings: 2

## Liveness
- Cleanup candidate status: `probe_declined`
- Cleanup reason: critical-path file (persistence/lock/schema/adapter or shipped public surface); per-file stash/restore would risk irreversible state
- Probe outcome: `declined`
- Probe decline reason: `removal_probe_declined_critical_path`

## Findings
- **PG-docs/doctrine_d31.md-drift-review** (medium, hypothesis): Drift requires review: missing or new atoms or letter-vs-spirit surfaces present without yet crossing a doctrine boundary.

---

Reproducer: regenerate this dossier with `python -m project_genealogy run-pass2`.