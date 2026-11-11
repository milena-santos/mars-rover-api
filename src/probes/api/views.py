"""HTTP views for probe launch, movement, and listing."""

from __future__ import annotations

from uuid import UUID

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from probes.api.serializers import (
    CommandHistoryEntrySerializer,
    LaunchProbeSerializer,
    MoveProbeSerializer,
    ProbeHistoryResponseSerializer,
    ProbeListResponseSerializer,
    ProbeStateSerializer,
)
from probes.application.services import ProbeService
from probes.domain.direction import Direction
from probes.infrastructure.repositories import DjangoProbeRepository


def build_probe_service() -> ProbeService:
    return ProbeService(repository=DjangoProbeRepository())


class ProbeListCreateView(APIView):
    @extend_schema(
        summary="List probes",
        responses={200: ProbeListResponseSerializer},
    )
    def get(self, request: Request) -> Response:
        probes = build_probe_service().list_probes()
        payload = []
        for probe in probes:
            payload.append(ProbeStateSerializer.from_probe(probe))
        return Response({"probes": payload})

    @extend_schema(
        summary="Launch probe",
        request=LaunchProbeSerializer,
        responses={201: ProbeStateSerializer},
    )
    def post(self, request: Request) -> Response:
        serializer = LaunchProbeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        probe = build_probe_service().launch(
            max_x=serializer.validated_data["x"],
            max_y=serializer.validated_data["y"],
            landing_x=serializer.validated_data["landing_x"],
            landing_y=serializer.validated_data["landing_y"],
            direction=Direction(serializer.validated_data["direction"]),
        )
        return Response(
            ProbeStateSerializer.from_probe(probe),
            status=status.HTTP_201_CREATED,
        )


class ProbeDetailView(APIView):
    @extend_schema(
        summary="Get probe",
        responses={200: ProbeStateSerializer},
    )
    def get(self, request: Request, probe_id: UUID) -> Response:
        probe = build_probe_service().get_probe(probe_id=probe_id)
        return Response(ProbeStateSerializer.from_probe(probe))


class ProbeHistoryView(APIView):
    @extend_schema(
        summary="Get probe command history",
        responses={200: ProbeHistoryResponseSerializer},
    )
    def get(self, request: Request, probe_id: UUID) -> Response:
        entries = build_probe_service().list_history(probe_id=probe_id)
        payload = []
        for entry in entries:
            payload.append(CommandHistoryEntrySerializer.from_entry(entry))
        return Response({"history": payload})


class ProbeMoveView(APIView):
    @extend_schema(
        summary="Move probe",
        request=MoveProbeSerializer,
        responses={200: ProbeStateSerializer},
    )
    def post(self, request: Request, probe_id: UUID) -> Response:
        serializer = MoveProbeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        probe = build_probe_service().move(
            probe_id=probe_id,
            commands=serializer.validated_data["commands"],
        )
        return Response(ProbeStateSerializer.from_probe(probe))
