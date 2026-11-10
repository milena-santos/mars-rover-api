"""HTTP views for probe launch, movement, and listing."""

from __future__ import annotations

from uuid import UUID

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from probes.api.serializers import (
    LaunchProbeSerializer,
    MoveProbeSerializer,
    ProbeStateSerializer,
)
from probes.application.services import ProbeService
from probes.domain.direction import Direction
from probes.infrastructure.repositories import DjangoProbeRepository


def build_probe_service() -> ProbeService:
    return ProbeService(repository=DjangoProbeRepository())


class ProbeListCreateView(APIView):
    def get(self, request: Request) -> Response:
        probes = build_probe_service().list_probes()
        return Response(
            {"probes": [ProbeStateSerializer.from_probe(probe) for probe in probes]}
        )

    def post(self, request: Request) -> Response:
        serializer = LaunchProbeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        probe = build_probe_service().launch(
            max_x=serializer.validated_data["x"],
            max_y=serializer.validated_data["y"],
            direction=Direction(serializer.validated_data["direction"]),
        )
        return Response(
            ProbeStateSerializer.from_probe(probe),
            status=status.HTTP_201_CREATED,
        )


class ProbeMoveView(APIView):
    def post(self, request: Request, probe_id: UUID) -> Response:
        serializer = MoveProbeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        probe = build_probe_service().move(
            probe_id=probe_id,
            commands=serializer.validated_data["commands"],
        )
        return Response(ProbeStateSerializer.from_probe(probe))
