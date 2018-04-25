import numpy
import collections
import time
import ctypes
import os
import sys
import random

import util
import verifier

lib = ctypes.cdll.LoadLibrary('code/bfs.so')

compute_num_coverable_ij = lib.compute_num_coverable
limited_bfs = lib.limited_bfs
covered_bfs = lib.covered_bfs
inaccessible_bfs = lib.inaccessible_bfs
find_path = lib.find_path
find_path_benefit = lib.find_path_benefit

def run_algorithm(name, data_layers,search_radius,access_point, save_period, choice):
	if choice == 0:
		return greedyAlgorithm(name, data_layers,search_radius,access_point, save_period)
	elif choice == 1:
		return scragglyAlgorithm(name, data_layers,search_radius,access_point, save_period)
	elif choice == 2:
		return scragglyAlgorithmNew(name, data_layers,search_radius,access_point, save_period)
	elif choice == 3:
		return randomAlgorithm(name, data_layers,search_radius,access_point, save_period)
	elif choice == 4:
		return choosyAlgorithm(name, data_layers,search_radius,access_point, save_period)

def bfs_path_benefit(start, mask, min_dist, roads,benefit, radius,covered):
	rows,cols=mask.shape
	start_i,start_j=start
	neighbours = numpy.array(min_dist==1, dtype=numpy.int32)
	roads = numpy.array(roads, dtype=numpy.int32)
	benefit = numpy.array(benefit, dtype=numpy.int32)
	covered = numpy.array(covered, dtype=numpy.int32)
	find_path_benefit(ctypes.c_int(rows), ctypes.c_int(cols), 
			  ctypes.c_int(start_i), ctypes.c_int(start_j), 
			  ctypes.c_void_p(mask.ctypes.data),
			  ctypes.c_void_p(neighbours.ctypes.data),
			  ctypes.c_void_p(roads.ctypes.data),
			  ctypes.c_void_p(benefit.ctypes.data),
			  ctypes.c_int(radius),
			  ctypes.c_void_p(covered.ctypes.data))
	return (roads,benefit)

def bfs_path(start,mask,min_dist,roads):
	rows,cols=mask.shape
	start_i,start_j=start
	neighbours = numpy.array(min_dist==1, dtype=numpy.int32)
	roads = numpy.array(roads, dtype=numpy.int32)
	find_path(ctypes.c_int(rows), ctypes.c_int(cols), 
			  ctypes.c_int(start_i), ctypes.c_int(start_j), 
			  ctypes.c_void_p(mask.ctypes.data),
			  ctypes.c_void_p(neighbours.ctypes.data),
			  ctypes.c_void_p(roads.ctypes.data))
	return roads

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

def choosyAlgorithm(name, data_layers,search_radius,access_point, save_period):
	print ("Running AlgorithmC on " + name)
	algStart = time.time()
	
	t1 = time.time()
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
		mask = ia_bfs(access_point[0],access_point[1],numpy.array(1-mask),mask)
	
	grid = util.ascToGrid(data_layers['roads'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	roads = numpy.array(grid)
	roads = numpy.multiply(mask,roads)
	#util.saveFile(roads, 'input_roads', data_layers)
	
	grid = util.ascToGrid(data_layers['veg'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	veg = numpy.array(grid)
	t2 = time.time()
	print("data preprocessing took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	min_dist = verifier.minDistForCells(roads, mask)
	t2 = time.time()
	print("init minimum distance from roads took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	dist_from_mask = verifier.minDistForCells(1-mask,mask)
	t2 = time.time()
	print("init minimum distance from mask took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	covered = numpy.zeros((nrows,ncols),dtype=numpy.int32)
	covered = computeCoveredGrid(min_dist,mask,search_radius)
	covered = (numpy.maximum(covered,numpy.array((1-veg)-(1-mask))))
	t2 = time.time()
	print("init covered grid took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	benefit = compute_num_coverable(roads,covered,mask,search_radius)
	t2 = time.time()
	print("init benefit grid took ", "{:.3f}".format(t2-t1), "seconds")
	
	coveredCells = numpy.sum(covered)
	cellsInMask = numpy.sum(mask)
	count=0
	print (count, coveredCells, cellsInMask)
	while(coveredCells < cellsInMask):
	
		#start = time.time()
		
		#t1 = time.time()
		a = numpy.where(benefit == numpy.max(benefit))
		array_of_max_indices = numpy.transpose(a)
		best_cell = (array_of_max_indices[0][0],array_of_max_indices[0][1])
		if len(array_of_max_indices) > 1:
			tied_set = set()
			for cell in array_of_max_indices:
				tied_set.add((cell[0],cell[1]))
			(best_cell,tied_set) = tied_less_than(tied_set,min_dist)
			if len(tied_set) > 1:
				best_cell = tied_less_than(tied_set,dist_from_mask)[0]
		#t2 = time.time()
		#print("	choose best cell took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		roads,benefit = bfs_path_benefit(best_cell, mask, min_dist, roads,benefit, search_radius,covered)
		#t2 = time.time()
		#print("	get path list and put cells on grid took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		min_dist = verifier.minDistForCells(roads, mask)
		#t2 = time.time()
		#print("	recompute mindistforcells took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		covered = computeCoveredGrid(min_dist,mask,search_radius)
		covered = (numpy.maximum(covered,numpy.array((1-veg)-(1-mask))))
		coveredCells = numpy.sum(covered)
		#t2 = time.time()
		#print("	recompute covered grid took ", "{:.3f}".format(t2-t1), "seconds")
		
		if (save_period > 0 and (count%save_period==0 or count == 1)):
			util.saveFile(roads, 'intermediate_roads'+'%04d'%count, data_layers)
			util.saveFile(covered, 'intermediate_covered'+'%04d'%count, data_layers)
		
		#end = time.time()
		count+=1
		#print (count, coveredCells, cellsInMask, "{:.3f}".format(end-start), "seconds")
		
	algEnd = time.time()
	print("choosyAlgorithm took ", "{:.3f}".format(algEnd-algStart), "seconds")
	return roads

def randomAlgorithm(name, data_layers,search_radius,access_point, save_period):
	print ("Running AlgorithmR on " + name)
	algStart = time.time()
	
	t1 = time.time()
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
		mask = ia_bfs(access_point[0],access_point[1],numpy.array(1-mask),mask)
	
	grid = util.ascToGrid(data_layers['roads'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	roads = numpy.array(grid)
	roads = numpy.multiply(mask,roads)
	#util.saveFile(roads, 'input_roads', data_layers)
	
	grid = util.ascToGrid(data_layers['veg'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	veg = numpy.array(grid)
	t2 = time.time()
	print("data preprocessing took ", "{:.3f}".format(t2-t1), "seconds")
	
	
	t1 = time.time()
	min_dist = verifier.minDistForCells(roads, mask)
	t2 = time.time()
	print("init mindistforcells grid took ", "{:.3f}".format(t2-t1), "seconds")
	
	print("init covered grid...")
	t1 = time.time()
	covered = numpy.zeros((nrows,ncols),dtype=numpy.int32)
	covered = computeCoveredGrid(min_dist,mask,search_radius)
	covered = (numpy.maximum(covered,numpy.array((1-veg)-(1-mask))))
	t2 = time.time()
	print("init covered grid took ", "{:.3f}".format(t2-t1), "seconds")
	

	coveredCells = numpy.sum(covered)
	cellsInMask = numpy.sum(mask)
	count=0
	print (count, coveredCells, cellsInMask)
	while(coveredCells < cellsInMask):
	
		#start = time.time()
		
		#t1 = time.time()
		covered_with_mask=numpy.array(covered+(1-mask))
		uncovered_indices = numpy.where(covered_with_mask==0)
		uncovered_cells=[]
		for i,x in enumerate(uncovered_indices[0]):
			uncovered_cells.append((uncovered_indices[0][i],uncovered_indices[1][i]))
		#t2 = time.time()
		#print("	get uncovered cells took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		traversal_list = []
		random_choice = random.choice(uncovered_cells)
		uncovered_cells.remove(random_choice)
		#t2 = time.time()
		#print("	randomly choose cell took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		roads = bfs_path(random_choice,mask,min_dist,roads)
		#t2 = time.time()
		#print("	get path list and put cells on grid took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		min_dist = verifier.minDistForCells(roads, mask)
		#t2 = time.time()
		#print("	recompute mindistforcells took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		covered = computeCoveredGrid(min_dist,mask,search_radius)
		covered = (numpy.maximum(covered,numpy.array((1-veg)-(1-mask))))
		coveredCells = numpy.sum(covered)
		#t2 = time.time()
		#print("	recompute covered grid took ", "{:.3f}".format(t2-t1), "seconds")
		
		if (save_period > 0 and (count%save_period==0 or count == 1)):
			util.saveFile(roads, 'intermediate_roads'+'%04d'%count, data_layers)
			util.saveFile(covered, 'intermediate_covered'+'%04d'%count, data_layers)
		
		#end = time.time()
		count+=1
		#print (count, coveredCells, cellsInMask, "{:.3f}".format(end-start), "seconds")
	
	algEnd = time.time()
	print("randomAlgorithm took ", "{:.3f}".format(algEnd-algStart), "seconds")
	return roads

def scragglyAlgorithmNew(name, data_layers,search_radius,access_point, save_period):
	print ("Running AlgorithmS2 on " + name)
	algStart = time.time()
	
	t1 = time.time()
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
		mask = ia_bfs(access_point[0],access_point[1],numpy.array(1-mask),mask)
	
	grid = util.ascToGrid(data_layers['roads'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	roads = numpy.array(grid)
	roads = numpy.multiply(mask,roads)
	#util.saveFile(roads, 'input_roads', data_layers)
	
	grid = util.ascToGrid(data_layers['veg'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	veg = numpy.array(grid)
	t2 = time.time()
	print("data preprocessing took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	min_dist = verifier.minDistForCells(roads, mask)
	mdn = numpy.multiply(veg,min_dist)
	t2 = time.time()
	print("init min dist grids took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	covered = numpy.zeros((nrows,ncols),dtype=numpy.int32)
	covered = computeCoveredGrid(min_dist,mask,search_radius)
	covered = (numpy.maximum(covered,numpy.array((1-veg)-(1-mask))))
	t2 = time.time()
	print("init covered grid took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	cell = numpy.unravel_index(numpy.argmin(mdn + covered*100000 + 100000*(1-mask)),mdn.shape)
	t2 = time.time()
	print("get cell with min mindist, not counting covered or masked cells took ", "{:.3f}".format(t2-t1), "seconds")

	count = 0
	while numpy.max(mdn) > search_radius:
		#start = time.time()
		#print("   max:",min_dist[cell]," cell: ",cell,search_radius)
		
		roads[cell] = 1
		
		#t1 = time.time()
		while min_dist[cell] > 0:
			#tt1 = time.time()
			best_num = 999999
			neighbours = util.getNeighbours(cell, mask)
			for neighbour in neighbours:
				if min_dist[neighbour] < best_num:
					best_cell = neighbour
					best_num = min_dist[neighbour]
			cell = best_cell
			roads[cell] = 1
			#tt2 = time.time()
			#print("  find neighbour of best cell with lowest min dist, add it to network took ", "{:.3f}".format(tt2-tt1), "seconds")
		#t2 = time.time()
		#print(" trace path from best cell took ", "{:.3f}".format(t2-t1), "seconds")
			
		#t1 = time.time()
		min_dist = verifier.minDistForCells(roads, mask)
		mdn = numpy.multiply(veg,min_dist)
		#t2 = time.time()
		#print(" recompute mindistforcells took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		covered = computeCoveredGrid(min_dist,mask,search_radius)
		covered = (numpy.maximum(covered,numpy.array((1-veg)-(1-mask))))
		cell = numpy.unravel_index(numpy.argmin(mdn + covered*100000 + 100000*(1-mask)),mdn.shape)
		#t2 = time.time()
		#print(" recompute covered grid and get best cell took ", "{:.3f}".format(t2-t1), "seconds")
		
		if (save_period > 0 and (count%save_period==0 or count == 1)):
			util.saveFile(roads, 'intermediate_roads'+'%04d'%count, data_layers)
			util.saveFile(covered, 'intermediate_covered'+'%04d'%count, data_layers)
		
		#end = time.time()
		#print (count, "{:.3f}".format(end-start), "seconds")
		count+=1
	
	algEnd = time.time()
	print("scragglyAlgorithmNew took ", "{:.3f}".format(algEnd-algStart), "seconds")
	return roads

def scragglyAlgorithm(name, data_layers,search_radius,access_point, save_period):
	print ("Running AlgorithmS1 on " + name)
	algStart = time.time()
	
	t1 = time.time()
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
		mask = ia_bfs(access_point[0],access_point[1],numpy.array(1-mask),mask)
	
	grid = util.ascToGrid(data_layers['roads'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	roads = numpy.array(grid)
	roads = numpy.multiply(mask,roads)
	#util.saveFile(roads, 'input_roads', data_layers)
	
	grid = util.ascToGrid(data_layers['veg'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	veg = numpy.array(grid)
	t2 = time.time()
	print("data preprocessing took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	min_dist = verifier.minDistForCells(roads, mask)
	mdn = numpy.multiply(veg,min_dist)
	t2 = time.time()
	print("init min dist grids took ", "{:.3f}".format(t2-t1), "seconds")
	
	t1 = time.time()
	cell = numpy.unravel_index(numpy.argmax(mdn),mdn.shape)
	t2 = time.time()
	print("get cell with max min dist took ", "{:.3f}".format(t2-t1), "seconds")
	
	count = 0
	while numpy.max(mdn) > search_radius:
		#start = time.time()
		#print("   max:",min_dist[cell]," cell: ",cell,search_radius)
		
		roads[cell] = 1
		
		#t1 = time.time()
		while min_dist[cell] > 0:
			#tt1 = time.time()
			best_num = 999999
			neighbours = util.getNeighbours(cell, mask)
			for neighbour in neighbours:
				if min_dist[neighbour] < best_num:
					best_cell = neighbour
					best_num = min_dist[neighbour]
			cell = best_cell
			roads[cell] = 1
			#tt2 = time.time()
			#print("  find neighbour of best cell with lowest min dist, add it to network took ", "{:.3f}".format(tt2-tt1), "seconds")
		#t2 = time.time()
		#print(" trace path from best cell took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		min_dist = verifier.minDistForCells(roads, mask)
		mdn = numpy.multiply(veg,min_dist)
		cell = numpy.unravel_index(numpy.argmax(mdn),mdn.shape)
		#t2 = time.time()
		#print(" recompute mindistforcells and get best cell took ", "{:.3f}".format(t2-t1), "seconds")
		
		if (save_period > 0 and (count%save_period==0 or count == 1)):
			util.saveFile(roads, 'intermediate_roads'+'%04d'%count, data_layers)
		
		#end = time.time()
		#print (count, "{:.3f}".format(end-start), "seconds")
		count+=1
		
	algEnd = time.time()
	print("scragglyAlgorithm took ", "{:.3f}".format(algEnd-algStart), "seconds")
	return roads

def greedyAlgorithm(name, data_layers,search_radius,access_point, save_period):
	print ("Running AlgorithmG on " + name)
	algStart = time.time()
	
	t1 = time.time()
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
		mask = ia_bfs(access_point[0],access_point[1],numpy.array(1-mask),mask)
	
	grid = util.ascToGrid(data_layers['roads'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	roads = numpy.array(grid)
	roads = numpy.multiply(mask,roads)
	#util.saveFile(roads, 'input_roads', data_layers)
	
	grid = util.ascToGrid(data_layers['veg'])
	grid = util.removeHeader(grid)
	grid = util.changeToInt(grid)
	veg = numpy.array(grid)
	t2 = time.time()
	print("data preprocessing took ", "{:.3f}".format(t2-t1), "seconds")
	
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
	covered = computeCoveredGrid(min_dist_grid,mask,search_radius)
	covered = (numpy.maximum(covered,numpy.array((1-veg)-(1-mask))))
	
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
		x+=1
		if x%250==0:
			start = time.time()
		
		#t1 = time.time()
		dist_from_uncovered = verifier.minDistForCells(1-covered-(1-mask), mask)
		#t2 = time.time()
		#print("	generate distance from uncovered cell grid took ", "{:.3f}".format(t2-t1), "seconds")
		
		#t1 = time.time()
		(best_cell,tied_set) = tied_greater_than(road_neighbours,benefit)
		if len(tied_set) > 1:
			(best_cell,tied_set) = tied_less_than(tied_set,dist_from_uncovered)
			if len(tied_set) > 1:
				best_cell = tied_less_than(tied_set,dist_from_mask)[0]
		#t2 = time.time()
		#print("	find best cell took ", "{:.3f}".format(t2-t1), "seconds")
	
		#t1 = time.time()
		'''set best_cell to be a road'''
		roads[best_cell] = 1
			
		'''get neighbours of best_cell, add them to the road_neighbours set, remove the best_cell
		   from the road_neighbours set since it is a road, not a neighbour'''
		new_neighbours = util.getNeighbours(best_cell, mask)
		for nbor in new_neighbours:
			if (roads[nbor] == 0):
				road_neighbours.add(nbor)
		road_neighbours.remove(best_cell)
		#t2 = time.time()
		#print("	place road on grid, update neighbours took", "{:.3f}".format(t2-t1), "seconds")

		#t1 = time.time()
		covered = numpy.array(covered,dtype=numpy.int32)
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
		#print ("	recompute the benefit grid took ", "{:.3f}".format(t2-t1), "seconds")
		
		'''save some intermediate modeled roads to show progress'''
		if (save_period > 0 and (x%save_period==0 or x == 1)):
			util.saveFile(roads, 'intermediate_roads'+'%04d'%x, data_layers)
			util.saveFile(covered, 'intermediate_covered'+'%04d'%x, data_layers)
			#util.saveFile(benefit, 'intermediate_benefit'+'%04d'%x, data_layers)
			#util.saveFile(min_dist_grid, 'intermediate_tiebreak'+'%04d'%x, data_layers)

		
		if x%250==0:
			end = time.time()	
			print (x, coveredCells, cellsInMask, "{:.3f}".format(end-start), "seconds")

	algEnd = time.time()
	print("greedyAlgorithm took ", "{:.3f}".format(algEnd-algStart), "seconds")
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

def computeCoveredGrid(min_dist,mask,search_radius):
	
	a = numpy.array(min_dist <= search_radius,dtype=numpy.int32)
	return(a-(1-mask))
