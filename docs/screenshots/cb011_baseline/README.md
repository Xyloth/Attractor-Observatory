# CB-011 Screenshot Baseline

Directory reserved for full-room screenshot baselines from the
CB-011 polish round. Capture at 1480 px viewport (the canonical
`max-width` set in `control_room/design_tokens.py`).

## Capture targets

| Filename                           | Room                  | Notes                                              |
|------------------------------------|-----------------------|----------------------------------------------------|
| `01_pulse_deck.png`                | Pulse Deck            | After CB-011: BUILD_LOG event cards (not docstring) |
| `02_world_observatory.png`         | World Observatory     | Includes W-1 drilldown showing 1,394 records        |
| `03_world_observatory_w1.png`      | World Observatory     | W-1 drilldown specifically — verify count visible   |
| `04_world_observatory_w0.png`      | World Observatory     | Math primitives drilldown                           |
| `05_motif_atlas.png`               | Motif Atlas           | Periodic table + lens coupling matrix               |
| `06_basin_floor_lab.png`           | Basin-Floor Lab       | BFG vs C020 split panel visible                     |
| `07_factory_intake_dock.png`       | Factory Intake Dock   | FIRE button + audit inbox + bulk-resolve UI         |
| `08_doctrine_console.png`          | Doctrine Console      | Class 13 + cross-links                              |
| `09_falsifier_ledger.png`          | Falsifier Ledger      | Per-falsifier rows                                  |
| `10_campaign_command.png`          | Campaign Command      | Campaign × gate grid                                |
| `11_ai_operations_tower.png`       | AI Operations Tower   | Agent activity + telemetry                          |
| `12_project_graph.png`             | Project Graph         | Click-to-room from each node                        |
| `13_portfolio_demo.png`            | Portfolio & Demo      | Paper bundle generator                              |

## Visual drift to flag (audit during capture)

CB-011's audit pass identified the following candidate drift between
the rendered surface and the design preview HTMLs in
`Visuals/preview/`:

* **Per-component design previews exist for**: `pills.html`,
  `doctrine-tablet.html`, `gate-grid.html`, `world-card.html`,
  `empty-state.html`, `health-badge.html`, `quarantine.html`,
  `room-glyphs.html`, `spacing.html`, `radii-shadows.html`,
  `color-*.html`, `type-*.html`. Compare each rendered component to
  its preview and flag mismatches in border-radius, color, padding,
  font weight.
* **Full-room mocks are NOT in `Visuals/preview/`**: there's no
  `pulse-deck.html` or `factory-intake-dock.html` to diff against.
  Visual drift at the room level can only be flagged subjectively.
* **Known suspected drift (from code inspection)**:
  - The methodology-review badge's amber pulse-dot may not match the
    pulse-dot weight used in `health-badge.html`.
  - The audit-inbox per-item card uses a 3 px left-border accent;
    the design previews use a flat-card pattern with no left accent.
  - The BFG-vs-C020 split panel uses a 2-column grid that may
    overflow at < 900 px viewport width — needs a media query.

## Capture procedure (manual or selenium)

1. Boot the Control Room: `python control_room/launcher.py`
2. Set viewport to 1480 × 900 px.
3. Navigate to each room; capture full-page PNG.
4. Save under this directory using the filenames above.
5. (Optional) Diff against the previous baseline using `imagemagick`:
   `compare -metric AE prev.png new.png diff.png`.
