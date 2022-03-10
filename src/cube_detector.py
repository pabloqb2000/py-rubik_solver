from cubes.cube import Cube
from cubes.cube_3d import Cube3D
from cubes.cube_robot import CubeRobot
from cubes.cube_capture import CubeCapture
from solvers.simple_solver_2 import SimpleSolver2
from vpython import vector
from tqdm import tqdm
import os

# Initialize robot
cube_robot = CubeRobot(speed=1)
cube_robot.config['cool_down'] = 0.5
os.system('clear')
print("Cube initialized")

# Wait for user to introduce the cube
cube_robot.un_hold()
print("Introduce the cube and press ENTER", end=" ")
input()
cube_robot.hold()

# Detect cube with camera
cube_cap = CubeCapture(cube_robot=cube_robot, video_capture=0, debug=False)
cube_dict = cube_cap.capture_cube()

# Generate solution for the cube
print("Generating solution for the cube")
cube = Cube(cube_dict)
solver = SimpleSolver2(cube)
solution = solver.solve()
print("Solution found")

# Show solution
print("Display solution")
mean_colors = cube_cap.mean_colors/255
mean_colors = [mean_colors[0], *mean_colors[1:-1][::-1], mean_colors[-1]]
cube_3d = Cube3D(
    cube_dict, 
    move_time = 1,
    wait_time = 0.1,
    colors_dict = {f: vector(*c) for f, c in zip(cube_dict.keys(), mean_colors)}
)

# Make the moves on the physical cube
print("Making moves")
for move in tqdm(solution):
    cube_3d.move(move)
    cube_robot.move(move)