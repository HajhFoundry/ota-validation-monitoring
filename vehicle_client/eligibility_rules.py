def check_battery(vehicle, campaign):
    if vehicle["battery"] < campaign["minimum_battery"]:
        return False, f"Battery too low: {vehicle['battery']}%"

    return True, "Battery OK"


def check_wifi(vehicle, campaign):
    if campaign["wifi_required"] and not vehicle["wifi_connected"]:
        return False, "WiFi required but not connected"

    return True, "WiFi OK"


def check_ignition(vehicle, campaign):
    if campaign["ignition_required_off"] and vehicle["ignition"]:
        return False, "Ignition must be OFF"

    return True, "Ignition OK"


def check_parked(vehicle, campaign):
    if campaign["vehicle_must_be_parked"] and vehicle["driving"]:
        return False, "Vehicle must be parked"

    return True, "Vehicle parked OK"


def evaluate_eligibility(vehicle, campaign):
    rules = [
        check_battery,
        check_wifi,
        check_ignition,
        check_parked
    ]

    failed_reasons = []

    for rule in rules:
        passed, reason = rule(vehicle, campaign)

        if not passed:
            failed_reasons.append(reason)

    if failed_reasons:
        return False, failed_reasons

    return True, ["Eligible"]