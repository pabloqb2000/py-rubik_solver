from itertools import product
from solvers.cube_solver import *
from solvers.iddfs import *
from cubes.util import *


def get_children_from_cube(cube, moves):
    """
        Generate new copies from the actual cube by applying the given moves
        moves that rotate the last moved face are not taken into consideration
        also moves that are commutative are discarded
    """
    if len(cube.moves_made) > 1:
        last_move, _ = cube.moves_made[-1]
        return (
            cube.copy().move((mov, n))
            for mov, n in moves
            if not (mov == last_move or (opposite_face[mov] == last_move and (n > 2 or mov in prioritary_faces)))
        )
    else:
        return (cube.copy().move(mov) for mov in moves)


def test_group1(cube):
    return True


def test_group2(cube):
    return True


def test_group3(cube):
    return True


class ThistlethwaiteSolver(CubeSolver):
    """
        ThistlethwaiteSolver uses Thistlethwaite's algorithm to solve the rubik's cube
        an explanation of this algorithm can be found in any of this pages:
            https://medium.com/@benjamin.botto/implementing-an-optimal-rubiks-cube-solver-using-korf-s-algorithm-bf750b332cf9
            https://math.stackexchange.com/questions/1362471/rubiks-cube-thistlethwaite-four-phase-algorithm
            https://www.jaapsch.net/puzzles/thistle.htm
        But basically, it works by using IDDFS to find a series of moves which move the cube to a group of cube states
        that can be solved with fewer moves. Since from that state fewer moves are needed the branching factor gets
        reduced and IDDFS can be used to take the cube to an even easier group of cube states until the cube is solved.
    """

    def __solve_cube__(self):
        cube = self.cube.copy()
        cube.record = True

        # cube, n = iddfs(cube, test_group1, lambda c: get_children_from_cube(c, product(direction_names, (1, 2, 3))))
        # cube, n = iddfs(cube, test_group2, lambda c: get_children_from_cube(c, product(direction_names, (1, 2, 3))))
        # cube, n = iddfs(cube, test_group3, lambda c: get_children_from_cube(c, product(direction_names, (1, 2, 3))))
        cube, n = iddfs(cube, lambda c: c.is_solved(), lambda c: get_children_from_cube(c, product(direction_names, (1, 2, 3))))

        self.cube.moves(cube.moves_made)
        return cube.moves_made
