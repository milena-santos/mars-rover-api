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
from probes.infrastructure.models import ProbeRecord
from probes.infrastructure.repositories import DjangoProbeRepository


@pytest.mark.django_db
def test_add_and_get_round_trip() -> None:
    repository = DjangoProbeRepository()
    probe = Probe(
        plateau=Plateau(max_x=5, max_y=5),
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
    first = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.EAST)
    second = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.WEST)

    repository.add(first)
    repository.add(second)

    probes = repository.list_all()

    assert [probe.id for probe in probes] == [first.id, second.id]


@pytest.mark.django_db
def test_save_persists_executed_commands() -> None:
    repository = DjangoProbeRepository()
    probe = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.NORTH)
    repository.add(probe)

    probe.execute(Command.parse_sequence("MRM"))
    repository.save(probe)

    loaded = repository.get(probe.id)

    assert loaded.position == Position(x=1, y=1)
    assert loaded.direction is Direction.EAST


@pytest.mark.django_db
def test_save_missing_probe_raises() -> None:
    repository = DjangoProbeRepository()
    probe = Probe(plateau=Plateau(max_x=5, max_y=5), direction=Direction.SOUTH)

    with pytest.raises(ProbeNotFoundError):
        repository.save(probe)
