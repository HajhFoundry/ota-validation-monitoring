def check_driver_distraction(vehicle, campaign):

    if vehicle["driving"]:
        return False, "Vehicle currently driving"

    return True, "Driving check passed"


def check_notification_policy(vehicle):

    if vehicle["driving"]:
        return False, "Notification blocked while driving"

    return True, "Notification allowed"


def evaluate_safety(vehicle, campaign):

    failed_reasons = []

    rules = [
        check_driver_distraction
    ]

    for rule in rules:

        passed, reason = rule(vehicle, campaign)

        if not passed:
            failed_reasons.append(reason)

    if failed_reasons:
        return False, failed_reasons

    return True, ["Safety checks passed"]