"""Adapter layer for the Observatory Control Room.

Each adapter is a pure read-from-disk function that returns a structured
payload of the form::

    {
        "status": "ok" | "missing" | "malformed",
        "data": <adapter-specific payload>,
        "rationale": "<one-line human-readable explanation>",
    }

Rooms branch on ``status``: on ``ok`` they render real content; on
anything else they route to ``components.empty_state.render_empty_state``.

D22 binding: adapters MUST NOT fabricate values for missing keys, MUST
NOT silently fill in plausible defaults, and MUST NOT raise on missing
input — they degrade to ``status: missing`` with a rationale citing the
absent path.

D9 binding: adapters MUST NOT silently suppress malformed input — they
return ``status: malformed`` with the parser error.
"""

from __future__ import annotations

from control_room.adapters.build_log import parse_build_log
from control_room.adapters.builder_telemetry import parse_builder_telemetry
from control_room.adapters.campaign_reports import parse_campaign_reports
from control_room.adapters.doctrine import parse_doctrine
from control_room.adapters.factory_store import parse_factory_store
from control_room.adapters.git_metadata import parse_git_metadata
from control_room.adapters.methods_falsifiers import parse_methods_falsifiers
from control_room.adapters.negative_space import parse_negative_space
from control_room.adapters.pytest_cache import parse_pytest_cache

# Adapter contract status values.
STATUS_OK = "ok"
STATUS_MISSING = "missing"
STATUS_MALFORMED = "malformed"


def adapter_status_values() -> tuple[str, str, str]:
    """Return the canonical adapter status enum."""
    return (STATUS_OK, STATUS_MISSING, STATUS_MALFORMED)


__all__ = [
    "STATUS_OK",
    "STATUS_MISSING",
    "STATUS_MALFORMED",
    "adapter_status_values",
    "parse_build_log",
    "parse_builder_telemetry",
    "parse_campaign_reports",
    "parse_doctrine",
    "parse_factory_store",
    "parse_git_metadata",
    "parse_methods_falsifiers",
    "parse_negative_space",
    "parse_pytest_cache",
]
