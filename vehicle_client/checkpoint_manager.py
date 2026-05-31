import json
import os


CHECKPOINT_FILE = "logs/checkpoints.json"


def save_checkpoint(vin, campaign_id, progress, state):

    checkpoint = {
        "vin": vin,
        "campaign_id": campaign_id,
        "progress": progress,
        "state": state
    }

    os.makedirs("logs", exist_ok=True)

    with open(CHECKPOINT_FILE, "w") as file:
        json.dump(checkpoint, file, indent=4)

    print(f"[CHECKPOINT SAVED] {progress}% - {state}")


def load_checkpoint():

    if not os.path.exists(CHECKPOINT_FILE):
        return None

    with open(CHECKPOINT_FILE, "r") as file:
        return json.load(file)

def clear_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        os.remove(CHECKPOINT_FILE)
        print("[CHECKPOINT CLEARED]")