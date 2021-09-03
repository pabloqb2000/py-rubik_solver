from cube import *
from simple_solver import *
import numpy as np

n_cubes = 2000
times, n_steps, shapes, coincidences, corners_coincidences, iterations = [], [], [], [], [], []

for _ in range(n_cubes):
    # Solve cube
    cube = Cube(shuffle=True)
    solver = SimpleSolver(cube)
    steps = solver.solve()

    # Store data
    times.append(solver.info["time"])
    n_steps.append(solver.info["steps"])
    shapes.append(solver.info["down_shape"])
    coincidences.append(solver.info["down_cross_coincidences"])
    corners_coincidences.append(solver.info["2nd_corner_coincidences"])
    iterations.append(solver.info["iterations"])

# Format data
times = np.array(times)
n_steps = np.array(n_steps)
shapes = np.array(shapes)
unique, counts = np.unique(shapes, return_counts=True)
shapes = dict(zip(unique, counts/n_cubes))
coincidences = np.array(coincidences)
unique, counts = np.unique(coincidences, return_counts=True)
coincidences = dict(zip(unique, counts/n_cubes))
corners_coincidences = np.array(corners_coincidences)
unique, counts = np.unique(corners_coincidences, return_counts=True)
corners_coincidences = dict(zip(unique, counts/n_cubes))
iterations = np.array(iterations)
unique, counts = np.unique(iterations, return_counts=True)
iterations = dict(zip(unique, counts/n_cubes))

# Print data
print(f"Solved {n_cubes} cubes")
print("Average solving time {:.4f} ms".format(np.mean(times) * 1000))
print("Average solving steps {:.3f}".format(np.mean(n_steps)))
print("Shape ocurrencies in down cross:", shapes)
print("Shape coincidences in down cross:", coincidences)
print("2nd corner coincidences", corners_coincidences)
print("iterations", iterations)
