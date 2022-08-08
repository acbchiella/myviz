from models import lidar, frame, messages, grid_frame, grid_map
from math import cos, sin, pi
import numpy as np
from vpython import vector, rate
import sys
# ---------------LIDAR-MOTOR------------
# This function takes the old (x, y, heading) pose and the motor ticks
# (ticks_left, ticks_right) and returns the new (x, y, heading).
def filter_step(old_pose, motor_ticks, ticks_to_mm, robot_width):
    x_old = old_pose[0]
    y_old = old_pose[1]
    theta_old = old_pose[2]

    delta_theta = (motor_ticks[1] - motor_ticks[0]) * ticks_to_mm / robot_width 
    delta_d =  (motor_ticks[0] + motor_ticks[1]) * ticks_to_mm / 2

    x = x_old + delta_d * cos(theta_old)
    y = y_old + delta_d * sin(theta_old)
    theta = (theta_old + delta_theta) % (2*pi)
    
    return (x, y, theta)


# -----------LIDAR MAP ------------------


# Initialize the map
map_msg = messages.GMapMsg(
    width=810,
    height=810,
    resolution=0.03
)
g_map = grid_map.GridMap(map_msg)

# g_map._update_map_laser([[10,10,0]], [0,0,0])

# ----------------------------------------

def lidar_async():
    msg_scan = messages.LaserScanMsg(
        angle_min_rad=-2.02485464000919,
        angle_max_rad=2.02485464000919,
        angle_increment_rad=0.006135923151543,
        ranges_mm = [1000 for i in range(0,660)],
        range_max_mm=10
    )

    msg_pose1 = messages.PoseMsg(orientation=np.array([0, 0, 3.717551306747922]), position=np.array([1850.0/1000, 1897.0/1000, 0]))
    msg_pose_odom = messages.PoseMsg(orientation=np.array([0, 0, 3.717551306747922]), position=np.array([1850.0/1000, 1897.0/1000, 0]))
    true_frame = frame.Frame(pose=msg_pose_odom, size=0.15, make_trail=True, trail_color=vector(0,1,0))
    lidar_ = lidar.Lidar(laser_msg=msg_scan, pose=msg_pose1, make_trail=True)

    ranges = []
    motor_ticks = []
    ticks = (0, 0)
    last_ticks = (0, 0)
    odom_pose = (1850.0/1000, 1897.0/1000, 3.717551306747922)
    first_scan_data = True
    with open(sys.path[0]+"/example/data1/robot4_scan.txt", encoding = 'utf-8') as f, \
        open(sys.path[0]+"/example/data1/robot4_reference.txt", encoding = 'utf-8') as f2,\
        open(sys.path[0]+"/example/data1/robot4_motors.txt", encoding = 'utf-8') as f3:
        for (line, line2, line3) in zip(f, f2, f3):
            rate(100)
            # ranges.append(list(map(int, line[3:])))
            if first_scan_data:
                first_scan_data = False
                # --------MOTOR---------------
                motor_ticks_row = line3.split()
                ticks = (int(motor_ticks_row[2]), int(motor_ticks_row[6]))
                last_ticks = ticks
                motor_ticks.append((ticks[0] - last_ticks[0], ticks[1] - last_ticks[1]))
            else:
                ranges = list(map(float, line.split()[3:]))
                pos = list(map(float, line2.split()[2:]))
                # --------MOTOR---------------
                motor_ticks_row = line3.split()
                ticks = (int(motor_ticks_row[2]), int(motor_ticks_row[6]))
                motor_ticks.append((ticks[0] - last_ticks[0], ticks[1] - last_ticks[1]))
                last_ticks = ticks

            if len(ranges)>0:
                # --------odometry------------
                odom_pose = filter_step(odom_pose, motor_ticks[-1], 0.349/1000.0, 173.0/1000.0)
                msg_pose_odom = messages.PoseMsg(orientation=np.array([0, 0, odom_pose[2]]), position=np.array([odom_pose[0], odom_pose[1], 0]))
                true_frame._update_frame_pose(msg_pose1)

                msg_scan.ranges_mm = ranges
                msg_pose1.position = np.array([pos[0]/1000, pos[1]/1000, 0])
                lidar_._update_beam_pos(laser_msg=msg_scan, pose=msg_pose_odom)

                #update map
                g_map._update_map_laser(lidar_.beams_pos_xyz, msg_pose_odom.position)
                # threading.Thread(target = g_map._update_map_laser, args=(lidar_.beams_pos_xyz, msg_pose_odom.position)).start()
                # input()



# import threading

# thread = threading.Thread(target = lidar_async)
# thread.start()


lidar_async()