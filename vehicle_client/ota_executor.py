import time

from checkpoint_manager import save_checkpoint
from backend_notifier import notify_backend


VIN = "VIN001"
CAMPAIGN = "FOTA_2026_001"


def execute_ota():

    print("\n=== OTA EXECUTION START ===\n")

    progress = 0

    for step in [25, 50]:

        progress = step

        print(f"Download Progress: {progress}%")

        time.sleep(1)

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

        print("\nWaiting for battery recovery...\n")

        time.sleep(2)

        battery = 65

        print(f"Battery recovered: {battery}%")

        print("Resuming OTA...\n")

    for step in [75, 100]:

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


if __name__ == "__main__":
    execute_ota()