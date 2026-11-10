"""Movement and rotation commands accepted by a probe."""

from __future__ import annotations

from enum import StrEnum

from probes.domain.exceptions import InvalidCommandError


class Command(StrEnum):
    LEFT = "L"
    RIGHT = "R"
    MOVE = "M"

    @classmethod
    def parse_sequence(cls, raw: str) -> tuple[Command, ...]:
        commands: list[Command] = []
        for index, symbol in enumerate(raw):
            try:
                commands.append(cls(symbol))
            except ValueError as exc:
                raise InvalidCommandError(
                    f"Invalid command '{symbol}' at position {index}."
                ) from exc
        return tuple(commands)
