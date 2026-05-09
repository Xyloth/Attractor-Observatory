"""Evidence-substance gates for source_bound claims.

The gate is intentionally conservative about what it proves. Identifier syntax
is Tier 1, live/registry resolution is Tier 2, title/claim consistency is Tier 3,
and a signed substance audit is Tier 4.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import IntEnum
from typing import Any


class EvidenceTier(IntEnum):
    NONE = 0
    IDENTIFIER_PARSED = 1
    IDENTIFIER_RESOLVES = 2
    TITLE_MATCHES_CLAIM = 3
    SUBSTANCE_AUDIT_SIGNED = 4


@dataclass(frozen=True)
class SubstanceGateResult:
    citation: str
    tier: EvidenceTier
    passed: bool
    minimum_tier: EvidenceTier
    checks: dict[str, bool]
    title: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "citation": self.citation,
            "tier": int(self.tier),
            "tier_label": self.tier.name.lower(),
            "passed": self.passed,
            "minimum_tier": int(self.minimum_tier),
            "checks": dict(self.checks),
            "title": self.title,
            "reason": self.reason,
        }


TITLE_REGISTRY = {
    "doi:10.1186/s13015-015-0042-8": "Algorithms for detecting and analysing autocatalytic sets",
    "doi:10.1098/rsif.2023.0732": "Self-generating autocatalytic networks: structural results, algorithms and their relevance to early biochemistry",
    "doi:10.1186/1759-2208-5-2": "Autocatalytic sets in a partitioned biochemical network",
    "doi:10.1186/1759-2208-3-5": "Autocatalytic sets extended: Dynamics, inhibition, and a generalization",
    "doi:10.3390/life8040062": "Autocatalytic Networks at the Basis of Life's Origin and Organization",
    "doi:10.1088/1367-2630/aa9fcd": "Autocatalytic sets and chemical organizations: modeling self-sustaining reaction networks at the origin of life",
    "doi:10.1038/362709a0": "Instability and decay of the primary structure of DNA",
    "pmid:8469282": "Instability and decay of the primary structure of DNA.",
    "doi:10.1007/bf01417909": "The self-organizing exploratory pattern of the argentine ant",
    "pmid:32546115": "The Bayesian superorganism: externalized memories facilitate distributed sampling.",
    "doi:10.1007/bf00623322": "Selforganization of matter and the evolution of biological macromolecules",
    "doi:10.1038/nature01568": "The evolutionary origin of complex features",
    "pmid:12736677": "The evolutionary origin of complex features.",
    "doi:10.1021/ja900919c": "Coupled Growth and Division of Model Protocell Membranes",
    "pmid:19323552": "Coupled growth and division of model protocell membranes.",
    "doi:10.1073/pnas.96.17.9716": "Neutral evolution of mutational robustness",
    "pmid:10449760": "Neutral evolution of mutational robustness.",
}

STOPWORDS = {
    "and",
    "are",
    "for",
    "from",
    "into",
    "the",
    "this",
    "that",
    "with",
    "within",
}

DOMAIN_SYNONYMS = {
    "autocatalytic": {"autocatalytic", "catalytic", "raf", "self-generating", "self-sustaining"},
    "closure": {"closure", "self-generating", "self-sustaining", "raf"},
    "reaction": {"reaction", "reactions", "network", "networks", "chemical", "chemistry"},
    "repair": {"repair", "damage", "instability", "decay", "disruption"},
    "memory": {"memory", "memories", "distributed", "externalized", "trail", "pheromone", "exploratory"},
    "lineage": {"lineage", "descent", "evolution", "evolutionary", "selforganization"},
    "lineages": {"lineage", "descent", "evolution", "evolutionary", "selforganization"},
    "evolution": {"evolution", "evolutionary", "evolvability", "descent", "lineage"},
    "replication": {"replication", "replicator", "macromolecules", "evolution"},
    "boundary": {"boundary", "membrane", "protocell", "vesicle", "division", "growth"},
    "floor": {"neutral", "robustness", "canalization", "variation", "phenotype"},
}


def identifier_parsed(citation: str) -> bool:
    text = citation.strip()
    return bool(
        re.fullmatch(r"doi:10\.\S+/\S+", text, flags=re.IGNORECASE)
        or re.fullmatch(r"pmid:\d+", text, flags=re.IGNORECASE)
        or re.fullmatch(r"https?://\S+", text, flags=re.IGNORECASE)
    )


def resolved_title(citation: str, metadata: dict[str, Any] | None = None) -> str:
    metadata = metadata or {}
    title = str(metadata.get("source_title") or metadata.get("resolved_title") or "").strip()
    if title:
        return title
    return TITLE_REGISTRY.get(citation.lower(), "")


def identifier_resolves(citation: str, metadata: dict[str, Any] | None = None) -> bool:
    metadata = metadata or {}
    status = metadata.get("resolver_status")
    if status in {200, "200", "ok", "resolved"}:
        return True
    return bool(resolved_title(citation, metadata))


def _tokens(text: str) -> set[str]:
    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) >= 4 and token not in STOPWORDS
    }
    tokens.update(token[:-1] for token in list(tokens) if token.endswith("s") and len(token) > 5)
    return tokens


def _expand(tokens: set[str]) -> set[str]:
    out = set(tokens)
    for token in list(tokens):
        out.update(DOMAIN_SYNONYMS.get(token, set()))
    return out


def title_matches_claim(title: str, claim: str) -> bool:
    title_tokens = _expand(_tokens(title))
    claim_tokens = _expand(_tokens(claim))
    if not title_tokens or not claim_tokens:
        return False
    overlap = title_tokens & claim_tokens
    high_signal = overlap - {"systems", "model", "models", "network", "networks"}
    return len(high_signal) >= 1 or len(overlap) >= 2


def substance_audit_signed(metadata: dict[str, Any] | None = None) -> bool:
    metadata = metadata or {}
    return metadata.get("substance_audit_signed") is True


def evaluate_source_bound(
    citation: str,
    claim: str,
    metadata: dict[str, Any] | None = None,
    *,
    minimum_tier: EvidenceTier = EvidenceTier.TITLE_MATCHES_CLAIM,
) -> SubstanceGateResult:
    metadata = metadata or {}
    title = resolved_title(citation, metadata)
    checks = {
        "identifier_parsed": identifier_parsed(citation),
        "identifier_resolves": False,
        "title_matches_claim": False,
        "substance_audit_signed": False,
    }
    if checks["identifier_parsed"]:
        checks["identifier_resolves"] = identifier_resolves(citation, metadata)
    if checks["identifier_resolves"]:
        checks["title_matches_claim"] = title_matches_claim(title, claim)
    if checks["title_matches_claim"]:
        checks["substance_audit_signed"] = substance_audit_signed(metadata)

    tier = EvidenceTier.NONE
    if checks["identifier_parsed"]:
        tier = EvidenceTier.IDENTIFIER_PARSED
    if checks["identifier_resolves"]:
        tier = EvidenceTier.IDENTIFIER_RESOLVES
    if checks["title_matches_claim"]:
        tier = EvidenceTier.TITLE_MATCHES_CLAIM
    if checks["substance_audit_signed"]:
        tier = EvidenceTier.SUBSTANCE_AUDIT_SIGNED

    return SubstanceGateResult(
        citation=citation,
        tier=tier,
        passed=tier >= minimum_tier,
        minimum_tier=minimum_tier,
        checks=checks,
        title=title,
        reason="source_bound evidence clears required tier"
        if tier >= minimum_tier
        else f"source_bound evidence reached tier {int(tier)} below required tier {int(minimum_tier)}",
    )
