"""W2 protocell world with membrane maintenance, repair, division, and lineage."""

from __future__ import annotations

import json
import math
from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from core.ids import content_id
from core.rng import RNG
from trace.schema.v1 import canonical_json, empty_trace, trace_content_hash


@dataclass
class Protocell:
    entity_id: str
    parent_ids: list[str]
    membrane_material: float
    membrane_integrity: float
    internal_resource: float
    internal_waste: float
    closure_marker: float
    alive: bool = True
    mutation_count: int = 0
    birth_t: float = 0.0
    death_t: float | None = None
    position: tuple[float, float] = (0.0, 0.0)

    def mass(self) -> float:
        return self.membrane_material + self.internal_resource + self.internal_waste + self.closure_marker


@dataclass
class ProtocellWorld:
    family: str = "protocell"
    implementation_id: str = "w2.protocell.boundary_dynamics"
    implementation_version: str = "0.1.0"
    seed: int = 0
    rng: RNG = field(default_factory=lambda: RNG(root_seed=0).split("protocell"))
    t: float = 0.0
    params: dict[str, Any] = field(default_factory=dict)
    cells: dict[str, Protocell] = field(default_factory=dict)
    states: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    boundaries: list[dict[str, Any]] = field(default_factory=list)
    material_ledger: list[dict[str, Any]] = field(default_factory=list)
    invariant_checks: list[dict[str, Any]] = field(default_factory=list)
    lineage_edges: list[dict[str, Any]] = field(default_factory=list)
    entity_counter: int = 0
    initial_mass: float = 0.0
    division_records: list[dict[str, float]] = field(default_factory=list)

    @classmethod
    def from_empirical_records(cls, records: list[Any], *, seed: int = 3302) -> dict[str, Any]:
        from factory_lowlevel.world_construction import construct_world_from_records

        return construct_world_from_records(
            cls,
            records,
            expected_world="protocell",
            accepted_record_types={"liposome_protocell_benchmark"},
            seed=seed,
            steps_default=36,
            dt_default=0.25,
        )

    def reset(self, seed: int, params: dict[str, Any]) -> dict[str, Any]:
        self.seed = seed
        self.rng = RNG(root_seed=seed).split("protocell")
        self.t = 0.0
        self.params = deepcopy(params)
        self.cells = {}
        self.states = []
        self.events = []
        self.boundaries = []
        self.material_ledger = []
        self.invariant_checks = []
        self.lineage_edges = []
        self.entity_counter = 0
        self.division_records = []
        self._birth_cell(
            parent_ids=[],
            membrane_material=float(params.get("initial_membrane_material", 10.0)),
            membrane_integrity=float(params.get("initial_membrane_integrity", 1.0)),
            internal_resource=float(params.get("initial_internal_resource", 8.0)),
            internal_waste=0.0,
            closure_marker=float(params.get("initial_closure_marker", 2.0)),
            position=(0.0, 0.0),
        )
        self.initial_mass = self._total_mass()
        self._record_state()
        return self.observe()

    def _next_entity_id(self) -> str:
        self.entity_counter += 1
        return f"pcell-{self.seed}-{self.entity_counter}"

    def _emit_event(self, event_type: str, payload: dict[str, Any], *, entity_id: str | None = None) -> dict[str, Any]:
        event = {
            "event_id": str(content_id("event", {"t": self.t, "index": len(self.events), "type": event_type, "payload": payload})),
            "type": event_type,
            "t_sim": self.t,
            "source": "protocell_world",
            "causes": [],
            "confidence": None,
            "payload": payload,
        }
        if entity_id is not None:
            event["entity_id"] = entity_id
        self.events.append(event)
        return event

    def _birth_cell(
        self,
        *,
        parent_ids: list[str],
        membrane_material: float,
        membrane_integrity: float,
        internal_resource: float,
        internal_waste: float,
        closure_marker: float,
        position: tuple[float, float],
    ) -> Protocell:
        cell = Protocell(
            entity_id=self._next_entity_id(),
            parent_ids=list(parent_ids),
            membrane_material=membrane_material,
            membrane_integrity=membrane_integrity,
            internal_resource=internal_resource,
            internal_waste=internal_waste,
            closure_marker=closure_marker,
            birth_t=self.t,
            position=position,
        )
        self.cells[cell.entity_id] = cell
        self._emit_event(
            "birth_event",
            {"entity_id": cell.entity_id, "parent_ids": parent_ids, "mass": cell.mass()},
            entity_id=cell.entity_id,
        )
        for parent in parent_ids:
            self.lineage_edges.append({"parent": parent, "child": cell.entity_id, "event_type": "birth_event", "t_sim": self.t})
        return cell

    def _total_mass(self) -> float:
        return sum(cell.mass() for cell in self.cells.values() if cell.alive)

    def _membrane_particles(self, cell: Protocell) -> list[dict[str, float]]:
        count = max(8, int(round(cell.membrane_material)))
        radius = math.sqrt(max(cell.membrane_material, 1.0)) / math.pi
        particles = []
        missing_arc = max(0.0, 1.0 - cell.membrane_integrity) * math.pi
        for index in range(count):
            angle = (2.0 * math.pi * index) / count
            present = not (missing_arc > 0 and -missing_arc / 2.0 <= math.atan2(math.sin(angle), math.cos(angle)) <= missing_arc / 2.0)
            if present:
                particles.append(
                    {
                        "x": cell.position[0] + radius * math.cos(angle),
                        "y": cell.position[1] + radius * math.sin(angle),
                        "angle": angle,
                    }
                )
        return particles

    def _record_state(self) -> None:
        alive_cells = [cell for cell in self.cells.values() if cell.alive]
        state = {
            "t_sim": self.t,
            "state": {
                "alive_count": float(len(alive_cells)),
                "total_membrane_material": sum(cell.membrane_material for cell in alive_cells),
                "mean_membrane_integrity": sum(cell.membrane_integrity for cell in alive_cells) / max(len(alive_cells), 1),
                "total_internal_resource": sum(cell.internal_resource for cell in alive_cells),
                "total_external_resource": float(self.params.get("external_resource", 20.0)),
                "total_closure_marker": sum(cell.closure_marker for cell in alive_cells),
                "total_waste": sum(cell.internal_waste for cell in alive_cells),
            },
            "entities": {
                cell.entity_id: {
                    "alive": cell.alive,
                    "parent_ids": cell.parent_ids,
                    "membrane_material": cell.membrane_material,
                    "membrane_integrity": cell.membrane_integrity,
                    "internal_resource": cell.internal_resource,
                    "internal_waste": cell.internal_waste,
                    "closure_marker": cell.closure_marker,
                    "mutation_count": cell.mutation_count,
                    "position": list(cell.position),
                }
                for cell in self.cells.values()
            },
        }
        self.states.append(state)
        for cell in self.cells.values():
            if not cell.alive:
                continue
            particles = self._membrane_particles(cell)
            angular_gaps = []
            if particles:
                angles = sorted(item["angle"] for item in particles)
                angular_gaps = [
                    (angles[(index + 1) % len(angles)] - angles[index]) % (2.0 * math.pi)
                    for index in range(len(angles))
                ]
            closed_cycle = bool(angular_gaps) and max(angular_gaps) < math.pi / 2.0
            self.boundaries.append(
                {
                    "t_sim": self.t,
                    "entity_id": cell.entity_id,
                    "boundary_kind": self.params.get("boundary_kind", "passive"),
                    "membrane_integrity": cell.membrane_integrity,
                    "membrane_material": cell.membrane_material,
                    "permeability": self._permeability(cell),
                    "particle_count": len(particles),
                    "max_angular_gap": max(angular_gaps, default=2.0 * math.pi),
                    "closed_cycle": closed_cycle,
                    "particles": particles,
                }
            )
        residual = self._total_mass() - self.initial_mass
        self.material_ledger.append({"t_sim": self.t, "total_mass": self._total_mass(), "mass_residual": residual})
        self.invariant_checks.append(
            {
                "invariant_id": "protocell.mass_nonnegative",
                "t_sim": self.t,
                "residual": min((cell.mass() for cell in alive_cells), default=0.0),
                "tolerance": 0.0,
                "passed": all(cell.mass() >= -1e-9 for cell in alive_cells),
            }
        )

    def _permeability(self, cell: Protocell) -> float:
        base = float(self.params.get("base_permeability", 0.05))
        return base + (1.0 - cell.membrane_integrity) * float(self.params.get("puncture_permeability_boost", 0.35))

    def _apply_puncture(self, cell: Protocell) -> None:
        if abs(self.t - float(self.params.get("puncture_time", 4.0))) > 1e-9:
            return
        damage = float(self.params.get("puncture_damage", 0.45))
        cell.membrane_integrity = max(0.0, cell.membrane_integrity - damage)
        removed = min(cell.membrane_material, damage * cell.membrane_material * 0.2)
        cell.membrane_material -= removed
        self._emit_event(
            "boundary_event",
            {"entity_id": cell.entity_id, "action": "puncture", "damage": damage, "removed_membrane_material": removed},
            entity_id=cell.entity_id,
        )

    def _repair_and_metabolise(self, cell: Protocell, dt: float) -> None:
        if not cell.alive:
            return
        permeability = self._permeability(cell)
        external = float(self.params.get("external_resource", 20.0))
        inflow = permeability * external * dt
        leak = permeability * (1.0 - cell.membrane_integrity) * cell.internal_resource * dt
        cell.internal_resource = max(0.0, cell.internal_resource + inflow - leak)
        cell.internal_waste += leak * 0.35

        kind = self.params.get("boundary_kind", "passive")
        internally_produced = bool(self.params.get("internal_produces_boundary", False))
        active_external = bool(self.params.get("external_repairs_boundary", False))
        production = 0.0
        if internally_produced and cell.internal_resource > 0.0:
            production = min(cell.internal_resource, float(self.params.get("membrane_production_rate", 0.18)) * cell.internal_resource * dt)
            cell.internal_resource -= production
            cell.membrane_material += production
            cell.closure_marker += production * 0.1
        elif active_external:
            production = float(self.params.get("external_repair_rate", 0.08)) * dt
            cell.membrane_material += production

        repair_rate = float(self.params.get("repair_rate", 0.0))
        if kind in {"active", "self_maintained", "heritable"} and repair_rate > 0.0:
            repair_source = production if internally_produced else float(self.params.get("external_repair_rate", 0.08)) * dt
            recovery = min(1.0 - cell.membrane_integrity, repair_rate * max(repair_source, 0.01))
            if recovery > 0.0:
                cell.membrane_integrity += recovery
                self._emit_event(
                    "repair_event",
                    {
                        "entity_id": cell.entity_id,
                        "recovery": recovery,
                        "internal_boundary_production": internally_produced,
                        "external_repair": active_external and not internally_produced,
                    },
                    entity_id=cell.entity_id,
                )
        if cell.membrane_integrity < float(self.params.get("death_integrity_threshold", 0.2)):
            cell.alive = False
            cell.death_t = self.t
            self._emit_event("death_event", {"entity_id": cell.entity_id, "reason": "boundary_failure"}, entity_id=cell.entity_id)

    def _divide_if_needed(self, cell: Protocell) -> None:
        threshold = float(self.params.get("division_threshold", 12.5))
        if threshold <= 0:
            return
        if not cell.alive or cell.membrane_material < threshold:
            return
        parent_mass = cell.mass()
        fidelity = float(self.params.get("division_fidelity", 0.96))
        words, self.rng = self.rng.draw_u32(1)
        mutated = (words[0] / 2**32) > fidelity
        mutation_count = 1 if mutated else 0
        child_mass_factor = 0.5
        child_positions = [(cell.position[0] - 0.1, cell.position[1]), (cell.position[0] + 0.1, cell.position[1])]
        payload_children = []
        for position in child_positions:
            child = self._birth_cell(
                parent_ids=[cell.entity_id],
                membrane_material=cell.membrane_material * child_mass_factor,
                membrane_integrity=max(0.8, cell.membrane_integrity),
                internal_resource=cell.internal_resource * child_mass_factor,
                internal_waste=cell.internal_waste * child_mass_factor,
                closure_marker=cell.closure_marker * child_mass_factor,
                position=position,
            )
            child.mutation_count = cell.mutation_count + mutation_count
            payload_children.append(child.entity_id)
        cell.alive = False
        cell.death_t = self.t
        child_mass = sum(self.cells[child_id].mass() for child_id in payload_children)
        self.division_records.append({"parent_mass": parent_mass, "child_mass": child_mass, "residual": child_mass - parent_mass})
        self._emit_event(
            "division_event",
            {
                "parent_id": cell.entity_id,
                "child_ids": payload_children,
                "parent_mass": parent_mass,
                "child_mass": child_mass,
                "mass_residual": child_mass - parent_mass,
                "mutation_occurred": mutated,
                "declared_fidelity": fidelity,
            },
            entity_id=cell.entity_id,
        )
        self._emit_event("death_event", {"entity_id": cell.entity_id, "reason": "division"}, entity_id=cell.entity_id)

    def step(self, dt: float) -> dict[str, Any]:
        self.t = round(self.t + dt, 12)
        for cell in list(self.cells.values()):
            if not cell.alive:
                continue
            self._apply_puncture(cell)
            self._repair_and_metabolise(cell, dt)
        for cell in list(self.cells.values()):
            self._divide_if_needed(cell)
        self._record_state()
        return self.observe()

    def observe(self) -> dict[str, Any]:
        return {"t_sim": self.t, "alive_count": sum(1 for cell in self.cells.values() if cell.alive)}

    def export_trace(self, output_path: str | Path) -> dict[str, Any]:
        manifest = {
            "schema_version": "1.0.0",
            "world_family": self.family,
            "world_implementation_id": self.implementation_id,
            "world_implementation_ver": self.implementation_version,
            "root_seed": self.seed,
            "rng_algorithm": self.rng.algorithm,
            "rng_initial_state_hash": RNG(root_seed=self.seed).split("protocell").state_hash(),
            "rng_final_state_hash": self.rng.state_hash(),
            "determinism_class": "replayable_to_eps",
            "determinism_eps": 1e-9,
            "license_class": "cc0",
            "retention_class": "indexed",
            "notes": "Campaign 002 W2 protocell trace.",
        }
        trace = empty_trace(manifest={**manifest, "trace_id": None}, parameter_record=self.params, mode_tag="exploratory", campaign_id="campaign-002")
        trace["state"] = self.states
        trace["events"] = self.events
        trace["boundaries"] = self.boundaries
        trace["material_ledger"] = self.material_ledger
        trace["invariant_checks"] = self.invariant_checks
        trace["entities"] = {
            entity_id: {
                "parent_ids": cell.parent_ids,
                "birth_t": cell.birth_t,
                "death_t": cell.death_t,
                "alive": cell.alive,
                "mutation_count": cell.mutation_count,
            }
            for entity_id, cell in self.cells.items()
        }
        trace["lineage"] = {"nodes": sorted(trace["entities"]), "edges": self.lineage_edges}
        trace["measurements"].append({"name": "division_records", "value": self.division_records, "t_sim": self.t})
        trace["manifest"]["trace_id"] = "sha256:" + trace_content_hash(trace)
        trace["signatures"].append(
            {
                "signature_id": "writer-content-hash",
                "signature_scheme": "sha256-trace-payload",
                "signature_hash": trace["manifest"]["trace_id"],
                "limitations": "Content hash signature only.",
            }
        )
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(canonical_json(trace) + "\n", encoding="utf-8")
        return trace


def protocell_scenario(
    scenario_id: str = "W2-self-maintained-protocell",
    *,
    boundary_kind: str = "self_maintained",
    internal_produces_boundary: bool = True,
    external_repairs_boundary: bool = False,
    heritable: bool = False,
    division_threshold: float = 11.5,
    mutation_rate: float = 0.04,
    puncture_damage: float = 0.45,
) -> dict[str, Any]:
    return {
        "scenario_id": scenario_id,
        "boundary_kind": boundary_kind,
        "internal_produces_boundary": internal_produces_boundary,
        "external_repairs_boundary": external_repairs_boundary,
        "heritable_boundary_production": heritable,
        "initial_membrane_material": 10.5,
        "initial_membrane_integrity": 1.0,
        "initial_internal_resource": 9.0,
        "initial_closure_marker": 2.0,
        "external_resource": 18.0,
        "base_permeability": 0.04,
        "puncture_permeability_boost": 0.35,
        "membrane_production_rate": 0.22 if internal_produces_boundary else 0.0,
        "repair_rate": 1.8 if boundary_kind in {"active", "self_maintained", "heritable"} else 0.0,
        "external_repair_rate": 0.16 if external_repairs_boundary else 0.0,
        "puncture_time": 4.0,
        "puncture_damage": puncture_damage,
        "division_threshold": division_threshold,
        "division_fidelity": 1.0 - mutation_rate,
        "death_integrity_threshold": 0.18,
    }
