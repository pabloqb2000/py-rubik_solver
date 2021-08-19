from cube import *
from simple_solver import *
import numpy as np

n_cubes = 2000
times, n_steps, shapes, coincidences = [], [], [], []

for _ in range(n_cubes):
    cube = Cube(shuffle=True)
    solver = SimpleSolver(cube)
    steps = solver.solve()
    times.append(solver.info["time"])
    n_steps.append(solver.info["steps"])
    shapes.append(solver.info["down_shape"])
    coincidences.append(solver.info["down_cross_coincidences"])

times = np.array(times)
n_steps = np.array(n_steps)
shapes = np.array(shapes)
unique, counts = np.unique(shapes, return_counts=True)
shapes = dict(zip(unique, counts/n_cubes))
coincidences = np.array(coincidences)
unique, counts = np.unique(coincidences, return_counts=True)
coincidences = dict(zip(unique, counts/n_cubes))

print(f"Solved {n_cubes} cubes")
print("Average solving time {:.4f} ms".format(np.mean(times) * 1000))
print("Average solving steps {:.3f}".format(np.mean(n_steps)))
print("Shape ocurrencies in down cross:", shapes)
print("Shape coincidences in down cross:", coincidences)
