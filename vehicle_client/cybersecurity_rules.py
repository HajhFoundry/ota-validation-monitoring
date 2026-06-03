def check_tls(vehicle):
    if not vehicle["tls_enabled"]:
        return False, "TLS not enabled"

    return True, "TLS valid"


def check_certificate(vehicle):
    if not vehicle["certificate_valid"]:
        return False, "Certificate invalid"

    return True, "Certificate valid"


def check_signature(vehicle):
    if not vehicle["package_signature_valid"]:
        return False, "Package signature invalid"

    return True, "Signature valid"


def check_checksum(vehicle):
    if not vehicle["checksum_valid"]:
        return False, "Checksum validation failed"

    return True, "Checksum valid"


def evaluate_cybersecurity(vehicle):
    rules = [
        check_tls,
        check_certificate,
        check_signature,
        check_checksum
    ]

    failed_reasons = []

    for rule in rules:
        passed, reason = rule(vehicle)

        if not passed:
            failed_reasons.append(reason)

    if failed_reasons:
        return False, failed_reasons

    return True, ["Cybersecurity checks passed"]