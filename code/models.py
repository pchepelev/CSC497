import numpy
import collections
import time

import util
import verifier

def scragglyAlgorithmNew(name, data_layers,search_radius):
	print ("Running scragglyAlgorithm on " + name)
	
	grid = util.ascToGrid(data_layers['mask'])
	ncols = (int(grid[0][-1]))
	nrows = (int(grid[1][-1]))
	cellsize = float(grid[4][-1])	
	grid = util.removeHeader(grid)
	#grid = util.fixFirstColRow(grid)
	grid = util.changeToInt(grid)
	mask = numpy.array(grid)
	
	grid = util.ascToGrid(data_layers['roads'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	roads = numpy.array(grid)
	roads = numpy.multiply(mask,roads)
	
	
	print("mindistforcells...")
	min_dist = verifier.minDistForCells(roads, mask)
	
	covered = numpy.zeros((nrows,ncols))
	print("init covered grid...")
	covered = computeCoveredGrid(covered,mask,nrows,ncols,min_dist,search_radius)
	covered = covered*mask
	

	x = 0
	cell = numpy.unravel_index(numpy.argmin(min_dist + covered*100000 + 100000*(1-mask)),min_dist.shape)
	while numpy.max(min_dist) > search_radius:
		x+=1
		print("min:",min_dist[cell]," cell: ",cell,search_radius)
		while min_dist[cell] > 0:
			print("	min_dist[",cell,"]:",min_dist[cell])
			best_num = 999999
			neighbours = util.getNeighbours(cell, mask)
			for neighbour in neighbours:
				if min_dist[neighbour] < best_num:
					best_cell = neighbour
					best_num = min_dist[neighbour]
			cell = best_cell
			roads[cell] = 1
		min_dist = verifier.minDistForCells(roads, mask)
		cell = numpy.unravel_index(numpy.argmin(min_dist + covered*100000 + 100000*(1-mask)),min_dist.shape)
		covered = computeCoveredGrid(covered,mask,nrows,ncols,min_dist,search_radius)
		covered = covered*mask
		util.saveFile(roads, 'roads'+str(x), data_layers)
		
		
	return roads

#heuristic model #1
def scragglyAlgorithm(name, data_layers,search_radius):
	print ("Running scragglyAlgorithm on " + name)
	
	grid = util.ascToGrid(data_layers['mask'])
	ncols = (int(grid[0][-1]))
	nrows = (int(grid[1][-1]))
	cellsize = float(grid[4][-1])	
	grid = util.removeHeader(grid)
	#grid = util.fixFirstColRow(grid)
	grid = util.changeToInt(grid)
	mask = numpy.array(grid)
	
	grid = util.ascToGrid(data_layers['roads'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	roads = numpy.array(grid)
	roads = numpy.multiply(mask,roads)
	
	print("mindistforcells...")
	min_dist = verifier.minDistForCells(roads, mask)
	x = 0
	cell = numpy.unravel_index(numpy.argmax(min_dist),min_dist.shape)
	while numpy.max(min_dist) > search_radius:
		x+=1
		print("max:",min_dist[cell]," cell: ",cell,search_radius)
		while min_dist[cell] > 0:
			print("	min_dist[",cell,"]:",min_dist[cell])
			best_num = 999999
			neighbours = util.getNeighbours(cell, mask)
			for neighbour in neighbours:
				if min_dist[neighbour] < best_num:
					best_cell = neighbour
					best_num = min_dist[neighbour]
			cell = best_cell
			roads[cell] = 1
		min_dist = verifier.minDistForCells(roads, mask)
		cell = numpy.unravel_index(numpy.argmax(min_dist),min_dist.shape)
		util.saveFile(roads, 'roads'+str(x), data_layers)
		
		
	return roads

#greedy algorithm 
def greedyAlgorithm(name, data_layers,search_radius):
	print ("Running greedyAlgorithm on " + name)
	
	grid = util.ascToGrid(data_layers['mask'])
	ncols = (int(grid[0][-1]))
	nrows = (int(grid[1][-1]))
	cellsize = float(grid[4][-1])	
	grid = util.removeHeader(grid)
	#grid = util.fixFirstColRow(grid)
	grid = util.changeToInt(grid)
	mask = numpy.array(grid)
	
	grid = util.ascToGrid(data_layers['roads'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	roads = numpy.array(grid)
	roads = numpy.multiply(mask,roads)
	
	print("mindistforcells...")
	min_dist = verifier.minDistForCells(roads, mask)
	
	covered = numpy.zeros((nrows,ncols))
	print("init covered grid...")
	covered = computeCoveredGrid(covered,mask,nrows,ncols,min_dist,search_radius)
	
	road_neighbours = set()
	print("queue neighbours of road cells initial")
	road_neighbours = computeNeighbours(road_neighbours, nrows, ncols, roads, mask)
	cellsInMask = numpy.sum(mask)

	coveredCells = numpy.sum(covered)
	x=0
	util.saveFile(roads, 'roads', data_layers)
	util.saveFile(covered, 'covered', data_layers)
	
	while (coveredCells < cellsInMask):
		x+=1
		print (x, coveredCells, cellsInMask)
		
		#set an initial "best neighbour" that will always be overwritten
		best_cell = (-1,-1)
		best_num = -1
		best_set = set()
		
		#for each neighbour in the neighbours of road cells
		for neighbour in road_neighbours:
			current_set = set()
			num_cells = 0
			queue = collections.deque()
			queue.appendleft((neighbour,0))
			#run a bfs from the neighbour to at most search radius distance from the neighbour
			while(queue):
				(cell,y) = queue.pop()
				for nbor in util.getNeighbours(cell, mask):
					if (y+1 <= search_radius):
						queue.appendleft((nbor,y+1))
					if (covered[nbor] == 0):
						num_cells += 1
						current_set.add(nbor)
			#if the number of covered cells gained by the current neighbour is greater than
			#the number of covered cells gained by the best neighbour, replace the
			#best neighbour with the current neighbour
			if (num_cells > best_num):
				best_cell = neighbour
				best_set = current_set
		
		#set best_cell to be a road
		roads[best_cell] = 1
		
		#get neighbours of best_cell, add them to the road_neighbours set, remove the best_cell
		#from the road_neighbours set since it is a road, not a neighbour
		new_neighbours = util.getNeighbours(best_cell, mask)
		for nbor in new_neighbours:
			if (roads[nbor] == 0):
				road_neighbours.add(nbor)
		road_neighbours.remove(best_cell)
		
		#recompute the covered cells grid
		for cell in best_set:
			covered[cell] = 1
			coveredCells += 1
		
		#save some incremental modeled roads to show progress
		if (x%10==0):
			util.saveFile(roads, 'roads'+str(x), data_layers)
			util.saveFile(covered, 'covered'+str(x), data_layers)

	return roads


def computeNeighbours(road_neighbours, nrows, ncols, roads, mask):
	for i in range(nrows):
		for j in range(ncols):
			cell = (i,j)
			if (roads[cell] == 1):
				neighbours_of_cell = util.getNeighbours(cell,mask)
				for neighbour in neighbours_of_cell:
					if (roads[neighbour] == 0):
						road_neighbours.add(neighbour)
	return road_neighbours

def computeCoveredGrid(covered,mask,nrows,ncols,min_dist,search_radius):
	
	'''
	numpy.array(A<5, dtype=int)
	'''
	
	for i in range(nrows):
		for j in range(ncols):
			if (min_dist[i][j] <= search_radius and mask[i][j] == 1):
				covered[i][j] = 1
	return covered


#returns an numpy array, spaced by separation,
#based on the mask in data_layers
def gridNetwork(name, data_layers, separation):
	print('Running gridNetwork on ' + name)

	grid = util.ascToGrid(data_layers['mask'])
	ncols = (int(grid[0][-1]))
	nrows = (int(grid[1][-1]))
	cellsize = float(grid[4][-1])
	cell_dist = int(separation/cellsize)
	
	grid = util.removeHeader(grid)
	#grid = util.fixFirstColRow(grid)
	grid = util.changeToInt(grid)
	mask = numpy.array(grid)
	
	roads_list = util.zeros(ncols,nrows)
	roads_list = genGrid(roads_list,cell_dist)
	roads = numpy.array(roads_list)
	
	masked_roads = numpy.multiply(roads,mask)
	
	return(masked_roads)



#returns numpy array of zeros with dimensions based on data_layers
def dummyNetwork(name,data_layers):
	print('Running dummyNetwork on ' + name)
	grid = util.ascToGrid(data_layers['mask'])
	ncols = (int(grid[0][-1]))
	nrows = (int(grid[1][-1]))
	return numpy.zeros((ncols,nrows))

#returns a 2D list with 1s in a grid pattern (grid separation = sep)
def genGrid (grid, sep):
	for i in range(len(grid)):
		for j in range(len(grid[0])):
			if (i%sep==0 or j%sep==0):
				grid[i][j]=1
	return grid