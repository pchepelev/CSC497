import json
import sys

import models
import util

if __name__ == '__main__':
	if len(sys.argv) < 3:
		print('Usage: %s <config file (JSON)> <How often to save intermediate grids (0: don\'t save)>'%sys.argv[0])
		sys.exit()

	file_name = sys.argv[1]
	save_period = int(sys.argv[2])
	print ('Opening: ' + file_name.split('/')[-1])

	#get info from json
	with open(file_name, 'r') as f:
		json_dict = json.load(f)
	name = json_dict.get('area_name')
	layers = dict(json_dict.get('layers').items())
	search_radius = json_dict.get('search_radius')

	#get grid file
	roads = models.greedyAlgorithm2TB(name, layers,search_radius, save_period)
	print("model created. saving file...")
	util.saveFile(roads, 'modeled_road', layers)