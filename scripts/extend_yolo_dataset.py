import os
import sys
import glob
import cv2
import numpy as np
import math


def adjust_gamma(image, gamma=0.6):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")

    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)


def increase_brightness(img, value=50):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def getVariant(img, labels, type="", corr=""):
    if type == "":
        new_img = img.copy()
        new_labels = labels.copy()
    if type == "FLIP_H":
        new_img = cv2.flip(img, 0)
        new_labels = labels.copy()
        new_labels[:, 2] = 1.0 - new_labels[:, 2]
    if type == "FLIP_V":
        new_img = cv2.flip(img, 1)
        new_labels = labels.copy()
        new_labels[:, 1] = 1.0 - new_labels[:, 1]
    if type == "FLIP_B":
        new_img = cv2.flip(img, -1)
        new_labels = labels.copy()
        new_labels[:, 1] = 1.0 - new_labels[:, 1]
        new_labels[:, 2] = 1.0 - new_labels[:, 2]

    if corr == "DARKER":
        new_img = adjust_gamma(new_img, gamma=0.6)
    if corr == "BRIGHTER":
        new_img = adjust_gamma(new_img, gamma=1.5)
    return new_img, new_labels


def safeBuild(folder):
    try:
        os.mkdir(folder)
    except:
        pass


def generateBasename():
    global global_counter, output_folder_images, output_folder_labels
    name = "{}".format(str(global_counter).zfill(5))
    global_counter += 1
    return os.path.join(output_folder_images, name+".jpg"), os.path.join(output_folder_labels, name+".txt")


dataset_folder = sys.argv[1]
output_folder = sys.argv[2]
output_folder_images = os.path.join(output_folder, "images")
output_folder_labels = os.path.join(output_folder, "labels")

safeBuild(output_folder)
safeBuild(output_folder_images)
safeBuild(output_folder_labels)

images_folder = os.path.join(dataset_folder, "images")
labels_folder = os.path.join(dataset_folder, "labels")

print(images_folder, labels_folder)

images = sorted(glob.glob(os.path.join(images_folder, "*.jpg")))
labels = sorted(glob.glob(os.path.join(labels_folder, "*.txt")))

frames = []
for i in range(0, len(images)):
    frames.append((images[i], labels[i]))


global_counter = 0


flips = [
    "",
    "FLIP_V",
    "FLIP_H",
    "FLIP_B"
]
corrs = [
    "",
    "DARKER",
    "BRIGHTER"
]


for f in frames:
    print(f)

    img = cv2.imread(f[0])
    labels = np.loadtxt(f[1])

    for flip in flips:
        for corr in corrs:
            print(flip, corr)
            v1 = getVariant(img, labels, flip, corr)
            image_path, label_path = generateBasename()
            cv2.imwrite(image_path, v1[0])
            np.savetxt(label_path, v1[1])

    print("Saveing", img.shape)
