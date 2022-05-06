from pandas import interval_range
import plotly
from plotly import graph_objs as go
from plotly import express as px
import json
from flask import Flask, render_template, Response
import numpy as np
from depth_processing import depth2xyzuv, pretty_depth
from scipy.spatial.transform import Rotation as R

app = Flask(__name__, static_url_path='/static')


def rotate(to_rot,degrees=10,rotation_axis=[1,0,0]):
    radians = np.radians(degrees)
    axis = np.array(rotation_axis)
    vector = radians * axis
    rotation = R.from_rotvec(vector)
    return rotation.apply(to_rot)

def crop_depth(arr,interval:tuple):

    arr_max=arr.max()
    arr=np.where((arr<interval[1]), arr, arr_max)
    arr=np.where((arr>=interval[0]), arr, arr_max)
    return arr

def squish_depth(arr,interval:tuple):
    arr_max=arr.max()
    arr[:,0:interval[0]]=arr_max
    arr[:,interval[1]:arr.shape[1]]=arr_max
    return arr



def get_xyz(xyz):
    return xyz[::-1, 1], xyz[::-1, 2], xyz[::-1, 0]

def create_point_cloud(depth):
    depth_resolution_skip=1
    
    u, v = np.mgrid[:480:depth_resolution_skip,
                        :640:depth_resolution_skip]
    xyz, uv = depth2xyzuv(
            depth[::depth_resolution_skip, ::depth_resolution_skip], u, v)
    return xyz

@app.route('/')
def plot():
    depth_1=np.load(f"/home/filip/Documents/3D-Scanner/depths/depth_0.npy")
    depth_2=np.load(f"/home/filip/Documents/3D-Scanner/depths/depth_10.npy")

    interval=(490,650)

    depth_1=crop_depth(depth_1,interval)
    depth_2=crop_depth(depth_2,interval)

    squish_interval=(200,400)
    depth_2=squish_depth(depth_2,squish_interval)

    depth_1 = create_point_cloud(depth_1)
    depth_2 = create_point_cloud(depth_2)
    depth_2 = rotate(depth_2)
    
    
    #total_depth=np.vstack((depth_1,depth_2))
    total_depth=depth_2

    x, y, z = get_xyz(total_depth)
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
