# CSC 497 - Spring 2018 - Logging Road Algorithms

### Run algorithm
python3 code/run_model.py (config file (.json)) (search radius) (how often to save intermediate grids (0=don't save)) ('output_filename')

This runs the selected algorithm using the specified search radius and creates a grid file called output_filename.asc in the out directory that represents the generated road network

#### Algorithm choices:
0 - AlgorithmG

1 - AlgorithmS1

2 - AlgorithmS2

3 - AlgorithmR

4 - AlgorithmC


### Verify model
python3 code/verify.py (config file (.json)) (input network (.asc)) (search radius)

This validates and displays the statistics of input network 