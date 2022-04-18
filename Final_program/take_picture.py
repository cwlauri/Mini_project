# This function takes and save the picture, in the picture folder
import cv2
import os


def take_picture(path):
    # First a connection to the camera has to made, where a cap on the data stream is set.
    videoCaptureObject = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    # Then the dimensions for the picture is set
    videoCaptureObject.set(3, 1920)  # width=1920
    videoCaptureObject.set(4, 1080)  # height=1080

    # Then the data from the camera is read, and a picture is taken.
    ret, frame = videoCaptureObject.read()

    # Then the picture is saved in the pictures folder, with the input path set in the main script.
    cv2.imwrite(os.path.join(path, 'Original.png'), frame)

    # Then the connection to the camera is broken
    videoCaptureObject.release()

    return print("Picture taken")
