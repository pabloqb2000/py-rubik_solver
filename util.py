from vpython import vector

solved_cube_dict = {
    "U": {
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
        "R": ["F", "R"]
    },
    "R": {
        "B": ["R", "B"]
    },
    "B": {
        "L": ["B", "L"]
    },
    "L": {
        "F": ["L", "F"]
    },
    "D": {
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

'''
solved_cube_dict = {
    "U": {
        "F": {"U": "U", "F": "F"},
        "R": {"U": "U", "R": "B"},
        "B": {"U": "U", "B": "B"},
        "L": {"U": "U", "L": "L"},
        "FR": {"U": "U", "F": "F", "R": "R"},
        "RB": {"U": "U", "R": "R", "B": "B"},
        "BL": {"U": "U", "B": "B", "L": "L"},
        "LF": {"U": "U", "L": "L", "F": "F"},
    },
    "F": {
        "R": {"F": "F", "R": "R"}
    },
    "R": {
        "B": {"R": "R", "B": "B"}
    },
    "B": {
        "L": {"B": "B", "L": "L"}
    },
    "L": {
        "F": {"L": "L", "F": "F"}
    },
    "D": {
        "F": {"D": "D", "F": "F"},
        "R": {"D": "D", "R": "R"},
        "B": {"D": "D", "B": "B"},
        "L": {"D": "D", "L": "L"},
        "FR": {"D": "D", "F": "F", "R": "R"},
        "RB": {"D": "D", "R": "R", "B": "B"},
        "BL": {"D": "D", "B": "B", "L": "L"},
        "LF": {"D": "D", "L": "L", "F": "F"},
    },
}
'''

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

