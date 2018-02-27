import numpy
import itertools

file = open("vegc.asc", "r")

grid1 = []

for line in file:
	nline = line.strip('\n')
	a = nline.split(" ")[1:]
	grid1.append(a)

grid1 = grid1[6:]

grid = []

for x in grid1:
	grid.append([float(i) for i in x])
	
array = numpy.array(grid)

print(array)