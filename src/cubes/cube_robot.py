import RPi.GPIO as GPIO
from time import sleep

resolution_values = {1:  (0, 0, 0),
                     2:  (1, 0, 0),
                     4:  (0, 1, 0),
                     8:  (1, 1, 0),
                     16: (0, 0, 1),
                     32: (1, 0, 1)}
motors = ["plate", "holder", "flipper"]
direction_values = {
    "cw": 1,
    "ccw": 0,
}

default_config = {
    "spr": 200,
    "base_delay": 0.0208 / 8,
    "cool_down": 0.2,
    "mode_pins": (14, 15, 18),
    "dir_step_pins": {
        # FILL THIS PROPERLY
        "plate":   (20, 21),
        "holder":  (16, 26),
        "flipper": (19, 12),
    },
    "resolution": 32,
    # FILL THIS PROPERLY
    "holder_degrees": 90,
    "holder_direction": "cw",
}


class CubeRobot:
    """
        Save cube configurations and setup pins for the movement of the motors
    """
    def __init__(self, config=default_config):
        config["base_delay"] /= config["resolution"]
        config["spr"] *= config["resolution"]
        self.config = config
        self.dir = {motor: "cw" for motor in motors}
        self.holding = False

        self.pins_setup()

    """
        Setup the pins that are going to be used
    """
    def pins_setup(self):
        config = self.config

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(config["mode_pins"], GPIO.OUT)
        GPIO.output(config["mode_pins"], resolution_values[config["resolution"]])
        for motor in motors:
            dir_pin, step_pin = config["dir_step_pins"][motor]
            GPIO.setup(dir_pin, GPIO.OUT)
            GPIO.setup(step_pin, GPIO.OUT)
            GPIO.output(dir_pin, direction_values[self.dir[motor]])

    """
        Rotate the given motor a certain number of degrees (0 - 360) in the given direction
    """
    def rotate_motor(self, motor, degrees, direction="cw"):
        # Update direction if necessary
        dir_pin, step_pin = self.config["dir_step_pins"][motor]
        if self.dir[motor] != direction:
            self.dir[motor] = direction
            GPIO.output(dir_pin, direction_values[self.dir[motor]])

        # Rotate motor
        steps = self.config["spw"] * degrees // 360
        for _ in range(steps):
            GPIO.output(step_pin, GPIO.HIGH)
            sleep(self.config["delay"])
            GPIO.output(step_pin, GPIO.LOW)
            sleep(self.config["delay"])

        sleep(self.config["cool_down"])

    """
        Move the flipper motor for a full rotation
    """
    def flip(self):
        self.rotate_motor("flipper", 360)

    """
        Move the holder motor to hold the upper pieces
    """
    def hold(self):
        if not self.hold:
            self.rotate_motor("holder", self.config["holder_degrees"], self.config["holder_direction"])
            self.holding = True

    """
        Move the holder motor to release the upper pieces
    """
    def un_hold(self):
        if self.hold:
            self.rotate_motor("holder", self.config["holder_degrees"],
                              "cw" if self.config["holder_direction"] == "ccw" else "ccw")
            self.holding = False

    """
        Move the plate motor clockwise for n*90 degrees (in the fastest direction)
    """
    def move_plate(self, n):
        n %= 4
        if n == 0:
            return
        dir = "cw" if n != 3 else "ccw"
        self.rotate_motor("plate", n*90 if n != 3 else 90, dir)
