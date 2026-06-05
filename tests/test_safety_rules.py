import json
from vehicle_client.safety_rules import evaluate_safety


def load_test_data():
    with open("test_data/safety_test_data.json", "r") as file:
        return json.load(file)


def test_safety_rules_from_json():
    test_cases = load_test_data()

    for case in test_cases:
        vehicle = {
            "vin": case["vin"],
            "driving": case["driving"]
        }

        campaign = {
            "campaign_id": "FOTA_2026_001"
        }

        result, reasons = evaluate_safety(vehicle, campaign)

        assert result is case["expected_result"], (
            f"{case['test_id']} failed. "
            f"VIN={case['vin']} "
            f"Expected={case['expected_result']} "
            f"Actual={result} "
            f"Reasons={reasons}"
        )