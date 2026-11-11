"""Process health endpoint used by containers and load balancers."""

from __future__ import annotations

from django.db import connection
from django.http import HttpRequest, JsonResponse


def health(_request: HttpRequest) -> JsonResponse:
    try:
        connection.ensure_connection()
    except Exception:
        return JsonResponse({"status": "error"}, status=503)

    return JsonResponse({"status": "ok"})
