from cubes.cube_robot import *
from time import sleep

cube_robot = CubeRobot(speed=1)
cube_robot.config['cool_down'] = 0.5
cube_robot.moves([
    random_move() for _ in range(3)
])
