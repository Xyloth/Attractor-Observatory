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
from dataclasses import dataclass
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
class AdapterResult:
    source: SourceDefinition
    cache_entry: SourceCacheEntry
    records: list[EmpiricalRecord]
    warnings: list[str]


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

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = True, timeout: int = 20) -> AdapterResult:
        cache_root = Path(cache_dir) / "nist_atomic_spectra"
        cache_root.mkdir(parents=True, exist_ok=True)
        raw_parts: list[str] = []
        warnings: list[str] = []
        retrieval_mode = "network"
        for spectrum in self.spectra:
            cache_path = cache_root / f"{spectrum.replace(' ', '_')}.csv"
            if cache_path.exists():
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
            provenance = {
                "source_url": self._query_url(spectrum),
                "source_home": source.url,
                "retrieved_at": utc_now(),
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

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = False, timeout: int = 20) -> AdapterResult:
        del allow_network, timeout
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
            provenance = {
                "doi": seed["doi"],
                "source_url": seed["source_url"],
                "citation": seed["citation"],
                "retrieved_at": utc_now(),
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
    parser_version = "pubchem-pug-rest-property-parser.v1"
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
        props = "MolecularFormula,CanonicalSMILES,IsomericSMILES,MolecularWeight,HeavyAtomCount,Complexity"
        return f"{self.base_url}/{cid}/property/{props}/JSON"

    def fetch(self, cache_dir: str | Path, *, allow_network: bool = True, timeout: int = 20) -> AdapterResult:
        cache_root = Path(cache_dir) / "pubchem_small_molecules"
        cache_root.mkdir(parents=True, exist_ok=True)
        source = self.source_definition()
        raw_payloads = []
        warnings: list[str] = []
        retrieval_mode = "network"
        property_rows: list[dict[str, Any]] = []
        for name, cid in self.cids.items():
            cache_path = cache_root / f"cid_{cid}.json"
            if cache_path.exists():
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
        return AdapterResult(source=source, cache_entry=cache_entry, records=records, warnings=warnings)

    def _parse_property_row(self, raw: str, cid: int, fallback_name: str) -> dict[str, Any]:
        import json

        payload = json.loads(raw)
        props = payload.get("PropertyTable", {}).get("Properties", [])
        if not props:
            props = PUBCHEM_SMALL_MOLECULE_SEEDS[cid]["PropertyTable"]["Properties"]
        row = dict(props[0])
        row.setdefault("CID", cid)
        row.setdefault("Name", fallback_name)
        return row

    def _record_from_row(self, row: dict[str, Any], source: SourceDefinition) -> EmpiricalRecord:
        cid = int(row["CID"])
        smiles = str(row.get("CanonicalSMILES") or row.get("IsomericSMILES") or "")
        formula = str(row.get("MolecularFormula", ""))
        atom_count = int(row.get("HeavyAtomCount") or _count_formula_atoms(formula))
        payload = {
            "cid": cid,
            "molecular_formula": formula,
            "canonical_smiles": smiles,
            "molecular_weight": float(row.get("MolecularWeight") or 0.0),
            "heavy_atom_count": atom_count,
            "bond_topology_proxy": _smiles_topology(smiles),
            "complexity": float(row.get("Complexity") or 0.0),
            "source_table": "PubChem PUG-REST compound property JSON",
        }
        provenance = {
            "source_url": self._query_url(cid),
            "source_home": source.url,
            "compound_url": f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}",
            "retrieved_at": utc_now(),
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


def _seed_rows_to_csv(rows: list[dict[str, str]]) -> str:
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=["Configuration", "Term", "J", "Level (eV)", "Uncertainty (eV)", "Reference"])
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue()


def json_dumps(payload: Any) -> str:
    import json

    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


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
