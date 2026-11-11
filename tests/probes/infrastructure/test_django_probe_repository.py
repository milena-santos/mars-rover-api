"""Tests for the Django ORM probe repository adapter."""

from __future__ import annotations

from uuid import uuid4

import pytest

from probes.domain import (
    Command,
    Direction,
    Plateau,
    Position,
    Probe,
    ProbeNotFoundError,
)
from probes.infrastructure.models import ProbeCommandLogRecord, ProbeRecord
from probes.infrastructure.repositories import DjangoProbeRepository


@pytest.mark.django_db
def test_add_and_get_round_trip() -> None:
    repository = DjangoProbeRepository()
    plateau = repository.create_shared_plateau(Plateau(max_x=5, max_y=5))
    probe = Probe(
        plateau=plateau,
        direction=Direction.NORTH,
        position=Position(x=1, y=2),
    )

    repository.add(probe)

    loaded = repository.get(probe.id)

    assert loaded.id == probe.id
    assert loaded.position == Position(x=1, y=2)
    assert loaded.direction is Direction.NORTH
    assert loaded.plateau == Plateau(max_x=5, max_y=5)
    assert ProbeRecord.objects.count() == 1


@pytest.mark.django_db
def test_get_missing_probe_raises() -> None:
    repository = DjangoProbeRepository()

    with pytest.raises(ProbeNotFoundError):
        repository.get(uuid4())


@pytest.mark.django_db
def test_list_all_returns_probes_in_creation_order() -> None:
    repository = DjangoProbeRepository()
    plateau = repository.create_shared_plateau(Plateau(max_x=5, max_y=5))
    first = Probe(
        plateau=plateau,
        direction=Direction.EAST,
        position=Position(x=0, y=0),
    )
    second = Probe(
        plateau=plateau,
        direction=Direction.WEST,
        position=Position(x=1, y=0),
    )

    repository.add(first)
    repository.add(second)

    probes = repository.list_all()
    probe_ids = []
    for probe in probes:
        probe_ids.append(probe.id)

    assert probe_ids == [first.id, second.id]


@pytest.mark.django_db
def test_save_persists_executed_commands() -> None:
    repository = DjangoProbeRepository()
    plateau = repository.create_shared_plateau(Plateau(max_x=5, max_y=5))
    probe = Probe(plateau=plateau, direction=Direction.NORTH)
    repository.add(probe)

    probe.execute(Command.parse_sequence("MRM"), occupied=frozenset())
    repository.save(probe)
    repository.add_command_log(probe, commands="MRM")

    loaded = repository.get(probe.id)
    history = repository.list_command_logs(probe.id)

    assert loaded.position == Position(x=1, y=1)
    assert loaded.direction is Direction.EAST
    assert len(history) == 1
    assert history[0].commands == "MRM"
    assert ProbeCommandLogRecord.objects.count() == 1


@pytest.mark.django_db
def test_save_missing_probe_raises() -> None:
    repository = DjangoProbeRepository()
    probe = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.SOUTH)

    with pytest.raises(ProbeNotFoundError):
        repository.save(probe)


@pytest.mark.django_db
def test_occupied_positions_excludes_selected_probe() -> None:
    repository = DjangoProbeRepository()
    plateau = repository.create_shared_plateau(Plateau(max_x=5, max_y=5))
    first = Probe(
        plateau=plateau,
        direction=Direction.NORTH,
        position=Position(x=0, y=0),
    )
    second = Probe(
        plateau=plateau,
        direction=Direction.EAST,
        position=Position(x=2, y=2),
    )
    repository.add(first)
    repository.add(second)

    occupied = repository.occupied_positions(exclude_probe_id=first.id)

    assert occupied == frozenset({Position(x=2, y=2)})
