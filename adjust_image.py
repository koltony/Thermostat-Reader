import cv2
import my_utilities
import numpy as np

def addroi():
    global rectPoints, image , th, lw, bh, rw
    if len(rectPoints) == 2:
        (th, lw), (bh, rw) = rectPoints
        if th > bh:
            temp = bh
            bh = th
            th = temp
            temp = lw
            lw = rw
            rw = temp

        rectPoints = []


def click(event, x, y, flags, param):
    # Accessing global variables
    global rectPoints

    if event == cv2.EVENT_LBUTTONUP:
        # adding (x, y) coordinates to the list
        rectPoints.append((x, y))
        print(rectPoints)
        # Drawing a marker
        cv2.drawMarker(image, (x, y), (0, 255, 0), cv2.MARKER_CROSS)
        cv2.imshow('Delimit region of interest', image)
        addroi()

def mainROI(img):
    global rectPoints, image, clone

    rectPoints = []
    image = img
    clone = img.copy()
    cv2.namedWindow('Delimit region of interest')
    cv2.setMouseCallback('Delimit region of interest', click)

    while True:

        cv2.imshow('Delimit region of interest', image)
        key = cv2.waitKey(0) & 0xFF

        if key == ord("r"):
            rectPoints = []
            print(rectPoints)
            image = clone.copy()


        elif key == ord("q") or key == ord("\n") or key == ord("\r"):
            break

    cv2.destroyAllWindows()
    return th, lw, bh, rw




