import json
from vehicle_client.campaign_manager import is_vehicle_targeted


def test_campaign_targeting_from_json():
    with open("test_data/campaign_test_data.json", "r") as file:
        test_cases = json.load(file)

    for case in test_cases:
        result, reason = is_vehicle_targeted(
            case["vehicle"],
            case["campaign"]
        )

        assert result is case["expected_result"], (
            f"{case['test_id']} failed. "
            f"Expected={case['expected_result']} Actual={result} Reason={reason}"
        )