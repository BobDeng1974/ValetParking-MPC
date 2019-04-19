'''This file holds all of our parameters.
Access these by from parameters import *
'''
import numpy as np

SHOW_PLOTS = True

T = 5       # horizon length
DT = 0.2    # time increment
dl = 1.0    # course tick
MAX_TIME = 600.0
TARGET_SPEED = 10.0 / 3.6

MIN_V = -20.0 / 3.6
MAX_V = 10.0 / 3.6
MIN_DELTA = np.deg2rad(45.0)
MAX_DELTA = np.deg2rad(45.0)
MAX_ACCEL = 1.0
MAX_DSTEER = np.deg2rad(30.0)

L = 2.5

#### Driving Cost Matrices ####
Q = np.diag([1.0, 1.0, 0.5, 0.5]) # State Cost Matrix
Qf = Q # Final State Cost Matrix
R = np.diag([0.1, 0.1]) # Control Input Cost Matrix
Rd = np.diag([0.1, 0.5]) # Control Input Difference Cost Matrix