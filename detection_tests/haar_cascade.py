import os

from haar_cascades.haar_classifier import HaarClassifier
from limits import CWD
from image_processing.base_actions import crop_image_part, open_image, save_image

if __name__ == '__main__':
    image_path = os.path.join(CWD, 'images', 'test3.jpg')
    image = open_image(image_path)
    hc = HaarClassifier(os.path.join(CWD, 'opencv_defaults', 'haarcascades', 'haarcascade_frontalface_default.xml'))
    res = hc.detect_mutliscale(image)
    if res is not None:
        for x, y, w, h in res:
            save_image(crop_image_part(image, (x, y, x+w, y+h)), 'test_result.jpg')
            print('Successfully detected faces.')
