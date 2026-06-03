import pytest
from vehicle_client.cybersecurity_rules import evaluate_cybersecurity


@pytest.mark.parametrize(
    "vehicle, expected_result",
    [
        (
            {
                "vin": "VIN001",
                "tls_enabled": True,
                "certificate_valid": True,
                "package_signature_valid": True,
                "checksum_valid": True
            },
            True
        ),
        (
            {
                "vin": "VIN002",
                "tls_enabled": True,
                "certificate_valid": True,
                "package_signature_valid": False,
                "checksum_valid": True
            },
            False
        ),
        (
            {
                "vin": "VIN003",
                "tls_enabled": True,
                "certificate_valid": True,
                "package_signature_valid": True,
                "checksum_valid": False
            },
            False
        ),
        (
            {
                "vin": "VIN004",
                "tls_enabled": False,
                "certificate_valid": True,
                "package_signature_valid": True,
                "checksum_valid": True
            },
            False
        ),
    ]
)
def test_cybersecurity_rules(vehicle, expected_result):
    result, reasons = evaluate_cybersecurity(vehicle)

    assert result is expected_result