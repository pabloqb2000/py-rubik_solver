from util import *
from cube_solver import *


class SimpleSolver(CubeSolver):
    """
        Beginners algorithm for solving the cube
        Solves the cube by going through different stages
        each solved by a different function
    """
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

    """
        Solve the cross on the UP face
    """
    def solve_first_cross(self):
        # Solve each of the cross pieces
        for side in side_names:
            if self.cube.cube_dict["U"]["F"] != ["U", side]:
                # Get the pieces on the UP face to the DOWN face
                for pos in side_names:
                    if side in self.cube.cube_dict["U"][pos] and "U" in self.cube.cube_dict["U"][pos]:
                        self.cube.move(pos, 2)
                        break

                # Get the pieces on the middle face to the DOWN face
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

                # Get the pieces to the UP face when the UP color is facing DOWN
                for i, pos in enumerate(side_names):
                    if self.cube.cube_dict["D"][pos] == ["U", side]:
                        self.cube.move("D", i)
                        self.cube.move("F", 2)
                        break

                # Get the pieces to the UP face when the UP color is facing OUT
                for i, pos in enumerate(side_names):
                    if self.cube.cube_dict["D"][pos] == [side, "U"]:
                        self.cube.move("D", i-1)
                        self.cube.move("R", -1)
                        self.cube.move("F",  1)
                        self.cube.move("R",  1)
                        break

            self.cube.move("UU", -1)

    """
        Solve the corners in the UP face
    """
    def solve_first_corners(self):
        cube = self.cube.cube_dict

        # Solve each of the corners
        for corner_name, corner_value in zip(up_corner_names, up_corner_values):
            # Get corner in UFR position from UP face
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

            # Get corner in UFR position from DOWN face
            for i, pos in enumerate(down_corner_names):
                if is_sublist(corner_value, cube["D"][pos]):
                    self.cube.move("D", i+1)
                    self.cube.move("R", 1)
                    self.cube.move("D", -1)
                    self.cube.move("R", -1)

            # Rotate corner to correct orientation
            # UP face facing FRONT
            if self.cube.cube_dict["U"]["FR"][1] == "U":
                self.cube.move("R",  1)
                self.cube.move("D", -1)
                self.cube.move("R", -1)
                self.cube.move("D",  1)
                self.cube.move("R",  1)
                self.cube.move("D", -1)
                self.cube.move("R", -1)
            # UP face facing RIGHT
            elif self.cube.cube_dict["U"]["FR"][2] == "U":
                self.cube.move("F", -1)
                self.cube.move("D",  1)
                self.cube.move("F",  1)
                self.cube.move("D", -1)
                self.cube.move("F", -1)
                self.cube.move("D",  1)
                self.cube.move("F",  1)

            self.cube.move("UU", -1)

    """
        Solve the middle "crown"
    """
    def solve_second_row(self):
        for s1, s2 in zip(side_names, side_names_roll):
            # Get the piece down if it is in the middle row
            for i in range(4):
                if s1 in self.cube.cube_dict["F"]["R"] and s2 in self.cube.cube_dict["F"]["R"]:
                    self.__get_2nd_row_front_right__()
                self.cube.move("UU", -1)

            # Get the piece up from the down face
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

    """
        Create a cross in the DOWN face
    """
    def solve_second_cross(self):
        # First we make a list of the stickers in the down face
        down_stickers = [self.cube.cube_dict["D"][s][0] for s in side_names]

        # Now we check the shape these stickers make
        if all([s == "D" for s in down_stickers]):  # Cross is solved
            self.info["down_shape"] = "+"
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

    """
        Take the pieces on the down cross
        to their correct position
    """
    def orientate_2nd_cross(self):
        # Orientate down face
        reps = 0
        for _ in range(4):
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
        if reps == 4:  # Cross shape
            self.info["down_cross_coincidences"] = "+"
            return
        elif self.cube.cube_dict["U"]["B"][1] == self.cube.cube_dict["B"]["B"]:  # Line shape
            self.info["down_cross_coincidences"] = "-"
            self.__orientate_2nd_cross()
            self.cube.move("UU", -1)
        else:  # L shape
            self.info["down_cross_coincidences"] = "l"
        self.__orientate_2nd_cross()
        self.cube.move("U", 1)

    """
        Position the corners on the DOWN face
    """
    def solve_second_corners(self):
        # Count corners already solved
        coincidences = self.__count_coincidences__()
        self.info["2nd_corner_coincidences"] = coincidences
        self.info["iterations"] = 0

        while coincidences != 4:
            if coincidences == 1:
                # Rotate to get coincidence in the UFR corner
                for _ in range(4):
                    piece = self.cube.cube_dict["U"]["FR"]
                    if self.cube.cube_dict["F"]["F"] in piece and \
                       self.cube.cube_dict["R"]["R"] in piece:
                        break
                    self.cube.move("UU", 1)

            # Iterate the position of the corners and recount
            self.__iterate_second_corners__()
            coincidences = self.__count_coincidences__()

    """
        Change the orientation of the corners in the DOWN face
    """
    def orientate_2nd_corners(self):
        # Rotate corner by corner
        # Check if all corners are oriented
        while not all(self.cube.cube_dict["U"][c][0] == "D" for c in up_corner_names):
            # Get a non oriented corner in the UFR corner
            for i in range(4):
                if self.cube.cube_dict["U"]["FR"][0] != "D":
                    break
                self.cube.move("U", 1)

            # Apply series of moves
            self.__orientate_2nd_corners__()

        # Rotate UP face to it's correct orientation
        while self.cube.cube_dict["U"]["F"][1] != self.cube.cube_dict["F"]["F"]:
            self.cube.move("U", 1)

    """
        Rotate the cube to it's correct orientation
    """
    def reorient_cube(self):
        self.cube.move("FF", 2)
        for _ in range(4):
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


