from vpython import *
from models.messages import PoseMsg

import numpy as np
# from scipy.spatial.transform import Rotation as R
from models.utils import R


class Frame:

    def __init__(self, pose: PoseMsg, size: float = 1, make_trail=False, trail_color=vector(0.5,0.5,1)) -> None:
        # rotation_matrix = R.from_euler('zyx', [pose.orientation[2], pose.orientation[1], pose.orientation[0]]).as_matrix()
        rotation_matrix = R(pose.orientation[0], pose.orientation[1], pose.orientation[2])
        
        
        self.v1 = np.array([size,0,0])
        self.v2 = np.array([0,size,0])
        self.v3 = np.array([0,0,size])
        
        v1_world = rotation_matrix.dot(self.v1) 
        v2_world = rotation_matrix.dot(self.v2) 
        v3_world = rotation_matrix.dot(self.v3) 

        self.a1 = arrow(
            pos=vector(pose.position[0], pose.position[1], pose.position[2]), 
            axis=vector(v1_world[0], v1_world[1], v1_world[2]), 
            color=vector(1,0,0),
            make_trail=make_trail,
            trail_radius=0.01,
            trail_color=trail_color
        )
        self.a2 = arrow(
            pos=vector(pose.position[0], pose.position[1], pose.position[2]), 
            axis=vector(v2_world[0], v2_world[1], v2_world[2]),  
            color=vector(0,1,0)
        )
        self.a3 = arrow(
            pos=vector(pose.position[0], pose.position[1], pose.position[2]), 
            axis=vector(v3_world[0], v3_world[1], v3_world[2]), 
            color=vector(0,0,1)
        )

    
    def _update_frame_pose(self, pose: PoseMsg):
        # rotation_matrix = R.from_euler('zyx', [pose.orientation[2], pose.orientation[1], pose.orientation[0]]).as_matrix()
        rotation_matrix = R(pose.orientation[0], pose.orientation[1], pose.orientation[2])
        
        v1_world = rotation_matrix.dot(self.v1) 
        v2_world = rotation_matrix.dot(self.v2) 
        v3_world = rotation_matrix.dot(self.v3) 

        self.a1.pos=vector(pose.position[0], pose.position[1], pose.position[2])
        self.a1.axis=vector(v1_world[0], v1_world[1], v1_world[2])

        self.a2.pos=vector(pose.position[0], pose.position[1], pose.position[2])
        self.a2.axis=vector(v2_world[0], v2_world[1], v2_world[2])

        self.a3.pos=vector(pose.position[0], pose.position[1], pose.position[2])
        self.a3.axis=vector(v3_world[0], v3_world[1], v3_world[2])