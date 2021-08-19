from util import *
from cube_solver import *


class SimpleSolver(CubeSolver):
    def __solve_cube__(self):
        self.cube.moves_made = []
        self.cube.record = True

        self.solve_first_cross()
        self.solve_first_corners()
        self.solve_second_row()
        self.solve_second_cross()
        self.orientate_2nd_cross()
        self.solve_second_corners()
        self.orientate_2nd_corners()
        self.reorient_cube()

        self.cube.record = False
        solution = self.cube.moves_made
        self.cube.moves_made = []
        return solution

    def solve_first_cross(self):
        for side in side_names:
            if self.cube.cube_dict["U"]["F"] != ["U", side]:
                # Top face
                for pos in side_names:
                    if side in self.cube.cube_dict["U"][pos] and "U" in self.cube.cube_dict["U"][pos]:
                        self.cube.move(pos, 2)
                        break

                # Middle face
                if side in self.cube.cube_dict["F"]["R"] and "U" in self.cube.cube_dict["F"]["R"]:
                    self.cube.move("F", -1)
                elif side in self.cube.cube_dict["R"]["B"] and "U" in self.cube.cube_dict["R"]["B"]:
                    self.cube.move("B",  1)
                    self.cube.move("D",  1)
                    self.cube.move("B", -1)
                elif side in self.cube.cube_dict["B"]["L"] and "U" in self.cube.cube_dict["B"]["L"]:
                    self.cube.move("B", -1)
                    self.cube.move("D",  1)
                    self.cube.move("B",  1)
                elif side in self.cube.cube_dict["L"]["F"] and "U" in self.cube.cube_dict["L"]["F"]:
                    self.cube.move("F",  1)

                # Down face, up color facing down
                for i, pos in enumerate(side_names):
                    if self.cube.cube_dict["D"][pos] == ["U", side]:
                        self.cube.move("D", i)
                        self.cube.move("F", 2)
                        break

                # Down face, side color facing down
                for i, pos in enumerate(side_names):
                    if self.cube.cube_dict["D"][pos] == [side, "U"]:
                        self.cube.move("D", i-1)
                        self.cube.move("R", -1)
                        self.cube.move("F",  1)
                        self.cube.move("R",  1)
                        break

            self.cube.move("UU", -1)

    def solve_first_corners(self):
        cube = self.cube.cube_dict
        for corner_name, corner_value in zip(up_corner_names, up_corner_values):
            # Get corner in UFR position from up face
            for i, pos in enumerate(up_corner_names):
                if is_sublist(corner_value, cube["U"][pos]):
                    self.cube.move("U", -i)

                    self.cube.move("R", 1)
                    self.cube.move("D", 1)
                    self.cube.move("R", -1)

                    self.cube.move("U", i)

                    self.cube.move("R", 1)
                    self.cube.move("D", -1)
                    self.cube.move("R", -1)

            # Get corner in UFR position from down face
            for i, pos in enumerate(down_corner_names):
                if is_sublist(corner_value, cube["D"][pos]):
                    self.cube.move("D", i+1)
                    self.cube.move("R", 1)
                    self.cube.move("D", -1)
                    self.cube.move("R", -1)

            # Rotate corner to correct orientation
            # Up face facing front
            if self.cube.cube_dict["U"]["FR"][1] == "U":
                self.cube.move("R",  1)
                self.cube.move("D", -1)
                self.cube.move("R", -1)
                self.cube.move("D",  1)
                self.cube.move("R",  1)
                self.cube.move("D", -1)
                self.cube.move("R", -1)
            # Up face facing right
            elif self.cube.cube_dict["U"]["FR"][2] == "U":
                self.cube.move("F", -1)
                self.cube.move("D",  1)
                self.cube.move("F",  1)
                self.cube.move("D", -1)
                self.cube.move("F", -1)
                self.cube.move("D",  1)
                self.cube.move("F",  1)

            self.cube.move("UU", -1)

    def solve_second_row(self):
        for s1, s2 in zip(side_names, side_names_roll):
            # Get the piece down if it is in the middle row
            for i in range(4):
                if s1 in self.cube.cube_dict["F"]["R"] and s2 in self.cube.cube_dict["F"]["R"]:
                    self.__get_2nd_row_front_right__()
                self.cube.move("UU", -1)

            # Get the piece up from the down row
            # Either s1 or s2 should be facing out
            # If s1 (front face) is facing out
            for i, s in enumerate(side_names):
                if self.cube.cube_dict["D"][s] == [s2, s1]:
                    self.cube.move("D", i)
                    self.__get_2nd_row_front_right__()
            # if s2 (right face) is facing out
            for i, s in enumerate(side_names):
                if self.cube.cube_dict["D"][s] == [s1, s2]:
                    self.cube.move("D", i - 1)
                    self.cube.move("UU", -1)
                    self.__get_2nd_row_front_left__()
                    self.cube.move("UU", 1)

            self.cube.move("UU", -1)

    def solve_second_cross(self):
        # First we compute the number of iterations needed
        # First we make a list of the stickers in the down face
        down_stickers = [self.cube.cube_dict["D"][s][0] for s in side_names]

        if all([s == "D" for s in down_stickers]):  # Cross is solved
            self.info["down_shape"] = "+"
            pass
        elif all([s != "D" for s in down_stickers]):  # None is solved
            self.info["down_shape"] = " "
            self.__iterate_second_cross__()
            self.cube.move("D", 2)
            self.__iterate_second_cross__()
            self.__iterate_second_cross__()
        elif down_stickers[0] == "D" and down_stickers[2] == "D":  # Vertical line is solved
            self.info["down_shape"] = "-"
            self.cube.move("D", 1)
            self.__iterate_second_cross__()
        elif down_stickers[1] == "D" and down_stickers[3] == "D":  # Horizontal line is solved
            self.info["down_shape"] = "-"
            self.__iterate_second_cross__()
        else:  # L shape is solved
            self.info["down_shape"] = "l"
            # Rotate L
            if down_stickers[0] == "D" and down_stickers[1] == "D":
                self.cube.move("D", 1)
            elif down_stickers[1] == "D" and down_stickers[2] == "D":
                self.cube.move("D", 2)
            elif down_stickers[2] == "D" and down_stickers[3] == "D":
                self.cube.move("D", -1)

            self.__iterate_second_cross__()
            self.__iterate_second_cross__()

    def orientate_2nd_cross(self):
        # Orientate down face
        reps = 0
        for i in range(4):
            # First we make a list of the stickers in the outside of the down face
            down_stickers = [self.cube.cube_dict["D"][s][1] for s in side_names]

            # Rotate down face until 2 or more stickers are oriented
            reps = 0
            for sticker, name in zip(down_stickers, side_names):
                if sticker == name:
                    reps += 1
            if reps >= 2:
                break
            self.cube.move("D", 1)

        # Rotate the cube to apply the series of moves
        for i in range(4):
            if self.cube.cube_dict["D"]["F"][1] == self.cube.cube_dict["F"]["F"]:
                break
            self.cube.move("UU", 1)
        if self.cube.cube_dict["D"]["R"][1] == self.cube.cube_dict["R"]["R"]:
            self.cube.move("UU", -1)
        self.cube.move("FF", 2)

        # Apply the moves
        if reps == 4:
            self.info["down_cross_coincidences"] = "+"
            return
        elif self.cube.cube_dict["U"]["B"][1] == self.cube.cube_dict["B"]["B"]:  # Line shape
            self.info["down_cross_coincidences"] = "-"
            self.__orientate_2nd_cross()
            self.cube.move("UU", -1)
        else:
            self.info["down_cross_coincidences"] = "l"
        self.__orientate_2nd_cross()
        self.cube.move("U", 1)

    def solve_second_corners(self):
        coincidences = self.__count_coincidences__()
        self.info["2nd_corner_coincidences"] = coincidences
        self.info["iterations"] = 0

        while coincidences != 4:
            if coincidences == 1:
                # Rotate to get coincidence in the UFR corner
                for i in range(4):
                    piece = self.cube.cube_dict["U"]["FR"]
                    if self.cube.cube_dict["F"]["F"] in piece and \
                       self.cube.cube_dict["R"]["R"] in piece:
                        break
                    self.cube.move("UU", 1)

            # Iterate the position of the corners
            self.__iterate_second_corners__()
            coincidences = self.__count_coincidences__()

    def orientate_2nd_corners(self):
        # Rotate corner by corner
        # Check if all corners are oriented
        while not all(self.cube.cube_dict["U"][c][0] == "D" for c in up_corner_names):
            for i in range(4):
                if self.cube.cube_dict["U"]["FR"][0] != "D":
                    break
                self.cube.move("U", 1)
            self.__orientate_2nd_corners__()

        while self.cube.cube_dict["U"]["F"][1] != self.cube.cube_dict["F"]["F"]:
            self.cube.move("U", 1)

    def reorient_cube(self):
        self.cube.move("FF", 2)
        for i in range(4):
            if self.cube.cube_dict["F"]["F"] == "F":
                return
            self.cube.move("UU", 1)

    def __get_2nd_row_front_right__(self):
        self.cube.move("D",  1)
        self.cube.move("R",  1)
        self.cube.move("D", -1)
        self.cube.move("R", -1)
        self.cube.move("D", -1)
        self.cube.move("F", -1)
        self.cube.move("D",  1)
        self.cube.move("F",  1)

    def __get_2nd_row_front_left__(self):
        self.cube.move("D", -1)
        self.cube.move("L", -1)
        self.cube.move("D",  1)
        self.cube.move("L",  1)
        self.cube.move("D",  1)
        self.cube.move("F",  1)
        self.cube.move("D", -1)
        self.cube.move("F", -1)

    def __iterate_second_cross__(self):
        self.cube.move("B", -1)
        self.cube.move("R", -1)
        self.cube.move("D", -1)
        self.cube.move("R",  1)
        self.cube.move("D",  1)
        self.cube.move("B",  1)

    def __orientate_2nd_cross(self):
        self.cube.move("R",  1)
        self.cube.move("U",  1)
        self.cube.move("R", -1)
        self.cube.move("U",  1)
        self.cube.move("R",  1)
        self.cube.move("U",  2)
        self.cube.move("R", -1)

    def __count_coincidences__(self):
        # Count the amount of corners in their correct position
        coincidences = 0
        for i in range(4):
            piece = self.cube.cube_dict["U"]["FR"]
            if self.cube.cube_dict["F"]["F"] in piece and \
               self.cube.cube_dict["R"]["R"] in piece:
                coincidences += 1
            self.cube.move("UU", 1, record=False)
        return coincidences

    def __iterate_second_corners__(self):
        self.cube.move("U", -1)
        self.cube.move("R", -1)
        self.cube.move("U",  1)
        self.cube.move("L",  1)
        self.cube.move("U", -1)
        self.cube.move("R",  1)
        self.cube.move("U",  1)
        self.cube.move("L", -1)

    def __orientate_2nd_corners__(self):
        self.info["iterations"] += 1
        self.cube.move("R",  1)
        self.cube.move("D",  1)
        self.cube.move("R", -1)
        self.cube.move("D", -1)


