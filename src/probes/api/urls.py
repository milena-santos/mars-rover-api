"""URL routes for the probes API."""

from django.urls import path

from probes.api.views import (
    ProbeDetailView,
    ProbeHistoryView,
    ProbeListCreateView,
    ProbeMoveView,
)

urlpatterns = [
    path("probes/", ProbeListCreateView.as_view(), name="probe-list-create"),
    path(
        "probes/<uuid:probe_id>/",
        ProbeDetailView.as_view(),
        name="probe-detail",
    ),
    path(
        "probes/<uuid:probe_id>/history/",
        ProbeHistoryView.as_view(),
        name="probe-history",
    ),
    path(
        "probes/<uuid:probe_id>/commands/",
        ProbeMoveView.as_view(),
        name="probe-move",
    ),
]
