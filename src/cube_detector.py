from cubes.cube_robot import CubeRobot
from cubes.cube_capture import CubeCapture

cube_robot = CubeRobot(speed=1)
cube_robot.config['cool_down'] = 0.5
cube_cap = CubeCapture(cube_robot=cube_robot)

cube_dict = cube_cap.capture_cube()
