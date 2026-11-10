"""Probe state and atomic command execution."""

from __future__ import annotations

from dataclasses import dataclass, field

from probes.domain.command import Command
from probes.domain.direction import Direction
from probes.domain.exceptions import OutOfBoundsError
from probes.domain.plateau import Plateau
from probes.domain.position import Position


@dataclass(slots=True)
class Probe:
    plateau: Plateau
    direction: Direction
    position: Position = field(default_factory=lambda: Position(x=0, y=0))

    def __post_init__(self) -> None:
        if not self.plateau.contains(self.position):
            raise OutOfBoundsError(
                f"Position ({self.position.x}, {self.position.y}) "
                "is outside the plateau."
            )

    def execute(self, commands: tuple[Command, ...]) -> None:
        next_position = self.position
        next_direction = self.direction

        for command in commands:
            if command is Command.LEFT:
                next_direction = next_direction.turn_left()
                continue
            if command is Command.RIGHT:
                next_direction = next_direction.turn_right()
                continue

            candidate = next_direction.move_from(next_position)
            if not self.plateau.contains(candidate):
                raise OutOfBoundsError(
                    "Command sequence would move the probe outside the plateau."
                )
            next_position = candidate

        self.position = next_position
        self.direction = next_direction
