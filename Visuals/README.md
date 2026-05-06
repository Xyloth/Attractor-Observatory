# Attractor Observatory — Design System

A dark, luminous research-cockpit visual language for the **Attractor Observatory Control Room** — a sidecar dashboard over a substrate-neutral instrument that explores stable energy-information attractors across 13 simulated worlds, AI-builder operations, calibration campaigns, motif registries, falsifiers, doctrine, and basin-floor geometry.

The design is **not** generic SaaS dark-mode. It is mission control crossed with an alien-biosphere observatory and a mathematical atlas. Every visual cue carries meaning. Beauty is allowed; decoration without semantic load is not.

> "Design a visually striking but scientifically honest Control Room … dense, lucid, alive, legible, and screenshot-worthy. Beauty is allowed, but every visual cue must carry meaning." — design brief, internalized.

---

## Sources

This design system was built primarily from the project's own canonical sources:

- **Codebase** — `Attractor Observatory/` (mounted local folder). Specifically:
  - `control_room/design_tokens.py` — the **canonical** token registry (proposal §6 + §14). Mirrored 1:1 into `colors_and_type.css`.
  - `control_room/components/empty_state.py` — D22 empty-state pathway (the SOLE no-data render path).
  - `control_room/rooms/*.py` — 10 room placeholders with name, icon, tagline, planned artifacts.
  - `control_room/app.py` — Streamlit shell wiring.
  - `docs/ARCHITECTURE.md`, `docs/TOUR.md`, `docs/DOCTRINE.md` — voice, tone, conceptual model.
  - `papers/methods/`, `papers/falsifiers/` — ceremonial / archival surfaces (informs Falsifier Ledger + Doctrine room treatments).

- **Design brief** — pasted in by the project owner; full prose preserved in `brief.md` for reference.

No Figma was provided.

---

## Index

- `colors_and_type.css` — design tokens (CSS vars: colors, type, spacing, radii, shadows)
- `fonts/` — Space Grotesk, Fraunces, JetBrains Mono (webfonts)
- `assets/` — logos, room glyphs, world emblems
- `preview/` — design-system preview cards (rendered in Design System tab)
- `ui_kits/control_room/` — full hi-fi recreation: 10 rooms + cross-cutting chrome + Living Project Graph
- `SKILL.md` — agent-skill manifest (cross-compatible with Claude Code)

## Original Index

```
.
├── README.md                  ← you are here
├── SKILL.md                   ← Agent Skills entry point (cross-compatible with Claude Code)
├── colors_and_type.css        ← canonical CSS tokens — mirrors design_tokens.py
├── brief.md                   ← original design brief (preserved verbatim)
│
├── assets/                    ← logos, world emblems, room glyphs (SVG)
│   ├── logo-mark.svg          ← the observatory mark
│   ├── logo-lockup.svg        ← mark + wordmark
│   ├── room-icons/            ← 10 custom room emblems
│   └── world-icons/           ← W1–W13 family glyphs
│
├── preview/                   ← Design System tab cards (~700×N each)
│   ├── color-status.html      ← five-status semantics (the most important card)
│   ├── color-surfaces.html
│   ├── color-worlds.html
│   ├── type-display.html
│   ├── type-mono.html
│   ├── type-scale.html
│   ├── spacing.html
│   ├── radii-shadows.html
│   ├── pills.html
│   ├── empty-state.html
│   ├── quarantine.html
│   ├── world-card.html
│   ├── room-glyphs.html
│   └── ...
│
└── ui_kits/
    └── control_room/          ← Control Room v0 — 10 rooms + cross-cutting chrome
        ├── README.md
        ├── index.html         ← interactive multi-room demo
        ├── tokens.css         ← @import of /colors_and_type.css
        ├── App.jsx
        ├── Sidebar.jsx
        ├── TopBar.jsx
        ├── EmptyState.jsx
        ├── Pill.jsx
        ├── Panel.jsx
        ├── HealthBadge.jsx
        ├── WorldCard.jsx
        ├── GateGrid.jsx
        ├── CampaignTimeline.jsx
        ├── FalsifierEvent.jsx
        ├── MotifNode.jsx
        ├── ProjectGraph.jsx
        ├── BasinFloor.jsx
        ├── DoctrineTablet.jsx
        ├── QuarantineBanner.jsx
        └── rooms/
            ├── PulseDeck.jsx
            ├── AIOperationsTower.jsx
            ├── CampaignCommand.jsx
            ├── WorldObservatory.jsx
            ├── MotifAtlas.jsx
            ├── BasinFloorLab.jsx
            ├── FalsifierLedger.jsx
            ├── DoctrineConsole.jsx
            ├── FactoryIntakeDock.jsx
            └── PortfolioDemo.jsx
```

---

## CONTENT FUNDAMENTALS

The voice is the project's own voice — earned by years of catching its own back doors. The tone is the load-bearing decision in every interface label. **It is not corporate. It is not playful. It is a serious instrument, written by people who have been wrong before and prefer to say so.**

### Tone

- **Honest before decorative.** Doctrine D22 — "empty rooms beat stocked rooms with mock data." If something is missing, the UI says missing. If something is exploratory, the UI says exploratory. Words like _candidate_, _exploratory_, _claim-bearing_, _falsified_, _downgraded_ are everywhere and they are weighted.
- **Plain, technical, lowercase-leaning.** Sidebar labels are sentence-case ("Pulse Deck", "Falsifier Ledger"); micro-copy and metadata are lowercase ("phase 0 — foundation", "no data — campaign needed", "writes restricted to control_room/cache/"). Avoid title case in chrome.
- **Mechanism over marketing.** "Strang-split RK4 reaction-diffusion solver" is preferred to "advanced solver." "estimation_delta converged from ~0.10 to [0.85, 1.0]" is preferred to "much improved."
- **Failure framed as result.** A falsifier is *publishable*, *signed*, *committed to `papers/falsifiers/`*. Never apologetic, never promotional. Use the verb _downgrade_, never _disable_; use _falsified_, never _broken_; use _exploratory_, never _draft_.
- **Seed not ceiling.** Specifications and instructions read as minimum standards, not maxima. The phrase *"the goal is to prevent underbuilding"* is canonical and may appear verbatim.

### Casing

- **Sidebar / room titles:** Title Case, sentence-leaning ("Pulse Deck", "AI Operations Tower").
- **Panel headers / card titles:** Title Case, short.
- **Status chips:** UPPERCASE, mono, letter-spaced (`VERIFIED`, `EXPLORATORY`, `FALSIFIED`, `CANDIDATE`, `MISSING`).
- **Metadata / footers / tags:** lowercase, mono (`phase 0 — foundation`, `feature/control-room-v0`, `c014 · 2026-04-29`).
- **Code / hashes / branches / task ids:** mono, mixed-case as written (`TASK-CB-007`, `feature/control-room-v0`, `0x3ddc84`, `d3f2a1c`).
- **Numeric readouts:** tabular numerals (`tnum` + `lnum`), monospaced or display.

### Pronouns and stance

- Avoid "I"/"you" entirely. The instrument speaks in third person about the project (`the builder`, `the architect`, `claude`, `codex`, `the PI`). Empty states address absence in the abstract: *"no data — campaign needed: X"*, not *"you don't have any data yet."*
- When the system asserts something, it does so flatly and with provenance: *"signed by codex_audit_002 · 2026-03-14 · class 12 candidate."*

### Emoji

- **Used sparingly, semantically, and only in nav.** The Streamlit sidebar uses one emoji per room (`📡 🌍 🎯 🛰 ✨ 🌐 ⚠️ 📜 ⚓ 🎬`). These are inherited but **the design system replaces them with custom SVG room glyphs** (`assets/room-icons/`); emojis remain only as a fallback for environments that can't render SVG.
- **Never decorative.** No 🚀 🎉 ✅ ❌ 🔥. Status is communicated through the chip + color system, not pictograms.

### Examples (verbatim from codebase)

> `feature/control-room-v0`
> `phase 0 — foundation`
> `read-only sidecar. D22 binding: empty rooms over mock data.`
> `writes restricted to control_room/cache/`
> `no data — campaign needed: BFG basin-floor traces (W1, W3, W5)`
> `expected artifact: campaign_009/basin_floor_geometry.jsonl`
> `D22 — empty rooms beat stocked rooms with mock data`
> `class 12 (Decorative Completeness) candidate is on watch.`

---

## VISUAL FOUNDATIONS

### Backgrounds

The base is an **observatory deep** — `#0a0e16`, a dark navy-graphite — never flat black. Composed in three layers:

1. **Base color** (`--bg-deep`) for the canvas.
2. **A faint grid** — 32px×32px lines at 32% opacity of `--border`, used as a *very* subtle technical underlay behind the sidebar and graph rooms. Implemented with two stacked `linear-gradient` background-images (`--grid-faint`).
3. **Soft radial glows** behind important panels — cyan (`#4fc3f7` @ 5%) at 20%/30%, violet (`#bd6df8` @ 4%) at 80%/70%. Implemented as `--noise-dim`. Result: deep navy night with the faintest sense of starfield.

No full-bleed photography. No raster textures. No corporate gradient banners. **Every "image" in the system is structural — a graph, a basin surface, a constellation, a contour map.** Where world-family imagery is required (W1–W13 cards, world chambers), it is rendered as inline SVG built from the world's own geometry — molecular constellations for chemistry, branching forms for morphogenesis, lattice circuits for digital, etc.

### Color

- **Primary palette**: cyan (trace), green (verified), amber (exploratory/warning), red (falsified), purple (motif), blue (active), gray-blue (unavailable), white-ice (claim-bearing). Each role has a single canonical hex.
- **Restraint**: a panel typically uses 1 status color + neutrals. Multiple-color panels signal a comparison (R/Y/G grids, agent-by-campaign stacks).
- **Saturation**: status colors are saturated; surfaces and text are desaturated. The eye lands on status first.
- **Soft fills** at 12% alpha are used for chip backgrounds and full-card status states.
- **Glow rings** (`box-shadow: 0 0 0 1px <color>, 0 0 24px <color@22%>`) signify *live* — pulse animations on active processes only.

### Type

- **Display**: Space Grotesk (600). Geometric, technical, restrained. Used for room titles, panel headings, big readouts.
- **Body**: Inter (400/500). Default UI copy.
- **Mono**: JetBrains Mono (500). Hashes, branches, task IDs, log lines, status chips, ALL metadata.
- **Serif (ceremonial)**: Fraunces (500). Used **only** in two places — the Doctrine Console rule headings (treated as inscribed law) and the Falsifier Ledger's "failed honestly" titles (treated as archival epitaph). Never in chrome, never in body.

Numerals are tabular. Hashes are short-form (`d3f2a1c`). Task IDs always render as `TASK-CB-NNN` (uppercase, hyphenated). Branches always render `feature/<slug>` in mono.

If the user wants the canonical Space Grotesk + JetBrains Mono + Fraunces in the production app, the CSS imports them from Google Fonts. **No font files were checked into the codebase**, so we picked the nearest exact match each was already declared with — no substitution flag needed for the primary three. Inter and Fraunces are the only secondaries; both load from Google Fonts.

### Spacing & Density

- 4-step base scale: 4 / 8 / 12 / 16 / 20 / 24 / 32 / 40 / 48 / 64.
- Panels use `padding: 20px` (`--space-5`); cards inside panels use `12px` gap (`--space-3`); section gaps are `24–32px`.
- Density is **dense but layered**: first glance simple (badge + headline), drill-down detailed (full table + provenance hash + audit history). Never both at once on the surface layer.

### Animation

- **Semantic only.** Each motion duration is a meaning:
  - `1800ms pulse` — active process
  - `4200ms slow-glow` — live monitored item
  - `600ms flash` — recent event (< 5 min)
  - `800ms fade` — historical artifact appearing
  - `8000ms orbit` — dependency / trace flow along an edge
  - `300ms jitter` — uncertainty (used **sparingly**; never decorative)
- **Easing**: `cubic-bezier(0.22, 0.61, 0.36, 1)` for entrance/out; `cubic-bezier(0.65, 0, 0.35, 1)` for in-out. No bounces. No springs.
- **Off in print/test.** `@media (prefers-reduced-motion: reduce)` disables everything. Screenshot capture path passes `MOTION_ENABLED_DEFAULT=False`.
- **Hover state**: panels lighten by ~6% (`--bg-panel` → `--bg-panel-raised`); chips and pills lift via `box-shadow: 0 0 0 1px currentColor, 0 0 12px currentColor@30%`. No translation, no scale. Hover is illumination, not motion.
- **Press state**: surfaces darken by ~4% and lose their glow ring momentarily; no shrink, no bounce.

### Borders

- 1px solid `--border` (#283042) for default panel edges.
- 1px solid `--border-strong` (#3a4560) on focus / hover-emphasized.
- **1px DASHED `--border-dashed` (#4a5266)** is the **canonical signal of absence**. It appears ONLY on empty-states and quarantine surfaces and **must never** be used on real-content cards. This is load-bearing: a recruiter or new collaborator should be able to scan a screenshot and pick out missing-data zones from real-data zones at a glance.
- Quarantine adds a **dashed amber border** (`rgba(245,166,35,0.55)`) plus a 14°/28° amber stripe pattern at 4% opacity — the visual equivalent of yellow-and-black hazard tape, dialed down.

### Shadows

- `--shadow-card`: subtle inner highlight + soft outer drop. Cool-toned. Used on raised cards.
- `--shadow-overlay`: deeper drop + 1px border, for modals / drilldowns.
- `--shadow-glow-soft`: large soft cyan glow at 15%, behind hero panels in Pulse Deck.
- **Status glows** (`--verified-glow`, `--active-glow`, etc.) double as both shadow and outline — outer 24px blur of the status color at 18–22%. Reserved for live/active cards.

### Corner radii

- `3px` — pills' inner badges, chip borders.
- `6px` — small inputs, dense table cells.
- `8px` — buttons, chips outer.
- `12px` — panels, cards (canonical).
- `999px` — status pills.

### Transparency & blur

- Used sparsely. The only places: (1) the Top Status Bar over the canvas in graph mode (`backdrop-filter: blur(8px)` on a `rgba(10,14,22,0.7)` surface), (2) hover tooltips, (3) the Project Graph's minimap.
- Soft fills at 12% alpha are flat (no blur), serving as status backgrounds inside chips and cards.

### Imagery

- **Cool, monochrome, structural.** No photography. No marketing illustration. No mascots.
- World thumbnails are SVG diagrams of each world's own dynamics — molecular reaction webs (W1), nested vesicles (W2), wave fields (W3), branching morphogenesis (W4), circuit lattices (W5), food-web layers (W6), insect-trail stigmergy (W7), neural loops (W8), pore-network minerals (W9), hyperedge nodes (W10), sequence-cloud quasispecies (W11), nested protocells (W12), recursive multi-scale rings (W13).
- The Project Graph is the system's iconic visual centerpiece.

### Layout rules

- Sidebar is fixed `224px`, never collapses to icon-only on desktop. Uses the room-icons SVG set + label.
- Top Status Bar is fixed at the top of the content area: `56px` tall, full-width, contains health badge + branch + last test + current task + search + snapshot button.
- Search input is full-width within the top bar (`max-width: 480px`), ALWAYS visible.
- Cards arrange on a 12-column grid with 24px gutters; on viewports < 1280px, collapse to 6-column; below 960px, stack vertically.

---

## ICONOGRAPHY

The codebase ships **no SVG icon library and no icon font** — it relies on Streamlit's emoji glyphs (`📡 🌍 🎯 🛰 ✨ 🌐 ⚠️ 📜 ⚓ 🎬`) for the 10 rooms. The design system replaces these with **a custom SVG room-glyph set in `assets/room-icons/`**, hand-drawn at 24px stroke-1.5 to fit the observatory's technical-linework aesthetic. The emoji are kept only as a string-fallback in `tokens` (matching what the Python ships).

**For functional UI icons** (search, close, chevron, refresh, copy, download, external-link, info, alert, check), the system imports **Lucide** from CDN. Lucide is 1.5px stroke, geometric, ASCII-clean — exactly the visual register the rest of the system uses. Substituted because the codebase ships none.

**For the W1–W13 world family**, the system ships custom SVG glyphs in `assets/world-icons/`. Each is a 32px abstract diagram of its world's primary dynamics, monochrome (currentColor), suitable for inline use in card headers and status grids.

**No emoji** in panels or content — only in nav as a fallback.

**No unicode characters** masquerading as icons (e.g. `→`, `✓`, `★`). Arrows and checks render through Lucide. Mathematical symbols (`∂`, `∇`, `≈`, `→`) **may** appear in body text in serif/mono where they describe equations — they are not icons.

**Logo**: a custom mark — concentric arcs converging on a single point, evoking both an observatory dish and a basin-floor manifold. SVG only. Comes in monogram (`logo-mark.svg`) and full lockup with wordmark (`logo-lockup.svg`).

---

## Status semantics — the load-bearing rule

Five claim states must be **distinguishable at a glance** in any room:

| State | Color | Pill | Border | Visual cue |
|---|---|---|---|---|
| **Verified / claim-bearing** | `--verified` `#3ddc84` | `VERIFIED` | solid | green pulse ring on hover |
| **Active / in-progress** | `--active` `#4fc3f7` | `ACTIVE` | solid | slow cyan pulse |
| **Exploratory / candidate** | `--warning` `#f5a623` | `EXPLORATORY` / `CANDIDATE` | solid | amber dot, no glow |
| **Missing / placeholder** | `--unavailable` `#5b6478` | `MISSING` | **DASHED** | dashed border, mono copy, D22 empty-state |
| **Falsified / downgraded** | `--failed` `#ff5468` | `FALSIFIED` | solid + slash | red prism, "failed honestly" badge |

This is more important than any decorative choice. **If a recruiter sees the dashboard, they should know what's real. If Claude Builder wires it, the semantics should be unambiguous.**

---

## What's next

- Iterate on the world-family SVG glyphs — current set is sketchy first pass.
- Decide whether the Living Project Graph wants WebGL or stays SVG (currently SVG; ~200 nodes is the practical ceiling).
- A light theme is **not** planned. The observatory is a dark instrument.

See `SKILL.md` for how an agent should use this kit.
