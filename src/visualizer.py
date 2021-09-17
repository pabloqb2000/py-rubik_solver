from cubes.cube_3d import *
from cubes.util import run_checks
from solvers.simple_solver import SimpleSolver
from solvers.simple_solver_2 import SimpleSolver2


# Create cube and generate solution
cube = Cube(shuffle=True, record=False)
cube_3d = Cube3D(cube.cube_dict)
cube_solver = SimpleSolver2(cube)
steps = cube_solver.solve()

run_checks(cube_solver.cube.cube_dict)

# Wait
for i in range(fps_def * 5):
    rate(fps_def)

# Make the moves
for step in steps:
    print(step)
    cube_3d.move(step)

# Loop
while True:
    rate(fps_def)


