from math import cos, sin
import numpy as np

def R(phi, theta, psi):
            r00 = cos(psi)*cos(theta)
            r01 = -sin(psi)*cos(phi) + cos(psi)*sin(theta)*sin(phi)
            r02 = sin(psi)*sin(phi) + cos(psi)*sin(theta)*cos(phi)

            r10 = sin(psi)*cos(theta)
            r11 = cos(psi)*cos(phi) + sin(psi)*sin(theta)*sin(phi)
            r12 = -cos(psi)*sin(phi) + sin(psi)*sin(theta)*cos(phi)

            r20 = -sin(theta)
            r21 = cos(theta)*sin(phi)
            r22 = cos(theta)*cos(phi)

            return np.matrix([[r00, r01, r02], [r10, r11, r12], [r20, r21, r22]]).A