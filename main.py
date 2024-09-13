from flask import Flask,render_template,Response
from camera import VideoCamera
import time
# initializing flask

app = Flask(__name__)

camera = VideoCamera()

# This is a route which will run browser on route '/'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vdo')
def vdo():
    return render_template('video.html')

def gen(camera):
    while True:
        start_time = time.time()
        frame = camera.get_frame()
        if frame is None:
            continue
        yield(b'--frame\r\n'
              b'Content-type:image/jpeg\r\n\r\n' + frame +b'\r\n\r\n')
        if time.time() - start_time >= 40:
            break

@app.route('/feed')
def feed():
    return Response(gen(camera),
                    mimetype='multipart/x-mixed-replace;boundary=frame')

@app.route('/count')
def final_count():
    count = camera.get_count()
    return f'Final Count: {count}'

# Now how to run a html file

if __name__=='__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)