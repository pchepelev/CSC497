# CSC 497 - Spring 2018 - Logging Road Algorithms

## How to run (example)
From root directory:

### Run model
python3 code/run_model.py data/wells_gray/wells_gray.json

This creates a grid file called modeled_road.asc in the out directory, that represents the road network

### Verify model
python3 code/verify.py data/wells_gray/wells_gray.json out/modeled_road.asc

This shows some statistics and outputs a grid file called bfs.asc in the out directory, that shows the traversal distance each cell from a road cell


## Information
Tool developed on python 3.5
Google Earth KML files in data/* directories