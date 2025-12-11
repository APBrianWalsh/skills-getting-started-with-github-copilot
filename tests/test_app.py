import pytest
from copy import deepcopy
from urllib.parse import quote
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    original_state = deepcopy(activities)
    try:
        yield
    finally:
        activities.clear()
        activities.update(deepcopy(original_state))


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities_returns_seed_data(client):
    response = client.get("/activities")
    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["description"]


def test_signup_adds_participant_to_activity(client):
    activity_name = "Gym Class"
    new_email = "new.student@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email},
    )

    assert response.status_code == 200
    assert new_email in activities[activity_name]["participants"]


def test_unregister_removes_participant_from_activity(client):
    activity_name = "Chess Club"
    existing_email = activities[activity_name]["participants"][0]

    response = client.delete(
        f"/activities/{activity_name}/participants/{quote(existing_email, safe='')}"
    )

    assert response.status_code == 200
    assert existing_email not in activities[activity_name]["participants"]
