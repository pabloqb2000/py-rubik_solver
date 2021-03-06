from cubes.cube import *
from cubes.util import run_checks
from solvers.simple_solver import *
from solvers.simple_solver_2 import *
import numpy as np

n_cubes = 2
print(f"Solving {n_cubes} cubes")

for Solver in [SimpleSolver, SimpleSolver2]:
    times, n_steps = [], []

    for _ in range(n_cubes):
        # Solve cube
        cube = Cube(shuffle=True)
        solver = Solver(cube)
        steps = solver.solve()

        # Validate solution
        cube.moves(steps)
        if not cube.is_solved():
            print("CUBE NOT SOLVED!")
            run_checks(cube.cube_dict)

        # Store data
        times.append(solver.info["time"])
        n_steps.append(solver.info["steps"])

    # Format data
    times = np.array(times)
    n_steps = np.array(n_steps)

    # Print data
    print(f"Solving algorithm {Solver.__name__}")
    print("Average solving time {:.4f} ms".format(np.mean(times) * 1000))
    print("Average solving steps {:.3f}".format(np.mean(n_steps)))

    print()
