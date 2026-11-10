"""Django persistence models for probes."""

from __future__ import annotations

import uuid

from django.db import models

from probes.domain.direction import DIRECTION_CHOICES


class ProbeRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    x = models.IntegerField()
    y = models.IntegerField()
    direction = models.CharField(
        max_length=5,
        choices=DIRECTION_CHOICES,
    )
    plateau_max_x = models.PositiveIntegerField()
    plateau_max_y = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"Probe {self.id} at ({self.x}, {self.y}) {self.direction}"
