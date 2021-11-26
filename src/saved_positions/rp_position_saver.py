import cv2
import numpy as np

cam = cv2.VideoCapture(0)
ret, frame = cam.read()
cam.release()

mouse_clicks = np.load(r'saved_positions/position_01.npy')

for pos in mouse_clicks:
    cv2.circle(frame, pos, 8, (255, 0, 0), 2)

cv2.imwrite("temp.jpg", frame)
