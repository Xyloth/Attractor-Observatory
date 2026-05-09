from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from formalism.floor_bfg.read_separation import assert_d31_read_separation, d31_import_denylist  # noqa: E402
from formalism.motif_contracts.adversarial import run_lens_adversarial_controls  # noqa: E402
from formalism.motif_contracts.schema import IndependenceVerdict, derive_independence_verdict  # noqa: E402


def _lens_result(score: float, encoded: dict[str, float]):
    return SimpleNamespace(
        declined=False,
        decline_reason=None,
        prediction_score=score,
        features_used=tuple(sorted(encoded)),
        encoded=encoded,
        trace_id="cb022-fixture",
    )


def test_d31_audit_catches_dynamic_import_and_split_outcome_summary(tmp_path):
    root = tmp_path / "fake_root"
    lens_dir = root / "formalism" / "floor_bfg"
    predicate_dir = root / "formalism" / "motif_contracts" / "predicates"
    lens_dir.mkdir(parents=True)
    predicate_dir.mkdir(parents=True)
    (lens_dir / "lenses.py").write_text(
        "\n".join(
            [
                "import importlib",
                "def cheating_lens(trace):",
                "    module_name = 'formalism.floor_bfg.' + 'bfg_v2_classifier'",
                "    importlib.import_module(module_name)",
                "    key = 'outcome' + '_summary'",
                "    return trace['perturbation_event'][key]",
            ]
        ),
        encoding="utf-8",
    )
    (lens_dir / "floor_join.py").write_text("def join_unit_outputs(predicate_rows, lens_rows):\n    return []\n", encoding="utf-8")
    for name in ("floor_connectivity.py", "floor_connectivity_bfg_v2.py"):
        (predicate_dir / name).write_text("def predicate(trace):\n    return None\n", encoding="utf-8")

    audit = assert_d31_read_separation(root)
    assert audit["passed"] is False
    assert any("imports the preprocessing classifier" in failure for failure in audit["failures"])
    assert any("outcome_summary" in failure for failure in audit["failures"])


def test_d31_runtime_import_hook_blocks_dynamic_classifier_import():
    with d31_import_denylist():
        with pytest.raises(ImportError, match="D31 read-separation violation"):
            __import__("formalism.floor_bfg.bfg_v2_classifier")


def test_metadata_identity_erasure_catches_world_family_cheat():
    trace = {
        "manifest": {"world_family": "crn"},
        "parameter_record": {"family": "crn"},
        "state": [{"state": {"x": 1.0}}, {"state": {"x": 2.0}}, {"state": {"x": 3.0}}, {"state": {"x": 4.0}}],
    }

    def cheating_lens(lens_id, motif_id, candidate):
        score = 1.0 if candidate["manifest"].get("world_family") == "crn" or candidate["parameter_record"].get("family") == "crn" else 0.0
        return _lens_result(score, {"metadata_world_family_score": score})

    result = run_lens_adversarial_controls(cheating_lens, "graph", "motif.repair.draft", trace)
    assert result["passed"] is False
    assert any(axis["axis"] == "metadata_identity_erasure" and not axis["passed"] for axis in result["axes"])


def test_source_object_canonicalization_catches_aliases_ancestors_and_wildcards():
    pred = [{"source_object": "state", "fields_read": ["x"]}]
    assert derive_independence_verdict(pred, [{"source_object": "events", "fields_read": ["type"]}]) == IndependenceVerdict.CLEAN
    assert derive_independence_verdict(pred, [{"source_object": "state", "fields_read": ["y"]}]) == IndependenceVerdict.PARTIAL
    assert derive_independence_verdict(pred, [{"source_object": "state", "fields_read": ["x"]}]) == IndependenceVerdict.BAD
    assert derive_independence_verdict(pred, [{"source_object": "state.x", "fields_read": ["value"]}]) == IndependenceVerdict.BAD
    assert derive_independence_verdict(pred, [{"source_object": "state", "fields_read": ["x.y"]}]) == IndependenceVerdict.BAD
    assert derive_independence_verdict(pred, [{"source_object": "state", "fields_read": ["*"]}]) == IndependenceVerdict.BAD
    assert derive_independence_verdict(pred, [{"source_object": "state", "fields_read": []}]) == IndependenceVerdict.UNKNOWN
    assert derive_independence_verdict(pred, [{"source_object": "", "fields_read": ["x"]}]) == IndependenceVerdict.INVALID


def test_value_label_erasure_catches_numeric_label_channel_cheat():
    trace = {
        "manifest": {"world_family": "field"},
        "state": [
            {"state": {"x": 0.1, "motif_present_label": 1}},
            {"state": {"x": 0.2, "motif_present_label": 1}},
            {"state": {"x": 0.3, "motif_present_label": 1}},
            {"state": {"x": 0.4, "motif_present_label": 1}},
        ],
    }

    def cheating_lens(lens_id, motif_id, candidate):
        labels = [row["state"].get("motif_present_label", 0) for row in candidate["state"]]
        score = sum(labels) / max(len(labels), 1)
        return _lens_result(score, {"motif_present_label_mean": score})

    result = run_lens_adversarial_controls(cheating_lens, "information", "motif.repair.draft", trace)
    assert result["passed"] is False
    assert any(axis["axis"] == "value_label_erasure" and not axis["passed"] for axis in result["axes"])
