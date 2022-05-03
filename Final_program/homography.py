# In here the picture will be taken, and the homography will be done
import cv2
import numpy as np
import os


def homography(qr_dim, workspace_width_x, workspace_length_y, pixiel_scale, path):
    # First the undistorted picture is imported and defined.
    img_un = cv2.imread(os.path.join(path, 'undistorted image.png'))

    # QR detection
    detection = cv2.QRCodeDetector()

    # Reading the information in the QR-codes, and the position of the corners in each of the QR codes.
    _, qr_nr, qr_coor, _ = detection.detectAndDecodeMulti(img_un)

    # Check for information, for error handling.
    # print("QR numbers")
    # print(qr_nr)
    # print("QR corner coordinates, same order as the QR numbers are show")
    # print(qr_coor)

    # Now the QR numbers and coordinates have to be set up in a matrix,
    # first a zero array is made to store the information
    qr_coor_new = np.zeros([4, 3])

    # Now the corner coordinate for each QR code are convert to center coordinates.
    for k in range(len(qr_nr)):
        qr_coor_new[k, 0] = int(str(qr_nr[k])[-1])
        for i in range(2):
            qr_coor_new[k, i + 1] = np.average(qr_coor[k, 0:4, i])

    # Check for information, for error handling.
    # print("matrix with the qr information")
    # print(qr_nr)

    # Now the coordinate has to be rearranged in the right order (QR1, QR2, QR3, QR4).
    qr_coor_new_order = qr_coor_new[qr_coor_new[:, 0].argsort()]

    # Check for information, for error handling.
    # print("sorted qr numbers, order 1,2,3 and 4")
    # print(qr_coor_new_order)

    # Now the coordinate destination for the homography, on the input image is defined.
    dst_coor = np.array([qr_coor_new_order[0, 1:3], qr_coor_new_order[1, 1:3], qr_coor_new_order[2, 1:3],
                         qr_coor_new_order[3, 1:3]])

    # Check for information, for error handling.
    # print("sorted qr numbers coordinates matrix, order 1,2,3 and 4")
    # print(dst_coor)

    # Now the real world dimensions are defined, by scaling the width and length between the qr code centers.
    src_y = (workspace_length_y - qr_dim) * pixiel_scale
    src_x = (workspace_width_x - qr_dim) * pixiel_scale

    # Now the plan for the homography is constructed, in the order 1,2,3 and 4
    src_coor = np.array([[0, 0], [0, src_y], [src_x, 0], [src_x, src_y]])

    # Then the output image size is increased so that the qr code are also in the picture
    qr_size = qr_dim * pixiel_scale
    src_coor_new = src_coor + int(qr_size / 2)

    # Check for information, for error handling.
    # print("src coordinates")
    # print(src_coor_new)

    # Now the homography is done
    h, _ = cv2.findHomography(dst_coor, src_coor_new)

    # Check for information, for error handling.
    # print("Homography matrix")
    # print(H)

    # Now the image is warp to the right perspective, and the picture saved.
    img_w = cv2.warpPerspective(img_un, h, (src_x + qr_size, src_y + qr_size))
    cv2.imwrite(os.path.join(path, 'Homography.png'), img_w)

    # Then a message is displayed
    return print('Homography done')
