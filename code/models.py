import numpy
import collections

import util
import verifier

#greedy algorithm 
def greedyAlgorithm(name, data_layers,search_radius):
	print ("Running greedyAlgorithm on " + name)
	
	grid = util.ascToGrid(data_layers['mask'])
	ncols = (int(grid[0][-1]))
	nrows = (int(grid[1][-1]))
	cellsize = float(grid[4][-1])	
	grid = util.removeHeader(grid)
	grid = util.fixFirstColRow(grid)
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
	while (numpy.sum(covered) < cellsInMask):
		print("whileloop+")
		best_cell = [-1,set()]
		for neighbour in road_neighbours:
			print("	forloop+")
			num_cells = 0
			added_cells = set()
			
			queue = collections.deque()
			queue.appendleft((neighbour[0],0))

			while(queue):
				#(cell,y) = queue.pop()
				pop_result = queue.pop()
				cell = pop_result[0]
				y = pop_result[1]
				#print("		bfswhileloop",type(cell),cell)
				for nbor in util.getNeighbours(cell, mask):
					if (y+1 <= search_radius):
						queue.appendleft((nbor,y+1))
					if (covered[nbor] == 0):
						num_cells = num_cells + 1
						added_cells.add(nbor)
			
			if (best_cell[0] < num_cells):
				best_cell[0] = num_cells
				best_cell[1] = added_cells
		
		road_neighbours.remove(best_cell[0])
		road[best_cell[0]]=1
		road_neighbours = computeNeighbours(road_neighbours, nrows, ncols, roads, mask)
		
		for i in added_cells:
			covered[i] = 1
			
		
		#compute number of new cells that would be covered if that cell were added to that road
		#choose the best cell to add based on the criteria
		#remove that cell from neighbour_list
		#recompute covered cell
		#recompute neighbours list

	
	print("saving...")			
	util.saveFile(covered, 'covered', data_layers)
	util.saveFile(min_dist, 'min_dist', data_layers)
	util.saveFile(roads, 'roads', data_layers)
	util.saveFile(mask, 'mask', data_layers)


	return roads


def computeNeighbours(road_neighbours, nrows, ncols, roads, mask):
	for i in range(nrows):
		for j in range(ncols):
			cell = (i,j)
			if (roads[cell] == 1):
				neighbours_of_cell = util.getNeighbours(cell,mask)
				for neighbour in neighbours_of_cell:
					neighbour_tuple = (cell, neighbour)
					road_neighbours.add(neighbour_tuple)
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
	grid = util.fixFirstColRow(grid)
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