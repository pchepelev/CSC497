import numpy
import ctypes
import os
import sys

lib = ctypes.cdll.LoadLibrary('code/test.so')
test_func = lib.full_bfs

rows = 18
cols = 9

dist_grid = numpy.zeros((rows,cols),dtype=numpy.int32)-1
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

print(dist_grid)
test_func(ctypes.c_int(rows),ctypes.c_int(cols),
		  ctypes.c_void_p(mask.ctypes.data),
		  ctypes.c_void_p(roads.ctypes.data),
		  ctypes.c_void_p(dist_grid.ctypes.data))
print(dist_grid)