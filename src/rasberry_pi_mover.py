from cubes.cube_robot import *
from time import sleep

cube_robot = CubeRobot(speed=1)
cube_robot.config['cool_down'] = 0.5

for _ in range(20):
    move, n = random_move()
    print(move, n)
    cube_robot.move((move, n))
print(repr(cube_robot.face_orientations))
