# Doctrine D19-D21: Evidence Sourcing and Densification

Mode: foundational
Spec version: sha256:492dbee22a401cec8679bd325c1ba1145084b5b8848b9beaf6c9b050b3e45729
Signed-by: Codex Builder

D19 - Source-bound extraction. No biological, ecological, or trait-derived
variable may be promoted beyond exploratory status unless it is bound to a
source, provenance record, license class, extraction path, and audit status.
AI systems extract and normalize; they are not evidence sources.

D20 - Extraction/detection separation. Extraction registry entries must be
content-hash-locked before detector sessions consult them. Detector reports
declare the ontology entries consulted and the registry lock they used.

D21 - Densification before claim-bearing. Claim-bearing observations require a
WorldDensificationReport showing the source world is claim_ready_densified for
the relevant motif. trace_valid and exploratory_densified are useful research
states, not claim-bearing states.

Campaign 011 enforces these doctrines through reports/campaign_011/d19_audit.json,
d20_audit.json, and d21_audit.json.
