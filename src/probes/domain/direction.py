"""Cardinal directions used by probes."""

from __future__ import annotations

from enum import StrEnum

from probes.domain.position import Position


class Direction(StrEnum):
    NORTH = "NORTH"
    EAST = "EAST"
    SOUTH = "SOUTH"
    WEST = "WEST"

    def turn_left(self) -> Direction:
        order = (
            Direction.NORTH,
            Direction.WEST,
            Direction.SOUTH,
            Direction.EAST,
        )
        return order[(order.index(self) + 1) % len(order)]

    def turn_right(self) -> Direction:
        order = (
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        )
        return order[(order.index(self) + 1) % len(order)]

    def move_from(self, position: Position) -> Position:
        deltas = {
            Direction.NORTH: (0, 1),
            Direction.EAST: (1, 0),
            Direction.SOUTH: (0, -1),
            Direction.WEST: (-1, 0),
        }
        delta_x, delta_y = deltas[self]
        return Position(x=position.x + delta_x, y=position.y + delta_y)


DIRECTION_VALUES = (
    Direction.NORTH.value,
    Direction.EAST.value,
    Direction.SOUTH.value,
    Direction.WEST.value,
)

DIRECTION_CHOICES = (
    (Direction.NORTH.value, Direction.NORTH.value),
    (Direction.EAST.value, Direction.EAST.value),
    (Direction.SOUTH.value, Direction.SOUTH.value),
    (Direction.WEST.value, Direction.WEST.value),
)
