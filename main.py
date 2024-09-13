from flask import Flask,render_template,Response
from camera import VideoCamera

# initializing flask

app = Flask(__name__)

# This is a route which will run browser on route '/'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vdo')
def vdo():
    return render_template('video.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-type:image/jpeg\r\n\r\n' + frame +b'\r\n\r\n')

@app.route('/feed')
def feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace;boundary=frame')

# Now how to run a html file

if __name__=='__main__':
    app.run(host='0.0.0.0',port='5000',debug=True)