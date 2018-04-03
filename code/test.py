import numpy
import ctypes
import os
import sys
import models
import verifier
import collections
import util

lib = ctypes.cdll.LoadLibrary('code/bfs.so')
limited_bfs = lib.limited_bfs

rows = 18
cols = 9
BCi= 2
BCj= 3
radius = 3
best_cell = (BCi,BCj)

mask = numpy.zeros((rows,cols),dtype=numpy.int32)+1
roads = numpy.zeros((rows,cols),dtype=numpy.int32)

roads[0][0] = 1
roads[0][1] = 1
roads[1][1] = 1
roads[1][2] = 1
roads[1][3] = 1

mask[0][-2] = 0
mask[0][-3] = 0
mask[0][-4] = 0
mask[1][-2] = 0
mask[1][-3] = 0
mask[1][-4] = 0
mask[2][-3] = 0
mask[2][-4] = 0

min_dist_grid = verifier.minDistForCells(roads, mask)

covered = numpy.zeros((rows,cols),dtype=numpy.int32)
covered = models.computeCoveredGrid(covered,mask,rows,cols,min_dist_grid,radius)

benefit = numpy.zeros((rows,cols),dtype=numpy.int32)

'''
print('roads')
print(roads)
print('mask')
print(mask)
print('min_dist_grid')
print(min_dist_grid)
print('covered')
print(covered)
print('benefit')
print(benefit)
'''

limited_bfs(ctypes.c_int(rows), ctypes.c_int(cols),
			ctypes.c_int(BCi), ctypes.c_int(BCj),
			ctypes.c_int(radius),
			ctypes.c_void_p(covered.ctypes.data),
			ctypes.c_void_p(mask.ctypes.data),
			ctypes.c_void_p(benefit.ctypes.data))
'''

benefit_visited = numpy.zeros((rows,cols),dtype=numpy.int32)
queue = collections.deque()
queue.appendleft((best_cell,0))
benefit_visited[best_cell]=1
while(queue):
	(cell,y) = queue.pop()
	for nbor_ben in util.getNeighbours(cell, mask):
		if (y+1 <= 2*radius+1 and benefit_visited[nbor_ben]==0):
			queue.appendleft((nbor_ben,y+1))
			benefit[nbor_ben] = models.compute_benefit_single_cell(roads, covered, mask, radius, nbor_ben[0], nbor_ben[1])
			benefit_visited[nbor_ben]=1
'''
print (benefit)





