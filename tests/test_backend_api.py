from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_get_vehicles():
    response = client.get("/vehicles")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_campaigns():
    response = client.get("/campaigns")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_ota_start_status_flow():
    start_response = client.post(
        "/ota/start",
        json={
            "vin": "VIN001",
            "campaign_id": "FOTA_2026_001"
        }
    )

    assert start_response.status_code == 200
    assert start_response.json()["state"] == "STARTED"

    status_response = client.get("/ota/status/VIN001")

    assert status_response.status_code == 200
    assert status_response.json()["vin"] == "VIN001"


def test_ota_update_status():
    response = client.post(
        "/ota/update-status",
        json={
            "vin": "VIN001",
            "campaign_id": "FOTA_2026_001",
            "state": "SUCCESS",
            "progress": 100,
            "message": "OTA completed successfully"
        }
    )

    assert response.status_code == 200
    assert response.json()["state"] == "SUCCESS"
    assert response.json()["progress"] == 100