from cubes.cube_robot import *
import numpy as np
from time import sleep

cube_robot = CubeRobot(speed=1)
cube_robot.config['cool_down'] = 0.5

cube_robot.un_hold()
for s in np.arange(0.2, 0.5, 0.05):
    print(s)
    cube_robot.config['flip_speed'] = s
    for _ in range(10):
        cube_robot.flip()
    sleep(1)
cube_robot.holder()
