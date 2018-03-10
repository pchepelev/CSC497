import json
import sys

import models
import util

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage: %s <config file (JSON)>'%sys.argv[0])
		sys.exit()

	file_name = sys.argv[1]
	print ('Opening: ' + file_name.split('/')[-1])

	#get info from json
	with open(file_name, 'r') as f:
		json_dict = json.load(f)
	name = json_dict.get('area_name')
	layers = dict(json_dict.get('layers').items())
	search_radius = json_dict.get('search_radius')

	#get grid file
	roads = models.greedyAlgorithm(name,layers,search_radius)
	print("model created. saving file...")
	util.saveFile(roads, 'modeled_road', layers)