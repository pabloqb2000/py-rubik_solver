from cube import *
from simple_solver import *
import numpy as np

n_cubes = 2000
times, n_steps = [], []
for _ in range(n_cubes):
    cube = Cube(shuffle=True)
    solver = SimpleSolver(cube)
    steps = solver.solve()
    times.append(solver.info["time"])
    n_steps.append(solver.info["steps"])
times = np.array(times)
n_steps = np.array(n_steps)

print(f"Solved {n_cubes} cubes")
print("Average solving time {:.4f} ms".format(np.mean(times) * 1000))
print("Average solving steps {:.3f}".format(np.mean(n_steps)))
