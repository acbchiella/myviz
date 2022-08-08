from vpython import *

import math
import numpy as np
# from scipy.spatial.transform import Rotation as R
from models.messages import LaserScanMsg, PoseMsg
from models import frame
from models.utils import R
# from numba import jit
# import threading


class Lidar:

    def __init__(self, laser_msg: LaserScanMsg, pose: PoseMsg, color=vector(1,0,0), make_trail=False):
        self.beams = []
        self.beams_pos_xyz = []
        self.angles = Lidar._get_angles(laser_msg)
        self.color = color
        self._create_beams(laser_msg, pose=pose)
        self.frame = frame.Frame(pose=pose, size=0.15, make_trail=make_trail)
        self.make_trail = make_trail
    

    def _get_angles(laser_msg: LaserScanMsg) -> list:
        angles = []
        # n_beams = ceil((laser_msg.angle_max_rad - laser_msg.angle_min_rad)/laser_msg.angle_increment_rad)
        n_beams = len(laser_msg.ranges_mm)
        for i in range(0, n_beams):
            angles.append(
                (i - n_beams/2)*laser_msg.angle_increment_rad
            )
        return angles

   
    def _create_beams(self, laser_msg: LaserScanMsg, pose: PoseMsg):
        for idx, angle in enumerate(self.angles):
            beam_pos = np.array([math.cos(angle)*laser_msg.ranges_mm[idx]/1000, math.sin(angle)*laser_msg.ranges_mm[idx]/1000, 0])
            # rotation_matrix = R.from_euler('zyx', [pose.orientation[2], pose.orientation[1], pose.orientation[0]]).as_matrix()
            rotation_matrix = R(pose.orientation[0], pose.orientation[1], pose.orientation[2])
            beam_pos_world = rotation_matrix.dot(beam_pos) + pose.position
            box_beam = box(pos=vector(beam_pos_world[0], beam_pos_world[1], beam_pos_world[2]), size=vector(0.01, 0.01, 0.01), color=self.color)
            self.beams_pos_xyz.append([float(beam_pos_world[0]), float(beam_pos_world[1]), float(beam_pos_world[2])])
            self.beams.append(box_beam)

    
    def _update_beam_pos(self, laser_msg: LaserScanMsg, pose: PoseMsg):

        # def _map_update_beam_pos(angle, range_b, beam, beams_pos_xyz):
        #     beam_pos = np.array([math.cos(angle)*range_b/1000, math.sin(angle)*range_b/1000, 0])
        #     # rotation_matrix = R.from_euler('zyx', [pose.orientation[2], pose.orientation[1], pose.orientation[0]]).as_matrix()
        #     rotation_matrix = R(pose.orientation[0], pose.orientation[1], pose.orientation[2])
        #     beam_pos_world = rotation_matrix.dot(beam_pos) + pose.position
        #     beam.pos = vector(beam_pos_world[0], beam_pos_world[1], beam_pos_world[2])
        #     beams_pos_xyz = beam_pos_world
        #     return beam
        # x = list(map(_map_update_beam_pos, self.angles, laser_msg.ranges_mm, self.beams, self.beams_pos_xyz))
        
        for idx, angle in enumerate(self.angles):
            beam_pos = np.array([math.cos(angle)*laser_msg.ranges_mm[idx]/1000, math.sin(angle)*laser_msg.ranges_mm[idx]/1000, 0])
            # rotation_matrix = R.from_euler('zyx', [pose.orientation[2], pose.orientation[1], pose.orientation[0]]).as_matrix()
            rotation_matrix = R(pose.orientation[0], pose.orientation[1], pose.orientation[2])
            beam_pos_world = rotation_matrix.dot(beam_pos) + pose.position
            self.beams[idx].pos = vector(beam_pos_world[0], beam_pos_world[1], beam_pos_world[2])
            self.beams_pos_xyz[idx] = beam_pos_world
        
        self.frame._update_frame_pose(pose=pose) 
