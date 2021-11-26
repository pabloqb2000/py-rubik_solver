from cubes.cube import Cube
from cubes.cube_robot import CubeRobot
from cubes.cube_capture import CubeCapture
from solvers.simple_solver_2 import SimpleSolver2
from tqdm import tqdm
import os

# Initialize robot
cube_robot = CubeRobot(speed=1)
cube_robot.config['cool_down'] = 0.5
os.system('clear')
print("Cube initialized")

# Detect cube with camera
cube_cap = CubeCapture(cube_robot=cube_robot, video_capture=0)
cube_dict = cube_cap.capture_cube()

# Generate solution for the cube
print("Generating solution for the cube")
cube = Cube(cube_dict)
solver = SimpleSolver2(cube)
solution = solver.solve()
print("Solution found")

# Make the moves on the physical cube
print("Making moves")
for move in tqdm(solution):
    cube_robot.move(move)