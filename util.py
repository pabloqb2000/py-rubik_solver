from vpython import vector
from random import choice, randint

solved_cube_dict = {
    "U": {
        "U": "U",
        "F": ["U", "F"],
        "R": ["U", "R"],
        "B": ["U", "B"],
        "L": ["U", "L"],
        "FR": ["U", "F", "R"],
        "RB": ["U", "R", "B"],
        "BL": ["U", "B", "L"],
        "LF": ["U", "L", "F"],
    },
    "F": {
        "F": "F",
        "R": ["F", "R"]
    },
    "R": {
        "R": "R",
        "B": ["R", "B"]
    },
    "B": {
        "B": "B",
        "L": ["B", "L"]
    },
    "L": {
        "L": "L",
        "F": ["L", "F"]
    },
    "D": {
        "D": "D",
        "F": ["D", "F"],
        "R": ["D", "R"],
        "B": ["D", "B"],
        "L": ["D", "L"],
        "FR": ["D", "F", "R"],
        "RB": ["D", "R", "B"],
        "BL": ["D", "B", "L"],
        "LF": ["D", "L", "F"],
    },
}

direction_names = list(solved_cube_dict.keys())
side_names = direction_names[1:-1]
side_names_roll = side_names[1:] + [side_names[0]]
direction_vectors = [
    vector(0, 1, 0),
    vector(0, 0, 1),
    vector(1, 0, 0),
    vector(0, 0, -1),
    vector(-1, 0, 0),
    vector(0, -1, 0),
]
direction_dict = {k: v for k, v in zip(direction_names, direction_vectors)}
up_corner_names = list(solved_cube_dict["U"].keys())[-4:]
up_corner_values = list(solved_cube_dict["U"].values())[-4:]
down_corner_names = list(solved_cube_dict["D"].keys())[-4:]
down_corner_values = list(solved_cube_dict["D"].values())[-4:]


def random_move():
    return choice(direction_names), randint(1, 3)


def is_sublist(a, b):
    return all([e in b for e in a])

