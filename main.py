import cv2
import seven_segment_detection
import perspective_transform
import my_utilities
import sys
import json
import os
import pandas as pd

# Read JSON configuration file
try:
    with open("settings.JSON", "r") as settings_file:
        settings = json.load(settings_file)
        settings_file.close()
except FileNotFoundError or FileExistsError:
    print("Error: No configuration file")

#Load SVD settings
SSD_settings_list = [settings["general_settings"][0]["detection_sensitivity"],
                 settings["general_settings"][0]["gaussian_w"],
                 settings["general_settings"][0]["gaussian_h"],
                 settings["general_settings"][0]["gaussian_sigma"],
                 settings["general_settings"][0]["k_1_erode_w"],
                 settings["general_settings"][0]["k_1_erode_h"],
                 settings["general_settings"][0]["k_2_dilate_w"],
                 settings["general_settings"][0]["k_2_dilate_h"],
                 settings["general_settings"][0]["k_3_erode_w"],
                 settings["general_settings"][0]["k_3_erode_h"]
                 ]

# File dialog stuff, to read the image and the path where the images are
try:
    img, image_path, directory_path, image_extension = my_utilities.openFiles()
except UnboundLocalError:
    sys.exit()

# Transforming image
move, ref = perspective_transform.mainPerspectiveTransform(settings["general_settings"][0]['aspect_ratio_width'] * 100,
                                                           settings["general_settings"][0]['aspect_ratio_height'] * 100,
                                                           settings["general_settings"][0]['image_resize'],
                                                           original_image=img)

cols = []
for i in range(0, len(settings["regions"])):
    cols.append(settings["regions"][i]["name"])

all_picture_values = []
df = pd.DataFrame()


counter = 1
for image_path in os.listdir(directory_path):
    input_path = os.path.join(directory_path, "image" + str(counter) + str(image_extension))
    img = cv2.imread(input_path, 0)
    try:
        img = my_utilities.resize(img,settings["general_settings"][0]['image_resize'])
        img = my_utilities.perspectiveTransform(ref, move, settings["general_settings"][0]['aspect_ratio_height'], img)
        img = my_utilities.rotateImage(img, settings["general_settings"][0]['image_rotate_degrees'])
    except AttributeError:
        print("More files in this directory")
        continue

    for r in range(0, len(settings["regions"])):
        try:
            region = img[
                     settings["regions"][r]["loc_top"]:settings["regions"][r]["loc_bot"],
                    settings["regions"][r]["loc_left"]:settings["regions"][r]["loc_right"]]

            if settings["regions"][r]["format"] == 1:
                value = seven_segment_detection.ssd_detection(region, SSD_settings_list,
                                                              settings["regions"][r]["format"],
                                                              settings["regions"][r]["max_digits"])
                all_picture_values.append(value)
            if settings["regions"][r]["format"] == 2:
                value = seven_segment_detection.ssd_detection(region,SSD_settings_list,
                                                              settings["regions"][r]["format"],
                                                              settings["regions"][r]["max_digits"])
                all_picture_values.append(value)
            elif settings["regions"][r]["format"] == 3:
                value = seven_segment_detection.ssd_detection(region, SSD_settings_list,
                                                              settings["regions"][r]["format"],
                                                              settings["regions"][r]["max_digits"])
                all_picture_values.append(value)
            elif settings["regions"][r]["format"] == 4:
                value = my_utilities.detectFurnace(region,
                                                   settings["general_settings"][0]['detection_sensitivity'])
                all_picture_values.append(value)
        except TypeError:
            pass
    value_dict = dict(zip(cols, all_picture_values))
    df = df.append(value_dict, ignore_index=True)
    all_picture_values.clear()
    counter += 1

my_utilities.saveFile(df)