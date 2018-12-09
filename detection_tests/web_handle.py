import os
import queue
import socket
import threading

import cv2
import numpy as np

from haar_cascades.haar_classifier import HaarClassifier
from limits import CWD
from utils.output_video_stream_handler import OutputVideoHandler
from image_processing.base_actions import draw_rectangle


class web_handle:
    def process_frame(self, frame: np.array) -> np.array:
        detection_result = self.classifier.detect_mutliscale(frame, scale_factor=1.05, min_neighbours=3)
        if detection_result is not None:
            for res in detection_result:
                x, y, w, h = res
                return draw_rectangle(frame, (x, y, x + w, y + h))
        return frame

    def data_receiving_thread(self, port):
        try:
            server_socket = socket.socket()
            server_socket.bind(('', port))
            server_socket.listen(1)
            connection, address = server_socket.accept()

            print(f'client {connection} {address} connected')
            self.connection_event.set()
            serialized_data = bytes()
            while True:
                data = connection.recv(2048)
                if not data:
                    break
                serialized_data += data
                if b'NEXTFRAME' in serialized_data:
                    frame_data = serialized_data[:serialized_data.index(b'NEXTFRAME')]
                    serialized_data = serialized_data[len(frame_data) + len(b'NEXTFRAME'):]
                    frame = np.fromstring(frame_data, dtype=np.uint8)
                    frame = cv2.imdecode(frame, 1)
                    self.inet_queue.put_nowait((True, frame))
        except:
            raise

    def __init__(self):
        self.inet_queue = queue.Queue()
        self.connection_event = threading.Event()
        self.data_recv_thread = threading.Thread(target=self.data_receiving_thread, args=(1337,))
        self.data_recv_thread.daemon = True
        self.data_recv_thread.start()

        self.classifier = HaarClassifier(
            os.path.join(CWD, 'opencv_defaults', 'haarcascades', 'haarcascade_frontalface_default.xml'))
        self.ovh = OutputVideoHandler(input_frame_queue=self.inet_queue, frame_processing_function=self.process_frame,
                                      threads_count=1, realtime_processing=False)
        self.connection_event.wait()
        self.ovh.start_processing_frames()

    def get_next_frame(self):
        timestamp, frame = self.ovh.get_next_frame()
        return frame
