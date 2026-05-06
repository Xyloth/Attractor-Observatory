"""Shared source-bound world construction helpers for Factory ingestion."""

from __future__ import annotations

from typing import Any


def construct_world_from_records(
    world_cls: type[Any],
    records: list[Any],
    *,
    expected_world: str,
    accepted_record_types: set[str],
    seed: int,
    steps_default: int = 24,
    dt_default: float = 0.25,
    records_as_params: bool = False,
) -> dict[str, Any]:
    accepted = []
    rejections = []
    for record in records:
        record_id = getattr(record, "record_id", "unknown")
        world_family = getattr(record, "world_family", "")
        record_type = getattr(record, "record_type", "")
        payload = getattr(record, "payload", {}) or {}
        if world_family != expected_world:
            rejections.append({"record_id": record_id, "reason": f"world_mismatch:{world_family}!={expected_world}"})
            continue
        if record_type not in accepted_record_types:
            rejections.append({"record_id": record_id, "reason": f"record_type_not_accepted:{record_type}"})
            continue
        if not records_as_params and not isinstance(payload.get("world_parameters"), dict):
            rejections.append({"record_id": record_id, "reason": "missing_world_parameters"})
            continue
        accepted.append(record)
    if not accepted:
        return {"world": None, "record_ids": [], "rejections": rejections}

    if records_as_params:
        params = {"records": [_record_to_dict(record) for record in accepted]}
    else:
        params = dict(accepted[0].payload["world_parameters"])

    try:
        world = world_cls()
        world.reset(seed=seed, params=params)
        if hasattr(world, "run_to_completion"):
            world.run_to_completion()
        elif hasattr(world, "step"):
            steps = int(params.get("steps", steps_default))
            dt = float(params.get("dt", dt_default))
            for _ in range(steps):
                world.step(dt)
    except Exception as exc:  # construction failures are routed as honest rejections.
        return {
            "world": None,
            "record_ids": [getattr(record, "record_id", "unknown") for record in accepted],
            "rejections": [
                *rejections,
                {
                    "record_id": getattr(accepted[0], "record_id", "unknown"),
                    "reason": f"world_construction_failed:{type(exc).__name__}:{exc}",
                },
            ],
        }
    return {
        "world": world,
        "record_ids": [record.record_id for record in accepted],
        "rejections": rejections,
    }


def _record_to_dict(record: Any) -> dict[str, Any]:
    if hasattr(record, "to_dict"):
        return record.to_dict()
    return {
        "record_id": getattr(record, "record_id", "unknown"),
        "source_id": getattr(record, "source_id", "unknown"),
        "world_family": getattr(record, "world_family", ""),
        "record_type": getattr(record, "record_type", ""),
        "canonical_name": getattr(record, "canonical_name", ""),
        "payload": getattr(record, "payload", {}) or {},
        "provenance": getattr(record, "provenance", {}) or {},
        "license_class": getattr(record, "license_class", "metadata_only"),
    }
