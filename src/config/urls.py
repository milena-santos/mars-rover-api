"""Root URL configuration for the Mars Rover API."""

from django.urls import include, path

urlpatterns = [
    path("api/", include("probes.api.urls")),
]
