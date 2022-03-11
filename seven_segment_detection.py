from typing import List
import cv2
import imutils
from imutils import contours
import my_utilities


def ssd_detection(img, settings_list, number_format, max_digits):
    # Segment size standardizing
    img = my_utilities.resize(img, 120)
    segment_sensitivity = settings_list[0]
    # Thresholding
    if settings_list[1] != 0:
        try:
            gau = cv2.GaussianBlur(img, (settings_list[1], settings_list[2]), settings_list[3])
        except:
            gau = img
            print("GaussianBlur Error")
    # threshold = cv2.threshold(gau, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    threshold = cv2.adaptiveThreshold(gau, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 199, 10)
    # threshold = cv2.adaptiveThreshold(gau, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 199, 10)

    # Morph
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(settings_list[4], settings_list[5]))
    morphed = cv2.erode(threshold, kernel1, img, iterations=1)
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(settings_list[6], settings_list[7]))
    morphed = cv2.dilate(morphed, kernel2, img, iterations=1)
    kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(settings_list[8], settings_list[9]))
    morphed = cv2.erode(morphed, kernel3, img, iterations=1)

    # Find and grab contours
    cntrs = cv2.findContours(morphed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cntrs = imutils.grab_contours(cntrs)
    num_contours = []
    minus = False

    # Throwing out small contours(First throwing out small contours and filter out minus signs)
    for ctr in cntrs:
        (x, y, w, h) = cv2.boundingRect(ctr)
        if w >= 15 and h >= 50:
            num_contours.append(ctr)
        elif (25 <= w <= 60) and (15 <= h <= 37):
            minus = True

    num_contours = contours.sort_contours(num_contours, method="left-to-right")[0]

    i = 1
    character_contours = len(num_contours)
    digits: List[int] = []

    for c in num_contours:
        (x, y, w, h) = cv2.boundingRect(c)
        roi = morphed[y:y + h, x:x + w]
        j = 1
        corrected = w
        shifting = 0

        # Checking if numbers merged with each other or with a dot
        # Number one
        if 7.4 > (h / w) > 3.75:
            digits.append(1)
            # print("Num 1")
            j = 2
        # Number one merged with a dot
        elif 3.75 >= (h / w) > 2.9:
            digits.append(1)
            j = 2
            # print("Number one merged with a dot")
        # Normal numbers
        elif 2.9 >= (h / w) > 1.6:
            # print("Normal number")
            corrected = w
            shifting = 0
            j = 1
        # Other numbers merged with a dot
        elif 1.6 >= (h / w) > 1.3:
            # Check if left or right number merged with a dot
            # print(character_contours)
            # print(i)
            if character_contours == 2 and i == 1:
                corrected = int(0.7 * w)
                shifting = 0
                j = 1
                # print("Left number merged with dot")
            elif character_contours == 3 and i == 2:
                corrected = int(0.7 * w)
                shifting = 0
                j = 1
                # print("Left number merged with dot")
            elif character_contours == 2 and i == 2:
                corrected = int(0.7 * w)
                shifting = int(w - corrected)
                j = 1
                # print("Right number merged with dot")
            elif character_contours == 3 and i == 3:
                corrected = int(0.7 * w)
                shifting = int(w - corrected)
                j = 1
                # print("Right number merged with dot")
            # One and another number merged with each other
        elif 1.3 >= (h / w) > 1.1:
            digits.append(1)
            corrected = int(0.55 * w)
            shifting = int(w - corrected) - 1
            j = 1
            character_contours += 1
            # print("One and another number merged with each other")
            # Two non-one number merged with each other
        elif 1.1 > (h / w) > 0.7:
            corrected = int(w / 2)
            shifting = int(w / 2)
            j = 0
            character_contours += 1
            # print("Two non-one number merged with each other")
            pass
        else:
            character_contours -= 1
            # print("Not a number")
            continue

        # Masks for segment detection
        vertical_area = (int(h * 1 / 2) * int(corrected * 1 / 3))
        horizontal_area = (int(h * 1 / 5) * int(corrected * 1 / 3))

        # Segments
        while j < 2:
            top = roi[0:int(h * 1 / 5), int(j * shifting + corrected * 1 / 3):int(j * shifting + corrected * 2 / 3)]
            top_left = roi[0:int(h * 1 / 2), 0:int(j * shifting + corrected * 1 / 3)]
            top_right = roi[0:int(h * 1 / 2), int(j * shifting + corrected * 2 / 3):w]
            center = roi[int(h * 2 / 5):int(h * 4 / 5),
                     int(j * shifting + corrected * 1 / 3):int(j * shifting + corrected * 2 / 3)]
            bottom = roi[int(h * 4 / 5):h, int(j * shifting + corrected * 1 / 3):int(j * shifting + corrected * 2 / 3)]
            bottom_left = roi[int(h * 1 / 2):h, 0:int(j * shifting + corrected * 1 / 3)]
            bottom_right = roi[int(h * 1 / 2):h, int(j * shifting + corrected * 2 / 3):j * shifting + corrected]
            j += 1
            # Detection of Number one(Its kinda redundant)
            if (h / 2.8) > w > (h / 7):
                digits.append(1)
                # Check segments, it loks worse than with a dictionary but it needs less steps to complete
            else:
                if segment_sensitivity >= (cv2.countNonZero(top) / horizontal_area):
                    digits.append(4)
                else:
                    if segment_sensitivity >= (cv2.countNonZero(bottom) / horizontal_area):
                        digits.append(7)
                    else:
                        if segment_sensitivity+0.2 >= (cv2.countNonZero(center) / horizontal_area):
                            digits.append(0)
                        else:
                            if segment_sensitivity >= (cv2.countNonZero(top_left) / vertical_area):
                                if segment_sensitivity >= (cv2.countNonZero(bottom_right) / vertical_area):
                                    digits.append(2)
                                else:
                                    digits.append(3)
                            else:
                                if segment_sensitivity >= (cv2.countNonZero(bottom_left) / vertical_area):
                                    if segment_sensitivity >= (cv2.countNonZero(top_right) / vertical_area):
                                        digits.append(5)
                                    else:
                                        digits.append(9)
                                else:
                                    if segment_sensitivity >= (cv2.countNonZero(top_right) / vertical_area):
                                        digits.append(6)
                                    else:
                                        digits.append(8)
        # cv2.imshow('Number: %d' % i, roi)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        i += 1

    if max_digits == 2:
        digits.append(0)
        character_contours += 1
    if number_format == 2 and max_digits == 4 and character_contours == 5:
        del digits[2]
        character_contours -=1
    # Form numbers based on the output digits and required type
    value = my_utilities.formatNumbers(number_format, character_contours, minus, digits)
    # print(value)
    return value
