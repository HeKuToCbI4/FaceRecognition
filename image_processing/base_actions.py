import numpy as np
import scipy.ndimage

from utils.logger import Logger

base_actions_logger = Logger('BaseActions')


def open_image(filename: str, greyscale: bool = False) -> np.array:
    try:
        return scipy.ndimage.imread(filename, greyscale)
    except FileNotFoundError as e:
        base_actions_logger.log_string(f'Failed to open image: {filename} due to {e}')
        return None


def save_image(image: np.array, path_to_file: str):
    pass


if __name__ == '__main__':
    open_image('meme_test.jpg')
