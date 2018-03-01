import numpy
import json
import sys
import os
from shutil import copyfile

import models
import verifier


def saveFile(grid, name):
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

		
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print('Usage: %s <config file (JSON)>'%sys.argv[0])
		sys.exit()

	file_name = sys.argv[1]
	print ('Opening: ' + file_name.split('/')[-1])

	#get info from json
	with open(file_name, 'r') as f:
		json_dict = json.load(f)
	name = json_dict.get('area_name')
	layers = dict(json_dict.get('layers').items())
	radius = json_dict.get('search_radius')

	#get grid file
	roads = models.gridNetwork(name,layers,1500)
	saveFile(roads, 'grid')

	grid = models.ascToGrid(layers['mask'])
	grid = models.removeHeader(grid)
	grid = models.fixFirstColRow(grid)
	grid = models.changeToInt(grid)
	mask_grid = numpy.array(grid)

	grid = models.ascToGrid(u'out/grid.asc')
	grid = models.removeHeader(grid)
	grid = models.changeToInt(grid)
	network_grid = numpy.array(grid)

	bfs_grid = verifier.minDistForCells(network_grid, mask_grid)
	saveFile(bfs_grid, 'bfs')

	grid = models.ascToGrid(layers['mask'])
	cellsize = float(grid[4][-1])
	
	print(verifier.roadsOnMask(network_grid, mask_grid))
	print(verifier.costOfRoadNetwork(network_grid))
	print(verifier.avgDistForArea(bfs_grid,mask_grid))
	print(verifier.allCellsWithinRadius(bfs_grid, mask_grid, radius,cellsize))