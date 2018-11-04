import cv2
import numpy as np

from utils.logger import Logger


class HaarClassifier:
    def __init__(self, configuration_file: str = None):
        """
        Wrapper for numpy haar classifier.
        :param configuration_file: path to xml file, if None - not trained classifier will be used.
        """
        self.logger = Logger('HaarCascadeClassifierLogger')
        self.config = configuration_file
        self.classifier = cv2.CascadeClassifier()
        if configuration_file is not None:
            try:
                loaded = self.classifier.load(configuration_file)
                if loaded:
                    self.logger.log_string(f'Successfully loaded configuration file {configuration_file}.')
                else:
                    self.logger.log_string(f'Failed to load configuration file'
                                           f' {configuration_file} due to unknown reason')
            except BaseException as e:
                self.logger.log_string(f'Failed to load configuration file {configuration_file} due to {e}.')

    def detect_mutliscale(self, image: np.array, scale_factor: float = 1.3, min_neighbours: int = 5) -> list:
        """
        Method which performs detection of faces in desired image/frame.
        :param image: Matrix of the type CV_8U containing an image where objects are detected.
        :param scale_factor: Parameter specifying how much the image size is reduced at each image scale.
        :param min_neighbours: Parameter specifying how many neighbors
        each candidate rectangle should have to retain it.
        :return: list of tuples with x, y, w, h of found faces.
        """
        try:
            return self.classifier.detectMultiScale(image, scaleFactor=scale_factor, minNeighbors=min_neighbours)
        except BaseException as e:
            self.logger.log_string(f'Failed to perform detection due to {e}.')
            return None
