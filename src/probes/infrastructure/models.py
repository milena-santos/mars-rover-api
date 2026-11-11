"""Django persistence models for probes."""

from __future__ import annotations

import uuid

from django.db import models

from probes.domain.direction import DIRECTION_CHOICES


class PlateauRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    max_x = models.PositiveIntegerField()
    max_y = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"Plateau {self.id} ({self.max_x}x{self.max_y})"


class ProbeRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    plateau = models.ForeignKey(
        PlateauRecord,
        on_delete=models.PROTECT,
        related_name="probes",
    )
    x = models.IntegerField()
    y = models.IntegerField()
    direction = models.CharField(
        max_length=5,
        choices=DIRECTION_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("plateau", "x", "y"),
                name="unique_probe_position_per_plateau",
            ),
        ]

    def __str__(self) -> str:
        return f"Probe {self.id} at ({self.x}, {self.y}) {self.direction}"


class ProbeCommandLogRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    probe = models.ForeignKey(
        ProbeRecord,
        on_delete=models.CASCADE,
        related_name="command_logs",
    )
    commands = models.TextField()
    x = models.IntegerField()
    y = models.IntegerField()
    direction = models.CharField(
        max_length=5,
        choices=DIRECTION_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"Log {self.id} for probe {self.probe_id}: {self.commands}"
