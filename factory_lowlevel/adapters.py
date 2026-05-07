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


class NISTAtomicSpectraAdapter:
    adapter_id = "adapter.nist_atomic_spectra.energy_levels.v0"
    parser_version = "nist-energy-csv-parser.v1"

    spectra = tuple(f"{symbol} I" for symbol in ELEMENT_SYMBOLS)
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
    adapter_id = "adapter.pubchem.small_molecule_primitives.v0"
    parser_version = "pubchem-pug-rest-property-parser.v2"
    cid_start = 1
    cid_stop = 2000
    max_records = 1500
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
            "selection_rule": "PubChem CID 1-2000; accepted if nonempty formula/SMILES, 1<=HeavyAtomCount<=64, 1<=MolecularWeight<=500; capped at 1500 records.",
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
        record = self._record_from_seed(source, raw, retrieval_mode)
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
            record_count=1,
            retrieval_mode=retrieval_mode,
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=[record], warnings=warnings)

    def _record_from_seed(self, source: SourceDefinition, raw: str, retrieval_mode: str) -> EmpiricalRecord:
        pathway_count = sum(1 for line in raw.splitlines() if line.strip())
        seed = KEGG_ECOLI_CRN_SEED
        species = sorted({name for edge in seed["reaction_edges"] for name in (edge["from"], edge["to"])})
        initial_state = {name: (8.0 if index == 0 else 1.0) for index, name in enumerate(species)}
        reactions = []
        for index, edge in enumerate(seed["reaction_edges"]):
            degree = float(edge.get("degree_proxy", 1.0))
            reactions.append(
                {
                    "reaction_id": edge["reaction_id"],
                    "reactants": {edge["from"]: 1.0},
                    "products": {edge["to"]: 1.0},
                    "catalysts": [],
                    "source_enzymes": edge.get("enzymes", []),
                    "rate": round(0.0125 * max(degree, 1.0), 6),
                    "rate_constant": round(0.0125 * max(degree, 1.0), 6),
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
            "world_parameters": {
                "initial_state": initial_state,
                "reactions": reactions,
                "projection_basis": "kegg_ecoli_structural_crn_v0",
                "source_undertermination": "KEGG structural topology does not provide rate constants for every edge; rates are deterministic degree-scaled projections and marked exploratory.",
            },
            "source_table": "KEGG REST pathway list and curated KEGG central-metabolism edge summary",
        }
        provenance = {
            "source_url": self.pathway_url,
            "source_home": source.url,
            "retrieved_at": utc_now(),
            "authority": "KEGG organism code eco, E. coli K-12 MG1655",
            "retrieval_mode": retrieval_mode,
            "raw_exported": False,
        }
        record_id = sha256({"source": source.source_id, "organism": "eco", "payload": payload})
        return EmpiricalRecord(
            record_id=record_id,
            source_id=source.source_id,
            world_family="crn",
            record_type="kegg_metabolic_network_summary",
            canonical_name="KEGG E. coli K-12 MG1655 central metabolism CRN projection",
            payload=payload,
            provenance=provenance,
            license_class=source.license_class,
        )


class ReactionDiffusionBenchmarkAdapter:
    adapter_id = "adapter.peer_reviewed.reaction_diffusion_benchmarks.v0"
    parser_version = "reaction-diffusion-benchmark-catalog.v1"

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
        raw = "\n".join(sorted(row["benchmark"] + "\t" + row["source_url"] for row in REACTION_DIFFUSION_SEEDS))
        (cache_root / "benchmarks.tsv").write_text(raw + "\n", encoding="utf-8")
        records = []
        for seed in REACTION_DIFFUSION_SEEDS:
            payload = {
                "benchmark": seed["benchmark"],
                "canonical_name": seed["canonical_name"],
                "reaction_model": seed["reaction_model"],
                "parameter_range": seed["parameter_range"],
                "world_parameters": seed["world_parameters"],
                "source_table": "peer-reviewed reaction-diffusion benchmark catalog",
            }
            provenance = {
                "source_url": seed["source_url"],
                "citation": seed["citation"],
                "retrieved_at": utc_now(),
                "authority": "peer_reviewed_reaction_diffusion_literature",
                "raw_exported": False,
            }
            record_id = sha256({"source": source.source_id, "benchmark": seed["benchmark"], "payload": payload})
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
        raw = "\n".join(sorted(row["benchmark"] + "\t" + row["source_url"] for row in PREBIOTIC_CHEMISTRY_SEEDS))
        (cache_root / "benchmarks.tsv").write_text(raw + "\n", encoding="utf-8")
        records = []
        for seed in PREBIOTIC_CHEMISTRY_SEEDS:
            payload = {
                "benchmark": seed["benchmark"],
                "canonical_name": seed["canonical_name"],
                "chemistry_context": seed["chemistry_context"],
                "parameter_basis": seed["parameter_basis"],
                "world_parameters": seed["world_parameters"],
                "source_table": "peer-reviewed prebiotic chemistry benchmark catalog",
            }
            provenance = {
                "source_url": seed["source_url"],
                "citation": seed["citation"],
                "retrieved_at": utc_now(),
                "authority": "peer_reviewed_prebiotic_chemistry_literature",
                "raw_exported": False,
            }
            record_id = sha256({"source": source.source_id, "benchmark": seed["benchmark"], "payload": payload})
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


class NCBIHIVQuasispeciesAdapter:
    adapter_id = "adapter.ncbi.hiv1.quasispecies_pilot.v0"
    parser_version = "ncbi-hiv1-quasispecies-parser.v1"
    efetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def source_definition(self) -> SourceDefinition:
        return SourceDefinition(
            source_id="source.ncbi.hiv1.reference_quasispecies_pilot",
            name="NCBI HIV-1 reference sequence plus peer-reviewed mutation-rate metadata",
            url="https://www.ncbi.nlm.nih.gov/nuccore/K03455.1",
            format="NCBI E-utilities FASTA plus curated mutation-rate reference",
            license_class="public_domain",
            license_note="NCBI sequence records are public-domain US government data; exported records keep compact derived sequence projections.",
            refresh_cadence="monthly",
            target_world="quasispecies",
            adapter_id=self.adapter_id,
            retrieval_mode_default="dry_run",
        )

    def _query_url(self) -> str:
        params = {"db": "nuccore", "id": "K03455.1", "rettype": "fasta", "retmode": "text"}
        return self.efetch_url + "?" + urllib.parse.urlencode(params)

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = True, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        cache_root = Path(cache_dir) / "ncbi_hiv1_quasispecies"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        cache_path = cache_root / "K03455.1.fasta"
        warnings: list[str] = []
        retrieval_mode = "bundled_authoritative_seed"
        raw = HIV1_HXB2_FASTA_SEED
        if cache_path.exists() and not force_refresh:
            raw = cache_path.read_text(encoding="utf-8-sig")
            retrieval_mode = "cache"
        elif allow_network:
            try:
                with urllib.request.urlopen(self._query_url(), timeout=timeout) as response:
                    raw = response.read().decode("utf-8", errors="replace")
                cache_path.write_text(raw, encoding="utf-8")
                retrieval_mode = "network"
            except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
                warnings.append(f"ncbi_fetch_failed:{type(exc).__name__}")
                cache_path.write_text(raw, encoding="utf-8")
        else:
            cache_path.write_text(raw, encoding="utf-8")
        sequence = _fasta_sequence(raw)
        if not sequence:
            sequence = _fasta_sequence(HIV1_HXB2_FASTA_SEED)
            retrieval_mode = "bundled_authoritative_seed"
        record = self._record_from_sequence(source, sequence, retrieval_mode)
        cache_entry = SourceCacheEntry(
            source_id=source.source_id,
            cache_id=sha256({"source_id": source.source_id, "raw": raw, "mutation_rate": HIV1_MUTATION_RATE_SOURCE}),
            fetched_at=utc_now(),
            url=source.url,
            raw_content_hash=sha256(raw),
            raw_cache_path=str(cache_root),
            parser_version=self.parser_version,
            license_class=source.license_class,
            export_policy="derived_sequence_projection_and_metadata_only",
            record_count=1,
            retrieval_mode=retrieval_mode,
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=[record], warnings=warnings)

    def _record_from_sequence(self, source: SourceDefinition, sequence: str, retrieval_mode: str) -> EmpiricalRecord:
        window = sequence[:240]
        master_sequence = _binary_sequence_projection(window)[:24]
        payload = {
            "accession": "K03455.1",
            "organism": "Human immunodeficiency virus type 1 (HXB2)",
            "sequence_length": len(sequence),
            "sequence_window_start": 1,
            "sequence_window_length": len(window),
            "binary_projection_basis": "A/C -> 0, G/T -> 1 over the first 240 nt of the NCBI reference sequence",
            "mutation_rate_source": HIV1_MUTATION_RATE_SOURCE,
            "world_parameters": {
                "benchmark": "neutral_networks",
                "master_sequence": master_sequence,
                "population_size": 96,
                "mutation_rate": 0.0025,
                "insertion_rate": 0.0005,
                "deletion_rate": 0.0005,
                "neutral_radius": 5,
                "selection_strength": 0.30,
                "landscape_mode": "near_neutral",
                "steps": 48,
                "source_undertermination": "NCBI reference sequence plus literature mutation-rate metadata is a pilot projection, not a sampled within-host quasispecies panel.",
            },
            "source_table": "NCBI E-utilities FASTA and peer-reviewed mutation-rate metadata",
        }
        provenance = {
            "source_url": self._query_url(),
            "source_home": source.url,
            "retrieved_at": utc_now(),
            "authority": "NIH NCBI Nucleotide",
            "retrieval_mode": retrieval_mode,
            "raw_exported": False,
        }
        record_id = sha256({"source": source.source_id, "accession": "K03455.1", "payload": payload})
        return EmpiricalRecord(
            record_id=record_id,
            source_id=source.source_id,
            world_family="quasispecies",
            record_type="ncbi_hiv1_sequence_pilot",
            canonical_name="NCBI HIV-1 HXB2 quasispecies pilot projection",
            payload=payload,
            provenance=provenance,
            license_class=source.license_class,
        )


class GBIFJornadaEcosystemAdapter:
    adapter_id = "adapter.gbif.jornada_basin.ecosystem_pilot.v0"
    parser_version = "gbif-jornada-occurrence-parser.v1"
    base_url = "https://api.gbif.org/v1/occurrence/search"
    geometry = "POLYGON((-107 32,-106 32,-106 33,-107 33,-107 32))"

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
        record = self._record_from_rows(source, rows, retrieval_mode)
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
            record_count=1,
            retrieval_mode=retrieval_mode,
        )
        return AdapterResult(source=source, cache_entry=cache_entry, records=[record], warnings=warnings)

    def _record_from_rows(self, source: SourceDefinition, rows: list[dict[str, Any]], retrieval_mode: str) -> EmpiricalRecord:
        by_guild: dict[str, int] = {}
        for row in rows:
            by_guild[row["guild"]] = by_guild.get(row["guild"], 0) + int(row["occurrence_count"])
        producer = by_guild.get("producer", 0)
        grazer = by_guild.get("grazer", 0)
        predator = by_guild.get("predator", 0)
        decomposer = by_guild.get("decomposer", 0)
        payload = {
            "site": "Jornada Basin LTER vicinity",
            "geometry": self.geometry,
            "taxa": rows,
            "guild_occurrence_counts": by_guild,
            "world_parameters": {
                "benchmark": "may_stability",
                "patch_count": 6,
                "steps": 80,
                "initial_producers": _sqrt_scaled(producer, 12.0, 80.0),
                "initial_grazers": _sqrt_scaled(grazer, 4.0, 28.0),
                "initial_predators": _sqrt_scaled(predator, 1.0, 10.0),
                "initial_decomposers": _sqrt_scaled(decomposer, 3.0, 18.0),
                "initial_resource": 95.0,
                "interaction_strength": 0.50,
                "interaction_radius": 1.45,
                "source_undertermination": "GBIF occurrence counts are observation-availability proxies, not biomass estimates; projection is exploratory and audit-visible.",
            },
            "source_table": "GBIF occurrence search count summaries by guild taxon",
        }
        provenance = {
            "source_url": self.base_url,
            "source_home": source.url,
            "retrieved_at": utc_now(),
            "authority": "GBIF occurrence API plus Jornada Basin LTER site framing",
            "retrieval_mode": retrieval_mode,
            "raw_exported": False,
        }
        record_id = sha256({"source": source.source_id, "site": payload["site"], "payload": payload})
        return EmpiricalRecord(
            record_id=record_id,
            source_id=source.source_id,
            world_family="ecosystem",
            record_type="gbif_ecosystem_occurrence_summary",
            canonical_name="GBIF Jornada Basin ecosystem occurrence pilot",
            payload=payload,
            provenance=provenance,
            license_class=source.license_class,
        )


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
        raw = json_dumps(self.seeds)
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
        for seed in self.seeds:
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
    source_name = "Szostak lab fatty-acid vesicle protocell benchmark metadata"
    source_url = "https://doi.org/10.1038/nature07018"
    target_world = "protocell"
    record_type = "liposome_protocell_benchmark"
    cache_name = "szostak_liposome_protocell"
    authority = "peer_reviewed_Szostak_lab_protocell_literature"
    refresh_cadence = "quarterly"
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
        }
    ]


class FlyBaseMorphogenProfileAdapter(CuratedWorldSeedAdapter):
    adapter_id = "adapter.flybase_vfb.morphogenesis.v0"
    parser_version = "flybase-vfb-morphogen-profile-parser.v1"
    source_id = "source.flybase_vfb.morphogen_profiles"
    source_name = "FlyBase / VirtualFlyBrain Drosophila morphogen-profile exports"
    source_url = "https://virtualflybrain.org/"
    target_world = "morphogenesis"
    record_type = "flybase_morphogen_profile"
    cache_name = "flybase_vfb_morphogenesis"
    authority = "FlyBase_and_VirtualFlyBrain_public_exports"
    refresh_cadence = "monthly"
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
        }
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
    seeds = [
        {
            "canonical_name": "avida_logic_task_copy_loop_trace",
            "source_url": "https://doi.org/10.1038/nature01568",
            "citation": "Lenski, Ofria, Pennock, and Adami, The evolutionary origin of complex features, Nature, 2003.",
            "world_parameters": {"benchmark": "copy_loop", "scenario_id": "W5-avida-copy-loop-projection"},
        }
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
    seeds = [
        {
            "canonical_name": "collective_trail_foraging_behavior_summary",
            "source_url": "https://www.movebank.org/cms/movebank-main",
            "citation": "Movebank public animal movement repository, collective movement study metadata.",
            "world_parameters": {"benchmark": "trail_foraging", "scenario_id": "W7-movebank-trail-foraging", "agent_count": 24},
        }
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
    seeds = [
        {
            "canonical_name": "allen_neural_homeostasis_control_summary",
            "source_url": "https://portal.brain-map.org/",
            "citation": "Allen Brain Atlas public API / Brain Map portal metadata.",
            "world_parameters": {"benchmark": "anticipation", "scenario_id": "W8-allen-anticipation-control"},
        }
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
    seeds = [
        {
            "canonical_name": "biomodels_high_order_reaction_hypergraph",
            "source_url": "https://www.ebi.ac.uk/biomodels/",
            "citation": "EMBL-EBI BioModels public curated computational biology model repository.",
            "world_parameters": {"benchmark": "high_order_closure", "scenario_id": "W10-biomodels-hypergraph"},
        }
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
    seeds = [
        {
            "canonical_name": "endosymbiotic_genome_reduction_mutualism_summary",
            "source_url": "https://www.ncbi.nlm.nih.gov/datasets/",
            "citation": "NCBI Datasets public genome metadata for endosymbiotic bacterial genome reduction examples.",
            "world_parameters": {"benchmark": "stable_mutualism", "scenario_id": "W12-ncbi-endosymbiosis-mutualism"},
        }
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
    seeds = [
        {
            "canonical_name": "physiome_nested_coupling_multiscale_model",
            "source_url": "https://models.physiomeproject.org/",
            "citation": "Physiome Model Repository public multi-scale model metadata.",
            "world_parameters": {"benchmark": "scale_separation", "scenario_id": "W13-physiome-scale-separation"},
        }
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


MATH_PRIMITIVE_SEEDS: list[dict[str, Any]] = [
    {
        "canonical_name": "fixed_point_linear_sink",
        "primitive_class": "fixed_point",
        "dimension": 1,
        "state_equation": "dx/dt = -lambda*x",
        "parameters": {"lambda": 1.0},
        "invariants": ["negative_real_eigenvalue", "single_basin"],
        "expected_stable_form": "asymptotically_stable_fixed_point",
        "doi": "10.1007/978-1-4757-3976-6",
        "source_url": "https://doi.org/10.1007/978-1-4757-3976-6",
        "citation": "Guckenheimer and Holmes, Nonlinear Oscillations, Dynamical Systems, and Bifurcations of Vector Fields.",
    },
    {
        "canonical_name": "hopf_limit_cycle_normal_form",
        "primitive_class": "limit_cycle",
        "dimension": 2,
        "state_equation": "dr/dt = mu*r - r^3; dtheta/dt = omega",
        "parameters": {"mu": 1.0, "omega": 1.0},
        "invariants": ["stable_radius", "phase_translation"],
        "expected_stable_form": "stable_limit_cycle",
        "doi": "10.1007/978-1-4757-3976-6",
        "source_url": "https://doi.org/10.1007/978-1-4757-3976-6",
        "citation": "Guckenheimer and Holmes, Hopf bifurcation normal form.",
    },
    {
        "canonical_name": "quasiperiodic_torus_flow",
        "primitive_class": "torus",
        "dimension": 2,
        "state_equation": "dtheta1/dt = omega1; dtheta2/dt = omega2 with irrational ratio",
        "parameters": {"omega1": 1.0, "omega2": 1.41421356237},
        "invariants": ["angle_wrap", "irrational_frequency_ratio"],
        "expected_stable_form": "quasiperiodic_torus",
        "doi": "10.1007/978-1-4612-1140-2",
        "source_url": "https://doi.org/10.1007/978-1-4612-1140-2",
        "citation": "Katok and Hasselblatt, Introduction to the Modern Theory of Dynamical Systems.",
    },
    {
        "canonical_name": "lorenz_1963_strange_attractor",
        "primitive_class": "strange_attractor",
        "dimension": 3,
        "state_equation": "dx/dt=sigma(y-x); dy/dt=x(rho-z)-y; dz/dt=xy-beta*z",
        "parameters": {"sigma": 10.0, "rho": 28.0, "beta": 2.6666666667},
        "invariants": ["sensitive_dependence", "bounded_absorbing_region"],
        "expected_stable_form": "strange_attractor",
        "doi": "10.1175/1520-0469(1963)020<0130:DNF>2.0.CO;2",
        "source_url": "https://doi.org/10.1175/1520-0469(1963)020%3C0130:DNF%3E2.0.CO;2",
        "citation": "Lorenz, Deterministic Nonperiodic Flow, Journal of the Atmospheric Sciences, 1963.",
    },
    {
        "canonical_name": "rossler_1976_continuous_chaos",
        "primitive_class": "strange_attractor",
        "dimension": 3,
        "state_equation": "dx/dt=-y-z; dy/dt=x+a*y; dz/dt=b+z*(x-c)",
        "parameters": {"a": 0.2, "b": 0.2, "c": 5.7},
        "invariants": ["spiral_band", "folding_return"],
        "expected_stable_form": "strange_attractor",
        "doi": "10.1016/0375-9601(76)90101-8",
        "source_url": "https://doi.org/10.1016/0375-9601(76)90101-8",
        "citation": "Rossler, An Equation for Continuous Chaos, Physics Letters A, 1976.",
    },
    {
        "canonical_name": "sprott_simple_chaotic_flow",
        "primitive_class": "strange_attractor",
        "dimension": 3,
        "state_equation": "example low-dimensional polynomial chaotic flow",
        "parameters": {"family": "Sprott"},
        "invariants": ["low_term_count", "chaotic_flow"],
        "expected_stable_form": "strange_attractor_family",
        "doi": "10.1103/PhysRevE.50.R647",
        "source_url": "https://doi.org/10.1103/PhysRevE.50.R647",
        "citation": "Sprott, Some simple chaotic flows, Physical Review E, 1994.",
    },
]


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
    "snapshot_note": "GBIF occurrence-count seed captured by TASK-033 live smoke on 2026-05-06; counts are observation proxies, not abundance claims.",
    "taxa": [
        {"scientific_name": "Bouteloua eriopoda", "guild": "producer", "role": "black grama grass", "occurrence_count": 89},
        {"scientific_name": "Larrea tridentata", "guild": "producer", "role": "creosote bush", "occurrence_count": 3878},
        {"scientific_name": "Dipodomys spectabilis", "guild": "grazer", "role": "granivorous rodent", "occurrence_count": 58},
        {"scientific_name": "Lepus californicus", "guild": "grazer", "role": "herbivorous lagomorph", "occurrence_count": 116},
        {"scientific_name": "Canis latrans", "guild": "predator", "role": "mesopredator", "occurrence_count": 129},
        {"scientific_name": "Vulpes macrotis", "guild": "predator", "role": "mesopredator", "occurrence_count": 36},
        {"scientific_name": "Ascomycota", "guild": "decomposer", "role": "fungal decomposer proxy", "occurrence_count": 664},
    ],
}
