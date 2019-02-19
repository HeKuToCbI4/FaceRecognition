import queue
import time
from multiprocessing import Event
from threading import Thread

import cv2

from utils.logger import Logger


class InputVideoHandler:
    def __init__(self, name: str = 'BaseInputVideoHandler', video_source_device: int = None,
                 video_source_file: str = None, fps: int = 24):
        """
        Creates object to handle video file/direct frames input from camera. If neither device/camera
        specified raises error.
        Initializes thread for capturing frames.
        :raise Exception if neither device/video input specified.
        :param name: Used for logging.
        :param video_source_deivce: index of source video device.
        :param video_source_file: name of input video file.
        :param fps: frame rate of a file to prevent memory overload.
        """
        self.name = name
        if video_source_device is None and video_source_file is None:
            raise Exception('Neither video source file nor video input device was specified.')
        self.capture = cv2.VideoCapture(video_source_device if video_source_device is not None else video_source_file)
        self.frame_queue = queue.Queue()
        self.capture_event = Event()
        self.logger = Logger(f'VideoHandler {self.name}')
        self.capture_thread = Thread(target=self._start_capture)
        self.capture_thread.daemon = True
        self.capture_thread.start()
        self.frames_per_second = fps

    def _start_capture(self):
        """
        Thread prototype for video capture. Reads frames and puts them in self.frame_queue.
        :return: None.
        """
        self.logger.log_string('Capture thread started.')
        while True:
            self.capture_event.wait()
            while self.capture_event.is_set():
                start_time = time.time()
                read_result = self.capture.read()
                ret, frame = read_result
                if ret:
                    self.frame_queue.put_nowait((time.time, frame))
                time.sleep(1 / self.frames_per_second + time.time() - start_time)

    def start_capture(self):
        """
        start capturing frames and put them into self.frame_queue.
        :return:  None.
        """
        self.capture_event.set()
        self.logger.log_string('Started video capture.')

    def stop_capture(self):
        """
        Stop capturing frames from video source.
        :return:
        """
        self.capture_event.clear()
        self.logger.log_string('Stopped capturing frames.')

    def get_next_frame(self) -> tuple:
        """
        Get next frame from frame_queue.
        :return: tuple of reference time and frame itself, if queue is not empty, None if there is no frames.
        """
        return self.frame_queue.get(timeout=1)

    def get_current_state(self) -> bool:
        self.logger.log_string(f'Current state of {self.name}: capture event {self.capture_event.is_set()}, '
                               f'queue is filled by {self.frame_queue.qsize()} frames.')
        return self.capture_event.is_set()

    def __del__(self):
        self.capture.release()
