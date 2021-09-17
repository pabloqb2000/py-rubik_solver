from cubes.util import *
from solvers.cube_solver import *
from solvers.simple_solver import *


def eliminate_rotations(solution):
    """
        This function looks for the steps that involve a rotation of the whole cube
        (UU, FF, RR moves) and translates the following moves to account for this rotation
        so that the rotation is no longer necessary
    """
    rotations = ["UU", "FF", "RR"]
    translate_dict = {dir: dir for dir in direction_names + rotations}
    new_solution = []

    for dir, n in solution:
        if dir in rotations:
            for _ in range(n % 4):
                translate_dict = new_translation(dir, translate_dict)
        else:
            new_solution.append((translate_dict[dir], n))

    return new_solution


def new_translation(dir, translate_dict):
    """
        Auxiliary function for the eliminate rotations function
        it returns the appropriate update for the translation dictionary
        given a rotation
    """
    new_translate_dict = translate_dict.copy()
    if dir == "UU":
        new_translate_dict["F"] = translate_dict["L"]
        new_translate_dict["R"] = translate_dict["F"]
        new_translate_dict["B"] = translate_dict["R"]
        new_translate_dict["L"] = translate_dict["B"]
        new_translate_dict["FF"] = translate_dict["RR"]
        new_translate_dict["RR"] = translate_dict["FF"]
    elif dir == "FF":
        new_translate_dict["U"] = translate_dict["R"]
        new_translate_dict["L"] = translate_dict["U"]
        new_translate_dict["D"] = translate_dict["L"]
        new_translate_dict["R"] = translate_dict["D"]
        new_translate_dict["RR"] = translate_dict["UU"]
        new_translate_dict["UU"] = translate_dict["RR"]
    elif dir == "RR":
        new_translate_dict["U"] = translate_dict["B"]
        new_translate_dict["F"] = translate_dict["U"]
        new_translate_dict["D"] = translate_dict["F"]
        new_translate_dict["B"] = translate_dict["D"]
        new_translate_dict["UU"] = translate_dict["FF"]
        new_translate_dict["FF"] = translate_dict["UU"]
    return new_translate_dict


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
            solution.pop(i)
            i -= 1
        elif i + 1 < len(solution):
            dir2, n2 = solution[i+1]
            
            if dir == dir2:
                solution[i] = (dir, (n + n2) % 4)
                solution.pop(i+1)
            else:
                i += 1
        else:
            break

    return solution


class SimpleSolver2(SimpleSolver):
    """
        Improved version of SimpleSolver
        it uses the same technique but some
        of the steps are optimized so found
        solutions with fewer moves
    """
    def __solve_cube__(self):
        solution = super().__solve_cube__()
        s_t = solution.copy()
        solution = eliminate_rotations(solution)
        '''for s, s2 in zip(solution, s_t):
            print(s, s2)
        for s in s_t[len(solution):]:
            print(s)'''
        solution = optimize_solution(solution)
        return solution
