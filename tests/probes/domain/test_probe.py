"""Tests for atomic probe command execution."""

import pytest

from probes.domain import (
    CollisionError,
    Command,
    Direction,
    OutOfBoundsError,
    Plateau,
    Position,
    Probe,
)


def test_probe_starts_at_origin_by_default() -> None:
    probe = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.NORTH)

    assert probe.position == Position(x=0, y=0)
    assert probe.direction is Direction.NORTH


def test_execute_matches_challenge_example() -> None:
    probe = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.NORTH)

    probe.execute(Command.parse_sequence("MRM"), occupied=frozenset())

    assert probe.position == Position(x=1, y=1)
    assert probe.direction is Direction.EAST


def test_execute_rotates_left_without_moving() -> None:
    probe = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.NORTH)

    probe.execute(Command.parse_sequence("L"), occupied=frozenset())

    assert probe.position == Position(x=0, y=0)
    assert probe.direction is Direction.WEST


def test_execute_is_atomic_when_sequence_leaves_plateau() -> None:
    probe = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.WEST)
    original_position = probe.position
    original_direction = probe.direction

    with pytest.raises(OutOfBoundsError):
        probe.execute(Command.parse_sequence("M"), occupied=frozenset())

    assert probe.position == original_position
    assert probe.direction is original_direction


def test_execute_is_atomic_for_later_out_of_bounds_command() -> None:
    probe = Probe(plateau=Plateau(max_x=1, max_y=1), direction=Direction.NORTH)

    with pytest.raises(OutOfBoundsError):
        probe.execute(Command.parse_sequence("MRMM"), occupied=frozenset())

    assert probe.position == Position(x=0, y=0)
    assert probe.direction is Direction.NORTH


def test_execute_is_atomic_when_sequence_collides() -> None:
    probe = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.NORTH)
    occupied = frozenset({Position(x=0, y=1)})

    with pytest.raises(CollisionError):
        probe.execute(Command.parse_sequence("MRM"), occupied=occupied)

    assert probe.position == Position(x=0, y=0)
    assert probe.direction is Direction.NORTH


def test_execute_empty_sequence_keeps_state() -> None:
    probe = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.SOUTH)

    probe.execute((), occupied=frozenset())

    assert probe.position == Position(x=0, y=0)
    assert probe.direction is Direction.SOUTH


def test_probe_rejects_initial_position_outside_plateau() -> None:
    with pytest.raises(OutOfBoundsError):
        Probe(
            plateau=Plateau(max_x=1, max_y=1),
            direction=Direction.NORTH,
            position=Position(x=2, y=0),
        )
