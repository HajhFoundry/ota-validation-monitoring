import json
from vehicle_client.cybersecurity_rules import evaluate_cybersecurity


def test_cybersecurity_rules_from_json():
    with open("test_data/cybersecurity_test_data.json", "r") as file:
        test_cases = json.load(file)

    for case in test_cases:
        vehicle = {
            "vin": case["vin"],
            "tls_enabled": case["tls_enabled"],
            "certificate_valid": case["certificate_valid"],
            "package_signature_valid": case["package_signature_valid"],
            "checksum_valid": case["checksum_valid"]
        }

        result, reasons = evaluate_cybersecurity(vehicle)

        assert result is case["expected_result"], f"{case['test_id']} failed: {reasons}"