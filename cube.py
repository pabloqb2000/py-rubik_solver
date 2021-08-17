from util import *
import copy


class Cube:
    def __init__(self, cube_dict=solved_cube_dict, shuffle=False, n_shuffles=200, record=False):
        self.cube_dict = copy.deepcopy(cube_dict)
        self.record = record
        self.moves_made = []

        if shuffle:
            self.moves([random_move() for _ in range(n_shuffles)])

    def copy(self):
        return Cube(self.cube_dict, shuffle=False)

    def is_solved(self):
        return self.cube_dict == solved_cube_dict

    def get_sides(self, h=0):
        sides = [self.cube_dict["U"][s] for s in side_names] + \
                [self.cube_dict[s][ss] for s, ss in zip(side_names, side_names_roll)] + \
                [self.cube_dict["D"][s] for s in side_names]
        return sides[4*h:]

    def rotate(self, axis, n=1):
        opposite = {"U": "D", "F": "B", "R": "L"}
        self.moves([
            (axis, n),
            (axis + opposite[axis], n),
            (opposite[axis], -n)
        ], record=False)

    def moves(self, moves, record=True):
        for move, n in moves:
            self.move(move, n, record=record)

    def move(self, move, n=1, record=True):
        if type(move) == tuple:
            move, n = move

        n %= 4
        if n == 0:
            return

        if self.record and record:
            self.moves_made.append((move, n))

        if move == "U":
            for _ in range(n):
                self.moveU()
        elif move == "F":
            for _ in range(n):
                self.moveF()
        elif move == "R":
            for _ in range(n):
                self.moveR()
        elif move == "B":
            for _ in range(n):
                self.moveB()
        elif move == "L":
            for _ in range(n):
                self.moveL()
        elif move == "D":
            for _ in range(n):
                self.moveD()
        elif move == "UD":
            for _ in range(n):
                self.moveUD()
        elif move == "FB":
            for _ in range(n):
                self.moveFB()
        elif move == "RL":
            for _ in range(n):
                self.moveRL()
        elif len(move) == 2 and move[0] == move[1]:
            self.rotate(move[0], n)

    def moveU(self):
        c = self.cube_dict["U"]

        c["F"], c["R"], c["B"], c["L"] = \
        c["L"], c["F"], c["R"], c["B"]

        c["FR"], c["RB"], c["BL"], c["LF"] = \
        c["LF"], c["FR"], c["RB"], c["BL"]

    def moveF(self):
        c = self.cube_dict

        c["U"]["F"], c["L"]["F"], c["D"]["F"], c["F"]["R"] = \
        c["F"]["R"][::-1], c["U"]["F"], c["L"]["F"], c["D"]["F"][::-1]

        c["U"]["LF"], c["D"]["LF"], c["D"]["FR"], c["U"]["FR"] = \
            [c["U"]["FR"][2], c["U"]["FR"][0], c["U"]["FR"][1]],\
            [c["U"]["LF"][1], c["U"]["LF"][0], c["U"]["LF"][2]],\
            [c["D"]["LF"][1], c["D"]["LF"][2], c["D"]["LF"][0]],\
            [c["D"]["FR"][2], c["D"]["FR"][1], c["D"]["FR"][0]]

    def moveR(self):
        c = self.cube_dict

        c["U"]["R"], c["F"]["R"], c["D"]["R"], c["R"]["B"] = \
        c["R"]["B"][::-1], c["U"]["R"], c["F"]["R"], c["D"]["R"][::-1]

        c["U"]["FR"], c["D"]["FR"], c["D"]["RB"], c["U"]["RB"] = \
            [c["U"]["RB"][2], c["U"]["RB"][0], c["U"]["RB"][1]],\
            [c["U"]["FR"][1], c["U"]["FR"][0], c["U"]["FR"][2]],\
            [c["D"]["FR"][1], c["D"]["FR"][2], c["D"]["FR"][0]],\
            [c["D"]["RB"][2], c["D"]["RB"][1], c["D"]["RB"][0]]

    def moveB(self):
        c = self.cube_dict

        c["U"]["B"], c["R"]["B"], c["D"]["B"], c["B"]["L"] = \
        c["B"]["L"][::-1], c["U"]["B"], c["R"]["B"], c["D"]["B"][::-1]

        c["U"]["RB"], c["D"]["RB"], c["D"]["BL"], c["U"]["BL"] = \
            [c["U"]["BL"][2], c["U"]["BL"][0], c["U"]["BL"][1]],\
            [c["U"]["RB"][1], c["U"]["RB"][0], c["U"]["RB"][2]],\
            [c["D"]["RB"][1], c["D"]["RB"][2], c["D"]["RB"][0]],\
            [c["D"]["BL"][2], c["D"]["BL"][1], c["D"]["BL"][0]]

    def moveL(self):
        c = self.cube_dict

        c["U"]["L"], c["B"]["L"], c["D"]["L"], c["L"]["F"] = \
        c["L"]["F"][::-1], c["U"]["L"], c["B"]["L"], c["D"]["L"][::-1]

        c["U"]["BL"], c["D"]["BL"], c["D"]["LF"], c["U"]["LF"] = \
            [c["U"]["LF"][2], c["U"]["LF"][0], c["U"]["LF"][1]],\
            [c["U"]["BL"][1], c["U"]["BL"][0], c["U"]["BL"][2]],\
            [c["D"]["BL"][1], c["D"]["BL"][2], c["D"]["BL"][0]],\
            [c["D"]["LF"][2], c["D"]["LF"][1], c["D"]["LF"][0]]

    def moveD(self):
        c = self.cube_dict["D"]

        c["F"], c["R"], c["B"], c["L"] = \
        c["R"], c["B"], c["L"], c["F"]

        c["FR"], c["RB"], c["BL"], c["LF"] = \
        c["RB"], c["BL"], c["LF"], c["FR"]

    def moveUD(self):
        c = self.cube_dict
        c["F"]["R"], c["R"]["B"], c["B"]["L"], c["L"]["F"] = \
        c["L"]["F"], c["F"]["R"], c["R"]["B"], c["B"]["L"]

        c["F"]["F"], c["R"]["R"], c["B"]["B"], c["L"]["L"] = \
        c["L"]["L"], c["F"]["F"], c["R"]["R"], c["B"]["B"]

    def moveFB(self):
        c = self.cube_dict
        c["U"]["L"], c["D"]["L"], c["D"]["R"], c["U"]["R"] = \
        c["U"]["R"][::-1], c["U"]["L"][::-1], c["D"]["L"][::-1], c["D"]["R"][::-1]

        c["U"]["U"], c["L"]["L"], c["D"]["D"], c["R"]["R"] = \
        c["R"]["R"], c["U"]["U"], c["L"]["L"], c["D"]["D"]

    def moveRL(self):
        c = self.cube_dict
        c["U"]["F"], c["D"]["F"], c["D"]["B"], c["U"]["B"] = \
        c["U"]["B"][::-1], c["U"]["F"][::-1], c["D"]["F"][::-1], c["D"]["B"][::-1]

        c["U"]["U"], c["F"]["F"], c["D"]["D"], c["B"]["B"] = \
        c["B"]["B"], c["U"]["U"], c["F"]["F"], c["D"]["D"]



