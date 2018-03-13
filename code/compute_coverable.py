
import numpy
import ctypes
import verifier

lib = ctypes.cdll.LoadLibrary('./compute_num_coverable.so')
compute_num_coverable_ij = lib.compute_num_coverable


def compute_num_coverable(roads, covered, mask, radius):
	rows, cols = roads.shape
	num_coverable = numpy.zeros(roads.shape,dtype=numpy.int32)
	covered = numpy.array(covered,dtype=numpy.int32)
	mask = numpy.array(mask,dtype=numpy.int32)
	for idx in range(roads.size):
		i = idx//cols
		j = idx%cols
		num_coverable[i,j] = compute_num_coverable_ij(ctypes.c_int(rows),ctypes.c_int(cols),ctypes.c_int(i),ctypes.c_int(j),
													  ctypes.c_int(radius),
													  ctypes.c_void_p(covered.ctypes.data),
													  ctypes.c_void_p(mask.ctypes.data))
	return num_coverable
	

if __name__ == '__main__':
	test_array = numpy.array((
			(0,0,0,0,0,0,0,0),
			(0,0,0,0,0,0,0,0),
			(0,0,0,0,0,0,0,0),
			(1,1,1,1,0,0,0,0),
			(0,0,0,1,0,0,0,0),
			(0,0,0,1,1,1,1,1),
			(0,0,0,0,0,0,0,0),
			(0,0,0,0,0,0,0,0) ), dtype=numpy.int32)
	test_mask = numpy.zeros(test_array.shape, dtype=numpy.int32) + 1
	
	test_radius = 2

	min_dist = verifier.minDistForCells(test_array,test_mask)
	
	test_covered = numpy.array(min_dist <= test_radius, dtype=numpy.int32)
	
	test_coverable_counts = compute_num_coverable(test_array,test_covered,test_mask, test_radius)
	
	print("Test Roads")
	print(test_array)
	print("Test Covered")
	print(test_covered)
	print("Test Coverable Counts")
	print(test_coverable_counts)