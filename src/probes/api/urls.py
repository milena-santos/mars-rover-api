"""URL routes for the probes API."""

from django.urls import path

from probes.api.views import ProbeListCreateView, ProbeMoveView

urlpatterns = [
    path("probes/", ProbeListCreateView.as_view(), name="probe-list-create"),
    path(
        "probes/<uuid:probe_id>/commands/",
        ProbeMoveView.as_view(),
        name="probe-move",
    ),
]
