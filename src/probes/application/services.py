"""Application services that orchestrate probe use cases."""

from __future__ import annotations

from uuid import UUID

from probes.application.ports import ProbeRepository
from probes.domain.command import Command
from probes.domain.direction import Direction
from probes.domain.exceptions import CollisionError, InvalidPlateauError
from probes.domain.history import CommandHistoryEntry
from probes.domain.plateau import Plateau
from probes.domain.position import Position
from probes.domain.probe import Probe


class ProbeService:
    def __init__(self, repository: ProbeRepository) -> None:
        self._repository = repository

    def launch(
        self,
        *,
        max_x: int,
        max_y: int,
        direction: Direction,
    ) -> Probe:
        requested = Plateau(max_x=max_x, max_y=max_y)
        shared = self._repository.get_shared_plateau()
        if shared is None:
            plateau = self._repository.create_shared_plateau(requested)
        elif shared != requested:
            raise InvalidPlateauError(
                "Launch dimensions must match the shared plateau "
                f"({shared.max_x}x{shared.max_y})."
            )
        else:
            plateau = shared

        landing = Position(x=0, y=0)
        occupied = self._repository.occupied_positions()
        if landing in occupied:
            raise CollisionError("Landing position (0, 0) is already occupied.")

        probe = Probe(plateau=plateau, direction=direction, position=landing)
        self._repository.add(probe)
        return probe

    def get_probe(self, *, probe_id: UUID) -> Probe:
        return self._repository.get(probe_id)

    def move(self, *, probe_id: UUID, commands: str) -> Probe:
        probe = self._repository.get(probe_id)
        occupied = self._repository.occupied_positions(exclude_probe_id=probe_id)
        probe.execute(Command.parse_sequence(commands), occupied=occupied)
        self._repository.save(probe)
        self._repository.add_command_log(probe, commands=commands)
        return probe

    def list_probes(self) -> list[Probe]:
        return self._repository.list_all()

    def list_history(self, *, probe_id: UUID) -> list[CommandHistoryEntry]:
        self._repository.get(probe_id)
        return self._repository.list_command_logs(probe_id)
