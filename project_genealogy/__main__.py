"""CLI dispatch for project_genealogy.

    python -m project_genealogy run-all
    python -m project_genealogy run-prepass
    python -m project_genealogy run-pass1
    python -m project_genealogy run-pass2
    python -m project_genealogy run-pass3
    python -m project_genealogy run-pass4
    python -m project_genealogy query <subcommand>

The ``query`` subcommand delegates to :mod:`project_genealogy.query` so
the documented invocation ``python -m project_genealogy.query files ...``
also works.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from project_genealogy import REPORT_DIR
from project_genealogy.runner import (
    run_all,
    run_pass1,
    run_pass2,
    run_pass3,
    run_pass4,
    run_prepass,
)
from project_genealogy.query import cli_main as query_cli


def _read_manifest(repo_root: Path) -> dict:
    p = repo_root / REPORT_DIR / "input_manifest.json"
    if not p.is_file():
        print("input_manifest.json not found; run run-prepass first", file=sys.stderr)
        sys.exit(2)
    return json.loads(p.read_text(encoding="utf-8"))


def _read_atlas(repo_root: Path) -> dict:
    p = repo_root / REPORT_DIR / "atlas_latest.json"
    if not p.is_file():
        print("atlas_latest.json not found; run run-pass3 first", file=sys.stderr)
        sys.exit(2)
    return json.loads(p.read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    argv = list(argv) if argv is not None else sys.argv[1:]
    if not argv:
        print(__doc__)
        return 0
    cmd = argv[0]
    rest = argv[1:]
    repo_root = Path.cwd()

    if cmd == "run-prepass":
        run_prepass(repo_root)
        return 0
    if cmd == "run-pass1":
        manifest = _read_manifest(repo_root)
        run_pass1(repo_root, manifest)
        return 0
    if cmd == "run-pass2":
        manifest = _read_manifest(repo_root)
        graph, births, currents = run_pass1(repo_root, manifest)
        run_pass2(repo_root, manifest, graph, births, currents)
        return 0
    if cmd == "run-pass3":
        manifest = _read_manifest(repo_root)
        graph, births, currents = run_pass1(repo_root, manifest)
        dossier_index = run_pass2(repo_root, manifest, graph, births, currents)
        run_pass3(repo_root, manifest, graph, dossier_index)
        return 0
    if cmd == "run-pass4":
        manifest = _read_manifest(repo_root)
        graph, births, currents = run_pass1(repo_root, manifest)
        dossier_index = run_pass2(repo_root, manifest, graph, births, currents)
        atlas = run_pass3(repo_root, manifest, graph, dossier_index)
        run_pass4(repo_root, manifest, atlas)
        return 0
    if cmd == "run-all":
        result = run_all(repo_root)
        print(json.dumps(result, indent=2))
        return 0
    if cmd == "query":
        return query_cli(rest)
    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
