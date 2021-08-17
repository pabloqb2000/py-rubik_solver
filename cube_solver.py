from time import time


class CubeSolver:
    def __init__(self, cube):
        self.cube = cube

    def solve(self):
        t0 = time()
        steps = self.__solve_cube__()
        t1 = time()

        if self.cube.is_solved():
            print("CUBE SOLVED!!")
            print("Solved in {:.2f} seconds".format(t1 - t0))
            print(f"Solution has {len(steps)} steps")
        else:
            print("Unable to solve cube")

        return steps

    def __solve_cube__(self):
        return []

