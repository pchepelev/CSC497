import numpy
import collections
import json
import sys
import ctypes
import time

import util
import models
lib = ctypes.cdll.LoadLibrary('code/bfs.so')
full_bfs = lib.full_bfs
bfs_along_roads = lib.bfs_along_roads
get_nearest_road_index = lib.get_nearest_road_index

def avg_transport_dist(min_dist_from_road, travel_dist_along_road, mask, input, roads):
	rows,cols = roads.shape
	nearest_road_indices = get_nearest_road_indices(mask, roads)
	tree_travel_dist = numpy.zeros((rows,cols),dtype=numpy.int32)
	
	for i in range(rows):
		for j in range(cols):
			tree_travel_dist[i][j] = min_dist_from_road[i][j] + travel_dist_along_road[nearest_road_indices[i][j]]
	return tree_travel_dist
	
			
def get_nearest_road_indices(mask, roads):
	rows,cols = roads.shape
	index = numpy.array([420,69])
	
	nearest_road_indices = numpy.zeros((rows,cols),dtype=object)
	mask = numpy.array(mask,dtype=numpy.int32)
	roads = numpy.array(roads,dtype=numpy.int32)
	index = numpy.array(index,dtype=numpy.int32)
	
	for i in range(rows):
		for j in range(cols):
			get_nearest_road_index( ctypes.c_int(rows),ctypes.c_int(cols),
									ctypes.c_int(i),ctypes.c_int(j),
									ctypes.c_void_p(mask.ctypes.data),
									ctypes.c_void_p(roads.ctypes.data),
									ctypes.c_void_p(index.ctypes.data))
			nearest_road_indices[i][j] = (index[0],index[1])
			
	
	return nearest_road_indices
	

def max_dist_from_input(mask, input, roads,data_layers):
	rows,cols = roads.shape
	dist = numpy.zeros((rows,cols),dtype=numpy.int32)-1
	
	mask = numpy.array(mask,dtype=numpy.int32)
	input = numpy.array(input,dtype=numpy.int32)
	roads = numpy.array(roads,dtype=numpy.int32)
	bfs_along_roads (ctypes.c_int(rows),ctypes.c_int(cols),
					 ctypes.c_void_p(mask.ctypes.data), 
					 ctypes.c_void_p(input.ctypes.data), 
					 ctypes.c_void_p(roads.ctypes.data), 
					 ctypes.c_void_p(dist.ctypes.data))
	util.saveFile(dist,'bfs_along_roads',data_layers)
	return (numpy.amax(dist),dist)

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
	if len(sys.argv) < 4:
		print('Usage: %s <config file (JSON)> <road grid file (ASC)> <search radius>'%sys.argv[0])
		sys.exit()

	file_name = sys.argv[1]
	search_radius = int(sys.argv[3])
	print ('Verifying: ' + file_name.split('/')[-1]+".....\n")

	#get info from json
	with open(file_name, 'r') as f:
		json_dict = json.load(f)
	name = json_dict.get('area_name')
	data_layers = dict(json_dict.get('layers').items())
	access_point = (int(json_dict.get('access_point_y')),int(json_dict.get('access_point_x')))

	grid = util.ascToGrid(data_layers['mask'])
	ncols = (int(grid[0][-1]))
	nrows = (int(grid[1][-1]))
	cellsize = float(grid[4][-1])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	mask = numpy.array(grid)

	for lyr in data_layers['inaccessible'].items():
		grid = util.ascToGrid(lyr[1])
		grid = util.removeHeader(grid)
		grid = util.changeToInt(grid)
		gridarray = numpy.array(grid)
		gridarray = numpy.array(1-gridarray)
		mask = numpy.minimum(gridarray,mask)
		mask = models.ia_bfs(access_point[0],access_point[1],numpy.array(1-mask),mask)
		
	grid = util.ascToGrid(data_layers['veg'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	veg = numpy.array(grid)
	
	mask_no_veg = numpy.multiply(mask,veg)
	
	#util.saveFile(mask, 'mask', data_layers)
		
	grid = util.ascToGrid(sys.argv[2])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	network_grid = numpy.array(grid)
	
	grid = util.ascToGrid(data_layers['roads'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	roads = numpy.array(grid)
	roads = numpy.multiply(mask,roads)

	bfs_grid = minDistForCells(network_grid, mask)
	#util.saveFile(bfs_grid, 'bfs', data_layers)
	
	max_dist,max_dist_grid = max_dist_from_input(mask, roads, network_grid,data_layers)
	
	tree = avg_transport_dist(bfs_grid, max_dist_grid, mask, roads, network_grid)
	
	#util.saveFile(treenu, 'tree', data_layers)
	
	print("                                 are there roads on the mask? "+str(roadsOnMask(network_grid, mask)))
	print("are all cells within the specified search radius from a road? "+str(allCellsWithinRadius(bfs_grid, mask_no_veg, search_radius,cellsize))+"\n")
	print("                                                    cost of road network = "+str(costOfRoadNetwork(network_grid)))
	print("   average traversal distance from road for all unmasked, forested cells = "+'%.3f'%(avgDistForArea(bfs_grid,mask_no_veg)))
	print("maximum distance from any cell on the generated roads to the input roads = "+str(max_dist))
	print("           average tree travel distance for all unmasked, forested cells = "+'%.3f'%(avgDistForArea(tree,mask_no_veg)))
	print("    (tree travel distance for a cellis the distance to the nearest road cell,\n     plus the minimum distance along the road network from that cell to the input roads)")