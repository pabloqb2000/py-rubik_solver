import cv2
import copy
import numpy as np
from util import *
from configs import *
from cube import Cube
from cube_3d import Cube3D
from simple_solver import *
from itertools import product
import matplotlib.pyplot as plt
from util import solved_cube_dict


def __detect_face__(frame, positions, r=detection_radius_def):
    """
        Take a picture of a face of the cube and extract the colors
        of the stickers in the face
    """

    # Get indices of the pixels around the given positions
    # All pixels at radius r from the given position are included
    idx = tuple(np.transpose(np.array([list(
            product(
                    range(y - r, y + r + 1),
                    range(x - r, x + r + 1),
                )
            ) for x, y in positions]),
        (2, 0, 1)))
    pixels = frame[idx]  # Get the pixel values at those positions
    color_means = np.mean(pixels, axis=1)  # Average the colors of the pixels around the position

    return color_means


def __take_pictures__(camera, positions):
    """
        Take pictures from the camera and extract the colors of the stickers
        by calling __detect_face__ on each picture
    """

    colors = [[255, 0, 0] for _ in range(9)]
    color_list = []

    while True:
        # Take frame
        ret, frame = camera.read()
        if not ret:
            print("Failed to take frame")
            exit()
        # Draw circles
        for pos, c in zip(positions, colors):
            cv2.circle(frame, pos, 20, (255, 255, 255), 8)
            cv2.circle(frame, pos, 20, c, 4)
        cv2.imshow("image", frame)

        # Keyboard response
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            # ESC pressed
            break
        elif k == 32:
            # SPACE pressed
            colors = __detect_face__(frame, positions)
            color_list.append(colors)

    return color_list


def __plot_3d_scatter_plot__(point_colors):
    """
        Show 3D scatter plot of the color points
        each point gets colored with it's color
    """
    point_colors_t = point_colors.T

    # Make plot
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter(*point_colors_t, s=100, c=point_colors / 255)
    ax.set_xlabel("R")
    ax.set_ylabel("G")
    ax.set_zlabel("B")
    plt.show()


def k_means(point_colors):
    """
        Classify the given colors in 6 clusters of 9 colors each
        First consider the middle face stickers as reference for each
        cluster, then assign the closest stickers to each cluster
        then compute the mean color of each cluster and repeat
    """

    # Extract the colors of the middle faces
    mean_colors = point_colors[np.arange(4, 4 + 9 * 6, 9)]
    closest_faces, counts = None, None

    for i in range(15):
        # Get the closest mean color for each sticker
        closest_faces = np.array([
            np.argmin(np.linalg.norm(mean_colors - sticker, axis=-1)) for sticker in point_colors
        ])

        # Recompute the mean color for each cluster
        mean_colors = np.array([
            np.mean(point_colors[closest_faces == j], axis=0) for j in range(6)
        ])

        # Count repetitions and break if necessary
        unique, counts = np.unique(closest_faces, return_counts=True)
        if len(counts) == 6 and all(counts == 9):
            print("Finished k-means in step:", i)
            break

    # Return error if not converged
    if not len(counts) == 6 or not all(counts == 9):
        return None, None
    return closest_faces, mean_colors


if __name__ == '__main__':
    get_new = True
    if get_new:
        # Start camera, windows and variables
        cam = cv2.VideoCapture(0)
        cv2.namedWindow("image")
        positions = np.load(r"saved_positions/position_01.npy")

        # Take pictures and get color info
        all_colors = __take_pictures__(cam, positions)

        # Close camera and window
        cam.release()
        cv2.destroyAllWindows()

        # Reformat to RGB
        all_colors = np.vstack(all_colors)
        all_colors[:, [0, 2]] = all_colors[:, [2, 0]]  # BGR to RGB

        # Show point clusters
        __plot_3d_scatter_plot__(all_colors)

        # If enough stickers where captured generate the cube
        if len(all_colors) != 9*6:
            print("Too many or too few stickers where captured, make sure to capture the six faces of the cube!")
            exit()

        np.save(r"all_colors_temp.tmp.npy", all_colors)
    else:
        all_colors = np.load(r"all_colors_temp.tmp.npy")

    # Apply k-means algorithm to classify the faces
    face_values, mean_colors = k_means(all_colors)
    if face_values is None:
        print("Couldn't classify colors correctly, you need to have consistent lighting conditions")
        exit()

    # Assign faces to a new cube dictionary
    cube_dict = copy.deepcopy(solved_cube_dict)
    cube_dict = assign_values(cube_dict, face_values)
    colors_dict = dict(zip(direction_names, array_to_vector(mean_colors/255)))
    cube = Cube3D(cube_dict, colors_dict=colors_dict)

    # Show solution
    # Create cube and generate solution
    cube_data = Cube(cube_dict=cube_dict, shuffle=False, record=False)
    cube_solver = SimpleSolver(cube_data)
    print("Solving")
    steps = cube_solver.solve()
    print("solved")

    # Make the moves
    for step in steps:
        print(step)
        cube.move(step)
