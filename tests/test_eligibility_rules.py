import json


def is_vehicle_eligible(battery, ignition, driving):
    if battery < 60:
        return False
    if ignition:
        return False
    if driving:
        return False
    return True


def test_eligibility_rules_from_json():
    with open("test_data/eligibility_test_data.json", "r") as file:
        test_cases = json.load(file)

    for case in test_cases:
        result = is_vehicle_eligible(
            case["battery"],
            case["ignition"],
            case["driving"]
        )

        assert result is case["expected_result"], f"{case['test_id']} failed"