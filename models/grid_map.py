from vpython import *

import math
import numpy as np
from models.messages import PoseMsg, GMapMsg
from models import frame
from models.utils import R


class GridMap:

    def __init__(self, map_msg:GMapMsg):
        self.map_msg = map_msg
        self.map = [None]*map_msg.height*map_msg.width
        # self._create_map()

    
    def _create_map(self):
        for j in range(self.map_msg.height):
            for i in range(self.map_msg.width):
                idx = self.map_msg._map_idx(self.map_msg.width, i,self.map_msg.height - j -1)
                ceilensity = self.map_msg.data[idx]/255 if self.map_msg.data[idx] else None
                self._create_map_poceil([i,j], ceilensity)
    
    
    def _create_map_poceil(self, pos_xy, ceilensity):
        idx = self.map_msg._map_idx(self.map_msg.width, pos_xy[0],self.map_msg.height - pos_xy[1] -1)
        color_ = vector(ceilensity, ceilensity, ceilensity) if ceilensity else vector(0, 0.3, 0.3)
        self.map[idx] = box(
            pos=vector(
                (pos_xy[0]-self.map_msg.origin_pos[0])*self.map_msg.resolution - self.map_msg.resolution/2,
                (pos_xy[1]-self.map_msg.origin_pos[1])*self.map_msg.resolution - self.map_msg.resolution/2,
                0
            ), 
            size=vector(self.map_msg.resolution,self.map_msg.resolution,0.001), 
            color=color_
        )
        self.map_msg.data[idx] = ceilensity

    def _update_map_ceil(self, pos_xy, ceilensity):
        idx = self.map_msg._map_idx(self.map_msg.width, pos_xy[0],self.map_msg.height - pos_xy[1] -1)
        if isinstance(self.map[idx], box):
            self.map[idx].color = vector(ceilensity, ceilensity, ceilensity) if ceilensity else vector(0, 0.3, 0.3) 
            self.map_msg.data[idx] = ceilensity
        else:
            self._create_map_poceil([pos_xy[0],pos_xy[1]], ceilensity)
    
    # def _update_map_msg_poceil(self, pos_xy, ceilensity):
    #     idx = self.map_msg._map_idx(self.map_msg.width, pos_xy[0],self.map_msg.height - pos_xy[1] -1)
    #     self.map_msg[idx] = ceilensity

    def _update_map_line(self, pos_xyz_2, pos_xyz_1):
        pos_xyz_1[0] = pos_xyz_1[0]/self.map_msg.resolution
        pos_xyz_1[1] = pos_xyz_1[1]/self.map_msg.resolution
        pos_xyz_2[0] = pos_xyz_2[0]/self.map_msg.resolution
        pos_xyz_2[1] = pos_xyz_2[1]/self.map_msg.resolution

        dx = ceil(pos_xyz_2[0]-pos_xyz_1[0])
        dy = ceil(pos_xyz_2[1]-pos_xyz_1[1])
        
        dx1 = abs(dx)
        dy1 = abs(dy)
        px = 2 * dy1 - dx1
        py = 2 * dx1 - dy1
        if (dy1 <= dx1):
            if (dx >= 0):
                x = ceil(pos_xyz_1[0])
                y = ceil(pos_xyz_1[1])
                xe = ceil(pos_xyz_2[0])
            else:
                x = ceil(pos_xyz_2[0])
                y = ceil(pos_xyz_2[1])
                xe = ceil(pos_xyz_1[0]) 
            self._update_map_ceil((x+self.map_msg.origin_pos[0],y+self.map_msg.origin_pos[1]), 1)
            i = 0
            while (x < xe):
                x += 1
                if (px < 0):
                    px += 2 * dy1 
                else:
                    y = y + 1 if (dx < 0 and dy < 0 or dx > 0 and dy > 0) else y - 1
                    px += 2 * (dy1 - dx1)
                self._update_map_ceil((x+self.map_msg.origin_pos[0],y+self.map_msg.origin_pos[1]), 1)
                i+=1
        else:
            if (dy >= 0):
                x = ceil(pos_xyz_1[0])
                y = ceil(pos_xyz_1[1])
                ye = ceil(pos_xyz_2[1])
            else:
                x = ceil(pos_xyz_2[0])
                y = ceil(pos_xyz_2[1])
                ye = ceil(pos_xyz_1[1])
            self._update_map_ceil((x+self.map_msg.origin_pos[0],y+self.map_msg.origin_pos[1]), 1)
            i = 0
            while (y < ye):
                y += 1
                if (py <= 0):
                    py += 2 * dx1 
                else:
                    x = x + 1 if (dx < 0 and dy < 0 or dx > 0 and dy > 0) else x - 1
                    py += 2 * (dx1 - dy1)
                self._update_map_ceil((x+self.map_msg.origin_pos[0],y+self.map_msg.origin_pos[1]), 1)
                i+=1
                # if y == ye:
                #     self._update_map_ceil((x+self.map_msg.origin_pos[0],y+self.map_msg.origin_pos[1]), 0)
        self._update_map_ceil((ceil(pos_xyz_2[0])+self.map_msg.origin_pos[0],ceil(pos_xyz_2[1])+self.map_msg.origin_pos[1]), 0)
    
    def _update_map_laser(self, pos_xyz_scan, pos_xyz_odom):
        for pos in pos_xyz_scan[0:len(pos_xyz_scan):1]:
            self._update_map_line(pos, [pos_xyz_odom[0], pos_xyz_odom[1]])

#Implementar o pluging que desenha o mapa
#tentar implementar o algoritmo da occupancygrid
#Dar um tapa na ceilerface, arruar as dependencias, subir para o github, criar uma descrição
#ver ceilertools para otimizar