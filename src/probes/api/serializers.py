"""DRF serializers for probe HTTP contracts."""

from __future__ import annotations

from typing import Any

from rest_framework import serializers

from probes.domain.direction import DIRECTION_VALUES
from probes.domain.history import CommandHistoryEntry
from probes.domain.plateau import MAX_PLATEAU_DIMENSION, Plateau
from probes.domain.probe import Probe


class LaunchProbeSerializer(serializers.Serializer[dict[str, Any]]):
    x = serializers.IntegerField(min_value=0, max_value=MAX_PLATEAU_DIMENSION)
    y = serializers.IntegerField(min_value=0, max_value=MAX_PLATEAU_DIMENSION)
    direction = serializers.ChoiceField(choices=DIRECTION_VALUES)


class MoveProbeSerializer(serializers.Serializer[dict[str, Any]]):
    commands = serializers.CharField(allow_blank=False, trim_whitespace=False)


class ProbeStateSerializer(serializers.Serializer[dict[str, Any]]):
    id = serializers.UUIDField()
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    direction = serializers.ChoiceField(choices=DIRECTION_VALUES)

    @classmethod
    def from_probe(cls, probe: Probe) -> dict[str, object]:
        return {
            "id": probe.id,
            "x": probe.position.x,
            "y": probe.position.y,
            "direction": probe.direction.value,
        }


class PlateauStateSerializer(serializers.Serializer[dict[str, Any]]):
    max_x = serializers.IntegerField()
    max_y = serializers.IntegerField()

    @classmethod
    def from_plateau(cls, plateau: Plateau) -> dict[str, int]:
        return {
            "max_x": plateau.max_x,
            "max_y": plateau.max_y,
        }


class ProbeListResponseSerializer(serializers.Serializer[dict[str, Any]]):
    probes = ProbeStateSerializer(many=True)
    plateau = PlateauStateSerializer(allow_null=True)


class CommandHistoryEntrySerializer(serializers.Serializer[dict[str, Any]]):
    id = serializers.UUIDField()
    commands = serializers.CharField()
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    direction = serializers.ChoiceField(choices=DIRECTION_VALUES)
    created_at = serializers.DateTimeField()

    @classmethod
    def from_entry(cls, entry: CommandHistoryEntry) -> dict[str, object]:
        return {
            "id": entry.id,
            "commands": entry.commands,
            "x": entry.position.x,
            "y": entry.position.y,
            "direction": entry.direction.value,
            "created_at": entry.created_at,
        }


class ProbeHistoryResponseSerializer(serializers.Serializer[dict[str, Any]]):
    history = CommandHistoryEntrySerializer(many=True)


class CollisionResponseSerializer(serializers.Serializer[dict[str, Any]]):
    event = serializers.CharField()
    detail = serializers.CharField()
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    destroyed = serializers.ListField(child=serializers.UUIDField())
