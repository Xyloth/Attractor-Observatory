"""AST-level D31 read-separation checks."""

from __future__ import annotations

import ast
import builtins
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any, Iterator


CLASSIFIER_MODULE = "formalism.floor_bfg.bfg_v2_classifier"
CLASSIFIER_SHORT = "bfg_v2_classifier"
LENS_FORBIDDEN_KEY = "outcome_summary"
PREDICATE_FORBIDDEN_KEY = "trajectory_geometry"


def assert_d31_read_separation(root: str | Path = ".") -> dict[str, Any]:
    root = Path(root)
    lens_path = root / "formalism" / "floor_bfg" / "lenses.py"
    predicate_paths = [
        root / "formalism" / "motif_contracts" / "predicates" / "floor_connectivity.py",
        root / "formalism" / "motif_contracts" / "predicates" / "floor_connectivity_bfg_v2.py",
    ]
    join_path = root / "formalism" / "floor_bfg" / "floor_join.py"
    failures: list[str] = []
    lens_tree = _parse(lens_path)
    if _imports_module(lens_tree, CLASSIFIER_MODULE, CLASSIFIER_SHORT):
        failures.append("floor BFG lens module imports the preprocessing classifier")
    if _references_forbidden_surface(lens_tree, LENS_FORBIDDEN_KEY):
        failures.append("floor BFG lens module reads or names outcome_summary")
    for path in predicate_paths:
        tree = _parse(path)
        if _references_forbidden_surface(tree, PREDICATE_FORBIDDEN_KEY):
            failures.append(f"{path.as_posix()} reads or names trajectory_geometry")
    if not join_path.exists():
        failures.append("floor_join.py missing; predicate/lens join must be isolated")
    else:
        join_tree = _parse(join_path)
        if not any(isinstance(node, ast.FunctionDef) and node.name == "join_unit_outputs" for node in ast.walk(join_tree)):
            failures.append("floor_join.py does not expose join_unit_outputs")
    return {
        "schema": "D31ReadSeparationAudit.v1",
        "passed": not failures,
        "failures": failures,
        "evidence_private": True,
        "implementation_path_status": "private_unshipped",
        "private_boundary_reason": "D29: formalism implementation modules are held outside the public branch; this audit records the private executable path names without claiming public-runnable evidence.",
        "lens_module": str(lens_path.as_posix()),
        "predicate_modules": [str(path.as_posix()) for path in predicate_paths],
        "join_module": str(join_path.as_posix()),
    }


def _parse(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def _imports_module(tree: ast.AST, module_name: str, short_name: str) -> bool:
    consts = _constant_string_bindings(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == module_name or alias.name.endswith("." + short_name) or alias.name == short_name:
                    return True
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module == module_name or module.endswith("." + short_name) or module == short_name:
                return True
            for alias in node.names:
                if alias.name == short_name:
                    return True
        elif isinstance(node, ast.Call):
            func_name = _call_name(node.func)
            args = [_static_string(arg, consts) for arg in node.args]
            if func_name in {"importlib.import_module", "__import__"}:
                if args and _module_matches(args[0], module_name, short_name):
                    return True
            if func_name == "getattr" and len(args) >= 2:
                if _module_matches(args[0], module_name, short_name) or args[1] == short_name:
                    return True
    return False


def _references_forbidden_surface(tree: ast.AST, needle: str) -> bool:
    consts = _constant_string_bindings(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and needle in node.id:
            return True
        if isinstance(node, ast.Attribute) and needle in node.attr:
            return True
        if isinstance(node, ast.Subscript) and _static_string(node.slice, consts) == needle:
            return True
        if isinstance(node, ast.Call) and _call_name(node.func) == "getattr":
            if len(node.args) >= 2 and _static_string(node.args[1], consts) == needle:
                return True
        value = _static_string(node, consts)
        if value and needle in value:
            return True
    return False


def _constant_string_bindings(tree: ast.AST) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            value = _static_string(node.value, bindings)
            if value is None:
                continue
            for target in node.targets:
                if isinstance(target, ast.Name):
                    bindings[target.id] = value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            value = _static_string(node.value, bindings) if node.value is not None else None
            if value is not None:
                bindings[node.target.id] = value
    return bindings


def _static_string(node: ast.AST | None, bindings: dict[str, str]) -> str | None:
    if node is None:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return bindings.get(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _static_string(node.left, bindings)
        right = _static_string(node.right, bindings)
        if left is not None and right is not None:
            return left + right
    if isinstance(node, ast.JoinedStr):
        parts: list[str] = []
        for value in node.values:
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                parts.append(value.value)
            elif isinstance(value, ast.FormattedValue):
                formatted = _static_string(value.value, bindings)
                if formatted is None:
                    return None
                parts.append(formatted)
            else:
                return None
        return "".join(parts)
    if isinstance(node, ast.Subscript):
        return _static_string(node.slice, bindings)
    return None


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def _module_matches(value: str | None, module_name: str, short_name: str) -> bool:
    if value is None:
        return False
    return value == module_name or value.endswith("." + short_name) or value == short_name


@contextmanager
def d31_import_denylist() -> Iterator[None]:
    """Deny runtime classifier imports in lens-runner probes."""

    original_import = builtins.__import__

    def guarded_import(name: str, globals_: dict[str, Any] | None = None, locals_: dict[str, Any] | None = None, fromlist: tuple[str, ...] = (), level: int = 0) -> ModuleType:
        if _module_matches(name, CLASSIFIER_MODULE, CLASSIFIER_SHORT) or CLASSIFIER_SHORT in fromlist:
            raise ImportError("D31 read-separation violation: lens runner attempted classifier import")
        return original_import(name, globals_, locals_, fromlist, level)

    builtins.__import__ = guarded_import
    try:
        yield
    finally:
        builtins.__import__ = original_import
