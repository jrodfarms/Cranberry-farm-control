import random

class MockSensors:
    def __init__(self):
        self.state = {
            "soil_moisture": "Dry",
            "air_temp_c_A": 23.0,
            "air_temp_c_B": 22.4,
            "air_temp_c_C": 22.0,
            "soil_temp_c_1": 15.0,
            "soil_temp_c_2": 14.5,
            "soil_temp_c_3": 14.2,
            "psi": 35.0,
            "irrigation_water_level_ok": True,
            "flood_level_1_cm": 5.0,
            "flood_level_2_cm": 4.0,
            "drain_float_on": False,
        }

    def tick(self):
        # drift temps and psi
        for k in ["air_temp_c_A","air_temp_c_B","air_temp_c_C",
                  "soil_temp_c_1","soil_temp_c_2","soil_temp_c_3"]:
            self.state[k] += random.uniform(-0.2,0.2)
        self.state["psi"] += random.uniform(-0.5,0.5)
        self.state["psi"] = max(0.0, self.state["psi"])
        # random flip soil moisture
        if random.random() < 0.05:
            self.state["soil_moisture"] = "Wet" if self.state["soil_moisture"]=="Dry" else "Dry"
        # flood levels drift
        self.state["flood_level_1_cm"] = max(0.0, self.state["flood_level_1_cm"] + random.uniform(-0.5,0.5))
        self.state["flood_level_2_cm"] = max(0.0, self.state["flood_level_2_cm"] + random.uniform(-0.5,0.5))
        # float rare toggle
        if random.random() < 0.02:
            self.state["drain_float_on"] = not self.state["drain_float_on"]
