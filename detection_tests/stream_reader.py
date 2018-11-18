import os

import cv2

from haar_cascades.haar_classifier import HaarClassifier
from image_processing.base_actions import draw_rectangle
from limits import CWD
from utils.input_video_stream_handler import InputVideoHandler
from utils.output_video_stream_handler import OutputVideoHandler


def process_frame(frame):
    detection_result = classifier.detect_mutliscale(frame)
    if detection_result is not None:
        for res in detection_result:
            x, y, w, h = res
            return draw_rectangle(frame, (x, y, x + w, y + h))
    return frame


if __name__ == '__main__':
    try:
        classifier = HaarClassifier(
            os.path.join(CWD, 'opencv_defaults', 'haarcascades', 'haarcascade_frontalface_default.xml'))
        vh = InputVideoHandler('Test VideoHandler', video_source_device=0)
        ovh = OutputVideoHandler(input_frame_queue=vh.frame_queue, frame_processing_function=process_frame,
                                 threads_count=2)
        print('Setting event for capture.')
        vh.start_capture()
        print('Event set.')
        ovh.start_processing_frames()
        while True:
            next_frame = ovh.get_next_frame()
            if next_frame is not None:
                ret, frame = next_frame
                cv2.imshow('CameraCapture', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f'Error {e} occurred.')
    finally:
        vh.stop_capture()
        ovh.stop_processing_frames()
        cv2.destroyAllWindows()
        vh.__del__()
