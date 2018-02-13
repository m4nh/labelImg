from dicttoxml import dicttoxml
from xml.dom import minidom
import xml.etree.ElementTree as ET
from xml.etree import ElementTree
import sys
import os
import glob
import numpy as np
import cv2

classes = {
    0: 'apple',
    1: 'banana',
    2: 'peach',
    3: 'pear',
    4: 'plum'
}

folder = sys.argv[1]
image_folder = os.path.join(folder, 'images')
label_folder = os.path.join(folder, 'labels')


images = sorted(glob.glob(os.path.join(image_folder, "*.jpg")))
labels = sorted(glob.glob(os.path.join(label_folder, "*.txt")))


for index in range(0, len(images)):

    image = images[index]
    label = np.loadtxt(labels[index])
    img = cv2.imread(image)
    print image
    print label
    print img.shape

    w = float(img.shape[1])
    h = float(img.shape[0])
    objects = []
    for r in label:
        cls = classes[int(r[0])]

        ow = int(r[3] * w)
        oh = int(r[4] * h)
        ox = int(r[1] * w - ow * 0.5)
        oy = int(r[2] * h - oh * 0.5)

        obj = {
            'name': cls,
            'pose': 'Unspecified',
            'truncated': 0,
            'difficult': 0,
            'bndbox': {
                'xmin': ox,
                'ymin': oy,
                'xmax': ox + ow,
                'ymax': oy + oh,
            }
        }
        objects.append(obj)
        print cls, ox, oy, ow, oh

    data = {
        'folder': 'images',
        'filename': os.path.basename(image),
        'path': image,
        'source': {'database': 'Unknown'},
        'size': {
            'width': w,
            'height': h,
            'depth': img.shape[2]
        }
    }

    xmlstr = dicttoxml(data, custom_root='annotation', attr_type=False)
    document = ET.fromstring(xmlstr)

    for i, o in enumerate(objects):
        print(i, o)
        ostr = dicttoxml(o, attr_type=False, custom_root='object').replace('<?xml version="1.0" encoding="UTF-8" ?>', '')
        oel = ET.fromstring(ostr)
        document.append(oel)

    xml = minidom.parseString(ElementTree.tostring(document))
    print(xml.toprettyxml())

    out_file = os.path.join(image_folder, os.path.splitext(os.path.basename(image))[0] + ".xml")
    f = open(out_file, 'w')
    f.write(xml.toprettyxml())
    f.close()
