'''Simulation loop'''
import numpy as np
import matplotlib.pyplot as plt

from .parameters import *
from .path_planner import *
from .mpc import linear_mpc, predict_motion
from .util import *

def update_vehicle_state(state, a, delta):
    '''Update Vehicle State based on mpc control output'''
    state.x = state.x + state.v * math.cos(state.phi) * DT
    state.y = state.y + state.v * math.sin(state.phi) * DT
    
    state.v = state.v + a * DT
    # Limit vehicle speed to plausible max/min
    state.v = max(min(state.v, MAX_V), MIN_V)

    # Limit steering angle to maximum value
    delta = max(min(delta, MAX_DELTA), -MIN_DELTA)
    state.phi = state.phi + (state.v * math.tan(delta) / L) * DT
    
    return state

def check_goal(goal):
    return False

def simulate(test_track, speed, dl):
    # Initialize the state
    state = vehicle_state(test_track[0][0], test_track[1][0], 0.0, test_track[2][0])
    goal = [test_track[0][-1], test_track[1][-1]]
    opt_control = control_input(a=0.0, delta=0.0)
    
    path_planner = PathPlanner(test_track, speed, 0)
    path_planner.index = path_planner.calc_nearest_index(state)
    # smooth_yaw -> Don't do for now

    # time loop
    time = 0.0
    t = [time]
    
    # book-keeping for plots
    x, y, phi, v = [], [], [], []
    a = 0.0
    delta = 0.0
    # temporary print
    np.set_printoptions(precision=3)
    while (time <= MAX_TIME):
        print('\n\n\t\t\t\t\ttime: {}'.format(time))
        # calc_ref_trajectory every time loop
        xref = path_planner.calc_ref_trajectory(state)
        print('xref: \n{}'.format(xref))

        x0 = [state.x, state.y, state.v, state.phi]
        print('x0: \n{}'.format(x0))
        xbar = predict_motion(x0, a, delta, xref)
        print('xbar: \n{}'.format(xbar))

        # iterative linear mpc every time loop
        opt_control, opt_state = linear_mpc(xref, xbar, x0, 0.0)
        # update state every time loop
        a = opt_control.a[0]
        delta = opt_control.delta[0]
        print('output a,d: \n{}, {}'.format(a, delta))
        state = update_vehicle_state(state, a, delta)
        print('updated state\n ')
        state.print_state()
        # update the lists for book-keeping

        # terminate if goal is reached (checkgoal())
        if check_goal(goal):
            break

        # increment time
        time += DT
        t.append(time)
        x.append(state.x)
        y.append(state.y)
        v.append(state.v)
        phi.append(state.phi)

        if SHOW_PLOTS:
            
            plt.subplot(2,2,3)
            plt.cla()
            if opt_state.x is not None:
                plt.plot(opt_state.x, opt_state.y, "c*", label="MPC")
            plt.plot(test_track[0], test_track[1], "--k", label="track")
            plt.plot(x, y, "xr", label="traj")
            plt.plot(xref[0, :], xref[1, :], "xb", label="xref")
            plt.plot(test_track[0][path_planner.index], test_track[1][path_planner.index], "go", markersize=6, label="target")
            plt.legend()
            plt.pause(0.001)

            plt.subplot(2,2,4)
            plt.plot(v, '-r')
            plt.plot(speed, '--b')
            plt.pause(0.001)

            print('MPC: \n {}, \n {}'.format(opt_state.x, opt_state.y))
            #input('press to continue..')
            

    return t, x, y, phi, v, a, delta