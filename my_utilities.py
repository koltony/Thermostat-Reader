import cv2
import os
import numpy as np
import tkinter as tk
import adjust_image
from tkinter import filedialog
from tkinter.messagebox import askyesno
from tkinter.messagebox import askokcancel

def perspectiveTransform(refpoint, movepoint, newheight, image):
    try:
        image = resize(image, newheight)
        h, w = image.shape[:2]
        src_pts = np.float32(refpoint).reshape(-1, 1, 2)
        mov_pts = np.float32(movepoint).reshape(-1, 1, 2)
        M, inliers = cv2.findHomography(mov_pts, src_pts, 0)
        image = cv2.warpPerspective(image, M, (w, h))
        return image
    except AttributeError:
        print("Attribute error at", image)

def resize(img, newimageheight):
    try:
        origin_img_width = img.shape[1]
        origin_img_height = img.shape[0]
        new_img_height = newimageheight
        new_img_width = int((new_img_height / origin_img_height) * origin_img_width)
        img = cv2.resize(img, (new_img_width, new_img_height), interpolation=cv2.INTER_AREA)
    except ZeroDivisionError:
        pass
    finally:
        return img

def rotateImage(img, degrees):
    try:
        (h, w) = img.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        rot_matrix = cv2.getRotationMatrix2D((cX, cY), degrees, 1.0)
        rotated = cv2.warpAffine(img, rot_matrix, (w, h))
        return rotated
    except:
        rotated = img
        return rotated


def openFiles():
    root = tk.Tk()
    root.withdraw()
    image_path = filedialog.askopenfilename(filetypes=[
        ("all image formats", ".png"),
        ("all image formats", ".jpeg"),
        ("all image formats", ".jpg")
    ])
    directory_path = os.path.dirname(image_path)
    image_name, image_extension = os.path.splitext(image_path)
    if len(image_path) > 0:
        img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    return img, image_path, directory_path, image_extension

def saveFile(df):
    root = tk.Tk()
    root.withdraw()
    try:
        with filedialog.asksaveasfile(mode='w', defaultextension=".xlsx") as file:
            df.to_excel(file.name)
    except AttributeError:
        print("The user cancelled save")

    root.destroy()  # close the dialogue box

#not working
def resizeAndSave(directory_path, image_extension, image):
    global delta_w, lw, rw, th, delta_h, bh, isused
    root = tk.Tk()
    root.withdraw()
    answer = askyesno(title="Confirmation", message="Do you want to adjust size of your pictures?")
    cutlist= []
    if answer:
        warning = askokcancel(title="WARNING", message="This action will change your images!")
        if warning:
            ct = 1

            try:
                original_h, original_w = image.shape[:2]
                im = resize(image, 720)
                new_h, new_w = im.shape[:2]
                delta_h = original_h/new_h
                delta_w = original_w/new_w

                th, lw, bh, rw = adjust_image.mainROI(im)
                cv2.destroyAllWindows()
                nlw =int(lw * delta_w)
                nrw =int(rw * delta_w)
                nth = int(th * delta_h)
                nbh = int(bh * delta_h)
                cutlist =[nlw, nrw, nth, nbh]
                isused = True
            except NameError:
                print("No region selected")
                isused = False
    else:
        isused = False
    return cutlist, isused
               # image[int(lw * delta_w):int(rw * delta_w), int(th * delta_h):int(bh * delta_h)]

def detectFurnace(img, segment_sensitivity):
    img = resize(img, 120)
    (h, w) = img.shape[:2]
    gau = cv2.GaussianBlur(img, (7, 7), 2.0)
    threshold = cv2.adaptiveThreshold(gau, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 199, 10)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, ksize=(5, 5))
    morphed = cv2.erode(threshold, kernel1, img, iterations=1)
    kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(35, 24))
    morphed = cv2.dilate(morphed, kernel2, img, iterations=1)
    kernel3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize=(2, 2))
    morphed = cv2.erode(morphed, kernel3, img, iterations=1)
    counted = cv2.countNonZero(morphed[int(h/2):int(h-2), int(w/4):int(w/4*3)])
    area = ((h/2-2) * w/2)
    try:
        if counted/area < segment_sensitivity:
            return 0
        else:
            return 1
    except ZeroDivisionError:
        print("Error 102")
        return 0


def formatNumbers(number_format, character_contours, minus, digits):
    # number_format 1 is time
    if number_format == 1 and character_contours == 2:
        if minus:
            value = ("-" + u"{}.{}".format(*digits))
        else:
            value = (u"{}.{}".format(*digits))
    elif number_format == 1 and character_contours == 3:
        if minus:
            value = ("-" + u"{}{}.{}".format(*digits))
        else:
            value = (u"{}{}.{}".format(*digits))
    # number_format 2 is time
    elif number_format == 2 and character_contours == 3:
        value = (u"{}:{}{}".format(*digits))
    elif number_format == 2 and character_contours == 4:
        value = (u"{}{}:{}{}".format(*digits))
    elif number_format == 2 and character_contours == 5:
        value = (u"{}:{}{}:{}{}".format(*digits))
    elif number_format == 2 and character_contours == 6:
        value = (u"{}{}:{}{}:{}{}".format(*digits))
    # number_format 3 is program
    elif number_format == 3 and character_contours == 1:
        value = (u"{}".format(*digits))
    else:
        print("Error: Out of range")
        print(digits)
        value = "NaN"
    return value
