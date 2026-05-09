"""Adversarial invariance controls for MotifContract.v2 predicates and lenses."""

from __future__ import annotations

import copy
from collections.abc import Callable
from typing import Any

from .schema import PredicateResult

Predicate = Callable[[dict[str, Any]], PredicateResult]
LensEvaluator = Callable[[str, str, dict[str, Any]], Any]
Transform = Callable[[dict[str, Any]], dict[str, Any]]

GENERATOR_ID_KEYS = {
    "benchmark",
    "campaign_id",
    "generator_id",
    "implementation_id",
    "scenario_class",
    "scenario_id",
    "world_implementation_id",
}

METADATA_IDENTITY_KEYS = {
    "adapter_id",
    "family",
    "implementation_family",
    "manifest_world_family",
    "parameter_family",
    "record_family",
    "scenario_family",
    "scenario_family_id",
    "source_family",
    "source_id",
    "substrate",
    "substrate_id",
    "world",
    "world_family",
    "world_family_id",
    "world_id",
}

VALUE_LABEL_KEYS = {
    "class",
    "class_id",
    "class_id_numeric",
    "expected_label",
    "label",
    "motif_label",
    "motif_present",
    "motif_present_label",
    "outcome_class",
    "positive",
    "positive_label",
    "scenario_label",
    "target",
    "target_class",
    "target_label",
    "verdict",
}


def _stable_alias(value: str, namespace: str, aliases: dict[str, str]) -> str:
    if value not in aliases:
        aliases[value] = f"{namespace}_{len(aliases):03d}"
    return aliases[value]


def _rename_mapping_keys(obj: Any, namespace: str, aliases: dict[str, str]) -> Any:
    if isinstance(obj, dict):
        return {
            _stable_alias(str(key), namespace, aliases): _rename_mapping_keys(value, namespace, aliases)
            for key, value in obj.items()
        }
    if isinstance(obj, list):
        return [_rename_mapping_keys(item, namespace, aliases) for item in obj]
    return obj


def event_token_rename(trace: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(trace)
    aliases: dict[str, str] = {}
    for event in out.get("events", []) if isinstance(out.get("events"), list) else []:
        if isinstance(event, dict) and "type" in event:
            event["type"] = _stable_alias(str(event["type"]), "evt", aliases)
    return out


def state_key_rename(trace: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(trace)
    aliases: dict[str, str] = {}
    rows = out.get("state", [])
    if not isinstance(rows, list):
        return out
    for row in rows:
        if not isinstance(row, dict):
            continue
        state = row.get("state")
        if isinstance(state, dict):
            row["state"] = {
                _stable_alias(str(key), "state", aliases): value
                for key, value in state.items()
            }
        else:
            for key in list(row.keys()):
                if key == "t_sim":
                    continue
                row[_stable_alias(str(key), "state", aliases)] = row.pop(key)
    return out


def payload_key_rename(trace: dict[str, Any]) -> dict[str, Any]:
    out = copy.deepcopy(trace)
    aliases: dict[str, str] = {}
    for event in out.get("events", []) if isinstance(out.get("events"), list) else []:
        if isinstance(event, dict) and isinstance(event.get("payload"), dict):
            event["payload"] = _rename_mapping_keys(event["payload"], "payload", aliases)
    return out


def generator_id_erasure(trace: dict[str, Any]) -> dict[str, Any]:
    def scrub(obj: Any) -> Any:
        if isinstance(obj, dict):
            cleaned = {}
            for key, value in obj.items():
                key_text = str(key)
                if key_text in GENERATOR_ID_KEYS or key_text.endswith("_generator_id"):
                    continue
                cleaned[key] = scrub(value)
            return cleaned
        if isinstance(obj, list):
            return [scrub(item) for item in obj]
        return obj

    return scrub(copy.deepcopy(trace))


def metadata_identity_erasure(trace: dict[str, Any]) -> dict[str, Any]:
    """Erase substrate/world identity channels outside the explicit generator-id set."""

    aliases: dict[str, str] = {}

    def scrub(obj: Any, parent_key: str = "") -> Any:
        if isinstance(obj, dict):
            cleaned = {}
            for key, value in obj.items():
                key_text = str(key)
                key_norm = key_text.lower()
                compound = f"{parent_key}_{key_norm}" if parent_key else key_norm
                if key_norm in METADATA_IDENTITY_KEYS or compound in METADATA_IDENTITY_KEYS:
                    if isinstance(value, str):
                        cleaned[key] = _stable_alias(value, "metadata_identity", aliases)
                    elif isinstance(value, (int, float, bool)):
                        cleaned[key] = 0
                    else:
                        cleaned[key] = None
                    continue
                cleaned[key] = scrub(value, key_norm)
            return cleaned
        if isinstance(obj, list):
            return [scrub(item, parent_key) for item in obj]
        return obj

    return scrub(copy.deepcopy(trace))


def value_label_erasure(trace: dict[str, Any]) -> dict[str, Any]:
    """Neutralize label-like values whose keys survive key-renaming controls."""

    aliases: dict[str, str] = {}

    def is_label_key(key: str) -> bool:
        key_norm = key.lower()
        return key_norm in VALUE_LABEL_KEYS or any(
            marker in key_norm
            for marker in ("label", "class_id", "motif_present", "target_class", "outcome_class")
        )

    def scrub_value(value: Any) -> Any:
        if isinstance(value, bool):
            return False
        if isinstance(value, (int, float)):
            return 0
        if isinstance(value, str):
            return _stable_alias(value, "value_label", aliases)
        return None

    def scrub(obj: Any) -> Any:
        if isinstance(obj, dict):
            return {
                key: scrub_value(value) if is_label_key(str(key)) else scrub(value)
                for key, value in obj.items()
            }
        if isinstance(obj, list):
            return [scrub(item) for item in obj]
        return obj

    return scrub(copy.deepcopy(trace))


TRANSFORMS: dict[str, Transform] = {
    "event_token_rename": event_token_rename,
    "state_key_rename": state_key_rename,
    "payload_key_rename": payload_key_rename,
    "generator_id_erasure": generator_id_erasure,
    "metadata_identity_erasure": metadata_identity_erasure,
    "value_label_erasure": value_label_erasure,
}


def run_adversarial_controls(predicate: Predicate, trace: dict[str, Any]) -> dict[str, Any]:
    base = predicate(trace)
    rows = []
    passed = True
    for name, transform in TRANSFORMS.items():
        transformed = predicate(transform(trace))
        unchanged = transformed.verdict == base.verdict
        passed = passed and unchanged
        rows.append(
            {
                "axis": name,
                "base_verdict": base.verdict.value,
                "transformed_verdict": transformed.verdict.value,
                "passed": unchanged,
                "transformed_rationale": transformed.rationale,
            }
        )
    return {
        "base_verdict": base.verdict.value,
        "passed": passed,
        "axes": rows,
    }


def run_controls_for_corpus(predicate: Predicate, traces: list[dict[str, Any]], *, limit: int = 12) -> dict[str, Any]:
    sampled = traces[:limit]
    rows = [run_adversarial_controls(predicate, trace) for trace in sampled]
    return {
        "sampled_trace_count": len(sampled),
        "passed": all(row["passed"] for row in rows),
        "failures": [row for row in rows if not row["passed"]],
        "rows": rows,
    }


def _lens_signature(result: Any) -> dict[str, Any]:
    """Return the stable, semantics-bearing part of a lens result."""
    return {
        "declined": bool(getattr(result, "declined")),
        "decline_reason": getattr(result, "decline_reason"),
        "prediction_score": float(getattr(result, "prediction_score")),
        "features_used": tuple(getattr(result, "features_used")),
        "encoded": dict(getattr(result, "encoded")),
    }


def run_lens_adversarial_controls(
    evaluator: LensEvaluator,
    lens_id: str,
    motif_id: str,
    trace: dict[str, Any],
    *,
    score_tolerance: float = 1e-12,
) -> dict[str, Any]:
    """Run four-axis invariance controls against one lens cell on one trace."""
    base = evaluator(lens_id, motif_id, trace)
    base_sig = _lens_signature(base)
    rows = []
    passed = True
    for name, transform in TRANSFORMS.items():
        transformed = evaluator(lens_id, motif_id, transform(trace))
        transformed_sig = _lens_signature(transformed)
        same_decline = transformed_sig["declined"] == base_sig["declined"]
        same_features = transformed_sig["features_used"] == base_sig["features_used"]
        same_encoded = transformed_sig["encoded"] == base_sig["encoded"]
        same_score = abs(transformed_sig["prediction_score"] - base_sig["prediction_score"]) <= score_tolerance
        unchanged = same_decline and same_features and same_encoded and same_score
        passed = passed and unchanged
        rows.append(
            {
                "axis": name,
                "passed": unchanged,
                "base": base_sig,
                "transformed": transformed_sig,
                "failure_reason": None
                if unchanged
                else {
                    "same_decline": same_decline,
                    "same_features": same_features,
                    "same_encoded": same_encoded,
                    "same_score": same_score,
                },
            }
        )
    return {
        "lens_id": lens_id,
        "motif_id": motif_id,
        "trace_id": getattr(base, "trace_id", "unknown"),
        "base": base_sig,
        "passed": passed,
        "axes": rows,
    }


def run_lens_controls_for_corpus(
    evaluator: LensEvaluator,
    lens_id: str,
    motif_id: str,
    traces: list[dict[str, Any]],
    *,
    limit: int = 12,
) -> dict[str, Any]:
    sampled = traces[:limit]
    rows = [run_lens_adversarial_controls(evaluator, lens_id, motif_id, trace) for trace in sampled]
    return {
        "lens_id": lens_id,
        "motif_id": motif_id,
        "sampled_trace_count": len(sampled),
        "passed": all(row["passed"] for row in rows),
        "failures": [row for row in rows if not row["passed"]],
        "rows": rows,
    }
