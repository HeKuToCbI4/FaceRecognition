import socket

import cv2

from utils.input_video_stream_handler import InputVideoHandler

if __name__ == '__main__':
    ivh = InputVideoHandler(video_source_device=0)
    ivh.start_capture()
    client_socket = socket.socket()
    client_socket.connect(('192.168.0.105', 1337))
    print('Connection successful!')
    while True:
        ret, frame = ivh.get_next_frame()
        encoded, buffer = cv2.imencode('.jpg', frame)
        client_socket.send(bytes(buffer))
        client_socket.send(b'NEXTFRAME')
