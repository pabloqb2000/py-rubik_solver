from cubes.util import *
from solvers.cube_solver import *
from solvers.simple_solver import *


def optimize_solution(solution):
    """
        Eliminate moves which have a full rotation (N % 4 = 0)
        since full rotations don't have any effects in the cube
        also if two consecutive moves are made in the same direction
        this moves are mixed in one move
    """
    i = 0
    while i < len(solution):
        dir, n = solution[i]

        if n % 4 == 0:
            solution = solution[:i] + solution[i+1:]
            i -= 1
        elif i + 1 < len(solution):
            dir2, n2 = solution[i+1]
            
            if dir == dir2:
                solution = solution[:i] + [(dir, (n + n2) % 4)] + solution[i+2:]
            else:
                i += 1
        else:
            i += 1

    return solution


class SimpleSolver2(SimpleSolver):
    """
        Improved version of SimpleSolver
        it uses the same technique but some
        of the steps are optimized so found
        solutions have less moves
    """
    def __solve_cube__(self):
        solution = super().__solve_cube__()
        return optimize_solution(solution)
