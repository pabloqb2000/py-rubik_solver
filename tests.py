from vpython import *
import numpy as np

floor = box (pos=vector(0,0,0), length=4, height=0.5, width=4, color=color.blue)
ball = sphere (pos=vector(0,4,0), radius=1, color=color.red)
ball.velocity = vector(0,-1,0)
dt = 0.01

while 1:
    rate(30)
    ball.pos = ball.pos + ball.velocity*dt
    if ball.pos.y < ball.radius:
        ball.velocity.y = abs(ball.velocity.y)
    else:
        ball.velocity.y = ball.velocity.y - 9.8*dt