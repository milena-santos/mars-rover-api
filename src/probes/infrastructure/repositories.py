"""Django ORM adapter for the ProbeRepository port."""

from __future__ import annotations

from uuid import UUID

from probes.domain.direction import Direction
from probes.domain.exceptions import ProbeNotFoundError
from probes.domain.history import CommandHistoryEntry
from probes.domain.plateau import Plateau
from probes.domain.position import Position
from probes.domain.probe import Probe
from probes.infrastructure.models import (
    PlateauRecord,
    ProbeCommandLogRecord,
    ProbeRecord,
)


class DjangoProbeRepository:
    def get_shared_plateau(self) -> Plateau | None:
        record = PlateauRecord.objects.order_by("created_at").first()
        if record is None:
            return None
        return Plateau(max_x=record.max_x, max_y=record.max_y)

    def create_shared_plateau(self, plateau: Plateau) -> Plateau:
        PlateauRecord.objects.create(max_x=plateau.max_x, max_y=plateau.max_y)
        return plateau

    def replace_shared_plateau(self, plateau: Plateau) -> Plateau:
        PlateauRecord.objects.all().delete()
        return self.create_shared_plateau(plateau)

    def occupied_positions(
        self, *, exclude_probe_id: UUID | None = None
    ) -> frozenset[Position]:
        queryset = ProbeRecord.objects.all()
        if exclude_probe_id is not None:
            queryset = queryset.exclude(pk=exclude_probe_id)

        positions: set[Position] = set()
        for record in queryset:
            positions.add(Position(x=record.x, y=record.y))
        return frozenset(positions)

    def find_id_at(self, position: Position) -> UUID | None:
        record = ProbeRecord.objects.filter(x=position.x, y=position.y).first()
        if record is None:
            return None
        return record.id

    def add(self, probe: Probe) -> None:
        plateau = PlateauRecord.objects.order_by("created_at").first()
        if plateau is None:
            raise ProbeNotFoundError("Shared plateau was not found.")

        ProbeRecord.objects.create(
            id=probe.id,
            plateau=plateau,
            x=probe.position.x,
            y=probe.position.y,
            direction=probe.direction.value,
        )

    def get(self, probe_id: UUID) -> Probe:
        try:
            record = ProbeRecord.objects.select_related("plateau").get(pk=probe_id)
        except ProbeRecord.DoesNotExist as exc:
            raise ProbeNotFoundError(f"Probe '{probe_id}' was not found.") from exc
        return self._to_domain(record)

    def list_all(self) -> list[Probe]:
        probes = []
        for record in ProbeRecord.objects.select_related("plateau").all():
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
        record.save(update_fields=("x", "y", "direction", "updated_at"))

    def delete_many(self, probe_ids: list[UUID]) -> None:
        if not probe_ids:
            return
        ProbeRecord.objects.filter(pk__in=probe_ids).delete()

    def add_command_log(self, probe: Probe, *, commands: str) -> CommandHistoryEntry:
        try:
            record = ProbeRecord.objects.get(pk=probe.id)
        except ProbeRecord.DoesNotExist as exc:
            raise ProbeNotFoundError(f"Probe '{probe.id}' was not found.") from exc

        log = ProbeCommandLogRecord.objects.create(
            probe=record,
            commands=commands,
            x=probe.position.x,
            y=probe.position.y,
            direction=probe.direction.value,
        )
        return CommandHistoryEntry(
            id=log.id,
            commands=log.commands,
            position=Position(x=log.x, y=log.y),
            direction=Direction(log.direction),
            created_at=log.created_at,
        )

    def list_command_logs(self, probe_id: UUID) -> list[CommandHistoryEntry]:
        if not ProbeRecord.objects.filter(pk=probe_id).exists():
            raise ProbeNotFoundError(f"Probe '{probe_id}' was not found.")

        entries: list[CommandHistoryEntry] = []
        logs = ProbeCommandLogRecord.objects.filter(probe_id=probe_id).order_by(
            "created_at"
        )
        for log in logs:
            entries.append(
                CommandHistoryEntry(
                    id=log.id,
                    commands=log.commands,
                    position=Position(x=log.x, y=log.y),
                    direction=Direction(log.direction),
                    created_at=log.created_at,
                )
            )
        return entries

    def clear_all(self) -> None:
        ProbeRecord.objects.all().delete()
        PlateauRecord.objects.all().delete()

    @staticmethod
    def _to_domain(record: ProbeRecord) -> Probe:
        return Probe(
            id=record.id,
            plateau=Plateau(
                max_x=record.plateau.max_x,
                max_y=record.plateau.max_y,
            ),
            direction=Direction(record.direction),
            position=Position(x=record.x, y=record.y),
        )
