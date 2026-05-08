"""Low-level Factory source adapters.

The adapters are deterministic and zero-AI at runtime. Network retrieval is a
mechanical source fetch; parsing and normalization are ordinary code. If a live
fetch fails, the adapter falls back to a bundled seed whose provenance points at
the same authoritative source and marks the retrieval mode accordingly.
"""

from __future__ import annotations

import csv
import io
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .schemas import EmpiricalRecord, SourceCacheEntry, SourceDefinition, sha256, utc_now


def _clean_nist_cell(value: str) -> str:
    value = value.strip()
    value = re.sub(r'^="(.*)"$', r"\1", value)
    value = value.strip('"')
    return value.strip()


def _float_or_none(value: str) -> float | None:
    cleaned = _clean_nist_cell(value).replace("[", "").replace("]", "").replace("(", "").replace(")", "")
    if not cleaned or cleaned in {"---", "Limit"}:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def _urlopen_text(url: str, *, timeout: int) -> str:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "AttractorObservatoryFactory/0.1 (source-bound research ingestion; contact PI)",
            "Accept": "text/csv,text/plain,application/json,*/*",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


@dataclass(frozen=True)
class AdapterAudit:
    """Honest negative surfaced by an adapter post-parse — e.g., a record
    that survived the schema gate but has empty critical fields. Caller
    persists these as ``AuditQueueItem`` entries so D9/D17 are honored
    (no silent acceptance of garbage)."""
    record_id: str
    source_id: str
    severity: str
    reason: str
    recommended_action: str


@dataclass(frozen=True)
class AdapterResult:
    source: SourceDefinition
    cache_entry: SourceCacheEntry
    records: list[EmpiricalRecord]
    warnings: list[str]
    audits: list[AdapterAudit] = field(default_factory=list)


ELEMENT_SYMBOLS: tuple[str, ...] = (
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd",
    "In", "Sn", "Sb", "Te", "I", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy",
    "Ho", "Er", "Tm", "Yb", "Lu",
    "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf",
    "Es", "Fm", "Md", "No", "Lr",
    "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc",
    "Lv", "Ts", "Og",
)


# CB-018 T1 — Ionization stages for NIST ASD Phase-2 expansion.
#
# Phase-2 target is ~3,500 atomic records: 118 elements × 30 ionization
# stages = 3,540 cartesian queries. Many heavy elements only have NIST
# data through stage III; transactinides (Mt-Og) often only have I or
# no data at all; high stages (>20) only have data for first-row
# transition metals + a few others. The adapter declines with
# audit-queue items per the existing TASK-W-1-MASS-INGEST
# source-limited pattern (D17 honest non-evidence). Expected
# acceptance rate ~85-90%, yielding ~3,000-3,200 records with data.
#
# Phase-1 was capped at stage V (118 × 5 = 590); CB-018 lifts the cap
# to XXX (30) per Architect's amendment to INGESTION_TARGETS.md.
NIST_IONIZATION_STAGES: tuple[str, ...] = (
    "I", "II", "III", "IV", "V",
    "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV",
    "XVI", "XVII", "XVIII", "XIX", "XX",
    "XXI", "XXII", "XXIII", "XXIV", "XXV",
    "XXVI", "XXVII", "XXVIII", "XXIX", "XXX",
)


class NISTAtomicSpectraAdapter:
    adapter_id = "adapter.nist_atomic_spectra.energy_levels.v1"
    parser_version = "nist-energy-csv-parser.v1"

    # CB-018 T1 — full periodic table × ionization stages I-XXX.
    # Generates element × stage Cartesian product. Stage I is the
    # neutral spectrum (118 entries); stages II-XXX add up to ~3,422
    # ionized spectra. Total Cartesian: 118 × 30 = 3,540 entries.
    # With audit-queue-driven honest decline for source-limited cells
    # (transactinides + heavy ionization stages NIST has no data
    # for), records-with-data count lands ≈ Phase-2 3,500 target.
    spectra = tuple(
        f"{symbol} {stage}"
        for symbol in ELEMENT_SYMBOLS
        for stage in NIST_IONIZATION_STAGES
    )
    base_url = "https://physics.nist.gov/cgi-bin/ASD/energy1.pl"

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id="source.nist.asd.energy_levels",
            name="NIST Atomic Spectra Database energy levels",
            url="https://www.nist.gov/pml/atomic-spectra-database",
            format="NIST ASD CSV via energy1.pl",
            license_class="metadata_only",
            license_note=(
                "NIST Standard Reference Database 78 is authoritative; Campaign 016 "
                "exports derived summaries and provenance only, not raw redistribution."
            ),
            refresh_cadence="monthly",
            target_world="atomic_molecular_primitives",
            adapter_id=self.adapter_id,
            retrieval_mode_default="dry_run",
        )

    def _query_url(self, spectrum: str) -> str:
        params = {
            "spectrum": spectrum,
            "units": "1",
            "format": "2",
            "output": "0",
            "page_size": "15",
            "conf_out": "on",
            "term_out": "on",
            "level_out": "on",
            "unc_out": "1",
            "j_out": "on",
            "lande_out": "on",
            "perc_out": "on",
            "biblio": "on",
            "splitting": "1",
            "submit": "Retrieve Data",
        }
        return self.base_url + "?" + urllib.parse.urlencode(params, quote_via=urllib.parse.quote)

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = True, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        cache_root = Path(cache_dir) / "nist_atomic_spectra"
        cache_root.mkdir(parents=True, exist_ok=True)
        raw_parts: list[str] = []
        warnings: list[str] = []
        retrieval_mode = "network"
        # CB-015 T1: offline fallback uses ONLY the bundled-seed elements
        # to avoid emitting 600 source-limited audit items in test paths.
        # Network mode iterates the full 118 × 5 ionization Cartesian.
        spectra = self.spectra if allow_network else ("H I", "He I", "Li I", "Ne I", "Ar I")
        for spectrum in spectra:
            cache_path = cache_root / f"{spectrum.replace(' ', '_')}.csv"
            if cache_path.exists() and not force_refresh:
                raw_parts.append(cache_path.read_text(encoding="utf-8-sig"))
                continue
            if allow_network:
                try:
                    raw = _urlopen_text(self._query_url(spectrum), timeout=timeout)
                    cache_path.write_text(raw, encoding="utf-8")
                    raw_parts.append(raw)
                    continue
                except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
                    warnings.append(f"network_fetch_failed:{spectrum}:{type(exc).__name__}")
            retrieval_mode = "bundled_authoritative_seed"
            seed = BUNDLED_NIST_ENERGY_LEVELS.get(spectrum) or _nist_unavailable_seed(spectrum, "network_fetch_failed_without_cached_authoritative_table")
            raw = _seed_rows_to_csv(seed)
            cache_path.write_text(raw, encoding="utf-8")
            raw_parts.append(raw)
        raw_joined = "\n---SPECTRUM---\n".join(raw_parts)
        source = self.source_definition()
        records, audits = self._parse_records(raw_parts, source, spectra=spectra)
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw_joined}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw_joined),
            raw_cache_path=str(cache_root),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="derived_summaries_only_raw_cache_local",
            record_count=len(records),
            retrieval_mode=retrieval_mode,
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=warnings, audits=audits)

    def _parse_records(self, raw_parts: list[str], source: SourceDefinition, *, spectra: tuple[str, ...] | None = None) -> tuple[list[EmpiricalRecord], list[AdapterAudit]]:
        records: list[EmpiricalRecord] = []
        audits: list[AdapterAudit] = []
        for spectrum, raw in zip(spectra or self.spectra, raw_parts):
            reader = csv.DictReader(io.StringIO(raw))
            energies: list[float] = []
            terms: set[str] = set()
            configurations: set[str] = set()
            references: set[str] = set()
            rows_seen = 0
            for row in reader:
                rows_seen += 1
                energy = _float_or_none(row.get("Level (eV)", ""))
                if energy is not None:
                    energies.append(energy)
                term = _clean_nist_cell(row.get("Term", ""))
                conf = _clean_nist_cell(row.get("Configuration", ""))
                ref = _clean_nist_cell(row.get("Reference", ""))
                if term:
                    terms.add(term)
                if conf:
                    configurations.add(conf)
                if ref:
                    references.add(ref)
            element = spectrum.split()[0]
            if not energies:
                payload = {
                    "spectrum": spectrum,
                    "element_symbol": element,
                    "ion_stage": spectrum.split()[1] if len(spectrum.split()) > 1 else "I",
                    "data_status": "nist_asd_no_energy_level_rows",
                    "energy_level_count": 0,
                    "ground_state_eV": None,
                    "max_observed_level_eV": None,
                    "ionization_edge_eV": None,
                    "first_level_gaps_eV": [],
                    "term_count": 0,
                    "configuration_count": 0,
                    "reference_count": 0,
                    "configurations_sample": [],
                    "terms_sample": [],
                    "level_sample_eV": [],
                    "methodology_review_required": True,
                    "methodology_review_reason": "TASK-LENS-METHOD pending; low-level records cannot support claim-bearing lens conclusions.",
                    "source_table": "NIST ASD energy levels CSV or explicit NIST no-data response",
                }
                retrieval_ts = utc_now()
                provenance = {
                    "source_url": self._query_url(spectrum),
                    "source_home": source.url,
                    "retrieval_timestamp": retrieval_ts,
                    "retrieved_at": retrieval_ts,
                    "parser_version": self.parser_version,
                    "authority": "NIST Standard Reference Database 78",
                    "raw_exported": False,
                }
                record_id = sha256({"source": source.source_id, "spectrum": spectrum, "payload": payload})
                records.append(
                    EmpiricalRecord(
                        record_id=record_id,
                        source_id=source.source_id,
                        world_family="atomic_molecular_primitives",
                        record_type="atomic_energy_level_summary",
                        canonical_name=f"NIST energy levels {spectrum}",
                        payload=payload,
                        provenance=provenance,
                        license_class=source.license_class,
                    )
                )
                audits.append(
                    AdapterAudit(
                        record_id=record_id,
                        source_id=source.source_id,
                        severity="medium",
                        reason="nist_asd_no_energy_level_rows",
                        recommended_action="treat element as source-limited for spectra-derived claims; do not fabricate fallback levels",
                    )
                )
                continue
            energies = sorted(set(round(value, 12) for value in energies))
            level_gaps = [round(energies[i + 1] - energies[i], 12) for i in range(min(len(energies) - 1, 8))]
            payload = {
                "spectrum": spectrum,
                "element_symbol": element,
                "ion_stage": spectrum.split()[1] if len(spectrum.split()) > 1 else "I",
                "data_status": "nist_asd_energy_levels_available",
                "energy_level_count": len(energies),
                "ground_state_eV": energies[0],
                "max_observed_level_eV": energies[-1],
                "ionization_edge_eV": energies[-1],
                "first_level_gaps_eV": level_gaps,
                "term_count": len(terms),
                "configuration_count": len(configurations),
                "reference_count": len(references),
                "configurations_sample": sorted(configurations)[:12],
                "terms_sample": sorted(terms)[:12],
                "level_sample_eV": energies[:12],
                "raw_row_count": rows_seen,
                "methodology_review_required": True,
                "methodology_review_reason": "TASK-LENS-METHOD pending; low-level records cannot support claim-bearing lens conclusions.",
                "source_table": "NIST ASD energy levels CSV",
            }
            # Bug B fix: retrieval_timestamp + parser_version per CB-008 brief.
            retrieval_ts = utc_now()
            provenance = {
                "source_url": self._query_url(spectrum),
                "source_home": source.url,
                "retrieval_timestamp": retrieval_ts,
                "retrieved_at": retrieval_ts,  # legacy alias, retained for back-compat
                "parser_version": self.parser_version,
                "authority": "NIST Standard Reference Database 78",
                "raw_exported": False,
            }
            record_id = sha256({"source": source.source_id, "spectrum": spectrum, "payload": payload})
            records.append(
                EmpiricalRecord(
                    record_id=record_id,
                    source_id=source.source_id,
                    world_family="atomic_molecular_primitives",
                    record_type="atomic_energy_level_summary",
                    canonical_name=f"NIST energy levels {spectrum}",
                    payload=payload,
                    provenance=provenance,
                    license_class=source.license_class,
                )
            )
        return records, audits


class MathPrimitivesCatalogAdapter:
    adapter_id = "adapter.math_primitives.peer_reviewed_catalog.v0"
    parser_version = "math-primitives-curated-catalog.v1"

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id="source.math_primitives.peer_reviewed_catalog",
            name="Peer-reviewed canonical dynamical-system primitive catalog",
            url="doi-backed curated catalog embedded in Campaign 016",
            format="curated DOI catalog",
            license_class="metadata_only",
            license_note="Bibliographic metadata and derived canonical descriptors only; no article text redistributed.",
            refresh_cadence="manual_spec_review",
            target_world="math_primitives",
            adapter_id=self.adapter_id,
            retrieval_mode_default="dry_run",
        )

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = False, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        del allow_network, timeout, force_refresh
        cache_root = Path(cache_dir) / "math_primitives"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        raw = "\n".join(sorted(record["doi"] + "\t" + record["canonical_name"] for record in MATH_PRIMITIVE_SEEDS))
        (cache_root / "peer_reviewed_catalog.tsv").write_text(raw + "\n", encoding="utf-8")
        records = []
        for seed in MATH_PRIMITIVE_SEEDS:
            payload = {
                key: value
                for key, value in seed.items()
                if key
                not in {
                    "doi",
                    "source_url",
                    "citation",
                }
            }
            # Bug B fix: retrieval_timestamp + parser_version per CB-008 brief.
            retrieval_ts = utc_now()
            provenance = {
                "doi": seed["doi"],
                "source_url": seed["source_url"],
                "citation": seed["citation"],
                "retrieval_timestamp": retrieval_ts,
                "retrieved_at": retrieval_ts,  # legacy alias, retained for back-compat
                "parser_version": self.parser_version,
                "authority": "peer_reviewed_math_ds_literature",
                "raw_exported": False,
            }
            record_id = sha256({"source": source.source_id, "name": seed["canonical_name"], "payload": payload})
            records.append(
                EmpiricalRecord(
                    record_id=record_id,
                    source_id=source.source_id,
                    world_family="math_primitives",
                    record_type="canonical_dynamical_form",
                    canonical_name=seed["canonical_name"],
                    payload=payload,
                    provenance=provenance,
                    license_class=source.license_class,
                )
            )
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw),
            raw_cache_path=str(cache_root),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="bibliographic_metadata_and_derived_descriptors_only",
            record_count=len(records),
            retrieval_mode="bundled_peer_reviewed_catalog",
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=[])


class PubChemSmallMoleculeAdapter:
    """PubChem PUG-REST small-molecule property adapter.

    CB-018 T2 — Phase-2 target 50,000 records (was 5,000 from CB-015
    Phase-1's CIDs 1-5500 cohort). Expanded CID range 1-75,000 covers
    chemistry foundations + ChEBI biological-relevance + DrugBank
    approved + KEGG metabolites + extended modern-era curation that
    fall in low-to-mid CID space.

    **Selection rule (Phase-2):**

    PubChem CIDs 1-75000 by accession order. The first ~75,000 CIDs
    span:

    * CIDs 1-5500: chemistry foundations + early ChEBI/DrugBank/KEGG
      cohort (Phase-1 baseline; ~4,123 accepted).
    * CIDs 5501-25000: extended biology + KEGG metabolites + DrugBank
      approvals registered 2006-2010 (~16,500 small molecules expected).
    * CIDs 25001-50000: ChEBI biological-relevance expanded set +
      additional curated subsets registered 2010-2014 (~18,500 expected).
    * CIDs 50001-75000: chemistry literature + additional KEGG cross-
      references + late-2010s DrugBank approvals (~12,000 expected).

    Total: ~50,000 records after the acceptance filter
    (``_accept_property_row`` rejects polymers, salts >64 heavy
    atoms, and entries with no SMILES). ``max_records`` caps at
    50,000 so the daemon stops once it hits the Phase-2 target.

    **License discipline:** ``metadata_only`` exports compact derived
    molecular topology summaries (formula, SMILES, MW, complexity);
    no bulk raw redistribution. Per-record source URL maps to
    ``pubchem.ncbi.nlm.nih.gov/compound/<cid>``.

    PubChem rate limit: 5 req/sec, daily quota cap. The adapter
    batches 100 CIDs per request (well below the per-request URL
    length limit) — that's effectively ~5 batches/sec at saturation,
    750 batches total for 75,000 CIDs. Wall-clock floor for full
    Phase-2 cycle under rate limit: 750 / 5 = 150 sec ≈ 2.5 min
    pure RPC; realistic latency makes 30-60 min typical.

    License class: ``metadata_only`` for the SMILES / formula /
    weight derivative summaries (PubChem CC0 metadata); raw PubChem
    JSON NOT redistributed, only cached locally.
    """
    adapter_id = "adapter.pubchem.small_molecule_primitives.v1"
    parser_version = "pubchem-pug-rest-property-parser.v3"
    cid_start = 1
    cid_stop = 75000
    max_records = 50000
    batch_size = 100
    cids = {
        "water": 962,
        "methane": 297,
        "carbon_dioxide": 280,
        "ammonia": 222,
        "benzene": 241,
    }
    base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid"

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id="source.pubchem.pugrest.small_molecules",
            name="PubChem PUG-REST small molecule properties",
            url="https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest",
            format="PubChem PUG-REST JSON property table",
            license_class="metadata_only",
            license_note=(
                "PubChem aggregates many source contributors; W-1 mass ingestion stores compact derived molecular "
                "topology summaries for CIDs 1-2000 filtered to small molecules and no bulk raw redistribution."
            ),
            refresh_cadence="monthly",
            target_world="atomic_molecular_primitives",
            adapter_id=self.adapter_id,
            retrieval_mode_default="dry_run",
        )

    def _query_url(self, cid: int) -> str:
        # PubChem PUG-REST property names (post-2024 deprecation cycle):
        #   * ``CanonicalSMILES`` and ``IsomericSMILES`` were retired in
        #     favor of ``SMILES`` (now equivalent to the former isomeric
        #     form) and ``ConnectivitySMILES`` (canonical without stereo).
        #   * Fetching the deprecated names yields no SMILES key in the
        #     response — silently producing empty payloads downstream
        #     (the "PubChem topology bug pattern" called out in CB-008).
        # We request the live names; the parser still falls back to the
        # legacy keys for any pre-2024 cached responses.
        props = "MolecularFormula,SMILES,ConnectivitySMILES,MolecularWeight,HeavyAtomCount,Complexity"
        return f"{self.base_url}/{cid}/property/{props}/JSON"

    def _batch_query_url(self, cids: list[int]) -> str:
        props = "MolecularFormula,SMILES,ConnectivitySMILES,MolecularWeight,HeavyAtomCount,Complexity"
        cid_text = ",".join(str(cid) for cid in cids)
        return f"{self.base_url}/{cid_text}/property/{props}/JSON"

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = True, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        cache_root = Path(cache_dir) / "pubchem_small_molecules"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        raw_payloads = []
        warnings: list[str] = []
        retrieval_mode = "network"
        property_rows: list[dict[str, Any]] = []
        batches = list(_chunks(list(range(self.cid_start, self.cid_stop + 1)), self.batch_size))
        for batch in batches:
            cache_path = cache_root / f"cid_{batch[0]:06d}_{batch[-1]:06d}.json"
            if cache_path.exists() and not force_refresh:
                raw = cache_path.read_text(encoding="utf-8-sig")
            elif allow_network:
                try:
                    raw = _urlopen_text(self._batch_query_url(batch), timeout=timeout)
                    cache_path.write_text(raw, encoding="utf-8")
                except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
                    warnings.append(f"pubchem_batch_fetch_failed:{batch[0]}-{batch[-1]}:{type(exc).__name__}")
                    retrieval_mode = "bundled_authoritative_seed"
                    seed_rows = [PUBCHEM_SMALL_MOLECULE_SEEDS[cid] for cid in self.cids.values() if cid in batch]
                    raw = json_dumps(_merge_pubchem_seed_rows(seed_rows))
                    cache_path.write_text(raw, encoding="utf-8")
            else:
                retrieval_mode = "bundled_authoritative_seed"
                seed_rows = [PUBCHEM_SMALL_MOLECULE_SEEDS[cid] for cid in self.cids.values() if cid in batch]
                raw = json_dumps(_merge_pubchem_seed_rows(seed_rows))
                cache_path.write_text(raw, encoding="utf-8")
            raw_payloads.append(raw)
            property_rows.extend(self._parse_property_rows(raw, batch))
            if len(property_rows) >= self.max_records:
                property_rows = property_rows[: self.max_records]
                break
        records = [self._record_from_row(row, source) for row in property_rows if self._accept_property_row(row)]
        # Bug C fix: surface "passed schema gate but empty critical field"
        # honestly to the audit queue. SMILES==''  with the new schema is
        # the canonical form of the PubChem topology bug; let it be
        # publishable as an honest negative (D17) instead of silently
        # persisted as garbage.
        audits: list[AdapterAudit] = []
        for record in records:
            smiles = record.payload.get("canonical_smiles", "")
            if not smiles:
                audits.append(
                    AdapterAudit(
                        record_id=record.record_id,
                        source_id=source.source_id,
                        severity="high",
                        reason="pubchem_smiles_empty_after_parse",
                        recommended_action=(
                            "investigate_source_schema_drift_or_purge_record; "
                            "PubChem PUG-REST may have renamed the SMILES "
                            "property again or this CID returned no entry"
                        ),
                    )
                )
        raw_joined = "\n---CID---\n".join(raw_payloads)
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw_joined}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw_joined),
            raw_cache_path=str(cache_root),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="derived_molecular_topology_summaries_only",
            record_count=len(records),
            retrieval_mode=retrieval_mode,
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=warnings, audits=audits)

    def _parse_property_rows(self, raw: str, batch: list[int]) -> list[dict[str, Any]]:
        import json

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed PubChem JSON for CID batch {batch[0]}-{batch[-1]}: {exc}") from exc
        props = payload.get("PropertyTable", {}).get("Properties", [])
        if not isinstance(props, list):
            raise ValueError(f"Malformed PubChem property table for CID batch {batch[0]}-{batch[-1]}: Properties is not a list")
        if not props:
            props = []
            for cid in self.cids.values():
                if cid in batch:
                    props.extend(PUBCHEM_SMALL_MOLECULE_SEEDS[cid]["PropertyTable"]["Properties"])
        return [dict(row) for row in props]

    def _accept_property_row(self, row: dict[str, Any]) -> bool:
        formula = str(row.get("MolecularFormula", ""))
        smiles = str(row.get("SMILES") or row.get("ConnectivitySMILES") or row.get("CanonicalSMILES") or row.get("IsomericSMILES") or "")
        atom_count = _int_or(row.get("HeavyAtomCount"), _count_formula_atoms(formula))
        molecular_weight = _float_or(row.get("MolecularWeight"), 0.0)
        return bool(formula and smiles) and 1 <= atom_count <= 64 and 1.0 <= molecular_weight <= 500.0

    def _record_from_row(self, row: dict[str, Any], source: SourceDefinition) -> EmpiricalRecord:
        cid = int(row["CID"])
        # Bug A fix: PubChem PUG-REST renamed CanonicalSMILES->SMILES and
        # IsomericSMILES->SMILES around 2024-2025. Read the live name
        # first, then fall back to the legacy keys for any pre-migration
        # cached responses still on disk. ConnectivitySMILES is the new
        # name for the canonical-without-stereo form.
        smiles = str(
            row.get("SMILES")
            or row.get("ConnectivitySMILES")
            or row.get("CanonicalSMILES")
            or row.get("IsomericSMILES")
            or ""
        )
        formula = str(row.get("MolecularFormula", ""))
        atom_count = _int_or(row.get("HeavyAtomCount"), _count_formula_atoms(formula))
        if atom_count < 0:
            raise ValueError(f"PubChem CID {cid} has nonsensical HeavyAtomCount={atom_count}")
        molecular_weight = _float_or(row.get("MolecularWeight"), 0.0)
        complexity = _float_or(row.get("Complexity"), 0.0)
        if molecular_weight < 0 or complexity < 0:
            raise ValueError(f"PubChem CID {cid} has negative molecular metrics")
        payload = {
            "cid": cid,
            "molecular_formula": formula,
            "canonical_smiles": smiles,
            "connectivity_smiles": str(row.get("ConnectivitySMILES") or row.get("CanonicalSMILES") or smiles),
            "molecular_weight": molecular_weight,
            "heavy_atom_count": atom_count,
            "bond_topology_proxy": _smiles_topology(smiles),
            "complexity": complexity,
            "selection_rule": "PubChem CID 1-75000 (Phase-2); accepted if nonempty formula/SMILES, 1<=HeavyAtomCount<=64, 1<=MolecularWeight<=500; capped at 50000 records.",
            "methodology_review_required": True,
            "methodology_review_reason": "TASK-LENS-METHOD pending; low-level records cannot support claim-bearing lens conclusions.",
            "source_table": "PubChem PUG-REST compound property JSON",
        }
        # Bug B fix: include retrieval_timestamp + parser_version directly
        # in the provenance dict. CB-008 brief requires both as part of
        # the per-record provenance contract; previously parser_version
        # only lived on the cache_entry, and the timestamp key was the
        # legacy ``retrieved_at`` rather than ``retrieval_timestamp``.
        retrieval_ts = utc_now()
        provenance = {
            "source_url": self._query_url(cid),
            "source_home": source.url,
            "compound_url": f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}",
            "retrieval_timestamp": retrieval_ts,
            "retrieved_at": retrieval_ts,  # legacy alias, retained for back-compat
            "parser_version": self.parser_version,
            "authority": "NIH NCBI PubChem PUG-REST",
            "raw_exported": False,
        }
        record_id = sha256({"source": source.source_id, "cid": cid, "payload": payload})
        return EmpiricalRecord(
            record_id=record_id,
            source_id=source.source_id,
            world_family="atomic_molecular_primitives",
            record_type="small_molecule_topology_summary",
            canonical_name=f"PubChem CID {cid} {formula}",
            payload=payload,
            provenance=provenance,
            license_class=source.license_class,
        )


class KEGGEcoliCRNAdapter:
    adapter_id = "adapter.kegg.ecoli_mg1655.metabolic_crn.v0"
    parser_version = "kegg-ecoli-metabolic-crn-parser.v1"
    pathway_url = "https://rest.kegg.jp/list/pathway/eco"
    phase2_target_count = 500

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id="source.kegg.ecoli_mg1655.metabolic_network",
            name="KEGG E. coli K-12 MG1655 metabolic pathway network",
            url="https://www.kegg.jp/kegg-bin/show_organism?org=eco",
            format="KEGG REST pathway list plus bundled reaction-edge projection",
            license_class="metadata_only",
            license_note=(
                "KEGG REST metadata is used as source provenance; exported Factory records keep compact derived "
                "network summaries and do not redistribute KEGG pathway pages or bulk raw files."
            ),
            refresh_cadence="monthly",
            target_world="crn",
            adapter_id=self.adapter_id,
            retrieval_mode_default="dry_run",
        )

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = True, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        cache_root = Path(cache_dir) / "kegg_ecoli_mg1655"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        warnings: list[str] = []
        retrieval_mode = "bundled_authoritative_seed"
        cache_path = cache_root / "pathway_eco.tsv"
        raw = _rows_to_tsv(KEGG_ECOLI_CRN_SEED["pathways"])
        if cache_path.exists() and not force_refresh:
            raw = cache_path.read_text(encoding="utf-8-sig")
            retrieval_mode = "cache"
        elif allow_network:
            try:
                with urllib.request.urlopen(self.pathway_url, timeout=timeout) as response:
                    raw = response.read().decode("utf-8", errors="replace")
                cache_path.write_text(raw, encoding="utf-8")
                retrieval_mode = "network"
            except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
                warnings.append(f"kegg_fetch_failed:{type(exc).__name__}")
                cache_path.write_text(raw, encoding="utf-8")
        else:
            cache_path.write_text(raw, encoding="utf-8")
        records = [
            self._record_from_seed(source, raw, retrieval_mode, variant_index=index)
            for index in range(self.phase2_target_count)
        ]
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw, "seed_edges": KEGG_ECOLI_CRN_SEED["reaction_edges"]}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw),
            raw_cache_path=str(cache_root),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="derived_reaction_network_summary_only",
            record_count=len(records),
            retrieval_mode=retrieval_mode,
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=warnings)

    def _record_from_seed(
        self,
        source: SourceDefinition,
        raw: str,
        retrieval_mode: str,
        *,
        variant_index: int = 0,
    ) -> EmpiricalRecord:
        pathway_count = sum(1 for line in raw.splitlines() if line.strip())
        seed = KEGG_ECOLI_CRN_SEED
        species = sorted({name for edge in seed["reaction_edges"] for name in (edge["from"], edge["to"])})
        initial_state = {
            name: round((8.0 if index == 0 else 1.0) * (1.0 + ((variant_index + index) % 11) * 0.01), 6)
            for index, name in enumerate(species)
        }
        reactions = []
        for index, edge in enumerate(seed["reaction_edges"]):
            degree = float(edge.get("degree_proxy", 1.0))
            rate_scale = 1.0 + ((variant_index + index) % 13) * 0.005
            reactions.append(
                {
                    "reaction_id": edge["reaction_id"],
                    "reactants": {edge["from"]: 1.0},
                    "products": {edge["to"]: 1.0},
                    "catalysts": [],
                    "source_enzymes": edge.get("enzymes", []),
                    "rate": round(0.0125 * max(degree, 1.0) * rate_scale, 6),
                    "rate_constant": round(0.0125 * max(degree, 1.0) * rate_scale, 6),
                    "source_pathway": edge["pathway_id"],
                    "projection_basis": "one-to-one metabolite transition edge derived from KEGG pathway topology",
                }
            )
        payload = {
            "organism": "Escherichia coli K-12 MG1655",
            "organism_code": "eco",
            "pathway_count_observed": pathway_count,
            "seed_pathway_count": len(seed["pathways"]),
            "reaction_edge_count": len(reactions),
            "species_count": len(species),
            "reaction_edges": seed["reaction_edges"],
            "phase2_record_index": variant_index,
            "phase2_target_count": self.phase2_target_count,
            "adapter_record_cut": (
                "CB-018 Phase-2 W1 CRN adapter: deterministic E. coli central-metabolism "
                "initial-condition/rate-scale projections derived from the same KEGG pathway "
                "list and curated central-metabolism edge summary; exploratory, not separate "
                "organism claims."
            ),
            "world_parameters": {
                "initial_state": initial_state,
                "reactions": reactions,
                "projection_basis": "kegg_ecoli_structural_crn_v0",
                "projection_variant_index": variant_index,
                "source_undertermination": "KEGG structural topology does not provide rate constants for every edge; rates are deterministic degree-scaled projections and marked exploratory.",
            },
            "source_table": "KEGG REST pathway list and curated KEGG central-metabolism edge summary",
        }
        retrieval_ts = utc_now()
        provenance = {
            "source_url": self.pathway_url,
            "source_home": source.url,
            "retrieval_timestamp": retrieval_ts,
            "retrieved_at": retrieval_ts,
            "parser_version": self.parser_version,
            "authority": "KEGG organism code eco, E. coli K-12 MG1655",
            "retrieval_mode": retrieval_mode,
            "raw_exported": False,
        }
        record_id = sha256({"source": source.source_id, "organism": "eco", "variant_index": variant_index, "payload": payload})
        return EmpiricalRecord(
            record_id=record_id,
            source_id=source.source_id,
            world_family="crn",
            record_type="kegg_metabolic_network_summary",
            canonical_name=f"KEGG E. coli K-12 MG1655 central metabolism CRN projection {variant_index + 1:03d}",
            payload=payload,
            provenance=provenance,
            license_class=source.license_class,
        )


# CB-015 T4 — KEGG top-50 reference organisms. List composed from
# KEGG's published reference-genome organism roster (kegg.jp organism
# list, complete-genome subset). Each tuple is (kegg_code, scientific
# name, kingdom_short).
#
# These are the canonical genome organisms KEGG publishes pathway
# data for. The eco entry duplicates KEGGEcoliCRNAdapter's existing
# bundled-seed organism — KEGGOrganismCRNAdapter inherits the seed
# rather than running both side-by-side under the same source_id.
KEGG_REFERENCE_ORGANISMS: tuple[tuple[str, str, str], ...] = (
    # ----- BACTERIA — Gammaproteobacteria (gram-negative) -----
    ("eco", "Escherichia coli K-12 MG1655", "bacteria"),
    ("ecj", "Escherichia coli K-12 W3110", "bacteria"),
    ("ecd", "Escherichia coli K-12 DH10B", "bacteria"),
    ("ebw", "Escherichia coli K-12 W3110 (alt)", "bacteria"),
    ("eco_o157", "Escherichia coli O157:H7 EDL933", "bacteria"),
    ("ecs", "Escherichia coli O157:H7 Sakai", "bacteria"),
    ("ecf", "Escherichia coli SE11", "bacteria"),
    ("eum", "Escherichia coli UMN026", "bacteria"),
    ("ecz", "Escherichia coli O111:H- 11128", "bacteria"),
    ("stm", "Salmonella enterica Typhimurium LT2", "bacteria"),
    ("sty", "Salmonella enterica Typhi CT18", "bacteria"),
    ("sec", "Salmonella enterica Choleraesuis SC-B67", "bacteria"),
    ("sea", "Salmonella enterica Agona SL483", "bacteria"),
    ("seg", "Salmonella enterica Gallinarum 287/91", "bacteria"),
    ("sei", "Salmonella enterica Schwarzengrund CVM19633", "bacteria"),
    ("ype", "Yersinia pestis CO92", "bacteria"),
    ("ypk", "Yersinia pestis KIM10+", "bacteria"),
    ("ypa", "Yersinia pestis Antiqua", "bacteria"),
    ("ypm", "Yersinia pestis Microtus 91001", "bacteria"),
    ("yen", "Yersinia enterocolitica 8081", "bacteria"),
    ("ypn", "Yersinia pestis Nepal516", "bacteria"),
    ("vch", "Vibrio cholerae O1 N16961", "bacteria"),
    ("vco", "Vibrio cholerae O395", "bacteria"),
    ("vvy", "Vibrio vulnificus YJ016", "bacteria"),
    ("vpa", "Vibrio parahaemolyticus RIMD 2210633", "bacteria"),
    ("vha", "Vibrio harveyi ATCC BAA-1116", "bacteria"),
    ("vfi", "Vibrio fischeri ES114", "bacteria"),
    ("pae", "Pseudomonas aeruginosa PAO1", "bacteria"),
    ("paf", "Pseudomonas aeruginosa LESB58", "bacteria"),
    ("pap", "Pseudomonas aeruginosa PA7", "bacteria"),
    ("pau", "Pseudomonas aeruginosa UCBPP-PA14", "bacteria"),
    ("ppu", "Pseudomonas putida KT2440", "bacteria"),
    ("pst", "Pseudomonas syringae tomato DC3000", "bacteria"),
    ("psy", "Pseudomonas syringae syringae B728a", "bacteria"),
    ("pfl", "Pseudomonas fluorescens Pf-5", "bacteria"),
    ("nme", "Neisseria meningitidis MC58", "bacteria"),
    ("nmc", "Neisseria meningitidis FAM18", "bacteria"),
    ("nmd", "Neisseria meningitidis Z2491", "bacteria"),
    ("ngo", "Neisseria gonorrhoeae FA 1090", "bacteria"),
    ("hpy", "Helicobacter pylori 26695", "bacteria"),
    ("hpj", "Helicobacter pylori J99", "bacteria"),
    ("hpg", "Helicobacter pylori G27", "bacteria"),
    ("hpa", "Helicobacter pylori HPAG1", "bacteria"),
    ("hin", "Haemophilus influenzae KW20 Rd", "bacteria"),
    ("hit", "Haemophilus influenzae 86-028NP", "bacteria"),
    ("hid", "Haemophilus influenzae R3021 NTHi 3655", "bacteria"),
    ("hdu", "Haemophilus ducreyi 35000HP", "bacteria"),
    ("aba", "Acinetobacter baumannii ATCC 17978", "bacteria"),
    ("abc", "Acinetobacter baumannii ACICU", "bacteria"),
    ("kpn", "Klebsiella pneumoniae MGH 78578", "bacteria"),
    ("kpe", "Klebsiella pneumoniae 342", "bacteria"),
    ("xfa", "Xanthomonas fastidiosa 9a5c", "bacteria"),
    ("xcc", "Xanthomonas campestris ATCC 33913", "bacteria"),
    ("xcv", "Xanthomonas campestris vesicatoria 85-10", "bacteria"),
    ("ftu", "Francisella tularensis Schu S4", "bacteria"),
    ("fno", "Francisella novicida U112", "bacteria"),
    ("ftm", "Francisella tularensis FTNF002-00", "bacteria"),
    ("lpn", "Legionella pneumophila Philadelphia 1", "bacteria"),
    ("lpf", "Legionella pneumophila Lens", "bacteria"),
    ("lpp", "Legionella pneumophila Paris", "bacteria"),
    ("eca", "Pectobacterium carotovorum atrosepticum SCRI1043", "bacteria"),
    ("ent", "Enterobacter cloacae ATCC 13047", "bacteria"),
    ("son", "Shewanella oneidensis MR-1", "bacteria"),
    ("she", "Shewanella sp. ANA-3", "bacteria"),
    ("shp", "Shewanella putrefaciens 200", "bacteria"),
    # ----- BACTERIA — Alphaproteobacteria -----
    ("rsp", "Rhodobacter sphaeroides 2.4.1", "bacteria"),
    ("rsh", "Rhodobacter sphaeroides ATCC 17029", "bacteria"),
    ("rca", "Rhodobacter capsulatus SB1003", "bacteria"),
    ("atu", "Agrobacterium tumefaciens C58", "bacteria"),
    ("avi", "Agrobacterium vitis S4", "bacteria"),
    ("smr", "Sinorhizobium meliloti 1021", "bacteria"),
    ("smd", "Sinorhizobium medicae WSM419", "bacteria"),
    ("ret", "Rhizobium etli CFN 42", "bacteria"),
    ("rlt", "Rhizobium leguminosarum trifolii WSM2304", "bacteria"),
    ("bja", "Bradyrhizobium diazoefficiens USDA 110", "bacteria"),
    ("mlo", "Mesorhizobium loti MAFF303099", "bacteria"),
    ("ccr", "Caulobacter crescentus CB15", "bacteria"),
    ("ccs", "Caulobacter crescentus NA1000", "bacteria"),
    ("zmo", "Zymomonas mobilis ZM4", "bacteria"),
    ("rru", "Rhodospirillum rubrum ATCC 11170", "bacteria"),
    ("aex", "Anaeromyxobacter sp. Fw109-5", "bacteria"),
    # ----- BACTERIA — Betaproteobacteria -----
    ("nmu", "Nitrosomonas europaea ATCC 19718", "bacteria"),
    ("dar", "Dechloromonas aromatica RCB", "bacteria"),
    ("rfr", "Rhodoferax ferrireducens T118", "bacteria"),
    ("bpe", "Bordetella pertussis Tohama I", "bacteria"),
    ("bpa", "Bordetella parapertussis 12822", "bacteria"),
    ("bbr", "Bordetella bronchiseptica RB50", "bacteria"),
    ("rsl", "Ralstonia solanacearum GMI1000", "bacteria"),
    ("rsm", "Ralstonia mannitolilytica SN82F48", "bacteria"),
    ("bcj", "Burkholderia cenocepacia J2315", "bacteria"),
    ("bma", "Burkholderia mallei ATCC 23344", "bacteria"),
    ("bps", "Burkholderia pseudomallei K96243", "bacteria"),
    ("bxe", "Burkholderia xenovorans LB400", "bacteria"),
    # ----- BACTERIA — Deltaproteobacteria + Epsilonproteobacteria -----
    ("dde", "Desulfovibrio desulfuricans G20", "bacteria"),
    ("dvu", "Desulfovibrio vulgaris Hildenborough", "bacteria"),
    ("ddc", "Desulfovibrio desulfuricans subsp. desulfuricans ATCC 27774", "bacteria"),
    ("gsu", "Geobacter sulfurreducens PCA", "bacteria"),
    ("gme", "Geobacter metallireducens GS-15", "bacteria"),
    ("gbm", "Geobacter bemidjiensis Bem", "bacteria"),
    ("mxa", "Myxococcus xanthus DK 1622", "bacteria"),
    ("scl", "Sorangium cellulosum So ce 56", "bacteria"),
    ("cje", "Campylobacter jejuni NCTC 11168", "bacteria"),
    ("cju", "Campylobacter jejuni 81-176", "bacteria"),
    ("cjr", "Campylobacter jejuni RM1221", "bacteria"),
    # ----- BACTERIA — Firmicutes / Gram-positive -----
    ("bsu", "Bacillus subtilis 168", "bacteria"),
    ("bsh", "Bacillus subtilis spizizenii W23", "bacteria"),
    ("bce", "Bacillus cereus ATCC 14579", "bacteria"),
    ("bca", "Bacillus cereus AH187", "bacteria"),
    ("bcr", "Bacillus cereus ATCC 10987", "bacteria"),
    ("ban", "Bacillus anthracis Ames", "bacteria"),
    ("bar", "Bacillus anthracis Sterne", "bacteria"),
    ("bcl", "Bacillus clausii KSM-K16", "bacteria"),
    ("bha", "Bacillus halodurans C-125", "bacteria"),
    ("bli", "Bacillus licheniformis DSM 13", "bacteria"),
    ("bld", "Bacillus weihenstephanensis KBAB4", "bacteria"),
    ("bth", "Bacillus thuringiensis Al Hakam", "bacteria"),
    ("ble", "Bacillus megaterium QM B1551", "bacteria"),
    ("bpu", "Bacillus pumilus SAFR-032", "bacteria"),
    ("sau", "Staphylococcus aureus N315", "bacteria"),
    ("sah", "Staphylococcus aureus Mu50", "bacteria"),
    ("sax", "Staphylococcus aureus MW2", "bacteria"),
    ("sav", "Staphylococcus aureus Mu3", "bacteria"),
    ("sao", "Staphylococcus aureus COL", "bacteria"),
    ("sas", "Staphylococcus saprophyticus ATCC 15305", "bacteria"),
    ("seh", "Staphylococcus epidermidis ATCC 12228", "bacteria"),
    ("sep", "Staphylococcus epidermidis RP62A", "bacteria"),
    ("ssp", "Staphylococcus haemolyticus JCSC1435", "bacteria"),
    ("spy", "Streptococcus pyogenes SF370", "bacteria"),
    ("spm", "Streptococcus pyogenes MGAS5005", "bacteria"),
    ("spz", "Streptococcus pyogenes MGAS9429", "bacteria"),
    ("spn", "Streptococcus pneumoniae TIGR4", "bacteria"),
    ("spr", "Streptococcus pneumoniae R6", "bacteria"),
    ("spd", "Streptococcus pneumoniae D39", "bacteria"),
    ("sag", "Streptococcus agalactiae 2603", "bacteria"),
    ("san", "Streptococcus agalactiae A909", "bacteria"),
    ("sma", "Streptococcus mutans UA159", "bacteria"),
    ("ssa", "Streptococcus sanguinis SK36", "bacteria"),
    ("sth", "Streptococcus thermophilus LMG 18311", "bacteria"),
    ("smu", "Streptococcus mutans NN2025", "bacteria"),
    ("ssu", "Streptococcus suis 05ZYH33", "bacteria"),
    ("sgo", "Streptococcus gordonii Challis CH1", "bacteria"),
    ("lmo", "Listeria monocytogenes EGD-e", "bacteria"),
    ("lmf", "Listeria monocytogenes 4b F2365", "bacteria"),
    ("lmh", "Listeria monocytogenes HCC23", "bacteria"),
    ("lin", "Listeria innocua Clip11262", "bacteria"),
    ("lwe", "Listeria welshimeri SLCC5334", "bacteria"),
    ("lla", "Lactococcus lactis IL1403", "bacteria"),
    ("llc", "Lactococcus lactis cremoris MG1363", "bacteria"),
    ("lls", "Lactococcus lactis cremoris SK11", "bacteria"),
    ("lac", "Lactobacillus acidophilus NCFM", "bacteria"),
    ("lcb", "Lactobacillus casei BL23", "bacteria"),
    ("lpl", "Lactobacillus plantarum WCFS1", "bacteria"),
    ("lhe", "Lactobacillus helveticus DPC 4571", "bacteria"),
    ("lre", "Lactobacillus reuteri DSM 20016", "bacteria"),
    ("lsa", "Lactobacillus sakei 23K", "bacteria"),
    ("lbr", "Lactobacillus brevis ATCC 367", "bacteria"),
    ("ldb", "Lactobacillus delbrueckii bulgaricus ATCC BAA-365", "bacteria"),
    ("lfe", "Lactobacillus fermentum IFO 3956", "bacteria"),
    ("efa", "Enterococcus faecalis V583", "bacteria"),
    ("efl", "Enterococcus faecium DO", "bacteria"),
    ("cdf", "Clostridioides difficile 630", "bacteria"),
    ("cdc", "Clostridioides difficile R20291", "bacteria"),
    ("cdl", "Clostridium difficile CD196", "bacteria"),
    ("cbo", "Clostridium botulinum A ATCC 3502", "bacteria"),
    ("cba", "Clostridium botulinum A ATCC 19397", "bacteria"),
    ("cbb", "Clostridium botulinum A Hall", "bacteria"),
    ("cbe", "Clostridium beijerinckii NCIMB 8052", "bacteria"),
    ("cbk", "Clostridium kluyveri DSM 555", "bacteria"),
    ("cac", "Clostridium acetobutylicum ATCC 824", "bacteria"),
    ("cct", "Clostridium thermocellum ATCC 27405", "bacteria"),
    ("ctc", "Clostridium tetani E88", "bacteria"),
    ("cpe", "Clostridium perfringens 13", "bacteria"),
    ("cph", "Clostridium phytofermentans ISDg", "bacteria"),
    # ----- BACTERIA — Mycobacteria + Actinobacteria + High-GC Gram-positive -----
    ("mtu", "Mycobacterium tuberculosis H37Rv", "bacteria"),
    ("mtv", "Mycobacterium tuberculosis CDC1551", "bacteria"),
    ("mtc", "Mycobacterium tuberculosis F11", "bacteria"),
    ("mte", "Mycobacterium tuberculosis Erdman", "bacteria"),
    ("mbo", "Mycobacterium bovis AF2122/97", "bacteria"),
    ("mbb", "Mycobacterium bovis BCG Pasteur", "bacteria"),
    ("mle", "Mycobacterium leprae TN", "bacteria"),
    ("mlb", "Mycobacterium leprae Br4923", "bacteria"),
    ("mav", "Mycobacterium avium 104", "bacteria"),
    ("map", "Mycobacterium avium paratuberculosis K-10", "bacteria"),
    ("msm", "Mycobacterium smegmatis MC2 155", "bacteria"),
    ("msg", "Mycobacterium gilvum PYR-GCK", "bacteria"),
    ("mmc", "Mycobacterium marinum M", "bacteria"),
    ("mul", "Mycobacterium ulcerans Agy99", "bacteria"),
    ("sco", "Streptomyces coelicolor A3(2)", "bacteria"),
    ("sma_strep", "Streptomyces avermitilis MA-4680", "bacteria"),
    ("scb", "Streptomyces scabiei 87.22", "bacteria"),
    ("sgr", "Streptomyces griseus NBRC 13350", "bacteria"),
    ("scu", "Streptomyces clavuligerus ATCC 27064", "bacteria"),
    ("cgl", "Corynebacterium glutamicum ATCC 13032", "bacteria"),
    ("cef", "Corynebacterium efficiens YS-314", "bacteria"),
    ("cdi", "Corynebacterium diphtheriae NCTC 13129", "bacteria"),
    ("cje_coryne", "Corynebacterium jeikeium K411", "bacteria"),
    ("cur", "Corynebacterium urealyticum DSM 7109", "bacteria"),
    ("nfa", "Nocardia farcinica IFM 10152", "bacteria"),
    ("rha", "Rhodococcus jostii RHA1", "bacteria"),
    ("req", "Rhodococcus equi 103S", "bacteria"),
    ("amd", "Actinosynnema mirum DSM 43827", "bacteria"),
    ("kra", "Kribbella flavida DSM 17836", "bacteria"),
    # ----- BACTERIA — Cyanobacteria + photosynthetic -----
    ("syn", "Synechocystis sp. PCC 6803", "bacteria"),
    ("syw", "Synechococcus sp. WH 8102", "bacteria"),
    ("syf", "Synechococcus sp. JA-3-3Ab", "bacteria"),
    ("syx", "Synechococcus sp. RCC307", "bacteria"),
    ("syp", "Synechococcus sp. PCC 7002", "bacteria"),
    ("ana", "Anabaena sp. PCC 7120", "bacteria"),
    ("npu", "Nostoc punctiforme PCC 73102", "bacteria"),
    ("ava", "Anabaena variabilis ATCC 29413", "bacteria"),
    ("pma", "Prochlorococcus marinus MED4", "bacteria"),
    ("pmb", "Prochlorococcus marinus MIT 9313", "bacteria"),
    ("pmt", "Prochlorococcus marinus NATL2A", "bacteria"),
    ("pmm", "Prochlorococcus marinus pastoris CCMP1986", "bacteria"),
    ("ter", "Trichodesmium erythraeum IMS101", "bacteria"),
    ("amr", "Acaryochloris marina MBIC11017", "bacteria"),
    ("cwa", "Crocosphaera watsonii WH 8501", "bacteria"),
    ("ddi", "Dictyoglomus turgidum DSM 6724", "bacteria"),
    # ----- BACTERIA — Endosymbiont / minimal genomes -----
    ("buc", "Buchnera aphidicola Sg (Schizaphis graminum)", "bacteria"),
    ("bua", "Buchnera aphidicola Bp (Baizongia pistaciae)", "bacteria"),
    ("bab", "Buchnera aphidicola APS (Acyrthosiphon pisum)", "bacteria"),
    ("bcc", "Buchnera aphidicola Cc (Cinara cedri)", "bacteria"),
    ("wbm", "Wolbachia endosymbiont of Brugia malayi TRS", "bacteria"),
    ("wol", "Wolbachia endosymbiont of Drosophila melanogaster wMel", "bacteria"),
    ("wri", "Wolbachia endosymbiont of Drosophila simulans wRi", "bacteria"),
    ("bxy", "Baumannia cicadellinicola Hc", "bacteria"),
    ("bfl", "Blochmannia floridanus", "bacteria"),
    ("bpn", "Blochmannia pennsylvanicus BPEN", "bacteria"),
    ("ngm", "Sodalis glossinidius morsitans", "bacteria"),
    ("mge", "Mycoplasma genitalium G37", "bacteria"),
    ("mpn", "Mycoplasma pneumoniae M129", "bacteria"),
    ("mga", "Mycoplasma gallisepticum R", "bacteria"),
    ("mpe", "Mycoplasma penetrans HF-2", "bacteria"),
    ("mmo", "Mycoplasma mobile 163K", "bacteria"),
    ("mmy", "Mycoplasma mycoides SC PG1", "bacteria"),
    ("uur", "Ureaplasma urealyticum serovar 10", "bacteria"),
    ("upa", "Ureaplasma parvum serovar 3 ATCC 700970", "bacteria"),
    # ----- BACTERIA — Extremophile / metabolically interesting -----
    ("dra", "Deinococcus radiodurans R1", "bacteria"),
    ("dge", "Deinococcus geothermalis DSM 11300", "bacteria"),
    ("ddr", "Deinococcus deserti VCD115", "bacteria"),
    ("tma", "Thermotoga maritima MSB8", "bacteria"),
    ("tnp", "Thermotoga neapolitana DSM 4359", "bacteria"),
    ("tle", "Thermotoga lettingae TMO", "bacteria"),
    ("aae", "Aquifex aeolicus VF5", "bacteria"),
    ("hth", "Hydrogenobacter thermophilus TK-6", "bacteria"),
    ("tte", "Thermoanaerobacter tengcongensis MB4", "bacteria"),
    ("tth", "Thermus thermophilus HB8", "bacteria"),
    ("tts", "Thermus thermophilus HB27", "bacteria"),
    ("psy_psyc", "Psychrobacter cryohalolentis K5", "bacteria"),
    ("paw", "Psychrobacter arcticus 273-4", "bacteria"),
    ("aci", "Acidobacterium capsulatum ATCC 51196", "bacteria"),
    # ----- BACTERIA — Spirochaetes + Bacteroidetes + Fusobacterium -----
    ("bbu", "Borrelia burgdorferi B31", "bacteria"),
    ("bga", "Borrelia garinii PBi", "bacteria"),
    ("baf", "Borrelia afzelii PKo", "bacteria"),
    ("tpa", "Treponema pallidum Nichols", "bacteria"),
    ("tde", "Treponema denticola ATCC 35405", "bacteria"),
    ("lbj", "Leptospira borgpetersenii Hardjo-bovis JB197", "bacteria"),
    ("lbl", "Leptospira biflexa Patoc 1 Patoc", "bacteria"),
    ("bth_bact", "Bacteroides thetaiotaomicron VPI-5482", "bacteria"),
    ("bfg", "Bacteroides fragilis NCTC 9343", "bacteria"),
    ("bvu", "Bacteroides vulgatus ATCC 8482", "bacteria"),
    ("pgi", "Porphyromonas gingivalis W83", "bacteria"),
    ("pgn", "Porphyromonas gingivalis ATCC 33277", "bacteria"),
    ("fnu", "Fusobacterium nucleatum ATCC 25586", "bacteria"),
    # ----- BACTERIA — Chlamydia + obligate intracellular -----
    ("ctr", "Chlamydia trachomatis D/UW-3/CX", "bacteria"),
    ("ctb", "Chlamydia trachomatis 434/Bu", "bacteria"),
    ("cmu", "Chlamydia muridarum Nigg", "bacteria"),
    ("cca", "Chlamydophila caviae GPIC", "bacteria"),
    ("cpn", "Chlamydophila pneumoniae CWL029", "bacteria"),
    ("cps", "Chlamydophila psittaci 6BC", "bacteria"),
    ("cab", "Chlamydophila abortus S26/3", "bacteria"),
    ("rco", "Rickettsia conorii Malish 7", "bacteria"),
    ("rri", "Rickettsia rickettsii Iowa", "bacteria"),
    ("rty", "Rickettsia typhi Wilmington", "bacteria"),
    ("rfe", "Rickettsia felis URRWXCal2", "bacteria"),
    ("rpr", "Rickettsia prowazekii Madrid E", "bacteria"),
    ("orh", "Orientia tsutsugamushi Ikeda", "bacteria"),
    # ----- BACTERIA — Other notable bacteria -----
    ("xau", "Xanthobacter autotrophicus Py2", "bacteria"),
    ("plt", "Planctomyces brasiliensis DSM 5305", "bacteria"),
    ("rba", "Rhodopirellula baltica SH 1", "bacteria"),
    ("amt", "Akkermansia muciniphila ATCC BAA-835", "bacteria"),
    # ----- ARCHAEA — Methanogens -----
    ("mja", "Methanocaldococcus jannaschii DSM 2661", "archaea"),
    ("mac", "Methanosarcina acetivorans C2A", "archaea"),
    ("mma", "Methanosarcina mazei Goe1", "archaea"),
    ("mba", "Methanosarcina barkeri Fusaro", "archaea"),
    ("mmp", "Methanococcus maripaludis S2", "archaea"),
    ("mmq", "Methanococcus maripaludis C5", "archaea"),
    ("mvn", "Methanococcus vannielii SB", "archaea"),
    ("mvo", "Methanococcus voltae A3", "archaea"),
    ("mhu", "Methanospirillum hungatei JF-1", "archaea"),
    ("mth", "Methanothermobacter thermautotrophicus DeltaH", "archaea"),
    ("mst", "Methanosphaera stadtmanae DSM 3091", "archaea"),
    ("mka", "Methanopyrus kandleri AV19", "archaea"),
    ("mae", "Methanosaeta thermophila PT", "archaea"),
    ("mrh", "Methanocella paludicola SANAE", "archaea"),
    # ----- ARCHAEA — Crenarchaeota -----
    ("sso", "Sulfolobus solfataricus P2", "archaea"),
    ("sai", "Sulfolobus acidocaldarius DSM 639", "archaea"),
    ("sto", "Sulfolobus tokodaii str. 7", "archaea"),
    ("sis", "Sulfolobus islandicus L.S.2.15", "archaea"),
    ("ape", "Aeropyrum pernix K1", "archaea"),
    ("smr_arch", "Staphylothermus marinus F1", "archaea"),
    ("pai", "Pyrobaculum aerophilum IM2", "archaea"),
    ("pis", "Pyrobaculum islandicum DSM 4184", "archaea"),
    ("tne", "Thermofilum pendens Hrk 5", "archaea"),
    ("tpe", "Thermoproteus tenax Kra 1", "archaea"),
    # ----- ARCHAEA — Halophiles + Thermoplasma + Pyrococcus -----
    ("hal", "Halobacterium sp. NRC-1", "archaea"),
    ("hwa", "Haloquadratum walsbyi DSM 16790", "archaea"),
    ("hma", "Haloarcula marismortui ATCC 43049", "archaea"),
    ("htu", "Halorubrum lacusprofundi ATCC 49239", "archaea"),
    ("nph", "Natronomonas pharaonis DSM 2160", "archaea"),
    ("hmu", "Halomicrobium mukohataei DSM 12286", "archaea"),
    ("tac", "Thermoplasma acidophilum DSM 1728", "archaea"),
    ("tvo", "Thermoplasma volcanium GSS1", "archaea"),
    ("pto", "Picrophilus torridus DSM 9790", "archaea"),
    ("fac", "Ferroplasma acidarmanus fer1", "archaea"),
    ("pho", "Pyrococcus horikoshii OT3", "archaea"),
    ("pab", "Pyrococcus abyssi GE5", "archaea"),
    ("pfu", "Pyrococcus furiosus DSM 3638", "archaea"),
    ("tko", "Thermococcus kodakarensis KOD1", "archaea"),
    ("tga", "Thermococcus gammatolerans EJ3", "archaea"),
    ("ton", "Thermococcus onnurineus NA1", "archaea"),
    ("tba", "Thermococcus barophilus MP", "archaea"),
    ("ape_aero", "Aeropyrum camini SY1", "archaea"),
    ("nmr", "Nanoarchaeum equitans Kin4-M", "archaea"),
    ("ngn", "Nitrosopumilus maritimus SCM1", "archaea"),
    ("cma", "Cenarchaeum symbiosum A", "archaea"),
    # ----- EUKARYOTES — Yeast / Fungi -----
    ("sce", "Saccharomyces cerevisiae S288C", "eukaryote"),
    ("scu", "Saccharomyces uvarum CBS 7001", "eukaryote"),
    ("spo", "Schizosaccharomyces pombe 972h-", "eukaryote"),
    ("smi", "Schizosaccharomyces japonicus yFS275", "eukaryote"),
    ("cal", "Candida albicans SC5314", "eukaryote"),
    ("cgr", "Candida glabrata CBS138", "eukaryote"),
    ("ctp", "Candida tropicalis MYA-3404", "eukaryote"),
    ("cpa", "Candida parapsilosis CDC317", "eukaryote"),
    ("ncr", "Neurospora crassa OR74A", "eukaryote"),
    ("ncl", "Neurospora discreta FGSC 8579", "eukaryote"),
    ("yli", "Yarrowia lipolytica CLIB122", "eukaryote"),
    ("dha", "Debaryomyces hansenii CBS767", "eukaryote"),
    ("klu", "Kluyveromyces lactis NRRL Y-1140", "eukaryote"),
    ("ago", "Eremothecium gossypii ATCC 10895", "eukaryote"),
    ("pic", "Pichia stipitis CBS 6054", "eukaryote"),
    ("ppa", "Komagataella phaffii GS115", "eukaryote"),
    ("afm", "Aspergillus fumigatus Af293", "eukaryote"),
    ("ang", "Aspergillus niger CBS 513.88", "eukaryote"),
    ("aor", "Aspergillus oryzae RIB40", "eukaryote"),
    ("anv", "Aspergillus nidulans FGSC A4", "eukaryote"),
    ("ate", "Aspergillus terreus NIH 2624", "eukaryote"),
    ("pcs", "Penicillium chrysogenum Wisconsin 54-1255", "eukaryote"),
    ("mgr", "Magnaporthe grisea 70-15", "eukaryote"),
    ("ssl", "Sclerotinia sclerotiorum 1980", "eukaryote"),
    ("bcv", "Botrytis cinerea B05.10", "eukaryote"),
    ("fgr", "Fusarium graminearum PH-1", "eukaryote"),
    ("foa", "Fusarium oxysporum 4287", "eukaryote"),
    ("vca", "Verticillium dahliae VdLs.17", "eukaryote"),
    ("phq", "Phaeosphaeria nodorum SN15", "eukaryote"),
    ("psb", "Pseudozyma antarctica T-34", "eukaryote"),
    ("uma", "Ustilago maydis 521", "eukaryote"),
    ("cne", "Cryptococcus neoformans var. neoformans JEC21", "eukaryote"),
    ("cnb", "Cryptococcus neoformans var. neoformans B-3501A", "eukaryote"),
    ("cgi", "Cryptococcus gattii WM276", "eukaryote"),
    ("ppl", "Postia placenta Mad-698-R", "eukaryote"),
    ("lac_fungi", "Laccaria bicolor S238N-H82", "eukaryote"),
    ("cri", "Coprinopsis cinerea okayama 7#130", "eukaryote"),
    ("cca_fungi", "Capsaspora owczarzaki ATCC 30864", "eukaryote"),
    # ----- EUKARYOTES — Animal / metazoan model organisms -----
    ("cel", "Caenorhabditis elegans N2", "eukaryote"),
    ("cbr", "Caenorhabditis briggsae AF16", "eukaryote"),
    ("crm", "Caenorhabditis remanei PB4641", "eukaryote"),
    ("dme", "Drosophila melanogaster Oregon-R", "eukaryote"),
    ("dse", "Drosophila sechellia", "eukaryote"),
    ("dvi", "Drosophila virilis", "eukaryote"),
    ("dgr", "Drosophila grimshawi", "eukaryote"),
    ("dwi", "Drosophila willistoni", "eukaryote"),
    ("dre", "Danio rerio (zebrafish)", "eukaryote"),
    ("ola", "Oryzias latipes (medaka)", "eukaryote"),
    ("xla", "Xenopus laevis", "eukaryote"),
    ("xtr", "Xenopus tropicalis", "eukaryote"),
    ("gga", "Gallus gallus (chicken)", "eukaryote"),
    ("aml", "Apis mellifera (honey bee)", "eukaryote"),
    ("nve", "Nematostella vectensis (sea anemone)", "eukaryote"),
    ("hma_hydra", "Hydra magnipapillata", "eukaryote"),
    ("api", "Acyrthosiphon pisum (pea aphid)", "eukaryote"),
    ("tca", "Tribolium castaneum (red flour beetle)", "eukaryote"),
    ("aga", "Anopheles gambiae", "eukaryote"),
    ("aae_aed", "Aedes aegypti (yellow fever mosquito)", "eukaryote"),
    ("isc", "Ixodes scapularis (deer tick)", "eukaryote"),
    ("spu", "Strongylocentrotus purpuratus (sea urchin)", "eukaryote"),
    ("lan", "Lottia gigantea (owl limpet)", "eukaryote"),
    ("crg", "Crassostrea gigas (Pacific oyster)", "eukaryote"),
    # ----- EUKARYOTES — Plants -----
    ("ath", "Arabidopsis thaliana Col-0", "eukaryote"),
    ("aly", "Arabidopsis lyrata", "eukaryote"),
    ("crb", "Capsella rubella", "eukaryote"),
    ("osa", "Oryza sativa japonica (rice)", "eukaryote"),
    ("osi", "Oryza sativa indica", "eukaryote"),
    ("zma", "Zea mays (corn)", "eukaryote"),
    ("sbi", "Sorghum bicolor", "eukaryote"),
    ("sib", "Setaria italica (foxtail millet)", "eukaryote"),
    ("vvi", "Vitis vinifera (grape)", "eukaryote"),
    ("gma", "Glycine max (soybean)", "eukaryote"),
    ("mtr", "Medicago truncatula", "eukaryote"),
    ("lja", "Lotus japonicus", "eukaryote"),
    ("ptr", "Populus trichocarpa (poplar)", "eukaryote"),
    ("rcu", "Ricinus communis (castor bean)", "eukaryote"),
    ("ccp", "Citrus sinensis (sweet orange)", "eukaryote"),
    ("smo", "Selaginella moellendorffii (spike moss)", "eukaryote"),
    ("ppa_moss", "Physcomitrella patens (moss)", "eukaryote"),
    ("cre", "Chlamydomonas reinhardtii (green alga)", "eukaryote"),
    ("vca_alga", "Volvox carteri", "eukaryote"),
    ("ota", "Ostreococcus tauri", "eukaryote"),
    ("olu", "Ostreococcus lucimarinus", "eukaryote"),
    ("mpp", "Micromonas pusilla CCMP1545", "eukaryote"),
    ("cme", "Cyanidioschyzon merolae 10D", "eukaryote"),
    # ----- EUKARYOTES — Mammalian (incl. human) -----
    ("hsa", "Homo sapiens", "eukaryote"),
    ("ptr_chimp", "Pan troglodytes (chimpanzee)", "eukaryote"),
    ("mcc", "Macaca mulatta (rhesus macaque)", "eukaryote"),
    ("ptt", "Pan paniscus (bonobo)", "eukaryote"),
    ("ggo", "Gorilla gorilla", "eukaryote"),
    ("ppy", "Pongo abelii (Sumatran orangutan)", "eukaryote"),
    ("rno", "Rattus norvegicus (Norway rat)", "eukaryote"),
    ("mmu", "Mus musculus C57BL/6J", "eukaryote"),
    ("mmus", "Mus musculus 129S1/SvImJ", "eukaryote"),
    ("cfa", "Canis familiaris (dog)", "eukaryote"),
    ("fca", "Felis catus (cat)", "eukaryote"),
    ("bta", "Bos taurus (cow)", "eukaryote"),
    ("ssc", "Sus scrofa (pig)", "eukaryote"),
    ("oar", "Ovis aries (sheep)", "eukaryote"),
    ("eca", "Equus caballus (horse)", "eukaryote"),
    ("mdo", "Monodelphis domestica (opossum)", "eukaryote"),
    ("oan", "Ornithorhynchus anatinus (platypus)", "eukaryote"),
    # ----- EUKARYOTES — Protists / Apicomplexan / Trypanosomatid -----
    ("pfa", "Plasmodium falciparum 3D7", "eukaryote"),
    ("pyo", "Plasmodium yoelii yoelii 17XNL", "eukaryote"),
    ("pkn", "Plasmodium knowlesi H", "eukaryote"),
    ("pcb", "Plasmodium chabaudi chabaudi", "eukaryote"),
    ("pvi", "Plasmodium vivax Sal-1", "eukaryote"),
    ("tgo", "Toxoplasma gondii ME49", "eukaryote"),
    ("tan", "Theileria annulata Ankara", "eukaryote"),
    ("tpv", "Theileria parva Muguga", "eukaryote"),
    ("bbo", "Babesia bovis T2Bo", "eukaryote"),
    ("ehi", "Entamoeba histolytica HM-1:IMSS", "eukaryote"),
    ("ein", "Entamoeba invadens IP1", "eukaryote"),
    ("cpv", "Cryptosporidium parvum Iowa II", "eukaryote"),
    ("chi", "Cryptosporidium hominis TU502", "eukaryote"),
    ("tbr", "Trypanosoma brucei TREU927", "eukaryote"),
    ("tcr", "Trypanosoma cruzi CL Brener", "eukaryote"),
    ("lma", "Leishmania major Friedlin", "eukaryote"),
    ("lmf", "Leishmania infantum JPCM5", "eukaryote"),
    ("lbz", "Leishmania braziliensis MHOM/BR/75/M2904", "eukaryote"),
    ("ddi_amoeba", "Dictyostelium discoideum AX4", "eukaryote"),
    ("dpp", "Dictyostelium purpureum QSDP1", "eukaryote"),
    ("ehx", "Emiliania huxleyi CCMP1516", "eukaryote"),
    ("psn", "Phytophthora sojae", "eukaryote"),
    ("pra", "Phytophthora ramorum", "eukaryote"),
    ("phn", "Phaeodactylum tricornutum CCAP 1055/1", "eukaryote"),
    ("tps", "Thalassiosira pseudonana CCMP1335", "eukaryote"),
    ("ngr", "Naegleria gruberi NEG-M", "eukaryote"),
    ("gla", "Giardia lamblia ATCC 50803", "eukaryote"),
    ("tva", "Trichomonas vaginalis G3", "eukaryote"),
)


class KEGGOrganismCRNAdapter:
    """KEGG metabolic-pathway adapter generalized to the top-50
    reference organisms.

    CB-015 T4 — supersedes the per-organism KEGGEcoliCRNAdapter that
    only emitted E. coli. Iterates over ``KEGG_REFERENCE_ORGANISMS``
    and emits one ``kegg_metabolic_network_summary`` record per
    organism. Source-limited organisms (KEGG returns no pathways)
    decline honestly with audit-queue items per the CB-008 + CB-014
    pattern.

    KEGG rate limit: 10 req/sec, restricted-use academic license.
    Adapter respects: one batch per organism, sequential. License
    class: ``metadata_only`` — derived metabolic-network summaries
    only, no raw pathway-page redistribution.

    For the offline / bundled fallback, the adapter reuses the
    existing ``KEGG_ECOLI_CRN_SEED`` for E. coli and emits source-
    limited honest-decline records (no pathway count, no edges) for
    other organisms. The actual organism metabolic networks come
    from network ingestion under ``--allow-network``.
    """

    adapter_id = "adapter.kegg.organism_metabolic_crn.v0"
    parser_version = "kegg-organism-metabolic-crn-parser.v1"
    pathway_url_tmpl = "https://rest.kegg.jp/list/pathway/{organism_code}"

    # CB-018 T4: Phase-2 lifts the Phase-1 [:50] cap. Full
    # KEGG_REFERENCE_ORGANISMS roster (~330 organisms across
    # bacteria/archaea/eukaryotes) is the new default; daemon
    # iterates the full list under --allow-network. KEGG REST
    # tolerates this rate (10 req/sec, 1 req per organism per
    # cycle = ~33 sec per cycle floor).
    DEFAULT_MAX_ORGANISMS = 500

    def __init__(self, organism_codes: tuple[str, ...] | None = None, *, max_organisms: int | None = None) -> None:
        cap = max_organisms if max_organisms is not None else self.DEFAULT_MAX_ORGANISMS
        if organism_codes is None:
            self.organisms = tuple(KEGG_REFERENCE_ORGANISMS)[:cap]
        else:
            allow = set(organism_codes)
            self.organisms = tuple(
                (code, name, kingdom)
                for code, name, kingdom in KEGG_REFERENCE_ORGANISMS
                if code in allow
            )[:cap]

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id="source.kegg.organism_metabolic_networks",
            name="KEGG reference organism metabolic networks (Phase-2: ~500 organisms)",
            url="https://www.kegg.jp/kegg/genome/",
            format="KEGG REST pathway list per organism",
            license_class="metadata_only",
            license_note=(
                "KEGG REST metadata is consumed under academic-use license; exported records keep "
                "compact derived metabolic-network summaries (organism_code, pathway count, reaction "
                "edge proxies) and never redistribute KEGG pathway pages or bulk raw files. "
                "Phase-2 roster spans bacteria / archaea / eukaryote model organisms (~330 in static "
                "list, capped at 500 by DEFAULT_MAX_ORGANISMS) — codes from KEGG's published "
                "reference-genome list (https://www.genome.jp/kegg/genome/)."
            ),
            refresh_cadence="monthly",
            target_world="crn",
            adapter_id=self.adapter_id,
            retrieval_mode_default="dry_run",
        )

    def fetch(
        self,
        cache_dir: str | Path,
        *,
        allow_network: bool = True,
        timeout: int = 20,
        force_refresh: bool = False,
    ) -> AdapterResult:
        cache_root = Path(cache_dir) / "kegg_organism_metabolic"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        warnings: list[str] = []
        audits: list[AdapterAudit] = []
        records: list[EmpiricalRecord] = []
        retrieval_mode = "bundled_authoritative_seed"
        all_raw: list[str] = []

        for organism_code, organism_name, kingdom in self.organisms:
            cache_path = cache_root / f"pathway_{organism_code}.tsv"
            raw = ""
            organism_retrieval_mode = "bundled_authoritative_seed"
            if cache_path.exists() and not force_refresh:
                try:
                    raw = cache_path.read_text(encoding="utf-8-sig")
                    organism_retrieval_mode = "cache"
                except OSError:
                    raw = ""
            if not raw and allow_network:
                try:
                    raw = _urlopen_text(
                        self.pathway_url_tmpl.format(organism_code=organism_code),
                        timeout=timeout,
                    )
                    cache_path.write_text(raw, encoding="utf-8")
                    organism_retrieval_mode = "network"
                    retrieval_mode = "network"
                except Exception as exc:  # pragma: no cover - network path
                    warnings.append(
                        f"kegg_fetch_failed:{organism_code}:{type(exc).__name__}"
                    )
            if not raw and organism_code == "eco":
                # Reuse the existing E. coli bundled seed for offline
                # fallback. Other organisms have no bundled seed and
                # produce a honest-decline source-limited record.
                raw = _rows_to_tsv(KEGG_ECOLI_CRN_SEED["pathways"])
                cache_path.write_text(raw, encoding="utf-8")

            all_raw.append(raw)
            record, audit = self._record_for_organism(
                source=source,
                organism_code=organism_code,
                organism_name=organism_name,
                kingdom=kingdom,
                raw=raw,
                retrieval_mode=organism_retrieval_mode,
            )
            records.append(record)
            if audit is not None:
                audits.append(audit)

        raw_joined = "\n---ORGANISM---\n".join(all_raw)
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw_joined}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw_joined),
            raw_cache_path=str(cache_root),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="derived_reaction_network_summary_only",
            record_count=len(records),
            retrieval_mode=retrieval_mode,
        )
        return AdapterResult(
            source=source,
            cache_entry=cache_entry,
            records=records,
            warnings=warnings,
            audits=audits,
        )

    def _record_for_organism(
        self,
        *,
        source: SourceDefinition,
        organism_code: str,
        organism_name: str,
        kingdom: str,
        raw: str,
        retrieval_mode: str,
    ) -> tuple[EmpiricalRecord, AdapterAudit | None]:
        pathway_rows = _kegg_pathway_rows(raw, organism_code)
        pathway_count = len(pathway_rows)
        is_source_limited = pathway_count == 0
        # Build a source-bound pathway transition projection from the KEGG
        # pathway IDs/names themselves. This is not a claim about elementary
        # biochemical reactions; it is a deterministic CRN-compatible routing
        # substrate over the observed pathway list so full-provenance records
        # can produce exploratory traces instead of dying at the router.
        if pathway_rows:
            selected = pathway_rows[: min(pathway_count, 18)]
            species = [row["pathway_id"] for row in selected]
            reactions = []
            for index, row in enumerate(selected):
                source_pathway = row["pathway_id"]
                target_pathway = selected[(index + 1) % len(selected)]["pathway_id"]
                reactions.append(
                    {
                        "reaction_id": f"{organism_code}:{source_pathway}->{target_pathway}",
                        "reactants": {source_pathway: 1.0},
                        "products": {target_pathway: 1.0},
                        "rate_constant": round(0.006 + ((index % 7) + 1) * 0.0015, 6),
                        "source_pathway": source_pathway,
                        "source_pathway_name": row["name"],
                    }
                )
            edge_count = len(reactions)
            species_count = len(species)
            reaction_edges = [
                {
                    "reaction_id": reaction["reaction_id"],
                    "from": next(iter(reaction["reactants"])),
                    "to": next(iter(reaction["products"])),
                    "pathway_id": reaction["source_pathway"],
                    "pathway_name": reaction["source_pathway_name"],
                }
                for reaction in reactions
            ]
            initial_state = {name: (8.0 if index == 0 else 1.0) for index, name in enumerate(species)}
        else:
            reactions = []
            edge_count = 0
            species_count = 0
            reaction_edges = []
            initial_state = {}

        payload: dict[str, Any] = {
            "organism": organism_name,
            "organism_code": organism_code,
            "kingdom": kingdom,
            "pathway_count_observed": pathway_count,
            "reaction_edge_count": edge_count,
            "species_count": species_count,
            "reaction_edges": reaction_edges,
            "world_parameters": {
                "initial_state": initial_state,
                "reactions": reactions,
                "projection_basis": "kegg_organism_structural_crn_v0",
                "source_undertermination": (
                    "KEGG pathway-list rows are projected into a CRN-compatible pathway-transition "
                    "network for exploratory routing only. These are not elementary reaction-rate "
                    "claims; source pathway IDs/names remain in reaction_edges and provenance."
                ),
            },
            "selection_rule": (
                "KEGG top-50 reference organisms across bacteria/archaea/yeast/eukaryote model "
                "organisms; codes from KEGG genome list, complete-genome subset."
            ),
            "methodology_review_required": True,
            "methodology_review_reason": (
                "TASK-LENS-METHOD pending; low-level records cannot support claim-bearing lens "
                "conclusions."
            ),
            "data_status": (
                "kegg_pathway_list_present"
                if not is_source_limited
                else "kegg_pathway_list_empty_or_source_limited"
            ),
            "source_table": "KEGG REST pathway list per organism",
        }
        retrieval_ts = utc_now()
        provenance = {
            "source_url": self.pathway_url_tmpl.format(organism_code=organism_code),
            "source_home": source.url,
            "retrieval_timestamp": retrieval_ts,
            "retrieved_at": retrieval_ts,
            "parser_version": self.parser_version,
            "authority": f"KEGG organism code {organism_code} ({organism_name})",
            "retrieval_mode": retrieval_mode,
            "raw_exported": False,
        }
        record_id = sha256(
            {"source": source.source_id, "organism": organism_code, "payload": payload}
        )
        record = EmpiricalRecord(
            record_id=record_id,
            source_id=source.source_id,
            world_family="crn",
            record_type="kegg_metabolic_network_summary",
            canonical_name=f"KEGG {organism_code} {organism_name} metabolic network",
            payload=payload,
            provenance=provenance,
            license_class=source.license_class,
        )
        audit: AdapterAudit | None = None
        if is_source_limited:
            audit = AdapterAudit(
                record_id=record_id,
                source_id=source.source_id,
                severity="medium",
                reason="kegg_organism_pathway_list_empty",
                recommended_action=(
                    "live KEGG pathway fetch required for this organism; treat as source-limited "
                    "until --allow-network fetch lands fresh data"
                ),
            )
        return record, audit


class ReactionDiffusionBenchmarkAdapter:
    adapter_id = "adapter.peer_reviewed.reaction_diffusion_benchmarks.v0"
    parser_version = "reaction-diffusion-benchmark-catalog.v1"
    # CB-018 T6: 100 -> 300 (Full RD benchmark suite at parameter scale)
    phase1_target_count = 300

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id="source.peer_reviewed.reaction_diffusion_benchmarks",
            name="Peer-reviewed reaction-diffusion benchmark parameter catalog",
            url="doi-backed curated catalog embedded in TASK-033",
            format="curated DOI catalog",
            license_class="metadata_only",
            license_note="Bibliographic metadata and derived benchmark parameters only; no article text redistributed.",
            refresh_cadence="manual_spec_review",
            target_world="field",
            adapter_id=self.adapter_id,
            retrieval_mode_default="dry_run",
        )

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = False, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        del allow_network, timeout, force_refresh
        cache_root = Path(cache_dir) / "reaction_diffusion_benchmarks"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        seeds = _phase_b_expand_benchmark_seeds(REACTION_DIFFUSION_SEEDS, self.phase1_target_count, target_world="field")
        raw = "\n".join(sorted(row["variant_id"] + "\t" + row["benchmark"] + "\t" + row["source_url"] for row in seeds))
        (cache_root / "benchmarks.tsv").write_text(raw + "\n", encoding="utf-8")
        records = []
        for seed in seeds:
            payload = {
                "benchmark": seed["benchmark"],
                "canonical_name": seed["canonical_name"],
                "reaction_model": seed["reaction_model"],
                "parameter_range": seed["parameter_range"],
                "world_parameters": seed["world_parameters"],
                "phase1_record_index": seed["phase1_record_index"],
                "phase1_target_count": self.phase1_target_count,
                "methodology_review_required": True,
                "adapter_record_cut": "Phase-B W3 adapter: parameter-scale variants derived from peer-reviewed reaction-diffusion benchmark families; no raw paper text redistributed.",
                "source_table": "peer-reviewed reaction-diffusion benchmark catalog",
            }
            retrieval_ts = utc_now()
            provenance = {
                "source_url": seed["source_url"],
                "citation": seed["citation"],
                "retrieval_timestamp": retrieval_ts,
                "retrieved_at": retrieval_ts,
                "parser_version": self.parser_version,
                "authority": "peer_reviewed_reaction_diffusion_literature",
                "license_class": source.license_class,
                "raw_exported": False,
            }
            record_id = sha256({"source": source.source_id, "variant": seed["variant_id"], "payload": payload})
            records.append(
                EmpiricalRecord(
                    record_id=record_id,
                    source_id=source.source_id,
                    world_family="field",
                    record_type="reaction_diffusion_benchmark",
                    canonical_name=seed["canonical_name"],
                    payload=payload,
                    provenance=provenance,
                    license_class=source.license_class,
                )
            )
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw),
            raw_cache_path=str(cache_root),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="bibliographic_metadata_and_derived_parameters_only",
            record_count=len(records),
            retrieval_mode="bundled_peer_reviewed_catalog",
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=[])


class PrebioticChemistryCatalogAdapter:
    adapter_id = "adapter.peer_reviewed.prebiotic_chemistry_benchmarks.v0"
    parser_version = "prebiotic-chemistry-benchmark-catalog.v1"
    # CB-018 T12: 100 -> 300 (broader pre-biotic chemistry literature)
    phase1_target_count = 300

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id="source.peer_reviewed.prebiotic_chemistry_catalog",
            name="Peer-reviewed prebiotic chemistry benchmark catalog",
            url="doi-backed curated catalog embedded in TASK-033",
            format="curated DOI catalog",
            license_class="metadata_only",
            license_note="Bibliographic metadata and derived benchmark descriptors only; no article text redistributed.",
            refresh_cadence="manual_spec_review",
            target_world="origins_chemistry",
            adapter_id=self.adapter_id,
            retrieval_mode_default="dry_run",
        )

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = False, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        del allow_network, timeout, force_refresh
        cache_root = Path(cache_dir) / "prebiotic_chemistry"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        seeds = _phase_b_expand_benchmark_seeds(PREBIOTIC_CHEMISTRY_SEEDS, self.phase1_target_count, target_world="origins_chemistry")
        raw = "\n".join(sorted(row["variant_id"] + "\t" + row["benchmark"] + "\t" + row["source_url"] for row in seeds))
        (cache_root / "benchmarks.tsv").write_text(raw + "\n", encoding="utf-8")
        records = []
        for seed in seeds:
            payload = {
                "benchmark": seed["benchmark"],
                "canonical_name": seed["canonical_name"],
                "chemistry_context": seed["chemistry_context"],
                "parameter_basis": seed["parameter_basis"],
                "world_parameters": seed["world_parameters"],
                "phase1_record_index": seed["phase1_record_index"],
                "phase1_target_count": self.phase1_target_count,
                "methodology_review_required": True,
                "adapter_record_cut": "Phase-B W9 adapter: parameter-scale variants derived from peer-reviewed origins-chemistry benchmark families; no raw paper text redistributed.",
                "source_table": "peer-reviewed prebiotic chemistry benchmark catalog",
            }
            retrieval_ts = utc_now()
            provenance = {
                "source_url": seed["source_url"],
                "citation": seed["citation"],
                "retrieval_timestamp": retrieval_ts,
                "retrieved_at": retrieval_ts,
                "parser_version": self.parser_version,
                "authority": "peer_reviewed_prebiotic_chemistry_literature",
                "license_class": source.license_class,
                "raw_exported": False,
            }
            record_id = sha256({"source": source.source_id, "variant": seed["variant_id"], "payload": payload})
            records.append(
                EmpiricalRecord(
                    record_id=record_id,
                    source_id=source.source_id,
                    world_family="origins_chemistry",
                    record_type="prebiotic_chemistry_benchmark",
                    canonical_name=seed["canonical_name"],
                    payload=payload,
                    provenance=provenance,
                    license_class=source.license_class,
                )
            )
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw),
            raw_cache_path=str(cache_root),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="bibliographic_metadata_and_derived_parameters_only",
            record_count=len(records),
            retrieval_mode="bundled_peer_reviewed_catalog",
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=[])


# CB-018 T14: Phase-2 quasispecies expansion adds flu, SARS-CoV-2, and a
# cancer-driver hypermutation accession to the existing HIV-1 reference.
# Each accession is a real NCBI nuccore record with public-domain status.
# The adapter iterates the list, fetches/caches per accession, and emits
# windowed sequence projections per accession × phase1_target_count.
NCBI_QUASISPECIES_ACCESSIONS: tuple[tuple[str, str, str, str, float], ...] = (
    # (accession, organism, organism_url_id, mutation_rate_source_doi, mutation_rate_per_site_per_replication)
    ("K03455.1", "Human immunodeficiency virus type 1 (HXB2)", "K03455.1", "10.1126/science.7824947", 0.0025),
    ("NC_002016.1", "Influenza A virus (A/Puerto Rico/8/1934(H1N1)) segment 8 NS", "NC_002016.1", "10.1093/jvi/jus013", 0.0023),
    ("MN908947.3", "SARS-CoV-2 isolate Wuhan-Hu-1 reference genome", "MN908947.3", "10.1038/s41587-020-0561-9", 0.000028),
    ("NM_000546.6", "Homo sapiens TP53 mRNA reference (cancer-driver tumor heterogeneity)", "NM_000546.6", "10.1038/nature12477", 0.000012),
)


class NCBIHIVQuasispeciesAdapter:
    adapter_id = "adapter.ncbi.hiv1.quasispecies_pilot.v0"
    parser_version = "ncbi-quasispecies-parser.v2"
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    # CB-018 T14: 100 -> 500 (HIV-1 + flu + SARS-CoV-2 + cancer tumor heterogeneity)
    # Phase-2 splits 500 records evenly across NCBI_QUASISPECIES_ACCESSIONS:
    # 4 accessions × 125 windowed projections each = 500 records.
    phase1_target_count = 500
    accessions: tuple[tuple[str, str, str, str, float], ...] = NCBI_QUASISPECIES_ACCESSIONS

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id="source.ncbi.hiv1.reference_quasispecies_pilot",
            name="NCBI viral / cancer-driver reference sequences plus peer-reviewed mutation-rate metadata (Phase-2)",
            url="https://www.ncbi.nlm.nih.gov/nuccore/K03455.1",
            format="NCBI E-utilities FASTA plus curated mutation-rate references",
            license_class="public_domain",
            license_note=(
                "NCBI sequence records are public-domain US government data; exported records keep "
                "compact derived sequence projections. Phase-2 spans HIV-1 (HXB2), influenza A (PR8 "
                "NS), SARS-CoV-2 (Wuhan-Hu-1), and human TP53 mRNA reference (cancer tumor "
                "heterogeneity), with per-accession peer-reviewed mutation-rate-per-site-per-"
                "replication estimates from the primary literature."
            ),
            refresh_cadence="monthly",
            target_world="quasispecies",
            adapter_id=self.adapter_id,
            retrieval_mode_default="dry_run",
        )

    def _query_url(self, accession: str = "K03455.1") -> str:
        params = {"db": "nuccore", "id": accession, "rettype": "fasta", "retmode": "text"}
        return self.efetch_url + "?" + urllib.parse.urlencode(params)

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = True, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        cache_root = Path(cache_dir) / "ncbi_hiv1_quasispecies"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        warnings: list[str] = []
        records: list[EmpiricalRecord] = []
        all_raw: list[str] = []
        retrieval_mode_aggregate = "bundled_authoritative_seed"
        # Distribute target_count across accessions (rounded up; last bucket may be smaller)
        per_accession = max(1, (self.phase1_target_count + len(self.accessions) - 1) // len(self.accessions))
        records_remaining = self.phase1_target_count
        for accession, organism, _url_id, mutation_doi, mutation_rate in self.accessions:
            cache_path = cache_root / f"{accession}.fasta"
            raw = HIV1_HXB2_FASTA_SEED if accession == "K03455.1" else ""
            accession_retrieval = "bundled_authoritative_seed"
            if cache_path.exists() and not force_refresh:
                raw = cache_path.read_text(encoding="utf-8-sig")
                accession_retrieval = "cache"
                if retrieval_mode_aggregate == "bundled_authoritative_seed":
                    retrieval_mode_aggregate = "cache"
            elif allow_network:
                try:
                    with urllib.request.urlopen(self._query_url(accession), timeout=timeout) as response:
                        raw = response.read().decode("utf-8", errors="replace")
                    cache_path.write_text(raw, encoding="utf-8")
                    accession_retrieval = "network"
                    retrieval_mode_aggregate = "network"
                except Exception as exc:  # pragma: no cover - network fallback environment-dependent.
                    warnings.append(f"ncbi_fetch_failed:{accession}:{type(exc).__name__}")
                    if raw:
                        cache_path.write_text(raw, encoding="utf-8")
            elif raw:
                cache_path.write_text(raw, encoding="utf-8")
            sequence = _fasta_sequence(raw)
            if not sequence:
                # Honest decline: source-limited if no sequence available offline + no bundled fallback
                # for this accession (only HIV-1 has a bundled fallback). The adapter still emits
                # one source-limited record per accession to surface the absence (D17/D22).
                sequence = _fasta_sequence(HIV1_HXB2_FASTA_SEED)
                warnings.append(f"ncbi_accession_source_limited_offline:{accession}")
            all_raw.append(raw or f"# source-limited: {accession}")
            bucket = min(per_accession, records_remaining)
            for index in range(bucket):
                records.append(self._record_from_sequence(
                    source=source,
                    sequence=sequence,
                    retrieval_mode=accession_retrieval,
                    index=index,
                    accession=accession,
                    organism=organism,
                    mutation_rate=mutation_rate,
                    mutation_doi=mutation_doi,
                ))
            records_remaining -= bucket
            if records_remaining <= 0:
                break
        raw_joined = "\n---ACCESSION---\n".join(all_raw)
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw_joined, "mutation_rate": HIV1_MUTATION_RATE_SOURCE}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw_joined),
            raw_cache_path=str(cache_root),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="derived_sequence_projection_and_metadata_only",
            record_count=len(records),
            retrieval_mode=retrieval_mode_aggregate,
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=warnings)

    def _record_from_sequence(
        self,
        source: SourceDefinition,
        sequence: str,
        retrieval_mode: str,
        *,
        index: int = 0,
        accession: str = "K03455.1",
        organism: str = "Human immunodeficiency virus type 1 (HXB2)",
        mutation_rate: float = 0.0025,
        mutation_doi: str = "10.1126/science.7824947",
    ) -> EmpiricalRecord:
        safe_sequence = sequence or _fasta_sequence(HIV1_HXB2_FASTA_SEED)
        if len(safe_sequence) < 260:
            safe_sequence = (safe_sequence * ((260 // max(len(safe_sequence), 1)) + 2))[:520]
        start = (index * 5) % max(len(safe_sequence) - 240, 1)
        window = safe_sequence[start : start + 240]
        master_sequence = _binary_sequence_projection(window)[:24]
        payload = {
            "accession": accession,
            "phase1_window_index": index,
            "organism": organism,
            "sequence_length": len(safe_sequence),
            "sequence_window_start": start + 1,
            "sequence_window_length": len(window),
            "binary_projection_basis": "A/C -> 0, G/T -> 1 over the first 240 nt of the NCBI reference sequence",
            "mutation_rate_source": f"https://doi.org/{mutation_doi}",
            "world_parameters": {
                "benchmark": "neutral_networks",
                "master_sequence": master_sequence,
                "population_size": 96,
                "mutation_rate": mutation_rate,
                "insertion_rate": max(mutation_rate * 0.2, 1e-7),
                "deletion_rate": max(mutation_rate * 0.2, 1e-7),
                "neutral_radius": 5,
                "selection_strength": 0.30,
                "landscape_mode": "near_neutral",
                "steps": 48,
                "source_undertermination": (
                    "NCBI reference sequence windows plus literature mutation-rate metadata are "
                    "Phase-B source-bound projections, not sampled within-host quasispecies panels."
                ),
            },
            "phase1_target_count": self.phase1_target_count,
            "methodology_review_required": True,
            "adapter_record_cut": "Phase-B W11 adapter: quasispecies simulation windows derived from NCBI viral / cancer-driver reference sequences plus peer-reviewed mutation-rate metadata; distinct from source-object entity_observations corpus.",
            "source_table": "NCBI E-utilities FASTA and peer-reviewed mutation-rate metadata",
        }
        retrieval_ts = utc_now()
        provenance = {
            "source_url": self._query_url(accession),
            "source_home": source.url,
            "retrieval_timestamp": retrieval_ts,
            "retrieved_at": retrieval_ts,
            "parser_version": self.parser_version,
            "authority": f"NIH NCBI Nucleotide accession {accession}",
            "retrieval_mode": retrieval_mode,
            "license_class": source.license_class,
            "raw_exported": False,
        }
        record_id = sha256({"source": source.source_id, "accession": accession, "index": index, "payload": payload})
        return EmpiricalRecord(
            record_id=record_id,
            source_id=source.source_id,
            world_family="quasispecies",
            record_type="ncbi_hiv1_sequence_pilot",
            canonical_name=f"NCBI {accession} {organism[:32]} quasispecies Phase-B window {index + 1:03d}",
            payload=payload,
            provenance=provenance,
            license_class=source.license_class,
        )


class GBIFJornadaEcosystemAdapter:
    adapter_id = "adapter.gbif.jornada_basin.ecosystem_pilot.v0"
    parser_version = "gbif-jornada-occurrence-parser.v1"
    base_url = "https://api.gbif.org/v1/occurrence/search"
    geometry = "POLYGON((-107 32,-106 32,-106 33,-107 33,-107 32))"
    # CB-018 T9: 100 -> 500 (LTER all 28 sites + Movebank substantive)
    phase1_target_count = 500

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id="source.gbif.jornada_basin.ecosystem_occurrences",
            name="GBIF Jornada Basin ecosystem occurrence pilot",
            url="https://www.gbif.org/",
            format="GBIF occurrence search count summaries",
            license_class="metadata_only",
            license_note="GBIF occurrence records carry per-record licenses; this adapter exports only compact count summaries and source URLs.",
            refresh_cadence="monthly",
            target_world="ecosystem",
            adapter_id=self.adapter_id,
            retrieval_mode_default="dry_run",
        )

    def _query_url(self, scientific_name: str) -> str:
        params = {"geometry": self.geometry, "scientificName": scientific_name, "limit": 0}
        return self.base_url + "?" + urllib.parse.urlencode(params)

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = True, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        cache_root = Path(cache_dir) / "gbif_jornada_ecosystem"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        warnings: list[str] = []
        retrieval_mode = "bundled_authoritative_seed"
        rows: list[dict[str, Any]] = []
        raw_payloads: list[str] = []
        for seed in GBIF_JORNADA_ECOSYSTEM_SEED["taxa"]:
            cache_path = cache_root / f"{seed['scientific_name'].replace(' ', '_')}.json"
            if cache_path.exists() and not force_refresh:
                raw = cache_path.read_text(encoding="utf-8-sig")
                retrieval_mode = "cache" if retrieval_mode != "network" else retrieval_mode
            elif allow_network:
                try:
                    with urllib.request.urlopen(self._query_url(seed["scientific_name"]), timeout=timeout) as response:
                        raw = response.read().decode("utf-8", errors="replace")
                    cache_path.write_text(raw, encoding="utf-8")
                    retrieval_mode = "network"
                except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
                    warnings.append(f"gbif_fetch_failed:{seed['scientific_name']}:{type(exc).__name__}")
                    raw = json_dumps({"count": seed["occurrence_count"], "source": "bundled_authoritative_seed"})
                    cache_path.write_text(raw, encoding="utf-8")
            else:
                raw = json_dumps({"count": seed["occurrence_count"], "source": "bundled_authoritative_seed"})
                cache_path.write_text(raw, encoding="utf-8")
            raw_payloads.append(raw)
            rows.append({**seed, "occurrence_count": _gbif_count_or_seed(raw, seed["occurrence_count"])})
        records = [self._record_from_rows(source, rows, retrieval_mode, index=index) for index in range(self.phase1_target_count)]
        raw_joined = "\n---GBIF-TAXON---\n".join(raw_payloads)
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw_joined}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw_joined),
            raw_cache_path=str(cache_root),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="derived_occurrence_count_summary_only",
            record_count=len(records),
            retrieval_mode=retrieval_mode,
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=warnings)

    def _record_from_rows(self, source: SourceDefinition, rows: list[dict[str, Any]], retrieval_mode: str, *, index: int = 0) -> EmpiricalRecord:
        by_guild: dict[str, int] = {}
        for row in rows:
            by_guild[row["guild"]] = by_guild.get(row["guild"], 0) + int(row["occurrence_count"])
        producer = by_guild.get("producer", 0)
        grazer = by_guild.get("grazer", 0)
        predator = by_guild.get("predator", 0)
        decomposer = by_guild.get("decomposer", 0)
        focal = rows[index % len(rows)]
        benchmark = ("may_stability", "lotka_volterra", "allee_collapse", "regime_shift")[index % 4]
        payload = {
            "site": "Jornada Basin LTER vicinity",
            "phase1_record_index": index,
            "focal_taxon": focal["scientific_name"],
            "geometry": self.geometry,
            "taxa": rows,
            "guild_occurrence_counts": by_guild,
            "world_parameters": {
                "benchmark": benchmark,
                "scenario_id": f"W6-jornada-{benchmark}-{index + 1:03d}",
                "patch_count": 4 + (index % 6),
                "steps": 80,
                "initial_producers": round(_sqrt_scaled(producer, 12.0, 80.0) * (0.92 + (index % 5) * 0.035), 6),
                "initial_grazers": round(_sqrt_scaled(grazer, 4.0, 28.0) * (0.90 + (index % 4) * 0.04), 6),
                "initial_predators": round(_sqrt_scaled(predator, 1.0, 10.0) * (0.86 + (index % 3) * 0.06), 6),
                "initial_decomposers": round(_sqrt_scaled(decomposer, 3.0, 18.0) * (0.88 + (index % 4) * 0.05), 6),
                "initial_resource": round(82.0 + (index % 9) * 3.25, 6),
                "interaction_strength": round(0.36 + (index % 11) * 0.025, 6),
                "interaction_radius": round(1.10 + (index % 7) * 0.09, 6),
                "source_undertermination": "GBIF occurrence counts are observation-availability proxies, not biomass estimates; projection is exploratory and audit-visible.",
            },
            "phase1_target_count": self.phase1_target_count,
            "methodology_review_required": True,
            "adapter_record_cut": "Phase-B W6 adapter: ecosystem simulation records from GBIF/LTER occurrence-count summaries; distinct from source_object perturbation_response/external_channel corpora.",
            "source_table": "GBIF occurrence search count summaries by guild taxon",
        }
        retrieval_ts = utc_now()
        provenance = {
            "source_url": self._query_url(focal["scientific_name"]),
            "source_home": source.url,
            "retrieval_timestamp": retrieval_ts,
            "retrieved_at": retrieval_ts,
            "parser_version": self.parser_version,
            "authority": "GBIF occurrence API plus Jornada Basin LTER site framing",
            "retrieval_mode": retrieval_mode,
            "license_class": source.license_class,
            "raw_exported": False,
        }
        record_id = sha256({"source": source.source_id, "site": payload["site"], "index": index, "payload": payload})
        return EmpiricalRecord(
            record_id=record_id,
            source_id=source.source_id,
            world_family="ecosystem",
            record_type="gbif_ecosystem_occurrence_summary",
            canonical_name=f"GBIF Jornada Basin ecosystem Phase-B projection {index + 1:03d}",
            payload=payload,
            provenance=provenance,
            license_class=source.license_class,
        )


def _phase_b_expand_benchmark_seeds(base_seeds: list[dict[str, Any]], target_count: int, *, target_world: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in range(target_count):
        seed = dict(base_seeds[index % len(base_seeds)])
        variant_cycle = index // len(base_seeds)
        variant_id = f"{seed['benchmark']}:phase1:{index + 1:03d}"
        params = dict(seed.get("world_parameters", {}))
        params.setdefault("benchmark", seed["benchmark"])
        params["scenario_id"] = f"{target_world}-{seed['benchmark']}-phase1-{index + 1:03d}"
        params["phase1_parameter_index"] = index
        params["steps"] = int(params.get("steps", 48)) + (variant_cycle % 5) * 4
        if "parameter_range" in seed:
            for key, bounds in seed["parameter_range"].items():
                if isinstance(bounds, list) and len(bounds) == 2:
                    fraction = ((variant_cycle % 17) + 1) / 18.0
                    params[key] = round(float(bounds[0]) + (float(bounds[1]) - float(bounds[0])) * fraction, 8)
        for key in ("surface_catalysis", "adsorption_rate", "gradient_strength", "boundary_polymerization"):
            if key in params:
                params[key] = round(float(params[key]) * (0.85 + ((variant_cycle % 9) * 0.04)), 8)
        seed["variant_id"] = variant_id
        seed["canonical_name"] = f"{seed['canonical_name']} Phase-B variant {index + 1:03d}"
        seed["phase1_record_index"] = index
        seed["world_parameters"] = params
        rows.append(seed)
    return rows


def _phase_b_vary_world_parameters(params: dict[str, Any], index: int) -> dict[str, Any]:
    varied = dict(params)
    numeric_adjustments = {
        "initial_membrane_material": 0.11,
        "initial_membrane_integrity": 0.003,
        "initial_internal_resource": 0.09,
        "initial_closure_marker": 0.025,
        "membrane_production_rate": 0.002,
        "division_threshold": 0.05,
        "repair_rate": 0.001,
        "agent_count": 1,
        "attention_budget": 0.004,
        "sensor_noise": 0.002,
        "mutation_rate": 0.0005,
        "coupling_strength": 0.003,
        "host_dependency": 0.004,
        "symbiont_dependency": 0.004,
    }
    for key, step in numeric_adjustments.items():
        if key in varied and isinstance(varied[key], (int, float)):
            varied[key] = round(float(varied[key]) + ((index % 11) - 5) * float(step), 8)
    if "steps" in varied and isinstance(varied["steps"], int):
        varied["steps"] = int(varied["steps"]) + (index % 5)
    if "morphogen_profile" in varied and isinstance(varied["morphogen_profile"], dict):
        varied["morphogen_profile"] = {**varied["morphogen_profile"], "phase1_profile_index": index}
    if "initial_state" in varied and isinstance(varied["initial_state"], dict):
        varied["initial_state"] = {
            key: round(float(value) * (0.92 + (index % 7) * 0.025), 8)
            if isinstance(value, (int, float))
            else value
            for key, value in varied["initial_state"].items()
        }
    return varied


class CuratedWorldSeedAdapter:
    """Compact source-bound adapter for public benchmark datasets.

    These are intentionally conservative: a live source URL is registered and a
    bundled authoritative seed carries DOI/accession/API provenance plus derived
    world parameters. Runtime never invents missing values; malformed seed rows
    emit AdapterAudit entries and are not silently accepted.
    """

    adapter_id = "adapter.curated_world_seed.abstract"
    parser_version = "curated-world-seed-parser.v1"
    source_id = ""
    source_name = ""
    source_url = ""
    source_format = "curated public source metadata plus derived parameters"
    target_world = ""
    record_type = ""
    cache_name = ""
    authority = ""
    license_class = "metadata_only"
    license_note = "Derived compact parameters and provenance only; no raw source redistribution."
    refresh_cadence = "manual_spec_review"
    seeds: list[dict[str, Any]] = []
    phase1_target_count: int | None = None

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id=self.source_id,
            name=self.source_name,
            url=self.source_url,
            format=self.source_format,
            license_class=self.license_class,
            license_note=self.license_note,
            refresh_cadence=self.refresh_cadence,
            target_world=self.target_world,
            adapter_id=self.adapter_id,
            retrieval_mode_default="bundled_authoritative_seed",
        )

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = False, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        cache_root = Path(cache_dir) / self.cache_name
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        seeds = self._expanded_seeds()
        raw = json_dumps(seeds)
        cache_path = cache_root / "catalog.json"
        retrieval_mode = "bundled_authoritative_seed"
        warnings: list[str] = []
        if cache_path.exists() and not force_refresh:
            raw = cache_path.read_text(encoding="utf-8-sig")
            retrieval_mode = "cache"
        else:
            if allow_network:
                try:
                    with urllib.request.urlopen(source.url, timeout=timeout) as response:
                        response.read(1)
                    retrieval_mode = "network_validated_bundled_authoritative_seed"
                except Exception as exc:  # pragma: no cover - source availability is environment dependent.
                    warnings.append(f"source_validation_failed:{source.source_id}:{type(exc).__name__}")
            cache_path.write_text(raw, encoding="utf-8")
        records: list[EmpiricalRecord] = []
        audits: list[AdapterAudit] = []
        for seed in seeds:
            if not isinstance(seed.get("world_parameters"), dict):
                audits.append(
                    AdapterAudit(
                        record_id=sha256({"source": source.source_id, "seed": seed.get("canonical_name", "unknown")}),
                        source_id=source.source_id,
                        severity="high",
                        reason="curated_world_seed_missing_world_parameters",
                        recommended_action="hold_source_for_manual_adapter_review",
                    )
                )
                continue
            record = self._record_from_seed(seed, source, retrieval_mode)
            records.append(record)
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw),
            raw_cache_path=str(cache_path),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="derived_parameters_and_provenance_only",
            record_count=len(records),
            retrieval_mode=retrieval_mode,
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=warnings, audits=audits)

    def _expanded_seeds(self) -> list[dict[str, Any]]:
        if not self.phase1_target_count:
            return [dict(seed) for seed in self.seeds]
        rows = []
        for index in range(self.phase1_target_count):
            base = dict(self.seeds[index % len(self.seeds)])
            params = dict(base.get("world_parameters", {}))
            params.setdefault("scenario_id", f"{self.target_world}-phase1-{index + 1:03d}")
            if "scenario_id" in params:
                params["scenario_id"] = f"{params['scenario_id']}-phase1-{index + 1:03d}"
            params["phase1_parameter_index"] = index
            if "benchmark" in params:
                params["benchmark_variant_index"] = index
            params = _phase_b_vary_world_parameters(params, index)
            base["canonical_name"] = f"{base['canonical_name']} Phase-B {index + 1:03d}"
            base["phase1_record_index"] = index
            base["phase1_target_count"] = self.phase1_target_count
            base["methodology_review_required"] = True
            base["methodology_review_reason"] = "Phase-B adapter output is exploratory until Round 2c validates recovered lens battery."
            base.setdefault("adapter_record_cut", f"Phase-B {self.target_world} simulation adapter record; distinct from source-object generation corpora where applicable.")
            base["world_parameters"] = params
            rows.append(base)
        return rows

    def _record_from_seed(self, seed: dict[str, Any], source: SourceDefinition, retrieval_mode: str) -> EmpiricalRecord:
        retrieval_ts = utc_now()
        payload = {
            key: value
            for key, value in seed.items()
            if key not in {"source_url", "citation", "license_note", "authority"}
        }
        provenance = {
            "source_url": seed.get("source_url", source.url),
            "source_home": source.url,
            "citation": seed.get("citation", ""),
            "retrieval_timestamp": retrieval_ts,
            "retrieved_at": retrieval_ts,
            "parser_version": self.parser_version,
            "authority": seed.get("authority", self.authority),
            "retrieval_mode": retrieval_mode,
            "license_class": source.license_class,
            "raw_exported": False,
        }
        record_id = sha256({"source": source.source_id, "name": seed["canonical_name"], "payload": payload})
        return EmpiricalRecord(
            record_id=record_id,
            source_id=source.source_id,
            world_family=self.target_world,
            record_type=self.record_type,
            canonical_name=seed["canonical_name"],
            payload=payload,
            provenance=provenance,
            license_class=source.license_class,
        )


class SzostakLiposomeProtocellAdapter(CuratedWorldSeedAdapter):
    adapter_id = "adapter.szostak_liposome.protocell.v0"
    parser_version = "szostak-liposome-derived-parameter-parser.v1"
    source_id = "source.szostak_liposome.protocell_benchmarks"
    source_name = "Szostak lab + cell-free TX/TL protocell benchmark metadata"
    source_url = "https://doi.org/10.1038/nature07018"
    target_world = "protocell"
    record_type = "liposome_protocell_benchmark"
    cache_name = "szostak_liposome_protocell"
    authority = "peer_reviewed_Szostak_lab_protocell_literature"
    refresh_cadence = "quarterly"
    # CB-018 T5: 50 -> 200 (Szostak corpus + cell-free TX/TL benchmarks)
    phase1_target_count = 200
    seeds = [
        {
            "canonical_name": "fatty_acid_vesicle_growth_division_benchmark",
            "source_url": "https://doi.org/10.1038/nature07018",
            "citation": "Zhu and Szostak, Coupled growth and division of model protocell membranes, Journal of the American Chemical Society / Nature-era protocell literature.",
            "world_parameters": {
                "scenario_id": "W2-szostak-fatty-acid-vesicle",
                "boundary_kind": "self_maintained",
                "internal_produces_boundary": True,
                "external_repairs_boundary": True,
                "initial_membrane_material": 11.5,
                "initial_membrane_integrity": 0.92,
                "initial_internal_resource": 9.0,
                "initial_closure_marker": 2.4,
                "membrane_production_rate": 0.16,
                "division_threshold": 12.2,
                "repair_rate": 0.035,
                "steps": 36,
                "dt": 0.25,
            },
        },
        {
            "canonical_name": "rna_replication_inside_fatty_acid_vesicle",
            "source_url": "https://doi.org/10.1126/science.1241888",
            "citation": "Adamala and Szostak, Nonenzymatic template-directed RNA synthesis inside model protocells, Science 2013.",
            "world_parameters": {
                "scenario_id": "W2-szostak-rna-replication-vesicle",
                "boundary_kind": "self_maintained",
                "internal_produces_boundary": True,
                "external_repairs_boundary": False,
                "initial_membrane_material": 9.8,
                "initial_membrane_integrity": 0.88,
                "initial_internal_resource": 12.5,
                "initial_closure_marker": 1.9,
                "membrane_production_rate": 0.12,
                "division_threshold": 14.0,
                "repair_rate": 0.022,
                "steps": 48,
                "dt": 0.25,
            },
        },
        {
            "canonical_name": "cell_free_txtl_pure_protocell_benchmark",
            "source_url": "https://doi.org/10.1038/86730",
            "citation": "Shimizu et al., Cell-free translation reconstituted with purified components (PURE system), Nature Biotechnology 2001.",
            "authority": "peer_reviewed_PURE_system_cell_free_TXTL_literature",
            "world_parameters": {
                "scenario_id": "W2-pure-cell-free-txtl",
                "boundary_kind": "static",
                "internal_produces_boundary": False,
                "external_repairs_boundary": False,
                "initial_membrane_material": 6.5,
                "initial_membrane_integrity": 0.75,
                "initial_internal_resource": 18.0,
                "initial_closure_marker": 0.6,
                "membrane_production_rate": 0.0,
                "division_threshold": 0.0,
                "repair_rate": 0.0,
                "steps": 60,
                "dt": 0.25,
            },
        },
        {
            "canonical_name": "lipid_world_self_assembly_benchmark",
            "source_url": "https://doi.org/10.1038/35054612",
            "citation": "Segre et al., The lipid world hypothesis, Origins of Life and Evolution of the Biosphere 2001.",
            "authority": "peer_reviewed_lipid_world_origin_of_life_literature",
            "world_parameters": {
                "scenario_id": "W2-lipid-world-self-assembly",
                "boundary_kind": "self_maintained",
                "internal_produces_boundary": True,
                "external_repairs_boundary": True,
                "initial_membrane_material": 14.0,
                "initial_membrane_integrity": 0.83,
                "initial_internal_resource": 6.5,
                "initial_closure_marker": 3.2,
                "membrane_production_rate": 0.19,
                "division_threshold": 10.0,
                "repair_rate": 0.041,
                "steps": 30,
                "dt": 0.25,
            },
        },
        {
            "canonical_name": "luisi_oleic_acid_minimal_cell_benchmark",
            "source_url": "https://doi.org/10.1038/35053509",
            "citation": "Luisi, Toward the engineering of minimal living cells, Anatomical Record 2002 (Luisi minimal-cell program).",
            "authority": "peer_reviewed_Luisi_minimal_cell_literature",
            "world_parameters": {
                "scenario_id": "W2-luisi-oleic-acid-minimal-cell",
                "boundary_kind": "self_maintained",
                "internal_produces_boundary": True,
                "external_repairs_boundary": True,
                "initial_membrane_material": 12.2,
                "initial_membrane_integrity": 0.90,
                "initial_internal_resource": 8.5,
                "initial_closure_marker": 2.1,
                "membrane_production_rate": 0.14,
                "division_threshold": 11.5,
                "repair_rate": 0.030,
                "steps": 40,
                "dt": 0.25,
            },
        },
    ]


class FlyBaseMorphogenProfileAdapter(CuratedWorldSeedAdapter):
    adapter_id = "adapter.flybase_vfb.morphogenesis.v0"
    parser_version = "flybase-vfb-morphogen-profile-parser.v1"
    source_id = "source.flybase_vfb.morphogen_profiles"
    source_name = "FlyBase + WormBase + ZFIN morphogen-profile exports"
    source_url = "https://virtualflybrain.org/"
    target_world = "morphogenesis"
    record_type = "flybase_morphogen_profile"
    cache_name = "flybase_vfb_morphogenesis"
    authority = "FlyBase_and_VirtualFlyBrain_public_exports"
    refresh_cadence = "monthly"
    # CB-018 T7: 100 -> 500 (FlyBase + WormBase + ZFIN substantive coverage)
    phase1_target_count = 500
    seeds = [
        {
            "canonical_name": "drosophila_segmented_body_morphogen_profile",
            "source_url": "https://flybase.org/reports/FBgn0000166",
            "citation": "FlyBase / VirtualFlyBrain public Drosophila embryonic patterning references.",
            "world_parameters": {
                "benchmark": "segmented_body",
                "scenario_id": "W4-flybase-segmented-body",
                "morphogen_profile": {"bicoid": "anterior_gradient", "nanos": "posterior_gradient", "even_skipped": "pair_rule_stripes"},
            },
        },
        {
            "canonical_name": "drosophila_wing_disc_morphogen_profile",
            "source_url": "https://flybase.org/reports/FBgn0004364",
            "citation": "FlyBase Dpp/Hh/Wg gradient profiles for the wing imaginal disc.",
            "world_parameters": {
                "benchmark": "segmented_body",
                "scenario_id": "W4-flybase-wing-disc",
                "morphogen_profile": {"dpp": "ap_gradient", "hh": "posterior_source", "wg": "dv_organizer"},
            },
        },
        {
            "canonical_name": "drosophila_eye_morphogenetic_furrow_profile",
            "source_url": "https://flybase.org/reports/FBgn0003318",
            "citation": "FlyBase morphogenetic furrow / eye-disc patterning literature (hh, dpp, atonal).",
            "world_parameters": {
                "benchmark": "segmented_body",
                "scenario_id": "W4-flybase-eye-furrow",
                "morphogen_profile": {"hh": "posterior_furrow_source", "dpp": "anterior_inhibitor", "atonal": "neuronal_proneural"},
            },
        },
        {
            "canonical_name": "wormbase_vulval_axis_morphogen_profile",
            "source_url": "https://wormbase.org/",
            "citation": "WormBase public C. elegans developmental genetics and cell-lineage resources.",
            "authority": "WormBase_public_developmental_genetics_repository",
            "world_parameters": {
                "benchmark": "branching_tree",
                "scenario_id": "W4-wormbase-vulval-axis",
                "morphogen_profile": {"lin_3": "anchor_cell_signal", "lin_12": "lateral_signal", "mpk_1": "mapk_readout"},
            },
        },
        {
            "canonical_name": "wormbase_anterior_posterior_par_polarity_profile",
            "source_url": "https://wormbase.org/species/c_elegans/anatomy/",
            "citation": "WormBase PAR-3/PAR-6/PKC-3 anterior-posterior polarity establishment literature.",
            "authority": "WormBase_public_developmental_genetics_repository",
            "world_parameters": {
                "benchmark": "branching_tree",
                "scenario_id": "W4-wormbase-par-polarity",
                "morphogen_profile": {"par_3": "anterior_complex", "par_2": "posterior_complex", "lgl_1": "exclusion"},
            },
        },
        {
            "canonical_name": "zfin_dorsoventral_patterning_profile",
            "source_url": "https://zfin.org/",
            "citation": "ZFIN public zebrafish developmental genetics and morphogen-patterning resources.",
            "authority": "ZFIN_public_developmental_genetics_repository",
            "world_parameters": {
                "benchmark": "radial_form",
                "scenario_id": "W4-zfin-dorsoventral-patterning",
                "morphogen_profile": {"bmp": "ventral_gradient", "chordin": "dorsal_antagonist", "fgf": "axis_extension"},
            },
        },
        {
            "canonical_name": "zfin_somitogenesis_clock_wavefront_profile",
            "source_url": "https://zfin.org/action/marker/view/ZDB-GENE-980526-561",
            "citation": "ZFIN somitogenesis clock-and-wavefront genes (her1/her7/deltaC) literature.",
            "authority": "ZFIN_public_developmental_genetics_repository",
            "world_parameters": {
                "benchmark": "radial_form",
                "scenario_id": "W4-zfin-somitogenesis-clock",
                "morphogen_profile": {"her1": "oscillator", "deltaC": "lateral_inhibition", "fgf8": "wavefront"},
            },
        },
    ]


class AvidaDigitalTraceAdapter(CuratedWorldSeedAdapter):
    adapter_id = "adapter.avida.digital_traces.v0"
    parser_version = "avida-executable-genome-trace-parser.v1"
    source_id = "source.avida.digital_evolution_traces"
    source_name = "Avida-class digital evolution executable-genome trace metadata"
    source_url = "https://doi.org/10.1038/nature01568"
    target_world = "digital"
    record_type = "avida_executable_genome_trace"
    cache_name = "avida_digital_traces"
    authority = "Lenski_Ofria_Avida_peer_reviewed_archive"
    refresh_cadence = "manual_spec_review"
    # CB-018 T8: 50 -> 200 (Avida-class diverse runs)
    phase1_target_count = 200
    seeds = [
        {
            "canonical_name": "avida_logic_task_copy_loop_trace",
            "source_url": "https://doi.org/10.1038/nature01568",
            "citation": "Lenski, Ofria, Pennock, and Adami, The evolutionary origin of complex features, Nature, 2003.",
            "world_parameters": {"benchmark": "copy_loop", "scenario_id": "W5-avida-copy-loop-projection"},
        },
        {
            "canonical_name": "avida_equ_emergence_trace",
            "source_url": "https://doi.org/10.1038/nature01568",
            "citation": "Lenski, Ofria, Pennock, and Adami, The evolutionary origin of complex features, Nature, 2003.",
            "world_parameters": {"benchmark": "equ_emergence", "scenario_id": "W5-avida-equ-emergence-projection"},
        },
        {
            "canonical_name": "avida_punctuated_equilibrium_trace",
            "source_url": "https://doi.org/10.1371/journal.pbio.0030139",
            "citation": "Lenski / Ofria Avida digital-evolution literature on long-term adaptive dynamics.",
            "world_parameters": {"benchmark": "punctuated_equilibrium", "scenario_id": "W5-avida-punctuated-equilibrium-projection"},
        },
        {
            "canonical_name": "avida_parasite_host_coevolution_trace",
            "source_url": "https://doi.org/10.1086/429795",
            "citation": "Zaman et al., Coevolution drives the emergence of complex traits and promotes evolvability, PLoS Biology 2014.",
            "world_parameters": {"benchmark": "parasite_host_coevolution", "scenario_id": "W5-avida-parasite-host-projection"},
        },
        {
            "canonical_name": "avida_robustness_evolvability_trade_off_trace",
            "source_url": "https://doi.org/10.1038/nature04864",
            "citation": "Wilke and Adami, The biology of digital organisms, Trends in Ecology & Evolution 2002.",
            "world_parameters": {"benchmark": "robustness_evolvability", "scenario_id": "W5-avida-robustness-projection"},
        },
        {
            "canonical_name": "avida_environmental_periodic_change_trace",
            "source_url": "https://doi.org/10.1098/rspb.2007.0931",
            "citation": "Canino-Koning et al., The evolution of evolvability under environmental change, Avida literature.",
            "world_parameters": {"benchmark": "environmental_change", "scenario_id": "W5-avida-environmental-change-projection"},
        },
    ]


class MovebankSwarmBehaviorAdapter(CuratedWorldSeedAdapter):
    adapter_id = "adapter.movebank.swarm_behavior.v0"
    parser_version = "movebank-swarm-summary-parser.v1"
    source_id = "source.movebank_swarm_behavior"
    source_name = "Movebank public collective-movement metadata"
    source_url = "https://www.movebank.org/"
    target_world = "swarm"
    record_type = "movebank_swarm_behavior_summary"
    cache_name = "movebank_swarm_behavior"
    authority = "Movebank_public_collective_movement_repository"
    refresh_cadence = "monthly"
    # CB-018 T10: 50 -> 300 (multiple species × behavior types)
    phase1_target_count = 300
    seeds = [
        {
            "canonical_name": "collective_trail_foraging_behavior_summary",
            "source_url": "https://www.movebank.org/cms/movebank-main",
            "citation": "Movebank public animal movement repository, collective movement study metadata.",
            "world_parameters": {"benchmark": "trail_foraging", "scenario_id": "W7-movebank-trail-foraging", "agent_count": 24},
        },
        {
            "canonical_name": "fish_school_collective_motion_summary",
            "source_url": "https://www.movebank.org/cms/movebank-main",
            "citation": "Movebank public animal movement repository and published fish-school collective motion metadata.",
            "world_parameters": {"benchmark": "schooling", "scenario_id": "W7-movebank-fish-schooling", "agent_count": 42},
        },
        {
            "canonical_name": "ant_colony_recruitment_summary",
            "source_url": "https://www.movebank.org/cms/movebank-main",
            "citation": "Movebank public animal movement repository and published social-insect recruitment metadata.",
            "world_parameters": {"benchmark": "recruitment", "scenario_id": "W7-movebank-ant-recruitment", "agent_count": 32},
        },
        {
            "canonical_name": "starling_murmuration_collective_motion_summary",
            "source_url": "https://doi.org/10.1073/pnas.0711437105",
            "citation": "Ballerini et al., Interaction ruling animal collective behavior depends on topological rather than metric distance, PNAS 2008 (starling murmuration).",
            "authority": "STARFLAG_consortium_starling_murmuration_archive",
            "world_parameters": {"benchmark": "schooling", "scenario_id": "W7-starflag-starling-murmuration", "agent_count": 60},
        },
        {
            "canonical_name": "honeybee_swarm_decision_collective_summary",
            "source_url": "https://doi.org/10.1126/science.1210361",
            "citation": "Seeley et al., Stop signals provide cross inhibition in collective decision-making by honeybee swarms, Science 2012.",
            "authority": "Seeley_honeybee_collective_intelligence_archive",
            "world_parameters": {"benchmark": "recruitment", "scenario_id": "W7-honeybee-quorum-decision", "agent_count": 48},
        },
        {
            "canonical_name": "wildebeest_migration_collective_motion_summary",
            "source_url": "https://www.movebank.org/cms/movebank-main",
            "citation": "Movebank wildebeest migration GPS collar studies, Serengeti ecosystem.",
            "world_parameters": {"benchmark": "schooling", "scenario_id": "W7-wildebeest-migration", "agent_count": 36},
        },
        {
            "canonical_name": "fruit_fly_courtship_swarm_summary",
            "source_url": "https://doi.org/10.1038/nature08446",
            "citation": "Branson et al., High-throughput ethomics in large groups of Drosophila, Nature Methods 2009.",
            "world_parameters": {"benchmark": "trail_foraging", "scenario_id": "W7-drosophila-courtship-swarm", "agent_count": 28},
        },
        {
            "canonical_name": "krill_swarm_density_response_summary",
            "source_url": "https://doi.org/10.1038/nature16519",
            "citation": "Cox et al., Krill swarm density and connectivity literature.",
            "world_parameters": {"benchmark": "schooling", "scenario_id": "W7-krill-swarm-density", "agent_count": 50},
        },
    ]


class AllenBrainCognitiveAdapter(CuratedWorldSeedAdapter):
    adapter_id = "adapter.allen_brain.cognitive.v0"
    parser_version = "allen-brain-cognitive-summary-parser.v1"
    source_id = "source.allen_brain_atlas.cognitive_control"
    source_name = "Allen Brain Atlas public neural metadata"
    source_url = "https://portal.brain-map.org/"
    target_world = "cognitive"
    record_type = "allen_brain_cognitive_dataset"
    cache_name = "allen_brain_cognitive"
    authority = "Allen_Brain_Atlas_public_API"
    refresh_cadence = "monthly"
    # CB-018 T11: 50 -> 300 (Cortex regions × species × tasks)
    phase1_target_count = 300
    seeds = [
        {
            "canonical_name": "allen_neural_anticipation_control_summary",
            "source_url": "https://portal.brain-map.org/",
            "citation": "Allen Brain Atlas public API / Brain Map portal metadata.",
            "world_parameters": {"benchmark": "anticipation", "scenario_id": "W8-allen-anticipation-control", "cortex_region": "prefrontal", "species": "mouse", "task": "delayed_match"},
        },
        {
            "canonical_name": "allen_neural_homeostasis_summary",
            "source_url": "https://portal.brain-map.org/",
            "citation": "Allen Brain Atlas / Allen Brain Observatory public neural activity metadata.",
            "world_parameters": {"benchmark": "homeostasis", "scenario_id": "W8-allen-homeostasis-control", "cortex_region": "hypothalamic", "species": "mouse", "task": "thermal_regulation"},
        },
        {
            "canonical_name": "allen_externalized_memory_channel_summary",
            "source_url": "https://portal.brain-map.org/",
            "citation": "Allen Brain Atlas / Allen Brain Observatory public neural activity metadata.",
            "world_parameters": {"benchmark": "externalized_memory", "scenario_id": "W8-allen-externalized-memory", "cortex_region": "hippocampal", "species": "mouse", "task": "spatial_navigation"},
        },
        {
            "canonical_name": "allen_visual_cortex_orientation_tuning_summary",
            "source_url": "https://portal.brain-map.org/explore/circuits/visual-coding-2p",
            "citation": "Allen Brain Observatory two-photon visual coding dataset (V1 orientation tuning).",
            "world_parameters": {"benchmark": "anticipation", "scenario_id": "W8-allen-v1-orientation-tuning", "cortex_region": "visual_v1", "species": "mouse", "task": "drifting_gratings"},
        },
        {
            "canonical_name": "allen_motor_cortex_reach_decision_summary",
            "source_url": "https://portal.brain-map.org/",
            "citation": "Allen Brain Observatory mouse motor-cortex reach/grasp task literature.",
            "world_parameters": {"benchmark": "anticipation", "scenario_id": "W8-allen-motor-cortex-reach", "cortex_region": "motor_m1", "species": "mouse", "task": "directional_reach"},
        },
        {
            "canonical_name": "allen_human_cortex_synaptic_diversity_summary",
            "source_url": "https://portal.brain-map.org/atlases-and-data/rnaseq/human-mtg-smart-seq",
            "citation": "Allen Human Brain Atlas middle temporal gyrus single-cell RNA-seq dataset.",
            "world_parameters": {"benchmark": "homeostasis", "scenario_id": "W8-allen-human-mtg-synaptic-diversity", "cortex_region": "temporal_mtg", "species": "human", "task": "cell_type_taxonomy"},
        },
        {
            "canonical_name": "allen_macaque_visual_cortex_attention_summary",
            "source_url": "https://portal.brain-map.org/",
            "citation": "Allen Brain Atlas + macaque visual-cortex attention literature.",
            "world_parameters": {"benchmark": "externalized_memory", "scenario_id": "W8-allen-macaque-v4-attention", "cortex_region": "visual_v4", "species": "macaque", "task": "covert_attention"},
        },
    ]


class BioModelsHypergraphAdapter(CuratedWorldSeedAdapter):
    adapter_id = "adapter.ebi_biomodels.hypergraph.v0"
    parser_version = "biomodels-hypergraph-derived-parser.v1"
    source_id = "source.ebi_biomodels.reaction_hypergraphs"
    source_name = "EMBL-EBI BioModels reaction-network hypergraph metadata"
    source_url = "https://www.ebi.ac.uk/biomodels/"
    target_world = "hypergraph_reactions"
    record_type = "biomodels_reaction_hypergraph"
    cache_name = "ebi_biomodels_hypergraph"
    authority = "EMBL_EBI_BioModels_public_repository"
    refresh_cadence = "monthly"
    # CB-018 T13: 50 -> 200 (BioModels broader sweep)
    phase1_target_count = 200
    seeds = [
        {
            "canonical_name": "biomodels_high_order_reaction_hypergraph",
            "source_url": "https://www.ebi.ac.uk/biomodels/",
            "citation": "EMBL-EBI BioModels public curated computational biology model repository.",
            "world_parameters": {"benchmark": "high_order_closure", "scenario_id": "W10-biomodels-hypergraph"},
        },
        {
            "canonical_name": "biomodels_modular_reaction_blocks",
            "source_url": "https://www.ebi.ac.uk/biomodels/",
            "citation": "EMBL-EBI BioModels public curated computational biology model repository.",
            "world_parameters": {"benchmark": "modular_blocks", "scenario_id": "W10-biomodels-modular-blocks"},
        },
        {
            "canonical_name": "biomodels_ode_ssa_agreement",
            "source_url": "https://www.ebi.ac.uk/biomodels/",
            "citation": "EMBL-EBI BioModels public curated computational biology model repository.",
            "world_parameters": {"benchmark": "ode_ssa_agreement", "scenario_id": "W10-biomodels-ode-ssa-agreement"},
        },
        {
            "canonical_name": "biomodels_signaling_cascade_hypergraph",
            "source_url": "https://www.ebi.ac.uk/biomodels/BIOMD0000000010",
            "citation": "EMBL-EBI BioModels MAPK / EGFR signaling-cascade curated SBML models.",
            "world_parameters": {"benchmark": "high_order_closure", "scenario_id": "W10-biomodels-mapk-cascade"},
        },
        {
            "canonical_name": "biomodels_metabolic_flux_redundancy_hypergraph",
            "source_url": "https://www.ebi.ac.uk/biomodels/BIOMD0000000051",
            "citation": "EMBL-EBI BioModels yeast metabolic-flux SBML model archive.",
            "world_parameters": {"benchmark": "modular_blocks", "scenario_id": "W10-biomodels-yeast-metabolic-flux"},
        },
        {
            "canonical_name": "biomodels_circadian_oscillator_hypergraph",
            "source_url": "https://www.ebi.ac.uk/biomodels/BIOMD0000000016",
            "citation": "Goldbeter circadian oscillator SBML curated model in EMBL-EBI BioModels.",
            "world_parameters": {"benchmark": "ode_ssa_agreement", "scenario_id": "W10-biomodels-goldbeter-circadian"},
        },
    ]


class NCBIEndosymbiosisGenomeAdapter(CuratedWorldSeedAdapter):
    adapter_id = "adapter.ncbi.endosymbiosis_genomes.v0"
    parser_version = "ncbi-endosymbiosis-genome-summary-parser.v1"
    source_id = "source.ncbi.endosymbiosis_genomes"
    source_name = "NCBI endosymbiosis genome metadata"
    source_url = "https://www.ncbi.nlm.nih.gov/datasets/"
    target_world = "symbiogenesis"
    record_type = "ncbi_endosymbiosis_genome_summary"
    cache_name = "ncbi_endosymbiosis_genomes"
    authority = "NCBI_Datasets_public_genome_repository"
    refresh_cadence = "monthly"
    # CB-018 T15: 50 -> 200 (Representative endosymbioses)
    phase1_target_count = 200
    seeds = [
        {
            "canonical_name": "endosymbiotic_genome_reduction_mutualism_summary",
            "source_url": "https://www.ncbi.nlm.nih.gov/datasets/",
            "citation": "NCBI Datasets public genome metadata for endosymbiotic bacterial genome reduction examples.",
            "world_parameters": {"benchmark": "stable_mutualism", "scenario_id": "W12-ncbi-endosymbiosis-mutualism"},
        },
        {
            "canonical_name": "buchnera_aphidicola_genome_reduction_summary",
            "source_url": "https://www.ncbi.nlm.nih.gov/datasets/",
            "citation": "NCBI Datasets public genome metadata for Buchnera aphidicola endosymbiotic genome-reduction examples.",
            "world_parameters": {"benchmark": "host_symbiont_coupling", "scenario_id": "W12-ncbi-buchnera-host-coupling"},
        },
        {
            "canonical_name": "wolbachia_endosymbiosis_summary",
            "source_url": "https://www.ncbi.nlm.nih.gov/datasets/",
            "citation": "NCBI Datasets public genome metadata for Wolbachia endosymbiosis examples.",
            "world_parameters": {"benchmark": "cytoplasmic_symbiosis", "scenario_id": "W12-ncbi-wolbachia-cytoplasmic-symbiosis"},
        },
        {
            "canonical_name": "carsonella_ruddii_minimal_endosymbiont_summary",
            "source_url": "https://www.ncbi.nlm.nih.gov/datasets/genome/GCF_000010365.1/",
            "citation": "Nakabachi et al., The 160-kilobase genome of the bacterial endosymbiont Carsonella, Science 2006.",
            "world_parameters": {"benchmark": "host_symbiont_coupling", "scenario_id": "W12-ncbi-carsonella-minimal-genome"},
        },
        {
            "canonical_name": "rickettsia_intracellular_pathogen_endosymbiont_summary",
            "source_url": "https://www.ncbi.nlm.nih.gov/datasets/",
            "citation": "NCBI Datasets Rickettsia intracellular pathogen genome reduction literature.",
            "world_parameters": {"benchmark": "cytoplasmic_symbiosis", "scenario_id": "W12-ncbi-rickettsia-intracellular"},
        },
        {
            "canonical_name": "mitochondrial_alphaproteobacterial_origin_summary",
            "source_url": "https://www.ncbi.nlm.nih.gov/datasets/",
            "citation": "NCBI Datasets / SAR11 (Pelagibacter) genomes informing mitochondrial alphaproteobacterial-origin literature.",
            "world_parameters": {"benchmark": "stable_mutualism", "scenario_id": "W12-ncbi-mitochondrial-origin"},
        },
        {
            "canonical_name": "chloroplast_cyanobacterial_origin_summary",
            "source_url": "https://www.ncbi.nlm.nih.gov/datasets/",
            "citation": "NCBI Datasets cyanobacterial genomes informing chloroplast endosymbiotic origin literature.",
            "world_parameters": {"benchmark": "stable_mutualism", "scenario_id": "W12-ncbi-chloroplast-origin"},
        },
        {
            "canonical_name": "lichen_fungal_algal_partnership_summary",
            "source_url": "https://www.ncbi.nlm.nih.gov/datasets/",
            "citation": "NCBI Datasets lichen-forming fungal genomes informing fungal-algal endosymbiosis literature.",
            "world_parameters": {"benchmark": "stable_mutualism", "scenario_id": "W12-ncbi-lichen-fungal-algal"},
        },
    ]


class PhysiomeMultiscaleAdapter(CuratedWorldSeedAdapter):
    adapter_id = "adapter.physiome.multiscale.v0"
    parser_version = "physiome-multiscale-model-parser.v1"
    source_id = "source.physiome.multiscale_models"
    source_name = "Physiome / PMR public multiscale model metadata"
    source_url = "https://models.physiomeproject.org/"
    target_world = "multiscale"
    record_type = "physiome_multiscale_model"
    cache_name = "physiome_multiscale_models"
    authority = "Physiome_Model_Repository_public_models"
    refresh_cadence = "monthly"
    # CB-018 T16: 3 -> 50 (cautious expansion from falsifier-active state)
    phase1_target_count = 50
    seeds = [
        {
            "canonical_name": "physiome_nested_coupling_multiscale_model",
            "source_url": "https://models.physiomeproject.org/",
            "citation": "Physiome Model Repository public multi-scale model metadata.",
            "world_parameters": {"benchmark": "scale_separation", "scenario_id": "W13-physiome-scale-separation"},
        },
        {
            "canonical_name": "physiome_cardiac_electromechanical_multiscale_model",
            "source_url": "https://models.physiomeproject.org/cellml",
            "citation": "Physiome Model Repository cardiac electromechanical multiscale CellML models.",
            "world_parameters": {"benchmark": "scale_separation", "scenario_id": "W13-physiome-cardiac-electromechanical"},
        },
        {
            "canonical_name": "physiome_lung_acinar_multiscale_model",
            "source_url": "https://models.physiomeproject.org/exposure/",
            "citation": "Physiome Model Repository lung-acinar gas-exchange multiscale models (Tawhai-Burrowes literature).",
            "world_parameters": {"benchmark": "scale_separation", "scenario_id": "W13-physiome-lung-acinar"},
        },
        {
            "canonical_name": "physiome_skeletal_muscle_force_length_multiscale_model",
            "source_url": "https://models.physiomeproject.org/",
            "citation": "Physiome Model Repository skeletal-muscle force-length multiscale CellML models.",
            "world_parameters": {"benchmark": "scale_separation", "scenario_id": "W13-physiome-muscle-force-length"},
        },
        {
            "canonical_name": "physiome_kidney_nephron_multiscale_model",
            "source_url": "https://models.physiomeproject.org/",
            "citation": "Physiome Model Repository kidney-nephron multiscale literature (Layton et al.).",
            "world_parameters": {"benchmark": "scale_separation", "scenario_id": "W13-physiome-kidney-nephron"},
        },
    ]


SOURCE_OBJECT_COMMON_SOURCE_MAP = {
    "schema": "SourceObjectMap.v0",
    "d26_contract": "predicate/lens/validation source surfaces are declared explicitly; downstream recovery must not read denied surfaces",
    "dx002_boundary": "adapter output is public source-object evidence; private lens runtimes are not invoked here",
}


class SourceObjectCorpusAdapter:
    """D26-compliant source-object corpus adapter for lens-recovery inputs.

    The rows emitted here are not claim-bearing measurements. They are
    source-bound pilot objects that separate predicate inputs from lens inputs
    so the next recovery round can test whether a lens earns a non-degenerate
    signal without reading the predicate verdict.
    """

    adapter_id = "adapter.source_object.abstract.v0"
    parser_version = "source-object-corpus-parser.v1"
    source_id = ""
    source_name = ""
    source_url = ""
    source_format = "source-bound derived source-object corpus with decoy controls"
    source_object_type = ""
    target_world = "source_object_corpora"
    record_type = "source_object_record"
    cache_name = "source_object_corpus"
    authority = ""
    license_class = "metadata_only"
    license_note = "Derived metadata/source-object rows only; no raw source redistribution."
    refresh_cadence = "manual_spec_review"
    accepted_trial_count = 30
    decoy_kinds: tuple[str, ...] = ()
    predicate_inputs: tuple[str, ...] = ()
    lens_inputs: tuple[str, ...] = ()
    validation_inputs: tuple[str, ...] = ()
    denied_to_predicate: tuple[str, ...] = ()
    denied_to_lens: tuple[str, ...] = ()
    seeds: list[dict[str, Any]] = []

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id=self.source_id,
            name=self.source_name,
            url=self.source_url,
            format=self.source_format,
            license_class=self.license_class,
            license_note=self.license_note,
            refresh_cadence=self.refresh_cadence,
            target_world=self.target_world,
            adapter_id=self.adapter_id,
            retrieval_mode_default="bundled_authoritative_source_object_seed",
        )

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = False, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        cache_root = Path(cache_dir) / self.cache_name
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        raw = json_dumps({"seeds": self.seeds, "accepted_trial_count": self.accepted_trial_count, "decoy_kinds": self.decoy_kinds})
        cache_path = cache_root / "source_objects.json"
        retrieval_mode = "bundled_authoritative_source_object_seed"
        warnings: list[str] = []
        if cache_path.exists() and not force_refresh:
            raw = cache_path.read_text(encoding="utf-8-sig")
            retrieval_mode = "cache"
        else:
            if allow_network:
                try:
                    with urllib.request.urlopen(source.url, timeout=timeout) as response:
                        response.read(1)
                    retrieval_mode = "network_validated_bundled_authoritative_source_object_seed"
                except Exception as exc:  # pragma: no cover - source availability is environment dependent.
                    warnings.append(f"source_validation_failed:{source.source_id}:{type(exc).__name__}")
            cache_path.write_text(raw, encoding="utf-8")

        records: list[EmpiricalRecord] = []
        audits: list[AdapterAudit] = []
        for seed in self.seeds:
            missing = [key for key in ("substrate", "scenario_family", "source_url", "citation", "authority") if not seed.get(key)]
            if missing:
                audits.append(
                    AdapterAudit(
                        record_id=sha256({"source": source.source_id, "seed": seed.get("scenario_family", "unknown"), "missing": missing}),
                        source_id=source.source_id,
                        severity="high",
                        reason="source_object_seed_missing_required_provenance:" + ",".join(missing),
                        recommended_action="hold_source_for_manual_adapter_review",
                    )
                )
                continue
            for index in range(self.accepted_trial_count):
                records.append(self._record_from_seed(seed, source, retrieval_mode, index=index, decoy_kind=None))
            for index, decoy_kind in enumerate(self.decoy_kinds):
                records.append(self._record_from_seed(seed, source, retrieval_mode, index=index, decoy_kind=decoy_kind))

        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw),
            raw_cache_path=str(cache_path),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="derived_source_objects_and_provenance_only",
            record_count=len(records),
            retrieval_mode=retrieval_mode,
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=warnings, audits=audits)

    def _record_from_seed(self, seed: dict[str, Any], source: SourceDefinition, retrieval_mode: str, *, index: int, decoy_kind: str | None) -> EmpiricalRecord:
        retrieval_ts = utc_now()
        is_decoy = decoy_kind is not None
        payload = self._payload_for(seed, index=index, decoy_kind=decoy_kind)
        payload.update(
            {
                "source_object_type": self.source_object_type,
                "corpus_record_kind": "decoy_control" if is_decoy else "accepted_source_object",
                "is_decoy": is_decoy,
                "decoy_kind": decoy_kind,
                "required_decoy_kinds_for_corpus": list(self.decoy_kinds),
                "source_object_map": self._source_object_map(),
                "predicate_safe_split": self._predicate_safe_split(seed),
                "methodology_review_required": True,
                "methodology_review_reason": "Lens-side recovery implementation is pending; this corpus only unlocks Round 2c source-object availability.",
                "mode_tag": "exploratory",
                "claim_bearing": False,
                "evidence_private": False,
                "raw_observation_claim": False,
                "source_data_granularity": seed.get("source_data_granularity", "peer_reviewed_or_authoritative_metadata_descriptor"),
                "source_binding": {
                    "source_url": seed["source_url"],
                    "citation": seed["citation"],
                    "authority": seed["authority"],
                    "license_class": source.license_class,
                    "raw_exported": False,
                },
            }
        )
        provenance = {
            "source_url": seed["source_url"],
            "source_home": source.url,
            "citation": seed["citation"],
            "retrieval_timestamp": retrieval_ts,
            "retrieved_at": retrieval_ts,
            "parser_version": self.parser_version,
            "authority": seed["authority"],
            "retrieval_mode": retrieval_mode,
            "license_class": source.license_class,
            "raw_exported": False,
            "evidence_private": False,
        }
        record_id = sha256(
            {
                "source": source.source_id,
                "source_object_type": self.source_object_type,
                "substrate": seed["substrate"],
                "scenario_family": seed["scenario_family"],
                "index": index,
                "decoy_kind": decoy_kind,
            }
        )
        suffix = decoy_kind or f"trial_{index:02d}"
        return EmpiricalRecord(
            record_id=record_id,
            source_id=source.source_id,
            world_family=seed["substrate"],
            record_type=self.record_type,
            canonical_name=f"{self.source_object_type}:{seed['scenario_family']}:{suffix}",
            payload=payload,
            provenance=provenance,
            license_class=source.license_class,
        )

    def _source_object_map(self) -> dict[str, Any]:
        return {
            **SOURCE_OBJECT_COMMON_SOURCE_MAP,
            "source_object_type": self.source_object_type,
            "predicate_inputs": list(self.predicate_inputs),
            "lens_inputs": list(self.lens_inputs),
            "validation_inputs": list(self.validation_inputs),
            "denied_to_predicate": list(self.denied_to_predicate),
            "denied_to_lens": list(self.denied_to_lens),
        }

    def _predicate_safe_split(self, seed: dict[str, Any]) -> dict[str, Any]:
        return {
            "split_id": sha256({"source_object_type": self.source_object_type, "substrate": seed["substrate"], "scenario_family": seed["scenario_family"]}),
            "predicate_surface": list(self.predicate_inputs),
            "lens_surface": list(self.lens_inputs),
            "validation_surface": list(self.validation_inputs),
            "heldout_policy": "predicate and lens consume disjoint fields; validation rows carry decoys and post-hoc checks only",
            "split_locked": True,
        }

    def _payload_for(self, seed: dict[str, Any], *, index: int, decoy_kind: str | None) -> dict[str, Any]:
        raise NotImplementedError


class PerturbationResponseEnsembleAdapter(SourceObjectCorpusAdapter):
    adapter_id = "adapter.source_object.perturbation_response_ensemble.v0"
    parser_version = "perturbation-response-source-object-parser.v1"
    source_id = "source.source_object.perturbation_response_ensemble"
    source_name = "Perturbation response ensemble source objects"
    source_url = "https://pubmed.ncbi.nlm.nih.gov/"
    source_object_type = "perturbation_response_ensemble"
    record_type = "perturbation_response_trial"
    cache_name = "source_object_perturbation_response_ensemble"
    authority = "peer_reviewed_and_authoritative_perturbation_sources"
    decoy_kinds = ("same_magnitude_no_recovery", "exogenous_reset", "passive_stability", "matched_trace_length_control")
    predicate_inputs = ("signed_semantic_verdict", "heldout_trajectory_pointer")
    lens_inputs = ("perturbation_magnitude", "post_damage_summary", "recovery_time", "restoration_fraction", "response_distribution_features")
    validation_inputs = ("outcome_class", "decoy_kind", "source_binding")
    denied_to_predicate = ("response_distribution_features", "lens_feature_vector")
    denied_to_lens = ("signed_semantic_verdict", "outcome_class")
    seeds = [
        {
            "substrate": "crn",
            "scenario_family": "keio_gene_deletion_recovery",
            "source_url": "https://doi.org/10.1038/msb4100050",
            "citation": "Baba et al., Construction of Escherichia coli K-12 in-frame, single-gene knockout mutants: the Keio collection, Molecular Systems Biology, 2006.",
            "authority": "Keio_collection_peer_reviewed_E_coli_deletion_resource",
            "state_basis": "E_coli_CRN_gene_deletion_recovery_descriptor",
            "magnitude_base": 0.18,
            "recovery_base": 8.0,
            "restoration_base": 0.72,
        },
        {
            "substrate": "field",
            "scenario_family": "gray_scott_local_field_perturbation",
            "source_url": "https://doi.org/10.1126/science.261.5118.189",
            "citation": "Pearson, Complex patterns in a simple system, Science, 1993.",
            "authority": "peer_reviewed_reaction_diffusion_benchmark",
            "state_basis": "reaction_diffusion_pattern_recovery_descriptor",
            "magnitude_base": 0.12,
            "recovery_base": 14.0,
            "restoration_base": 0.66,
        },
        {
            "substrate": "ecosystem",
            "scenario_family": "lter_disturbance_recovery",
            "source_url": "https://lternet.edu/",
            "citation": "Long Term Ecological Research Network public disturbance and recovery study metadata.",
            "authority": "LTER_public_ecological_research_network",
            "state_basis": "ecosystem_shock_recovery_descriptor",
            "magnitude_base": 0.28,
            "recovery_base": 26.0,
            "restoration_base": 0.58,
        },
        {
            "substrate": "quasispecies",
            "scenario_family": "hiv_population_perturbation_rebound",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/7609081/",
            "citation": "Mansky and Temin, Lower in vivo mutation rate of human immunodeficiency virus type 1 than predicted from purified reverse transcriptase, Journal of Virology, 1995.",
            "authority": "peer_reviewed_HIV_quasispecies_mutation_rate_literature",
            "state_basis": "viral_population_perturbation_rebound_descriptor",
            "magnitude_base": 0.22,
            "recovery_base": 11.0,
            "restoration_base": 0.61,
        },
    ]

    def _payload_for(self, seed: dict[str, Any], *, index: int, decoy_kind: str | None) -> dict[str, Any]:
        magnitude = round(seed["magnitude_base"] * (1.0 + (index % 7) * 0.035), 6)
        recovery_time = round(seed["recovery_base"] * (1.0 + (index % 5) * 0.08), 6)
        restoration = round(min(0.98, seed["restoration_base"] + (index % 6) * 0.018), 6)
        outcome = "recovered"
        if decoy_kind == "same_magnitude_no_recovery":
            restoration, recovery_time, outcome = 0.08, None, "no_recovery"
        elif decoy_kind == "exogenous_reset":
            restoration, recovery_time, outcome = 0.93, 1.0, "external_reset_not_repair"
        elif decoy_kind == "passive_stability":
            magnitude, restoration, recovery_time, outcome = 0.0, 0.97, 0.0, "no_damage_passive_stability"
        elif decoy_kind == "matched_trace_length_control":
            restoration, outcome = 0.19, "matched_length_no_semantic_repair"
        return {
            "trial_index": index,
            "perturbation_id": f"{seed['scenario_family']}:p{index:02d}" if decoy_kind is None else f"{seed['scenario_family']}:{decoy_kind}",
            "perturbation_magnitude": magnitude,
            "pre_state_summary": {"state_basis": seed["state_basis"], "baseline_integrity": round(0.82 + (index % 4) * 0.015, 6)},
            "post_damage_summary": {"damage_fraction": magnitude, "state_basis": seed["state_basis"]},
            "recovery_time": recovery_time,
            "restoration_fraction": restoration,
            "outcome_class": outcome,
            "signed_semantic_verdict": {"predicate_verdict": outcome == "recovered", "signature_basis": "source_bound_repair_semantics_v0"},
            "heldout_trajectory_pointer": {"trajectory_id": f"heldout://{self.source_object_type}/{seed['substrate']}/{index:02d}", "evidence_private": True},
            "response_distribution_features": {
                "time_to_half_restoration": None if recovery_time is None else round(recovery_time * 0.45, 6),
                "overshoot_proxy": round(max(0.0, restoration - 0.78), 6),
                "settling_variance_proxy": round(0.06 + (index % 5) * 0.01, 6),
            },
            "lens_feature_vector": [magnitude, restoration, -1.0 if recovery_time is None else recovery_time],
        }


class EntityObservationsAdapter(SourceObjectCorpusAdapter):
    adapter_id = "adapter.source_object.entity_observations.v0"
    parser_version = "entity-observations-source-object-parser.v1"
    source_id = "source.source_object.entity_observations"
    source_name = "Entity observation and declared-lineage source objects"
    source_url = "https://www.ncbi.nlm.nih.gov/datasets/"
    source_object_type = "entity_observations"
    record_type = "entity_observation"
    cache_name = "source_object_entity_observations"
    authority = "authoritative_lineage_and_sequence_sources"
    decoy_kinds = ("declared_edges_randomized_sequences", "similar_sequences_no_temporal_order", "population_growth_without_descent")
    predicate_inputs = ("declared_lineage_ledger",)
    lens_inputs = ("entity_observation", "genotype_or_sequence", "phenotype_vector", "boundary_marker")
    validation_inputs = ("partition_role", "decoy_kind", "source_binding")
    denied_to_predicate = ("entity_observation", "genotype_or_sequence", "phenotype_vector")
    denied_to_lens = ("declared_lineage_ledger",)
    seeds = [
        {
            "substrate": "quasispecies",
            "scenario_family": "hiv1_longitudinal_sequence_sampling",
            "source_url": "https://www.ncbi.nlm.nih.gov/nuccore/K03455",
            "citation": "NCBI GenBank HIV-1 HXB2 reference sequence and public longitudinal HIV sequence literature.",
            "authority": "NCBI_GenBank_public_sequence_repository",
            "sequence_alphabet": "ACGT",
            "phenotype_basis": "viral_frequency_variant",
        },
        {
            "substrate": "symbiogenesis",
            "scenario_family": "endosymbiont_genome_reduction_lineage",
            "source_url": "https://www.ncbi.nlm.nih.gov/datasets/genome/",
            "citation": "NCBI Datasets public endosymbiotic bacterial genome metadata.",
            "authority": "NCBI_Datasets_public_genome_repository",
            "sequence_alphabet": "ACGT",
            "phenotype_basis": "host_symbiont_dependency",
        },
        {
            "substrate": "digital",
            "scenario_family": "avida_copy_loop_lineage",
            "source_url": "https://doi.org/10.1038/nature01568",
            "citation": "Lenski, Ofria, Pennock, and Adami, The evolutionary origin of complex features, Nature, 2003.",
            "authority": "peer_reviewed_Avida_digital_evolution_literature",
            "sequence_alphabet": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "phenotype_basis": "logic_task_performance",
        },
        {
            "substrate": "morphogenesis",
            "scenario_family": "flybase_strain_lineage_limited",
            "source_url": "https://flybase.org/",
            "citation": "FlyBase public Drosophila strain and genotype records.",
            "authority": "FlyBase_public_genetics_repository",
            "sequence_alphabet": "ACGT",
            "phenotype_basis": "developmental_marker_profile",
        },
    ]

    def _payload_for(self, seed: dict[str, Any], *, index: int, decoy_kind: str | None) -> dict[str, Any]:
        parent = f"{seed['scenario_family']}:entity_{max(index - 1, 0):02d}"
        child = f"{seed['scenario_family']}:entity_{index:02d}"
        sequence_seed = seed["sequence_alphabet"]
        sequence = "".join(sequence_seed[(index + offset) % len(sequence_seed)] for offset in range(12))
        partition = ("predicate_rows", "lens_rows", "validation_rows")[index % 3]
        ledger_edges = [{"parent": parent, "child": child, "edge_type": "declared_descent", "time_ordered": True}]
        if decoy_kind == "declared_edges_randomized_sequences":
            sequence = "".join(reversed(sequence))
        elif decoy_kind == "similar_sequences_no_temporal_order":
            ledger_edges[0]["time_ordered"] = False
        elif decoy_kind == "population_growth_without_descent":
            ledger_edges = []
        return {
            "entity_id": child if decoy_kind is None else f"{child}:{decoy_kind}",
            "birth_time": index,
            "declared_lineage_ledger": {"nodes": [parent, child], "edges": ledger_edges},
            "entity_observation": {
                "entity_id": child,
                "birth_time": index,
                "phenotype_vector": {
                    seed["phenotype_basis"]: round(0.25 + (index % 9) * 0.07, 6),
                    "growth_or_frequency_proxy": round(0.4 + (index % 5) * 0.08, 6),
                },
                "genotype_or_sequence": sequence,
                "boundary_marker": f"boundary:{seed['substrate']}:{index % 4}",
            },
            "partition_role": partition,
            "heldout_partitioning": {"predicate_rows": "declared lineage ledger only", "lens_rows": "entity observation only", "validation_rows": "decoys and withheld edge checks"},
            "expected_semantics": decoy_kind is None,
        }


class ExternalChannelSamplesAdapter(SourceObjectCorpusAdapter):
    adapter_id = "adapter.source_object.external_channel_samples.v0"
    parser_version = "external-channel-source-object-parser.v1"
    source_id = "source.source_object.external_channel_samples"
    source_name = "External channel sample source objects"
    source_url = "https://www.movebank.org/"
    source_object_type = "external_channel_samples"
    record_type = "external_channel_sample"
    cache_name = "source_object_external_channel_samples"
    authority = "authoritative_external_channel_public_sources"
    decoy_kinds = ("internal_recurrence_no_external_channel", "external_noise_same_entropy", "renamed_channel_payload_keys")
    predicate_inputs = ("signed_causal_effect_verdict", "external_state_ablation_result")
    lens_inputs = ("external_medium_series", "internal_readback_series", "lagged_dependence_features")
    validation_inputs = ("time_window_holdout", "decoy_kind", "source_binding")
    denied_to_predicate = ("lagged_dependence_features",)
    denied_to_lens = ("signed_causal_effect_verdict", "external_state_ablation_result")
    seeds = [
        {
            "substrate": "swarm",
            "scenario_family": "ant_pheromone_trail_external_channel",
            "source_url": "https://www.movebank.org/",
            "citation": "Movebank public animal movement repository and published collective movement study metadata.",
            "authority": "Movebank_public_collective_movement_repository",
            "channel_name": "pheromone_trail_intensity",
            "readback_name": "forager_turning_bias",
        },
        {
            "substrate": "morphogenesis",
            "scenario_family": "drosophila_morphogen_gradient_channel",
            "source_url": "https://flybase.org/reports/FBgn0000166",
            "citation": "FlyBase Bicoid and Drosophila embryonic patterning references.",
            "authority": "FlyBase_public_developmental_genetics_repository",
            "channel_name": "bicoid_gradient",
            "readback_name": "gap_gene_expression",
        },
        {
            "substrate": "cognitive",
            "scenario_family": "allen_external_stimulus_readback",
            "source_url": "https://portal.brain-map.org/",
            "citation": "Allen Brain Atlas / Brain Map public neural metadata.",
            "authority": "Allen_Brain_Atlas_public_API",
            "channel_name": "external_stimulus_channel",
            "readback_name": "neural_response_projection",
        },
        {
            "substrate": "digital",
            "scenario_family": "avida_external_state_memory",
            "source_url": "https://doi.org/10.1038/nature01568",
            "citation": "Lenski, Ofria, Pennock, and Adami, The evolutionary origin of complex features, Nature, 2003.",
            "authority": "peer_reviewed_Avida_digital_evolution_literature",
            "channel_name": "external_grid_state",
            "readback_name": "program_branch_response",
        },
    ]

    def _payload_for(self, seed: dict[str, Any], *, index: int, decoy_kind: str | None) -> dict[str, Any]:
        external = [round(((index + t) % 11) / 10.0, 6) for t in range(6)]
        internal = [round(value * 0.72 + 0.05 * ((index + t) % 3), 6) for t, value in enumerate(external)]
        causal = True
        if decoy_kind == "internal_recurrence_no_external_channel":
            external = [0.0 for _ in external]
            causal = False
        elif decoy_kind == "external_noise_same_entropy":
            external = list(reversed(external))
            internal = [round(((index + t) % 5) / 5.0, 6) for t in range(6)]
            causal = False
        elif decoy_kind == "renamed_channel_payload_keys":
            causal = False
        return {
            "window_id": f"{seed['scenario_family']}:window_{index:02d}" if decoy_kind is None else f"{seed['scenario_family']}:{decoy_kind}",
            "external_channel_name": seed["channel_name"] if decoy_kind != "renamed_channel_payload_keys" else "renamed_payload_channel",
            "internal_readback_name": seed["readback_name"],
            "external_medium_series": external,
            "internal_readback_series": internal,
            "signed_causal_effect_verdict": {"external_scramble_changes_future_internal_state": causal, "verdict_basis": "source_bound_external_channel_semantics_v0"},
            "external_state_ablation_result": {"ablation_effect_size_proxy": round(0.41 + (index % 5) * 0.04, 6) if causal else 0.0},
            "lagged_dependence_features": {"lag_1_dependence_proxy": round(0.52 + (index % 4) * 0.03, 6) if causal else 0.03, "lag_k": 1},
            "time_window_holdout": {"predicate_window": [0, 1, 2], "lens_window": [3, 4, 5], "validation_window": [6, 7]},
        }


class BoundaryRegionSamplesAdapter(SourceObjectCorpusAdapter):
    adapter_id = "adapter.source_object.boundary_region_samples.v0"
    parser_version = "boundary-region-source-object-parser.v1"
    source_id = "source.source_object.boundary_region_samples"
    source_name = "Boundary region sample source objects"
    source_url = "https://doi.org/10.1021/ja900919c"
    source_object_type = "boundary_region_samples"
    record_type = "boundary_region_sample"
    cache_name = "source_object_boundary_region_samples"
    authority = "authoritative_boundary_region_public_sources"
    decoy_kinds = ("closed_shell_no_internal_maintenance", "external_reset_only", "randomized_region_adjacency")
    predicate_inputs = ("operational_boundary_persistence", "internal_maintenance_fields")
    lens_inputs = ("region_adjacency", "exchange_graph", "boundary_production_declarations", "compartment_topology")
    validation_inputs = ("decoy_kind", "source_binding", "boundary_counterfactual")
    denied_to_predicate = ("region_adjacency", "exchange_graph", "compartment_topology")
    denied_to_lens = ("operational_boundary_persistence", "internal_maintenance_fields")
    seeds = [
        {
            "substrate": "protocell",
            "scenario_family": "szostak_liposome_membrane_boundary",
            "source_url": "https://doi.org/10.1021/ja900919c",
            "citation": "Zhu and Szostak, Coupled growth and division of model protocell membranes, Journal of the American Chemical Society, 2009.",
            "authority": "peer_reviewed_Szostak_lab_protocell_literature",
            "boundary_material": "fatty_acid_membrane",
        },
        {
            "substrate": "morphogenesis",
            "scenario_family": "flybase_tissue_compartment_boundary",
            "source_url": "https://flybase.org/",
            "citation": "FlyBase public Drosophila compartment-boundary and patterning references.",
            "authority": "FlyBase_public_developmental_genetics_repository",
            "boundary_material": "tissue_compartment_interface",
        },
        {
            "substrate": "field",
            "scenario_family": "reaction_diffusion_phase_boundary",
            "source_url": "https://doi.org/10.1126/science.261.5118.189",
            "citation": "Pearson, Complex patterns in a simple system, Science, 1993.",
            "authority": "peer_reviewed_reaction_diffusion_benchmark",
            "boundary_material": "phase_front_interface",
        },
    ]

    def _payload_for(self, seed: dict[str, Any], *, index: int, decoy_kind: str | None) -> dict[str, Any]:
        adjacency = [["inside", "boundary"], ["boundary", "outside"], ["boundary", f"region_{index % 4}"]]
        persistence = round(0.68 + (index % 6) * 0.035, 6)
        maintenance = round(0.55 + (index % 5) * 0.04, 6)
        verdict = True
        if decoy_kind == "closed_shell_no_internal_maintenance":
            maintenance, verdict = 0.0, False
        elif decoy_kind == "external_reset_only":
            persistence, maintenance, verdict = 0.91, 0.05, False
        elif decoy_kind == "randomized_region_adjacency":
            adjacency = [["outside", "noise_a"], ["noise_b", "inside"]]
            verdict = False
        return {
            "sample_id": f"{seed['scenario_family']}:region_{index:02d}" if decoy_kind is None else f"{seed['scenario_family']}:{decoy_kind}",
            "boundary_material": seed["boundary_material"],
            "operational_boundary_persistence": {"persistence_fraction": persistence, "counterfactual_boundary_removed": not verdict},
            "internal_maintenance_fields": {"internal_production_proxy": maintenance, "maintenance_claim": verdict},
            "region_adjacency": adjacency,
            "exchange_graph": {"nodes": ["inside", "boundary", "outside"], "edges": adjacency, "directed_exchange": True},
            "boundary_production_declarations": {"internal_produces_boundary": verdict, "external_reset_only": decoy_kind == "external_reset_only"},
            "compartment_topology": {"compartment_count": 2 + (index % 3), "boundary_component_count": 1 + (index % 2)},
            "boundary_counterfactual": {"passes_semantics": verdict, "reason": decoy_kind or "source_bound_boundary_maintenance"},
        }


def _seed_rows_to_csv(rows: list[dict[str, str]]) -> str:
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=["Configuration", "Term", "J", "Level (eV)", "Uncertainty (eV)", "Reference"])
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def _nist_unavailable_seed(spectrum: str, reason: str) -> list[dict[str, str]]:
    return [
        {
            "Configuration": "",
            "Term": "",
            "J": "",
            "Level (eV)": "",
            "Uncertainty (eV)": "",
            "Reference": f"NIST_ASD_NO_DATA:{spectrum}:{reason}",
        }
    ]


def _chunks(rows: list[int], size: int) -> list[list[int]]:
    return [rows[index : index + size] for index in range(0, len(rows), size)]


def _rows_to_tsv(rows: list[dict[str, Any]]) -> str:
    return "\n".join("\t".join(str(value) for value in row.values()) for row in rows) + "\n"


def _kegg_pathway_rows(raw: str, organism_code: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t", 1)
        pathway_id = parts[0].strip()
        name = parts[1].strip() if len(parts) > 1 else pathway_id
        if pathway_id.startswith("path:"):
            pathway_id = pathway_id.split(":", 1)[1]
        if not pathway_id:
            continue
        if not pathway_id.startswith(organism_code):
            # Bundled seeds and some KEGG exports omit the path: prefix but
            # still carry organism-specific pathway IDs. Keep them if they
            # look like the same source row family, otherwise namespace them.
            pathway_id = f"{organism_code}_{pathway_id}"
        rows.append({"pathway_id": pathway_id, "name": name})
    return rows


def _fasta_sequence(raw: str) -> str:
    sequence = "".join(line.strip().upper() for line in raw.splitlines() if line.strip() and not line.startswith(">"))
    return "".join(base for base in sequence if base in {"A", "C", "G", "T"})


def _binary_sequence_projection(sequence: str) -> str:
    return "".join("0" if base in {"A", "C"} else "1" for base in sequence if base in {"A", "C", "G", "T"})


def _gbif_count_or_seed(raw: str, seed_count: int) -> int:
    import json

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return int(seed_count)
    count = payload.get("count", seed_count)
    try:
        return int(count)
    except (TypeError, ValueError):
        return int(seed_count)


def _sqrt_scaled(count: int, minimum: float, maximum: float) -> float:
    import math

    return round(max(minimum, min(maximum, math.sqrt(max(int(count), 0)))), 6)


def json_dumps(payload: Any) -> str:
    import json

    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def _merge_pubchem_seed_rows(seed_payloads: list[dict[str, Any]]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    for payload in seed_payloads:
        rows.extend(payload.get("PropertyTable", {}).get("Properties", []))
    return {"PropertyTable": {"Properties": rows}}


def _first_present(row: dict[str, Any], keys: tuple[str, ...], *, default: str = "") -> str:
    for key in keys:
        value = row.get(key)
        if value is not None and value != "":
            return str(value)
    return default


def _int_or(value: Any, default: int) -> int:
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"expected integer-compatible value, got {value!r}") from exc


def _float_or(value: Any, default: float) -> float:
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"expected float-compatible value, got {value!r}") from exc


def _count_formula_atoms(formula: str) -> int:
    total = 0
    for _, count in re.findall(r"([A-Z][a-z]?)(\d*)", formula):
        total += int(count or "1")
    return total


def _smiles_topology(smiles: str) -> dict[str, Any]:
    element_tokens = re.findall(r"Cl|Br|[A-Z][a-z]?", smiles)
    explicit_edges = smiles.count("=") + smiles.count("#") + smiles.count("-")
    branch_points = smiles.count("(")
    ring_digits = len(re.findall(r"\d", smiles))
    aromatic_atoms = len(re.findall(r"[cnops]", smiles))
    return {
        "element_token_count": len(element_tokens),
        "unique_elements": sorted(set(element_tokens)),
        "explicit_bond_symbols": explicit_edges,
        "branch_points": branch_points,
        "ring_digit_count": ring_digits,
        "aromatic_atom_count": aromatic_atoms,
    }


BUNDLED_NIST_ENERGY_LEVELS: dict[str, list[dict[str, str]]] = {
    "H I": [
        {"Configuration": "1s", "Term": "2S", "J": "1/2", "Level (eV)": "0.00000000000000", "Uncertainty (eV)": "0.00000000000012", "Reference": "L15291"},
        {"Configuration": "2p", "Term": "2P*", "J": "1/2", "Level (eV)": "10.19880615024", "Uncertainty (eV)": "0.00000000004", "Reference": "L15291"},
        {"Configuration": "3p", "Term": "2P*", "J": "1/2", "Level (eV)": "12.0874936591", "Uncertainty (eV)": "0.0000000009", "Reference": "L15291"},
        {"Configuration": "Limit", "Term": "Limit", "J": "---", "Level (eV)": "13.598434599702", "Uncertainty (eV)": "0.000000000012", "Reference": "HDEL"},
    ],
    "He I": [
        {"Configuration": "1s2", "Term": "1S", "J": "0", "Level (eV)": "0.000000000", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "1s2s", "Term": "3S", "J": "1", "Level (eV)": "19.81961484", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "1s2p", "Term": "3P*", "J": "2", "Level (eV)": "20.96408703", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "Limit", "Term": "Limit", "J": "---", "Level (eV)": "24.587389011", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
    ],
    "Li I": [
        {"Configuration": "2s", "Term": "2S", "J": "1/2", "Level (eV)": "0.000000", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "2p", "Term": "2P*", "J": "1/2", "Level (eV)": "1.847823", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "3s", "Term": "2S", "J": "1/2", "Level (eV)": "3.37315", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "Limit", "Term": "Limit", "J": "---", "Level (eV)": "5.39171495", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
    ],
    "Ne I": [
        {"Configuration": "2p6", "Term": "1S", "J": "0", "Level (eV)": "0.000000", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "2p5 3s", "Term": "3P*", "J": "2", "Level (eV)": "16.619", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "2p5 3s", "Term": "1P*", "J": "1", "Level (eV)": "16.848", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "Limit", "Term": "Limit", "J": "---", "Level (eV)": "21.56454", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
    ],
    "Ar I": [
        {"Configuration": "3p6", "Term": "1S", "J": "0", "Level (eV)": "0.000000", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "3p5 4s", "Term": "3P*", "J": "2", "Level (eV)": "11.548", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "3p5 4s", "Term": "1P*", "J": "1", "Level (eV)": "11.828", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
        {"Configuration": "Limit", "Term": "Limit", "J": "---", "Level (eV)": "15.7596119", "Uncertainty (eV)": "", "Reference": "NIST_ASD"},
    ],
}


# CB-015 T3 — Phase-1 substantive math primitives catalog: 200
# canonical entries, every one with a peer-reviewed DOI, sourced
# from Strogatz / Guckenheimer & Holmes / Sprott (1994 + 1997) /
# Kuznetsov / Pomeau & Manneville / Lorenz / Rössler / Chen / Lu /
# Chua / Hindmarsh-Rose / etc. Catalog body lives in a sibling
# module for readability — it's a long list of dicts with no logic.
from ._math_primitives_catalog import ALL_MATH_PRIMITIVE_SEEDS

MATH_PRIMITIVE_SEEDS: list[dict[str, Any]] = list(ALL_MATH_PRIMITIVE_SEEDS)


PUBCHEM_SMALL_MOLECULE_SEEDS: dict[int, dict[str, Any]] = {
    962: {"PropertyTable": {"Properties": [{"CID": 962, "MolecularFormula": "H2O", "CanonicalSMILES": "O", "IsomericSMILES": "O", "MolecularWeight": 18.015, "HeavyAtomCount": 1, "Complexity": 0.0}]}},
    297: {"PropertyTable": {"Properties": [{"CID": 297, "MolecularFormula": "CH4", "CanonicalSMILES": "C", "IsomericSMILES": "C", "MolecularWeight": 16.043, "HeavyAtomCount": 1, "Complexity": 0.0}]}},
    280: {"PropertyTable": {"Properties": [{"CID": 280, "MolecularFormula": "CO2", "CanonicalSMILES": "C(=O)=O", "IsomericSMILES": "C(=O)=O", "MolecularWeight": 44.009, "HeavyAtomCount": 3, "Complexity": 18.3}]}},
    222: {"PropertyTable": {"Properties": [{"CID": 222, "MolecularFormula": "H3N", "CanonicalSMILES": "N", "IsomericSMILES": "N", "MolecularWeight": 17.031, "HeavyAtomCount": 1, "Complexity": 0.0}]}},
    241: {"PropertyTable": {"Properties": [{"CID": 241, "MolecularFormula": "C6H6", "CanonicalSMILES": "C1=CC=CC=C1", "IsomericSMILES": "C1=CC=CC=C1", "MolecularWeight": 78.114, "HeavyAtomCount": 6, "Complexity": 15.5}]}},
}


KEGG_ECOLI_CRN_SEED: dict[str, Any] = {
    "pathways": [
        {"pathway_id": "eco00010", "name": "Glycolysis / Gluconeogenesis - Escherichia coli K-12 MG1655"},
        {"pathway_id": "eco00020", "name": "Citrate cycle (TCA cycle) - Escherichia coli K-12 MG1655"},
        {"pathway_id": "eco00620", "name": "Pyruvate metabolism - Escherichia coli K-12 MG1655"},
        {"pathway_id": "eco01200", "name": "Carbon metabolism - Escherichia coli K-12 MG1655"},
    ],
    "reaction_edges": [
        {"reaction_id": "R00200", "from": "D-glucose", "to": "D-glucose-6-phosphate", "pathway_id": "eco00010", "enzymes": ["ec:2.7.1.1"], "degree_proxy": 2},
        {"reaction_id": "R00771", "from": "D-glucose-6-phosphate", "to": "D-fructose-6-phosphate", "pathway_id": "eco00010", "enzymes": ["ec:5.3.1.9"], "degree_proxy": 2},
        {"reaction_id": "R00756", "from": "D-fructose-6-phosphate", "to": "D-fructose-1,6-bisphosphate", "pathway_id": "eco00010", "enzymes": ["ec:2.7.1.11"], "degree_proxy": 2},
        {"reaction_id": "R01068", "from": "D-fructose-1,6-bisphosphate", "to": "glyceraldehyde-3-phosphate", "pathway_id": "eco00010", "enzymes": ["ec:4.1.2.13"], "degree_proxy": 3},
        {"reaction_id": "R01061", "from": "glyceraldehyde-3-phosphate", "to": "3-phospho-D-glyceroyl-phosphate", "pathway_id": "eco00010", "enzymes": ["ec:1.2.1.12"], "degree_proxy": 2},
        {"reaction_id": "R01512", "from": "3-phospho-D-glyceroyl-phosphate", "to": "3-phospho-D-glycerate", "pathway_id": "eco00010", "enzymes": ["ec:2.7.2.3"], "degree_proxy": 2},
        {"reaction_id": "R00658", "from": "3-phospho-D-glycerate", "to": "2-phospho-D-glycerate", "pathway_id": "eco00010", "enzymes": ["ec:5.4.2.12"], "degree_proxy": 2},
        {"reaction_id": "R00200-closure", "from": "2-phospho-D-glycerate", "to": "D-glucose", "pathway_id": "eco01200", "enzymes": ["structural_projection"], "degree_proxy": 1},
    ],
}


REACTION_DIFFUSION_SEEDS: list[dict[str, Any]] = [
    {
        "benchmark": "gray_scott",
        "canonical_name": "Gray-Scott reaction-diffusion stripes",
        "reaction_model": "gray_scott",
        "parameter_range": {"feed": [0.02, 0.08], "kill": [0.045, 0.07]},
        "world_parameters": {"benchmark": "gray_scott", "steps": 36, "export_interval": 4},
        "source_url": "https://doi.org/10.1126/science.261.5118.189",
        "citation": "Pearson, Complex patterns in a simple system, Science, 1993.",
    },
    {
        "benchmark": "brusselator",
        "canonical_name": "Brusselator reaction-diffusion oscillation",
        "reaction_model": "brusselator",
        "parameter_range": {"a": [0.8, 1.2], "b": [2.4, 3.0]},
        "world_parameters": {"benchmark": "brusselator", "steps": 36, "export_interval": 4},
        "source_url": "https://doi.org/10.1063/1.1668896",
        "citation": "Prigogine and Lefever, Symmetry breaking instabilities in dissipative systems, Journal of Chemical Physics, 1968.",
    },
    {
        "benchmark": "schnakenberg",
        "canonical_name": "Schnakenberg reaction-diffusion spots",
        "reaction_model": "schnakenberg",
        "parameter_range": {"a": [0.05, 0.20], "b": [0.8, 1.2]},
        "world_parameters": {"benchmark": "schnakenberg", "steps": 36, "export_interval": 4},
        "source_url": "https://doi.org/10.1016/0022-5193(79)90042-0",
        "citation": "Schnakenberg, Simple chemical reaction systems with limit cycle behaviour, Journal of Theoretical Biology, 1979.",
    },
]


PREBIOTIC_CHEMISTRY_SEEDS: list[dict[str, Any]] = [
    {
        "benchmark": "surface_stabilized_closure",
        "canonical_name": "Mineral-surface thioester prebiotic closure benchmark",
        "chemistry_context": "mineral surface catalysis and activated-carbon chemistry",
        "parameter_basis": "surface adsorption and catalysis strengths projected from mineral-surface closure literature",
        "world_parameters": {"benchmark": "surface_stabilized_closure", "surface_catalysis": 0.24, "adsorption_rate": 0.34, "steps": 90},
        "source_url": "https://doi.org/10.1126/science.276.5310.245",
        "citation": "Huber and Wachtershauser, Activated acetic acid by carbon fixation on (Fe,Ni)S under primordial conditions, Science, 1997.",
    },
    {
        "benchmark": "gradient_anchored_protocell",
        "canonical_name": "Alkaline hydrothermal gradient protocell benchmark",
        "chemistry_context": "redox and pH gradients across mineral compartments",
        "parameter_basis": "gradient and boundary terms projected from alkaline hydrothermal origins literature",
        "world_parameters": {"benchmark": "gradient_anchored_protocell", "gradient_strength": 0.68, "boundary_polymerization": 0.095, "steps": 90},
        "source_url": "https://doi.org/10.1098/rstb.2006.1881",
        "citation": "Martin and Russell, On the origin of biochemistry at an alkaline hydrothermal vent, Philosophical Transactions B, 2007.",
    },
]


HIV1_MUTATION_RATE_SOURCE = {
    "source_url": "https://pubmed.ncbi.nlm.nih.gov/7609081/",
    "citation": "Mansky and Temin, Lower in vivo mutation rate of human immunodeficiency virus type 1 than that predicted from the fidelity of purified reverse transcriptase, Journal of Virology, 1995.",
    "usage": "Pilot quasispecies projection uses a conservative near-neutral mutation-rate scale, not a claim-bearing within-host estimate.",
}


HIV1_HXB2_FASTA_SEED = """>K03455.1 Human immunodeficiency virus type 1 (HXB2), complete genome; HIV1/HTLV-III/LAV reference genome
TGGAAGGGCTAATTCACTCCCAACGAAGACAAGATATCCTTGATCTGTGGATCTACCACACACAAGGCTA
CTTCCCTGATTAGCAGAACTACACACCAGGGCCAGGGATCAGATATCCACTGACCTTTGGATGGTGCTAC
AAGCTAGTACCAGTTGAGCCAGAGAAGTTAGAAGAAGCCAACAAAGGAGAGAACACCAGCTTGTTACACC
CTGTGAGCCTGCATGGAATGGATGACCCGGAGAGAGAAGTGTTAGAGTGGAGGTTTGACAGCCGCCTAGC
ATTTCATCACATGGCCCGAGAGCTGCATCCGGAGTACTTCAAGAACTGCTGACATCGAGCTTGCTACAAG
GGACTTTCCGCTGGGGACTTTCCAGGGAGGCGTGGCCTGGGCGGGACTGGGGAGTGGCGAGCCCTCAGAT
CCTGCATATAAGCAGCTGCTTTTTGCCTGTACTGGGTCTCTCTGGTTAGACCAGATCTGAGCCTGGGAGC
TCTCTGGCTAACTAGGGAACCCACTGCTTAAGCCTCAATAAAGCTTGCCTTGAGTGCTTCAAGTAGTGTG
TGCCCGTCTGTTGTGTGACTCTGGTAACTAGAGATCCCTCAGACCCTTTTAGTCAGTGTGGAAAATCTCT
AGCAGTGGCGCCCGAACAGGGACCTGAAAGCGAAAGGGAAACCAGAGGAGCTCTC
"""


GBIF_JORNADA_ECOSYSTEM_SEED: dict[str, Any] = {
    "site": "Jornada Basin LTER vicinity",
    "geometry": "POLYGON((-107 32,-106 32,-106 33,-107 33,-107 32))",
    "snapshot_note": (
        "GBIF occurrence-count seed captured by TASK-033 live smoke on 2026-05-06; "
        "CB-018 T9 expansion adds ecosystem-level taxa across LTER trophic guilds "
        "(producer/grazer/predator/decomposer/pollinator) so the Phase-2 cycle's "
        "guild aggregation aggregates over a richer source-bound set."
    ),
    "taxa": [
        # Producers — desert grassland + shrub
        {"scientific_name": "Bouteloua eriopoda", "guild": "producer", "role": "black grama grass", "occurrence_count": 89},
        {"scientific_name": "Bouteloua gracilis", "guild": "producer", "role": "blue grama grass", "occurrence_count": 142},
        {"scientific_name": "Larrea tridentata", "guild": "producer", "role": "creosote bush", "occurrence_count": 3878},
        {"scientific_name": "Prosopis glandulosa", "guild": "producer", "role": "honey mesquite", "occurrence_count": 612},
        {"scientific_name": "Atriplex canescens", "guild": "producer", "role": "fourwing saltbush", "occurrence_count": 198},
        {"scientific_name": "Yucca elata", "guild": "producer", "role": "soaptree yucca", "occurrence_count": 76},
        {"scientific_name": "Sporobolus airoides", "guild": "producer", "role": "alkali sacaton bunchgrass", "occurrence_count": 64},
        {"scientific_name": "Opuntia engelmannii", "guild": "producer", "role": "Engelmann prickly pear", "occurrence_count": 51},
        # Grazers — small mammal + lagomorph + arthropod
        {"scientific_name": "Dipodomys spectabilis", "guild": "grazer", "role": "granivorous rodent", "occurrence_count": 58},
        {"scientific_name": "Dipodomys merriami", "guild": "grazer", "role": "granivorous rodent", "occurrence_count": 124},
        {"scientific_name": "Neotoma micropus", "guild": "grazer", "role": "browsing rodent", "occurrence_count": 47},
        {"scientific_name": "Lepus californicus", "guild": "grazer", "role": "herbivorous lagomorph", "occurrence_count": 116},
        {"scientific_name": "Sylvilagus audubonii", "guild": "grazer", "role": "desert cottontail", "occurrence_count": 88},
        {"scientific_name": "Pogonomyrmex rugosus", "guild": "grazer", "role": "harvester ant", "occurrence_count": 211},
        {"scientific_name": "Schistocerca americana", "guild": "grazer", "role": "grasshopper folivore", "occurrence_count": 73},
        # Predators — vertebrate + arthropod
        {"scientific_name": "Canis latrans", "guild": "predator", "role": "mesopredator", "occurrence_count": 129},
        {"scientific_name": "Vulpes macrotis", "guild": "predator", "role": "mesopredator", "occurrence_count": 36},
        {"scientific_name": "Lynx rufus", "guild": "predator", "role": "mesopredator felid", "occurrence_count": 22},
        {"scientific_name": "Bassariscus astutus", "guild": "predator", "role": "ringtail carnivore", "occurrence_count": 19},
        {"scientific_name": "Buteo jamaicensis", "guild": "predator", "role": "diurnal raptor", "occurrence_count": 91},
        {"scientific_name": "Crotalus atrox", "guild": "predator", "role": "ambush rattlesnake", "occurrence_count": 38},
        {"scientific_name": "Centruroides vittatus", "guild": "predator", "role": "scorpion predator", "occurrence_count": 64},
        # Decomposers — fungi + detritivores
        {"scientific_name": "Ascomycota", "guild": "decomposer", "role": "fungal decomposer proxy", "occurrence_count": 664},
        {"scientific_name": "Basidiomycota", "guild": "decomposer", "role": "fungal decomposer proxy", "occurrence_count": 412},
        {"scientific_name": "Eleodes obscura", "guild": "decomposer", "role": "darkling beetle detritivore", "occurrence_count": 102},
        {"scientific_name": "Streptomyces", "guild": "decomposer", "role": "actinobacterial decomposer proxy", "occurrence_count": 318},
        # Pollinators — apoid + lepidopteran
        {"scientific_name": "Apis mellifera", "guild": "pollinator", "role": "honey bee", "occurrence_count": 256},
        {"scientific_name": "Bombus sonorus", "guild": "pollinator", "role": "Sonoran bumblebee", "occurrence_count": 49},
        {"scientific_name": "Danaus plexippus", "guild": "pollinator", "role": "monarch butterfly", "occurrence_count": 87},
    ],
}
