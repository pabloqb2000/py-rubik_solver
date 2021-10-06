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

opposite_face = {"U": "D", "F": "B", "R": "L", "D": "U", "B": "F", "L": "R"}
prioritary_faces = ["U", "F", "R"]
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


def array_to_vector(arr):
    return [vector(*a) for a in arr]


def run_checks(cube_dict):
    """
        Check the different stages of the simple_solver algorithm
    """
    print("First cross solved:", all(cube_dict["U"][pos] == ["U", pos] for pos in side_names))
    print("First corners position:", all(
        "U" in cube_dict["U"][name] and
        name[0] in cube_dict["U"][name] and
        name[1] in cube_dict["U"][name]
        for name in up_corner_names))
    print("First corners rotation:", all(cube_dict["U"][name] == ["U", name[0], name[1]]
                                         for name in up_corner_names))

    print("Second row position:", all(cube_dict[s1][s2] == [s1, s2]
                                      for s1, s2 in zip(side_names, side_names_roll)))

    print("Down cross solved:", all(cube_dict["D"][pos][0] == "D" for pos in side_names))
    print("Down cross solved:", all(cube_dict["D"][pos] == ["D", pos] for pos in side_names))
    print("Second corners position:", all(
        "D" in cube_dict["D"][name] and
        name[0] in cube_dict["D"][name] and
        name[1] in cube_dict["D"][name]
        for name in down_corner_names))

    print("CUBE SOLVED:", cube_dict == solved_cube_dict)


def assign_values(c, values):
    """
        Given a cube dictionary and a list of values for each face
        assign to each sticker the corresponding value
    """
    c["U"]["BL"][0] = direction_names[values[0]]
    c["U"]["B"][0] = direction_names[values[1]]
    c["U"]["RB"][0] = direction_names[values[2]]
    c["U"]["L"][0] = direction_names[values[3]]
    c["U"]["U"] = direction_names[values[4]]
    c["U"]["R"][0] = direction_names[values[5]]
    c["U"]["LF"][0] = direction_names[values[6]]
    c["U"]["F"][0] = direction_names[values[7]]
    c["U"]["FR"][0] = direction_names[values[8]]

    c["U"]["LF"][2] = direction_names[values[9]]
    c["U"]["F"][1] = direction_names[values[10]]
    c["U"]["FR"][1] = direction_names[values[11]]
    c["L"]["F"][1] = direction_names[values[12]]
    c["F"]["F"] = direction_names[values[13]]
    c["F"]["R"][0] = direction_names[values[14]]
    c["D"]["LF"][2] = direction_names[values[15]]
    c["D"]["F"][1] = direction_names[values[16]]
    c["D"]["FR"][1] = direction_names[values[17]]

    c["U"]["FR"][2] = direction_names[values[18]]
    c["U"]["R"][1] = direction_names[values[19]]
    c["U"]["RB"][1] = direction_names[values[20]]
    c["F"]["R"][1] = direction_names[values[21]]
    c["R"]["R"] = direction_names[values[22]]
    c["R"]["B"][0] = direction_names[values[23]]
    c["D"]["FR"][2] = direction_names[values[24]]
    c["D"]["R"][1] = direction_names[values[25]]
    c["D"]["RB"][1] = direction_names[values[26]]

    c["U"]["RB"][2] = direction_names[values[27]]
    c["U"]["B"][1] = direction_names[values[28]]
    c["U"]["BL"][1] = direction_names[values[29]]
    c["R"]["B"][1] = direction_names[values[30]]
    c["B"]["B"] = direction_names[values[31]]
    c["B"]["L"][0] = direction_names[values[32]]
    c["D"]["RB"][2] = direction_names[values[33]]
    c["D"]["B"][1] = direction_names[values[34]]
    c["D"]["BL"][1] = direction_names[values[35]]

    c["U"]["BL"][2] = direction_names[values[36]]
    c["U"]["L"][1] = direction_names[values[37]]
    c["U"]["LF"][1] = direction_names[values[38]]
    c["B"]["L"][1] = direction_names[values[39]]
    c["L"]["L"] = direction_names[values[40]]
    c["L"]["F"][0] = direction_names[values[41]]
    c["D"]["BL"][2] = direction_names[values[42]]
    c["D"]["L"][1] = direction_names[values[43]]
    c["D"]["LF"][1] = direction_names[values[44]]

    c["D"]["LF"][0] = direction_names[values[45]]
    c["D"]["F"][0] = direction_names[values[46]]
    c["D"]["FR"][0] = direction_names[values[47]]
    c["D"]["L"][0] = direction_names[values[48]]
    c["D"]["D"] = direction_names[values[49]]
    c["D"]["R"][0] = direction_names[values[50]]
    c["D"]["BL"][0] = direction_names[values[51]]
    c["D"]["B"][0] = direction_names[values[52]]
    c["D"]["RB"][0] = direction_names[values[53]]

    return c

