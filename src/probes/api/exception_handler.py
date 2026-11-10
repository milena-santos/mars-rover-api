"""Map domain errors to HTTP responses."""

from __future__ import annotations

from typing import Any

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from probes.domain.exceptions import (
    InvalidCommandError,
    InvalidPlateauError,
    OutOfBoundsError,
    ProbeNotFoundError,
)

_DOMAIN_STATUS = {
    InvalidCommandError: status.HTTP_400_BAD_REQUEST,
    InvalidPlateauError: status.HTTP_400_BAD_REQUEST,
    OutOfBoundsError: status.HTTP_400_BAD_REQUEST,
    ProbeNotFoundError: status.HTTP_404_NOT_FOUND,
}


def domain_exception_handler(
    exc: Exception, context: dict[str, Any]
) -> Response | None:
    response = exception_handler(exc, context)
    if response is not None:
        return response

    for error_type, http_status in _DOMAIN_STATUS.items():
        if isinstance(exc, error_type):
            return Response({"detail": str(exc)}, status=http_status)
    return None
