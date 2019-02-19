import csv
import queue
import time
from multiprocessing import cpu_count
from threading import Thread, Event

import numpy as np

from utils.logger import Logger

initialization_failure = 'Failed to initialize {what} because {failure_reason}.'


### TODO: Add logging, add docs.
class OutputVideoHandler:
    def __init__(self, input_frame_queue: queue.Queue = None, name: str = 'BaseOutputVideoHandler',
                 frame_processing_function=None, threads_count: int = cpu_count(), frame_rate: int = 24,
                 realtime_processing=True):
        self.logger = Logger(name)
        self.name = name
        if input_frame_queue is None:
            failure_message = initialization_failure.format(name, 'frame queue is empty')
            self.logger.log_string(failure_message)
            raise Exception(failure_message)
        if frame_rate < 1:
            failure_message = initialization_failure.format(name, "frame must be greater than zero")
            self.logger.log_string(failure_message)
            raise Exception(failure_message)
        if threads_count < 1:
            failure_message = initialization_failure.format(name, 'threads count should be greater than zero')
            self.logger.log_string(failure_message)
            raise Exception(failure_message)
        self.threads_count = threads_count
        self.input_queue = input_frame_queue
        self.output_queue = queue.PriorityQueue()
        self.frame_processing_function = frame_processing_function
        self.realtime_processing = realtime_processing
        self.timeout_on_frame = 1.0 / frame_rate
        self.threads = [Thread(target=self._process_frame, args=(t_id,)) for t_id in range(self.threads_count)]
        self.process_frames_event = Event()
        for t in self.threads:
            t.daemon = True
            t.start()

    def _process_frame(self, thread_id: int):
        logger = Logger(f'{self.name} thread {thread_id}')
        statistics = open(f'proc_time_thread{thread_id}.txt', 'w+', newline='')
        writer = csv.writer(statistics)
        while True:
            self.process_frames_event.wait()
            try:
                next_frame = self.input_queue.get(block=False, timeout=1)
            except queue.Empty:
                logger.log_string('Warning: failed to get frame from input queue within 1 second.')
                next_frame = None
            if next_frame is not None:
                ret, frame = next_frame
                start_time = time.time()
                if self.frame_processing_function is not None:
                    frame = self.frame_processing_function(frame)
                # Avoid putting outdated frames. ###TODO: Improve condition
                processing_time = time.time() - start_time
                writer.writerow([processing_time])
                if processing_time > self.timeout_on_frame and self.realtime_processing:
                    continue
                self.output_queue.put_nowait((start_time, frame))

    def start_processing_frames(self):
        self.process_frames_event.set()

    def stop_processing_frames(self):
        self.process_frames_event.clear()

    def get_next_frame(self)->(bool, np.array):
        return self.output_queue.get(timeout=3)
