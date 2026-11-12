"""Application services that orchestrate probe use cases."""

from __future__ import annotations

from uuid import UUID

from probes.application.move_result import (
    CollisionOutcome,
    LaunchResult,
    MoveResult,
    MoveSuccess,
)
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
    ) -> LaunchResult:
        requested = Plateau(max_x=max_x, max_y=max_y)
        shared = self._repository.get_shared_plateau()
        active_probes = self._repository.list_all()
        if shared is None:
            plateau = self._repository.create_shared_plateau(requested)
        elif shared == requested:
            plateau = shared
        elif not active_probes:
            plateau = self._repository.replace_shared_plateau(requested)
        else:
            raise InvalidPlateauError(
                "Launch dimensions must match the shared plateau "
                f"({shared.max_x}x{shared.max_y})."
            )

        landing = Position(x=0, y=0)
        incoming = Probe(plateau=plateau, direction=direction, position=landing)
        other_id = self._repository.find_id_at(landing)
        if other_id is not None:
            self._repository.delete_many([other_id])
            return CollisionOutcome(
                position=landing,
                destroyed=(incoming.id, other_id),
            )

        self._repository.add(incoming)
        return incoming

    def get_probe(self, *, probe_id: UUID) -> Probe:
        return self._repository.get(probe_id)

    def move(self, *, probe_id: UUID, commands: str) -> MoveResult:
        probe = self._repository.get(probe_id)
        occupied = self._repository.occupied_positions(exclude_probe_id=probe_id)
        try:
            probe.execute(Command.parse_sequence(commands), occupied=occupied)
        except CollisionError as exc:
            other_id = self._repository.find_id_at(exc.position)
            destroyed: list[UUID] = [probe_id]
            if other_id is not None and other_id != probe_id:
                destroyed.append(other_id)
            self._repository.delete_many(destroyed)
            return CollisionOutcome(
                position=exc.position,
                destroyed=tuple(destroyed),
            )

        self._repository.save(probe)
        self._repository.add_command_log(probe, commands=commands)
        return MoveSuccess(probe=probe)

    def list_probes(self) -> list[Probe]:
        return self._repository.list_all()

    def list_history(self, *, probe_id: UUID) -> list[CommandHistoryEntry]:
        self._repository.get(probe_id)
        return self._repository.list_command_logs(probe_id)

    def clear_all(self) -> None:
        self._repository.clear_all()
