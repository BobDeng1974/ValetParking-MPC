'''Simulates a path planner'''

import numpy as np
import math

from .parameters import DT, T, dl

class PathPlanner:
    def __init__(self, test_track, speed, index):
        self.cx = test_track[0]
        self.cy = test_track[1]
        self.cphi = test_track[2]
        self.ck = test_track[3]
        self.speed = speed
        self.index = index

        self.xref = None
    
    def calc_ref_trajectory(self, state):
        '''Simulates an online path planner by returning x_ref'''
        xref = np.zeros((4, T+1))
        dref = np.zeros((1, T+1))
        n = len(self.cx)

        ind = self.calc_nearest_index(state)
        print('self.index: {}'.format(self.index))
        print('ind: {}'.format(ind))
        if self.index >= ind:
            ind = self.index

        self.index = ind
        print('self.index: {}'.format(self.index))
        print('ind: {}'.format(ind))

        xref[0,0] = self.cx[ind]
        xref[1,0] = self.cy[ind]
        xref[2,0] = self.speed[ind]
        xref[3,0] = self.cphi[ind]
        dref[0,0] = 0.0

        travel = 0.0
        for i in range(T+1):
            travel += abs(state.v) * DT
            dind = int(round(travel / dl))

            if (ind + dind) < n:
                xref[0, i] = self.cx[ind + dind]
                xref[1, i] = self.cy[ind + dind]
                xref[2, i] = self.speed[ind + dind]
                xref[3,i ] = self.cphi[ind + dind]
                dref[0, i] = 0.0
            else:
                xref[0, i] = self.cx[n - 1]
                xref[1, i] = self.cy[n - 1]
                xref[2, i] = self.speed[n - 1]
                xref[3, i] = self.cphi[n - 1]
                dref[0, i] = 0.0
        
        self.xref = xref
        return self.xref

    def calc_nearest_index(self, state):
        '''Helper function for path planner. Returns nearest index'''
        dx = [state.x - icx for icx in self.cx[self.index:(self.index + 10)]]
        dy = [state.y - icy for icy in self.cy[self.index:(self.index + 10)]]
        d = [idx**2 + idy**2 for (idx, idy) in zip(dx, dy)]
        ind = d.index(min(d)) + self.index

        return ind

    def distance_to_go(self, state):
        '''Calculate the # of course ticks left from current state to the goal'''
        ind = self.calc_nearest_index(state)
        return len(self.cx[ind:])
