import json
from fastapi.testclient import TestClient
from backend.main import app


client = TestClient(app)


def test_backend_api_from_json():
    with open("test_data/backend_api_test_data.json", "r") as file:
        test_cases = json.load(file)

    for case in test_cases:
        if case["method"] == "GET":
            response = client.get(case["endpoint"])
        elif case["method"] == "POST":
            response = client.post(
                case["endpoint"],
                json=case.get("payload", {})
            )
        else:
            raise ValueError(f"Unsupported method: {case['method']}")

        assert response.status_code == case["expected_status"], (
            f"{case['test_id']} failed. "
            f"Expected status={case['expected_status']} "
            f"Actual={response.status_code}"
        )

        if "expected_state" in case:
            assert response.json()["state"] == case["expected_state"], (
                f"{case['test_id']} failed. "
                f"Expected state={case['expected_state']} "
                f"Actual={response.json().get('state')}"
            )