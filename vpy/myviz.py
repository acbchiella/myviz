from vpython import *
from models import grid_frame

class MyViz:
     def __init__(self):
        set_browser('pyqt')
        scene.width = 800
        scene.height = 800
        scene.background = color.gray(0.3)
        scene.range = 8 
        scene.camera.pos = vector(0.190521, -1.02901, 5.1454)
        scene.camera.axis = vector(2.00527e-07, 0.962709, -5.00575)
        scene.lights = []
        scene.ambient=color.gray(0.7)
        def move():
            print('pos: ', scene.camera.pos)
            print('axis: ', scene.camera.axis)

        scene.bind("mousemove", move)

        grid_frame.GridFrame(width=80, height=80, grid_size=0.1, radius=0.001, color=color.gray(0.8))#vector(0.2,0.2,0.2))

