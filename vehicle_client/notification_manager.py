def send_notification(vehicle, message):
    if vehicle["driving"]:
        print(f"[NOTIFICATION BLOCKED] {vehicle['vin']} vehicle is driving")
        return "BLOCKED_IN_VEHICLE"

    print(f"[IN-VEHICLE NOTIFICATION] {vehicle['vin']} - {message}")

    if vehicle["enrolled_notifications"]:
        print(f"[MOBILE/EMAIL NOTIFICATION] {vehicle['vin']} - {message}")
        return "SENT_IN_VEHICLE_AND_EXTERNAL"

    return "SENT_IN_VEHICLE_ONLY"