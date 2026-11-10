"""Rectangular plateau that bounds probe movement."""

from __future__ import annotations

from dataclasses import dataclass

from probes.domain.exceptions import InvalidPlateauError
from probes.domain.position import Position


@dataclass(frozen=True, slots=True)
class Plateau:
    max_x: int
    max_y: int

    def __post_init__(self) -> None:
        if self.max_x < 0 or self.max_y < 0:
            raise InvalidPlateauError(
                "Plateau dimensions must be greater than or equal to zero."
            )

    def contains(self, position: Position) -> bool:
        return 0 <= position.x <= self.max_x and 0 <= position.y <= self.max_y
