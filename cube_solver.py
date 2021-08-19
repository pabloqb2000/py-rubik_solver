from time import time


class CubeSolver:
    """
        Initialize the solver
        copy the cube if necessary
    """
    def __init__(self, cube, copy=True):
        self.cube = cube.copy() if copy else cube
        self.info = {}

    """
        Solve the cube
        return a list of the steps for the solution
    """
    def solve(self):
        t0 = time()
        steps = self.__solve_cube__()
        t1 = time()

        if not self.cube.is_solved():
            print("Unable to solve cube")

        self.info["time"] = t1 - t0
        self.info["steps"] = len(steps)

        return steps

    """
        Abstract function for solving the cube
    """
    def __solve_cube__(self):
        return [], {}

