import cv2
import numpy as np

from image_processing.base_actions import open_image


class HOG_descriptor:
    def __init__(self, input_image: np.array,
                 hog_configuration: str = 'hog_params.xml'):
        self.descriptor = cv2.HOGDescriptor(hog_configuration)
        self.image = input_image

    def get_features(self):
        self.descriptor.compute(self.image)

    def detect_face(self):
        self.descriptor.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        return self.descriptor.detect(self.image)


if __name__ == '__main__':
    img = open_image('test3.jpg', greyscale=False)
    hd = HOG_descriptor(img)
    print(hd.detect_face())
