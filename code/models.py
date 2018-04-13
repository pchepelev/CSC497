import numpy
import collections
import time
import ctypes
import os
import sys

import util
import verifier

lib = ctypes.cdll.LoadLibrary('code/bfs.so')

compute_num_coverable_ij = lib.compute_num_coverable
limited_bfs = lib.limited_bfs
covered_bfs = lib.covered_bfs
inaccessible_bfs = lib.inaccessible_bfs

def bfs_limited(nrows, ncols, BCi, BCj, search_radius, covered, mask, benefit):
	
	covered = numpy.array(covered,dtype=numpy.int32)
	mask = numpy.array(mask,dtype=numpy.int32)
	benefit = numpy.array(benefit,dtype=numpy.int32)
	
	limited_bfs(ctypes.c_int(nrows), ctypes.c_int(ncols),
				ctypes.c_int(BCi), ctypes.c_int(BCj),
				ctypes.c_int(search_radius),
				ctypes.c_void_p(covered.ctypes.data),
				ctypes.c_void_p(mask.ctypes.data),
				ctypes.c_void_p(benefit.ctypes.data))
	
	return benefit
	

def ia_bfs (x,y,g1,g2):
	rows, cols = g1.shape
	grid = numpy.array(g1,dtype=numpy.int32)
	mask = numpy.array(g2,dtype=numpy.int32)
	inaccessible_bfs(ctypes.c_int(rows), ctypes.c_int(cols),
					 ctypes.c_int(x), ctypes.c_int(y),
					 ctypes.c_void_p(grid.ctypes.data),
					 ctypes.c_void_p(mask.ctypes.data))
	return mask
	
def compute_benefit_single_cell(roads, covered, mask, radius, i, j):
	rows, cols = roads.shape
	covered = numpy.array(covered,dtype=numpy.int32)
	mask = numpy.array(mask,dtype=numpy.int32)
	return compute_num_coverable_ij(ctypes.c_int(rows),ctypes.c_int(cols),ctypes.c_int(i),ctypes.c_int(j),
														  ctypes.c_int(radius),
														  ctypes.c_void_p(covered.ctypes.data),
														  ctypes.c_void_p(mask.ctypes.data))

def compute_num_coverable(roads, covered, mask, radius):
	rows, cols = roads.shape
	num_coverable = numpy.zeros(roads.shape,dtype=numpy.int32)
	covered = numpy.array(covered,dtype=numpy.int32)
	mask = numpy.array(mask,dtype=numpy.int32)
	for idx in range(roads.size):
		i = idx//cols
		j = idx%cols
		num_coverable[i,j] = compute_num_coverable_ij(ctypes.c_int(rows),ctypes.c_int(cols),ctypes.c_int(i),ctypes.c_int(j),
													  ctypes.c_int(radius),
													  ctypes.c_void_p(covered.ctypes.data),
													  ctypes.c_void_p(mask.ctypes.data))
	return num_coverable

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

#greedy algorithm with 2 tiebreakers
def greedyAlgorithm(name, data_layers,search_radius,access_point, save_period):
	print ("Running greedyAlgorithm on " + name)
	
	grid = util.ascToGrid(data_layers['mask'])
	ncols = (int(grid[0][-1]))
	nrows = (int(grid[1][-1]))
	cellsize = float(grid[4][-1])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	mask = numpy.array(grid)
	mask = ia_bfs(access_point[0],access_point[1],numpy.array(1-mask),mask)
	
	grid = util.ascToGrid(data_layers['roads'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	roads = numpy.array(grid)
	roads = numpy.multiply(mask,roads)
	util.saveFile(roads, 'input_roads', data_layers)
	
	grid = util.ascToGrid(data_layers['veg'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	veg = numpy.array(grid)
	
	
	for lyr in data_layers['inaccessible'].items():
		grid = util.ascToGrid(lyr[1])
		grid = util.removeHeader(grid)
		grid = util.changeToInt(grid)
		gridarray = numpy.array(grid)
		mask = ia_bfs(access_point[0],access_point[1],gridarray,mask)
	
	
	t1 = time.time()
	min_dist_grid = verifier.minDistForCells(roads, mask)
	t2 = time.time()
	print("get minimum distance from roads took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	dist_from_mask = verifier.minDistForCells(1-mask,mask)
	t2 = time.time()
	print("get minimum distance from mask took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	covered = numpy.zeros((nrows,ncols),dtype=numpy.int32)
	covered = computeCoveredGrid(min_dist_grid,search_radius)
	covered = (numpy.maximum(covered,numpy.array(1-veg)))
	t2 = time.time()
	print("init covered grid took ", "{:.3f}".format(t2-t1), "seconds")
	
	
	t1 = time.time()
	benefit = compute_num_coverable(roads,covered,mask,search_radius)
	t2 = time.time()
	print("init benefit grid took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	road_neighbours = set()
	road_neighbours = computeNeighbours(road_neighbours, nrows, ncols, roads, mask)
	t2 = time.time()
	print("compute Neighbours of roads took ", "{:.3f}".format(t2-t1), "seconds")
	x=0
	coveredCells = numpy.sum(covered)
	cellsInMask = numpy.sum(mask)
	
	print (x, coveredCells, cellsInMask)
	
	while (coveredCells < cellsInMask):
		#time.sleep(1)
		x+=1
		start = time.time()
		
		#t1 = time.time()
		min_dist_grid = verifier.minDistForCells(1-covered-(1-mask), mask)
		#t2 = time.time()
		#print("	generate min_dist grid took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		(best_cell,tied_set) = tied_greater_than(road_neighbours,benefit)
		if len(tied_set) > 1:
			(best_cell,tied_set) = tied_less_than(tied_set,min_dist_grid)
		if len(tied_set) > 1:
			best_cell = tied_less_than(tied_set,dist_from_mask)[0]
		#t2 = time.time()
		#print("	find best cell took ", "{:.3f}".format(t2-t1), "seconds")
	
	
		#t1 = time.time()
		#set best_cell to be a road
		roads[best_cell] = 1
		
		#get neighbours of best_cell, add them to the road_neighbours set, remove the best_cell
		#from the road_neighbours set since it is a road, not a neighbour
		new_neighbours = util.getNeighbours(best_cell, mask)
		for nbor in new_neighbours:
			if (roads[nbor] == 0):
				road_neighbours.add(nbor)
		road_neighbours.remove(best_cell)
		#t2 = time.time()
		#print("	place road on grid, update neighbours took", "{:.3f}".format(t2-t1), "seconds")
		
		
		#t1 = time.time()
		(BCi,BCj)=best_cell
		coveredCells += covered_bfs(ctypes.c_int(nrows), ctypes.c_int(ncols), 
									ctypes.c_int(BCi), ctypes.c_int(BCj), 
									ctypes.c_int(search_radius), 
									ctypes.c_void_p(covered.ctypes.data), 
									ctypes.c_void_p(mask.ctypes.data))
		#t2 = time.time()
		#print ("	recompute the covered cells grid took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		covered = numpy.array(covered,dtype=numpy.int32)
		mask = numpy.array(mask,dtype=numpy.int32)
		benefit = numpy.array(benefit,dtype=numpy.int32)
		
		limited_bfs(ctypes.c_int(nrows), ctypes.c_int(ncols),
					ctypes.c_int(BCi), ctypes.c_int(BCj),
					ctypes.c_int(search_radius),
					ctypes.c_void_p(covered.ctypes.data),
					ctypes.c_void_p(mask.ctypes.data),
					ctypes.c_void_p(benefit.ctypes.data))
		
		#t2 = time.time()
		#print ("	recompute the benefit grid ", "{:.3f}".format(t2-t1), "seconds")
				
		#save some intermediate modeled roads to show progress	
		if (save_period > 0 and (x%save_period==0 or x == 1)):
			util.saveFile(roads, 'intermediate_roads'+'%04d'%x, data_layers)
			util.saveFile(covered, 'intermediate_covered'+'%04d'%x, data_layers)
			#util.saveFile(benefit, 'intermediate_benefit'+'%04d'%x, data_layers)
			#util.saveFile(min_dist_grid, 'intermediate_tiebreak'+'%04d'%x, data_layers)

		#print (roads)
		end = time.time()
		print (x, coveredCells, cellsInMask, "{:.3f}".format(end-start), "seconds")
		
	return roads

def tied_greater_than(input_set, grid):
	best_num = -1
	best_cell = (-1,-1)
	tied_set = set()
	for cell in input_set:
		if (grid[cell] > best_num):
			best_cell = cell
			best_num = grid[cell]
			tied_set = {cell}
		elif grid[cell] == best_num:
			tied_set.add(cell)
	return (best_cell,tied_set)

def tied_less_than(input_set, grid):
	best_num = 99999
	best_cell = (-1,-1)
	tied_set = set()
	for cell in input_set:
		if (grid[cell] < best_num):
			best_cell = cell
			best_num = grid[cell]
			tied_set = {cell}
		elif grid[cell] == best_num:
			tied_set.add(cell)
	return (best_cell,tied_set)

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

def computeCoveredGrid(min_dist,search_radius):
	
	a = numpy.array(min_dist <= search_radius,dtype=numpy.int32)
	return a

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