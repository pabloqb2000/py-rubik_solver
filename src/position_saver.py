import cv2
import numpy as np

mouse_clicks = []


def draw_circle(event, x, y, flags, param):
    global mouse_clicks
    if event == cv2.EVENT_LBUTTONDBLCLK:
        if len(mouse_clicks) < 9:
            mouse_clicks.append((x, y))
        else:
            mouse_clicks = mouse_clicks[1:] + [(x, y)]


cam = cv2.VideoCapture(0)
cv2.namedWindow("image")
cv2.setMouseCallback('image', draw_circle)

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    for pos in mouse_clicks:
        cv2.circle(frame, pos, 8, (255, 0, 0), 2)
    cv2.imshow("image", frame)

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        # ESC pressed
        break
    elif k == 32:
        # SPACE pressed
        if len(mouse_clicks) == 9:
            arr = np.array(mouse_clicks)
            np.save(r"saved_positions/position_01.npy", arr)
            print("Saved!")
        else:
            print("Not enough positions!")

cam.release()
cv2.destroyAllWindows()
