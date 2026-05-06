# Campaign 035: Mass-Ingestion Prerequisite Build

## Mode

`mode_tag: exploratory`

Campaign 035 extends the Factory from a seven-world pilot to a full 15-world
ingestion surface. The campaign does not promote any motif claim. Its purpose is
operational: establish deterministic source adapters, world constructors,
continuous-cycle daemon mechanics, and evidence-boundary markers required before
mass ingestion can run unattended.

## Adapter Expansion

Eight adapters were added for the previously missing world families:

| World | Adapter | Source boundary | Runtime policy |
| --- | --- | --- | --- |
| W2 Protocell | `SzostakLiposomeProtocellAdapter` | peer-reviewed liposome / vesicle benchmark literature | bundled authoritative seed, optional live URL validation |
| W4 Morphogenesis | `FlyBaseMorphogenProfileAdapter` | FlyBase / VirtualFlyBrain public source boundary | bundled authoritative seed, optional live URL validation |
| W5 Digital | `AvidaDigitalTraceAdapter` | Avida / Lenski-Ofria-Adami literature boundary | bundled authoritative seed, optional live URL validation |
| W7 Swarm | `MovebankSwarmBehaviorAdapter` | Movebank movement-data authority boundary | bundled authoritative seed, optional live URL validation |
| W8 Cognitive | `AllenBrainCognitiveAdapter` | Allen Brain Atlas public portal boundary | bundled authoritative seed, optional live URL validation |
| W10 Hypergraph | `BioModelsHypergraphAdapter` | EMBL-EBI BioModels boundary | bundled authoritative seed, optional live URL validation |
| W12 Symbiogenesis | `NCBIEndosymbiosisGenomeAdapter` | NCBI genome record boundary | bundled authoritative seed, optional live URL validation |
| W13 Multiscale | `PhysiomeMultiscaleAdapter` | Physiome model repository boundary | bundled authoritative seed, optional live URL validation |

The adapters are conservative. They store compact derived parameters and
provenance, not raw dataset dumps. Missing `world_parameters` emits an
`AdapterAudit` item. Live network mode validates the source boundary when
requested; failed validation falls back to the bundled authoritative seed and
surfaces a warning.

## World Constructors

All 15 worlds now expose `from_empirical_records()`:

- W-1 and W0 accept source-bound record payloads as construction parameters.
- W1, W3, W6, W9, and W11 retain their TASK-033 constructors.
- W2, W4, W5, W7, W8, W10, W12, and W13 consume deterministic
  `world_parameters` from the new adapters.

The shared constructor helper enforces:

- `world_family` match;
- accepted `record_type`;
- required `world_parameters`, unless the world explicitly accepts records as
  parameters;
- structured rejection on mismatch or construction failure.

No constructor fills missing values with fabricated defaults to force a trace.

## Continuous Daemon

`factory_lowlevel.continuous_daemon` and `factory_daemon.bat` provide unattended
cycle execution.

Quality gates implemented:

- source-level cadence checks via `refresh_cadence`;
- one due source per run, so failure quarantines only that source for the cycle;
- retry ceiling with exponential backoff;
- disk-budget refusal before writes;
- heartbeat output for liveness detection;
- JSONL session ledger;
- Ctrl-C stop request handling at the cycle boundary.

## Evidence Boundary

Generated trace references in public run records carry:

```json
{
  "evidence_private": true,
  "trace_path_status": "private_unshipped"
}
```

This applies both to `trace_records` and `life_forms`. It preserves D23:
evidence paths either dereference in the shipped surface or declare a private
boundary at point of use.

## Verification

Observed campaign smoke:

- adapters selected: 16;
- worlds simulated: 15;
- records ingested: 32;
- traces produced: 32;
- routing rejections: 0.

Relevant verification pass:

```text
42 passed in 62.66s
```

The test slice covered Campaign 016, Campaign 019, public contracts, TASK-033,
and TASK-035 adapter, FIRE integration, and continuous-daemon tests.

Live-validation smoke for the eight new curated adapters:

- 7/8 source boundaries validated with `network_validated_bundled_authoritative_seed`.
- `PhysiomeMultiscaleAdapter` surfaced one `URLError` and fell back to
  `bundled_authoritative_seed`.

That fallback is acceptable for this campaign because the adapter still emits a
warning and stores only source-bound derived parameters. It should remain visible
in future live daemon sessions rather than being suppressed.
