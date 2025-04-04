import json
import sys

import models
import util

if __name__ == '__main__':
	
	if len(sys.argv) < 6:
		print('Usage: %s <config file (JSON)> <search radius> <How often to save intermediate grids (0: don\'t save)> <algorithm choice> <output filename>'%sys.argv[0])
		sys.exit()

	file_name = sys.argv[1]
	search_radius = int(sys.argv[2])
	save_period = int(sys.argv[3])
	choice = int(sys.argv[4])
	print ('Opening: ' + file_name.split('/')[-1])

	#get info from json
	with open(file_name, 'r') as f:
		json_dict = json.load(f)
	name = json_dict.get('area_name')
	layers = dict(json_dict.get('layers').items())
	access_point = (int(json_dict.get('access_point_y')),int(json_dict.get('access_point_x')))

	#get grid file
	roads = models.run_algorithm(name, layers,search_radius,access_point, save_period, choice)
	print("model created. saving file...")
	util.saveFile(roads, sys.argv[5], layers)