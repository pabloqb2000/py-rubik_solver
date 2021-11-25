# from cubes.cube_robot import CubeRobot
from cubes.cube_capture import CubeCapture

cube_robot = None
cube_cap = CubeCapture(cube_robot=cube_robot)

cube_cap.capture_cube()
