from time import sleep
from cubes.util import *
from cubes.configs import *
from solvers.simple_solver import *
import matplotlib.pyplot as plt
from itertools import product
import numpy as np
import copy
import cv2

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
        print(counts)
        return None, None
    return closest_faces, mean_colors

class CubeCapture:
    """
        Class for generating a cube object by rotating a physical cube
        and taking photos with a webcam
    """

    def __init__(self, cube_robot, video_capture=0):
        self.cube_robot = cube_robot
        self.n_video_capture = video_capture
        self.pos = np.load(r"saved_positions/position_01.npy")
        self.i = 0

    def take_face_pictures(self):
        color_list = []

        # Detect UP face
        color_list.append(self.__detect_face__())

        # Detect LEFT face
        self.cube_robot.flip()
        color_list.append(self.__detect_face__())

        # Detect FRONT face
        self.cube_robot.move_plate(1)
        self.cube_robot.flip()
        color_list.append(self.__detect_face__())

        # Detect RIGHT face
        self.cube_robot.flip()
        color_list.append(self.__detect_face__())

        # Detect BACK face
        self.cube_robot.flip()
        color_list.append(self.__detect_face__())

        # Detect DOWN face
        self.cube_robot.move_plate(-1)
        self.cube_robot.flip()
        color_list.append(self.__detect_face__())

        # Restore
        self.cube_robot.flip()
        self.cube_robot.flip()
        self.cube_robot.move_plate(1)


        # Reformat to RGB
        color_list = np.vstack(color_list)
        color_list[:, [0, 2]] = color_list[:, [2, 0]]  # BGR to RGB
        return color_list

    def __detect_face__(self, r=detection_radius_def):
        """
            Take a picture of a face of the cube and extract the colors
            of the stickers in the face
        """
        sleep(0.5)
        self.vc = cv2.VideoCapture(self.n_video_capture)
        ret, frame = self.vc.read()
        if not ret:
            print("Failed to take frame")
            exit()
        cv2.imwrite(f"temp{self.i}.jpg", frame)
        self.i += 1
        self.vc.release()

        # Get indices of the pixels around the given positions
        # All pixels at radius r from the given position are included
        idx = tuple(np.transpose(np.array([list(
                product(
                        range(y - r, y + r + 1),
                        range(x - r, x + r + 1),
                    )
                ) for x, y in self.pos]),
            (2, 0, 1)))
        pixels = frame[idx]  # Get the pixel values at those positions
        color_means = np.mean(pixels, axis=1)  # Average the colors of the pixels around the position

        return color_means

    def get_cube_dict(self, values):
        c = copy.deepcopy(solved_cube_dict)
        dir_name = ['U', 'L', 'F', 'R', 'B', 'D']

        c["U"]["RB"][0] = dir_name[values[0]]
        c["U"]["R"][0]  = dir_name[values[1]]
        c["U"]["FR"][0] = dir_name[values[2]]
        c["U"]["B"][0]  = dir_name[values[3]]
        c["U"]["U"]     = dir_name[values[4]]
        c["U"]["F"][0]  = dir_name[values[5]]
        c["U"]["BL"][0] = dir_name[values[6]]
        c["U"]["L"][0]  = dir_name[values[7]]
        c["U"]["LF"][0] = dir_name[values[8]]

        c["U"]["BL"][2] = dir_name[values[9]]
        c["U"]["L"][1]  = dir_name[values[10]]
        c["U"]["LF"][1] = dir_name[values[11]]
        c["B"]["L"][1]  = dir_name[values[12]]
        c["L"]["L"]     = dir_name[values[13]]
        c["L"]["F"][0]  = dir_name[values[14]]
        c["D"]["BL"][2] = dir_name[values[15]]
        c["D"]["L"][1]  = dir_name[values[16]]
        c["D"]["LF"][1] = dir_name[values[17]]

        c["D"]["LF"][2] = dir_name[values[18]]
        c["L"]["F"][1]  = dir_name[values[19]]
        c["U"]["LF"][2] = dir_name[values[20]]
        c["D"]["F"][1]  = dir_name[values[21]]
        c["F"]["F"]     = dir_name[values[22]]
        c["U"]["F"][1]  = dir_name[values[23]]
        c["D"]["FR"][1] = dir_name[values[24]]
        c["F"]["R"][0]  = dir_name[values[25]]
        c["U"]["FR"][1] = dir_name[values[26]]

        c["D"]["FR"][2] = dir_name[values[27]]
        c["F"]["R"][1]  = dir_name[values[28]]
        c["U"]["FR"][2] = dir_name[values[29]]
        c["D"]["R"][1]  = dir_name[values[30]]
        c["R"]["R"]     = dir_name[values[31]]
        c["U"]["R"][1]  = dir_name[values[32]]
        c["D"]["RB"][1] = dir_name[values[33]]
        c["R"]["B"][0]  = dir_name[values[34]]
        c["U"]["RB"][1] = dir_name[values[35]]

        c["D"]["RB"][2] = dir_name[values[36]]
        c["R"]["B"][1]  = dir_name[values[37]]
        c["U"]["RB"][2] = dir_name[values[38]]
        c["D"]["B"][1]  = dir_name[values[39]]
        c["B"]["B"]     = dir_name[values[40]]
        c["U"]["B"][1]  = dir_name[values[41]]
        c["D"]["BL"][1] = dir_name[values[42]]
        c["B"]["L"][0]  = dir_name[values[43]]
        c["U"]["BL"][1] = dir_name[values[44]]

        c["D"]["RB"][0] = dir_name[values[45]]
        c["D"]["B"][0]  = dir_name[values[46]]
        c["D"]["BL"][0] = dir_name[values[47]]
        c["D"]["R"][0]  = dir_name[values[48]]
        c["D"]["D"]     = dir_name[values[49]]
        c["D"]["L"][0]  = dir_name[values[50]]
        c["D"]["FR"][0] = dir_name[values[51]]
        c["D"]["F"][0]  = dir_name[values[52]]
        c["D"]["LF"][0] = dir_name[values[53]]

        return c

    def __plot_3d_scatter_plot__(self, point_colors):
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

    def capture_cube(self):
        self.cube_robot.un_hold()
        color_list = self.take_face_pictures()

        self.__plot_3d_scatter_plot__(color_list)

        face_values, mean_colors = k_means(color_list)
        if face_values is None:
            print("Couldn't classify colors correctly, you need to have consistent lighting conditions")
            exit()

        return self.get_cube_dict(face_values)
