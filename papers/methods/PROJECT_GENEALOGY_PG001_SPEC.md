# Project Genealogy PG-001 Spec v2.1

Status: launch specification for PG-001
Authoring passes:
- v2 (OG Builder / Codex): pushbacks on v1, atom-decomposed birth predicate, DepthVector.v1, typed temporal multigraph, evidence-lock pre-pass, full schemas, falsifiability protocol, doctrine bindings, mistake-class targeting, 15 acceptance gates
- v2.1 (Architect Claude): Project Mission and coherence Pass 4, mechanical removal-probe protocol replacing reference-count heuristic, Mission Control tab integration as a required deliverable, explicit deferral of the negative-space "cloud" layer to a future ticket

Intended executor: fresh Claude Builder instance
Scope: specification only; no audit execution in this ticket

## Core Proposition

Project Genealogy is a source-bound, doctrine-aware genealogy of the Attractor Observatory codebase and artifact tree. It reconstructs why each tracked file was born, what predicate it currently appears to satisfy, how it relates to sibling and descendant files, and whether the current artifact still fulfills the original spirit rather than only the letter of its contract. It differs from ordinary dependency graphs, coverage tools, and static analyzers because its primary object is not "what imports what"; its primary object is a file's birth predicate, evidence chain, doctrine obligations, drift trajectory, and falsifiable audit findings. PG-001 is load-bearing because the project is now large enough that future builders can accidentally preserve contract surfaces while losing intent; the genealogy is the instrument that makes that loss visible before it becomes scientific debt.

One-sentence test: PG-001 is successful only if a fresh auditor can pick any dossier, rerun the cited evidence probes, and decide whether the file's current behavior still satisfies its birth predicate without trusting the AI's prose.

## Pushbacks On v1

### Pushback 1: "Spirit = first commit ticket" is too narrow

The first commit is the starting point, not the definition. Some files are renamed, split, generated, restored from private history, or born from refactors whose real predicate is inherited from a parent file. PG-001 defines spirit as the recoverable birth predicate, with a source-priority chain:

1. Explicit ticket or campaign brief cited in the creating commit, BUILD_LOG entry, or file header.
2. If the file was moved or copied, the parent file's predicate plus the split or rename rationale.
3. If the file is generated, the generator's predicate plus the generated artifact contract.
4. If no predicate can be reconstructed, `birth.status = honest_decline`; do not infer intent from current code.

One-sentence test: if the executor cannot cite the exact commit, ticket, build-log line, parent file, or generator that establishes the birth predicate, the dossier must decline reconstruction.

### Pushback 2: the proposed depth 4-tuple is gameable

The proposed axes were edge-path coverage, test density, doctrine-binding count, and audit-queue integration. Two of those are weak as written:

- Test density can reward shallow tests.
- Doctrine-binding count rewards decorative Dxx mentions.

PG-001 replaces the 4-tuple with a non-scalar `DepthVector.v1` of five measured axes:

1. `predicate_atom_coverage`: birth predicate atoms with current executable evidence divided by claimable birth predicate atoms.
2. `adversarial_surface_coverage`: known bad cases, decoys, negative paths, or exception paths with reproducers divided by required bad cases for that file's role.
3. `doctrine_binding_quality`: required doctrine bindings classified as `verified`, `claimed_only`, `missing`, `not_applicable`, or `contradicted`; this is not a count.
4. `evidence_integration`: D11/D23/D29 style source binding, artifact dereferenceability, private-boundary markers, and audit/falsifier routing.
5. `operational_load_bearingness`: number and kind of downstream artifacts that import, execute, generate from, validate with, or cite the file, weighted by edge type rather than raw count.

The vector is never compressed into an authoritative single depth score. UIs may display a selected axis or the minimum axis as an exploratory view, but the dossier and atlas keep all five axes.

One-sentence test: a file with many tests and many Dxx comments but no negative controls and no source-bound evidence must not appear deep.

### Pushback 3: Y=doctrine in the 3D map is not mechanically well-defined

A file can bind multiple doctrines or none. Mapping doctrine to a single Y coordinate forces arbitrary choice and hides cross-doctrine collisions. PG-001 uses:

- X: birth time or first-seen commit order.
- Y: artifact family or system layer, such as `world`, `factory`, `formalism`, `report`, `control_room`, `doctrine`, `test`, `script`.
- Z: selected depth axis, defaulting to `predicate_atom_coverage`.
- Color: drift status.
- Size: operational load-bearingness.
- Shape or outline: liveness status and honest-decline state.
- Doctrine: filter, facet, hover field, or edge overlay, not a primary coordinate.

One-sentence test: a file binding both D26 and D29 must be visible without choosing one doctrine and hiding the other.

### Pushback 4: three passes miss the evidence-lock step

The v1 three-pass structure starts too late. PG-001 must first bind the repository state, ticket corpus, build log, doctrine registry, and extraction rules. Otherwise a later dossier can cite moving evidence. PG-001 uses one pre-pass plus three execution passes.

One-sentence test: every dossier and atlas must name the same input manifest hash, or the run is invalid.

## Operational Definitions

### File

A file is any git-tracked path included by the PG-001 input manifest. Untracked runtime artifacts are excluded unless explicitly listed in the manifest. Ignored private implementation paths may be represented as private evidence only when D23/D29 markers are present.

One-sentence test: `git ls-files` plus the PG input filters must reproduce the audited file set.

### Birth Predicate

The birth predicate is the formal promise a file was created to satisfy, represented as a set of predicate atoms. A predicate atom has:

- `atom_id`
- `statement`
- `source_ref`
- `acceptance_evidence_expected`
- `forbidden_failure_modes`
- `doctrine_bindings_expected`

Examples:

- "Adapter emits source-bound records with provenance fields."
- "Report carries `claim_eligible=false` when Step 0 substrate suitability fails."
- "Control Room empty state displays absence rather than mock data."

One-sentence test: removing a birth predicate atom should name one specific behavior the file no longer has to satisfy.

### Current Predicate

The current predicate is the behavior the file currently exposes, reconstructed from current executable surfaces: public functions/classes, CLI commands, tests, reports generated by the file, imports, schema fields, docs that cite the file, and runtime outputs. Current predicate extraction may use docstrings and comments as hints, but not as proof.

One-sentence test: a current predicate atom must cite a current file span, exported symbol, test, generated report, or command output.

### Spirit

Spirit is the relationship between birth predicate and current predicate under doctrine. A file is spirit-preserving when current evidence satisfies the birth predicate atoms without crossing a doctrine boundary, even if implementation details changed. A file can drift positively if it deepens the predicate while preserving or explicitly superseding the birth promise.

One-sentence test: a file that still returns green but now reads an answer-bearing payload instead of the original trace evidence has violated spirit even if the surface output is unchanged.

### Drift

Drift is the atom-level difference between birth predicate and current predicate. PG-001 does not use unconstrained language embeddings as the authority. It computes:

- `missing_birth_atoms`: promised atoms absent now.
- `changed_atoms`: atoms whose thresholds, sources, or doctrine bindings changed.
- `new_atoms`: current atoms not present at birth.
- `doctrine_boundary_crossings`: changes that violate or newly invoke Dxx rules.
- `letter_vs_spirit_flags`: code surfaces that catch one literal symptom while leaving the failure mode class open.
- `negative_space_flags`: promised A/B/C where A and B exist but C silently disappeared.

Drift statuses:

- `none`: no material atom change.
- `positive_deepening`: new atoms deepen the file without weakening birth atoms.
- `neutral_refactor`: implementation changed; predicate atoms unchanged.
- `review_required`: material drift but no doctrine boundary crossed.
- `bad_drift`: missing/changed atoms cross a doctrine boundary or invalidate an acceptance criterion.
- `honest_decline`: insufficient evidence to compare.

One-sentence test: every non-`none` drift status must cite the atom diff that caused it.

### Letter-vs-Spirit Fix

A letter-coupled fix handles a specific symptom string, exception type, key name, or narrow branch while leaving the broader failure mode class unhandled. A spirit-level fix handles the class of failure and carries at least one adversarial reproducer for a nearby variant.

Detection surfaces:

- `try`/`except`, `catch`, and error-result branches.
- Regex or string matching used as a gate.
- Threshold guards.
- AST branches around schema keys, source ids, benchmark names, or report statuses.
- Tests added in the same ticket as the fix.

One-sentence test: if renaming the failing key, swapping an equivalent exception, or changing the stratum label bypasses the fix, it is letter-coupled unless the dossier shows a class-level guard.

### DepthVector.v1

Depth is the five-axis vector defined in Pushback 2. Required raw fields:

```json
{
  "predicate_atom_coverage": {
    "claimable_atoms": 0,
    "covered_atoms": 0,
    "missing_atoms": [],
    "value": null
  },
  "adversarial_surface_coverage": {
    "required_bad_cases": [],
    "covered_bad_cases": [],
    "missing_bad_cases": [],
    "value": null
  },
  "doctrine_binding_quality": {
    "required": [],
    "verified": [],
    "claimed_only": [],
    "missing": [],
    "contradicted": [],
    "not_applicable": []
  },
  "evidence_integration": {
    "source_bound_claims": 0,
    "dereferenceable_evidence_refs": 0,
    "private_evidence_refs": 0,
    "unresolved_evidence_refs": 0,
    "audit_queue_or_falsifier_route": "present|absent|not_applicable"
  },
  "operational_load_bearingness": {
    "imports_in": 0,
    "imports_out": 0,
    "generates_artifacts": [],
    "validated_by": [],
    "cited_by_reports": [],
    "weighted_value": 0.0
  }
}
```

One-sentence test: depth can be low because any one axis is low; PG-001 must not hide a weak axis behind strong ones.

### Genealogy Relationships

The genealogy graph is a typed temporal multigraph, not a DAG and not a forest.

Reason: birth/spawn edges should be acyclic by commit time, but runtime imports, validation loops, report citations, and generated-artifact relationships can cycle. Forcing a DAG would erase real feedback loops.

Required edge types:

- `spawned_by_ticket`: file born from ticket/campaign/driver.
- `derived_from_file`: split, copy, move, or refactor from another file.
- `generated_by`: artifact produced by a script or validator.
- `imports`: code import.
- `executes`: CLI, test, or scheduler executes another file.
- `validates`: test/report validates file behavior.
- `cites`: docs/reports cite file as evidence.
- `shares_birth_cohort`: files born in the same ticket.
- `implements_same_doctrine`: files claim or enforce the same Dxx rule.
- `contradicts_doctrine_peer`: detected collision between files binding the same doctrine.

Definitions:

- Parent: a ticket, file, or generator with a direct birth or derivation edge into the file.
- Child: inverse of parent, later by first-seen commit or generation timestamp.
- Sibling: file sharing a birth ticket, source parent, or generator.
- Cohort: all files sharing the same spawn ticket or generated run.

One-sentence test: if two files import each other, the runtime graph may cycle, but their birth edges must still have time direction or honest decline.

### Project Mission

The project mission is the apex predicate the entire codebase exists to satisfy. It sits one level above cohorts: variable -> file -> cohort -> mission. For Attractor Observatory the mission is to be a substrate-neutral computational research instrument that detects the named motifs across stratified substrates under predicate-lens-independent methodology, with research-grade evidence discipline.

The mission is itself a set of `mission_atoms` reconstructed from existing artifacts in the pre-pass. PG-001 does not invent mission atoms. Allowed sources, in priority order:

1. The doctrine corpus (`docs/DOCTRINE.md`, `docs/doctrine_*.md`, `docs/doctrine_registry.json`).
2. Active campaign drivers (`CODEX_*.md`, `TASK-*.md`, `DX-*.md`, `CLAUDE_*.md`).
3. `BUILD_LOG.md` headers and ratification entries.
4. The project README and architectural method documents under `papers/methods/`.

Each mission atom requires:

- `mission_atom_id`
- `statement`
- `source_refs` (which doctrine line, which campaign brief, which BUILD_LOG entry)
- `expected_artifact_families` (which artifact_family layers should serve this atom; e.g., `world`, `factory`, `formalism`, `report`, `control_room`)
- `expected_drift_constraint` (under what change does drift away from this atom become bad)

If a candidate mission claim cannot be tied to source refs, it is declined as `mission_atom_insufficient_source`. If it ties to sources but cannot name expected artifact families, it is declined as `mission_atom_too_abstract`. Declines are first-class outputs; an audit running on a project with unclear mission must say so.

One-sentence test: a mission atom must cite at least one specific source ref and name at least one expected artifact_family, or it is declined.

## Curation Of The Twelve Proposed Axes

| Axis | Decision | PG-001 treatment | Reason |
|---|---|---|---|
| Letter-vs-spirit fix detection | Accept as core | Required drift sub-analysis for error handlers, threshold guards, regex/string gates, and tests born in bug-fix tickets. | This is the PI's kill-shot pattern and maps directly to Classes 2, 3, 6, 11, and 13. |
| Negative-space drift | Accept as core | Required `missing_birth_atoms` and `negative_space_flags`. | The absence of promised C is invisible without predicate atom reconstruction. |
| Death detection | Accept, scoped | Emit `liveness.cleanup_candidate`, never delete or queue destruction in PG-001. | Useful, but cleanup is a downstream Destroyer task. |
| Multi-temporal audit | Accept, narrowed | Use birth -> peak-clarity -> now only when peak-clarity can be mechanically identified. | Valuable trajectory signal; fuzzy "best version" would be vibes. |
| Falsifiability per claim | Accept with constraint | Every finding needs a reproducer. Narrative summaries need evidence refs but not every sentence is a finding. | Achievable for findings, not for all prose without absurd overhead. |
| D11 compliance for audit itself | Accept as core | Every finding and predicate atom carries evidence refs; source-less claims become hypotheses or declines. | The audit must be an evidence artifact. |
| Cross-doctrine collision detection | Accept as core | Required cross-file pass over files claiming or enforcing the same Dxx. | Directly targets Class 13 and doctrine drift. |
| Cohort analysis | Accept as core (extended in Pass 4) | Required cohort summaries and sibling consistency checks; cohort alignment to mission atoms is computed in the project-level coherence pass. | Files born together share intent; cohort-level drift is stronger than isolated drift, and cohort-level alignment to mission is the apex coherence signal. |
| Mistake-class mapping | Accept as core | Every finding maps to Class 1-13 or `unmapped_candidate`. | Keeps the audit connected to observed failure modes. |
| Query API | Accept as core | Required Python API plus CLI query wrappers. | The research value is in interrogation, not only visualization. |
| Living artifact with hooks | Accept, phased | Versioned atlases required; PR/CI hook specified but can run advisory in v1. | Hard-blocking CI on a new genealogy instrument is premature. |
| Honest decline | Accept as core | Required decline taxonomy and decline counts in atlas. | Prevents AI interpolation from becoming fake evidence. |

One-sentence test: if an axis cannot produce machine-readable evidence or an honest decline, it does not enter PG-001 as a finding source.

## Dossier Schema

Schema name: `ProjectGenealogyDossier.v1`

Path:

- JSON: `reports/project_genealogy/dossiers/<safe_path>.json`
- Markdown: `reports/project_genealogy/dossiers/<safe_path>.md`

The JSON is authoritative. The Markdown is a human-readable rendering and must carry the JSON `content_hash`.

Required JSON fields:

```json
{
  "schema": "ProjectGenealogyDossier.v1",
  "file": {
    "path": "",
    "path_hash": "",
    "tracked": true,
    "language": "",
    "artifact_family": "",
    "line_count": 0,
    "byte_count": 0,
    "generated_status": "source|generated|report|unknown",
    "private_boundary": {
      "evidence_private": false,
      "reason": ""
    }
  },
  "run_binding": {
    "input_manifest_hash": "",
    "branch": "",
    "head_commit": "",
    "workspace_dirty": true,
    "generated_at": "",
    "generation_command": "",
    "pg_version": "PG-001"
  },
  "birth": {
    "status": "recovered|honest_decline",
    "first_seen_commit": "",
    "first_seen_date": "",
    "spawn_ticket": "",
    "birth_cohort_id": "",
    "parent_refs": [],
    "evidence_refs": [],
    "decline_reason": "",
    "birth_predicate": {
      "predicate_id": "",
      "atoms": [],
      "acceptance_criteria": [],
      "forbidden_patterns": [],
      "expected_doctrine_bindings": [],
      "content_hash": ""
    }
  },
  "current": {
    "status": "recovered|partial|honest_decline",
    "evidence_refs": [],
    "current_predicate": {
      "predicate_id": "",
      "atoms": [],
      "public_symbols": [],
      "commands": [],
      "generated_artifacts": [],
      "observed_doctrine_bindings": [],
      "content_hash": ""
    },
    "decline_reason": ""
  },
  "genealogy": {
    "parents": [],
    "children": [],
    "siblings": [],
    "cohort": {
      "cohort_id": "",
      "spawn_ticket": "",
      "members": []
    },
    "edges": []
  },
  "depth": {},
  "drift_assessment": {
    "status": "none|positive_deepening|neutral_refactor|review_required|bad_drift|honest_decline",
    "missing_birth_atoms": [],
    "changed_atoms": [],
    "new_atoms": [],
    "doctrine_boundary_crossings": [],
    "letter_vs_spirit_flags": [],
    "negative_space_flags": [],
    "reproducer_refs": []
  },
  "liveness": {
    "last_touched_commit": "",
    "last_touched_date": "",
    "downstream_reference_count": 0,
    "runtime_reference_count": 0,
    "cleanup_candidate_status": "unknown|removable_clean|removable_with_warnings|not_removable|probe_declined",
    "cleanup_reason": "",
    "removal_probe": {
      "ran_at": "",
      "command": "",
      "outcome": "",
      "diff_summary": "",
      "evidence_refs": [],
      "decline_reason": ""
    }
  },
  "consistency": {
    "cohort_findings": [],
    "cross_doctrine_collisions": [],
    "sibling_divergence": []
  },
  "findings": [],
  "declines": [],
  "content_hash": ""
}
```

Required `evidence_ref` shape:

```json
{
  "ref_id": "",
  "kind": "commit|build_log|ticket|file_span|test|report|command|schema|private",
  "locator": "",
  "content_hash": "",
  "evidence_private": false,
  "note": ""
}
```

Required `finding` shape:

```json
{
  "finding_id": "",
  "severity": "info|low|medium|high|critical",
  "status": "confirmed|hypothesis|honest_decline|resolved_by_current_state",
  "claim": "",
  "mistake_classes": [],
  "doctrine_refs": [],
  "evidence_refs": [],
  "reproducer": {
    "kind": "command|git_query|grep|ast_probe|json_query|manual_decline",
    "command": "",
    "expected_result": "",
    "last_run_status": "pass|fail|not_run|not_applicable"
  },
  "recommendation": ""
}
```

Content-hash discipline:

- `content_hash` is SHA-256 over canonical JSON excluding the `content_hash` field itself.
- Markdown dossiers must name the JSON path and JSON content hash.
- If the repository is dirty, `workspace_dirty=true` is allowed but the dirty file list must be in the run manifest.

One-sentence test: deleting the Markdown dossier must not remove any machine-readable claim; deleting the JSON dossier must invalidate the Markdown rendering.

## Atlas Schema

Schema name: `ProjectGenealogyAtlas.v1`

Paths:

- Versioned: `reports/project_genealogy/atlas_<YYYYMMDDTHHMMSSZ>.json`
- Pointer: `reports/project_genealogy/atlas_latest.json`

Required fields:

```json
{
  "schema": "ProjectGenealogyAtlas.v1",
  "run_binding": {
    "input_manifest_hash": "",
    "branch": "",
    "head_commit": "",
    "workspace_dirty": true,
    "generation_command": "",
    "generated_at": "",
    "freshness_status": "computed_at_read|stale|unknown"
  },
  "summary": {
    "file_count": 0,
    "dossier_count": 0,
    "decline_count": 0,
    "confirmed_finding_count": 0,
    "bad_drift_count": 0,
    "cleanup_candidate_count_by_status": {},
    "cohort_count": 0,
    "edge_count_by_type": {},
    "depth_axis_distributions": {},
    "drift_status_counts": {},
    "mission_atom_count": 0,
    "mission_coverage_status_counts": {},
    "cohort_alignment_status_counts": {},
    "coherence_report_path": "",
    "coherence_report_hash": ""
  },
  "nodes": [],
  "edges": [],
  "cohorts": [],
  "doctrine_index": {},
  "ticket_index": {},
  "mistake_class_index": {},
  "liveness_index": {},
  "query_materializations": {},
  "declines": [],
  "content_hash": ""
}
```

Required node shape:

```json
{
  "node_id": "",
  "path": "",
  "artifact_family": "",
  "birth_time": "",
  "spawn_ticket": "",
  "dossier_path": "",
  "dossier_hash": "",
  "depth": {},
  "drift_status": "",
  "load_bearingness": 0.0,
  "doctrine_refs": [],
  "mistake_classes": [],
  "cleanup_candidate": false,
  "honest_decline": false
}
```

Required edge shape:

```json
{
  "edge_id": "",
  "edge_type": "",
  "source": "",
  "target": "",
  "evidence_refs": [],
  "confidence": "mechanical|strong|weak|honest_decline",
  "created_at_commit": "",
  "private_boundary": {
    "evidence_private": false,
    "reason": ""
  }
}
```

One-sentence test: the atlas graph must be reconstructable from dossier JSON files and the input manifest without reading prose.

## Project Coherence Report Schema

Schema name: `ProjectCoherenceReport.v1`

Paths:

- Versioned: `reports/project_genealogy/coherence_<YYYYMMDDTHHMMSSZ>.json`
- Pointer: `reports/project_genealogy/coherence_latest.json`

Required fields:

```json
{
  "schema": "ProjectCoherenceReport.v1",
  "run_binding": {
    "input_manifest_hash": "",
    "atlas_hash": "",
    "branch": "",
    "head_commit": "",
    "generated_at": ""
  },
  "mission": {
    "mission_predicate_id": "",
    "atoms": [],
    "source_refs": [],
    "content_hash": ""
  },
  "coverage_by_atom": [
    {
      "mission_atom_id": "",
      "statement": "",
      "expected_artifact_families": [],
      "serving_cohorts": [],
      "serving_files": [],
      "coverage_status": "covered|partial|orphan|declined",
      "evidence_refs": [],
      "decline_reason": ""
    }
  ],
  "cohort_alignment": [
    {
      "cohort_id": "",
      "spawn_ticket": "",
      "members": [],
      "served_mission_atoms": [],
      "alignment_status": "aligned|partial|drifted|unmapped|declined",
      "evidence_refs": [],
      "decline_reason": ""
    }
  ],
  "trajectory": {
    "compared_atlas_versions": [],
    "atoms_with_strengthening_drift": [],
    "atoms_with_weakening_drift": [],
    "trajectory_status": "improving|stable|degrading|insufficient_history|declined"
  },
  "findings": [],
  "declines": [],
  "content_hash": ""
}
```

Coherence findings reuse the standard `finding` shape from the dossier schema, including reproducer requirements. A mission-coverage finding's reproducer is typically a `json_query` against the atlas plus dossier hashes.

One-sentence test: every `coverage_by_atom` entry must either name serving cohorts/files or carry `coverage_status=orphan|declined` with a reason; mission atoms cannot quietly disappear from the report.

## Query API Surface

Module name: `project_genealogy.query`

Required Python API:

```python
from pathlib import Path
from typing import Literal

class GenealogyIndex:
    @classmethod
    def load(cls, atlas_path: str | Path) -> "GenealogyIndex": ...

    def dossier(self, path: str) -> dict: ...

    def files(
        self,
        *,
        path_glob: str | None = None,
        artifact_family: str | None = None,
        doctrine: str | None = None,
        ticket: str | None = None,
        drift_status: str | None = None,
        mistake_class: str | None = None,
        cleanup_candidate: bool | None = None,
        honest_decline: bool | None = None,
    ) -> list[dict]: ...

    def parents(self, file_path: str, *, edge_types: list[str] | None = None) -> list[dict]: ...
    def children(self, file_path: str, *, edge_types: list[str] | None = None) -> list[dict]: ...
    def siblings(self, file_path: str, *, relation: Literal["birth_cohort", "parent", "doctrine"] = "birth_cohort") -> list[dict]: ...
    def cohort(self, *, ticket: str | None = None, cohort_id: str | None = None) -> dict: ...
    def orphans(self, *, kind: Literal["no_birth_predicate", "no_runtime_refs", "no_parent"] = "no_birth_predicate") -> list[dict]: ...
    def findings(
        self,
        *,
        severity: str | None = None,
        status: str | None = None,
        mistake_class: str | None = None,
        doctrine: str | None = None,
        reproducible: bool | None = None,
    ) -> list[dict]: ...

    def doctrine_collisions(self, doctrine: str | None = None) -> list[dict]: ...
    def depth_outliers(self, *, axis: str, bottom_n: int = 20) -> list[dict]: ...
```

Required CLI wrappers:

```powershell
python -m project_genealogy.query files --doctrine D26 --drift bad_drift
python -m project_genealogy.query siblings --file factory_lowlevel/adapters.py
python -m project_genealogy.query cohort --ticket TASK-SOURCE-OBJ-GEN
python -m project_genealogy.query orphans --kind no_birth_predicate
python -m project_genealogy.query findings --mistake-class Class13 --reproducible true
```

One-sentence test: every query result row must include `path`, `dossier_path`, `dossier_hash`, and the evidence field that made it match.

## 3D Visualization Contract

The visualization is an atlas entry point, not an evidence source.

Required:

- Load only `ProjectGenealogyAtlas.v1` and linked dossier JSON files.
- Render one node per audited file.
- Render typed edges with filters by edge type.
- Default coordinates:
  - X: birth order or first-seen time.
  - Y: artifact family/system layer.
  - Z: selected depth axis, default `predicate_atom_coverage`.
  - Color: drift status.
  - Size: operational load-bearingness.
  - Shape/outline: liveness and honest-decline state.
- Hover shows path, spawn ticket, depth vector summary, drift status, top finding, and content hash.
- Click opens the dossier.
- Empty or missing data must render via honest empty state; no mock nodes.

Nice-to-have:

- Cohort hulls or group outlines.
- Doctrine filter overlays.
- Side-by-side diff between atlas versions.

Out of scope for v1:

- Force-directed layouts as evidence.
- AI-generated relationship edges not present in atlas JSON.
- 3D screenshots as proof of project health.
- Destroyer queue creation.

One-sentence test: changing the 3D layout must not change any audit conclusion.

### Mission Control Integration

PG-001 ships a Streamlit Control Room tab named `Project Genealogy`. The tab is part of the existing Mission Control under `control_room/` and lives behind the same heartbeat-keyed token, autorefresh policy, and freshness-computed-at-read discipline as the rest of the dashboard.

Required contract:

- Tab loads only `reports/project_genealogy/atlas_latest.json` and the linked dossier JSON files. No mock or placeholder data; D22 absence-honest empty state when artifacts are missing.
- Renders one Plotly `Scatter3d` trace per visible artifact_family with one marker per audited file under the default coordinates from the 3D Visualization Contract above (X: birth time, Y: artifact_family, Z: selected depth axis, color: drift_status, size: operational_load_bearingness, marker outline: liveness/honest-decline state).
- Renders typed edges as Plotly 3D line traces filterable by edge type. Default visible edge types: `derived_from_file`, `spawned_by_ticket`, `contradicts_doctrine_peer`. All ten edge types selectable.
- The view supports orbit, zoom, and pan; the Streamlit user resets view to the deterministic default with a one-click control.
- Hover panel surfaces path, spawn_ticket, DepthVector summary (all five axes), drift_status, top finding (severity + claim + reproducer.last_run_status), and dossier_hash.
- Click on a node opens the corresponding Markdown dossier in a side drawer or new section of the same page. The drawer never edits dossier content.
- Filters surfaced in the sidebar: doctrine, drift_status, mistake_class, cohort, artifact_family, cleanup_candidate_status, honest_decline.
- Time slider over versioned `atlas_<timestamp>.json` files in `reports/project_genealogy/`. When only one atlas exists, the slider is disabled with an honest "single snapshot" empty state.
- Mission Coherence panel: shows mission atoms, `coverage_status` per atom (covered/partial/orphan/declined), cohort alignment heatmap, and trajectory verdict; all read from `coherence_latest.json` only.
- A "Removable Files" panel lists `cleanup_candidate_status` distribution and the file list per status; each row shows the removal_probe outcome and links to the dossier. PG-001 surfaces candidates; it does not propose deletions.
- Counts shown in any panel must equal counts in `atlas_latest.json` and `coherence_latest.json`. If they differ the tab renders a degraded-state banner naming the mismatch; it does not silently reconcile.

Out of scope for v1:

- Force-directed re-layouts that aren't deterministic from atlas data.
- AI-generated relationship suggestions inside the tab.
- Editing dossier, atlas, or coherence content from the tab.
- Triggering audit reruns from the tab (audit reruns are CLI-only in v1).

One-sentence test: closing and reopening the tab against the same `atlas_latest.json` and `coherence_latest.json` must produce an identical render; nondeterminism in coordinates, counts, or finding lists is a bug.

## Execution Plan

PG-001 uses one pre-pass plus three execution passes.

### Pre-pass: Evidence Lock

Inputs:

- `git ls-files`
- `git log --follow --name-status`
- `BUILD_LOG.md`
- `CODEX_*.md`, `TASK-*.md`, `DX-*.md`, `CLAUDE_*.md`
- `docs/DOCTRINE.md` and `docs/doctrine_*.md`
- `docs/doctrine_registry.json`
- current public tests and report summaries

Outputs:

- `reports/project_genealogy/input_manifest.json`
- manifest content hash
- file inclusion/exclusion filters
- dirty-worktree list
- doctrine registry binding
- ticket/build-log index

Acceptance criteria:

- Manifest names branch, commit, dirty status, generation command, and all input files.
- Every later dossier cites the same manifest hash.
- Missing private paths are represented as D23/D29 boundaries, not silently ignored.

One-sentence test: rerunning the pre-pass at the same HEAD with the same filters produces the same manifest hash, except for allowed generated timestamp fields excluded from the hash.

### Pass 1: Structural Genealogy

Inputs:

- input manifest
- git history
- imports and execution references
- generated-artifact references
- report citations

Outputs:

- preliminary atlas nodes
- typed edge list
- cohort index
- parent/child/sibling candidates
- unresolved relationship declines

Acceptance criteria:

- Every tracked included file has one node.
- Every edge has an evidence ref.
- Birth/spawn edges are time-directed or declined.
- Runtime/import/citation cycles are allowed and typed.

One-sentence test: a file with no recoverable parent still appears as a node with `birth.status=honest_decline`, not as an omitted file.

### Pass 2: Per-File Predicate, Depth, And Drift

Inputs:

- Pass 1 graph
- ticket/build-log index
- current file content
- tests/reports/commands cited by the file
- doctrine registry

Outputs:

- one `ProjectGenealogyDossier.v1` JSON per file
- one Markdown rendering per dossier
- per-file findings and declines

Acceptance criteria:

- Every dossier has birth predicate or honest decline.
- Every current predicate atom has evidence.
- Every drift finding cites atom diffs and a reproducer.
- Every depth vector axis is filled or declined.
- Letter-vs-spirit analysis runs on every detected error-handler/fix surface.

One-sentence test: a dossier with a confirmed finding but no reproducer is invalid.

### Pass 3: Cross-File Consistency, Atlas, And Query Publication

Inputs:

- all dossiers
- Pass 1 graph
- doctrine registry
- mistake catalog

Outputs:

- versioned `ProjectGenealogyAtlas.v1`
- `atlas_latest.json`
- query index
- cross-doctrine collision report
- cohort drift report
- liveness cleanup-candidate report

Acceptance criteria:

- All dossier hashes in atlas resolve.
- Cohort summaries include all sibling files.
- Cross-doctrine collision detector reports zero or findings with reproducers.
- Query API answers the required examples.
- Public tests cover schema, query API, honest declines, and no-mock visualization data.

One-sentence test: deleting one dossier causes atlas validation to fail, not silently shrink the graph.

### Pass 4: Project-Level Coherence

Inputs:

- atlas from Pass 3
- mission predicate (mission atoms + source refs) from input manifest
- versioned atlas history under `reports/project_genealogy/` for trajectory analysis
- doctrine registry

Outputs:

- `ProjectCoherenceReport.v1` versioned + `coherence_latest.json` pointer
- atlas summary updated with `mission_atom_count`, `mission_coverage_status_counts`, `cohort_alignment_status_counts`, and `coherence_report_path/hash`
- mission-coverage and cohort-alignment findings routed back into per-file dossiers where a specific file is implicated, with reproducer ref to the coherence report

Acceptance criteria:

- Every mission atom has either serving cohorts/files or `coverage_status ∈ {orphan, declined}` with a reason.
- Every cohort has either served mission atoms or `alignment_status ∈ {unmapped, declined}` with a reason.
- Trajectory analysis runs when at least two prior atlases exist; otherwise marks `trajectory_status=insufficient_history` honestly. Trajectory degradation findings cite specific atom diffs across atlas versions.
- No prose-only mission claims; every coverage assertion cites cohort_id, file dossier_hash, or atom diff evidence.
- Coherence findings reuse the standard `finding` shape and reproducer requirements.

One-sentence test: a mission atom marked `covered` must name at least one serving file with a dossier hash; abstract or prose-only claims of coverage are forbidden.

## Falsifiability Protocol

Every confirmed finding must include a reproducer. A reproducer is a minimal deterministic way to re-derive the finding from the bound input manifest.

Allowed reproducer kinds:

- `command`: exact shell command, expected exit code, expected key output.
- `git_query`: exact `git log`, `git show`, or `git diff` command.
- `grep`: exact pattern and expected count or location.
- `ast_probe`: named parser, selector, and expected node match.
- `json_query`: JSON path or jq-like path plus expected value.
- `manual_decline`: used only when no mechanical reproducer is possible; finding status must be `honest_decline` or `hypothesis`, not `confirmed`.

Bias controls:

1. Extraction and judgment are separate artifacts. Evidence extraction creates predicate atoms and source refs. Finding detectors consume those atoms; they do not invent evidence in prose.
2. Prose renderers cannot introduce facts absent from JSON.
3. Thresholds for drift, liveness, and load-bearingness are declared in the input manifest before findings are emitted.
4. If a finding maps to Class 10 or Class 11, the dossier must decompose where the apparent property comes from, not just whether the corpus has it.
5. If the current file is private or ignored, the public dossier may cite it only with `evidence_private=true` and cannot claim public reproducibility.

One-sentence test: if an auditor cannot rerun or inspect the reproducer, the finding cannot be `confirmed`.

## Removal Probe Protocol

The `liveness.cleanup_candidate_status` field requires mechanical evidence, not reference-count heuristics. Reference counts are necessary but not sufficient: a file with zero imports may still be a CLI entry point, a generated artifact, a fixture loaded by name, or a private boundary marker. PG-001 distinguishes "looks unreferenced" from "removable without breaking verifiable behavior."

Per-file removal probe:

1. Stash the file in isolation (`git stash push <path>` or equivalent worktree-local move that does not touch other files).
2. Run the public test suite: `python -m pytest public_tests/ -q`.
3. Run any `artifact_family` smoke commands declared in the input manifest's probe registry. Examples:
   - `factory` family: `python -m factory_lowlevel.continuous_daemon --dry-run --cycles 0`
   - `report` family: re-validate any report-summary integrity checks that the file claims to feed.
   - `control_room` family: `python -c "from control_room.launcher import main"` import-smoke, plus a deterministic Streamlit AppTest render where applicable.
4. Capture pass/fail and an output diff vs the pre-stash baseline.
5. Restore the file (`git stash pop`).

Outcomes recorded in `liveness.removal_probe`:

- `removable_clean`: tests pass and registered smokes pass with diff_summary empty.
- `removable_with_warnings`: tests pass and smokes pass but observed output diffs in non-error fields (logs, ordering, timings); human review required before any cleanup.
- `not_removable`: tests fail or registered smokes break; the file is load-bearing even if reference counts are low.
- `probe_declined`: the file sits on a critical path where probing would risk irreversible state. Manifest must list these paths explicitly.

Required `probe_declined` paths in the input manifest's probe registry include at minimum:

- Persistence layer (anything that writes `factory_store/`, `daemon_state.json`, or `.daemon_lock`).
- Lock acquisition / safety modules (`factory_lowlevel/launch_safety.py` and equivalents).
- Schema definition modules whose removal would invalidate validation across the tree.
- Adapters whose removal would silently drop substrate coverage (verify by Pass 1 import + spawn graph).
- Test files themselves (probing a test by deleting it is meta-circular).
- Files inside private gitignored paths (`worlds/`, `motifs/`, etc.) — these get `evidence_private=true` and the probe is declined under D23.

The probe is itself the reproducer for any non-`unknown` `cleanup_candidate_status`. Without a recorded probe, the status defaults to `unknown` and the file is excluded from the cleanup_candidates list. PG-001 does not delete files; the Removable Files panel lists candidates with their probe outcomes for human triage.

If running the full probe is too expensive in a single PG-001 run (e.g., thousands of files), the manifest may declare a probe-budget. Files exceeding the budget are recorded as `unknown` rather than `removable_clean`; under-claimed status is permitted, over-claimed is not.

One-sentence test: a `cleanup_candidate_status ∈ {removable_clean, removable_with_warnings, not_removable}` finding without a corresponding `removal_probe.outcome` and recorded `command` is invalid and must be downgraded to `unknown`.

## Doctrine Bindings

PG-001 directly binds to:

- D7: depth cannot be satisfied by surface files without substance evidence.
- D9: drift/depth thresholds must be declared before running the audit, not tuned afterward.
- D10: project labels such as "world", "lens", "factory", or "genealogy" are not evidence without operational predicates.
- D11: every audit claim needs an evidence chain; stale or source-less claims are downgraded.
- D12: gates are measurements, not counts; "all files scanned" is a precondition, not a quality gate.
- D13: PG itself records substance of generated reports, query code, tests, and visualization.
- D17/D17.5: falsifiers and caveats are surfaced as first-class outputs; proxy line floors do not override substance audits.
- D18: run manifest and thresholds are locked before dossier findings.
- D19: extraction is source-bound; AI is not an evidence source.
- D20: extraction/detection separation applies to PG itself.
- D22: visualization and dashboards show absence honestly.
- D23/D29: every evidence path resolves or carries a private/unshipped marker.
- D24/D30: atlas and sidecars bind freshness at read time.
- D25: public docs only claim public verification when shipped.
- D26: birth predicate extraction and current predicate judgment declare source-object maps; self-matching is flagged.
- D27: a file is not considered recovered by cosmetic renaming or interface movement.
- D31: if floor-connectivity artifacts are audited, PG must respect D31 row/field separation and cannot collapse predicate and lens surfaces.

Compliance checks:

- `pg_manifest_thresholds_locked`: thresholds and filters exist before Pass 2.
- `pg_evidence_ref_resolves_or_private`: all evidence refs pass D23/D29.
- `pg_no_prose_only_findings`: all confirmed findings have JSON evidence and reproducer.
- `pg_no_mock_viz_data`: visualization node/edge counts equal atlas node/edge counts; coherence panel counts equal `coherence_latest.json` counts.
- `pg_source_object_independence`: birth/current predicate comparisons declare source surfaces and overlap status.
- `pg_mission_atoms_traceable`: every mission atom resolves to at least one source ref in the doctrine corpus, BUILD_LOG, campaign drivers, or method documents; AI-invented mission atoms are forbidden.
- `pg_removal_probe_evidence`: every non-`unknown` `cleanup_candidate_status` has a recorded `removal_probe` with command and outcome.

One-sentence test: PG-001 cannot criticize predicate-lens coupling in the project while using prose-only self-matched evidence in its own findings.

## Mistake-Class Targeting

PG-001 targets the observed mistake catalog as follows:

| Class | Detected evidence |
|---|---|
| Class 1 Static-input contamination | Current predicate or detector reads config, expected labels, scenario payloads, or report verdicts that contain the answer. Emits source-overlap finding and AST/file-span reproducer. |
| Class 2 Direction inversion | Gate/test comparison fails adversarial sanity check or expected-bad fixture. Emits command/json reproducer showing bad input passes. |
| Class 3 Soft enforcement, strict display | Displayed threshold differs from enforced code threshold. Emits pair of refs: report threshold and code threshold. |
| Class 4 Scenario-internal hardcoding | AST branch on benchmark/scenario/source id inside step/update/apply/mutation path writes state. Emits AST reproducer. |
| Class 5 Surface coverage without substance | Birth predicate atoms absent despite file/report/test presence. Emits missing atom list and shallow-test evidence. Pass 4 also emits a Class 5 candidate when a cohort claims to serve a mission atom but its member dossiers lack the predicate atoms that mission atom requires. |
| Class 6 Engineered passing | Thresholds or coefficients appear tuned to expected outputs without locked null/spec source. Emits threshold provenance decline or reproducer. |
| Class 7 Surface labels as primitives | Label used as evidence without operational predicate. Emits label surface and missing predicate atom. |
| Class 8 Abstract scalar standing in | Scalar/summary object substitutes for richer state promised by birth predicate. Emits promised-rich-object atom and current scalar evidence. |
| Class 9 Spec-detail mismatch | Header counts, gate lists, summaries, and tables disagree. Emits count reproducer. |
| Class 10 Test-architecture/substrate-presence mismatch | File/test measures a property on corpus/artifact where property is absent. Emits Step 0 property-presence probe. |
| Class 11 Categorical confound through pooling | Aggregate signal arises between readable strata rather than within them. Emits stratum decomposition and blocked-control status. |
| Class 12 Decorative completeness | UI/report fills absent data with mock or placeholder content. Emits missing artifact plus rendered/display path. |
| Class 13 Predicate-detector surface coupling | Predicate and detector/current audit judgment read same source object fields. Emits source-object map overlap. |

If a finding does not map cleanly, use `mistake_class: unmapped_candidate` with `candidate_class_rationale`; do not invent Class 14 in PG-001.

One-sentence test: a finding without mistake-class mapping or explicit `unmapped_candidate` is incomplete.

## Honest Declines

Required decline reasons:

- `birth_predicate_not_recoverable`
- `current_predicate_not_recoverable`
- `private_history_unavailable`
- `generated_artifact_without_generator_binding`
- `ambiguous_parentage`
- `no_mechanical_reproducer`
- `file_out_of_scope_by_manifest`
- `public_runtime_boundary`
- `doctrine_mapping_ambiguous`
- `mission_atom_insufficient_source`
- `mission_atom_too_abstract`
- `removal_probe_declined_critical_path`
- `removal_probe_over_budget`
- `trajectory_insufficient_history`

Declines are counted in the atlas and rendered in the 3D view. A decline is not a failure of PG-001; a fabricated reconstruction is.

One-sentence test: the number of declines must be visible in the atlas summary and queryable.

## Out Of Scope For PG-001

PG-001 does not:

- Build or run the Destroyer queue.
- Delete files or propose automatic refactors. The Removable Files panel is a candidate list, never a deletion order.
- Prove line-by-line semantic correctness.
- Replace the test suite, type checker, or static analyzer.
- Run full mutation testing.
- Audit untracked ignored runtime dumps unless explicitly in the manifest.
- Treat AI narrative as evidence.
- Promote any scientific claim because a code genealogy looks healthy.
- Make the 3D visualization a truth surface.
- Require a hard-blocking CI gate on every PR in v1; advisory CI is enough until false-positive behavior is measured.
- Map the project's negative-space "extrapolation surface" — what the project is NOT but could become. PG-001 audits interior fidelity to the existing mission. The exterior potential / cloud layer is a separate audit philosophy and a future ticket (PG-002 or NS-001). The `positive_deepening` drift status is the only mechanism in this spec that accommodates beneficial growth toward the mission; mapping the unrealized surface is explicitly deferred to preserve the research instrument's openness while PG-001 is bedded in.

One-sentence test: if a proposed PG-001 output would change project code, delete files, promote science, or harden the project against directions it has not yet explored, it belongs to a downstream ticket.

## Acceptance Gates

PG-001 implementation must pass:

1. `PG1_manifest_locked`: input manifest exists and all dossiers cite its hash.
2. `PG2_all_tracked_files_accounted`: every included git-tracked file has dossier or explicit manifest exclusion.
3. `PG3_birth_predicate_or_decline`: every dossier has birth predicate or honest decline.
4. `PG4_current_predicate_or_decline`: every dossier has current predicate or honest decline.
5. `PG5_depth_vector_complete`: all five depth axes filled or declined.
6. `PG6_drift_atom_diff`: every drift status other than `none` cites atom diffs.
7. `PG7_findings_falsifiable`: every confirmed finding has a reproducer.
8. `PG8_evidence_refs_bound`: evidence refs resolve or carry private markers.
9. `PG9_no_mock_viz`: visualization data equals atlas data; no synthetic filler.
10. `PG10_query_api_examples`: required query examples execute against the atlas.
11. `PG11_cohort_consistency`: birth cohorts are indexed and queryable.
12. `PG12_cross_doctrine_collision_pass`: collisions are reported or zero with evidence.
13. `PG13_mistake_class_mapping`: every finding maps to Class 1-13 or `unmapped_candidate`.
14. `PG14_public_verification_honesty`: public claims name shipped tests/scripts or private boundary.
15. `PG15_versioned_atlas`: versioned atlas and latest pointer exist with freshness binding.
16. `PG16_mission_atoms_locked`: input manifest contains mission atoms with source refs; the `ProjectCoherenceReport.v1` and every coherence finding cite the same mission predicate hash.
17. `PG17_mission_coverage_complete`: every mission atom has either serving cohorts/files or `coverage_status ∈ {orphan, declined}` with a recorded reason; every cohort has either served mission atoms or `alignment_status ∈ {unmapped, declined}` with a reason.
18. `PG18_removal_probe_evidence`: every `cleanup_candidate_status ∈ {removable_clean, removable_with_warnings, not_removable}` has a `removal_probe` with `command` and `outcome`; bare `unknown` and `probe_declined` are allowed and counted in the atlas summary.
19. `PG19_control_room_tab_renders`: the Mission Control `Project Genealogy` tab renders deterministically from `atlas_latest.json` and `coherence_latest.json`, surfaces honest empty state when artifacts are absent, and reports node/edge/coverage counts equal to the underlying JSON.
20. `PG20_trajectory_history_honest`: trajectory analysis runs when at least two prior atlases exist; otherwise the report records `trajectory_status=insufficient_history` rather than a fabricated verdict.

One-sentence test: PG-001 is not complete because it wrote dossiers; it is complete when the twenty gates above are measured and green or honestly declined with reasons.

## Launch Instruction For Fresh Claude

Read this spec first, then read `CLAUDE_BUILDER_INITIATION.md` mistake catalog, `docs/DOCTRINE.md`, `docs/doctrine_registry.json`, and `BUILD_LOG.md`. Sample several `papers/methods/*.md` documents and recent `CODEX_*.md` / `TASK-*.md` drivers so the mission-atom reconstruction has the corpus it needs.

Do not run the genealogy audit until the pre-pass has produced a locked input manifest containing the file inclusion filters, the threshold policy, the mission atom set with source refs, the artifact_family probe registry for the removal probe, and the explicit list of `probe_declined` critical paths.

If any field in this spec is impossible to populate mechanically, write a BLOCKER-PG001 note rather than filling it with interpretation. The honest-decline taxonomy exists for exactly this case; use it.

The Mission Control tab is part of the v1 deliverable, not a follow-up. Pass 3 and Pass 4 outputs feed it; the tab is acceptance-gated under PG19. Do not ship dossiers + atlas + coherence report without also wiring the Streamlit tab.
