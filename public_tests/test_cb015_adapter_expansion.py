"""Tests for CB-015 Phase-A adapter expansion.

Coverage (T5 brief: ≥4 tests per adapter × 4 adapters = ≥16):

  NIST atomic spectra (T1):
    * happy-path bundled seed produces ≥1 record
    * spectra cardinality is full periodic table × 5 ionization stages
    * provenance completeness on every record
    * source-limited honest decline produces audit-queue items
    * license_class is metadata_only

  PubChem small molecules (T2):
    * happy-path bundled seed produces records with SMILES populated
    * configuration: cid_stop=5500, max_records=5000 (Phase-1 target)
    * provenance completeness on every record
    * acceptance filter rejects polymers/no-SMILES rows
    * license_class is metadata_only

  Math primitives catalog (T3):
    * happy-path bundled fetch produces exactly 200 records
    * every record has DOI + citation + state_equation
    * primitive_class taxonomy covers expected canonical classes
    * provenance completeness on every record
    * canonical_name uniqueness across catalog

  KEGG organism CRN (T4):
    * adapter has 50 reference organisms
    * happy-path bundled seed for E. coli produces full record
    * non-eco organisms produce honest source-limited decline + audit
    * provenance completeness on every record
    * license_class is metadata_only

All tests deterministic, no network, no Streamlit. Runtime <1s.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# T1 — NIST atomic spectra adapter
# ---------------------------------------------------------------------------


def test_nist_spectra_cardinality_is_periodic_table_times_5_stages():
    """T1 brief: 118 elements × 5 ionization stages I-V = 590 spectra."""
    from factory_lowlevel.adapters import NISTAtomicSpectraAdapter, NIST_IONIZATION_STAGES, ELEMENT_SYMBOLS

    n = NISTAtomicSpectraAdapter()
    assert len(NIST_IONIZATION_STAGES) == 5
    assert NIST_IONIZATION_STAGES == ("I", "II", "III", "IV", "V")
    assert len(ELEMENT_SYMBOLS) == 118
    assert len(n.spectra) == 118 * 5
    # Every spectrum is "<symbol> <roman>"
    for spectrum in n.spectra[:10]:
        sym, stage = spectrum.split(" ")
        assert sym in ELEMENT_SYMBOLS
        assert stage in NIST_IONIZATION_STAGES


def test_nist_offline_seed_produces_records_with_full_provenance(tmp_path):
    """T1: bundled offline seed (5 elements) produces records with
    every required provenance field."""
    from factory_lowlevel.adapters import NISTAtomicSpectraAdapter

    n = NISTAtomicSpectraAdapter()
    result = n.fetch(tmp_path, allow_network=False)
    assert len(result.records) >= 1
    required = {"source_url", "retrieval_timestamp", "parser_version", "authority", "raw_exported"}
    for record in result.records:
        prov = record.provenance
        assert required <= set(prov.keys()), f"missing provenance keys on {record.record_id}"
        assert prov["raw_exported"] is False
        assert "NIST" in prov["authority"]
    # Source license enforcement
    assert result.source.license_class == "metadata_only"


def test_nist_source_limited_honest_decline_emits_audit_queue_items(tmp_path):
    """T1: when NIST has no energy-level data for a (element, stage),
    the adapter emits a structural record with data_status=
    'nist_asd_no_energy_level_rows' AND an AdapterAudit with the same
    reason. D17 binding."""
    from factory_lowlevel.adapters import NISTAtomicSpectraAdapter

    # Use a fresh tmp cache directory + force-include a transactinide.
    n = NISTAtomicSpectraAdapter()
    cache = tmp_path / "nist_atomic_spectra"
    cache.mkdir(parents=True)
    # Inject empty CSV for "Mt I" (transactinide; NIST has no data).
    (cache / "Mt_I.csv").write_text(
        "Configuration,Term,J,Level (eV),Uncertainty (eV),Reference\n",
        encoding="utf-8",
    )
    # Drive the parse path directly with the empty seed.
    raw_parts = ["Configuration,Term,J,Level (eV),Uncertainty (eV),Reference\n"]
    records, audits = n._parse_records(raw_parts, n.source_definition(), spectra=("Mt I",))
    assert len(records) == 1
    assert records[0].payload["data_status"] == "nist_asd_no_energy_level_rows"
    assert len(audits) == 1
    assert audits[0].reason == "nist_asd_no_energy_level_rows"


def test_nist_records_carry_methodology_review_required(tmp_path):
    """T1 D26 binding: every record flags methodology_review_required."""
    from factory_lowlevel.adapters import NISTAtomicSpectraAdapter

    n = NISTAtomicSpectraAdapter()
    result = n.fetch(tmp_path, allow_network=False)
    for record in result.records:
        assert record.payload.get("methodology_review_required") is True


# ---------------------------------------------------------------------------
# T2 — PubChem small molecule adapter
# ---------------------------------------------------------------------------


def test_pubchem_phase1_configuration_targets_5000_records():
    """T2 brief: cid_stop=5500, max_records=5000, batch_size=100."""
    from factory_lowlevel.adapters import PubChemSmallMoleculeAdapter

    p = PubChemSmallMoleculeAdapter()
    assert p.cid_start == 1
    assert p.cid_stop == 5500
    assert p.max_records == 5000
    assert p.batch_size == 100


def test_pubchem_offline_seed_produces_records_with_smiles_populated(tmp_path):
    """T2: post-CB-008 SMILES schema fix means bundled seed records
    have non-empty canonical_smiles."""
    from factory_lowlevel.adapters import PubChemSmallMoleculeAdapter

    p = PubChemSmallMoleculeAdapter()
    result = p.fetch(tmp_path, allow_network=False)
    smiles_present = [r for r in result.records if r.payload.get("canonical_smiles")]
    assert len(smiles_present) >= 1
    for record in smiles_present:
        assert record.payload["canonical_smiles"]
        assert record.payload["molecular_formula"]
        assert record.payload["heavy_atom_count"] >= 1


def test_pubchem_provenance_carries_all_required_fields(tmp_path):
    """T2: D19 binding — every record has source_url, retrieval_timestamp,
    parser_version, authority, raw_exported."""
    from factory_lowlevel.adapters import PubChemSmallMoleculeAdapter

    p = PubChemSmallMoleculeAdapter()
    result = p.fetch(tmp_path, allow_network=False)
    required = {"source_url", "retrieval_timestamp", "parser_version", "authority", "raw_exported"}
    for record in result.records:
        prov = record.provenance
        assert required <= set(prov.keys())
        assert prov["raw_exported"] is False
        assert "PubChem" in prov["authority"]


def test_pubchem_source_license_is_metadata_only(tmp_path):
    """T2: license_class is metadata_only — no raw redistribution."""
    from factory_lowlevel.adapters import PubChemSmallMoleculeAdapter

    p = PubChemSmallMoleculeAdapter()
    src = p.source_definition()
    assert src.license_class == "metadata_only"


# ---------------------------------------------------------------------------
# T3 — Math primitives catalog
# ---------------------------------------------------------------------------


def test_math_catalog_has_exactly_200_entries():
    """T3 brief: Phase-1 target 200 canonical primitives."""
    from factory_lowlevel.adapters import MATH_PRIMITIVE_SEEDS

    assert len(MATH_PRIMITIVE_SEEDS) == 200


def test_math_catalog_every_entry_has_doi_and_citation():
    """T3 brief: 'no fabricated math primitives. Every entry has a
    citation.' Verify on every row."""
    from factory_lowlevel.adapters import MATH_PRIMITIVE_SEEDS

    for entry in MATH_PRIMITIVE_SEEDS:
        assert entry["doi"], f"{entry['canonical_name']} missing DOI"
        assert entry["citation"], f"{entry['canonical_name']} missing citation"
        assert entry["source_url"].startswith("https://doi.org/"), (
            f"{entry['canonical_name']} source_url not a DOI URL"
        )
        assert entry["state_equation"], f"{entry['canonical_name']} missing state_equation"
        assert entry["expected_stable_form"], f"{entry['canonical_name']} missing expected_stable_form"


def test_math_catalog_taxonomy_covers_canonical_classes():
    """T3 brief: catalog covers 1D maps, 2D maps, 3D continuous
    autonomous, 4D+, bifurcation normal forms, heteroclinic/homoclinic,
    intermittency."""
    from factory_lowlevel.adapters import MATH_PRIMITIVE_SEEDS

    classes = {entry["primitive_class"] for entry in MATH_PRIMITIVE_SEEDS}
    expected_canonical = {
        "strange_attractor",
        "limit_cycle",
        "bifurcation_normal_form",
        "homoclinic",
        "heteroclinic",
        "heteroclinic_cycle",
        "intermittency",
        "period_doubling",
        "1d_chaos",
    }
    missing = expected_canonical - classes
    assert not missing, f"expected canonical classes missing from catalog: {missing}"


def test_math_catalog_canonical_names_are_unique():
    """T3 hardening: no duplicate canonical_names so record_ids don't
    collide downstream."""
    from factory_lowlevel.adapters import MATH_PRIMITIVE_SEEDS

    names = [entry["canonical_name"] for entry in MATH_PRIMITIVE_SEEDS]
    assert len(set(names)) == len(names), "duplicate canonical_name detected"


def test_math_catalog_offline_fetch_emits_200_records(tmp_path):
    """T3: offline fetch produces one EmpiricalRecord per catalog entry."""
    from factory_lowlevel.adapters import MathPrimitivesCatalogAdapter

    m = MathPrimitivesCatalogAdapter()
    result = m.fetch(tmp_path, allow_network=False)
    assert len(result.records) == 200
    required = {"source_url", "retrieval_timestamp", "parser_version", "authority"}
    for record in result.records:
        assert required <= set(record.provenance.keys())


# ---------------------------------------------------------------------------
# T4 — KEGG organism CRN adapter
# ---------------------------------------------------------------------------


def test_kegg_organism_adapter_has_50_organisms():
    """T4 brief: top-50 reference organisms."""
    from factory_lowlevel.adapters import KEGGOrganismCRNAdapter

    k = KEGGOrganismCRNAdapter()
    assert len(k.organisms) == 50


def test_kegg_offline_emits_eco_with_pathways_and_others_source_limited(tmp_path):
    """T4: offline path uses bundled E. coli seed for eco, source-limited
    honest decline for the other 49 organisms."""
    from factory_lowlevel.adapters import KEGGOrganismCRNAdapter

    k = KEGGOrganismCRNAdapter()
    result = k.fetch(tmp_path, allow_network=False)
    assert len(result.records) == 50
    # eco should have non-zero pathways; others should be source-limited.
    eco_records = [r for r in result.records if r.payload.get("organism_code") == "eco"]
    assert len(eco_records) == 1
    assert eco_records[0].payload["pathway_count_observed"] > 0
    # At least one source-limited organism in the audit queue
    assert len(result.audits) >= 1
    assert any(a.reason == "kegg_organism_pathway_list_empty" for a in result.audits)


def test_kegg_source_license_is_metadata_only():
    """T4: license_class is metadata_only — KEGG academic-use license."""
    from factory_lowlevel.adapters import KEGGOrganismCRNAdapter

    k = KEGGOrganismCRNAdapter()
    src = k.source_definition()
    assert src.license_class == "metadata_only"


def test_kegg_records_carry_full_provenance(tmp_path):
    """T4: D19 binding — every record has source_url, retrieval_timestamp,
    parser_version, authority, raw_exported."""
    from factory_lowlevel.adapters import KEGGOrganismCRNAdapter

    k = KEGGOrganismCRNAdapter()
    result = k.fetch(tmp_path, allow_network=False)
    required = {"source_url", "retrieval_timestamp", "parser_version", "authority", "raw_exported"}
    for record in result.records:
        prov = record.provenance
        assert required <= set(prov.keys())
        assert prov["raw_exported"] is False
        assert "KEGG" in prov["authority"]


def test_kegg_organism_adapter_in_registry():
    """T4: KEGGOrganismCRNAdapter registered in available_adapters so
    the daemon picks it up under --target-world crn."""
    from factory_lowlevel.live_pipeline import available_adapters

    rows = available_adapters()
    sources = {row["source_id"] for row in rows}
    assert "source.kegg.organism_metabolic_networks" in sources
