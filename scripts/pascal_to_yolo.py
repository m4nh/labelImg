import xml.etree.ElementTree
import glob
import os

classes_map = {
    "clam": 0,
    "scrap": 1
}


def yolify(path):
    e = xml.etree.ElementTree.parse(path).getroot()
    to_write = []
    size = e.find('size')
    width = int(size.find('width').text)
    height = int(size.find('height').text)
    for ann in e.findall('object'):
        name = ann.find('name').text
        print("Annotation:", name)
        box = ann.find('bndbox')
        xmin = float(box.find('xmin').text)
        xmax = float(box.find('xmax').text)
        ymin = float(box.find('ymin').text)
        ymax = float(box.find('ymax').text)

        box_w = (xmax-xmin)/width
        box_h = (ymax-ymin)/height
        x_center = xmin/width + box_w/2
        y_center = ymin/height + box_h/2
        to_write.append('{} {} {} {} {}'.format(
            classes_map[name], x_center, y_center, box_w, box_h))

    return '\n'.join(to_write)


image_folder = '/Users/daniele/Desktop/to_delete/CopemoTest/images'
annotation_folder = '/Users/daniele/Desktop/to_delete/CopemoTest/images'
destination_folder = '/tmp/pino'

image_files = glob.glob(os.path.join(image_folder, '*.jpg'))
annotation_files = [x.replace('jpg', 'xml').replace(
    image_folder, annotation_folder) for x in image_files]
os.makedirs(destination_folder, exist_ok=True)

for i, a in zip(image_files, annotation_files):
    dest_file = a.replace(
        annotation_folder, destination_folder).replace('xml', 'txt')
    with open(dest_file, 'w+') as f_out:
        f_out.write(yolify(a))
