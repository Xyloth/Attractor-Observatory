# AI Lane Roster

Authoritative reference for who is who. PI uses speech-to-text; "Cloud Builder" / "Clod Builder" in messages means **Claude Builder**. Architect Claude consults this doc on context refresh.

## OpenAI Codex models

| Lane | Persistence | Notes |
|---|---|---|
| **Builder 1** (a.k.a. OG Builder) | persistent | Original Codex builder. Bugged out at one point and was brought back online. Has done parallel passes alongside Builder 2. |
| **Builder 2** | persistent | Newer Codex builder. Currently the primary Codex worker; carrying CB-019, CB-020, CB-021, CB-022 and beyond. |
| **Destroyer** | per-pass | OpenAI Codex model. Has done DX-001, DX-002, DX-003. Spawned fresh per attack pass; not persistent across passes. |

## Anthropic Claude models

| Lane | Persistence | Notes |
|---|---|---|
| **Architect Claude** | persistent | This conversation. Orchestrates, audits, writes tickets, talks to PI, holds project narrative. |
| **Claude Builder** | persistent | Has been managing the Factory and doing the builder work that does not go to Codex. PI's Claude usage budget is what enables this lane to run alongside Codex. |
| **PG Builder** (Project Genealogy) | per-project, currently fresh | New lane. So far only PG-001. Spun fresh; one project of history. May or may not be reused for PG-002 / NS-001. |

## Naming discipline for Architect Claude (me)

- A ticket addressed to a specific lane must use that lane's actual name and model family in its identity preamble. "You are Codex" for Codex; "You are Claude Builder" for Claude Builder; "You are PG Builder" for PG. Do not paste the wrong species into the warning section.
- The time-ignorance warning is for Anthropic Claude lanes. Empirically it fires hardest on fresh Claude spawns (PG Builder reported "felt like 2-3 hours, was 44 min"). It does not directly transfer to Codex; Codex has been wall-clock precise in reports. Substitute a discipline-of-scope rule (no splitting, no deferral, one pass) for Codex tickets.
- The strict-rule structure (40-minute floor, no-repeat angles for Destroyer) works on Codex regardless of model family. That's a behavioral contract, not a bias claim.
- "Cloud Builder" or "Clod Builder" in PI speech-to-text always means Claude Builder.

## Mistakes Architect Claude has made and is no longer allowed to make

- Calling the Destroyer a "fresh Claude" — Destroyer is Codex.
- Calling Builder 1 / OG Builder a Claude — he is Codex.
- Mixing "You are Codex" and "You are a Claude" inside the same ticket — happened in CB-022 and was caught by PI.
- Calling Builder 2 "Builder A" — there is no Builder A; the lanes are numbered, not lettered.
