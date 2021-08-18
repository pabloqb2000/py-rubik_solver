from time import time


class CubeSolver:
    def __init__(self, cube, copy=True):
        self.cube = cube.copy() if copy else cube
        self.info = {}

    def solve(self):
        t0 = time()
        steps, info = self.__solve_cube__()
        t1 = time()

        if not self.cube.is_solved():
            print("Unable to solve cube")

        self.info = {
            "time": t1 - t0,
            "steps": len(steps),
            "sol_info": info,
        }

        return steps

    def __solve_cube__(self):
        return [], {}

