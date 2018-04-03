import numpy
import collections
import json
import sys
import ctypes
import time

import util
lib = ctypes.cdll.LoadLibrary('code/bfs.so')
full_bfs = lib.full_bfs

#returns the total distances of the distance grid
def getTotalDistance(distances):
	sum = 0
	rows,cols = distances.shape
	for i in range(rows):
		for j in range(cols):
			if distances[i][j]!=-1:
				sum = sum + distances[i][j]
	return sum

#determines if all cells in the distance grid are within the specified search radius
def allCellsWithinRadius(dist_grid, mask_grid, radius,cellsize):
	rows,cols = mask_grid.shape
	for i in range(rows):
		for j in range(cols):
			if mask_grid[i][j]==1:
				if dist_grid[i][j] > radius:
					return False
	return True

#determines if there are any roads outside of the study area
def roadsOnMask(data, mask):
	rows,cols = data.shape
	for i in range(rows):
		for j in range(cols):
			if mask[i][j] == 0:
				if data[i][j] == 1:
					return True
	return False

#returns the cost of the road network (currently number of road cells)
def costOfRoadNetwork(array):
	return numpy.sum(array)

def minDistForCellsC(rows,cols):
	grid = min_dist_for_cells(ctypes.c_int(rows),ctypes.c_int(cols))
	return grid

#returns a grid that shows how far (BFS traversal) each cell is from a road
def minDistForCells(roads, mask):
	
	rows,cols = roads.shape
	dist_grid = numpy.zeros((rows,cols),dtype=numpy.int32)-1
	roads = numpy.array(roads,dtype=numpy.int32)
	mask = numpy.array(mask,dtype=numpy.int32)
	
	full_bfs(ctypes.c_int(rows),ctypes.c_int(cols),
			  ctypes.c_void_p(mask.ctypes.data),
			  ctypes.c_void_p(roads.ctypes.data),
			  ctypes.c_void_p(dist_grid.ctypes.data))
	
	return dist_grid

#averages the distance grid by the number of cells in the mask
def avgDistForArea(dist_grid, mask_grid):
	cells_in_area = numpy.sum(mask_grid)
	total_distance = getTotalDistance(dist_grid)
	return float(total_distance)/float(cells_in_area)

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print('Usage: %s <config file (JSON)> <road grid file (ASC)>'%sys.argv[0])
		sys.exit()

	file_name = sys.argv[1]
	print ('Opening: ' + file_name.split('/')[-1])

	#get info from json
	with open(file_name, 'r') as f:
		json_dict = json.load(f)
	name = json_dict.get('area_name')
	layers = dict(json_dict.get('layers').items())
	radius = json_dict.get('search_radius')

	grid = util.ascToGrid(layers['mask'])
	grid = util.removeHeader(grid)
	#grid = util.fixFirstColRow(grid)
	grid = util.changeToInt(grid)
	mask_grid = numpy.array(grid)

	grid = util.ascToGrid(sys.argv[2])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	network_grid = numpy.array(grid)

	bfs_grid = minDistForCells(network_grid, mask_grid)
	util.saveFile(bfs_grid, 'bfs', layers)

	grid = util.ascToGrid(layers['mask'])
	cellsize = float(grid[4][-1])
	
	print("are there roads on the mask? "+str(roadsOnMask(network_grid, mask_grid)))
	print("cost of road network = "+str(costOfRoadNetwork(network_grid)))
	print("avg traversal distance from road for all cells in mask = "+str(avgDistForArea(bfs_grid,mask_grid)))
	print("are all cells within the specified search radius from a road? "+str(allCellsWithinRadius(bfs_grid, mask_grid, radius,cellsize)))