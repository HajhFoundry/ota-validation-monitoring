import json


def load_rules_config():
    with open("config/ota_rules_config.json", "r") as file:
        return json.load(file)


def evaluate_safety(vehicle, campaign):
    config = load_rules_config()
    failed_reasons = []

    if config["block_if_vehicle_driving"] and vehicle["driving"]:
        failed_reasons.append("Vehicle is driving")

    if failed_reasons:
        return False, failed_reasons

    return True, ["Safety checks passed"]


def check_notification_policy(vehicle):
    if vehicle["driving"]:
        return False, "Notification blocked while driving"

    return True, "Notification allowed"