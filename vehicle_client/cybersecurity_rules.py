import json


def load_rules_config():
    with open("config/ota_rules_config.json", "r") as file:
        return json.load(file)


def evaluate_cybersecurity(vehicle):
    config = load_rules_config()
    failed_reasons = []

    if config["require_tls"] and not vehicle["tls_enabled"]:
        failed_reasons.append("TLS not enabled")

    if config["require_valid_certificate"] and not vehicle["certificate_valid"]:
        failed_reasons.append("Certificate invalid")

    if config["require_valid_signature"] and not vehicle["package_signature_valid"]:
        failed_reasons.append("Package signature invalid")

    if config["require_valid_checksum"] and not vehicle["checksum_valid"]:
        failed_reasons.append("Checksum validation failed")

    if failed_reasons:
        return False, failed_reasons

    return True, ["Cybersecurity checks passed"]