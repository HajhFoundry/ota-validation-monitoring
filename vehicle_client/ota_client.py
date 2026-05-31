from enum import Enum
import time


class OTAState(Enum):
    IDLE = "IDLE"
    CHECKING_FOR_UPDATE = "CHECKING_FOR_UPDATE"
    UPDATE_AVAILABLE = "UPDATE_AVAILABLE"
    DOWNLOADING = "DOWNLOADING"
    VERIFYING = "VERIFYING"
    INSTALLING = "INSTALLING"
    REBOOTING = "REBOOTING"
    SUCCESS = "SUCCESS"


class OTAClient:

    def __init__(self, vin):
        self.vin = vin
        self.state = OTAState.IDLE

    def transition(self, new_state):
        self.state = new_state
        print(f"[{self.vin}] -> {self.state.value}")

    def run_update(self):

        self.transition(OTAState.CHECKING_FOR_UPDATE)
        time.sleep(1)

        self.transition(OTAState.UPDATE_AVAILABLE)
        time.sleep(1)

        self.transition(OTAState.DOWNLOADING)
        time.sleep(1)

        self.transition(OTAState.VERIFYING)
        time.sleep(1)

        self.transition(OTAState.INSTALLING)
        time.sleep(1)

        self.transition(OTAState.REBOOTING)
        time.sleep(1)

        self.transition(OTAState.SUCCESS)


if __name__ == "__main__":
    vehicle = OTAClient("VIN123456")
    vehicle.run_update()