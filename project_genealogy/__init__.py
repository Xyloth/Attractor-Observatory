"""Project Genealogy PG-001 — source-bound, doctrine-aware genealogy.

Public surfaces:

* :mod:`project_genealogy.manifest` — pre-pass evidence-lock manifest.
* :mod:`project_genealogy.birth` — birth predicate reconstruction.
* :mod:`project_genealogy.current` — current predicate extraction.
* :mod:`project_genealogy.graph` — structural genealogy / atlas builder.
* :mod:`project_genealogy.drift` — drift detection (atom diff).
* :mod:`project_genealogy.depth` — DepthVector.v1.
* :mod:`project_genealogy.probe` — mechanical removal probe.
* :mod:`project_genealogy.coherence` — Project Coherence Report (Pass 4).
* :mod:`project_genealogy.query` — :class:`GenealogyIndex` + CLI.
* :mod:`project_genealogy.schemas` — schema names and version pins.

Entry points:

    python -m project_genealogy run-prepass
    python -m project_genealogy run-pass1
    python -m project_genealogy run-pass2
    python -m project_genealogy run-pass3
    python -m project_genealogy run-pass4
    python -m project_genealogy query <subcommand>

The audit produces machine-authoritative JSON; Markdown is a rendering of
JSON. Deleting any JSON dossier invalidates the corresponding Markdown.
"""

from __future__ import annotations

PG_VERSION = "PG-001"

DOSSIER_SCHEMA = "ProjectGenealogyDossier.v1"
ATLAS_SCHEMA = "ProjectGenealogyAtlas.v1"
COHERENCE_SCHEMA = "ProjectCoherenceReport.v1"
MANIFEST_SCHEMA = "ProjectGenealogyManifest.v1"

REPORT_DIR = "reports/project_genealogy"
DOSSIER_DIR = "reports/project_genealogy/dossiers"

__all__ = [
    "PG_VERSION",
    "DOSSIER_SCHEMA",
    "ATLAS_SCHEMA",
    "COHERENCE_SCHEMA",
    "MANIFEST_SCHEMA",
    "REPORT_DIR",
    "DOSSIER_DIR",
]
