from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_unknown_user_returns_404():
    response = client.get("/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_unknown_user_health_summary_returns_404():
    response = client.get("/health-summary/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_unknown_user_health_data_returns_404():
    response = client.get("/health-data/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_unknown_user_recommendations_returns_404():
    response = client.get("/recommendations/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_future_hydration_date_is_rejected():
    future_date = (
        date.today() + timedelta(days=1)
    ).isoformat()

    response = client.post(
        "/health-data",
        json={
            "user_id": 1,
            "date": future_date,
            "water_intake_ml": 2000,
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Hydration date cannot be in the future"
    )


def test_invalid_hydration_input_is_rejected():
    response = client.post(
        "/health-data",
        json={
            "user_id": 1,
            "date": date.today().isoformat(),
            "water_intake_ml": -500,
        },
    )

    assert response.status_code == 422


def test_existing_user_profile_can_be_loaded():
    response = client.get("/users/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert "name" in data
    assert "daily_water_target_ml" in data


def test_existing_user_summary_is_returned():
    response = client.get("/health-summary/1")

    assert response.status_code == 200

    data = response.json()

    assert data["user_id"] == 1
    assert "target_ml" in data
    assert "average_intake_ml" in data
    assert "trend" in data
    assert "data_quality" in data