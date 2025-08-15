class PumpController:
    def __init__(self):
        self.state = {
            "irrigation_on": False,
            "flood1_on": False,
            "flood2_on": False,
            "drain_on": False
        }

    def set_irrigation(self, on: bool):
        self.state["irrigation_on"] = bool(on)
        # TODO: replace with actual GPIO relay control on the Pi

    def set_flood(self, idx: int, on: bool):
        key = "flood1_on" if idx == 1 else "flood2_on"
        self.state[key] = bool(on)

    def set_drain(self, on: bool):
        self.state["drain_on"] = bool(on)
