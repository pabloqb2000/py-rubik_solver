from vpython import *
from cube import *
from configs import *

cube = Cube()
cube_dict = cube.cube_dict
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


def update_box_colors(cube_dict, box_dict):
    for face_name in cube_dict:
        for box_name in cube_dict[face_name]:
            for i, box_face_type in enumerate(cube_dict[face_name][box_name]):
                if i == 0:
                    box_face_name = face_name
                else:
                    box_face_name = box_name[i - 1]

                box_dict[face_name][box_name][box_face_name].color = colors_dict[box_face_type]


c = 0
while 1:
    rate(5)  # fps

    c += 1
    if c % 5 == 0:
        cube.move(*random_move())
        # cube.move("U", 2)
        update_box_colors(cube_dict, box_dict)


