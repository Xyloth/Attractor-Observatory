"""Tests for CB-017 Streamlit duplicate-element-id hotfix.

Symptom: ``World Observatory → math primitives drill-down`` raised
``StreamlitDuplicateElementId`` because ``_render_math_primitives``
emitted ``st.plotly_chart`` per record without a ``key=`` argument.
Streamlit auto-generates element IDs from chart parameters, so
multiple charts whose serialized parameters happen to hash alike
collide.

Fix the *class* of bug, not the symptom: any chart-rendering call
emitted in a loop must carry a deterministic, record-derived
``key=``. This module pins that contract for ``control_room/rooms/``
and ``control_room/components/`` via two AST-walking lint tests
plus a render smoke test on the canonical drill-down helpers.

Tests
-----

* ``test_no_chart_call_in_loop_without_key`` — direct case: any
  ``st.plotly_chart`` (or sibling chart API) emitted inside a
  ``for``/``while`` loop must include a ``key=`` kwarg.
* ``test_no_helper_called_from_loop_emits_chart_without_key`` —
  helper-called-from-loop case: a function that emits a chart
  without ``key=`` must not be invoked from inside another
  function's loop. (Catches the ``_render_atom_card`` pattern that
  the direct lint missed in CB-017.)
* ``test_render_math_primitives_two_records_no_collision`` — render
  smoke: build two distinct math-primitive records (Lorenz +
  Rössler) and confirm ``_render_math_primitives`` does not raise
  ``StreamlitDuplicateElementId``. Skipped if Streamlit isn't
  importable.
* ``test_render_atomic_molecular_two_atoms_no_collision`` — render
  smoke for the helper-in-loop path.

Runtime <0.5s without the render smokes; <2s with them. No network.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


# ---------------------------------------------------------------------------
# AST lint primitives
# ---------------------------------------------------------------------------

# Streamlit chart APIs that:
#   (a) collide on auto-generated element ID when called repeatedly with
#       similarly-shaped parameters, AND
#   (b) accept a ``key=`` keyword argument as the documented fix.
#
# Layout containers (st.columns, st.expander, st.tabs) are excluded because
# they don't accept ``key=`` and don't trigger the duplicate-id error in
# practice. ``st.json``, ``st.code``, ``st.image`` likewise have no ``key``
# parameter; they're handled by uniqueness of the rendered body.
CHART_APIS_WITH_KEY: frozenset[str] = frozenset({
    "plotly_chart",
    "altair_chart",
    "pyplot",
    "bokeh_chart",
    "vega_lite_chart",
    "pydeck_chart",
    "graphviz_chart",
    "line_chart",
    "bar_chart",
    "area_chart",
    "scatter_chart",
    "map",
    "dataframe",
    "data_editor",
})


def _is_streamlit_chart_call(node: ast.AST) -> str | None:
    """Return the chart API name if ``node`` is a call like ``st.plotly_chart(...)``
    or ``streamlit.plotly_chart(...)`` against one of CHART_APIS_WITH_KEY,
    else None."""
    if not isinstance(node, ast.Call):
        return None
    f = node.func
    if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
        if f.value.id in {"st", "streamlit"} and f.attr in CHART_APIS_WITH_KEY:
            return f.attr
    return None


def _has_key_kwarg(call: ast.Call) -> bool:
    return any(kw.arg == "key" for kw in call.keywords)


class _DirectLoopAuditor(ast.NodeVisitor):
    """Find ``st.<chart>(...)`` calls inside ``for``/``while`` loops
    that lack a ``key=`` kwarg."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._loop_depth = 0
        self.findings: list[tuple[Path, int, str]] = []

    def visit_For(self, node: ast.For) -> None:
        self._loop_depth += 1
        self.generic_visit(node)
        self._loop_depth -= 1

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._loop_depth += 1
        self.generic_visit(node)
        self._loop_depth -= 1

    def visit_While(self, node: ast.While) -> None:
        self._loop_depth += 1
        self.generic_visit(node)
        self._loop_depth -= 1

    def visit_Call(self, node: ast.Call) -> None:
        api = _is_streamlit_chart_call(node)
        if api and self._loop_depth > 0 and not _has_key_kwarg(node):
            self.findings.append((self.path, node.lineno, api))
        self.generic_visit(node)


class _HelperFromLoopAuditor(ast.NodeVisitor):
    """Find a function ``f`` that emits a chart without ``key=`` AND is
    called from inside another function's loop. The chart in the helper
    only needs ``key=`` if at least one call site is in a loop."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._fn_stack: list[str] = []
        self._loop_depth = 0
        # fn_name -> [(line, api)] of chart calls without key, recorded only
        # at zero loop depth inside the fn (they need key only if the fn is
        # called from a loop elsewhere — that's what we're hunting).
        self.fn_charts_no_key: dict[str, list[tuple[int, str]]] = {}
        # fn_name -> [(callee_name, lineno, in_loop)]
        self.fn_calls_local: dict[str, list[tuple[str, int, bool]]] = {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._fn_stack.append(node.name)
        self.fn_charts_no_key.setdefault(node.name, [])
        self.fn_calls_local.setdefault(node.name, [])
        prev = self._loop_depth
        self._loop_depth = 0
        self.generic_visit(node)
        self._loop_depth = prev
        self._fn_stack.pop()

    visit_AsyncFunctionDef = visit_FunctionDef  # type: ignore[assignment]

    def visit_For(self, node: ast.For) -> None:
        self._loop_depth += 1
        self.generic_visit(node)
        self._loop_depth -= 1

    def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
        self._loop_depth += 1
        self.generic_visit(node)
        self._loop_depth -= 1

    def visit_While(self, node: ast.While) -> None:
        self._loop_depth += 1
        self.generic_visit(node)
        self._loop_depth -= 1

    def visit_Call(self, node: ast.Call) -> None:
        if not self._fn_stack:
            self.generic_visit(node)
            return
        api = _is_streamlit_chart_call(node)
        if api and not _has_key_kwarg(node) and self._loop_depth == 0:
            self.fn_charts_no_key[self._fn_stack[-1]].append((node.lineno, api))
        if isinstance(node.func, ast.Name):
            self.fn_calls_local[self._fn_stack[-1]].append(
                (node.func.id, node.lineno, self._loop_depth > 0)
            )
        self.generic_visit(node)

    def helper_in_loop_findings(self) -> list[dict]:
        helpers = {fn for fn, charts in self.fn_charts_no_key.items() if charts}
        out: list[dict] = []
        for caller, calls in self.fn_calls_local.items():
            for callee, lineno, in_loop in calls:
                if in_loop and callee in helpers:
                    for cl, api in self.fn_charts_no_key[callee]:
                        out.append({
                            "path": self.path,
                            "caller": caller,
                            "callee": callee,
                            "call_line": lineno,
                            "helper_chart_line": cl,
                            "helper_chart_api": api,
                        })
        return out


def _scanned_files() -> list[Path]:
    roots = [
        ROOT / "control_room" / "rooms",
        ROOT / "control_room" / "components",
    ]
    files: list[Path] = []
    for root in roots:
        if root.exists():
            files.extend(sorted(root.rglob("*.py")))
    return files


# ---------------------------------------------------------------------------
# Test 1 — direct in-loop chart call
# ---------------------------------------------------------------------------


def test_no_chart_call_in_loop_without_key():
    """Pin the canonical CB-017 fix: every chart API call inside a
    ``for``/``while`` loop in ``control_room/rooms/`` or
    ``control_room/components/`` must carry a ``key=`` kwarg.

    Failure surface: a unit test crash beats a Streamlit runtime
    crash on a user's machine when they click the drill-down."""
    findings: list[tuple[Path, int, str]] = []
    for p in _scanned_files():
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        a = _DirectLoopAuditor(p)
        a.visit(tree)
        findings.extend(a.findings)

    if findings:
        msg_lines = [
            "Found chart-API calls in loops without `key=`. "
            "Add a deterministic key derived from the record (record_id, "
            "canonical_name, etc.) to prevent StreamlitDuplicateElementId:",
            "",
        ]
        for path, line, api in findings:
            try:
                rel = path.relative_to(ROOT)
            except ValueError:
                rel = path
            msg_lines.append(f"  {rel}:{line}  st.{api}()  (no key=)")
        pytest.fail("\n".join(msg_lines))


# ---------------------------------------------------------------------------
# Test 2 — helper-called-from-loop
# ---------------------------------------------------------------------------


def test_no_helper_called_from_loop_emits_chart_without_key():
    """The CB-017 ``_render_atom_card`` pattern: a helper emits a
    chart without ``key=``, and the helper is called from a loop in
    another function. Same Streamlit collision as direct-in-loop."""
    findings: list[dict] = []
    for p in _scanned_files():
        try:
            tree = ast.parse(p.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        a = _HelperFromLoopAuditor(p)
        a.visit(tree)
        findings.extend(a.helper_in_loop_findings())

    if findings:
        msg_lines = [
            "Found helper functions that emit chart calls without `key=` "
            "AND are called from inside a loop. Same StreamlitDuplicateElementId "
            "risk as direct-in-loop. Add `key=` inside the helper, derived "
            "from the helper's argument(s):",
            "",
        ]
        for f in findings:
            try:
                rel = f["path"].relative_to(ROOT)
            except ValueError:
                rel = f["path"]
            msg_lines.append(
                f"  {rel}: {f['caller']}() calls {f['callee']}() "
                f"in loop @line {f['call_line']}; helper emits "
                f"st.{f['helper_chart_api']} @line {f['helper_chart_line']} (no key=)"
            )
        pytest.fail("\n".join(msg_lines))


# ---------------------------------------------------------------------------
# Test 3 — render smoke for math primitives (the original failure case)
# ---------------------------------------------------------------------------


def _streamlit_available() -> bool:
    try:
        import streamlit  # noqa: F401
        return True
    except Exception:
        return False


def _make_math_primitive_record(rid: str, canonical: str, primitive_class: str = "ode") -> dict:
    return {
        "record_id": rid,
        "source_id": "src.math_primitives",
        "world_family": "math_primitives",
        "record_type": "math_primitive_summary",
        "canonical_name": canonical,
        "payload": {
            "canonical_name": canonical,
            "primitive_class": primitive_class,
            "dimension": 3,
            "expected_stable_form": "strange_attractor",
            "invariants": ["bounded"],
            "parameters": {"sigma": 10.0, "rho": 28.0, "beta": 8 / 3},
            "state_equation": f"d{canonical}/dt = ...",
        },
        "provenance": {
            "source_url": "https://example.com",
            "retrieval_timestamp": "2026-05-07T17:00:00Z",
            "parser_version": "test",
            "authority": "test",
            "raw_exported": False,
        },
        "license_class": "metadata_only",
        "mode_tag": "exploratory",
        "schema_version": "EmpiricalRecord.v1",
    }


@pytest.mark.skipif(not _streamlit_available(), reason="streamlit not importable in this env")
def test_render_math_primitives_two_records_no_collision():
    """End-to-end: feed two distinct math-primitive records to
    ``_render_math_primitives`` under streamlit.testing.AppTest. The
    pre-fix code would raise StreamlitDuplicateElementId because the
    Plotly figures end up with identical hash signatures when state
    isn't varied. Post-fix, the deterministic key= keeps them apart."""
    try:
        from streamlit.testing.v1 import AppTest
    except Exception:
        pytest.skip("streamlit.testing.v1 not available")

    script = """
import sys
from pathlib import Path
sys.path.insert(0, r"{root}")
from control_room.rooms._world_drilldown import _render_math_primitives

records = [
    {{
        "record_id": "sha256:rec_a_aaaaaaaa",
        "canonical_name": "lorenz",
        "record_type": "math_primitive_summary",
        "payload": {{
            "canonical_name": "lorenz",
            "primitive_class": "ode",
            "dimension": 3,
            "expected_stable_form": "strange_attractor",
            "invariants": ["bounded"],
            "parameters": {{"sigma": 10.0, "rho": 28.0, "beta": 2.667}},
            "state_equation": "dx/dt = sigma*(y-x)",
        }},
    }},
    {{
        "record_id": "sha256:rec_b_bbbbbbbb",
        "canonical_name": "rossler",
        "record_type": "math_primitive_summary",
        "payload": {{
            "canonical_name": "rossler",
            "primitive_class": "ode",
            "dimension": 3,
            "expected_stable_form": "strange_attractor",
            "invariants": ["bounded"],
            "parameters": {{"a": 0.2, "b": 0.2, "c": 5.7}},
            "state_equation": "dx/dt = -y - z",
        }},
    }},
]
_render_math_primitives(records)
""".format(root=str(ROOT).replace("\\", "\\\\"))

    at = AppTest.from_string(script).run(timeout=15)
    # Must NOT raise StreamlitDuplicateElementId. AppTest captures
    # exceptions on at.exception.
    assert not at.exception, (
        f"_render_math_primitives raised: "
        f"{[str(e) for e in at.exception]}"
    )


# ---------------------------------------------------------------------------
# Test 4 — render smoke for atomic_molecular helper-in-loop path
# ---------------------------------------------------------------------------


@pytest.mark.skipif(not _streamlit_available(), reason="streamlit not importable in this env")
def test_render_atomic_molecular_two_atoms_no_collision():
    """Helper-in-loop path: two atom cards, each rendering an energy
    ladder Plotly figure via ``_render_atom_card``. Pre-fix collision
    would raise StreamlitDuplicateElementId."""
    try:
        from streamlit.testing.v1 import AppTest
    except Exception:
        pytest.skip("streamlit.testing.v1 not available")

    script = """
import sys
from pathlib import Path
sys.path.insert(0, r"{root}")
from control_room.rooms._world_drilldown import _render_atomic_molecular

records = [
    {{
        "record_id": "sha256:nist_h_aaaaaaaa",
        "canonical_name": "H I",
        "record_type": "atomic_energy_level_summary",
        "payload": {{
            "element_symbol": "H",
            "spectrum": "H I",
            "ion_stage": "I",
            "ground_state_eV": 0.0,
            "max_observed_level_eV": 13.6,
            "first_level_gaps_eV": [10.2, 1.89, 0.66],
            "energy_level_count": 30,
            "term_count": 12,
        }},
        "provenance": {{"source_url": "https://nist.gov/test"}},
    }},
    {{
        "record_id": "sha256:nist_he_bbbbbbbb",
        "canonical_name": "He I",
        "record_type": "atomic_energy_level_summary",
        "payload": {{
            "element_symbol": "He",
            "spectrum": "He I",
            "ion_stage": "I",
            "ground_state_eV": 0.0,
            "max_observed_level_eV": 24.6,
            "first_level_gaps_eV": [19.8, 1.14, 0.41],
            "energy_level_count": 25,
            "term_count": 9,
        }},
        "provenance": {{"source_url": "https://nist.gov/test"}},
    }},
]
_render_atomic_molecular(records)
""".format(root=str(ROOT).replace("\\", "\\\\"))

    at = AppTest.from_string(script).run(timeout=15)
    assert not at.exception, (
        f"_render_atomic_molecular raised: "
        f"{[str(e) for e in at.exception]}"
    )


# ---------------------------------------------------------------------------
# Test 5 — meta: scanner finds chart calls when they exist
# ---------------------------------------------------------------------------


def test_lint_finds_violation_in_synthetic_module(tmp_path):
    """Sanity check for the AST walker: a synthetic module with a
    known violation must produce a finding. Guards against the lint
    silently passing because the scanner stopped working."""
    synthetic = tmp_path / "synth.py"
    synthetic.write_text(
        "import streamlit as st\n"
        "def render(records):\n"
        "    for r in records:\n"
        "        st.plotly_chart(make_fig(r), use_container_width=True)\n",
        encoding="utf-8",
    )
    tree = ast.parse(synthetic.read_text(encoding="utf-8"))
    a = _DirectLoopAuditor(synthetic)
    a.visit(tree)
    assert len(a.findings) == 1
    assert a.findings[0][2] == "plotly_chart"


def test_lint_ignores_chart_with_key(tmp_path):
    """Inverse sanity check: a synthetic module that adds key= must
    NOT produce a finding."""
    synthetic = tmp_path / "synth_keyed.py"
    synthetic.write_text(
        "import streamlit as st\n"
        "def render(records):\n"
        "    for r in records:\n"
        "        st.plotly_chart(make_fig(r), use_container_width=True, key=f'k_{r}')\n",
        encoding="utf-8",
    )
    tree = ast.parse(synthetic.read_text(encoding="utf-8"))
    a = _DirectLoopAuditor(synthetic)
    a.visit(tree)
    assert a.findings == []


def test_lint_helper_walker_finds_synthetic_pattern(tmp_path):
    """Sanity check for the helper-in-loop walker."""
    synthetic = tmp_path / "synth_helper.py"
    synthetic.write_text(
        "import streamlit as st\n"
        "def helper(r):\n"
        "    st.plotly_chart(make_fig(r), use_container_width=True)\n"
        "def caller(records):\n"
        "    for r in records:\n"
        "        helper(r)\n",
        encoding="utf-8",
    )
    tree = ast.parse(synthetic.read_text(encoding="utf-8"))
    a = _HelperFromLoopAuditor(synthetic)
    a.visit(tree)
    findings = a.helper_in_loop_findings()
    assert len(findings) == 1
    assert findings[0]["caller"] == "caller"
    assert findings[0]["callee"] == "helper"
    assert findings[0]["helper_chart_api"] == "plotly_chart"
