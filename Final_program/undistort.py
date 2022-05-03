# This function undistorted the taken picture
import cv2
import numpy as np
import os


def undistort(path):
    # First the picture is called and defined.
    img = cv2.imread(os.path.join(path, 'Original.png'))

    # Then from the camera calibration done in Matlab, the values for undistorting the picture is defined, a more
    # detailed discretion of each of these intrinsic values is found in the report.
    ca_matrix = np.array([[1458.44479595608, 0, 945.728710457185],
                          [0, 1449.70998748913, 530.376541819689],
                          [0, 0, 1]])

    distortion_co = np.array([0.0358131336238750, -0.149379521755432, 0, 0, 0])

    # Then the picture is undistorted, by using the intrinsic values and the picture taking in function(take_picture).
    und_img = cv2.undistort(img, ca_matrix, distortion_co)

    # Then the picture is saved in the pictures folder, with the input path defined in the main script.
    cv2.imwrite(os.path.join(path, 'undistorted image.png'), und_img)

    # A message is displayed.
    return print("Picture undistorted")
