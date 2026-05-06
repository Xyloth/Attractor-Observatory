# Control Room — Room Reference

Quick per-room reference for AI agents reading the codebase. Each room
follows the same shape: imports adapter(s), routes non-`ok` status
through `render_empty_state`, renders real-data panels via the chrome
helpers in `control_room.components`.

D22 binds every room: **the empty-state component is the SOLE no-data
render path**. No fallbacks, no plausible defaults, no styled mocks.

| # | Room | Module | Adapters consumed | Phase |
|---|------|--------|-------------------|-------|
| 1 | Pulse Deck | `pulse_deck.py` | git_metadata, builder_telemetry, build_log, campaign_reports, pytest_cache, methods_falsifiers, snapshot diff | 1 |
| 2 | World Observatory | `world_observatory.py` | factory_store, campaign_reports, methods_falsifiers + canonical 15-world list | 1 |
| 3 | Campaign Command | `campaign_command.py` | campaign_reports, build_log | 1 |
| 4 | AI Operations Tower | `ai_operations_tower.py` | builder_telemetry, build_log, doctrine | 1 |
| 5 | Motif Atlas | `motif_atlas.py` | factory_store, campaign_reports + canonical 6-motif list + Campaign 010 coverage matrix | 1 |
| 6 | Basin-Floor Lab | `basin_floor_lab.py` | methods_falsifiers + Campaign 010 deficit map + Campaign 013 replication / adversarial / substrate-blocked records | 1 |
| 7 | Falsifier & Negative-Space Ledger | `falsifier_ledger.py` | methods_falsifiers, negative_space | 1 |
| 8 | Doctrine & Integrity Console | `doctrine_console.py` | doctrine, factory_store (detector decline) | 1 |
| 9 | Factory Intake Dock | `factory_intake_dock.py` | `factory_lowlevel.live_pipeline` + `control_room/cache/factory_runs/` | 2 |
| 10 | Project Graph | `project_graph.py` | All Phase 0 adapters + edge enrichment from papers/methods + BUILD_LOG | 2 |
| 11 | Portfolio & Demo Mode | `portfolio_demo.py` | snapshot.build_snapshot (composes all adapters) + screenshot capture rig | 3 |

## Per-room contract

Every room module exposes:

```python
ROOM_ID: str       # short slug; sidebar nav key
ROOM_NAME: str     # human-readable label
ROOM_ICON: str     # single-glyph emoji (sidebar)
ROOM_TAGLINE: str  # one-line subtitle
ROOM_PHASE: str    # which Phase shipped the room
def render() -> None: ...  # Streamlit entry; no return
```

Lazy imports of `streamlit` keep the modules importable in adapter-only
test contexts.

## Pulse Deck (`pulse_deck.py`)

**Purpose:** First-glance project state in 10 seconds.

**Layout (top→bottom):**
1. 4 metric cards: active branch, latest commit, pytest cache, builder task.
2. Needs-attention lane (red/amber if active, green "all clear" otherwise).
3. Gate grid (campaigns × passed/total) + recent BUILD_LOG events.
4. Calibration trajectory (Plotly, log-y, all models).
5. **What-changed-since-last-session** diff against `state_prior.json`.
6. Recent falsifiers (papers/falsifiers/* index).

**D22 hits:** every panel routes through `render_empty_state` if its
adapter returns non-ok or if no falsifier records exist.

## AI Operations Tower (`ai_operations_tower.py`)

**Purpose:** Paper A's calibration empirics visual layer.

**Key panels:**
- Agent cards (Claude Builder / Codex / Architect Claude) with task counts and mean-delta.
- Calibration delta chart (log-y, 1.0 reference line); the Estimation
  Loop convergence story rendered as a single chart.
- Frozen Class 1-12 mistake catalog with status (10/11 ratified, 12 candidate).
- Recent audit catches from BUILD_LOG.
- Doctrine arc (D7-D25) cards.

## Campaign Command (`campaign_command.py`)

**Purpose:** Per-campaign timeline + gate detail.

**Key panels:**
- 4 metric cards (total / green / in-progress / no-report).
- Plotly campaign timeline bar chart (passed gates per campaign).
- Gate grid + per-campaign detail table.
- Audit log (BUILD_LOG entries matching audit/meta-audit/campaign tokens).

## World Observatory (`world_observatory.py`)

**Purpose:** Visualize all 15 worlds (W-1 atomic / W0 math primitives /
W1-W13).

**Density colors:** verified=claim_ready / warning=exploratory_densified
/ failed=falsifier_active / active=trace_valid.

**SVG icons:** loaded from `control_room/static/world-icons/`.
Codex 1.5x's W0 / W-1 icons resolve via `chrome.WORLD_ICON_ALTERNATES`
the moment they land in the static directory.

## Motif Atlas (`motif_atlas.py`)

**Purpose:** 6 motifs as living objects.

**Highlight:** floor_connectivity card carries Campaign 013 replication
result (formal_gap + N7 p + verdict) inline. The motif × lens coverage
heatmap is sourced from `reports/campaign_010/coverage_matrix.json`.

## Basin-Floor Lab (`basin_floor_lab.py`)

**Purpose:** floor_connectivity replication trail.

**Surfaces:** Campaign 013 verdict, adversarial control verdict, substrate-blocked
verdict, multisubstrate v2 per-substrate scientific verdicts, falsifier records.

**Honest absence:** the basin-surface 3D visualization (proposal §9.6)
is intentionally rendered as empty-state per §7.6 closing line and D22.

## Falsifier & Negative-Space Ledger (`falsifier_ledger.py`)

**Purpose:** Make failure visible. D17 binding.

**Surfaces:** papers/falsifiers/ index + atlas/negative_space/ registry +
papers/methods/ index (Truth Pass + Substance Audits + methods docs).

## Doctrine & Integrity Console (`doctrine_console.py`)

**Purpose:** Rules + integrity surface.

**Surfaces:** doctrine registry + DOCTRINE.md headings + Class 1-12
mistake catalog with origins + Campaign 016 detector decline rendered
as load-bearing signal per D17.

## Factory Intake Dock (`factory_intake_dock.py`)

**Purpose:** Live multi-world Factory console.

**Surfaces:** target-world selector, source-adapter selector, source-bound
parameter inputs, FIRE button, live stage progress, life-form trace list,
trace/lens drilldown, per-world motif fire rates, and run history.

**Artifacts:** run records live under `control_room/cache/factory_runs/`;
Campaign 021 report and traces live under `reports/campaign_021/`.

**D22/D23:** empty results stay visible as no-fire or no-run states; trace
paths in run records are dereferenceable in the shipped workspace.

## Project Graph (`project_graph.py`)

**Purpose:** Cross-cutting living node-edge map.

**Nodes (7 types):** worlds, campaigns, motifs, agents, doctrines,
falsifiers, reports.

**Edges (8 types):** produced, audited, falsified, depends-on,
detected-in, modifies, supports, conflicts-with.

**Layout:** type-anchored polar constellation, deterministic from
`md5(node_id)`; same input → byte-identical positions.

**Click-to-navigate:** select a node from the dropdown + "jump to" button
to route via `st.session_state`. URL anchor `?room=<id>` is the
documented fallback.

## Portfolio & Demo Mode (`portfolio_demo.py`)

**Purpose:** Public face. 6-scene curated walk-through.

**Scenes:**
1. Project thesis slide (composed from real adapter data).
2. Architecture SVG (4 planes + cross-cutting).
3. AI agent workflow SVG (cross-audit triangle).
4-9. The 6 README screenshot targets (Pulse Deck → World Observatory →
   AI Ops Tower → Motif Atlas → Falsifier Ledger → Project Graph).

**Capture rig:** writes `control_room/portfolio/readme_assets.json`
manifest. Streamlit doesn't export PNGs from the dashboard surface;
manual screenshot or Selenium follow-up lands the bytes at the manifest's
declared filenames.

## Snapshot endpoint

Each render calls `control_room.snapshot.write_snapshot()`, which
writes `control_room/snapshots/state_<UTC>.json` + maintains
`state_latest.json` and `state_prior.json` (the prior is
auto-promoted from latest before each new write).

A fresh AI agent reads `state_latest.json` ONCE at session start to get
the full structured digest covering every adapter — no need to parse 50
source files.

## Read-only enforcement

`tests/test_control_room_readonly.py` AST-walks every `*.py` under
`control_room/` and verifies write targets are rooted at one of three
sidecar-writable paths: `cache/`, `snapshots/`, `portfolio/`. The
deliberate-violation sandbox confirms the scanner catches violations.
The marker-uniqueness test verifies the empty-state HTML marker is
emitted only by `components/empty_state.py` (and the components
re-export).
