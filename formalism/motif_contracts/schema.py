"""MotifContract.v2 schema and source-object-map independence rules."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Iterable


class VerdictState(StrEnum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    INVALID_MALFORMED = "invalid_malformed"


class IndependenceVerdict(StrEnum):
    CLEAN = "CLEAN"
    PARTIAL = "PARTIAL"
    BAD = "BAD"
    UNKNOWN = "UNKNOWN"
    INVALID = "INVALID"


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def content_hash(payload: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SourceObjectEntry:
    source_object: str
    type: str
    fields_read: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_object": self.source_object,
            "type": self.type,
            "fields_read": list(self.fields_read),
        }


def _normalise_som(rows: Iterable[SourceObjectEntry | dict[str, Any]]) -> list[SourceObjectEntry]:
    normalised: list[SourceObjectEntry] = []
    for row in rows:
        if isinstance(row, SourceObjectEntry):
            normalised.append(row)
            continue
        normalised.append(
            SourceObjectEntry(
                source_object=str(row["source_object"]),
                type=str(row.get("type", "unknown")),
                fields_read=tuple(str(item) for item in row.get("fields_read", [])),
            )
        )
    return normalised


_SELF_VALUE_FIELDS = {"", ".", "self", "value", "$value"}
_UNKNOWN_FIELDS = {"unknown", "tbd", "n/a", "na", "unspecified"}


def _path_tokens(path: str) -> tuple[str, ...]:
    cleaned = (
        path.strip()
        .replace("[", ".")
        .replace("]", "")
        .replace("/", ".")
        .replace("::", ".")
    )
    tokens = tuple(token for token in cleaned.split(".") if token)
    if tokens == ("x",):
        return ("state", "x")
    return tokens


def _field_tokens(path: str) -> tuple[str, ...]:
    cleaned = (
        path.strip()
        .replace("[", ".")
        .replace("]", "")
        .replace("/", ".")
        .replace("::", ".")
    )
    return tuple(token for token in cleaned.split(".") if token)


def _canonical_paths(entry: SourceObjectEntry) -> tuple[tuple[str, ...], ...]:
    object_path = _path_tokens(entry.source_object)
    if not object_path:
        return tuple()
    fields = tuple(str(field).strip() for field in entry.fields_read)
    if not fields:
        return (object_path,)
    out: list[tuple[str, ...]] = []
    for field in fields:
        if field.lower() in _SELF_VALUE_FIELDS:
            out.append(object_path)
            continue
        field_path = _field_tokens(field)
        if not field_path:
            out.append(object_path)
        elif object_path[-len(field_path) :] == field_path:
            out.append(object_path)
        else:
            out.append(object_path + field_path)
    return tuple(out)


def _has_unknown_fields(entry: SourceObjectEntry) -> bool:
    if not entry.fields_read:
        return True
    return any(str(field).strip().lower() in _UNKNOWN_FIELDS for field in entry.fields_read)


def _path_overlaps(left: tuple[str, ...], right: tuple[str, ...]) -> bool:
    if not left or not right:
        return False
    width = min(len(left), len(right))
    for index in range(width):
        if left[index] in {"*", "**"} or right[index] in {"*", "**"}:
            return True
        if left[index] != right[index]:
            return False
    return True


def derive_independence_verdict(
    predicate_som: Iterable[SourceObjectEntry | dict[str, Any]],
    lens_som: Iterable[SourceObjectEntry | dict[str, Any]],
) -> IndependenceVerdict:
    pred = _normalise_som(predicate_som)
    lens = _normalise_som(lens_som)
    if not pred or not lens:
        return IndependenceVerdict.UNKNOWN

    pred_paths = [(entry, _canonical_paths(entry)) for entry in pred]
    lens_paths = [(entry, _canonical_paths(entry)) for entry in lens]
    if any(not paths for _, paths in pred_paths + lens_paths):
        return IndependenceVerdict.INVALID

    overlapping_source_objects = False
    unknown_overlap = False
    for pred_entry, pred_entry_paths in pred_paths:
        for lens_entry, lens_entry_paths in lens_paths:
            pred_object = _path_tokens(pred_entry.source_object)
            lens_object = _path_tokens(lens_entry.source_object)
            if not _path_overlaps(pred_object, lens_object):
                continue
            overlapping_source_objects = True
            if _has_unknown_fields(pred_entry) or _has_unknown_fields(lens_entry):
                unknown_overlap = True
                continue
            for pred_path in pred_entry_paths:
                for lens_path in lens_entry_paths:
                    if _path_overlaps(pred_path, lens_path):
                        return IndependenceVerdict.BAD

    if unknown_overlap:
        return IndependenceVerdict.UNKNOWN
    if overlapping_source_objects:
        return IndependenceVerdict.PARTIAL
    return IndependenceVerdict.CLEAN


@dataclass(frozen=True)
class LensContract:
    lens_id: str
    features: tuple[str, ...]
    source_object_map: tuple[SourceObjectEntry, ...]
    justification: str = ""

    def independence_from(self, predicate_som: Iterable[SourceObjectEntry]) -> IndependenceVerdict:
        return derive_independence_verdict(predicate_som, self.source_object_map)

    def to_dict(self, predicate_som: Iterable[SourceObjectEntry]) -> dict[str, Any]:
        return {
            "features": list(self.features),
            "source_object_map": [entry.to_dict() for entry in self.source_object_map],
            "shares_input_with_predicate": self.independence_from(predicate_som).value,
            "justification": self.justification,
        }


@dataclass(frozen=True)
class MotifContractV2:
    motif_id: str
    semantic_definition: str
    allowed_evidence: tuple[str, ...]
    forbidden_evidence: tuple[str, ...]
    predicate_abstraction_layer: str
    predicate_source_object_map: tuple[SourceObjectEntry, ...]
    lens_abstraction_layer: tuple[LensContract, ...]
    invariance_requirements: tuple[str, ...]
    decoy_controls: tuple[str, ...]
    promotion_requirements: tuple[str, ...]
    known_failure_modes: tuple[str, ...]
    empirically_positive_worlds: tuple[dict[str, Any], ...]
    contract_version: str = "2"
    signed_at: str = "2026-05-06T00:00:00-04:00"
    signed_by: tuple[str, ...] = ("James Dye (PI)", "Architect Claude", "Codex 1.5x")

    def payload_without_hash(self) -> dict[str, Any]:
        return {
            "motif_id": self.motif_id,
            "contract_version": self.contract_version,
            "signed_at": self.signed_at,
            "signed_by": list(self.signed_by),
            "semantic_definition": self.semantic_definition,
            "allowed_evidence": list(self.allowed_evidence),
            "forbidden_evidence": list(self.forbidden_evidence),
            "predicate_abstraction_layer": self.predicate_abstraction_layer,
            "predicate_source_object_map": [entry.to_dict() for entry in self.predicate_source_object_map],
            "lens_abstraction_layer": {
                lens.lens_id: lens.to_dict(self.predicate_source_object_map)
                for lens in self.lens_abstraction_layer
            },
            "invariance_requirements": list(self.invariance_requirements),
            "decoy_controls": list(self.decoy_controls),
            "promotion_requirements": list(self.promotion_requirements),
            "known_failure_modes": list(self.known_failure_modes),
            "empirically_positive_worlds": list(self.empirically_positive_worlds),
            "verdict_states": [state.value for state in VerdictState],
        }

    def content_hash(self) -> str:
        return content_hash(self.payload_without_hash())

    def to_dict(self) -> dict[str, Any]:
        payload = self.payload_without_hash()
        payload["content_hash"] = self.content_hash()
        return payload

    def signature(self) -> dict[str, Any]:
        return {
            "scheme": "sha256-canonical-json",
            "signed_by": list(self.signed_by),
            "signed_hash": self.content_hash(),
            "status": "contract_v2_locked_for_task_motif_impl",
        }


@dataclass(frozen=True)
class PredicateResult:
    motif_id: str
    verdict: VerdictState
    rationale: str
    evidence: dict[str, Any] = field(default_factory=dict)

    @property
    def positive(self) -> bool:
        return self.verdict == VerdictState.POSITIVE

    @property
    def evaluable(self) -> bool:
        return self.verdict in {VerdictState.POSITIVE, VerdictState.NEGATIVE}

    def to_dict(self) -> dict[str, Any]:
        return {
            "motif_id": self.motif_id,
            "verdict": self.verdict.value,
            "rationale": self.rationale,
            "evidence": self.evidence,
        }
