"""TASK-CB-018 Phase-2 mass-density expansion — per-adapter tests.

Pins the Phase-2 target counts and contract for each of the 16 adapters
expanded in CB-018. Each test does an offline cache-only fetch against
a tmp_path cache_dir and checks:

* Record count meets the offline-mode floor (full Phase-2 counts only
  emerge under --allow-network with a populated cache; offline mode
  hits the bundled-seed limit per adapter, which is the floor).
* Per-record full provenance per ADAPTER_PAYLOAD_CONTRACT.md
  (source_url, retrieval_timestamp, parser_version, authority,
  raw_exported).
* License class set per source.
* Where contract demands `world_parameters`, the router-required keys
  appear in payload['world_parameters'].

Plus aggregate tests:
* `MATH_PRIMITIVE_SEEDS` >= 600 entries (Phase-2 catalog density).
* All canonical_names unique across the catalog.
* `KEGG_REFERENCE_ORGANISMS` >= 300 entries.
* `NIST_IONIZATION_STAGES` covers I through XXX.
* `PubChemSmallMoleculeAdapter` cid_stop >= 75000, max_records >= 50000.

Runtime <2s total. No network, no Streamlit.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------


REQUIRED_PROVENANCE_KEYS = {
    "source_url",
    "retrieval_timestamp",
    "parser_version",
    "authority",
    "raw_exported",
}


def _check_record_provenance(record) -> None:
    """Assert per-record provenance contract. D19 binding."""
    missing = REQUIRED_PROVENANCE_KEYS - set(record.provenance.keys())
    assert not missing, f"record {record.record_id[:16]} missing provenance keys: {missing}"
    assert record.license_class, f"record {record.record_id[:16]} has empty license_class"
    assert record.canonical_name, f"record {record.record_id[:16]} has empty canonical_name"
    assert record.world_family, f"record {record.record_id[:16]} has empty world_family"


# ---------------------------------------------------------------------------
# T1 — NIST atomic spectra (Phase-2 stages I-XXX expansion)
# ---------------------------------------------------------------------------


def test_t1_nist_ionization_stages_extended_to_30(tmp_path):
    from factory_lowlevel.adapters import NIST_IONIZATION_STAGES, NISTAtomicSpectraAdapter, ELEMENT_SYMBOLS
    assert len(NIST_IONIZATION_STAGES) == 30, f"Phase-2 expects 30 stages, got {len(NIST_IONIZATION_STAGES)}"
    assert NIST_IONIZATION_STAGES[0] == "I"
    assert NIST_IONIZATION_STAGES[-1] == "XXX"
    # Cartesian: 118 elements x 30 stages = 3540 spectra
    assert len(NISTAtomicSpectraAdapter.spectra) == 118 * 30 == 3540


def test_t1_nist_offline_fetch(tmp_path):
    """Offline mode falls back to bundled-seed (5 spectra). Records carry full provenance."""
    from factory_lowlevel.adapters import NISTAtomicSpectraAdapter
    adapter = NISTAtomicSpectraAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) >= 5, "expected offline-bundled-seed records"
    for r in result.records:
        _check_record_provenance(r)
        assert r.world_family == "atomic_molecular_primitives"


# ---------------------------------------------------------------------------
# T2 — PubChem small-molecule expansion
# ---------------------------------------------------------------------------


def test_t2_pubchem_phase_2_constants(tmp_path):
    from factory_lowlevel.adapters import PubChemSmallMoleculeAdapter
    assert PubChemSmallMoleculeAdapter.cid_stop >= 75000, "Phase-2 cid_stop must reach 75K+"
    assert PubChemSmallMoleculeAdapter.max_records >= 50000, "Phase-2 max_records must hit 50K target"
    assert PubChemSmallMoleculeAdapter.cid_start == 1
    assert PubChemSmallMoleculeAdapter.batch_size == 100


def test_t2_pubchem_offline_fetch(tmp_path):
    from factory_lowlevel.adapters import PubChemSmallMoleculeAdapter
    adapter = PubChemSmallMoleculeAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) >= 5
    for r in result.records:
        _check_record_provenance(r)
        assert r.world_family == "atomic_molecular_primitives"


# ---------------------------------------------------------------------------
# T3 — Math primitives catalog (600+ entries)
# ---------------------------------------------------------------------------


def test_t3_math_primitives_catalog_size():
    from factory_lowlevel._math_primitives_catalog import ALL_MATH_PRIMITIVE_SEEDS
    assert 600 <= len(ALL_MATH_PRIMITIVE_SEEDS) <= 650, (
        f"Phase-2 math catalog must be 600-650, got {len(ALL_MATH_PRIMITIVE_SEEDS)}"
    )


def test_t3_math_primitives_unique_canonical_names():
    from factory_lowlevel._math_primitives_catalog import ALL_MATH_PRIMITIVE_SEEDS
    names = [r["canonical_name"] for r in ALL_MATH_PRIMITIVE_SEEDS]
    assert len(set(names)) == len(names), (
        f"duplicate canonical_names: {len(names) - len(set(names))} duplicates"
    )


def test_t3_math_primitives_have_required_fields():
    from factory_lowlevel._math_primitives_catalog import ALL_MATH_PRIMITIVE_SEEDS
    required = {"canonical_name", "primitive_class", "dimension", "state_equation",
                "parameters", "expected_stable_form", "doi", "source_url", "citation"}
    for entry in ALL_MATH_PRIMITIVE_SEEDS:
        missing = required - set(entry.keys())
        assert not missing, f"entry {entry.get('canonical_name', '?')} missing fields: {missing}"


def test_t3_math_primitives_offline_fetch(tmp_path):
    from factory_lowlevel.adapters import MathPrimitivesCatalogAdapter
    adapter = MathPrimitivesCatalogAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) >= 600
    for r in result.records[:50]:  # spot-check first 50
        _check_record_provenance(r)
        assert r.world_family == "math_primitives"
        # Phase-2 contract: math_primitives needs primitive_class, dimension, state_equation
        # at top-level payload (not under world_parameters per ADAPTER_PAYLOAD_CONTRACT.md)
        assert "primitive_class" in r.payload
        assert "dimension" in r.payload
        assert "state_equation" in r.payload


# ---------------------------------------------------------------------------
# T4 — KEGG organism expansion (~330+ static, default cap 500)
# ---------------------------------------------------------------------------


def test_t4_kegg_static_roster_expanded():
    from factory_lowlevel.adapters import KEGG_REFERENCE_ORGANISMS
    assert len(KEGG_REFERENCE_ORGANISMS) >= 300, (
        f"Phase-2 KEGG roster must be >= 300 organisms, got {len(KEGG_REFERENCE_ORGANISMS)}"
    )
    # Spot-check kingdom diversity
    kingdoms = {kingdom for _, _, kingdom in KEGG_REFERENCE_ORGANISMS}
    assert kingdoms == {"bacteria", "archaea", "eukaryote"}, (
        f"expected {{bacteria, archaea, eukaryote}}, got {kingdoms}"
    )


def test_t4_kegg_default_max_organisms_cap():
    from factory_lowlevel.adapters import KEGGOrganismCRNAdapter
    assert KEGGOrganismCRNAdapter.DEFAULT_MAX_ORGANISMS >= 500
    adapter = KEGGOrganismCRNAdapter()
    assert len(adapter.organisms) >= 300, (
        f"default-constructed adapter should have >= 300 organisms"
    )


def test_t4_kegg_offline_fetch(tmp_path):
    from factory_lowlevel.adapters import KEGGOrganismCRNAdapter
    adapter = KEGGOrganismCRNAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    # Offline: most organisms produce honest-decline records (no cached pathway list)
    # but the adapter still emits one record per organism
    assert len(result.records) >= 300
    for r in result.records[:20]:
        _check_record_provenance(r)
        assert r.world_family == "crn"
        # CRN router contract: world_parameters must contain initial_state + reactions
        wp = r.payload.get("world_parameters", {})
        assert "initial_state" in wp
        assert "reactions" in wp


# ---------------------------------------------------------------------------
# T5 — Szostak Liposome Protocell (Phase-2: 200)
# ---------------------------------------------------------------------------


def test_t5_szostak_protocell_phase_2(tmp_path):
    from factory_lowlevel.adapters import SzostakLiposomeProtocellAdapter
    assert SzostakLiposomeProtocellAdapter.phase1_target_count == 200
    assert len(SzostakLiposomeProtocellAdapter.seeds) >= 4, (
        "Phase-2 protocell expects orthogonal seeds: Szostak + RNA-vesicle + PURE TX/TL + lipid-world + Luisi"
    )
    adapter = SzostakLiposomeProtocellAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 200
    for r in result.records[:10]:
        _check_record_provenance(r)
        assert r.world_family == "protocell"
        wp = r.payload.get("world_parameters", {})
        assert "scenario_id" in wp or "benchmark" in wp


# ---------------------------------------------------------------------------
# T6 — Reaction-Diffusion (Phase-2: 300)
# ---------------------------------------------------------------------------


def test_t6_reaction_diffusion_phase_2(tmp_path):
    from factory_lowlevel.adapters import ReactionDiffusionBenchmarkAdapter
    assert ReactionDiffusionBenchmarkAdapter.phase1_target_count == 300
    adapter = ReactionDiffusionBenchmarkAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 300
    for r in result.records[:10]:
        _check_record_provenance(r)
        assert r.world_family == "field"


# ---------------------------------------------------------------------------
# T7 — FlyBase / WormBase / ZFIN morphogenesis (Phase-2: 500)
# ---------------------------------------------------------------------------


def test_t7_morphogenesis_phase_2(tmp_path):
    from factory_lowlevel.adapters import FlyBaseMorphogenProfileAdapter
    assert FlyBaseMorphogenProfileAdapter.phase1_target_count == 500
    assert len(FlyBaseMorphogenProfileAdapter.seeds) >= 6, (
        "Phase-2 morphogenesis expects FlyBase + WormBase + ZFIN orthogonal seeds"
    )
    adapter = FlyBaseMorphogenProfileAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 500
    for r in result.records[:10]:
        _check_record_provenance(r)
        assert r.world_family == "morphogenesis"


# ---------------------------------------------------------------------------
# T8 — Avida digital traces (Phase-2: 200)
# ---------------------------------------------------------------------------


def test_t8_avida_digital_phase_2(tmp_path):
    from factory_lowlevel.adapters import AvidaDigitalTraceAdapter
    assert AvidaDigitalTraceAdapter.phase1_target_count == 200
    assert len(AvidaDigitalTraceAdapter.seeds) >= 5, (
        "Phase-2 Avida expects diverse runs: copy + equ + punctuated + parasite + robustness + env-change"
    )
    adapter = AvidaDigitalTraceAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 200
    for r in result.records[:5]:
        _check_record_provenance(r)
        assert r.world_family == "digital"


# ---------------------------------------------------------------------------
# T9 — GBIF Jornada ecosystem (Phase-2: 500)
# ---------------------------------------------------------------------------


def test_t9_gbif_ecosystem_phase_2(tmp_path):
    from factory_lowlevel.adapters import GBIFJornadaEcosystemAdapter, GBIF_JORNADA_ECOSYSTEM_SEED
    assert GBIFJornadaEcosystemAdapter.phase1_target_count == 500
    taxa = GBIF_JORNADA_ECOSYSTEM_SEED["taxa"]
    assert len(taxa) >= 20, (
        f"Phase-2 GBIF expects >= 20 taxa across 5 guilds; got {len(taxa)}"
    )
    guilds = {t["guild"] for t in taxa}
    assert "pollinator" in guilds, "Phase-2 GBIF added pollinator guild for orthogonal coverage"
    adapter = GBIFJornadaEcosystemAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 500
    for r in result.records[:5]:
        _check_record_provenance(r)
        assert r.world_family == "ecosystem"


# ---------------------------------------------------------------------------
# T10 — Movebank swarm (Phase-2: 300)
# ---------------------------------------------------------------------------


def test_t10_movebank_swarm_phase_2(tmp_path):
    from factory_lowlevel.adapters import MovebankSwarmBehaviorAdapter
    assert MovebankSwarmBehaviorAdapter.phase1_target_count == 300
    assert len(MovebankSwarmBehaviorAdapter.seeds) >= 6, (
        "Phase-2 swarm expects >= 6 species/behavior orthogonal seeds"
    )
    adapter = MovebankSwarmBehaviorAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 300
    for r in result.records[:5]:
        _check_record_provenance(r)
        assert r.world_family == "swarm"


# ---------------------------------------------------------------------------
# T11 — Allen Brain cognitive (Phase-2: 300)
# ---------------------------------------------------------------------------


def test_t11_allen_brain_cognitive_phase_2(tmp_path):
    from factory_lowlevel.adapters import AllenBrainCognitiveAdapter
    assert AllenBrainCognitiveAdapter.phase1_target_count == 300
    assert len(AllenBrainCognitiveAdapter.seeds) >= 6, (
        "Phase-2 cognitive expects cortex region x species x task orthogonal seeds"
    )
    # Cortex region diversity
    regions = {s["world_parameters"].get("cortex_region") for s in AllenBrainCognitiveAdapter.seeds if "cortex_region" in s["world_parameters"]}
    assert len(regions) >= 4, f"expected diverse cortex regions, got {regions}"
    adapter = AllenBrainCognitiveAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 300
    for r in result.records[:5]:
        _check_record_provenance(r)
        assert r.world_family == "cognitive"


# ---------------------------------------------------------------------------
# T12 — Prebiotic chemistry (Phase-2: 300)
# ---------------------------------------------------------------------------


def test_t12_prebiotic_chemistry_phase_2(tmp_path):
    from factory_lowlevel.adapters import PrebioticChemistryCatalogAdapter
    assert PrebioticChemistryCatalogAdapter.phase1_target_count == 300
    adapter = PrebioticChemistryCatalogAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 300
    for r in result.records[:5]:
        _check_record_provenance(r)
        assert r.world_family == "origins_chemistry"


# ---------------------------------------------------------------------------
# T13 — BioModels hypergraph (Phase-2: 200)
# ---------------------------------------------------------------------------


def test_t13_biomodels_hypergraph_phase_2(tmp_path):
    from factory_lowlevel.adapters import BioModelsHypergraphAdapter
    assert BioModelsHypergraphAdapter.phase1_target_count == 200
    assert len(BioModelsHypergraphAdapter.seeds) >= 5
    adapter = BioModelsHypergraphAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 200
    for r in result.records[:5]:
        _check_record_provenance(r)
        assert r.world_family == "hypergraph_reactions"


# ---------------------------------------------------------------------------
# T14 — NCBI quasispecies (Phase-2: 500 across 4 accessions)
# ---------------------------------------------------------------------------


def test_t14_ncbi_quasispecies_phase_2(tmp_path):
    from factory_lowlevel.adapters import NCBIHIVQuasispeciesAdapter, NCBI_QUASISPECIES_ACCESSIONS
    assert NCBIHIVQuasispeciesAdapter.phase1_target_count == 500
    assert len(NCBI_QUASISPECIES_ACCESSIONS) == 4, (
        f"Phase-2 expects 4 accessions: HIV-1, flu, SARS-CoV-2, TP53; got {len(NCBI_QUASISPECIES_ACCESSIONS)}"
    )
    accessions = [a[0] for a in NCBI_QUASISPECIES_ACCESSIONS]
    assert "K03455.1" in accessions, "HIV-1 HXB2 baseline must remain"
    assert "MN908947.3" in accessions, "SARS-CoV-2 Wuhan-Hu-1 added"
    adapter = NCBIHIVQuasispeciesAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 500
    # Records should span all accessions
    seen_accessions = {r.payload.get("accession") for r in result.records}
    assert len(seen_accessions) == 4, f"all 4 accessions emit records; got {seen_accessions}"
    for r in result.records[:5]:
        _check_record_provenance(r)
        assert r.world_family == "quasispecies"


# ---------------------------------------------------------------------------
# T15 — NCBI endosymbiosis (Phase-2: 200)
# ---------------------------------------------------------------------------


def test_t15_ncbi_endosymbiosis_phase_2(tmp_path):
    from factory_lowlevel.adapters import NCBIEndosymbiosisGenomeAdapter
    assert NCBIEndosymbiosisGenomeAdapter.phase1_target_count == 200
    assert len(NCBIEndosymbiosisGenomeAdapter.seeds) >= 6
    adapter = NCBIEndosymbiosisGenomeAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 200
    for r in result.records[:5]:
        _check_record_provenance(r)
        assert r.world_family == "symbiogenesis"


# ---------------------------------------------------------------------------
# T16 — Physiome multiscale (Phase-2: 50)
# ---------------------------------------------------------------------------


def test_t16_physiome_multiscale_phase_2(tmp_path):
    from factory_lowlevel.adapters import PhysiomeMultiscaleAdapter
    assert PhysiomeMultiscaleAdapter.phase1_target_count == 50
    assert len(PhysiomeMultiscaleAdapter.seeds) >= 4, (
        "Phase-2 multiscale expansion adds cardiac, lung, muscle, kidney models"
    )
    adapter = PhysiomeMultiscaleAdapter()
    result = adapter.fetch(cache_dir=str(tmp_path / "cache"), allow_network=False)
    assert len(result.records) == 50
    for r in result.records[:5]:
        _check_record_provenance(r)
        assert r.world_family == "multiscale"


# ---------------------------------------------------------------------------
# T17 — End-to-end aggregate verify (offline cycle)
# ---------------------------------------------------------------------------


def test_t17_aggregate_offline_cycle_no_exceptions(tmp_path):
    """Run all 16 Phase-2 adapters in offline cache-only mode through fetch().
    Every adapter must complete without raising; aggregate record count
    must hit a substantial floor."""
    from factory_lowlevel.adapters import (
        NISTAtomicSpectraAdapter, PubChemSmallMoleculeAdapter, MathPrimitivesCatalogAdapter,
        KEGGOrganismCRNAdapter, SzostakLiposomeProtocellAdapter,
        ReactionDiffusionBenchmarkAdapter, FlyBaseMorphogenProfileAdapter,
        AvidaDigitalTraceAdapter, GBIFJornadaEcosystemAdapter,
        MovebankSwarmBehaviorAdapter, AllenBrainCognitiveAdapter,
        PrebioticChemistryCatalogAdapter, BioModelsHypergraphAdapter,
        NCBIHIVQuasispeciesAdapter, NCBIEndosymbiosisGenomeAdapter,
        PhysiomeMultiscaleAdapter,
    )
    adapter_classes = [
        NISTAtomicSpectraAdapter, PubChemSmallMoleculeAdapter, MathPrimitivesCatalogAdapter,
        KEGGOrganismCRNAdapter, SzostakLiposomeProtocellAdapter,
        ReactionDiffusionBenchmarkAdapter, FlyBaseMorphogenProfileAdapter,
        AvidaDigitalTraceAdapter, GBIFJornadaEcosystemAdapter,
        MovebankSwarmBehaviorAdapter, AllenBrainCognitiveAdapter,
        PrebioticChemistryCatalogAdapter, BioModelsHypergraphAdapter,
        NCBIHIVQuasispeciesAdapter, NCBIEndosymbiosisGenomeAdapter,
        PhysiomeMultiscaleAdapter,
    ]
    cache_dir = tmp_path / "cycle_cache"
    total = 0
    for cls in adapter_classes:
        adapter = cls()
        result = adapter.fetch(cache_dir=str(cache_dir), allow_network=False)
        assert len(result.records) > 0, f"{cls.__name__} produced 0 records in offline mode"
        total += len(result.records)
    # Phase-2 offline floor: 4500 records (NIST/PubChem at bundled-seed limits + all upper worlds + math + KEGG)
    assert total >= 4500, f"Phase-2 offline aggregate must be >= 4500, got {total}"
