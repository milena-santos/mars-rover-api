"""HTTP contract tests for the probes API."""

from __future__ import annotations

from uuid import uuid4

import pytest
from rest_framework import status
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


def launch_payload(
    *,
    x: int = 5,
    y: int = 5,
    direction: str = "NORTH",
) -> dict[str, object]:
    return {
        "x": x,
        "y": y,
        "direction": direction,
    }


@pytest.mark.django_db
def test_launch_probe_starts_at_origin(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/probes/",
        launch_payload(direction="NORTH"),
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
        launch_payload(),
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
        launch_payload(direction="WEST"),
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
def test_move_collision_destroys_both_probes(api_client: APIClient) -> None:
    first = api_client.post(
        "/api/probes/",
        launch_payload(direction="NORTH"),
        format="json",
    ).json()
    api_client.post(
        f"/api/probes/{first['id']}/commands/",
        {"commands": "M"},
        format="json",
    )
    second = api_client.post(
        "/api/probes/",
        launch_payload(direction="NORTH"),
        format="json",
    ).json()

    response = api_client.post(
        f"/api/probes/{second['id']}/commands/",
        {"commands": "M"},
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["event"] == "collision"
    assert body["x"] == 0
    assert body["y"] == 1
    assert set(body["destroyed"]) == {first["id"], second["id"]}

    listing = api_client.get("/api/probes/")
    assert listing.json() == {
        "probes": [],
        "plateau": {"max_x": 5, "max_y": 5},
    }
    assert api_client.get(f"/api/probes/{first['id']}/").status_code == (
        status.HTTP_404_NOT_FOUND
    )
    assert api_client.get(f"/api/probes/{second['id']}/").status_code == (
        status.HTTP_404_NOT_FOUND
    )


@pytest.mark.django_db
def test_launch_collision_destroys_both_probes(api_client: APIClient) -> None:
    first = api_client.post(
        "/api/probes/",
        launch_payload(direction="NORTH"),
        format="json",
    ).json()

    response = api_client.post(
        "/api/probes/",
        launch_payload(direction="EAST"),
        format="json",
    )

    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["event"] == "collision"
    assert body["x"] == 0
    assert body["y"] == 0
    assert first["id"] in body["destroyed"]
    assert len(body["destroyed"]) == 2

    listing = api_client.get("/api/probes/")
    assert listing.json() == {
        "probes": [],
        "plateau": {"max_x": 5, "max_y": 5},
    }
    assert api_client.get(f"/api/probes/{first['id']}/").status_code == (
        status.HTTP_404_NOT_FOUND
    )


@pytest.mark.django_db
def test_launch_rejects_mismatched_shared_plateau_while_probes_exist(
    api_client: APIClient,
) -> None:
    api_client.post(
        "/api/probes/",
        launch_payload(x=5, y=5),
        format="json",
    )

    response = api_client.post(
        "/api/probes/",
        launch_payload(x=3, y=3),
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_launch_allows_new_plateau_when_mission_is_empty(
    api_client: APIClient,
) -> None:
    first = api_client.post(
        "/api/probes/",
        launch_payload(x=5, y=5, direction="NORTH"),
        format="json",
    ).json()
    api_client.post(
        "/api/probes/",
        launch_payload(x=5, y=5, direction="EAST"),
        format="json",
    )
    listing = api_client.get("/api/probes/")
    assert listing.json() == {
        "probes": [],
        "plateau": {"max_x": 5, "max_y": 5},
    }
    assert api_client.get(f"/api/probes/{first['id']}/").status_code == (
        status.HTTP_404_NOT_FOUND
    )

    relaunch = api_client.post(
        "/api/probes/",
        launch_payload(x=3, y=3, direction="SOUTH"),
        format="json",
    )

    assert relaunch.status_code == status.HTTP_201_CREATED
    assert relaunch.json()["direction"] == "SOUTH"
    assert relaunch.json()["x"] == 0
    assert relaunch.json()["y"] == 0


@pytest.mark.django_db
def test_move_rejects_invalid_commands(api_client: APIClient) -> None:
    launch = api_client.post(
        "/api/probes/",
        launch_payload(),
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
        launch_payload(),
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
        launch_payload(direction="NORTH"),
        format="json",
    ).json()
    moved_first = api_client.post(
        f"/api/probes/{first['id']}/commands/",
        {"commands": "M"},
        format="json",
    ).json()
    second = api_client.post(
        "/api/probes/",
        launch_payload(direction="EAST"),
        format="json",
    ).json()

    response = api_client.get("/api/probes/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "probes": [moved_first, second],
        "plateau": {"max_x": 5, "max_y": 5},
    }


@pytest.mark.django_db
def test_history_returns_successful_command_sequences(
    api_client: APIClient,
) -> None:
    launch = api_client.post(
        "/api/probes/",
        launch_payload(),
        format="json",
    ).json()
    probe_id = launch["id"]

    api_client.post(
        f"/api/probes/{probe_id}/commands/",
        {"commands": "MRM"},
        format="json",
    )
    api_client.post(
        f"/api/probes/{probe_id}/commands/",
        {"commands": "M"},
        format="json",
    )

    response = api_client.get(f"/api/probes/{probe_id}/history/")

    assert response.status_code == status.HTTP_200_OK
    history = response.json()["history"]
    assert len(history) == 2
    assert history[0]["commands"] == "MRM"
    assert history[0]["x"] == 1
    assert history[0]["y"] == 1
    assert history[0]["direction"] == "EAST"
    assert history[1]["commands"] == "M"
    assert history[1]["x"] == 2
    assert history[1]["y"] == 1
    assert history[1]["direction"] == "EAST"
    assert "created_at" in history[0]
    assert "id" in history[0]


@pytest.mark.django_db
def test_failed_move_does_not_create_history_entry(api_client: APIClient) -> None:
    launch = api_client.post(
        "/api/probes/",
        launch_payload(direction="WEST"),
        format="json",
    ).json()
    probe_id = launch["id"]

    api_client.post(
        f"/api/probes/{probe_id}/commands/",
        {"commands": "M"},
        format="json",
    )

    response = api_client.get(f"/api/probes/{probe_id}/history/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"history": []}


@pytest.mark.django_db
def test_launch_rejects_invalid_direction(api_client: APIClient) -> None:
    response = api_client.post(
        "/api/probes/",
        launch_payload(direction="UP"),
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_clear_all_removes_probes_and_allows_new_mission(
    api_client: APIClient,
) -> None:
    first = api_client.post(
        "/api/probes/",
        launch_payload(direction="NORTH"),
        format="json",
    ).json()
    api_client.post(
        f"/api/probes/{first['id']}/commands/",
        {"commands": "M"},
        format="json",
    )
    api_client.post(
        "/api/probes/",
        launch_payload(direction="EAST"),
        format="json",
    )

    cleared = api_client.delete("/api/probes/")
    assert cleared.status_code == status.HTTP_204_NO_CONTENT

    listing = api_client.get("/api/probes/")
    assert listing.json() == {"probes": [], "plateau": None}

    relaunch = api_client.post(
        "/api/probes/",
        launch_payload(x=3, y=3, direction="SOUTH"),
        format="json",
    )
    assert relaunch.status_code == status.HTTP_201_CREATED
    assert relaunch.json()["x"] == 0
    assert relaunch.json()["y"] == 0
    assert relaunch.json()["direction"] == "SOUTH"
