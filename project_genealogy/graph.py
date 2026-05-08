"""Structural genealogy — Pass 1.

Builds:

* :class:`StructuralGraph` — typed multigraph between audited files.
* Cohort index keyed on ``birth_cohort_id`` (spawn ticket or first commit).
* Edge types per spec:
    - spawned_by_ticket
    - derived_from_file
    - generated_by
    - imports
    - executes
    - validates
    - cites
    - shares_birth_cohort
    - implements_same_doctrine
    - contradicts_doctrine_peer

Birth and derivation edges are time-directed where possible. Runtime/import
cycles are allowed (typed multigraph, not DAG).
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class StructuralGraph:
    nodes: dict[str, dict[str, Any]] = field(default_factory=dict)
    edges: list[dict[str, Any]] = field(default_factory=list)
    cohorts: dict[str, dict[str, Any]] = field(default_factory=dict)

    def add_node(self, rel_path: str, payload: dict[str, Any]) -> None:
        self.nodes[rel_path] = payload

    def add_edge(self, edge: dict[str, Any]) -> None:
        self.edges.append(edge)

    def add_to_cohort(self, cohort_id: str, member: str, spawn_ticket: str) -> None:
        coh = self.cohorts.setdefault(
            cohort_id,
            {
                "cohort_id": cohort_id,
                "spawn_ticket": spawn_ticket,
                "members": [],
            },
        )
        if member not in coh["members"]:
            coh["members"].append(member)

    def parents(self, rel_path: str, edge_types: list[str] | None = None) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for e in self.edges:
            if e["target"] == rel_path:
                if edge_types is None or e["edge_type"] in edge_types:
                    out.append(e)
        return out

    def children(self, rel_path: str, edge_types: list[str] | None = None) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for e in self.edges:
            if e["source"] == rel_path:
                if edge_types is None or e["edge_type"] in edge_types:
                    out.append(e)
        return out


# ----- Edge construction ----------------------------------------------------


# Maps Python module imports back to file paths in this repo (best-effort).
_LOCAL_PACKAGES: tuple[str, ...] = (
    "control_room",
    "factory_lowlevel",
    "project_genealogy",
    "atlas",
    "Visuals",
    "ai_os",
    "scripts",
    "public_tests",
    # Private modules also resolved if copied via setup_worktree:
    "worlds",
    "motifs",
    "validation",
    "nulls",
    "core",
    "trace",
    "formalism",
    "biology",
    "search",
    "ops",
    "experiments",
    "evidence",
    "tests",
)


def import_to_repo_path(import_name: str, repo_root: Path) -> str | None:
    """Best-effort resolve a module import to a tracked path."""
    parts = import_name.split(".")
    if not parts or parts[0] not in _LOCAL_PACKAGES:
        return None
    candidate = repo_root / Path(*parts[:-1]) / (parts[-1] + ".py")
    if candidate.is_file():
        return str(candidate.relative_to(repo_root)).replace("\\", "/")
    candidate = repo_root / Path(*parts) / "__init__.py"
    if candidate.is_file():
        return str(candidate.relative_to(repo_root)).replace("\\", "/")
    candidate = repo_root / Path(*parts[:-1]) / "__init__.py"
    if candidate.is_file():
        return str(candidate.relative_to(repo_root)).replace("\\", "/")
    return None


def edge_id(prefix: str, source: str, target: str, n: int) -> str:
    return f"{prefix}::{source}->{target}::{n}"


def build_structural_graph(
    repo_root: Path,
    audited_files: list[dict[str, Any]],
    birth_records: dict[str, dict[str, Any]],
    current_records: dict[str, dict[str, Any]],
) -> StructuralGraph:
    """Build the typed multigraph plus cohort index.

    Inputs:
    * ``audited_files``: list of {path, artifact_family} entries from
      the manifest.
    * ``birth_records``: mapping rel_path -> birth payload.
    * ``current_records``: mapping rel_path -> current payload.
    """
    g = StructuralGraph()
    audited_paths = {a["path"] for a in audited_files}

    # Add nodes.
    for entry in audited_files:
        rel = entry["path"]
        g.add_node(rel, {
            "artifact_family": entry["artifact_family"],
            "critical_path": entry.get("critical_path", False),
        })

    # Cohorts via spawn_ticket or first commit.
    for rel, birth in birth_records.items():
        if birth.get("status") != "recovered":
            continue
        cohort_id = birth.get("birth_cohort_id") or birth.get("first_seen_commit") or ""
        ticket = birth.get("spawn_ticket") or ""
        if cohort_id:
            g.add_to_cohort(cohort_id, rel, ticket)

    edge_counter = 0

    # spawned_by_ticket edges (one per file with a recovered birth).
    for rel, birth in birth_records.items():
        if birth.get("status") == "recovered" and birth.get("spawn_ticket"):
            edge_counter += 1
            g.add_edge({
                "edge_id": edge_id("spawned_by_ticket", birth["spawn_ticket"], rel, edge_counter),
                "edge_type": "spawned_by_ticket",
                "source": birth["spawn_ticket"],
                "target": rel,
                "evidence_refs": [
                    {
                        "ref_id": f"spawn::{rel}",
                        "kind": "commit",
                        "locator": birth["first_seen_commit"],
                        "content_hash": "",
                        "evidence_private": False,
                        "note": "first-seen commit subject contained ticket id",
                    }
                ],
                "confidence": "mechanical",
                "created_at_commit": birth["first_seen_commit"],
                "private_boundary": {"evidence_private": False, "reason": ""},
            })

    # derived_from_file edges (renames detected by git --follow).
    for rel, birth in birth_records.items():
        for parent in birth.get("parent_refs", []):
            if parent.get("kind") != "rename_predecessor":
                continue
            old = parent.get("locator")
            if not old:
                continue
            edge_counter += 1
            g.add_edge({
                "edge_id": edge_id("derived_from_file", old, rel, edge_counter),
                "edge_type": "derived_from_file",
                "source": old,
                "target": rel,
                "evidence_refs": [
                    {
                        "ref_id": f"rename::{rel}",
                        "kind": "git_query",
                        "locator": f"git log --follow -- {rel}",
                        "content_hash": "",
                        "evidence_private": False,
                        "note": "rename predecessor detected by git's --follow",
                    }
                ],
                "confidence": "mechanical",
                "created_at_commit": birth.get("first_seen_commit", ""),
                "private_boundary": {"evidence_private": False, "reason": ""},
            })

    # imports edges from current.imports_out.
    for rel, current in current_records.items():
        cp = current.get("current_predicate", {})
        for imp in cp.get("imports_out", []):
            target = import_to_repo_path(imp, repo_root)
            if target is None or target not in audited_paths:
                continue
            if target == rel:
                continue
            edge_counter += 1
            # Boundary: private modules under setup_worktree dirs are
            # listed as non-public; mark the edge boundary.
            private = target.split("/", 1)[0] in (
                "worlds", "motifs", "validation", "nulls", "core",
                "trace", "formalism", "biology", "search", "ops",
                "experiments", "evidence", "tests",
            )
            g.add_edge({
                "edge_id": edge_id("imports", rel, target, edge_counter),
                "edge_type": "imports",
                "source": rel,
                "target": target,
                "evidence_refs": [
                    {
                        "ref_id": f"import::{rel}::{target}",
                        "kind": "ast_probe",
                        "locator": f"{rel}#import:{imp}",
                        "content_hash": "",
                        "evidence_private": private,
                        "note": (
                            "private module import; setup_worktree copies these"
                            if private
                            else "import resolved to tracked file"
                        ),
                    }
                ],
                "confidence": "mechanical",
                "created_at_commit": "",
                "private_boundary": {
                    "evidence_private": private,
                    "reason": "private gitignored module" if private else "",
                },
            })

    # validates edges: tests in public_tests/ that mention an imported repo path.
    for rel, current in current_records.items():
        if not rel.startswith("public_tests/"):
            continue
        cp = current.get("current_predicate", {})
        for imp in cp.get("imports_out", []):
            target = import_to_repo_path(imp, repo_root)
            if target is None or target not in audited_paths:
                continue
            edge_counter += 1
            g.add_edge({
                "edge_id": edge_id("validates", rel, target, edge_counter),
                "edge_type": "validates",
                "source": rel,
                "target": target,
                "evidence_refs": [
                    {
                        "ref_id": f"validates::{rel}::{target}",
                        "kind": "ast_probe",
                        "locator": f"{rel}#tests",
                        "content_hash": "",
                        "evidence_private": False,
                        "note": "public test imports a runtime module",
                    }
                ],
                "confidence": "mechanical",
                "created_at_commit": "",
                "private_boundary": {"evidence_private": False, "reason": ""},
            })

    # shares_birth_cohort edges. Capped to chain edges between sorted
    # consecutive members so cohorts of size N produce N-1 edges instead of
    # N*(N-1)/2. The cohorts table itself enumerates full membership; the
    # edge type marks pairwise connectivity for visualization filters.
    for cohort_id, coh in g.cohorts.items():
        members = sorted(coh["members"])
        if len(members) < 2:
            continue
        for i in range(len(members) - 1):
            a = members[i]
            b = members[i + 1]
            edge_counter += 1
            g.add_edge({
                "edge_id": edge_id("shares_birth_cohort", a, b, edge_counter),
                "edge_type": "shares_birth_cohort",
                "source": a,
                "target": b,
                "evidence_refs": [
                    {
                        "ref_id": f"cohort::{cohort_id}",
                        "kind": "git_query",
                        "locator": f"birth_cohort_id={cohort_id}",
                        "content_hash": "",
                        "evidence_private": False,
                        "note": (
                            "members share spawn_ticket / first-seen commit; "
                            "edge is a chain link between sorted members"
                        ),
                    }
                ],
                "confidence": "mechanical",
                "created_at_commit": "",
                "private_boundary": {"evidence_private": False, "reason": ""},
            })

    # implements_same_doctrine edges (when files mention the same Dxx).
    doctrine_to_files: dict[str, list[str]] = defaultdict(list)
    for rel, current in current_records.items():
        cp = current.get("current_predicate", {})
        for d in cp.get("observed_doctrine_bindings", []):
            doctrine_to_files[d].append(rel)
    for d, files in doctrine_to_files.items():
        if len(files) < 2:
            continue
        # Cap to chain edges (one forward neighbor in sorted order). Full
        # membership for the doctrine is surfaced via the atlas
        # ``doctrine_index``; the edge type carries a representative pair.
        files_sorted = sorted(files)
        for i, a in enumerate(files_sorted):
            for b in files_sorted[i + 1 : i + 2]:
                edge_counter += 1
                g.add_edge({
                    "edge_id": edge_id(f"implements_same_doctrine::{d}", a, b, edge_counter),
                    "edge_type": "implements_same_doctrine",
                    "source": a,
                    "target": b,
                    "evidence_refs": [
                        {
                            "ref_id": f"doctrine::{d}::{a}::{b}",
                            "kind": "grep",
                            "locator": f"both files mention {d}",
                            "content_hash": "",
                            "evidence_private": False,
                            "note": f"shared mention of doctrine {d}",
                        }
                    ],
                    "confidence": "weak",
                    "created_at_commit": "",
                    "private_boundary": {"evidence_private": False, "reason": ""},
                    "doctrine_id": d,
                })

    # cites edges: report family files mentioning a tracked file path.
    citation_re = re.compile(
        r"(reports/[\w./_-]+|"
        r"papers/[\w./_-]+|"
        r"docs/[\w./_-]+|"
        r"control_room/[\w./_-]+|"
        r"factory_lowlevel/[\w./_-]+|"
        r"public_tests/[\w./_-]+)"
    )
    for rel, current in current_records.items():
        family = g.nodes.get(rel, {}).get("artifact_family", "")
        if family not in {"report", "method", "audit_report", "doctrine", "driver_or_root_doc"}:
            continue
        try:
            text = (repo_root / rel).read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        seen: set[str] = set()
        for m in citation_re.finditer(text):
            cit = m.group(0).strip(".,)")
            if cit in audited_paths and cit != rel and cit not in seen:
                seen.add(cit)
                edge_counter += 1
                g.add_edge({
                    "edge_id": edge_id("cites", rel, cit, edge_counter),
                    "edge_type": "cites",
                    "source": rel,
                    "target": cit,
                    "evidence_refs": [
                        {
                            "ref_id": f"cite::{rel}::{cit}",
                            "kind": "grep",
                            "locator": f"{rel}#{cit}",
                            "content_hash": "",
                            "evidence_private": False,
                            "note": "literal path reference in report/method/doc",
                        }
                    ],
                    "confidence": "strong",
                    "created_at_commit": "",
                    "private_boundary": {"evidence_private": False, "reason": ""},
                })

    return g
