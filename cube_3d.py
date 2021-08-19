from vpython import *
from cube import *
from util import *
from configs import *
from time import time
import numpy as np


def smooth_step(x):
    return 0.5 - np.cos(x * pi) / 2


class Cube3D(Cube):
    def __init__(self, cube_dict=solved_cube_dict, shuffle=False, n_shuffles=200, record=False, do_copy=False,
                 fps=fps_def, move_time=move_time_def):
        super().__init__(cube_dict, shuffle, n_shuffles, record, do_copy)
        self.base_box = None
        self.box_dict = self.init_graphics_cube()
        self.box_cube = Cube(self.box_dict, shuffle=False, do_copy=False)

        self.fps = fps
        self.move_time = move_time

    def init_graphics_cube(self):
        cube_dict = self.cube_dict
        self.base_box = box(pos=vector(0, 0, 0), length=3, height=3, width=3, color=base_color)

        box_dict = {}
        for face_name, dir in direction_dict.items():
            face_dict = {}
            for box_name in cube_dict[face_name]:
                v = dir
                if box_name != face_name:
                    for c in box_name:
                        v = v + direction_dict[c]
                box_face_list = []
                for i, box_face_type in enumerate(cube_dict[face_name][box_name]):
                    if i == 0:
                        box_face_name = face_name
                    else:
                        box_face_name = box_name[i - 1]

                    box_obj = box(pos=v + direction_dict[box_face_name] * box_height,
                                  length=1 - box_margin,
                                  height=1 - box_margin,
                                  width=1 - box_margin,
                                  color=colors_dict[box_face_type])
                    self.tmp = box_obj
                    box_face_list.append(box_obj)
                face_dict[box_name] = box_face_list
            box_dict[face_name] = face_dict
        return box_dict

    def rotate(self, axis, n=1):
        super().rotate(axis, n)
        self.box_cube.rotate(axis, n)

    def move(self, move, n=1, record=True, step_func=smooth_step):
        super().move(move, n, record)

        if type(move) == tuple:
            move, n = move
        n %= 4
        if n == 0:
            return

        cubes = self.get_cubes_from_move(move)
        axis = direction_dict[move[0]]
        t0, rotated = time(), 0
        t = n if n <= 2 else -1

        while time() - t0 <= self.move_time * t:
            rate(self.fps)
            rotation = pi / 2 * step_func((time() - t0) / self.move_time / t) * t
            for cube in cubes:
                cube.rotate(
                    angle=rotation - rotated,
                    axis=axis,
                    origin=vector(0, 0, 0)
                )
            rotated = rotation

        for i in range(20):
            rate(5)

        # Update graphics cube
        self.box_cube.move(move, n, record)

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
        elif len(move) == 2 and move[0] == move[1]:
            return self.get_cubes_from_move("U") + self.get_cubes_from_move("D") + \
                [c["F"]["R"], c["R"]["B"], c["B"]["L"], c["L"]["F"],
                 c["F"]["F"], c["R"]["R"], c["B"]["B"], c["L"]["L"]]
