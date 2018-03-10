import numpy
import os
from shutil import copyfile

#save the numpy grid  to filename name, using layers
def saveFile(grid, name, layers):
	numpy.savetxt(u'out/numbers',grid,fmt='%d')
	
	#get header file
	with open(layers['elevation'],'r') as headerfile:
		with open(u'out/header','w') as outfile:
			for i in range(6):
				outfile.write(headerfile.readline())
	
	#combine files
	filenames = [u'out/header',u'out/numbers']
	with open(u'out/'+name+'.asc','w') as outfile:
		for fname in filenames:
			with open(fname) as infile:
				for line in infile:
					outfile.write(line)
	
	
	#remove temp files
	for i in filenames:
		os.remove(i)
	
	#copy aux files to out
	extensions = ['.prj','.asc.aux.xml']
	for i in extensions:
		src = (layers['mask'].split('.')[0]+i)
		dst = (u'out/'+name + i)
		copyfile(src, dst)

#if the mask has ones in the first row and column, this returns a version with zeros in those spots
def fixFirstColRow(grid):
	for i in range(len(grid)):
		grid[i][0] = '0'
	for i in range(len(grid[0])):
		grid[0][i] = '0'
	return grid

#takes a python 2D list and returns one without the first 6 lines
def removeHeader(grid):
	return grid[6:]
	
#takes a 2D list with string values and returns a 2D list with int values
def changeToInt(grid):
	for i in range(len(grid)):
		for j in range(len(grid[0])):
			grid[i][j] = int(grid[i][j])
	return grid

#takes an .asc file and returns a python 2D list
def ascToGrid(filename):
	with open(filename,'r') as mask_file:
		grid = []
		for line in mask_file:
			nline = line.strip('\n')
			if (nline.split(" ")[0] == ''):
				a = nline.split(" ")[1:]
			else:
				a = nline.split(" ")
			grid.append(a)
	return grid
	
#returns a 2D list of 0s with specified dimensions
def zeros(ncols,nrows):
	return [[0 for col in range(ncols)] for row in range(nrows)]

#returns a list of points that are neighbours of cell 
def getNeighbours(cell, mask):
	list = []
	rows,cols = mask.shape
	

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