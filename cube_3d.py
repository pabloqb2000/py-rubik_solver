from vpython import *
from cube import *
from util import *
from configs import *
from time import time
import numpy as np


def smooth_step(x):
    return 0.5 - np.cos(x * pi) / 2


class Cube3D(Cube):
    """
        Initialize the cube structure
        Shuffle and copy the cube if necessary
        Initialize cubes for the 3D representation
    """
    def __init__(self, cube_dict=solved_cube_dict, shuffle=False, n_shuffles=200, record=False, do_copy=False,
                 fps=fps_def, move_time=move_time_def, wait_time=wait_time_def):
        super().__init__(cube_dict, shuffle, n_shuffles, record, do_copy)

        # Initialize boxes
        self.base_box_list = []
        self.box_dict, self.base_box_dict = self.init_graphics_cube()
        # New cube to store and rotate the box objects
        self.box_cube = Cube(self.box_dict, shuffle=False, do_copy=False)

        # Visual parameters
        self.fps = fps
        self.move_time = move_time
        self.wait_time = wait_time

    """
        Create all the boxes necessary to represent the cube
    """
    def init_graphics_cube(self):
        cube_dict = self.cube_dict

        box_dict = {}
        base_box_dict = {dir_name: [] for dir_name in direction_names}

        # For each face
        for face_name, dir in direction_dict.items():
            face_dict = {}

            # For each piece of the face
            for box_name in cube_dict[face_name]:
                box_face_list = []

                # Compute the offset of the piece
                v = dir
                if box_name != face_name:
                    for c in box_name:
                        v = v + direction_dict[c]

                # For each sticker in the piece
                for i, box_face_type in enumerate(cube_dict[face_name][box_name]):
                    # Get the name of the sticker
                    if i == 0:
                        box_face_name = face_name
                    else:
                        box_face_name = box_name[i - 1]

                    # Create a cube for the sticker
                    box_obj = box(pos=v + direction_dict[box_face_name] * box_height,
                                  length=1 - box_margin,
                                  height=1 - box_margin,
                                  width=1 - box_margin,
                                  color=colors_dict[box_face_type])
                    box_face_list.append(box_obj)
                face_dict[box_name] = box_face_list

                # Create a base cube for the piece
                base_box = box(
                            pos=v,
                            length=1,
                            height=1,
                            width=1,
                            color=base_color)

                # Store this base cube
                self.base_box_list.append(base_box)
                for dir_name in direction_names:
                    if dir_name in face_name + box_name:
                        base_box_dict[dir_name].append(base_box)

            box_dict[face_name] = face_dict
        return box_dict, base_box_dict

    """
        Make the appropriate animation for the given move
    """
    def move(self, move, n=1, record=True, step_func=smooth_step):
        super().move(move, n, record)

        # Prepare arguments
        if type(move) == tuple:
            move, n = move
        n %= 4
        if n == 0 or not record:
            return

        # Prepare variables
        cubes = self.get_cubes_from_move(move)
        base_cubes = self.get_base_cubes_from_move(move)
        axis = direction_dict[move[0]]
        t0, rotated = time(), 0
        t = n if n <= 2 else -1

        # Animate all cubes
        while time() - t0 <= self.move_time * np.abs(t):
            rate(self.fps)
            rotation = pi / 2 * step_func((time() - t0) / self.move_time / t) * t
            for cube in cubes + base_cubes:
                cube.rotate(
                    angle=rotation - rotated,
                    axis=axis,
                    origin=vector(0, 0, 0)
                )
            rotated = rotation

        # Finish rotation
        rotation = pi / 2 * t
        for cube in cubes:
            cube.rotate(
                angle=rotation - rotated,
                axis=axis,
                origin=vector(0, 0, 0)
            )

        # Undo base rotations
        for cube in base_cubes:
            cube.rotate(
                angle=-rotated,
                axis=axis,
                origin=vector(0, 0, 0)
            )

        # Wait
        t0 = time()
        while time() - t0 < self.wait_time:
            rate(self.fps)

        # Update graphics cube
        self.box_cube.move(move, n, record)

    """
        Return a list of the cubes that should rotate on a given move
    """
    def get_cubes_from_move(self, move):
        c = self.box_cube.cube_dict
        if move == "U" or move == "D":
            c = self.box_cube.cube_dict[move]
            return c["F"] + c["R"] + c["B"] + c["L"] + c[move] + c["FR"] + c["RB"] + c["BL"] + c["LF"]
        elif move == "F":
            return c["U"]["F"] + c["L"]["F"] + c["D"]["F"] + c["F"]["R"] + \
                   c["U"]["LF"] + c["D"]["LF"] + c["D"]["FR"] + c["U"]["FR"] + c[move][move]
        elif move == "R":
            return c["U"]["R"] + c["F"]["R"] + c["D"]["R"] + c["R"]["B"] + \
                   c["U"]["FR"] + c["D"]["FR"] + c["D"]["RB"] + c["U"]["RB"] + c[move][move]
        elif move == "B":
            return c["U"]["B"] + c["R"]["B"] + c["D"]["B"] + c["B"]["L"] + \
                   c["U"]["RB"] + c["D"]["RB"] + c["D"]["BL"] + c["U"]["BL"] + c[move][move]
        elif move == "L":
            return c["U"]["L"] + c["B"]["L"] + c["D"]["L"] + c["L"]["F"] + \
                   c["U"]["BL"] + c["D"]["BL"] + c["D"]["LF"] + c["U"]["LF"] + c[move][move]
        elif move == "UD":
            return c["F"]["R"] + c["R"]["B"] + c["B"]["L"] + c["L"]["F"] + \
                   c["F"]["F"] + c["R"]["R"] + c["B"]["B"] + c["L"]["L"]
        elif move == "FB":
            return c["U"]["L"] + c["D"]["L"] + c["D"]["R"] + c["U"]["R"] + \
                   c["U"]["U"] + c["L"]["L"] + c["D"]["D"] + c["R"]["R"]
        elif move == "RL":
            return c["U"]["F"] + c["D"]["F"] + c["D"]["B"] + c["U"]["B"] + \
                   c["U"]["U"] + c["F"]["F"] + c["D"]["D"] + c["B"]["B"]
        else:
            all_stickers = []
            for k in c:
                for kk in c[k]:
                    if type(c[k][kk]) is list:
                        all_stickers += c[k][kk]
                    else:
                        all_stickers.append(c[k][kk])
            return all_stickers

    """
        Return a list of the base cubes that should rotate on a given move
    """
    def get_base_cubes_from_move(self, move):
        if len(move) == 1:
            return self.base_box_dict[move]
        elif move[0] != move[1]:
            return [cube for cube in self.base_box_list
                    if cube not in self.base_box_dict[move[0]] and cube not in self.base_box_dict[move[1]]]
        else:
            return self.base_box_dict["U"] + self.base_box_dict["D"] + self.get_base_cubes_from_move("UD")

