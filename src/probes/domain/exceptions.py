"""Domain errors for probe navigation."""

from __future__ import annotations

from probes.domain.position import Position


class InvalidCommandError(ValueError):
    """Raised when a command sequence contains an unknown command."""


class InvalidPlateauError(ValueError):
    """Raised when plateau dimensions are invalid."""


class OutOfBoundsError(ValueError):
    """Raised when a probe would leave the plateau."""


class CollisionError(ValueError):
    """Raised when a probe would occupy another probe's position."""

    def __init__(self, message: str, *, position: Position) -> None:
        super().__init__(message)
        self.position = position


class ProbeNotFoundError(LookupError):
    """Raised when a probe id does not exist in storage."""
