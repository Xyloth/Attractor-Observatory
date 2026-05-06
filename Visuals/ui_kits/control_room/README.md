# Control Room — UI Kit

Hi-fi recreation of the Attractor Observatory Control Room (proposal §7). Ten rooms + cross-cutting chrome (sidebar, top status bar, search, snapshot) + the Living Project Graph (cross-cutting overlay).

This kit is **not production code**. It mocks data and cuts corners on real adapters. The visual language matches the canonical tokens 1:1.

## Files

- `index.html` — interactive demo. Sidebar nav between all 10 rooms + a Living Project Graph overlay.
- `App.jsx` — root, holds router state + mock data store.
- `Sidebar.jsx`, `TopBar.jsx`, `Search.jsx`, `SnapshotButton.jsx` — cross-cutting chrome.
- `EmptyState.jsx`, `Pill.jsx`, `Panel.jsx` — primitives.
- `HealthBadge.jsx`, `WorldCard.jsx`, `GateGrid.jsx`, `CampaignTimeline.jsx`, `FalsifierEvent.jsx`, `MotifNode.jsx`, `BasinFloor.jsx`, `DoctrineTablet.jsx`, `QuarantineBanner.jsx` — composite components.
- `ProjectGraph.jsx` — the iconic centerpiece (force-directed living node-edge map).
- `RoomGlyph.jsx`, `WorldGlyph.jsx` — icon helpers.
- `mockData.js` — synthetic but plausible data, sourced from real telemetry shapes in `Attractor Observatory/project_telemetry/` and `reports/`.
- `rooms/` — one JSX per room (PulseDeck, AIOperationsTower, CampaignCommand, WorldObservatory, MotifAtlas, BasinFloorLab, FalsifierLedger, DoctrineConsole, FactoryIntakeDock, PortfolioDemo).

## Run

Open `index.html`. No build step. React + Babel from CDN.

## Doctrine compliance

Every "no data" path in the kit routes through `<EmptyState />`. Every status state is one of the five canonical pills. The Factory Intake Dock screams `NOT FOR PROMOTION` at the top.
