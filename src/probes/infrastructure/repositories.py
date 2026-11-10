"""Django ORM adapter for the ProbeRepository port."""

from __future__ import annotations

from uuid import UUID

from probes.domain.direction import Direction
from probes.domain.exceptions import ProbeNotFoundError
from probes.domain.plateau import Plateau
from probes.domain.position import Position
from probes.domain.probe import Probe
from probes.infrastructure.models import ProbeRecord


class DjangoProbeRepository:
    def add(self, probe: Probe) -> None:
        ProbeRecord.objects.create(
            id=probe.id,
            x=probe.position.x,
            y=probe.position.y,
            direction=probe.direction.value,
            plateau_max_x=probe.plateau.max_x,
            plateau_max_y=probe.plateau.max_y,
        )

    def get(self, probe_id: UUID) -> Probe:
        try:
            record = ProbeRecord.objects.get(pk=probe_id)
        except ProbeRecord.DoesNotExist as exc:
            raise ProbeNotFoundError(f"Probe '{probe_id}' was not found.") from exc
        return self._to_domain(record)

    def list_all(self) -> list[Probe]:
        probes = []
        for record in ProbeRecord.objects.all():
            probes.append(self._to_domain(record))
        return probes

    def save(self, probe: Probe) -> None:
        try:
            record = ProbeRecord.objects.get(pk=probe.id)
        except ProbeRecord.DoesNotExist as exc:
            raise ProbeNotFoundError(f"Probe '{probe.id}' was not found.") from exc

        record.x = probe.position.x
        record.y = probe.position.y
        record.direction = probe.direction.value
        record.plateau_max_x = probe.plateau.max_x
        record.plateau_max_y = probe.plateau.max_y
        record.save(
            update_fields=(
                "x",
                "y",
                "direction",
                "plateau_max_x",
                "plateau_max_y",
                "updated_at",
            )
        )

    @staticmethod
    def _to_domain(record: ProbeRecord) -> Probe:
        return Probe(
            id=record.id,
            plateau=Plateau(max_x=record.plateau_max_x, max_y=record.plateau_max_y),
            direction=Direction(record.direction),
            position=Position(x=record.x, y=record.y),
        )
