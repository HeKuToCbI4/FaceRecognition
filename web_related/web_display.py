import cv2
from flask import Flask, render_template, Response

from web_related.web_handle import web_handle

app = Flask(__name__)


def gen(ovh):
    while True:
        frame = ovh.get_next_frame()
        ret, frame = cv2.imencode('.jpg', frame)
        frame = frame.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(web_handle()), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8090, debug=True)
