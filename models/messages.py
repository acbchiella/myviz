from dataclasses import dataclass
from typing import List
import numpy as np
from math import ceil


@dataclass
class LaserScanMsg:
    def __init__(
        self, 
        angle_min_rad: float,
        angle_max_rad: float,
        angle_increment_rad: float,
        ranges_mm:List[float],
        range_max_mm:float
    ) -> None:
        self.angle_min_rad = angle_min_rad
        self.angle_max_rad = angle_max_rad
        self.angle_increment_rad = angle_increment_rad
        self.ranges_mm = ranges_mm
        self.range_max_mm = range_max_mm


@dataclass
class PoseMsg:
    def __init__(
        self, 
        position=np.array([0, 0, 0]),
        orientation=np.array([0, 0, 0])
    ) -> None:
        self.position = position
        self.orientation = orientation


@dataclass
class GMapMsg:
    def __init__(
        self,
        width:int,
        height:int,
        resolution:float,
        origin_pos=np.array([0, 0, 0])
    ) -> None:
        self.width = width
        self.height = height
        self.resolution = resolution
        self.origin_pos = np.array([(width//2), (height//2), 0])#origin_pos
        self.data = [None]*width*height

    def _map_idx(self, sdx, i, j):
        return sdx*j+i

    def _update_data_from_2d_matrix(self, matrix_data, width, height):
        # data = [None]*width*height
        for j in range(height):
            for i in range(width):
                self.data[self._map_idx(self.width, i - self.origin_pos[0], self.height - j - 1 - self.origin_pos[1])] = matrix_data[j, i]
        # return data
