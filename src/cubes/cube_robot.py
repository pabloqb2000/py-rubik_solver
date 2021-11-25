from cubes.util import *
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
    "cool_down": 0.1,
    "mode_pins": (14, 15, 18),
    "dir_step_pins": {
        "plate":   (16, 26),
        "holder":  (13, 19),
        "flipper": (20, 21),
    },
    "flip_speed": 0.25,
    "extra_plate_turn": 8,
    "extra_hold_turn": 0,
    "resolution": 32,
    "holder_degrees": 90,
    "holder_direction": "cw",
}

def inv(dir):
    return dir+'P' if dir[-1] != 'P' else dir[:-1]

def new_translation(dir, translate_dict):
    """
        Auxiliary function for the eliminate rotations function
        it returns the appropriate update for the translation dictionary
        given a rotation
    """
    new_translate_dict = translate_dict.copy()

    dir_new, n = translate_dict[dir], 3 if len(translate_dict[dir]) > 2 else 1
    d = dir_new[:2]

    if dir == "UU":
        new_translate_dict["RR"] = translate_dict["FF"]
        new_translate_dict["FF"] = inv(translate_dict["RR"])
    elif dir == "FF":
        new_translate_dict["UU"] = translate_dict["RR"]
        new_translate_dict["RR"] = inv(translate_dict["UU"])
    elif dir == "RR":
        new_translate_dict["UU"] = translate_dict["FF"]
        new_translate_dict["FF"] = inv(translate_dict["UU"])
    
    for _ in range(n):
        if d == "UU":
            new_translate_dict["F"] = translate_dict["R"]
            new_translate_dict["R"] = translate_dict["B"]
            new_translate_dict["B"] = translate_dict["L"]
            new_translate_dict["L"] = translate_dict["F"]
        elif d == "FF":
            new_translate_dict["U"] = translate_dict["L"]
            new_translate_dict["L"] = translate_dict["D"]
            new_translate_dict["D"] = translate_dict["R"]
            new_translate_dict["R"] = translate_dict["U"]
        elif d == "RR":
            new_translate_dict["U"] = translate_dict["F"]
            new_translate_dict["F"] = translate_dict["D"]
            new_translate_dict["D"] = translate_dict["B"]
            new_translate_dict["B"] = translate_dict["U"]
        for dn in direction_names:
            translate_dict[dn] = new_translate_dict[dn]
    return new_translate_dict


class CubeRobot:
    """
        Save cube configurations and setup pins for the movement of the motors
    """
    def __init__(self, config=default_config, speed=1):
        config["base_delay"] /= config["resolution"]
        config["delay"] = config["base_delay"] / speed
        config["spr"] *= config["resolution"]
        self.config = config
        self.dir = {motor: "cw" for motor in motors}
        self.holding = True

        self.pins_setup()
        self.face_orientations = {d: d for d in direction_names + ['UU', 'FF', 'RR']}

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
    def rotate_motor(self, motor, degrees, direction="cw", speed_factor=1):
        # Update for negative numbers
        if degrees < 0:
            direction = "ccw" if direction == "cw" else "cw"
            degrees = -degrees

        # Update direction if necessary
        dir_pin, step_pin = self.config["dir_step_pins"][motor]
        if self.dir[motor] != direction:
            self.dir[motor] = direction
            GPIO.output(dir_pin, direction_values[self.dir[motor]])

        # Rotate motor
        steps = self.config["spr"] * degrees // 360
        for _ in range(steps):
            GPIO.output(step_pin, GPIO.HIGH)
            sleep(self.config["delay"] / speed_factor)
            GPIO.output(step_pin, GPIO.LOW)
            sleep(self.config["delay"] / speed_factor)

        sleep(self.config["cool_down"])

    """
        Move the flipper motor for a full rotation
        And update the orientations dictionary
    """
    def flip(self):
        self.rotate_motor("flipper", 90, direction="ccw", speed_factor=self.config["flip_speed"])
        self.rotate_motor("flipper", 270, direction="ccw", speed_factor=4)
        
        for _ in range(3):
            self.face_orientations = new_translation("FF", self.face_orientations)

    """
        Move the holder motor to hold the upper pieces
    """
    def hold(self):
        if not self.holding:
            self.rotate_motor("holder", self.config["holder_degrees"] + self.config["extra_hold_turn"], self.config["holder_direction"], speed_factor=2)
            self.holding = True

    """
        Move the holder motor to release the upper pieces
    """
    def un_hold(self):
        if self.holding:
            self.rotate_motor("holder", self.config["holder_degrees"],
                              "cw" if self.config["holder_direction"] == "ccw" else "ccw", speed_factor=2)
            self.holding = False

    """
        Move the plate motor clockwise for n*90 degrees (in the fastest direction)
        And update the orientations dictionary
    """
    def move_plate(self, n):
        n %= 4
        if n == 0:
            return
        dir = "ccw" if n != 3 else "cw"
        angle = n*90 if n != 3 else 90
        if self.holding:
            angle += self.config["extra_plate_turn"]
        self.rotate_motor("plate", angle, dir, speed_factor=4)
        if self.holding and self.config["extra_plate_turn"] > 0:
            self.un_hold()
            self.rotate_motor("plate", -self.config["extra_plate_turn"], dir, speed_factor=4)
            self.hold()

        # Update the orientations dictionary
        if not self.holding:
            for _ in range((-n) % 4):
                self.face_orientations = new_translation("UU", self.face_orientations)

    """
        Apply a list of moves
        Each move should be a tuple like: ("U", -1)
    """
    def moves(self, moves):
        for dir, n in moves:
            self.move(dir, n)

    """
        Move one of the faces of the cube
        dir indicates the face that needs to be moved
        and n the number of 90 degree counterclock-wise rotations
        to apply to that face
    """
    def move(self, dir, n=1):
        # Format parameters
        if type(dir) == tuple:
            dir, n = dir
        n %= 4
        if n == 0:
            return
        dir = self.face_orientations[dir]

        # Unhold if necessary
        if dir != "D":
            self.un_hold()

        # Get the face to rotate down
        # Get Up face to the Left
        if dir == "U":
            self.flip()
            dir = "R"
        # Get all other faces to the left
        if dir == "F":
            self.move_plate(-1)
        elif dir == "L":
            self.move_plate(2)
        elif dir == "B":
            self.move_plate(1)
        # Get the Left face Down
        if dir != "D":
            self.flip()

        # Rotate the Down face
        self.hold()
        self.move_plate(n)

