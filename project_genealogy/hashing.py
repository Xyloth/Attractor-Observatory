"""Canonical JSON + SHA-256 utilities.

`content_hash` for any PG-001 artifact is SHA-256 over the canonical JSON
encoding of the artifact, with the `content_hash` field itself excluded
from the input. Canonical JSON: sort_keys=True, separators=(",", ":"),
ensure_ascii=False.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_json(obj: Any) -> str:
    """Return the canonical JSON encoding of ``obj`` (sort_keys, compact)."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(data: bytes | str) -> str:
    """Return ``sha256:<hex>`` for the given bytes/string."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return "sha256:" + hashlib.sha256(data).hexdigest()


def content_hash(payload: dict) -> str:
    """Hash ``payload`` minus its own ``content_hash`` field."""
    if not isinstance(payload, dict):
        raise TypeError("content_hash expects a dict")
    stripped = {k: v for k, v in payload.items() if k != "content_hash"}
    return sha256_hex(canonical_json(stripped))


def hash_file(path: Path) -> str:
    """Hash a file's bytes (used for evidence_ref content_hashes)."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def write_with_hash(path: Path, payload: dict) -> str:
    """Compute content_hash, store it on the payload, write canonical JSON.

    Returns the computed hash. The output is pretty-printed (indent=2) for
    human readability, but the hash is computed on the canonical compact
    encoding so it is render-independent.
    """
    payload = dict(payload)  # shallow copy
    payload.pop("content_hash", None)
    h = sha256_hex(canonical_json(payload))
    payload["content_hash"] = h
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return h


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_content_hash(payload: dict) -> bool:
    """Return True iff payload['content_hash'] matches recomputation."""
    if "content_hash" not in payload:
        return False
    recomputed = content_hash(payload)
    return recomputed == payload["content_hash"]
