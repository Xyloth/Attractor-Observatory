from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from formalism.evidence.substance_gate import EvidenceTier, evaluate_source_bound, identifier_parsed  # noqa: E402
from formalism.motif_contracts.contracts import all_contracts  # noqa: E402


def test_substance_gate_separates_identifier_shape_resolution_and_support():
    assert identifier_parsed("doi:10.1186/s13015-015-0042-8")
    assert identifier_parsed("pmid:25969692")
    assert identifier_parsed("https://example.org/paper")

    resolved_wrong = evaluate_source_bound(
        "doi:10.1098/rsif.2017.0228",
        "RAF/autocatalytic reaction networks",
        {"resolver_status": 200, "resolved_title": "Adhesion modulation using glue droplet spreading in spider capture silk"},
    )
    assert resolved_wrong.tier == EvidenceTier.IDENTIFIER_RESOLVES
    assert resolved_wrong.passed is False

    supported = evaluate_source_bound(
        "doi:10.1186/s13015-015-0042-8",
        "RAF/autocatalytic reaction networks",
    )
    assert supported.tier >= EvidenceTier.TITLE_MATCHES_CLAIM
    assert supported.passed is True


def test_every_source_bound_motif_contract_claim_clears_tier3_or_is_diagnostic():
    failures = []
    for motif_id, contract in all_contracts().items():
        for world in contract.empirically_positive_worlds:
            if world.get("mapping_status") != "source_bound":
                continue
            claim = "; ".join(world.get("instances", []))
            for citation in world.get("citations", []):
                result = evaluate_source_bound(citation, claim, world)
                diagnostic = world.get("evidence_tier") == "1_diagnostic"
                if not result.passed and not diagnostic:
                    failures.append((motif_id, world.get("world_family"), citation, result.to_dict()))
    assert not failures


def test_campaign006_missing_run_paths_are_routed_to_audit_queue():
    audit_queue = json.loads((ROOT / "reports/campaign_006/audit_queue.json").read_text(encoding="utf-8"))
    assert any(row.get("audit_id") == "CB022-B4-campaign006-private-run-paths" for row in audit_queue)


def test_tracked_json_path_references_resolve_or_have_private_boundary_marker():
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
    tracked_set = {Path(rel).as_posix() for rel in tracked}
    missing = []

    def looks_like_path(key: str, value: str) -> bool:
        lower_key = key.lower()
        lower_value = value.lower().strip()
        if lower_value.startswith(("http://", "https://", "doi:", "pmid:", "sha256:")):
            return False
        if not any(marker in lower_key for marker in ("path", "file", "artifact", "report", "script")):
            return False
        return (
            "/" in value
            or "\\" in value
            or lower_value.endswith((".json", ".md", ".py", ".txt", ".csv", ".lock", ".signed"))
            or lower_value.startswith("python ")
        )

    def resolves_on_shipped_surface(value: str) -> bool:
        text = value.strip().strip('"')
        if text.startswith("python "):
            return False
        path = Path(text.replace("\\", "/"))
        if path.is_absolute():
            try:
                rel = path.relative_to(ROOT).as_posix()
            except ValueError:
                return False
        else:
            rel = path.as_posix()
        return rel in tracked_set

    def marked(node: dict, key: str) -> bool:
        return (
            node.get("evidence_private") is True
            or node.get(f"{key}_status") == "private_unshipped"
            or node.get("path_status") == "private_unshipped"
        )

    def walk(node, rel: str, json_path: str = ""):
        if isinstance(node, dict):
            for key, value in node.items():
                child_path = f"{json_path}.{key}" if json_path else key
                if isinstance(value, str) and looks_like_path(key, value) and not resolves_on_shipped_surface(value) and not marked(node, key):
                    missing.append((rel, child_path, value))
                elif isinstance(value, (dict, list)):
                    walk(value, rel, child_path)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                if isinstance(value, (dict, list)):
                    walk(value, rel, f"{json_path}.{index}" if json_path else str(index))

    for rel in tracked:
        if not rel.endswith(".json") or rel.startswith(("papers/falsification/DX-003/", ".claude/")):
            continue
        try:
            payload = json.loads((ROOT / rel).read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError):
            continue
        walk(payload, rel)

    assert not missing
