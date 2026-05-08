"""Current predicate extraction and structural relations.

The current predicate is the behavior the file currently exposes,
reconstructed from current executable surfaces:

* Public functions/classes (Python files)
* CLI commands (``__main__`` blocks)
* Tests (pytest functions starting with ``test_``)
* Imports of/by other tracked files (cross-file edges)
* Generated artifacts (the report path the file produces)
* Grep-pattern evidence in non-Python files (markdown, JSON, text)
* Runtime references in docs/reports

The extractor uses Python's :mod:`ast` for code surfaces and uses literal
regex matching (no docstrings as authority) for evidence in non-code
files.
"""

from __future__ import annotations

import ast
import re
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

# Mirror of ``project_genealogy.birth.FAMILY_BIRTH_ATOMS`` patterns. Listed
# here so :func:`extract_current` can verify the patterns mechanically
# against current file content and emit `grep`-kinded evidence atoms when
# the patterns hit. This keeps drift atom-kind matching honest for
# non-Python files (markdown, JSON, text) where AST surfaces don't apply.
GREP_EVIDENCE_PATTERNS: dict[str, list[tuple[str, str]]] = {
    "doctrine": [
        ("doctrine_id_present", r"D\d{1,2}(?:\.\d)?"),
        ("ratified_or_binding", r"ratified|binding|enforced"),
    ],
    "method": [
        ("method_term_present", r"method|prereg|audit|locked"),
    ],
    "report": [
        ("provenance_present", r"content_hash|evidence_private|generated_at|locked_instrument|provenance"),
    ],
    "audit_report": [
        ("audit_binding_present", r"input_manifest_hash|content_hash"),
    ],
    "telemetry": [
        ("telemetry_metadata_present", r"model_name|task_id|estimated_minutes|actual_minutes"),
    ],
    "script": [
        ("script_usage_present", r"Usage|usage|setup|launch|fire|run"),
    ],
    "atlas": [
        ("atlas_versioning_present", r"content_hash|version|registry"),
    ],
    "spec": [
        ("spec_terms_present", r"acceptance|gate|threshold|spec"),
    ],
    "visual": [
        ("visual_term_present", r"Visuals|logo|color"),
    ],
    "ai_os": [
        ("ai_os_terms_present", r"decision|memory|state|builder"),
    ],
    "driver_or_root_doc": [
        ("driver_intent_present", r"Goal|Acceptance|Task|Driver|Mission"),
    ],
    "docs": [
        ("doc_terms_present", r"doctrine|handbook|method|audit"),
    ],
    "paper": [
        ("paper_terms_present", r"falsifier|prereg|method|signed"),
    ],
    "falsifier": [
        ("falsifier_terms_present", r"falsifier|signed|provenance"),
    ],
    "prereg": [
        ("prereg_lock_present", r"content_hash|signed|prereg"),
    ],
    "control_room": [
        ("empty_state_or_render_present", r"render_empty_state|EMPTY_STATE_HTML_MARKER|def render"),
    ],
}


# Detect letter-coupled fix surfaces (try/except, regex/string gates).
LETTER_VS_SPIRIT_PATTERNS = [
    re.compile(r"except\s+\w+(?:\s+as\s+\w+)?:"),
    re.compile(r"except\s*\([^)]+\)\s*(?:as\s+\w+)?:"),
    re.compile(r"if\s+\w+\s*==\s*['\"]\w+['\"]"),
    re.compile(r"if\s+\w+\s+in\s+\{[^}]+\}"),
    re.compile(r"re\.match|re\.search|re\.fullmatch"),
    re.compile(r"startswith\(['\"][^'\"]+['\"]\)"),
    re.compile(r"endswith\(['\"][^'\"]+['\"]\)"),
]


def python_public_symbols(text: str) -> dict[str, list[str]]:
    """Return public function/class names + their import statements."""
    out = {"functions": [], "classes": [], "imports": [], "cli": []}
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return out
    has_main_block = False
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                out["functions"].append(node.name)
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith("_"):
                out["classes"].append(node.name)
        elif isinstance(node, ast.Import):
            for n in node.names:
                out["imports"].append(n.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for n in node.names:
                full = f"{mod}.{n.name}" if mod else n.name
                out["imports"].append(full)
        elif isinstance(node, ast.If):
            test = ast.unparse(node.test) if hasattr(ast, "unparse") else ""
            if "__name__" in test and "__main__" in test:
                has_main_block = True
    if has_main_block:
        out["cli"].append("__main__")
    return out


def find_pytest_functions(text: str) -> list[str]:
    """Return names of pytest-style ``test_*`` functions in the file."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    out: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name.startswith("test_"):
                out.append(node.name)
    return out


def detect_letter_vs_spirit_surfaces(text: str) -> list[dict[str, Any]]:
    """Return matches for letter-coupled patterns with line numbers."""
    surfaces: list[dict[str, Any]] = []
    for i, line in enumerate(text.splitlines(), start=1):
        for pat in LETTER_VS_SPIRIT_PATTERNS:
            if pat.search(line):
                surfaces.append({
                    "line": i,
                    "snippet": line.strip()[:200],
                    "pattern": pat.pattern,
                })
                break
    return surfaces


def detect_doctrine_mentions(text: str) -> list[str]:
    """Return doctrine IDs referenced anywhere in the file."""
    return sorted(set(re.findall(r"\bD\d{1,2}(?:\.\d)?\b", text)))


def detect_class_pattern_matches(text: str) -> list[dict[str, Any]]:
    """Detect mentions of mistake-class patterns.

    Returns a list of ``{class_id, pattern, line}`` records.
    """
    out: list[dict[str, Any]] = []
    patterns = [
        (
            "Class4",
            re.compile(r"if\s+self\.scenario\.benchmark|if\s+benchmark\s*=="),
            "scenario-internal benchmark branching",
        ),
        (
            "Class3",
            re.compile(r"#\s*soft|softened|allow_below"),
            "soft enforcement comments",
        ),
        (
            "Class6",
            re.compile(r"0\.\d{2}\s*\+\s*0\.\d{2}\s*\*"),
            "engineered prediction polynomial",
        ),
        (
            "Class12",
            re.compile(r"placeholder|mock_data|lorem|fake_data", re.IGNORECASE),
            "decorative completeness",
        ),
    ]
    for i, line in enumerate(text.splitlines(), start=1):
        for cls, pat, note in patterns:
            if pat.search(line):
                out.append({
                    "class_id": cls,
                    "line": i,
                    "snippet": line.strip()[:200],
                    "note": note,
                })
                break
    return out


def extract_current(
    repo_root: Path,
    rel_path: str,
    artifact_family: str,
) -> dict[str, Any]:
    """Reconstruct the current section of a dossier."""
    p = repo_root / rel_path
    if not p.is_file():
        return {
            "status": "honest_decline",
            "decline_reason": "current_predicate_not_recoverable",
            "evidence_refs": [],
            "current_predicate": {
                "predicate_id": f"current::{rel_path}",
                "atoms": [],
                "public_symbols": [],
                "commands": [],
                "generated_artifacts": [],
                "observed_doctrine_bindings": [],
                "content_hash": "",
            },
        }
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {
            "status": "honest_decline",
            "decline_reason": "current_predicate_not_recoverable",
            "evidence_refs": [],
            "current_predicate": {
                "predicate_id": f"current::{rel_path}",
                "atoms": [],
                "public_symbols": [],
                "commands": [],
                "generated_artifacts": [],
                "observed_doctrine_bindings": [],
                "content_hash": "",
            },
        }

    line_count = text.count("\n") + (0 if text.endswith("\n") else 1)
    byte_count = len(text.encode("utf-8"))
    public_symbols: list[str] = []
    commands: list[str] = []
    imports_out: list[str] = []
    test_functions: list[str] = []

    if rel_path.endswith(".py"):
        sym = python_public_symbols(text)
        public_symbols = sorted(set(sym["functions"]) | set(sym["classes"]))
        commands = sym["cli"]
        imports_out = sorted(set(sym["imports"]))
        test_functions = find_pytest_functions(text)

    doctrines = detect_doctrine_mentions(text)
    letter_surfaces = detect_letter_vs_spirit_surfaces(text)
    class_matches = detect_class_pattern_matches(text)

    atoms: list[dict[str, Any]] = []
    if public_symbols:
        atoms.append({
            "atom_id": "public_surface_present",
            "statement": (
                f"Module exposes public symbols: {', '.join(public_symbols[:8])}"
                + ("..." if len(public_symbols) > 8 else "")
            ),
            "source_ref": {"kind": "ast_probe", "locator": f"{rel_path}#public_symbols"},
        })
    if commands:
        atoms.append({
            "atom_id": "cli_entry_present",
            "statement": "Module has __main__ entry block.",
            "source_ref": {"kind": "ast_probe", "locator": f"{rel_path}#main"},
        })
    if test_functions:
        atoms.append({
            "atom_id": "pytest_assertions_present",
            "statement": (
                f"Module exposes {len(test_functions)} pytest functions: "
                f"{', '.join(test_functions[:6])}"
                + ("..." if len(test_functions) > 6 else "")
            ),
            "source_ref": {"kind": "ast_probe", "locator": f"{rel_path}#tests"},
        })
    if imports_out:
        atoms.append({
            "atom_id": "imports_reference_internal",
            "statement": (
                f"Module imports: {', '.join(imports_out[:6])}"
                + ("..." if len(imports_out) > 6 else "")
            ),
            "source_ref": {"kind": "ast_probe", "locator": f"{rel_path}#imports"},
        })
    if line_count >= 1:
        atoms.append({
            "atom_id": "file_present_with_size",
            "statement": f"Tracked file with {line_count} lines / {byte_count} bytes at HEAD.",
            "source_ref": {"kind": "file_span", "locator": rel_path},
        })

    # Grep-pattern evidence for the file's family. Emits one current atom
    # per matching pattern with source_ref.kind = 'grep' so drift kind
    # matching works for non-Python files.
    for atom_id, pattern in GREP_EVIDENCE_PATTERNS.get(artifact_family, []):
        try:
            if re.search(pattern, text, re.IGNORECASE):
                atoms.append({
                    "atom_id": atom_id,
                    "statement": f"Pattern /{pattern}/ matches in current file.",
                    "source_ref": {
                        "kind": "grep",
                        "locator": f"{rel_path}#pattern:{pattern}",
                    },
                })
        except re.error:
            continue

    evidence_refs = [
        {
            "ref_id": f"current::{rel_path}::head",
            "kind": "file_span",
            "locator": rel_path,
            "content_hash": "",
            "evidence_private": False,
            "note": "current contents at HEAD",
        },
    ]
    if test_functions:
        evidence_refs.append({
            "ref_id": f"current::{rel_path}::pytest",
            "kind": "test",
            "locator": f"{rel_path}::{','.join(test_functions[:3])}",
            "content_hash": "",
            "evidence_private": False,
            "note": "pytest functions discoverable via collection",
        })

    return {
        "status": "recovered",
        "decline_reason": "",
        "evidence_refs": evidence_refs,
        "current_predicate": {
            "predicate_id": f"current::{rel_path}",
            "atoms": atoms,
            "public_symbols": public_symbols,
            "commands": commands,
            "generated_artifacts": [],  # filled in graph pass
            "observed_doctrine_bindings": doctrines,
            "imports_out": imports_out,
            "test_functions": test_functions,
            "letter_vs_spirit_surfaces": letter_surfaces,
            "class_pattern_matches": class_matches,
            "line_count": line_count,
            "byte_count": byte_count,
            "content_hash": "",
        },
    }
