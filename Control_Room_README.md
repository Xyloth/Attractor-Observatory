# Attractor Observatory — Control Room

Live command interface for worlds, campaigns, motifs, falsifiers, and AI
research operations. Built as a sidecar to the scientific core. The
Control Room **reads** the project's artifacts — it does not author
science, mutate registries, or promote claims.

> The Control Room may visualize almost everything. It should mutate
> almost nothing. — proposal §3

![Pulse Deck](control_room/portfolio/01_pulse_deck.png)

## Run it

### Native window (recommended)

Double-click `Launch Control Room.bat` at the repo root. A WebView2
window opens to the Control Room.

Optional flags:

```
Launch Control Room.bat              REM default: console + native window
Launch Control Room.bat /quiet       REM no console; pythonw silent mode
Launch Control Room.bat /no-window   REM Streamlit only (open in browser)
Launch Control Room.bat /port=8765   REM custom port
```

### Browser (manual fallback)

```bash
pip install -r requirements.txt
streamlit run control_room/app.py
```

Open `http://localhost:8501` (default Streamlit port). The launcher uses
8765 by default to keep the desktop experience predictable.

### Hardening

The launcher (`control_room/launcher.py`):

* **Detects port conflicts** and kills the holding process on Windows
  via `netstat -ano` + `taskkill /F /PID`, on POSIX via `lsof -ti` +
  `kill -9`. Replicates manual port-conflict resolution automatically.
* **Detects Streamlit** on PATH first; falls back to
  `python -m streamlit`; surfaces a helpful pip-install message if
  neither path works.
* **Degrades gracefully** if `pywebview` is not installed: keeps
  Streamlit running and tells the user the browser URL.
* **Optional `--no-window`** for environments without a windowing system.

## What's in the dashboard

The Control Room ships **11 rooms** organized by question class
(proposal §7 + §9.1 Project Graph):

| # | Room | Question | Phase |
|---|------|----------|-------|
| 1 | Pulse Deck | What is happening right now? | 1 |
| 2 | World Observatory | Which worlds exist and how dense are they? | 1 |
| 3 | Campaign Command | Which campaigns ran and what passed? | 1 |
| 4 | AI Operations Tower | How are the AI agents performing? | 1 |
| 5 | Motif Atlas | Which motifs cross which worlds? | 1 |
| 6 | Basin-Floor Lab | Where is the floor connectivity candidate? | 1 |
| 7 | Falsifier Ledger | What has been falsified? | 1 |
| 8 | Doctrine Console | Which rules bind, which violations surfaced? | 1 |
| 9 | Factory Intake Dock | What did the autonomous Factory ingest? | 1 |
| 10 | Project Graph | The living node-edge map of the project | 2 |
| 11 | Portfolio & Demo Mode | 60-second curated walk-through | 3 |

Per-room data sources and design rationale: see
[`control_room/rooms/README.md`](control_room/rooms/README.md).

## Screenshots

### Pulse Deck — live heartbeat

![Pulse Deck](control_room/portfolio/01_pulse_deck.png)

Branch + last commit + pytest cache + builder task as 4 first-glance
metric cards. Needs-attention lane is bright red/amber when failed
campaigns or pytest failures surface; green "all clear" otherwise.
Below the fold: gate grid (campaigns × passed/total), recent BUILD_LOG
events, **calibration trajectory** (estimate vs actual for every
agent), what-changed-since-last-session diff, recent falsifiers.

### World Observatory — 15-world inventory

![World Observatory](control_room/portfolio/02_world_observatory.png)

W-1 atomic / molecular + W0 math primitives (Campaign 016 additions) +
W1-W13 (the canonical 13 worlds). Density classes color-coded:
verified=`claim_ready_densified`, warning=`exploratory_densified`,
failed=`falsifier_active`, active=`trace_valid`. Plotly world heatmap
below the inventory grid surfaces density × motif richness at a glance.

### AI Operations Tower — Paper A's calibration empirics

![AI Ops Tower](control_room/portfolio/03_ai_operations_tower.png)

Three agent cards with task counts and mean-delta. Below: the
calibration trajectory chart (log-y; 1.0 reference line) plotting every
agent's estimate-vs-actual ratio over time. The Estimation Loop
convergence story rendered as a single auditable chart. Class 1-12
mistake catalog + audit log + doctrine arc.

### Motif Atlas — 6 motifs across worlds

![Motif Atlas](control_room/portfolio/04_motif_atlas.png)

Process-role / interaction-channel / overlap-field counts from
Campaign 016 ontology; 6 motif cards (closure, boundary, repair,
lineage, memory, **floor_connectivity**); Plotly motif × lens coverage
heatmap from Campaign 010. floor_connectivity card carries Campaign
013 replication verdict inline.

### Falsifier Ledger — honest failures published

![Falsifier Ledger](control_room/portfolio/05_falsifier_ledger.png)

papers/falsifiers/ + atlas/negative_space/ + papers/methods/ as the
project's "this failed honestly" surface. D17 binding (floor falsifiers
are publishable) made visible.

### Project Graph — living node-edge map

![Project Graph](control_room/portfolio/06_project_graph.png)

7 node types (worlds / campaigns / motifs / agents / doctrines /
falsifiers / reports) wired by 8 edge types. Edges sourced from real
provenance: `produced` from campaign artifacts, `audited` from
BUILD_LOG agent + campaign matches, `detected-in` from canonical lens
registry domain, `depends-on` from `papers/methods/*` markdown
cross-references, `modifies` from BUILD_LOG file-touch declarations.
Click-to-navigate routes a node to its room of origin.

## Architecture

The Control Room is a sidecar visualization layer, not part of the
scientific core. Information flows up only:

```
┌──────────────────────────────────────────────────────────────────┐
│ ATLAS PLANE         (slow, public-facing)                        │
│   periodic table │ atlas DB │ replays │ negative-space registry │
├──────────────────────────────────────────────────────────────────┤
│ ANALYSIS PLANE      (medium, scientifically primary)             │
│   motif registry │ detectors │ lens registry │ scoring │ nulls   │
├──────────────────────────────────────────────────────────────────┤
│ DATA PLANE          (append-only, schema-versioned)              │
│   SystemTrace store │ event store │ lineage store │ ledgers      │
├──────────────────────────────────────────────────────────────────┤
│ SUBSTRATE PLANE     (fast, world-specific)                       │
│   W-1 / W0 / W1-W13 world engines │ search │ perturbation        │
└──────────────────────────────────────────────────────────────────┘
                ↑       Provenance graph spans all planes        ↑
                ↑       Telemetry plane spans all planes         ↑
```

The Control Room **reads** all four planes via the adapter layer
(`control_room/adapters/`). It writes to exactly three sidecar paths:

* `control_room/cache/` — UI state cache.
* `control_room/snapshots/` — AI-consumption snapshots (see below).
* `control_room/portfolio/` — README image assets.

This restriction is enforced **mechanically** by
`tests/test_control_room_readonly.py`, which AST-walks every `.py`
under `control_room/` and verifies write targets are cache-rooted.

## How AI agents read this dashboard

A fresh AI agent (post-compaction Architect Claude, fresh Codex 1.5x
session, fresh Claude Builder) **reads ONE file** to get the full
project state:

```
control_room/snapshots/state_latest.json
```

This snapshot is written every time the dashboard renders any room. It
carries a structured digest (`ControlRoomSnapshot.v1`) of:

* **project_health** — score 0-100, active warnings, current branch.
* **current_agent_telemetry** — task counts + delta means per agent.
* **calibration_trajectory** — every agent's per-task delta = actual /
  estimated, with min/max/latest.
* **campaigns** — every campaign's status + gate counts + schema.
* **doctrine** — D7-D22 registry IDs.
* **mistake_catalog** — Class 1-12 with status (11 ratified, 1
  candidate).
* **falsifiers** — papers/falsifiers/ + negative_space counts and file
  names.
* **factory_state** — Campaign 016 empirical / normalized / edge counts +
  detector decline rate.
* **detector_decline** — Campaign 016 96/96 decline as load-bearing
  signal per D17.
* **git_state** — branch + last commit + recent log.
* **pytest_status** — last_failed + nodeid count.
* **recent_changes** — most-recent BUILD_LOG entries.
* **raw_adapter_payloads** — `{status, rationale}` for every adapter so
  the consumer knows which sections are real vs missing.

The `purpose` and `consumer_guidance` fields explain the read order
explicitly per agent role. The schema is versioned; CB-007 ships
`v1`.

For the diff between snapshots:

```
control_room/snapshots/state_prior.json
```

Auto-promoted from `state_latest.json` on each write. The Pulse Deck's
"what changed since last session" panel computes
`diff_snapshots(prior, current)` and surfaces structured deltas
(campaign status changes, pytest count changes, falsifier count
changes, doctrine count changes, new BUILD_LOG headers, latest-delta
movement).

The snapshot is a **first-class sidecar artifact** for AI consumption,
not just a cache. It is the canonical entry point.

## Doctrine bindings

* **D22 — Empty rooms beat stocked rooms with mock data.** Every "no
  data" path routes through the single empty-state component.
  Mechanism, not policy: the test scanner verifies the marker is unique
  to `components/empty_state.py`.
* **D17 — Floor falsifiers are publishable.** The Falsifier Ledger room
  is the surface; the Doctrine Console renders Campaign 016's 96/96
  detector decline as load-bearing signal, not a failure to suppress.
* **D9 — No engineered passes.** Adapters return
  `{status, data, rationale}`; non-`ok` status routes to empty-state
  honestly.
* **D14 — No fabricated values.** Adapters parse what's on disk.
* **Class 12 candidate — Decorative Completeness.** On watch per D22.

## Test coverage

```
$ pytest tests/test_control_room_adapters.py tests/test_control_room_readonly.py tests/test_control_room_rooms.py
```

76 tests across 3 modules:

* **test_control_room_adapters.py** — 16 tests: 8 happy-path + 8
  missing-file degradation per adapter.
* **test_control_room_readonly.py** — 4 tests: scanner walks
  control_room/, marker uniqueness, deliberate-violation sandbox,
  permitted-cache-write sandbox.
* **test_control_room_rooms.py** — 56 tests: per-room metadata
  contract, registry order, render dispatch, snapshot endpoint shape,
  diff first-launch + steady-state + change detection, project graph
  determinism, edge enrichment provenance, empty-state HTML marker,
  factory adapter, chrome helpers, portfolio room, app shell helpers.

Phase 0 baseline was 20; Phase 3 (CB-007) brings the count to 76.

## Future tweaks

* **W0 / W-1 SVG icons.** Codex 1.5x is producing
  `w0-math-primitives.svg` and `w-minus1-atomic-molecular.svg` to match
  the existing 13 world icons. The chrome resolver
  (`components/chrome.WORLD_ICON_ALTERNATES`) will pick them up the
  moment they land in `control_room/static/world-icons/`. Until then,
  those two world cards render with a gray placeholder block.
* **3D basin surface (Basin-Floor Lab).** Intentional honest absence
  per proposal §7.6 ("this room should not fake mathematical
  precision"). Faithful 3D requires lens-projected trace coordinates
  (Campaign 017+ work).
* **Streamlit `on_select` plotly_chart events.** Available in Streamlit
  ≥ 1.37; would replace the Project Graph dropdown + button with true
  click events. The dropdown path is the documented stable fallback.
* **Headless screenshot rig.** The Portfolio Demo's capture targets are
  declared in `control_room/portfolio/readme_assets.json`; a Selenium
  follow-up could automate the actual PNG capture.
* **Live file-watching.** The dashboard re-renders on user nav; auto-
  refresh on file changes is deferred. Streamlit's
  `--server.fileWatcherType` is currently `none` (avoids re-renders
  while the user is reading).
* **Per-trace replay panel.** Mentioned in proposal §7.2 as optional;
  deferred — would require trace-stepping infrastructure that doesn't
  exist yet.
* **Edge enrichment to motifs / doctrines.** Currently `produced`,
  `audited`, `detected-in`, `falsified`, `depends-on`, `modifies` are
  derived from real provenance; `supports` and `conflicts-with` exist
  in the legend with 0 instances honestly. Could mine more BUILD_LOG
  audit entries for these.
* **Sidebar agent-identity ribbon.** Codex 1.5x's design shows
  per-agent borders/glyphs on cards using the agent palette; CB-005
  shipped the `--agent-*` color tokens but the cards don't yet
  consistently apply them. Phase-4-style polish if PI requests.

## Provenance

* Phase 0 (TASK-CB-004, ~16 min): foundation, 8 adapters, D22
  ratification, 20 tests.
* Phase 1 (TASK-CB-005, ~13 min): 8 substantive rooms wired, factory
  adapter, Visuals/ design system integrated, 23 SVG assets.
* Phase 2 (TASK-CB-006, ~4 min): Project Graph (11th room),
  type-anchored layout, 7 node types + 4 edge types from real adapters.
* Phase 3 (TASK-CB-007): production polish — Portfolio Demo, click-to-
  navigate, snapshot endpoint, what-changed diff, edge enrichment, 76
  tests, README + per-room docs, launcher hardening.

Branch: `feature/control-room-v0` (no merge to main). Tracked through
[BUILD_LOG.md](BUILD_LOG.md).

— Built by Claude Builder for the Attractor Observatory project, under
spec v1.2 + binding doctrine D7–D22.
