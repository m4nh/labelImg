import sys
import os
import glob
import random
import shutil
folder = sys.argv[1]

image_folder = os.path.join(folder, 'images')
label_folder = os.path.join(folder, 'labels')


output_folder = sys.argv[2]
howmany = 1000

images = sorted(glob.glob(os.path.join(image_folder, "*.jpg")))
labels = sorted(glob.glob(os.path.join(label_folder, "*.txt")))


# random.shuffle(images)

# images = images[:howmany]
# print images

pairs = []
for i, image in enumerate(images):
    pairs.append((image, labels[i]))


random.shuffle(pairs)
pairs = pairs[:howmany]


image_output_folder = os.path.join(output_folder, "images")
label_output_folder = os.path.join(output_folder, "labels")
os.makedirs(output_folder)
os.makedirs(image_output_folder)
os.makedirs(label_output_folder)

counter = 0
for pair in pairs:
    counter_str = str(counter).zfill(5)

    image_out = os.path.join(image_output_folder, counter_str + ".jpg")
    label_out = os.path.join(label_output_folder, counter_str + ".txt")
    shutil.copy(pair[0], image_out)
    shutil.copy(pair[1], label_out)
    print image_out, label_out
    counter += 1
