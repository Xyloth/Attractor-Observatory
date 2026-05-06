— preserved verbatim from the project owner —

# Design brief — visuals list for Claude Design

(Flat enumeration of the ~70 visual elements across 10 rooms + cross-cutting + Project Graph, plus theme & icon notes. See README for the high-level synthesis.)

The full brief was pasted in chat at project init. Key extractions live in:

- `README.md` (CONTENT FUNDAMENTALS, VISUAL FOUNDATIONS, ICONOGRAPHY, status semantics).
- `colors_and_type.css` (canonical tokens, sourced from `Attractor Observatory/control_room/design_tokens.py`).
- `ui_kits/control_room/` (the 10 rooms as JSX components + interactive demo).

The brief asked for:

1. A **complete visual kit** — colors, type, card styles, glow rules, spacing, borders, icons, room hero backgrounds, world family icons, motif glyphs, empty-state designs, quarantine styling, falsifier styling, project-graph treatment, basin-floor surface treatment, README screenshot composition style.
2. The **most important rule** — five distinguishable statuses: verified / exploratory / candidate / missing / falsified.
3. **Theme**: dark scientific observatory + living systems atlas. Mission control + alien biosphere lab + mathematical atlas + AI ops cockpit. Not cyberpunk. Not generic SaaS. Not biology textbook.
4. **The iconic centerpiece**: the **Living Project Graph** — a force-directed map where worlds, campaigns, motifs, traces, agents, doctrines, falsifiers, and reports are all nodes. Pulses on recent change. Red fractures on falsifiers.
