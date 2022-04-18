# This function wil find the rotation, position and color of the DUPLO bricks or from now call blocks.

from collections import deque
import cv2
import os
import numpy as np


def vision(qr_dim, pixel_scale, path):
    # First the homography picture is imported from the picture folder, and defined.
    img_H = cv2.imread(os.path.join(path, 'Homography.png'))

    # Converting the picture from RGB to HSV spectrum, and saving the picture in the picture folder
    img_HSV = cv2.cvtColor(img_H, cv2.COLOR_BGR2HSV)
    cv2.imwrite(os.path.join(path, 'Picture in HSV.png'), img_HSV)

    # Defining kernel for morphology
    kernel = np.ones((10, 10), np.uint8)

    # Then the HSV picture is imported
    img = cv2.imread(os.path.join(path, 'Picture in HSV.png'))

    # Defining upper and lower bound of all the colors,
    # HSV -> (hue, saturation, value) and in python it is (H/2, (S/100) * 255, (V/100) * 255)
    # Orange
    u_b_o = (12, 255, 255)
    l_b_o = (0, 100, 100)

    # Yellow
    u_b_y = (24, 255, 255)
    l_b_y = (14, 100, 100)

    # Blue
    u_b_b = (150, 255, 255)
    l_b_b = (50, 100, 100)

    # Green
    u_b_g = (40, 255, 255)
    l_b_g = (32, 100, 30)

    # Black
    u_b_bl = (180, 255, 80)
    l_b_bl = (0, 0, 0)

    # Now each color blocks are isolated.
    # Orange
    bin_o = cv2.inRange(img, l_b_o, u_b_o)
    bin_o_c = cv2.morphologyEx(bin_o, cv2.MORPH_CLOSE, kernel)
    bin_o_c_o = cv2.morphologyEx(bin_o_c, cv2.MORPH_OPEN, kernel)

    # Save picture with isolated block for the color orange, for error handling.
    # cv2.imwrite("Orange.png", bin_o_c_o)

    # Yellow
    bin_y = cv2.inRange(img, l_b_y, u_b_y)
    bin_y_c = cv2.morphologyEx(bin_y, cv2.MORPH_CLOSE, kernel)
    bin_y_c_o = cv2.morphologyEx(bin_y_c, cv2.MORPH_OPEN, kernel)

    # Save picture with isolated block for the color yellow, for error handling.
    # cv2.imwrite("Yellow.png", bin_y_c_o)

    # Blue
    bin_b = cv2.inRange(img, l_b_b, u_b_b)
    bin_b_c = cv2.morphologyEx(bin_b, cv2.MORPH_CLOSE, kernel)
    bin_b_c_o = cv2.morphologyEx(bin_b_c, cv2.MORPH_OPEN, kernel)

    # Save picture with isolated block for the color blue, for error handling.
    # cv2.imwrite("Blue.png", bin_b_c_o)

    # Green
    bin_g = cv2.inRange(img, l_b_g, u_b_g)
    bin_g_c = cv2.morphologyEx(bin_g, cv2.MORPH_CLOSE, kernel)
    bin_g_c_o = cv2.morphologyEx(bin_g_c, cv2.MORPH_OPEN, kernel)

    # Save picture with isolated block for the color green, for error handling.
    # cv2.imwrite("Green.png", bin_g_c_o)

    # And for the color black the QR codes has to be deleted, this is done by isolating the specific indexes in the
    # picture array where the QR codes are and setting there value to 0.

    # Fist we isolate everything that is black .
    bin_bl = cv2.inRange(img, l_b_bl, u_b_bl)
    bin_bl_c = cv2.morphologyEx(bin_bl, cv2.MORPH_CLOSE, kernel)
    bin_bl_c_o = cv2.morphologyEx(bin_bl_c, cv2.MORPH_OPEN, kernel)

    # Then the shape of the image is found.
    img_shape = bin_bl_c_o.shape

    # Check information, for error handling.
    # print(img_shape)
    # print(img_shape[1])

    # Defining the QR dimension, where 30 is added to make sure that the Whole QR code is deleted,
    # this is 3 mm in real dimensions.
    qr_size = (qr_dim * pixel_scale) + 30

    # Now the index values for different QR codes to 0, one at the time.
    # QR code 1
    bin_bl_c_o[0:qr_size, 0:qr_size] = 0

    # QR code 2
    bin_bl_c_o[0:qr_size, (img_shape[1] - qr_size):img_shape[1]] = 0

    # QR code 3
    bin_bl_c_o[(img_shape[0] - qr_size):img_shape[0], 0:qr_size] = 0

    # QR code 4
    bin_bl_c_o[(img_shape[0] - qr_size):img_shape[0], (img_shape[1] - qr_size):img_shape[1]] = 0

    # Save picture with isolated block for the color black, for error handling.
    # cv2.imwrite("black.png", bin_bl_c_o)

    # Then isolated blocks are added together in one matrix/picture.
    bin_all = bin_o_c_o + bin_y_c_o + bin_b_c_o + bin_g_c_o + bin_bl_c_o

    # Then the binary picture is saved in the pictures folder.
    cv2.imwrite(os.path.join(path, 'Binary image without background.png'), bin_all)

    # ---------------------Finding the center coordinates, rotation and color----------------------------------------

    # Now the position and rotation of the blocks are found
    # First the binary picture that was just found is load in and defined.
    img_c_r = cv2.imread(os.path.join(path, 'Binary image without background.png'), cv2.IMREAD_GRAYSCALE)

    # Find all the contours in the threshold image
    contours, _ = cv2.findContours(img_c_r, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Then two deque are created, to save the values for each interation of the for loop.
    queue_rotation = deque()
    queue_c_coor = deque()

    # Now a for loop is set up to go through all the block contours.
    for i, c in enumerate(contours):

        # Calculate the area of each contour
        area = cv2.contourArea(c)

        # Ignore contours that are too small or too large
        if area < 10000 or 10000000000 < area:
            continue

        # cv.minAreaRect returns:
        # (center(x, y), (width, height), angle of rotation) = cv2.minAreaRect(c)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Retrieve the key parameters of the rotated bounding box
        center = (round(rect[0][0], 2), round(rect[0][1]), 2)
        width = round(rect[1][0], 2)
        height = round(rect[1][1], 2)
        angle = round(rect[2], 2)

        # Here the right anlges are defined.
        if width < height:
            angle = 180 - angle
        else:
            angle = 90 - angle

        # Save the values in the deques.
        queue_c_coor.append(center)
        queue_rotation.append(angle)

        # To make a picture that displays the rotation for error handling, the values have to be integers.
        center_1 = (int(rect[0][0]), int(rect[0][1]))

        # Then a picture is set up, which shows the outline of the block contours and their rotation.
        label = "  Rotation Angle: " + str(angle) + " degrees"
        cv2.putText(img_c_r, label, (center_1[0] - 50, center_1[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.drawContours(img_c_r, [box], 0, (0, 0, 255), 2)

        # This picture is saved, in the picture folder.
        cv2.imwrite(os.path.join(path, 'rotation_test_pic.png'), img_c_r)

    # Check information for center points and rotation.
    # print(queue_c_coor)
    # print(queue_rotation)

    # Then the two deque are defined as np arrays.
    rotation = np.array(queue_rotation)
    center_coor = np.array(queue_c_coor)

    # Check information for center points and rotation.
    # print(center_coor)
    # print(rotation)

    # Then the desired matrix with (x,y,angel) is set up, and saved in the block matrix.
    # First for the x,y center coordinates.
    block_matrix = np.zeros([len(rotation), 4])
    for k in range(len(rotation)):
        for i in range(2):
            block_matrix[(k - 1), i] = round(center_coor[(k - 1), i], 2)

    # Then the rotation.
    for k in range(len(rotation)):
        for i in range(1):
            block_matrix[(k - 1), (i + 2)] = round(rotation[(k - 1)], 2)

    # Then the color for each block has to be found.
    # First the HSV picture is import.
    img_color = cv2.imread(os.path.join(path, 'Picture in HSV.png'))

    # The color for each block is found by finding the center of the brick and find the color in a square around
    # that point. This is done for each detected block, in a for loop. Where the range is found through the number
    # of rotation values.
    for k in range(len(rotation)):
        # First the x and y values from the Block matrix is put into np arrays.
        coord_x = np.array((block_matrix[(k - 1), 0]))
        coord_y = np.array((block_matrix[(k - 1), 1]))

        # Then the values are saved as integers.
        coord_x_new = np.array(coord_x.astype(int))
        coord_y_new = np.array(coord_y.astype(int))

        # Then an array is made which hold both the x and y values.
        center_coor_new = np.array([coord_y_new, coord_x_new])

        # Then a square in the middle of each block is made, to find the color of the square.
        color = np.array(img_color[center_coor_new[0] - 25:center_coor_new[0] + 25,
                         center_coor_new[1]:center_coor_new[1] + 25])

        # All the values in these squares are averaged, to find a more reliable value.
        color_new = np.mean(color, axis=(0, 1))

        # The color values are divided into color_int_1 = hue, color_int_2 saturation, color_int_3 value.
        color_int_1 = int(color_new[0])
        color_int_2 = int(color_new[1])
        color_int_3 = int(color_new[2])

        # Display values for error handling.
        # print(center_coor_new)
        # print(color)
        # print(color_int_1,color_int_2,color_int_3)

        # Then an if loop is set up that goes through each block and checks if the color value is inbetween the defined
        # color thresholds.
        if l_b_g[0] <= color_int_1 <= u_b_g[0] and \
                l_b_g[1] <= color_int_2 <= u_b_g[1] and \
                l_b_g[2] <= color_int_3 <= u_b_g[2]:
            # Then, if the found average color is inbetween the threshold, the color value in the block matrix is set
            # to a color specific value. This is done for all the different colors types and threshold.
            block_matrix[(k - 1), 3] = 1  # ("Green")

        elif l_b_b[0] <= color_int_1 <= u_b_b[0] and \
                l_b_b[1] <= color_int_2 <= u_b_b[1] and \
                l_b_b[2] <= color_int_3 <= u_b_b[2]:
            block_matrix[(k - 1), 3] = 2  # ("Blue")

        elif l_b_y[0] <= color_int_1 <= u_b_y[0] and \
                l_b_y[1] <= color_int_2 <= u_b_y[1] and \
                l_b_y[2] <= color_int_3 <= u_b_y[2]:
            block_matrix[(k - 1), 3] = 3  # ("Yellow")

        elif l_b_o[0] <= color_int_1 <= u_b_o[0] and \
                l_b_o[1] <= color_int_2 <= u_b_o[1] and \
                l_b_o[2] <= color_int_3 <= u_b_o[2]:
            block_matrix[(k - 1), 3] = 4  # ("Orange")

        elif l_b_bl[0] <= color_int_1 <= u_b_bl[0] and \
                l_b_bl[1] <= color_int_2 <= u_b_bl[1] and \
                l_b_bl[2] <= color_int_3 <= u_b_bl[2]:
            block_matrix[(k - 1), 3] = 5  # ("Black")

    # Display block matrix for error handling.
    # print(block_matrix)

    # Then when the vision part is done a message is displayed, and the Block matrix is returned
    print('Vision part done')
    return block_matrix
