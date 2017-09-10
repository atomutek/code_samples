#!/usr/bin/env python

'''
    File name: salami_sweep.py
    Python Version: 2.7
    Description: Safe, Laser & Mirror code assignment for Ascent.
                 Sweep line version.
'''

__author__ = "Matthieu Destephe"
__email__ = "matt@atomutek.org"

# Import
import os
import numpy as np
import time
import sys
from collections import defaultdict
from bisect import bisect_left, bisect_right

import bst

# Constants
MAX_SIZE = 1000000
MAX_MIRRORS = 200000
MIRROR_45 = 45           # /    right_mirror
MIRROR_135 = 135          # \   left_mirror

UP = 8
DOWN = 2
LEFT = 4
RIGHT = 6

# [Helper Functions]

def find_lt(a, x, max_value):
    'Find rightmost value less than x'
    i = bisect_left(a, x)
    if i:
        return a[i-1]
    else:
        return max_value


def find_gt(a, x, max_value):
    'Find leftmost value greater than x'
    i = bisect_right(a, x)
    if i != len(a):
        return a[i]
    else:
        return max_value


# [Class]

class Safe:

    col = 0
    row = 0
    intersections = None

    dv_lines = defaultdict(list)
    dh_lines = defaultdict(list)
    mirrors_x = defaultdict(list)
    mirrors_y = defaultdict(list)


    def __init__(self, config_file):
        with open(config_file,'r') as conf:
            # read first line with r c m n
            [r,c,m,n] = conf.readline()[:-1].split(' ')
            [r,c,m,n] = [ int(x) for x in [r,c,m,n] ]

            # No mirror
            if m == 0 and n == 0:
                raise Exception("Impossible")

            if r > MAX_SIZE or c > MAX_SIZE:
                raise Exception("Row or column size is incorrect.")

            if m > MAX_MIRRORS or n > MAX_MIRRORS:
                raise Exception("Mirror size is incorrect.")

            self.row, self.col = r, c
            self.v_lines = []
            self.h_lines = []

            for right_mirror in xrange(m):
                coordinate = conf.readline()[:-1].split(' ')
                [x,y] = [int(c) for c in coordinate]
                self.mirrors_x[x].append((y,MIRROR_45))
                self.mirrors_y[y].append((x,MIRROR_45))
            for left_mirror in xrange(n):
                coordinate = conf.readline()[:-1].split(' ')
                [x,y] = [int(c) for c in coordinate]
                self.mirrors_x[x].append((y,MIRROR_135))
                self.mirrors_y[y].append((x,MIRROR_135))


    def get_orientation(self, orientation, x, y):
        if x > self.row or y > self.col:
            return None
        [mirror] = [item[1] for item in self.mirrors_x[x] if item[0] == y]
        if orientation == LEFT and mirror == MIRROR_45 or \
            orientation == RIGHT and mirror == MIRROR_135:
            return DOWN
        if orientation == LEFT and mirror == MIRROR_135 or \
            orientation == RIGHT and mirror == MIRROR_45:
            return UP
        if orientation == UP and mirror == MIRROR_45 or \
            orientation == DOWN and mirror == MIRROR_135:
            return RIGHT
        if orientation == UP and mirror == MIRROR_135 or \
            orientation == DOWN and mirror == MIRROR_45:
            return LEFT


    def get_nearest_mirror_in_that_direction(self, x,y,orientation):
        if orientation == UP:
            new_x = find_lt([c[0] for c in self.mirrors_y[y]], x, 0)
            return new_x, y
        if orientation == DOWN:
            new_x = find_gt([c[0] for c in self.mirrors_y[y]], x, self.row+1)
            return new_x, y
        if orientation == RIGHT:
            new_y = find_gt([c[0] for c in self.mirrors_x[x]], y, self.col+1)
            return x, new_y
        if orientation == LEFT:
            new_y = find_lt([c[0] for c in self.mirrors_x[x]], y, 0)
            return x, new_y


    def trace_from_laser(self, x, y, orientation):
        '''
            Simulate the route of the laser from one point x, y and a
            orientation
        '''
        if x == 0 or y == 0 or x == self.row+1 or y == self.col+1:
            return x,y

        n_x, n_y = self.get_nearest_mirror_in_that_direction(x,y,orientation)
        n_orientation = self.get_orientation(orientation, n_x,n_y)

        if orientation == UP or orientation == DOWN:
            self.dv_lines[y] = sorted([x,n_x])
        if orientation == RIGHT or orientation == LEFT:
            self.dh_lines[y] = (sorted([y,n_y]),x)

        return self.trace_from_laser(n_x,n_y, n_orientation)


    def trace_from_emitter(self):
        return self.trace_from_laser(1,1,RIGHT)


    def trace_from_detector(self):
        return self.trace_from_laser(self.row,self.col,LEFT)


    def solve(self):
        '''Solve the Safe'''
        x,y = self.trace_from_emitter()
        if x >= self.row and y > self.col:
            print "0"
            return 1
        self.trace_from_detector()
        self.solve_with_bst()

        return 0


    def solve_with_bst(self):
        nb_solutions = 0
        small_x, small_y = 0, 0
        active_segments = defaultdict(list)
        r = bst.Node(0)
        for y in xrange(self.col+1):
            new_segment = g.dh_lines[y]
            end_segment = active_segments[y] == y
            vertical_range = g.dv_lines[y]
            if new_segment: #there is a new left endpoint
                # TODO consider new_segment as a possible list
                left_endpoint = new_segment[0][0]
                right_endpoint = new_segment[0][1]
                node_value = new_segment[1]
                bst.insert(r, bst.Node(node_value))
                active_segments[right_endpoint].append(node_value)
            if end_segment: # if the segment coming to an end
                active_segments[y].remove(end_segment)
                bst.delete(r,end_segment)
            if vertical_range:
                solutions = bst.search_range(r, vertical_range[0],vertical_range[1])
                if solutions:
                    if not small_x:
                        small_x, small_y = [solutions[0],y]
                    nb_solutions += len(solutions)

        print nb_solutions, small_x, small_y




if __name__ == "__main__":

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print "Wrong numbers of parameters"
        print "python salamy_sweep.py file_to_input"
        sys.exit(1)

    try:
        g = Safe(sys.argv[1])
        g.solve()
    except Exception, e:
        if 'impossible' in e.message.lower():
            print "Impossible"
        else:
            print e.message
