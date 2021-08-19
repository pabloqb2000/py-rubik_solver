from vpython import color, vector

'''
    Colors
'''
bg_color = color.black
base_color = color.gray(0.4)
colors_dict = {
    "U": color.white,
    "F": color.red,
    "R": color.blue,
    "B": color.orange,
    "L": color.green,
    "D": color.yellow,
}

'''
    Sizes
'''
box_margin = 0.15
box_height = 0.2

'''
    Times
'''
fps_def = 30
move_time_def = 2
wait_time_def = 0.8
speed = 20

move_time_def /= speed
wait_time_def /= speed
