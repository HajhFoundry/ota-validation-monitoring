import pytest
from vehicle_client.safety_rules import evaluate_safety


@pytest.mark.parametrize(
    "vehicle, expected_result",
    [
        (
            {
                "vin": "VIN001",
                "driving": False
            },
            True
        ),
        (
            {
                "vin": "VIN002",
                "driving": False
            },
            True
        ),
        (
            {
                "vin": "VIN003",
                "driving": True
            },
            False
        ),
    ]
)
def test_vehicle_driving_safety_rule(vehicle, expected_result):
    campaign = {
        "campaign_id": "FOTA_2026_001"
    }

    result, reasons = evaluate_safety(vehicle, campaign)

    assert result is expected_result