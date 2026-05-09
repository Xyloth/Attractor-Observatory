# DX-003 Round 6 - External Identifier Reality Collision

round_id: 6
attack_angle: I treated the project's external citations as reality anchors rather than internal tokens. This round asked whether MotifContract.v2's `empirically_positive_worlds` citations resolve against live external registries, whether the resolved titles support the world/motif labels they are used for, and whether campaign reports preserve enough source substance to prevent a DOI-shaped string from masquerading as evidence.
elapsed_at_round_start: approximately 00:26:44 after T_start
elapsed_at_round_end: 00:33:27.7500822 after T_start

## Surfaces Examined

- `formalism/motif_contracts/contracts.py`
- `formalism/motif_contracts/schema.py`
- `reports/campaign_023/full_report.json`
- `reports/campaign_024/full_report.json`
- `papers/methods/MOTIF_CONTRACT_SCHEMA_v2.md`
- `papers/methods/CAMPAIGN_023_MOTIF_CONTRACT_IMPL.md`
- `papers/methods/CAMPAIGN_024_LENS_SIDE_DECOUPLING.md`
- Live resolver checks through Crossref Works API and NCBI PubMed ESummary for all DOI/PMID strings embedded in the locked motif contracts.

## Findings

### R6-F1 - Broken - Autocatalytic Closure W1 Is Source-Bound To Unrelated Papers

severity: red
claim: The `motif.autocatalytic_closure.draft` contract lists W1 `RAF/autocatalytic reaction networks` as `source_bound` with citations `doi:10.1098/rsif.2017.0228` and `doi:10.1371/journal.pone.0084054`. Live resolution of those DOI records returns titles about spider capture silk adhesion and essential tremor neuroanatomy/propranolol response, not RAFs, autocatalytic sets, reaction networks, or chemistry. The instrument's DOI syntax is real, but the semantic evidence binding is false.

reproducer:

```powershell
Get-Content papers\falsification\DX-003\round_6_reproducers\contract_citation_semantic_probe.txt
```

expected output includes:

```text
flagged_obvious_mismatches=2
{"citation": "doi:10.1098/rsif.2017.0228", ... "instances": ["RAF/autocatalytic reaction networks"], ... "resolved_title": "Adhesion modulation using glue droplet spreading in spider capture silk", ...}
{"citation": "doi:10.1371/journal.pone.0084054", ... "instances": ["RAF/autocatalytic reaction networks"], ... "resolved_title": "Neuroanatomical Heterogeneity of Essential Tremor According to Propranolol Response", ...}
```

secondary reproducer:

```powershell
Select-String -Path formalism\motif_contracts\contracts.py,reports\campaign_023\full_report.json,reports\campaign_024\full_report.json -Pattern "10\.1098/rsif\.2017\.0228|10\.1371/journal\.pone\.0084054|RAF/autocatalytic reaction networks" -Context 2,2
```

mistake_class mapping: Class 14 candidate: DOI-shaped semantic non-evidence. This is not merely missing provenance; it is a valid external identifier attached to the wrong scientific claim.
doctrine_refs: D23/D29 provenance discipline; D26 MotifContract.v2 source-object discipline; D17 via-negativa publication of failures.
suggested_triage: technical_repair plus architectural_discussion. Every `empirically_positive_worlds` entry needs substance audit before it can serve as a reality anchor; `source_bound` should not be allowed to mean only "string has a DOI".

### R6-F2 - Fake-Passed - Contract Citation Identifiers Resolve, But Substance Audit Is Still Globally False

severity: amber
claim: The resolver pass successfully resolved all 30 contract citation rows, which proves only identifier dereferenceability. The same payload reports `substance_audit_signed_true=0`, and campaign 023/024 reports embed those empirical-positive-world records while still passing their no-promotion gates. That is honest in the narrow sense (`claim_eligible=false`), but fake-green in the broader reality-audit sense: the reports can carry `source_bound` empirical positives with zero signed substance audit and no machine gate distinguishes "identifier resolves" from "paper supports the mapped motif/world claim."

reproducer:

```powershell
Get-Content papers\falsification\DX-003\round_6_reproducers\contract_citation_semantic_probe.txt
Select-String -Path reports\campaign_023\full_report.json,reports\campaign_024\full_report.json -Pattern "source_bound|substance_audit_signed|claim_eligible|no_claim_bearing_promotion" -Context 1,1
```

expected output includes `citation_rows=30`, `resolver_rows=30`, `substance_audit_signed_true=0`, plus `claim_eligible: false` and `no_claim_bearing_promotion` gates passing.
mistake_class mapping: provenance/fake-green hybrid.
doctrine_refs: D23, D26, D29.
suggested_triage: architectural_discussion. This may be acceptable for exploratory status, but it needs a distinct display/gate state: `identifier_resolved_but_substance_unaudited`.

### R6-F3 - Instrument Held - Locked Contract DOI/PMID Strings Are Dereferenceable

severity: informational
claim: All DOI and PMID identifiers embedded directly in `formalism/motif_contracts/contracts.py` resolved through Crossref or NCBI at audit time. The failure is semantic support, not broken identifier syntax.

reproducer:

```powershell
Get-Content papers\falsification\DX-003\round_6_reproducers\contract_external_id_resolution.json
```

expected output: 22 DOI records and 8 PMID records, with resolver status/title data for every row.
mistake_class mapping: provenance via-negativa.
doctrine_refs: D17.
suggested_triage: acceptable as a survived sub-attack.

### R6-F4 - Indeterminate - Broad Repo DOI-Like Extraction Finds Malformed Substrings In Raw Source Blobs

severity: informational
claim: A broad regex over the repo found DOI-like substrings with appended `$false$<date>` and truncated parenthetical DOIs inside ITIS cache/raw exported records. Inspection showed those examples are raw `$SRC` strings or regex artifacts, not necessarily normalized DOI fields. This is not a confirmed finding yet, but it is an attack seed for a schema-aware source-citation audit.

reproducer:

```powershell
Get-Content papers\falsification\DX-003\round_6_reproducers\external_ids_extracted.txt -TotalCount 80
Get-Content papers\falsification\DX-003\round_6_reproducers\doi_shape_examples.txt -TotalCount 120
```

mistake_class mapping: hypothesis; raw-source/provenance parsing.
doctrine_refs: D23/D29.
suggested_triage: n/a until a schema-aware DOI-field scan confirms whether normalized records are affected.

## Hypotheses

- A full semantic citation audit will probably find more DOI-shaped non-evidence, especially in `EXPLORATORY` empirical-positive-world rows where broad analogies were accepted as citations.
- `source_bound` is overloaded. It currently appears to combine dereferenceability, world mapping, and support strength; those should be separate fields.
- Crossref title resolution is a cheap first-pass guard that should run before a citation becomes a contract reality anchor.

## Reproducer Artifacts

- `round_6_reproducers/external_ids_extracted.txt`
- `round_6_reproducers/doi_shape_examples.txt`
- `round_6_reproducers/contract_external_id_resolution.json`
- `round_6_reproducers/contract_external_id_resolution_preview.txt`
- `round_6_reproducers/contract_citation_semantic_probe.json`
- `round_6_reproducers/contract_citation_semantic_probe.txt`
