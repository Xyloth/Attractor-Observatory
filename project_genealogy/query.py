"""Query API + CLI surface.

Required Python API per the spec's §"Query API Surface":

    GenealogyIndex.load(atlas_path)
    .dossier(path)
    .files(path_glob, artifact_family, doctrine, ticket, drift_status,
           mistake_class, cleanup_candidate, honest_decline)
    .parents(file_path, edge_types)
    .children(file_path, edge_types)
    .siblings(file_path, relation)
    .cohort(ticket=, cohort_id=)
    .orphans(kind)
    .findings(severity, status, mistake_class, doctrine, reproducible)
    .doctrine_collisions(doctrine)
    .depth_outliers(axis, bottom_n)

CLI wrappers:

    python -m project_genealogy.query files --doctrine D26 --drift bad_drift
    python -m project_genealogy.query siblings --file factory_lowlevel/adapters.py
    python -m project_genealogy.query cohort --ticket TASK-SOURCE-OBJ-GEN
    python -m project_genealogy.query orphans --kind no_birth_predicate
    python -m project_genealogy.query findings --mistake-class Class13 --reproducible true

Every result row carries ``path``, ``dossier_path``, ``dossier_hash``, and
the matching evidence field.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from pathlib import Path
from typing import Any, Literal

from project_genealogy import REPORT_DIR


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _bool(s: Any) -> bool | None:
    if s is None:
        return None
    if isinstance(s, bool):
        return s
    if isinstance(s, str):
        return s.lower() in {"1", "true", "yes", "y"}
    return bool(s)


class GenealogyIndex:
    """Read-only index over a published ``ProjectGenealogyAtlas.v1`` file.

    Loads dossier JSON files lazily on demand.
    """

    def __init__(self, atlas: dict[str, Any], repo_root: Path):
        self.atlas = atlas
        self.repo_root = repo_root
        self._dossiers: dict[str, dict[str, Any]] = {}

    @classmethod
    def load(cls, atlas_path: str | Path) -> "GenealogyIndex":
        p = Path(atlas_path)
        atlas = _load_json(p)
        # Repo root: the atlas lives at <repo>/reports/project_genealogy/atlas_*.json
        repo_root = p.parent.parent.parent
        return cls(atlas, repo_root)

    # --- Dossier access -----------------------------------------------------

    def dossier(self, path: str) -> dict[str, Any]:
        if path in self._dossiers:
            return self._dossiers[path]
        for n in self.atlas.get("nodes", []):
            if n["path"] == path:
                p = self.repo_root / n["dossier_path"]
                d = _load_json(p)
                self._dossiers[path] = d
                return d
        raise KeyError(f"unknown path: {path}")

    # --- File queries -------------------------------------------------------

    def files(
        self,
        *,
        path_glob: str | None = None,
        artifact_family: str | None = None,
        doctrine: str | None = None,
        ticket: str | None = None,
        drift_status: str | None = None,
        mistake_class: str | None = None,
        cleanup_candidate: bool | None = None,
        honest_decline: bool | None = None,
    ) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for n in self.atlas.get("nodes", []):
            if path_glob and not fnmatch.fnmatch(n["path"], path_glob):
                continue
            if artifact_family and n["artifact_family"] != artifact_family:
                continue
            if doctrine and doctrine not in n.get("doctrine_refs", []):
                continue
            if ticket and n.get("spawn_ticket") != ticket:
                continue
            if drift_status and n.get("drift_status") != drift_status:
                continue
            if mistake_class and mistake_class not in n.get("mistake_classes", []):
                continue
            if cleanup_candidate is not None and bool(n.get("cleanup_candidate")) != cleanup_candidate:
                continue
            if honest_decline is not None and bool(n.get("honest_decline")) != honest_decline:
                continue
            out.append({
                "path": n["path"],
                "dossier_path": n["dossier_path"],
                "dossier_hash": n["dossier_hash"],
                "artifact_family": n["artifact_family"],
                "spawn_ticket": n.get("spawn_ticket", ""),
                "drift_status": n.get("drift_status", ""),
                "doctrine_refs": n.get("doctrine_refs", []),
                "mistake_classes": n.get("mistake_classes", []),
                "cleanup_candidate_status": n.get("cleanup_candidate_status", "unknown"),
            })
        return out

    # --- Edge queries -------------------------------------------------------

    def _edges_of(self, file_path: str, *, side: Literal["parents", "children"], edge_types: list[str] | None) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for e in self.atlas.get("edges", []):
            if side == "parents" and e["target"] != file_path:
                continue
            if side == "children" and e["source"] != file_path:
                continue
            if edge_types is not None and e["edge_type"] not in edge_types:
                continue
            out.append({
                "path": e["target"] if side == "children" else e["source"],
                "edge_id": e["edge_id"],
                "edge_type": e["edge_type"],
                "evidence_refs": e.get("evidence_refs", []),
                "dossier_path": self._dossier_path_for(e["target"] if side == "children" else e["source"]),
                "dossier_hash": self._dossier_hash_for(e["target"] if side == "children" else e["source"]),
            })
        return out

    def parents(self, file_path: str, *, edge_types: list[str] | None = None) -> list[dict[str, Any]]:
        return self._edges_of(file_path, side="parents", edge_types=edge_types)

    def children(self, file_path: str, *, edge_types: list[str] | None = None) -> list[dict[str, Any]]:
        return self._edges_of(file_path, side="children", edge_types=edge_types)

    def _dossier_path_for(self, p: str) -> str:
        for n in self.atlas.get("nodes", []):
            if n["path"] == p:
                return n["dossier_path"]
        return ""

    def _dossier_hash_for(self, p: str) -> str:
        for n in self.atlas.get("nodes", []):
            if n["path"] == p:
                return n["dossier_hash"]
        return ""

    def siblings(
        self,
        file_path: str,
        *,
        relation: Literal["birth_cohort", "parent", "doctrine"] = "birth_cohort",
    ) -> list[dict[str, Any]]:
        if relation == "birth_cohort":
            for c in self.atlas.get("cohorts", []):
                if file_path in c.get("members", []):
                    return [
                        {
                            "path": m,
                            "dossier_path": self._dossier_path_for(m),
                            "dossier_hash": self._dossier_hash_for(m),
                            "cohort_id": c["cohort_id"],
                            "spawn_ticket": c.get("spawn_ticket", ""),
                        }
                        for m in c["members"]
                        if m != file_path
                    ]
            return []
        if relation == "parent":
            parents = self.parents(file_path, edge_types=["derived_from_file"])
            siblings: list[dict[str, Any]] = []
            for p in parents:
                for child in self.children(p["path"], edge_types=["derived_from_file"]):
                    if child["path"] != file_path:
                        siblings.append(child)
            return siblings
        if relation == "doctrine":
            target_d = set()
            for n in self.atlas.get("nodes", []):
                if n["path"] == file_path:
                    target_d = set(n.get("doctrine_refs", []))
                    break
            return [
                {
                    "path": n["path"],
                    "dossier_path": n["dossier_path"],
                    "dossier_hash": n["dossier_hash"],
                    "shared_doctrine": sorted(target_d & set(n.get("doctrine_refs", []))),
                }
                for n in self.atlas.get("nodes", [])
                if n["path"] != file_path and (set(n.get("doctrine_refs", [])) & target_d)
            ]
        return []

    def cohort(self, *, ticket: str | None = None, cohort_id: str | None = None) -> dict[str, Any]:
        for c in self.atlas.get("cohorts", []):
            if ticket and c.get("spawn_ticket") == ticket:
                return c
            if cohort_id and c.get("cohort_id") == cohort_id:
                return c
        return {"cohort_id": "", "spawn_ticket": ticket or "", "members": []}

    def orphans(
        self,
        *,
        kind: Literal["no_birth_predicate", "no_runtime_refs", "no_parent"] = "no_birth_predicate",
    ) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        nodes = self.atlas.get("nodes", [])
        edges = self.atlas.get("edges", [])
        if kind == "no_birth_predicate":
            for n in nodes:
                if n.get("honest_decline"):
                    out.append({
                        "path": n["path"],
                        "dossier_path": n["dossier_path"],
                        "dossier_hash": n["dossier_hash"],
                        "kind": kind,
                    })
        elif kind == "no_runtime_refs":
            referenced = {e["target"] for e in edges if e["edge_type"] in {"imports", "validates", "cites"}}
            for n in nodes:
                if n["path"] not in referenced:
                    out.append({
                        "path": n["path"],
                        "dossier_path": n["dossier_path"],
                        "dossier_hash": n["dossier_hash"],
                        "kind": kind,
                    })
        elif kind == "no_parent":
            with_parent = {e["target"] for e in edges if e["edge_type"] in {"spawned_by_ticket", "derived_from_file", "generated_by"}}
            for n in nodes:
                if n["path"] not in with_parent:
                    out.append({
                        "path": n["path"],
                        "dossier_path": n["dossier_path"],
                        "dossier_hash": n["dossier_hash"],
                        "kind": kind,
                    })
        return out

    def findings(
        self,
        *,
        severity: str | None = None,
        status: str | None = None,
        mistake_class: str | None = None,
        doctrine: str | None = None,
        reproducible: bool | None = None,
    ) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for n in self.atlas.get("nodes", []):
            try:
                d = self.dossier(n["path"])
            except KeyError:
                continue
            for fnd in d.get("findings", []):
                if severity and fnd.get("severity") != severity:
                    continue
                if status and fnd.get("status") != status:
                    continue
                if mistake_class and mistake_class not in fnd.get("mistake_classes", []):
                    continue
                if doctrine and doctrine not in fnd.get("doctrine_refs", []):
                    continue
                if reproducible is not None:
                    has_reproducer = bool(fnd.get("reproducer", {}).get("command"))
                    if has_reproducer != reproducible:
                        continue
                out.append({
                    "path": n["path"],
                    "dossier_path": n["dossier_path"],
                    "dossier_hash": n["dossier_hash"],
                    "finding_id": fnd["finding_id"],
                    "severity": fnd["severity"],
                    "status": fnd["status"],
                    "claim": fnd["claim"],
                    "mistake_classes": fnd.get("mistake_classes", []),
                    "doctrine_refs": fnd.get("doctrine_refs", []),
                    "reproducer": fnd.get("reproducer", {}),
                })
        return out

    def doctrine_collisions(self, doctrine: str | None = None) -> list[dict[str, Any]]:
        """Return contradicts_doctrine_peer edges (or all implements_same_doctrine)."""
        out: list[dict[str, Any]] = []
        for e in self.atlas.get("edges", []):
            if e["edge_type"] not in {"contradicts_doctrine_peer", "implements_same_doctrine"}:
                continue
            if doctrine and e.get("doctrine_id") != doctrine:
                continue
            out.append({
                "edge_id": e["edge_id"],
                "edge_type": e["edge_type"],
                "source": e["source"],
                "target": e["target"],
                "doctrine_id": e.get("doctrine_id", ""),
                "evidence_refs": e.get("evidence_refs", []),
                "dossier_path": self._dossier_path_for(e["source"]),
                "dossier_hash": self._dossier_hash_for(e["source"]),
                "path": e["source"],
            })
        return out

    def depth_outliers(self, *, axis: str, bottom_n: int = 20) -> list[dict[str, Any]]:
        rows: list[tuple[float, dict[str, Any]]] = []
        for n in self.atlas.get("nodes", []):
            v = n.get("depth", {}).get(axis, {}).get("value")
            if v is None:
                continue
            rows.append((float(v), n))
        rows.sort(key=lambda x: x[0])
        return [
            {
                "path": n["path"],
                "dossier_path": n["dossier_path"],
                "dossier_hash": n["dossier_hash"],
                "axis": axis,
                "value": v,
            }
            for v, n in rows[:bottom_n]
        ]


# ----- CLI -----------------------------------------------------------------


def _default_atlas_path() -> Path:
    return Path("reports/project_genealogy/atlas_latest.json")


def _print_rows(rows: list[dict[str, Any]]) -> None:
    """Write JSON to stdout without forcing the platform locale codec.

    Windows defaults to cp1252 which cannot encode many characters
    present in repo paths and findings; ``ensure_ascii=True`` keeps the
    output portable across locales while preserving JSON validity.
    """
    payload = json.dumps(rows, indent=2, ensure_ascii=True, default=str)
    try:
        print(payload)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(payload.encode("utf-8") + b"\n")


def cli_files(args: argparse.Namespace) -> int:
    idx = GenealogyIndex.load(args.atlas)
    rows = idx.files(
        path_glob=args.path_glob,
        artifact_family=args.artifact_family,
        doctrine=args.doctrine,
        ticket=args.ticket,
        drift_status=args.drift,
        mistake_class=args.mistake_class,
        cleanup_candidate=_bool(args.cleanup_candidate),
        honest_decline=_bool(args.honest_decline),
    )
    _print_rows(rows)
    return 0


def cli_siblings(args: argparse.Namespace) -> int:
    idx = GenealogyIndex.load(args.atlas)
    rows = idx.siblings(args.file, relation=args.relation)
    _print_rows(rows)
    return 0


def cli_parents(args: argparse.Namespace) -> int:
    idx = GenealogyIndex.load(args.atlas)
    edge_types = args.edge_types.split(",") if args.edge_types else None
    rows = idx.parents(args.file, edge_types=edge_types)
    _print_rows(rows)
    return 0


def cli_children(args: argparse.Namespace) -> int:
    idx = GenealogyIndex.load(args.atlas)
    edge_types = args.edge_types.split(",") if args.edge_types else None
    rows = idx.children(args.file, edge_types=edge_types)
    _print_rows(rows)
    return 0


def cli_cohort(args: argparse.Namespace) -> int:
    idx = GenealogyIndex.load(args.atlas)
    coh = idx.cohort(ticket=args.ticket, cohort_id=args.cohort_id)
    payload = json.dumps(coh, indent=2, ensure_ascii=True, default=str)
    try:
        print(payload)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(payload.encode("utf-8") + b"\n")
    return 0


def cli_orphans(args: argparse.Namespace) -> int:
    idx = GenealogyIndex.load(args.atlas)
    rows = idx.orphans(kind=args.kind)
    _print_rows(rows)
    return 0


def cli_findings(args: argparse.Namespace) -> int:
    idx = GenealogyIndex.load(args.atlas)
    rows = idx.findings(
        severity=args.severity,
        status=args.status,
        mistake_class=args.mistake_class,
        doctrine=args.doctrine,
        reproducible=_bool(args.reproducible),
    )
    _print_rows(rows)
    return 0


def cli_doctrine_collisions(args: argparse.Namespace) -> int:
    idx = GenealogyIndex.load(args.atlas)
    rows = idx.doctrine_collisions(doctrine=args.doctrine)
    _print_rows(rows)
    return 0


def cli_depth_outliers(args: argparse.Namespace) -> int:
    idx = GenealogyIndex.load(args.atlas)
    rows = idx.depth_outliers(axis=args.axis, bottom_n=args.bottom_n)
    _print_rows(rows)
    return 0


def make_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="project_genealogy.query", description="PG-001 query CLI")
    p.add_argument("--atlas", default=str(_default_atlas_path()), help="path to atlas JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("files")
    f.add_argument("--path-glob", default=None)
    f.add_argument("--artifact-family", default=None)
    f.add_argument("--doctrine", default=None)
    f.add_argument("--ticket", default=None)
    f.add_argument("--drift", default=None, dest="drift")
    f.add_argument("--mistake-class", default=None, dest="mistake_class")
    f.add_argument("--cleanup-candidate", default=None, dest="cleanup_candidate")
    f.add_argument("--honest-decline", default=None, dest="honest_decline")
    f.set_defaults(func=cli_files)

    s = sub.add_parser("siblings")
    s.add_argument("--file", required=True)
    s.add_argument("--relation", default="birth_cohort", choices=["birth_cohort", "parent", "doctrine"])
    s.set_defaults(func=cli_siblings)

    pa = sub.add_parser("parents")
    pa.add_argument("--file", required=True)
    pa.add_argument("--edge-types", default=None, dest="edge_types")
    pa.set_defaults(func=cli_parents)

    ch = sub.add_parser("children")
    ch.add_argument("--file", required=True)
    ch.add_argument("--edge-types", default=None, dest="edge_types")
    ch.set_defaults(func=cli_children)

    co = sub.add_parser("cohort")
    co.add_argument("--ticket", default=None)
    co.add_argument("--cohort-id", default=None, dest="cohort_id")
    co.set_defaults(func=cli_cohort)

    o = sub.add_parser("orphans")
    o.add_argument("--kind", default="no_birth_predicate", choices=["no_birth_predicate", "no_runtime_refs", "no_parent"])
    o.set_defaults(func=cli_orphans)

    fnd = sub.add_parser("findings")
    fnd.add_argument("--severity", default=None)
    fnd.add_argument("--status", default=None)
    fnd.add_argument("--mistake-class", default=None, dest="mistake_class")
    fnd.add_argument("--doctrine", default=None)
    fnd.add_argument("--reproducible", default=None)
    fnd.set_defaults(func=cli_findings)

    dc = sub.add_parser("doctrine-collisions")
    dc.add_argument("--doctrine", default=None)
    dc.set_defaults(func=cli_doctrine_collisions)

    dx = sub.add_parser("depth-outliers")
    dx.add_argument("--axis", default="predicate_atom_coverage")
    dx.add_argument("--bottom-n", type=int, default=20, dest="bottom_n")
    dx.set_defaults(func=cli_depth_outliers)

    return p


def cli_main(argv: list[str] | None = None) -> int:
    parser = make_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(cli_main())
