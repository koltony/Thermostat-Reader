import numpy as np
import cv2
import my_utilities


# Computing and executing transformation
def point_match():
    if (len(refPts) == len(movPts)) and (len(refPts) >= 4):
        # Initializing Numpy arrays for OpenCV
        # OpenCV expects Numpy array of size (n, 1, 2)
        src_pts = np.float32(refPts).reshape(-1, 1, 2)
        mov_pts = np.float32(movPts).reshape(-1, 1, 2)
        # Perspective transzformáció
        M, inliers = cv2.findHomography(mov_pts, src_pts, 0)

        if M is None:
            print('No solution found!')
        else:
            # Executing transformation and dislaying image
            image_reg = cv2.warpPerspective(clone, M, (w, h))
            cv2.destroyWindow("Perspective Transform")
            cv2.imshow('Transformed Image', image_reg)
            #cv2.waitKey(0)


def click(event, x, y, flags, param):
    # Accessing global variables
    global movPts

    if event == cv2.EVENT_LBUTTONUP:
        # adding (x, y) coordinates to the list
        movPts.append((x, y))
        print(movPts)

        # Drawing a marker
        cv2.drawMarker(image, (x, y), (0, 255, 0), cv2.MARKER_CROSS)
        # cv2.circle(image2, (x-1, y-1), 3, (0, 255, 0), 2)
        cv2.imshow('Perspective Transform', image)
        point_match()


def mainPerspectiveTransform(aspect_ratio_width, aspect_ratio_height, newimageheight, original_image):
    global h, w, refPts, movPts, image, clone

    refPts = []
    movPts = []
    image = original_image
    image = my_utilities.resize(image, newimageheight)
    clone = image.copy()
    cv2.namedWindow('Perspective Transform')
    cv2.setMouseCallback('Perspective Transform', click)

    h, w = image.shape[:2]

    refPts = [(0, 0), (aspect_ratio_width * 1, 0), (aspect_ratio_width * 1, aspect_ratio_height * 1), (0, aspect_ratio_height * 1)]

    while True:

        cv2.imshow('Perspective Transform', image)
        key = cv2.waitKey(0) & 0xFF

        if key == ord("r") or key == ("\b"):
            movPts = []
            print(movPts)
            image = clone.copy()
        elif key == ord("q") or key == ord("\n") or key == ord("\r"):
            break

    cv2.destroyAllWindows()
    return movPts, refPts