import time

from checkpoint_manager import save_checkpoint, load_checkpoint, clear_checkpoint
from backend_notifier import notify_backend
from notification_manager import send_notification

VIN = "VIN001"
CAMPAIGN = "FOTA_2026_001"

VEHICLE = {
    "vin": VIN,
    "driving": False,
    "enrolled_notifications": True
}



def execute_ota():
    print("\n=== OTA EXECUTION START ===\n")
    send_notification(
    VEHICLE,
    "OTA update is available and ready to start."
    )
    checkpoint = load_checkpoint()

    if checkpoint:
        progress = checkpoint["progress"]
        print(
            f"[CHECKPOINT FOUND] "
            f"VIN={checkpoint['vin']} "
            f"Campaign={checkpoint['campaign_id']} "
            f"Progress={progress}% "
            f"State={checkpoint['state']}"
        )
        print("\nResuming from saved checkpoint...\n")
    else:
        progress = 0

    for step in [25, 50]:
        if step <= progress:
            continue

        progress = step
        print(f"Download Progress: {progress}%")
        time.sleep(1)

    if progress == 50 and not checkpoint:
        battery = 59

        if battery < 60:
            print("\nBattery dropped below threshold")

            save_checkpoint(
                VIN,
                CAMPAIGN,
                progress,
                "PAUSED_LOW_BATTERY"
            )

            notify_backend(
                VIN,
                CAMPAIGN,
                "PAUSED_LOW_BATTERY"
            )

            print("\nOTA paused. Run again after battery recovery.\n")

            send_notification(
                VEHICLE,
                "OTA update paused due to low battery. It will resume when conditions improve."
            )
            return

    battery = 65
    print(f"Battery OK: {battery}%")
    print("Continuing OTA...\n")

    for step in [75, 100]:
        if step <= progress:
            continue

        progress = step
        print(f"Download Progress: {progress}%")
        time.sleep(1)

    print("\nVERIFYING PACKAGE")
    time.sleep(1)

    print("INSTALLING")
    time.sleep(1)

    print("REBOOTING")
    time.sleep(1)

    print("SUCCESS")

    notify_backend(
        VIN,
        CAMPAIGN,
        "SUCCESS"
    )

    send_notification(
        VEHICLE,
        "OTA update completed successfully."
    )

    clear_checkpoint()


if __name__ == "__main__":
    execute_ota()