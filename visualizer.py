from vpython import *
from cube import *
from configs import *
from time import time
from simple_solver import *


cube = Cube(shuffle=True, record=False)
cube.move("F", 2)
cube.move("D", -1)
print(cube.cube_dict)
cube_dictionary = cube.cube_dict
cube_solver = SimpleSolver(cube.copy())
steps = cube_solver.solve()


def init_graphics_cube(cube_dict):
    base_box = box(pos=vector(0, 0, 0), length=3, height=3, width=3, color=base_color)

    box_dict = {}
    for face_name, dir in direction_dict.items():
        face_dict = {}
        for box_name in cube_dict[face_name]:
            v = dir
            if box_name != face_name:
                for c in box_name:
                    v = v + direction_dict[c]
            box_face_dict = {}
            for i, box_face_type in enumerate(cube_dict[face_name][box_name]):
                if i == 0:
                    box_face_name = face_name
                else:
                    box_face_name = box_name[i-1]

                box_obj = box(pos=v + direction_dict[box_face_name]*box_height,
                              length=1 - box_margin,
                              height=1 - box_margin,
                              width=1 - box_margin,
                              color=colors_dict[box_face_type])
                box_face_dict[box_face_name] = box_obj
            face_dict[box_name] = box_face_dict
        box_dict[face_name] = face_dict
    return box_dict


def update_box_colors(cube_dict, box_dict):
    for face_name in cube_dict:
        for box_name in cube_dict[face_name]:
            for i, box_face_type in enumerate(cube_dict[face_name][box_name]):
                if i == 0:
                    box_face_name = face_name
                else:
                    box_face_name = box_name[i - 1]

                box_dict[face_name][box_name][box_face_name].color = colors_dict[box_face_type]


print("First cross solved:", all(cube_solver.cube.cube_dict["U"][pos] == ["U", pos] for pos in side_names))
print("First corners position:", all(
    "U" in cube_solver.cube.cube_dict["U"][name] and
    name[0] in cube_solver.cube.cube_dict["U"][name] and
    name[1] in cube_solver.cube.cube_dict["U"][name]
    for name in up_corner_names))
print("First corners rotation:", all(cube_solver.cube.cube_dict["U"][name] == ["U", name[0], name[1]]
                                     for name in up_corner_names))
print("Second row position:", all(cube_solver.cube.cube_dict[s1][s2] == [s1, s2]
                                  for s1, s2 in zip(side_names, side_names_roll)))
print("Down cross solved:", all(cube_solver.cube.cube_dict["D"][pos][0] == "D" for pos in side_names))
print("Down cross solved:", all(cube_solver.cube.cube_dict["D"][pos] == ["D", pos] for pos in side_names))


box_dictionary = init_graphics_cube(cube_dictionary)
dt = 0
t0 = time()
step = 0
while 1:
    rate(10)  # fps

    if time() - t0 > dt:
        t0 = time()
        # cube.move(*random_move())
        if step < len(steps):
            cube.move(steps[step])
            step += 1
        update_box_colors(cube_dictionary, box_dictionary)


