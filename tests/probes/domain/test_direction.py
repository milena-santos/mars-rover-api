"""Tests for direction rotation and movement."""

from probes.domain import Direction, Position


def test_turn_left_rotates_counter_clockwise() -> None:
    assert Direction.NORTH.turn_left() is Direction.WEST
    assert Direction.WEST.turn_left() is Direction.SOUTH
    assert Direction.SOUTH.turn_left() is Direction.EAST
    assert Direction.EAST.turn_left() is Direction.NORTH


def test_turn_right_rotates_clockwise() -> None:
    assert Direction.NORTH.turn_right() is Direction.EAST
    assert Direction.EAST.turn_right() is Direction.SOUTH
    assert Direction.SOUTH.turn_right() is Direction.WEST
    assert Direction.WEST.turn_right() is Direction.NORTH


def test_move_from_advances_one_step() -> None:
    origin = Position(x=1, y=1)

    assert Direction.NORTH.move_from(origin) == Position(x=1, y=2)
    assert Direction.EAST.move_from(origin) == Position(x=2, y=1)
    assert Direction.SOUTH.move_from(origin) == Position(x=1, y=0)
    assert Direction.WEST.move_from(origin) == Position(x=0, y=1)
