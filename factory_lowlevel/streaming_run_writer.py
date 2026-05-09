"""Incremental run-payload writer for Factory live cycles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .schemas import canonical_json, sha256, utc_now


class StreamingRunWriter:
    """Write run sections as they become available, then publish a manifest."""

    def __init__(self, run_root: str | Path, *, run_id_hint: str) -> None:
        self.run_root = Path(run_root)
        self.run_id_hint = _safe_name(run_id_hint)
        self.section_root = self.run_root / "sections" / self.run_id_hint
        self.section_root.mkdir(parents=True, exist_ok=True)
        self.sections: dict[str, dict[str, Any]] = {}
        self.started_at = utc_now()

    def write_section(self, name: str, payload: Any) -> dict[str, Any]:
        safe_name = _safe_name(name)
        path = self.section_root / f"{safe_name}.json"
        body = {
            "schema": "FactoryRunPayloadSection.v1",
            "section": name,
            "written_at": utc_now(),
            "payload": payload,
        }
        path.write_text(canonical_json(body) + "\n", encoding="utf-8")
        row = {
            "path": str(path),
            "content_hash": sha256(body),
            "bytes": path.stat().st_size,
        }
        self.sections[name] = row
        return row

    def finish(self, metadata: dict[str, Any]) -> dict[str, Any]:
        manifest = {
            "schema": "FactoryStreamingRunPayloadManifest.v1",
            "started_at": self.started_at,
            "completed_at": utc_now(),
            "run_id_hint": self.run_id_hint,
            "metadata": metadata,
            "sections": dict(sorted(self.sections.items())),
        }
        manifest["content_hash"] = sha256({key: value for key, value in manifest.items() if key != "content_hash"})
        path = self.section_root / "manifest.json"
        path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        latest_path = self.run_root / "latest_run_manifest.json"
        latest_path.parent.mkdir(parents=True, exist_ok=True)
        latest_path.write_text(json.dumps(manifest, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        manifest["path"] = str(path)
        return manifest


def _safe_name(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in value)
    return cleaned[:96] or "run"
