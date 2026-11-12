"""Persistence ports used by application services."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from probes.domain.history import CommandHistoryEntry
from probes.domain.plateau import Plateau
from probes.domain.position import Position
from probes.domain.probe import Probe


class ProbeRepository(Protocol):
    def get_shared_plateau(self) -> Plateau | None:
        """Return the shared plateau when one already exists."""

    def create_shared_plateau(self, plateau: Plateau) -> Plateau:
        """Persist the first shared plateau for the mission."""

    def replace_shared_plateau(self, plateau: Plateau) -> Plateau:
        """Replace the shared plateau when the mission has no probes."""

    def occupied_positions(
        self, *, exclude_probe_id: UUID | None = None
    ) -> frozenset[Position]:
        """Return positions currently held by probes."""

    def find_id_at(self, position: Position) -> UUID | None:
        """Return the probe id occupying a position, if any."""

    def add(self, probe: Probe) -> None:
        """Persist a newly created probe."""

    def get(self, probe_id: UUID) -> Probe:
        """Load one probe by id or raise ProbeNotFoundError."""

    def list_all(self) -> list[Probe]:
        """Return all probes ordered by creation time."""

    def save(self, probe: Probe) -> None:
        """Update an existing probe or raise ProbeNotFoundError."""

    def delete_many(self, probe_ids: list[UUID]) -> None:
        """Remove the given probes and their command history."""

    def add_command_log(self, probe: Probe, *, commands: str) -> CommandHistoryEntry:
        """Persist a successful command sequence for telemetry."""

    def list_command_logs(self, probe_id: UUID) -> list[CommandHistoryEntry]:
        """Return successful command history for one probe."""

    def clear_all(self) -> None:
        """Remove every probe, command log, and shared plateau."""
