import numpy
import json
import sys
import os
from shutil import copyfile

import models

if len(sys.argv) < 2:
	print('Usage: %s <config file (JSON)>'%sys.argv[0])
	sys.exit()

os.chdir("..")
file_name = sys.argv[1]
print ('Opening: ' + file_name.split('/')[-1])

#get info from json
with open(file_name, 'r') as f:
	json_dict = json.load(f)
name = json_dict.get('area_name')
layers = dict(json_dict.get('layers').items())
radius = json_dict.get('search_radius')

#get grid file
roads = models.gridNetwork(name,layers,radius)
numpy.savetxt(u'out/grid',roads,fmt='%d')

#get header file
with open(layers['elevation'],'r') as headerfile:
	with open(u'out/header','w') as outfile:
		for i in range(6):
			outfile.write(headerfile.readline())

#combine files
filenames = [u'out/header',u'out/grid']
with open(u'out/out.asc','w') as outfile:
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
	dst = (u'out/out' + i)
	copyfile(src, dst)
	
	
	
	