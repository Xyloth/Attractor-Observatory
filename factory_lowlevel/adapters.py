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


class NISTAtomicSpectraAdapter:
    adapter_id = "adapter.nist_atomic_spectra.energy_levels.v0"
    parser_version = "nist-energy-csv-parser.v1"

    spectra = ("H I", "He I", "Li I", "Ne I", "Ar I")
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
        return self.base_url + "?" + urllib.parse.urlencode(params)

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = True, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        cache_root = Path(cache_dir) / "nist_atomic_spectra"
        cache_root.mkdir(parents=True, exist_ok=True)
        raw_parts: list[str] = []
        warnings: list[str] = []
        retrieval_mode = "network"
        for spectrum in self.spectra:
            cache_path = cache_root / f"{spectrum.replace(' ', '_')}.csv"
            if cache_path.exists() and not force_refresh:
                raw_parts.append(cache_path.read_text(encoding="utf-8-sig"))
                continue
            if allow_network:
                try:
                    with urllib.request.urlopen(self._query_url(spectrum), timeout=timeout) as response:
                        raw = response.read().decode("utf-8", errors="replace")
                    cache_path.write_text(raw, encoding="utf-8")
                    raw_parts.append(raw)
                    continue
                except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
                    warnings.append(f"network_fetch_failed:{spectrum}:{type(exc).__name__}")
            retrieval_mode = "bundled_authoritative_seed"
            seed = BUNDLED_NIST_ENERGY_LEVELS[spectrum]
            raw = _seed_rows_to_csv(seed)
            cache_path.write_text(raw, encoding="utf-8")
            raw_parts.append(raw)
        raw_joined = "\n---SPECTRUM---\n".join(raw_parts)
        source = self.source_definition()
        records = self._parse_records(raw_parts, source)
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
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=warnings)

    def _parse_records(self, raw_parts: list[str], source: SourceDefinition) -> list[EmpiricalRecord]:
        records: list[EmpiricalRecord] = []
        for spectrum, raw in zip(self.spectra, raw_parts):
            reader = csv.DictReader(io.StringIO(raw))
            energies: list[float] = []
            terms: set[str] = set()
            configurations: set[str] = set()
            references: set[str] = set()
            for row in reader:
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
            if not energies:
                continue
            energies = sorted(set(round(value, 12) for value in energies))
            level_gaps = [round(energies[i + 1] - energies[i], 12) for i in range(min(len(energies) - 1, 8))]
            element = spectrum.split()[0]
            payload = {
                "spectrum": spectrum,
                "element_symbol": element,
                "ion_stage": spectrum.split()[1] if len(spectrum.split()) > 1 else "I",
                "energy_level_count": len(energies),
                "ground_state_eV": energies[0],
                "max_observed_level_eV": energies[-1],
                "first_level_gaps_eV": level_gaps,
                "term_count": len(terms),
                "configuration_count": len(configurations),
                "reference_count": len(references),
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
        return records


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
                "PubChem aggregates many source contributors; Campaign 016 stores compact derived molecular "
                "topology summaries with per-record PubChem URLs and no bulk redistribution."
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

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = True, timeout: int = 20, force_refresh: bool = False) -> AdapterResult:
        cache_root = Path(cache_dir) / "pubchem_small_molecules"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        raw_payloads = []
        warnings: list[str] = []
        retrieval_mode = "network"
        property_rows: list[dict[str, Any]] = []
        for name, cid in self.cids.items():
            cache_path = cache_root / f"cid_{cid}.json"
            if cache_path.exists() and not force_refresh:
                raw = cache_path.read_text(encoding="utf-8-sig")
            elif allow_network:
                try:
                    with urllib.request.urlopen(self._query_url(cid), timeout=timeout) as response:
                        raw = response.read().decode("utf-8", errors="replace")
                    cache_path.write_text(raw, encoding="utf-8")
                except Exception as exc:  # pragma: no cover - network fallback is environment dependent.
                    warnings.append(f"pubchem_fetch_failed:{cid}:{type(exc).__name__}")
                    retrieval_mode = "bundled_authoritative_seed"
                    raw = json_dumps(PUBCHEM_SMALL_MOLECULE_SEEDS[cid])
                    cache_path.write_text(raw, encoding="utf-8")
            else:
                retrieval_mode = "bundled_authoritative_seed"
                raw = json_dumps(PUBCHEM_SMALL_MOLECULE_SEEDS[cid])
                cache_path.write_text(raw, encoding="utf-8")
            raw_payloads.append(raw)
            property_rows.append(self._parse_property_row(raw, cid, name))
        records = [self._record_from_row(row, source) for row in property_rows]
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

    def _parse_property_row(self, raw: str, cid: int, fallback_name: str) -> dict[str, Any]:
        import json

        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Malformed PubChem JSON for CID {cid}: {exc}") from exc
        props = payload.get("PropertyTable", {}).get("Properties", [])
        if not isinstance(props, list):
            raise ValueError(f"Malformed PubChem property table for CID {cid}: Properties is not a list")
        if not props:
            props = PUBCHEM_SMALL_MOLECULE_SEEDS[cid]["PropertyTable"]["Properties"]
        row = dict(props[0])
        row.setdefault("CID", cid)
        row.setdefault("Name", fallback_name)
        return row

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
            "molecular_weight": molecular_weight,
            "heavy_atom_count": atom_count,
            "bond_topology_proxy": _smiles_topology(smiles),
            "complexity": complexity,
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


def _seed_rows_to_csv(rows: list[dict[str, str]]) -> str:
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=["Configuration", "Term", "J", "Level (eV)", "Uncertainty (eV)", "Reference"])
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


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
