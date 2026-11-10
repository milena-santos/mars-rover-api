"""DRF serializers for probe HTTP contracts."""

from __future__ import annotations

from typing import Any

from rest_framework import serializers

from probes.domain.direction import Direction
from probes.domain.probe import Probe


class LaunchProbeSerializer(serializers.Serializer[dict[str, Any]]):
    x = serializers.IntegerField(min_value=0)
    y = serializers.IntegerField(min_value=0)
    direction = serializers.ChoiceField(choices=[item.value for item in Direction])


class MoveProbeSerializer(serializers.Serializer[dict[str, Any]]):
    commands = serializers.CharField(allow_blank=False, trim_whitespace=False)


class ProbeStateSerializer(serializers.Serializer[dict[str, Any]]):
    id = serializers.UUIDField()
    x = serializers.IntegerField()
    y = serializers.IntegerField()
    direction = serializers.ChoiceField(choices=[item.value for item in Direction])

    @classmethod
    def from_probe(cls, probe: Probe) -> dict[str, object]:
        return {
            "id": probe.id,
            "x": probe.position.x,
            "y": probe.position.y,
            "direction": probe.direction.value,
        }
