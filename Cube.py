from util import *


class Cube:
    def __init__(self, cube_dict=solved_cube_dict):
        self.cube_dict = cube_dict.copy() # DEEP COPY ??

    def is_solved(self):
        return  self.cube_dict == solved_cube_dict

    def moves(self, moves):
        for move, n in moves:
            self.move(move, n)

    def move(self, move, n=1):
        n %= 4

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

    def get_sides(self, h=0):
        sides = [self.cube_dict["U"][s] for s in side_names] + \
                [self.cube_dict[s][ss] for s, ss in zip(side_names, side_names_roll)] + \
                [self.cube_dict["D"][s] for s in side_names]
        return sides[4*h:]


