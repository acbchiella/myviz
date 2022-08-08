from vpython import *

import math
import numpy as np
from models.messages import PoseMsg
from models import frame
from models.utils import R


class GridFrame:

    def __init__(self, width:int, height:int, grid_size:float, radius:float=0.002, color=vector(0,0,0)):
        for xx in range(-width//2, width//2 + 1):
            curve(pos=[(xx*grid_size, -width//2*grid_size, 0), (xx*grid_size, width//2*grid_size, 0)], color=color, radius=radius)
        for yy in range(-height//2, height//2 + 1):
            curve(pos=[(-height//2*grid_size, yy*grid_size, 0), (height//2*grid_size, yy*grid_size, 0)], color=color, radius=radius)

        frame_ = frame.Frame(pose=PoseMsg(), size=0.25)