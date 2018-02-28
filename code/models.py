import numpy

#returns numpy array of zeros with dimensions based on data_layers
def dummyNetwork(name,data_layers):
	print('Running dummyNetwork on ' + name)
	grid = ascToGrid(data_layers['mask'])
	ncols = (int(grid[0][-1]))
	nrows = (int(grid[1][-1]))
	return numpy.zeros((ncols,nrows))

#returns an numpy array, spaced by search_radius,
#based on the mask in data_layers
def gridNetwork(name, data_layers, search_radius):
	print('Running gridNetwork on ' + name)

	grid = ascToGrid(data_layers['mask'])
	ncols = (int(grid[0][-1]))
	nrows = (int(grid[1][-1]))
	cellsize = float(grid[4][-1])
	cell_dist = int(search_radius/cellsize)
	
	grid = removeHeader(grid)
	grid = fixFirstColRow(grid)
	grid = changeToInt(grid)
	mask = numpy.array(grid)
	
	roads_list = zeros(ncols,nrows)
	roads_list = genGrid(roads_list,cell_dist)
	roads = numpy.array(roads_list)
	
	masked_roads = numpy.multiply(roads,mask)
	
	return(masked_roads)

#returns a 2D list with 1s in a grid pattern (grid separation = sep)
def genGrid (grid, sep):
	for i in range(len(grid)):
		for j in range(len(grid[0])):
			if (i%sep==0 or j%sep==0):
				grid[i][j]=1
	return grid

#returns a 2D list of 0s with specified dimensions
def zeros(ncols,nrows):
	return [[0 for col in range(ncols)] for row in range(nrows)]

#takes a 2D list with string values and returns a 2D list with int values
def changeToInt(grid):
	for i in range(len(grid)):
		for j in range(len(grid[0])):
			grid[i][j] = int(grid[i][j])
	return grid

#if the mask has ones in the first row and column, this returns a version
#with zeros in those spots
def fixFirstColRow(grid):
	for i in range(len(grid)):
		grid[i][0] = '0'
	for i in range(len(grid[0])):
		grid[0][i] = '0'
	return grid

#takes a python 2D list and returns one without the first 6 lines
def removeHeader(grid):
	return grid[6:]

#takes an .asc file and returns a python 2D list
def ascToGrid(filename):
	with open(filename,'r') as mask_file:
		grid = []
		for line in mask_file:
			nline = line.strip('\n')
			a = nline.split(" ")[1:]
			grid.append(a)
	return grid