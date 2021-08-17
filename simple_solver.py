from util import *
from cube_solver import *


class SimpleSolver(CubeSolver):
    def __solve_cube__(self):
        self.cube.moves_made = []
        self.cube.record = True

        self.solve_first_cross()
        self.solve_first_corners()

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

            self.cube.move("UU", -1)



