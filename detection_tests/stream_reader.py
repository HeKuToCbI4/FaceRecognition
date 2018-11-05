from utils.video_handler import VideoHandler
import cv2
import numpy as np
from haar_cascades.haar_classifier import HaarClassifier
import os
from limits import CWD
from image_processing.base_actions import draw_rectangle

if __name__ == '__main__':
    try:
        classifier = HaarClassifier(
            os.path.join(CWD, 'opencv_defaults', 'haarcascades', 'haarcascade_frontalface_default.xml'))
        vh = VideoHandler('Test VideoHandler', video_source_device=0)
        print('Setting event for capture.')
        vh.start_capture()
        print('Event set.')
        while True:
            next_frame = vh.get_next_frame()
            if next_frame is not None:
                ret, frame = next_frame
                detection_result = classifier.detect_mutliscale(frame)
                if detection_result is not None:
                    for res in detection_result:
                        x, y, w, h = res
                        frame = draw_rectangle(frame, (x, y, x + w, y + h))
                cv2.imshow('CameraCapture', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except BaseException as e:
        print(f'Error {e} occurred.')
    finally:
        cv2.destroyAllWindows()
        vh.__del__()
