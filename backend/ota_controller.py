ota_status_store = {}


def start_ota(vin, campaign_id):
    ota_status_store[vin] = {
        "vin": vin,
        "campaign_id": campaign_id,
        "state": "STARTED",
        "progress": 0,
        "message": "OTA update started"
    }
    return ota_status_store[vin]


def pause_ota(vin):
    if vin not in ota_status_store:
        return {"error": "No OTA session found", "vin": vin}

    ota_status_store[vin]["state"] = "PAUSED"
    ota_status_store[vin]["message"] = "OTA update paused"
    return ota_status_store[vin]


def resume_ota(vin):
    if vin not in ota_status_store:
        return {"error": "No OTA session found", "vin": vin}

    ota_status_store[vin]["state"] = "RESUMED"
    ota_status_store[vin]["message"] = "OTA update resumed"
    return ota_status_store[vin]


def get_ota_status(vin):
    if vin not in ota_status_store:
        return {"error": "No OTA status found", "vin": vin}

    return ota_status_store[vin]