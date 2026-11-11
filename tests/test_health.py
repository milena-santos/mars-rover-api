"""Health endpoint contract."""

from __future__ import annotations

import pytest
from django.test import Client


@pytest.mark.django_db
def test_health_returns_ok_when_database_is_available(client: Client) -> None:
    response = client.get("/health/")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
