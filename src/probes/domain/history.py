"""Successful command execution telemetry for a probe."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from probes.domain.direction import Direction
from probes.domain.position import Position


@dataclass(frozen=True, slots=True)
class CommandHistoryEntry:
    id: UUID
    commands: str
    position: Position
    direction: Direction
    created_at: datetime
