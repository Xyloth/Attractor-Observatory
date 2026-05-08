"""Birth predicate reconstruction.

A birth predicate is the formal promise a file was created to satisfy. The
spec's source-priority chain (per §"Pushback 1"):

1. Explicit ticket/campaign brief cited in the creating commit, BUILD_LOG
   entry, or file header.
2. Parent file's predicate plus the rename/split rationale (renames or
   copies).
3. Generator's predicate plus the generated artifact contract.
4. ``birth.status = honest_decline`` if no predicate can be reconstructed.

This module:
* Reads the file's first-seen commit via ``git log --diff-filter=A --follow``.
* Pulls the commit message body.
* Looks for ticket/campaign/driver IDs in the commit message and the
  BUILD_LOG.
* For Python files, extracts the module docstring as a candidate
  birth-predicate-statement source (hint, not proof — current predicate
  must still cite executable evidence).
* Returns predicate atoms that cite source refs.

All atoms record :class:`evidence_ref` shapes so dossiers can reproduce
the lookup.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# Pattern: TASK-XYZ-NNN, CODEX_NNN, DX-NNN, CB-NNN, campaign_NNN, etc.
TICKET_RE = re.compile(
    r"\b("
    r"TASK[-_][A-Z0-9]+(?:[-_][A-Z0-9]+)*"
    r"|CODEX[_-][A-Z0-9]+(?:[-_][A-Z0-9]+)*"
    r"|DX[-_]\d{3,}"
    r"|CB[-_]\d{3,}"
    r"|CAMPAIGN[-_]\d+"
    r"|campaign_\d{3}"
    r"|PG[-_]\d{3,}"
    r"|MS\d+"
    r")\b",
    re.IGNORECASE,
)

DOCTRINE_RE = re.compile(r"\bD\d{1,2}(?:\.\d)?\b")


def _git(*args: str) -> str:
    out = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=False,
    )
    return out.stdout


def first_commit_for_file(rel_path: str) -> dict[str, str] | None:
    """Return the first-seen commit for a tracked file, with --follow.

    Uses ``git log --diff-filter=A --follow --reverse -- <path>`` to find
    the add commit; returns the oldest add-commit for path-renames.
    """
    out = _git(
        "log",
        "--diff-filter=A",
        "--follow",
        "--reverse",
        "--format=%H%x09%aI%x09%an%x09%s",
        "--",
        rel_path,
    )
    lines = [line for line in out.splitlines() if line.strip()]
    if not lines:
        return None
    sha, iso, author, subject = lines[0].split("\t", 3)
    return {
        "commit": sha,
        "date": iso,
        "author": author,
        "subject": subject,
    }


def commit_message(sha: str) -> str:
    return _git("show", "-s", "--format=%B", sha).strip()


def find_renames_for_file(rel_path: str) -> list[str]:
    """Return prior names of the file via git's rename detection."""
    out = _git(
        "log",
        "--follow",
        "--name-status",
        "--format=COMMIT %H",
        "--",
        rel_path,
    )
    parents: set[str] = set()
    for line in out.splitlines():
        if line.startswith("R") and "\t" in line:
            parts = line.split("\t")
            if len(parts) >= 3:
                old_name = parts[1]
                if old_name and old_name != rel_path:
                    parents.add(old_name)
    return sorted(parents)


def python_module_docstring(repo_root: Path, rel_path: str) -> str | None:
    """Return the top-level module docstring of a Python file, or None."""
    if not rel_path.endswith(".py"):
        return None
    try:
        text = (repo_root / rel_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    # Naive but robust: find the first triple-quoted string at module level.
    # Strip leading lines that are blank or `from __future__` etc.
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        s = lines[i].strip()
        if not s or s.startswith("#") or s.startswith("from __future__"):
            i += 1
            continue
        break
    if i >= len(lines):
        return None
    leader = lines[i].lstrip()
    quote = None
    if leader.startswith('"""'):
        quote = '"""'
    elif leader.startswith("'''"):
        quote = "'''"
    else:
        return None
    body = leader[3:]
    # Single-line docstring?
    if quote in body:
        return body[: body.index(quote)].strip() or None
    parts: list[str] = [body]
    for j in range(i + 1, len(lines)):
        ln = lines[j]
        if quote in ln:
            parts.append(ln[: ln.index(quote)])
            return "\n".join(parts).strip() or None
        parts.append(ln)
    return None


def header_marker_block(repo_root: Path, rel_path: str, max_lines: int = 30) -> str:
    """Return the first N non-blank lines of a non-Python file as header text."""
    try:
        text = (repo_root / rel_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    out: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        out.append(s)
        if len(out) >= max_lines:
            break
    return "\n".join(out)


# Per-family atom seeds: the spec's predicate atoms will *partially* be
# inferred from header text and partially derived from family conventions.
# E.g., a ``test`` family file is expected to satisfy at minimum a
# `behavior_assertion_present` atom; a ``doctrine`` family file is expected
# to satisfy a `binding_rule_named` atom.

FAMILY_BIRTH_ATOMS: dict[str, list[dict[str, Any]]] = {
    "test": [
        {
            "atom_id": "behavior_assertion_present",
            "statement": "Module exposes at least one assert-bearing pytest function.",
            "acceptance_evidence_expected": [
                {"kind": "ast_probe", "selector": "function_with_assert"},
            ],
            "forbidden_failure_modes": [
                "test asserts only existence of a module without behavior",
            ],
            "doctrine_bindings_expected": ["D7", "D12", "D29"],
        },
    ],
    "doctrine": [
        {
            "atom_id": "binding_rule_named",
            "statement": "Document declares a binding doctrine rule with a numbered ID and ratification.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": r"D\d{1,2}(?:\.\d)?"},
                {"kind": "grep", "pattern": "ratified|binding|enforced"},
            ],
            "forbidden_failure_modes": [
                "rule named without ratification path",
                "rule weakened by inconvenience",
            ],
            "doctrine_bindings_expected": ["D11", "D29"],
        },
    ],
    "method": [
        {
            "atom_id": "method_documented",
            "statement": "Document records a method, prereg, or audit with locked instruments.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "method|prereg|audit|locked"},
            ],
            "forbidden_failure_modes": [
                "method drifts from named locked instruments without explicit deviation",
            ],
            "doctrine_bindings_expected": ["D11", "D18", "D29"],
        },
    ],
    "factory": [
        {
            "atom_id": "factory_module_exposes_callable",
            "statement": "Module exposes runnable factory components consumed by the daemon/pipeline.",
            "acceptance_evidence_expected": [
                {"kind": "ast_probe", "selector": "public_function_or_class"},
            ],
            "forbidden_failure_modes": [
                "module is a stub (Class 5)",
                "module hardcodes scenario-internal answers (Class 4)",
            ],
            "doctrine_bindings_expected": ["D7", "D14", "D17.5"],
        },
    ],
    "control_room": [
        {
            "atom_id": "control_room_surface_renders",
            "statement": "Module renders a Control Room surface with honest empty state.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "render_empty_state|EMPTY_STATE_HTML_MARKER|render\\("},
            ],
            "forbidden_failure_modes": [
                "decorative completeness (Class 12)",
                "mock data in absence",
            ],
            "doctrine_bindings_expected": ["D22", "D24", "D30"],
        },
    ],
    "report": [
        {
            "atom_id": "report_records_data",
            "statement": "Report serializes structured data for post-hoc analysis.",
            "acceptance_evidence_expected": [
                {"kind": "file_span"},
            ],
            "forbidden_failure_modes": [
                "report contents are mock or placeholder (Class 12)",
            ],
            "doctrine_bindings_expected": ["D11"],
        },
    ],
    "audit_report": [
        {
            "atom_id": "audit_report_traceable",
            "statement": "Audit report is bound to manifest hash and dossier hashes for reproducibility.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "input_manifest_hash|content_hash"},
            ],
            "forbidden_failure_modes": [
                "audit prose without machine-readable claims",
            ],
            "doctrine_bindings_expected": ["D11", "D24"],
        },
    ],
    "audit_instrument": [
        {
            "atom_id": "audit_instrument_executes",
            "statement": "Module is part of the PG-001 audit instrument and exposes a callable surface.",
            "acceptance_evidence_expected": [
                {"kind": "ast_probe", "selector": "public_function_or_class"},
            ],
            "forbidden_failure_modes": [
                "instrument that interpolates findings without source refs (D19)",
            ],
            "doctrine_bindings_expected": ["D11", "D19", "D20"],
        },
    ],
    "telemetry": [
        {
            "atom_id": "telemetry_record_appended",
            "statement": "File appends a telemetry record under a stable schema.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "model_name|task_id|estimated_minutes|actual_minutes"},
            ],
            "forbidden_failure_modes": [
                "telemetry record without identifying metadata",
            ],
            "doctrine_bindings_expected": ["D11"],
        },
    ],
    "script": [
        {
            "atom_id": "script_executes_purposefully",
            "statement": "Script automates a declared developer workflow.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "Usage|usage|setup|launch|fire|run"},
            ],
            "forbidden_failure_modes": [
                "script that wraps unrelated commands without contract",
            ],
            "doctrine_bindings_expected": [],
        },
    ],
    "atlas": [
        {
            "atom_id": "atlas_artifact_versioned",
            "statement": "Atlas/registry artifact carries version or content_hash and references real artifacts.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "content_hash|version|registry"},
            ],
            "forbidden_failure_modes": [
                "atlas artifact citing absent or unshipped paths without private markers",
            ],
            "doctrine_bindings_expected": ["D11", "D23"],
        },
    ],
    "spec": [
        {
            "atom_id": "spec_states_acceptance",
            "statement": "Spec carries acceptance gates with measurable comparisons.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "acceptance|gate|threshold|spec"},
            ],
            "forbidden_failure_modes": [
                "spec gates that are counts without thresholds (D12)",
            ],
            "doctrine_bindings_expected": ["D9", "D12"],
        },
    ],
    "visual": [
        {
            "atom_id": "visual_asset_used",
            "statement": "Visual asset/document is referenced by control_room or public docs.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "Visuals|logo|color"},
            ],
            "forbidden_failure_modes": [],
            "doctrine_bindings_expected": [],
        },
    ],
    "ai_os": [
        {
            "atom_id": "ai_os_state_recorded",
            "statement": "ai_os/ artifact records cross-builder state, decision logs, or memory in a machine-readable form.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "decision|memory|state|builder"},
            ],
            "forbidden_failure_modes": [],
            "doctrine_bindings_expected": ["D11"],
        },
    ],
    "driver_or_root_doc": [
        {
            "atom_id": "driver_states_intent",
            "statement": "Driver/root doc declares a task or campaign intent that other artifacts can cite.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "Goal|Acceptance|Task|Driver|Mission"},
            ],
            "forbidden_failure_modes": [
                "intent without acceptance gates or hand-off",
            ],
            "doctrine_bindings_expected": [],
        },
    ],
    "root_artifact": [
        {
            "atom_id": "root_artifact_serves_repo",
            "statement": "Top-level artifact serves a repo-wide convention (license, citation, ignore, requirements, container).",
            "acceptance_evidence_expected": [],
            "forbidden_failure_modes": [],
            "doctrine_bindings_expected": [],
        },
    ],
    "docs": [
        {
            "atom_id": "doc_serves_handbook",
            "statement": "Doc serves the project handbook (doctrine support, methodology, audit notes).",
            "acceptance_evidence_expected": [],
            "forbidden_failure_modes": [],
            "doctrine_bindings_expected": ["D11"],
        },
    ],
    "paper": [
        {
            "atom_id": "paper_artifact_in_falsifier_or_prereg",
            "statement": "Paper-side artifact (falsifier, prereg, method) carries provenance and signature where required.",
            "acceptance_evidence_expected": [],
            "forbidden_failure_modes": [],
            "doctrine_bindings_expected": ["D17", "D18"],
        },
    ],
    "falsifier": [
        {
            "atom_id": "falsifier_signed_record",
            "statement": "Falsifier record carries provenance and is not deletable for inconvenience (D17).",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "falsifier|signed|provenance"},
            ],
            "forbidden_failure_modes": [
                "falsifier deletion without ratified withdrawal",
            ],
            "doctrine_bindings_expected": ["D17"],
        },
    ],
    "prereg": [
        {
            "atom_id": "prereg_locks_instruments",
            "statement": "Prereg artifact locks basis/lens instruments with a content_hash.",
            "acceptance_evidence_expected": [
                {"kind": "grep", "pattern": "content_hash|signed|prereg"},
            ],
            "forbidden_failure_modes": [
                "post-hoc tuning of locked instruments (D18)",
            ],
            "doctrine_bindings_expected": ["D18"],
        },
    ],
    "other": [
        {
            "atom_id": "tracked_artifact_present",
            "statement": "File is tracked under git but does not match a higher-priority family.",
            "acceptance_evidence_expected": [],
            "forbidden_failure_modes": [],
            "doctrine_bindings_expected": [],
        },
    ],
}


def reconstruct_birth(
    repo_root: Path,
    rel_path: str,
    artifact_family: str,
) -> dict[str, Any]:
    """Reconstruct the birth section of a dossier."""
    first = first_commit_for_file(rel_path)
    if first is None:
        return {
            "status": "honest_decline",
            "decline_reason": "private_history_unavailable",
            "first_seen_commit": "",
            "first_seen_date": "",
            "spawn_ticket": "",
            "birth_cohort_id": "",
            "parent_refs": [],
            "evidence_refs": [],
            "birth_predicate": {
                "predicate_id": f"birth::{rel_path}",
                "atoms": [],
                "acceptance_criteria": [],
                "forbidden_patterns": [],
                "expected_doctrine_bindings": [],
                "content_hash": "",
            },
        }

    msg = commit_message(first["commit"])
    tickets = TICKET_RE.findall(msg)
    spawn_ticket = tickets[0] if tickets else ""
    cohort_id = spawn_ticket or first["commit"]
    parents = find_renames_for_file(rel_path)

    docstring = python_module_docstring(repo_root, rel_path)
    header = ""
    if not docstring:
        header = header_marker_block(repo_root, rel_path)

    # Family-default atoms; statement field is enriched with file-specific
    # text from the docstring/header when available.
    atoms = []
    family_atoms = FAMILY_BIRTH_ATOMS.get(artifact_family, FAMILY_BIRTH_ATOMS["other"])
    for proto in family_atoms:
        atom = dict(proto)
        atom["source_ref"] = {
            "kind": "commit",
            "locator": first["commit"],
            "subject": first["subject"],
            "ticket": spawn_ticket,
        }
        atoms.append(atom)

    # If the docstring contains a ticket reference or a doctrine ID, add
    # an additional file-specific atom.
    if docstring or header:
        text = docstring or header
        text_excerpt = text[:400]
        ticket_in_text = TICKET_RE.findall(text_excerpt)
        doctrines = DOCTRINE_RE.findall(text_excerpt)
        if ticket_in_text or doctrines:
            atoms.append({
                "atom_id": "header_declared_intent",
                "statement": text_excerpt.strip(),
                "source_ref": {
                    "kind": "file_span",
                    "locator": f"{rel_path}#header",
                    "ticket": ticket_in_text[0] if ticket_in_text else spawn_ticket,
                },
                "acceptance_evidence_expected": [],
                "forbidden_failure_modes": [],
                "doctrine_bindings_expected": doctrines,
            })

    evidence_refs = [
        {
            "ref_id": f"birth::{rel_path}::commit",
            "kind": "commit",
            "locator": first["commit"],
            "content_hash": "",
            "evidence_private": False,
            "note": first["subject"],
        }
    ]
    if spawn_ticket:
        evidence_refs.append({
            "ref_id": f"birth::{rel_path}::ticket",
            "kind": "ticket",
            "locator": spawn_ticket,
            "content_hash": "",
            "evidence_private": False,
            "note": "ticket id parsed from creating commit subject",
        })
    if docstring:
        evidence_refs.append({
            "ref_id": f"birth::{rel_path}::docstring",
            "kind": "file_span",
            "locator": f"{rel_path}#docstring",
            "content_hash": "",
            "evidence_private": False,
            "note": "module docstring at file head",
        })

    return {
        "status": "recovered",
        "decline_reason": "",
        "first_seen_commit": first["commit"],
        "first_seen_date": first["date"],
        "spawn_ticket": spawn_ticket,
        "birth_cohort_id": cohort_id,
        "parent_refs": [
            {
                "kind": "rename_predecessor",
                "locator": p,
            }
            for p in parents
        ],
        "evidence_refs": evidence_refs,
        "birth_predicate": {
            "predicate_id": f"birth::{rel_path}",
            "atoms": atoms,
            "acceptance_criteria": [
                a.get("statement", "")
                for a in atoms
                if a.get("statement")
            ],
            "forbidden_patterns": sorted({
                m
                for a in atoms
                for m in a.get("forbidden_failure_modes", [])
            }),
            "expected_doctrine_bindings": sorted({
                d
                for a in atoms
                for d in a.get("doctrine_bindings_expected", [])
            }),
            "content_hash": "",
        },
    }
