"""Append-only sharded store for high-volume Factory records.

CB-022 Topic F moves the daemon away from "load the entire store before
writing one more source" as the only persistence path. The legacy JSON
files remain the public snapshot surface; this module adds an append-only
NDJSON layer partitioned by world family so writers can persist records
without reading the full prior corpus.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Iterator

from .schemas import canonical_json


class ShardedFactoryStore:
    """Append-only per-world NDJSON persistence.

    The index file is one record id per line. It keeps appends idempotent
    without loading the existing NDJSON payloads into memory.
    """

    def __init__(self, root: str | Path) -> None:
        self.root = Path(root)
        self.shard_root = self.root / "shards"
        self.shard_root.mkdir(parents=True, exist_ok=True)

    def append_records(self, records: Iterable[Any]) -> dict[str, Any]:
        counts: dict[str, int] = {}
        skipped = 0
        for record in records:
            row = record.to_dict() if hasattr(record, "to_dict") else dict(record)
            world_family = str(row.get("world_family") or "unknown")
            record_id = str(row.get("record_id") or "")
            if not record_id:
                skipped += 1
                continue
            if self._record_seen(world_family, record_id):
                skipped += 1
                continue
            shard_dir = self.shard_root / _safe_shard_name(world_family)
            shard_dir.mkdir(parents=True, exist_ok=True)
            with (shard_dir / "empirical_records.ndjson").open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(canonical_json(row) + "\n")
            with (shard_dir / "record_ids.txt").open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(record_id + "\n")
            counts[world_family] = counts.get(world_family, 0) + 1
        manifest = {
            "schema": "FactoryShardedStoreManifest.v1",
            "shard_root": str(self.shard_root),
            "appended_by_world": counts,
            "skipped_existing_or_invalid": skipped,
        }
        (self.shard_root / "manifest.json").write_text(
            json.dumps(manifest, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        return manifest

    def iter_records(self, world_family: str | None = None) -> Iterator[dict[str, Any]]:
        paths: list[Path]
        if world_family:
            paths = [self.shard_root / _safe_shard_name(world_family) / "empirical_records.ndjson"]
        else:
            paths = sorted(self.shard_root.glob("*/empirical_records.ndjson"))
        for path in paths:
            if not path.exists():
                continue
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    if line.strip():
                        yield json.loads(line)

    def _record_seen(self, world_family: str, record_id: str) -> bool:
        index_path = self.shard_root / _safe_shard_name(world_family) / "record_ids.txt"
        if not index_path.exists():
            return False
        with index_path.open("r", encoding="utf-8") as handle:
            return any(line.rstrip("\n") == record_id for line in handle)


def _safe_shard_name(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in value)
