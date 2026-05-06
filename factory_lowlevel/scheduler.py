"""Simple autonomous scheduler surface for the low-level Factory.

Campaign 016 does not install a persistent service. It ships the deterministic
loop/plan object a future Windows Task Scheduler entry or daemon can invoke.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FactorySchedule:
    schedule_id: str
    mode: str
    cadence_seconds: int
    command: str
    dry_run_default: bool
    requires_ai_runtime: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": "LowLevelFactorySchedule.v1",
            "schedule_id": self.schedule_id,
            "mode": self.mode,
            "cadence_seconds": self.cadence_seconds,
            "command": self.command,
            "dry_run_default": self.dry_run_default,
            "requires_ai_runtime": self.requires_ai_runtime,
            "windows_task_scheduler_hint": (
                "schtasks /Create /SC HOURLY /TN AttractorLowLevelFactory "
                "/TR \"python observatory_cli.py campaign016 --routine-ingest\""
            ),
        }


def default_schedule() -> FactorySchedule:
    return FactorySchedule(
        schedule_id="factory.low_level.hourly.dry_run",
        mode="loop_or_task_scheduler",
        cadence_seconds=3600,
        command="python observatory_cli.py campaign016 --routine-ingest",
        dry_run_default=True,
    )
