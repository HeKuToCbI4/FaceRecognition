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
        return self.descriptor.detectMultiScale(self.image, winStride=(4, 4), padding=(8, 8), scale=1.05)
