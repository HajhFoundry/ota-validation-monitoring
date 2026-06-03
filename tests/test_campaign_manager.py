import pytest
from vehicle_client.campaign_manager import is_vehicle_targeted


@pytest.mark.parametrize(
    "vehicle, campaign, expected_result",
    [
        (
            {
                "vin": "VIN001",
                "model": "Explorer",
                "year": 2025,
                "region": "NA",
                "update_type": "FOTA"
            },
            {
                "campaign_id": "FOTA_2026_001",
                "target_model": "Explorer",
                "target_year": 2025,
                "target_region": "NA",
                "update_type": "FOTA"
            },
            True
        ),
        (
            {
                "vin": "VIN002",
                "model": "MustangMachE",
                "year": 2024,
                "region": "NA",
                "update_type": "AOTA"
            },
            {
                "campaign_id": "FOTA_2026_001",
                "target_model": "Explorer",
                "target_year": 2025,
                "target_region": "NA",
                "update_type": "FOTA"
            },
            False
        ),
        (
            {
                "vin": "VIN003",
                "model": "Explorer",
                "year": 2025,
                "region": "EU",
                "update_type": "FOTA"
            },
            {
                "campaign_id": "FOTA_2026_001",
                "target_model": "Explorer",
                "target_year": 2025,
                "target_region": "NA",
                "update_type": "FOTA"
            },
            False
        ),
    ]
)
def test_vehicle_campaign_targeting(vehicle, campaign, expected_result):
    result, reason = is_vehicle_targeted(vehicle, campaign)

    assert result is expected_result