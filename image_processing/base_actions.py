import numpy as np
import scipy.ndimage
import scipy.misc
import skimage.transform
import cv2

from utils.logger import Logger

base_actions_logger = Logger('BaseActions')


def open_image(filename: str, greyscale: bool = False) -> np.array:
    """
    Function that opens image file and returns it's representation as numpy array
    In case where file doesn't exist - logs error.
    :param filename: image file name to open.
    :param greyscale: if True image will be read as greyscale, else - rgb.
    :return: numpy array representation of image
    """
    try:
        return cv2.imread(filename, not greyscale)
    except FileNotFoundError as e:
        base_actions_logger.log_string(f'Failed to open image: {filename} due to {e}')
        return None


def save_image(image: np.array, path_to_file: str) -> bool:
    """
    Used to save image to file. Returns True if operation succeeded false otherwise.
    :param image: numpy repr. of an image. (Numpy array)
    :param path_to_file: filename where to save result.
    :return: True if operation succeed False otherwise.
    """
    try:
        scipy.misc.imsave(path_to_file, image)
        return True
    except BaseException as e:
        base_actions_logger.log_string(f'Failed to save {path_to_file} due to {e}.')
        return False


def resize_image(image: np.array, target_size: tuple) -> np.array:
    """
    Wrapper for resize function from skimage. Returns result of resizing image to target size,
    in case of error logs information about it.
    :param image: source image to be resized
    :param target_size: tuple of two integer values, x and y dimensions of result image.
    :return: result of resizing, None if error happens.
    """
    try:
        return skimage.transform.resize(image, target_size)
    except BaseException as e:
        base_actions_logger.log_string(f'Failed to rescale image to size {target_size} due to {e}')
        return None


def crop_image_part(source_image: np.array, crop_from_to: tuple) -> np.array:
    from copy import deepcopy
    """
    Function that crops image from start point to end point
    :param source_image: numpy array representation of source image
    :param crop_from_to: tuple with 4 values, start x and y and end x and y
    (10, 10, 20, 20) means crop from point (10,10) to (20,20)
    :return: numpy array representation of image fragment, None in case of errors.
    """
    try:
        # noinspection PyTupleAssignmentBalance
        # assuming we have enough values in statement.
        x_start, y_start, x_end, y_end = (*crop_from_to,)
        crop_target = deepcopy(source_image)[x_start:x_end, y_start:y_end]
        return crop_target
    except BaseException as e:
        base_actions_logger.log_string(f'Failed to crop image with {crop_from_to} parameters due to {e}.')
        return None


def normalize_image():
    pass

if __name__ == '__main__':
    # lenovo = open_image('test.jpg')
    # cropped_lenovo = crop_image_part(lenovo, (120, 120, 240, 240))
    # save_image(cropped_lenovo, 'crop_test.jpg')
    print(cv2.imread('test.jpg'))
