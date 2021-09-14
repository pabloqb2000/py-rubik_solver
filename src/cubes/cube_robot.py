from cubes.cube import *
import RPi.GPIO as GPIO
from time import sleep

resolution_values = {1:  (0, 0, 0),
                     2:  (1, 0, 0),
                     4:  (0, 1, 0),
                     8:  (1, 1, 0),
                     16: (0, 0, 1),
                     32: (1, 0, 1)}

default_config = {
    "spr": 200,
    "base_delay": 0.0208,
    "speed": 8,
    "cool_down": 0.2,
    "mode_pins": (14, 15, 18),
    "dir_step_pins": {
        # FILL THIS PROPERLY
        "plate":   (20, 21),
        "holder":  (16, 26),
        "flipper": (19, 12),
    },
    "resolution": 32,
}


class CubeRobot(Cube):
    def __init__(self, config=default_config):
        config["base_delay"] /= config["resolution"]
        config["spr"] *= config["resolution"]

        self.pins_setup()

    def pins_setup(self):
        pass