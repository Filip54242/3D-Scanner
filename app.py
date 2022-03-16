import plotly
from plotly import graph_objs as go
from plotly import express as px
import json
from flask import Flask, render_template, Response
from motor_controller import MotorController
from kinect_controller import KinectController, KinectImageType


kinect = KinectController()
motor = MotorController()
app = Flask(__name__, static_url_path='/static')


def generate_image():
    while True:
        if kinect._device_open() is not True:
            frame = kinect.get_jpg_image().tobytes()
            yield(b'--frame\r\n'
                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rgb_image')
def rgb_image():
    kinect.change_output_type(KinectImageType.RGB)
    return "200"


@app.route('/depth_colorized')
def depth_colorized():
    kinect.change_output_type(KinectImageType.DEPTH_COLORIZED)
    return "200"


@app.route('/depth_raw')
def depth_raw():
    kinect.change_output_type(KinectImageType.DEPTH_RAW)
    return "200"

@app.route('/clockwise')
def rotate_clockwise():
    motor.rotate_clockwise(10)
    return "200"

@app.route('/counterclockwise')
def rotate_counterclockwise():
    motor.rotate_counter_clockwise(10)
    return "200"

@app.route('/image')
def image():
    return Response(generate_image(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/plot')
def plot():
    kinect.set_skip(2)
    x, y, z = kinect.create_point_cloud()
    fig = go.Figure(data=[
        go.Scatter3d(x=x, y=y, z=-z,
                     mode='markers', marker=dict(
                         color="black",
                         size=1,
                         sizemode='diameter'
                     ))])
    fig.update_layout(title_text="title", margin={
        "r": 0, "t": 0, "l": 0, "b": 0}, height=800)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('plot.html', graphJSON=graphJSON)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
