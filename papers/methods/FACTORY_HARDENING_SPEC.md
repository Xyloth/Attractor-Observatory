# Factory Hardening Spec

Status: TASK-027 readiness checklist
Owner: Codex Builder
Mode: exploratory
Scope: W0 math primitives and W-1 atomic/molecular primitives only
Gate count: 59

This spec defines the quality gates the low-level Factory must pass before live autonomous ingestion can run unattended. The target state is practical: the PI can leave a machine on while the daemon downloads, categorizes, filters, routes, and audits source records without runtime AI and without admitting false data into the scientific record.

No gate below authorizes claim-bearing promotion. Passing this checklist only authorizes unattended exploratory ingestion into the low-level Factory. AI may act at design time and audit time, not inside the daemon ingestion path.

## Readiness Rule

The daemon is live-ready only if every gate below passes under a cold start, a warm cache rerun, a forced schema-mismatch fixture, and a stop/start recovery fixture. Any red gate forces `daemon_mode = dry_run` and creates a high-severity audit item.

## A. Source-Validity Gates

| Gate | Measurement | Pass condition |
|---|---|---|
| SV-01 allowed source registry | Source URL host checked against allowlist | Host is one of NIST, IUPAC, ChEBI, PubChem, or a peer-reviewed math.DS DOI/catalog source |
| SV-02 canonical URL retained | Every source definition has canonical URL | `source.url` is nonempty, HTTPS or DOI, and stored in `SourceDefinition` |
| SV-03 retrieval URL retained | Every empirical record has retrieval URL | `provenance.source_url` or DOI resolves to the fetched or curated record path |
| SV-04 retrieval timestamp retained | Every record and cache entry has timestamp | `retrieved_at` or `fetched_at` is ISO UTC and non-null |
| SV-05 license class enforced | License class checked before export | Only `cc0`, `public_domain`, `open`, or `metadata_only` records enter exported empirical records |
| SV-06 raw redistribution policy | Raw cache policy checked per source | Metadata-only sources export derived summaries only; raw cache stays local |
| SV-07 authority label present | Every source carries authority text | NIST/PubChem/DOI authority appears in provenance, not inferred by filename |
| SV-08 retrieval-mode honesty | Fetch path records mode | `network`, `bundled_authoritative_seed`, `bundled_peer_reviewed_catalog`, or `dry_run` is stored and surfaced |

## B. Schema-Survival Gates

| Gate | Measurement | Pass condition |
|---|---|---|
| SS-01 parser version pinned | Adapter parser version recorded | `parser_version` is persisted in source cache and report artifacts |
| SS-02 required-key contract | Adapter validates required fields | Missing required source keys produce audit item, not best-effort normal output |
| SS-03 unknown-key census | Adapter records unexpected source keys | Schema drift report lists new keys by source and parser version |
| SS-04 source schema bump response | Forced fixture changes source shape | Daemon switches that source to hold/audit and continues unaffected sources |
| SS-05 normalized schema roundtrip | Normalized references serialize/parse | Canonical JSON roundtrip preserves IDs and all four ontology axes |
| SS-06 evidence graph rebuild determinism | Rebuild graph twice from same refs | Evidence-edge IDs and counts are byte-identical |
| SS-07 schema mismatch severity | Incompatible schema fixture | High-severity audit item with `recommended_action = adapter_review_before_rerun` |

## C. Adversarial-Input Gates

| Gate | Measurement | Pass condition |
|---|---|---|
| AI-01 math missing strange-attractor | Degenerate math catalog fixture | Source-native stable-form detector declines |
| AI-02 atomic single energy level | Spectrum fixture with one level | Discrete-spectrum detector declines |
| AI-03 molecule no heavy atoms | Molecular fixture with zero heavy atoms | Molecular-topology detector declines |
| AI-04 malformed source file | Invalid CSV/JSON fixture | Adapter emits audit item and zero normalized references for bad record |
| AI-05 partial response | Truncated network/cache payload | Daemon retains cache entry but blocks normalization for incomplete records |
| AI-06 stale cache | Cache older than refresh cadence | Daemon surfaces medium audit item and marks retrieval mode stale-cache |
| AI-07 duplicate records | Duplicate source rows | Empirical record ID deduplicates deterministically; duplicate count is reported |
| AI-08 nonsensical numeric values | Negative counts, NaN, impossible levels | Record held for audit before world routing |

## D. Audit-Queue Gates

| Gate | Measurement | Pass condition |
|---|---|---|
| AQ-01 restricted license route | Restricted-license fixture | Record is held in source cache only and high-severity audit item is created |
| AQ-02 schema mismatch route | Schema mismatch fixture | High-severity audit item references source, parser, and failing keys |
| AQ-03 detector anomaly route | Source-native detector mismatch | Medium or high audit item created before report can go green |
| AQ-04 queue persistence | Write/read audit queue | Audit item IDs and recommended actions survive daemon restart |
| AQ-05 surfacing path | Control Room/monitor state reads queue count | `factory_intake_dock_state.audit_queue_count` equals persisted queue count |
| AQ-06 timeout policy | Source fetch exceeds timeout | Source is skipped for that cycle, audit item records timeout and retry window |
| AQ-07 retry ceiling | Repeated transient failures | After configured retry limit, source moves to manual review, not infinite retry |

## E. Idempotence Gates

| Gate | Measurement | Pass condition |
|---|---|---|
| ID-01 cold rerun equality | Two dry-run ingestions from empty stores | Record IDs, normalized IDs, routed worlds, and evidence graph are identical |
| ID-02 warm-cache equality | Rerun with existing source cache | Normalized output and evidence graph are identical to cold run |
| ID-03 ledger duplicate detection | Same run ID appended twice | Session record marks duplicate run ID and does not imply new science |
| ID-04 stable content hashes | Store snapshot hash recomputed | Hash is stable after timestamp-free canonicalization of scientific payload |
| ID-05 no hidden mutable state | Run after process restart | Output matches prior run without relying on in-memory registry state |

## F. Detector-Decline Preservation Gates

| Gate | Measurement | Pass condition |
|---|---|---|
| DD-01 raw low-level lens decline | Existing formal lenses evaluate W0/W-1 raw traces | The 96/96 decline pattern is preserved and surfaced as signal |
| DD-02 no decline-patching path | Static inspection of detector/report code | No branch rewrites low-level world family to avoid raw decline measurement |
| DD-03 projection kept separate | Projection diagnostics stored under bridge/projection fields | Projection nondeclines never overwrite raw decline counts |
| DD-04 source-native detector separation | Source-native detector rows separate from formal lenses | Source-native fires do not affect formal coverage scores |
| DD-05 decline-as-signal report | Monitor state and methods doc include interpretation | Decline count is visible in every downstream summary that shows detector state |

## G. Schema-Mismatch And Math-Shadow Bridge Gates

| Gate | Measurement | Pass condition |
|---|---|---|
| MS-01 bridge code labeled | Projection code/report inspected | Every projection field uses `projection`, `bridge`, or `math_shadow` language |
| MS-02 no bridge-as-finding | Projection report checked | `claim_eligible` is false and interpretation states diagnostic-only |
| MS-03 projection-basis comparison | Multiple projections per low-level world | Nondecline counts are reported per basis, not collapsed into one answer |
| MS-04 source basis retained | Each projection row stores source and projected world family | Downstream readers can recover the original low-level source family |
| MS-05 doctrine revision candidate path | Bridge exposes need for doctrine change | Candidate doctrine revisions go to decision log; no doctrine ratified by daemon |

## H. Daemon-State Recovery Gates

| Gate | Measurement | Pass condition |
|---|---|---|
| DR-01 stop before normalization | Kill/restart after cache write | Cache survives; records are normalized exactly once on restart |
| DR-02 stop before evidence graph | Kill/restart after normalized refs | Evidence graph rebuilds from refs without duplicate edges |
| DR-03 corrupt partial file | Truncated JSON artifact in store | Daemon quarantines file and rebuilds from last valid layer or stops dry-run |
| DR-04 session ledger recovery | Ledger contains malformed line | Bad line is ignored with audit item; valid prior run IDs still detected |
| DR-05 atomic write policy | Store write inspected | Scientific artifacts are written through temp/replace or equivalent corruption-safe path before live mode |

## I. Provenance-Chain Gates

| Gate | Measurement | Pass condition |
|---|---|---|
| PC-01 cache-to-record link | Every empirical record links to source cache | `source_id` and raw content hash chain can be reconstructed |
| PC-02 record-to-normalized link | Every normalized ref points to empirical record | Missing empirical record creates audit item |
| PC-03 normalized-to-edge link | Every evidence edge lists source record IDs | Edge confidence can be traced back to records |
| PC-04 record-to-world trace link | World traces contain source-bound record IDs | Trace events/states point to empirical record IDs |
| PC-05 license in every layer | Cache, record, normalized report, trace metadata | License/export policy remains visible through all layers |

## J. Readiness-Certification Gates

| Gate | Measurement | Pass condition |
|---|---|---|
| RC-01 zero runtime AI proof | Static and runtime check | No ingestion path imports or calls AI/model connectors |
| RC-02 dry-run default | Scheduler and daemon config | Live network ingestion is opt-in; unattended mode starts from dry-run-safe config |
| RC-03 high-risk regression slice | Run tests for Factory, Campaign 016, Control Room adapter | All targeted tests pass after regeneration |
| RC-04 readiness packet | Single JSON readiness report | Report includes all gate IDs, pass/fail, evidence path, and blocking audit items |

## Current TASK-027 Status

TASK-027 implements the first adversarial detector controls and projection-basis comparison for Campaign 016. It does not certify unattended live mode. The remaining largest gap is daemon recovery under interrupted writes; that needs explicit temp/replace persistence and stop/start fixtures before the PI should leave live ingestion running overnight.
