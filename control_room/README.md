# Observatory Control Room

Sidecar visualization layer for Attractor Observatory. Read-heavy,
branch-isolated, non-claim-bearing. Phase 0 (TASK-CB-004) ships the
foundation: app shell, design tokens, empty-state component (D22),
adapter layer, and read-only enforcement.

## Run it

```bash
pip install -r requirements.txt
streamlit run control_room/app.py
```

The app launches a local dark-mode dashboard with sidebar navigation
across 10 rooms (proposal §7). Phase 0 rooms are intentionally placeholder
pages — they render the empty-state component with an explanation of
which Phase will populate them. **This is a feature, not a defect.**
Doctrine D22 (`docs/doctrine_d22.md`) binds the project to honest
absence over decorative completeness.

## Architecture

```
control_room/
├── app.py                  # Streamlit entry
├── design_tokens.py        # color / motion / typography (proposal §14)
├── components/
│   └── empty_state.py      # the SOLE no-data render path (D22)
├── adapters/               # 8 file-format-specific parsers
│   ├── build_log.py
│   ├── builder_telemetry.py
│   ├── campaign_reports.py
│   ├── doctrine.py
│   ├── methods_falsifiers.py
│   ├── negative_space.py
│   ├── git_metadata.py
│   └── pytest_cache.py
├── rooms/                  # 10 placeholder rooms (Phase 0)
│   ├── pulse_deck.py
│   ├── world_observatory.py
│   ├── campaign_command.py
│   ├── ai_operations_tower.py
│   ├── motif_atlas.py
│   ├── basin_floor_lab.py
│   ├── falsifier_ledger.py
│   ├── doctrine_console.py
│   ├── factory_intake_dock.py
│   └── portfolio_demo.py
├── cache/                  # the ONLY writable path under control_room/
└── README.md
```

## Doctrine

* **D22 — Empty rooms beat stocked rooms with mock data** (new in TASK-CB-004).
  Honest absence beats decorative completeness. `components/empty_state.py`
  is the single source of truth for "no data" rendering. Class 12
  (Decorative Completeness) candidate is on watch.
* **D7-D21 binding generally.** No new doctrine beyond D22.

## Adapter contract

Every adapter returns `{"status": "ok"|"missing"|"malformed", "data":
..., "rationale": "<one-line>"}`. Rooms branch on `status`: `ok` → render
real content; otherwise → empty-state component. There is no plausible-
defaults pathway.

## Read-only enforcement

`tests/test_control_room_readonly.py` verifies that no module under
`control_room/` writes outside `control_room/cache/`. The test:

1. Walks every `.py` file under `control_room/` for `open(..., 'w')`,
   `Path.write_text`, `Path.write_bytes`, `os.remove`, `shutil.rmtree`,
   etc. patterns and confirms each call's first argument is rooted at
   `control_room/cache/`.
2. Exercises a deliberate-violation attempt (a temporary patched module
   that tries to write outside cache/) and asserts the violation is
   detected.

## Phase 0 acceptance gates

* Streamlit app launches without error.
* Sidebar nav works; each room renders.
* Every Phase 0 room renders via the empty-state component (D22).
* Adapter happy-path + missing-file tests pass.
* Read-only enforcement test passes.
* CI smoke test passes.

## Phases 1-4 (planned, not in this campaign)

* **Phase 1:** Pulse Deck, AI Operations Tower, Campaign Command,
  World Observatory.
* **Phase 2:** Motif Atlas, Basin-Floor Lab, Falsifier Ledger,
  Doctrine Console, Factory Intake Dock.
* **Phase 3:** Project Graph (heavyweight cross-cutting viz).
* **Phase 4:** Polish (Portfolio/Demo, tests fill-out, screenshots,
  README expansion).
