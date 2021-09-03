from cubes.cube_3d import *
from solvers.simple_solver import *


# Create cube and generate solution
cube = Cube(shuffle=True, record=False)
cube_3d = Cube3D(cube.cube_dict)
cube_solver = SimpleSolver(cube)
steps = cube_solver.solve()
print(cube.cube_dict)


"""
    Check the different stages of the simple_solver algorithm
"""
def run_checks():
    print("First cross solved:", all(cube_solver.cube.cube_dict["U"][pos] == ["U", pos] for pos in side_names))
    print("First corners position:", all(
        "U" in cube_solver.cube.cube_dict["U"][name] and
        name[0] in cube_solver.cube.cube_dict["U"][name] and
        name[1] in cube_solver.cube.cube_dict["U"][name]
        for name in up_corner_names))
    print("First corners rotation:", all(cube_solver.cube.cube_dict["U"][name] == ["U", name[0], name[1]]
                                         for name in up_corner_names))

    print("Second row position:", all(cube_solver.cube.cube_dict[s1][s2] == [s1, s2]
                                      for s1, s2 in zip(side_names, side_names_roll)))

    print("Down cross solved:", all(cube_solver.cube.cube_dict["D"][pos][0] == "D" for pos in side_names))
    print("Down cross solved:", all(cube_solver.cube.cube_dict["D"][pos] == ["D", pos] for pos in side_names))
    print("Second corners position:", all(
        "D" in cube_solver.cube.cube_dict["D"][name] and
        name[0] in cube_solver.cube.cube_dict["D"][name] and
        name[1] in cube_solver.cube.cube_dict["D"][name]
        for name in down_corner_names))

    print("CUBE SOLVED:", cube_solver.cube.is_solved())


run_checks()

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


