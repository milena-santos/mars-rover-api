"""Application services that orchestrate probe use cases."""

from __future__ import annotations

from uuid import UUID

from probes.application.ports import ProbeRepository
from probes.domain.command import Command
from probes.domain.direction import Direction
from probes.domain.plateau import Plateau
from probes.domain.probe import Probe


class ProbeService:
    def __init__(self, repository: ProbeRepository) -> None:
        self._repository = repository

    def launch(self, *, max_x: int, max_y: int, direction: Direction) -> Probe:
        probe = Probe(plateau=Plateau(max_x=max_x, max_y=max_y), direction=direction)
        self._repository.add(probe)
        return probe

    def move(self, *, probe_id: UUID, commands: str) -> Probe:
        probe = self._repository.get(probe_id)
        probe.execute(Command.parse_sequence(commands))
        self._repository.save(probe)
        return probe

    def list_probes(self) -> list[Probe]:
        return self._repository.list_all()
