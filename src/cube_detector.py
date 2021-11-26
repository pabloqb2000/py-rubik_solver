from cubes.cube import Cube
from cubes.cube_robot import CubeRobot
from cubes.cube_capture import CubeCapture
from solvers.simple_solver_2 import SimpleSolver2
from tqdm import tqdm

cube_robot = CubeRobot(speed=1)
cube_robot.config['cool_down'] = 0.5
cube_cap = CubeCapture(cube_robot=cube_robot, video_capture=0)

cube_dict = cube_cap.capture_cube()

cube_robot.hold()
print(cube_dict)
print(repr(cube_dict))

cube = Cube(cube_dict)
solver = SimpleSolver2(cube)
solution = solver.solve()

for move in tqdm(solution):
    cube_robot.move(move)