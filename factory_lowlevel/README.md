# Low-Level Factory

The Factory is a daemon-safe ingestion path for source-bound empirical records.
It does not use AI at runtime. Adapters fetch or load authoritative seed
payloads, normalize records, route them into compatible worlds, simulate traces,
evaluate motif lenses, and persist exploratory outputs with provenance.

## World Coverage

TASK-035 extends the Factory routing surface to all 15 current worlds:

- W-1 `atomic_molecular_primitives`
- W0 `math_primitives`
- W1 `crn`
- W2 `protocell`
- W3 `field`
- W4 `morphogenesis`
- W5 `digital`
- W6 `ecosystem`
- W7 `swarm`
- W8 `cognitive`
- W9 `origins_chemistry`
- W10 `hypergraph_reactions`
- W11 `quasispecies`
- W12 `symbiogenesis`
- W13 `multiscale`

Each world has a `from_empirical_records()` constructor. Constructors accept only
records whose `world_family`, `record_type`, and required `world_parameters`
match the target world. Underdetermined records are rejected with a structured
reason and routed to audit rather than filled with invented values.

## Running A Single Live Cycle

```powershell
python - <<'PY'
from factory_lowlevel.live_pipeline import run_live_factory_cycle, summarize_run

run = run_live_factory_cycle(
    allow_network=False,
    store_root="reports/campaign_035/factory_store",
    cache_dir="reports/campaign_035/source_cache",
    run_root="reports/campaign_035/factory_runs",
    trace_root="reports/campaign_035/traces",
    trigger="manual_factory_cycle",
)
print(summarize_run(run))
PY
```

Use `allow_network=True` only when live refresh is intended. Tests and campaign
smokes use deterministic bundled-authoritative fallbacks so source behavior is
repeatable.

## Continuous Daemon

Windows launcher:

```powershell
.\factory_daemon.bat --cycles 1 --allow-network
```

Python entry point:

```powershell
python -m factory_lowlevel.continuous_daemon --cycles 1 --allow-network
```

Default daemon behavior:

- honors each source `refresh_cadence`;
- runs due sources independently so one adapter failure quarantines that source
  for the cycle while other due sources continue;
- retries transient failures with exponential backoff up to `--retry-ceiling`;
- refuses to run when source-cache or audit-queue disk budget is exceeded;
- writes a heartbeat at `control_room/cache/factory_daemon_heartbeat.json`;
- writes session records to `project_telemetry/factory_daemon_sessions.jsonl`;
- handles Ctrl-C by finishing the current cycle boundary and recording a clean
  stop state.

## Evidence Boundary

Generated trace files under `reports/*/traces/` and daemon trace folders are
private/generated evidence surfaces. Public run records that include `trace_path`
must carry:

```json
{
  "evidence_private": true,
  "trace_path_status": "private_unshipped"
}
```

This is a D23 boundary marker, not a scientific downgrade. It means the run
record is honest about where the detailed trace artifact lives.

## Verification

Focused TASK-035 checks:

```powershell
pytest tests\test_world_adapters_task035.py `
  public_tests\test_task035_world_adapters.py `
  public_tests\test_task035_fire_integration.py `
  public_tests\test_task035_continuous_daemon.py -q
```

