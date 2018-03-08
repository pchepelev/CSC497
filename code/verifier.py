import numpy
import collections
import json
import sys

import util

def getTotalDistance(distances):
	sum = 0
	rows,cols = distances.shape
	for i in range(rows):
		for j in range(cols):
			if distances[i][j]!=-1:
				sum = sum + distances[i][j]
	return sum

def allCellsWithinRadius(dist_grid, mask_grid, radius,cellsize):
	rows,cols = mask_grid.shape
	for i in range(rows):
		for j in range(cols):
			if mask_grid[i][j]==1:
				if dist_grid[i][j]*cellsize > radius:
					return False
	return True

def roadsOnMask(data, mask):
	rows,cols = data.shape
	for i in range(rows):
		for j in range(cols):
			if mask[i][j] == 0:
				if data[i][j] == 1:
					return True
	return False

def costOfRoadNetwork(array):
	return numpy.sum(array)

def minDistForCells(roads, mask):
	queue = collections.deque()
	visited = set()
	rows,cols = roads.shape
	distance_grid = numpy.full((rows,cols),-1)
	
	#queue road cells
	for i in range(rows):
		for j in range(cols):
			if (roads[i][j] == 1):
				queue.appendleft((i,j))
				distance_grid[i][j] = 0
				
	#while queue is not empty, pop cell from queue, queue all not visited neighbours
	while(queue):
		(x,y) = queue.pop()
		cell = (x,y)
		for neighbour in getNeighbours(cell, roads, mask):
			if distance_grid[neighbour]==-1:
				queue.appendleft(neighbour)
				distance_grid[neighbour]=distance_grid[cell]+1

	return distance_grid

def avgDistForArea(dist_grid, mask_grid):
	cells_in_area = numpy.sum(mask_grid)
	total_distance = getTotalDistance(dist_grid)
	return float(total_distance)/float(cells_in_area)

def getNeighbours(cell, grid, mask):
	list = []
	rows,cols = grid.shape

	#North
	if (cell[0]+1 >= 0 and cell[0]+1 < rows):
		if (cell[1] >= 0 and cell[1] < cols):
			if (mask[(cell[0]+1,cell[1])] == 1):
				list.append((cell[0]+1,cell[1]))

	#East
	if (cell[0] >= 0 and cell[0] < rows):
		if (cell[1]+1 >= 0 and cell[1]+1 < cols):
			if (mask[(cell[0],cell[1]+1)] == 1):
				list.append((cell[0],cell[1]+1))

	#South
	if (cell[0]-1 >= 0 and cell[0]-1 < rows):
		if (cell[1] >= 0 and cell[1] < cols):
			if (mask[(cell[0]-1,cell[1])] == 1):
				list.append((cell[0]-1,cell[1]))

	#West
	if (cell[0] >= 0 and cell[0] < rows):
		if (cell[1]-1 >= 0 and cell[1]-1 < cols):
			if (mask[(cell[0],cell[1]-1)] == 1):
				list.append((cell[0],cell[1]-1))
			
	return list


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
	grid = util.fixFirstColRow(grid)
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
	
	print(roadsOnMask(network_grid, mask_grid))
	print(costOfRoadNetwork(network_grid))
	print(avgDistForArea(bfs_grid,mask_grid))
	print(allCellsWithinRadius(bfs_grid, mask_grid, radius,cellsize))


'''
	each cell that is considered is within radius
	each masked cell doesnt have a road on it

cost of road network (for now, just number of road cells)
minimum distance for a cell from a road

Average distance statistic:
 - For each cell, compute its "natural distance": the minimum distance from that cell to a road
 - Average the natural distances of every cell
'''