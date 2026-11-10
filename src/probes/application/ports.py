"""Persistence ports used by application services."""

from __future__ import annotations

from typing import Protocol
from uuid import UUID

from probes.domain.probe import Probe


class ProbeRepository(Protocol):
    def add(self, probe: Probe) -> None:
        """Persist a newly created probe."""

    def get(self, probe_id: UUID) -> Probe:
        """Load one probe by id or raise ProbeNotFoundError."""

    def list_all(self) -> list[Probe]:
        """Return all probes ordered by creation time."""

    def save(self, probe: Probe) -> None:
        """Update an existing probe or raise ProbeNotFoundError."""
