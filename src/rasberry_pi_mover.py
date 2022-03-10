from cubes.cube_robot import *
import numpy as np
from cubes.util import random_move
from time import sleep

cube_robot = CubeRobot(speed=1)
cube_robot.config['cool_down'] = 0.5

# cube_robot.un_hold()
cube_robot.holding = True
for s in [0.05]:# np.arange(0.05, 0.2, 0.05):
    print(s)
    cube_robot.config['flip_speed'] = s
    for _ in range(10):
        cube_robot.move(random_move())
    sleep(1)

