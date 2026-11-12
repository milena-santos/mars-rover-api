"""Result types for probe launch and movement."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from probes.domain.position import Position
from probes.domain.probe import Probe


@dataclass(frozen=True, slots=True)
class MoveSuccess:
    probe: Probe


@dataclass(frozen=True, slots=True)
class CollisionOutcome:
    position: Position
    destroyed: tuple[UUID, ...]


MoveResult = MoveSuccess | CollisionOutcome
LaunchResult = Probe | CollisionOutcome
