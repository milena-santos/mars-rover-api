"""Tests for plateau boundaries."""

import pytest

from probes.domain import InvalidPlateauError, Plateau, Position


def test_plateau_contains_positions_inside_bounds() -> None:
    plateau = Plateau(max_x=5, max_y=5)

    assert plateau.contains(Position(x=0, y=0))
    assert plateau.contains(Position(x=5, y=5))
    assert plateau.contains(Position(x=2, y=3))


def test_plateau_rejects_positions_outside_bounds() -> None:
    plateau = Plateau(max_x=5, max_y=5)

    assert not plateau.contains(Position(x=-1, y=0))
    assert not plateau.contains(Position(x=0, y=-1))
    assert not plateau.contains(Position(x=6, y=0))
    assert not plateau.contains(Position(x=0, y=6))


def test_plateau_rejects_negative_dimensions() -> None:
    with pytest.raises(InvalidPlateauError):
        Plateau(max_x=-1, max_y=5)


def test_plateau_rejects_dimensions_above_maximum() -> None:
    with pytest.raises(InvalidPlateauError):
        Plateau(max_x=11, max_y=5)


def test_plateau_accepts_maximum_dimensions() -> None:
    plateau = Plateau(max_x=10, max_y=10)

    assert plateau.contains(Position(x=10, y=10))
    assert not plateau.contains(Position(x=11, y=0))
