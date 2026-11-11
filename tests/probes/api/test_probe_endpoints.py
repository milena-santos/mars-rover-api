"""HTTP contract tests for the probes API."""

from __future__ import annotations

from uuid import uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
def test_launch_probe_returns_origin_state(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/probes/",
        {"x": 5, "y": 5, "direction": "NORTH"},
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["x"] == 0
    assert body["y"] == 0
    assert body["direction"] == "NORTH"
    assert body["id"]


@pytest.mark.django_db
def test_move_probe_matches_challenge_example(api_client: APIClient) -> None:
    launch = api_client.post(
        "/api/probes/",
        {"x": 5, "y": 5, "direction": "NORTH"},
        format="json",
    )
    probe_id = launch.json()["id"]

    response = api_client.post(
        f"/api/probes/{probe_id}/commands/",
        {"commands": "MRM"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": probe_id,
        "x": 1,
        "y": 1,
        "direction": "EAST",
    }


@pytest.mark.django_db
def test_move_rejects_out_of_bounds_without_changing_state(
    api_client: APIClient,
) -> None:
    launch = api_client.post(
        "/api/probes/",
        {"x": 5, "y": 5, "direction": "WEST"},
        format="json",
    )
    probe_id = launch.json()["id"]

    response = api_client.post(
        f"/api/probes/{probe_id}/commands/",
        {"commands": "M"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()

    listing = api_client.get("/api/probes/")
    assert listing.json()["probes"] == [
        {
            "id": probe_id,
            "x": 0,
            "y": 0,
            "direction": "WEST",
        }
    ]


@pytest.mark.django_db
def test_move_rejects_invalid_commands(api_client: APIClient) -> None:
    launch = api_client.post(
        "/api/probes/",
        {"x": 5, "y": 5, "direction": "NORTH"},
        format="json",
    )
    probe_id = launch.json()["id"]

    response = api_client.post(
        f"/api/probes/{probe_id}/commands/",
        {"commands": "MX"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_move_unknown_probe_returns_not_found(api_client: APIClient) -> None:
    response = api_client.post(
        f"/api/probes/{uuid4()}/commands/",
        {"commands": "M"},
        format="json",
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_get_probe_returns_current_state(api_client: APIClient) -> None:
    launch = api_client.post(
        "/api/probes/",
        {"x": 5, "y": 5, "direction": "NORTH"},
        format="json",
    ).json()

    response = api_client.get(f"/api/probes/{launch['id']}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == launch


@pytest.mark.django_db
def test_get_unknown_probe_returns_not_found(api_client: APIClient) -> None:
    response = api_client.get(f"/api/probes/{uuid4()}/")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_list_probes_returns_all_states(api_client: APIClient) -> None:
    first = api_client.post(
        "/api/probes/",
        {"x": 5, "y": 5, "direction": "NORTH"},
        format="json",
    ).json()
    second = api_client.post(
        "/api/probes/",
        {"x": 3, "y": 3, "direction": "EAST"},
        format="json",
    ).json()

    response = api_client.get("/api/probes/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"probes": [first, second]}


@pytest.mark.django_db
def test_launch_rejects_invalid_direction(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/probes/",
        {"x": 5, "y": 5, "direction": "UP"},
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
