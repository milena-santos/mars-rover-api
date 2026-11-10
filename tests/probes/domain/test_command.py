"""Tests for command sequence parsing."""

import pytest

from probes.domain import Command, InvalidCommandError


def test_parse_sequence_returns_known_commands() -> None:
    assert Command.parse_sequence("LMR") == (
        Command.LEFT,
        Command.MOVE,
        Command.RIGHT,
    )


def test_parse_sequence_allows_empty_input() -> None:
    assert Command.parse_sequence("") == ()


def test_parse_sequence_rejects_unknown_symbols() -> None:
    with pytest.raises(InvalidCommandError, match="position 1"):
        Command.parse_sequence("MXM")
