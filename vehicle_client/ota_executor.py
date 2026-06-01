import time
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from mqtt.mqtt_publisher import publish_ota_status

from checkpoint_manager import save_checkpoint, load_checkpoint, clear_checkpoint
from backend_notifier import notify_backend
from notification_manager import send_notification
from ota_state import OTAState


VIN = "VIN001"
CAMPAIGN = "FOTA_2026_001"

VEHICLE = {
    "vin": VIN,
    "driving": False,
    "enrolled_notifications": True
}

def publish_state(state, progress):
    publish_ota_status(
        VIN,
        {
            "vin": VIN,
            "campaign_id": CAMPAIGN,
            "state": state,
            "progress": progress
        }
    )

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
        publish_state(
            OTAState.PENDING.value,
            progress
        )
        time.sleep(1)

    if progress == 50 and not checkpoint:
        battery = 59

        if battery < 60:
            print("\nBattery dropped below threshold")

            save_checkpoint(
                VIN,
                CAMPAIGN,
                progress,
                OTAState.PAUSED_LOW_BATTERY.value
            )

            notify_backend(
                VIN,
                CAMPAIGN,
                OTAState.PAUSED_LOW_BATTERY.value
            )

            publish_state(
                OTAState.PAUSED_LOW_BATTERY.value,
                progress
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
    publish_state(
        OTAState.PENDING.value,
        progress
    )
    for step in [75, 100]:
        if step <= progress:
            continue

        progress = step
        print(f"Download Progress: {progress}%")
        publish_state(
            OTAState.DOWNLOADING.value,
            progress
        )
        time.sleep(1)

    publish_state(
        OTAState.VERIFYING.value,
        progress
    )
    publish_state(
        OTAState.INSTALLING.value,
        progress
    )
    publish_state(
        OTAState.REBOOTING.value,
        progress
    )
    publish_state(
        OTAState.SUCCESS.value,
        progress
    )
    time.sleep(1)

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