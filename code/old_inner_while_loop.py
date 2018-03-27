		#for each neighbour in the neighbours of road cells
		for neighbour in road_neighbours:
			current_set = set()
			num_cells = 0
			queue = collections.deque()
			queue.appendleft((neighbour,0))
			#run a bfs from the neighbour to at most search radius distance from the neighbour
			while(queue):
				(cell,y) = queue.pop()
				for nbor in util.getNeighbours(cell, mask):
					if (y+1 < search_radius):
						queue.appendleft((nbor,y+1))
					if (covered[nbor] == 0):
						num_cells += 1
						current_set.add(nbor)
			#if the number of covered cells gained by the current neighbour is greater than
			#the number of covered cells gained by the best neighbour, replace the
			#best neighbour with the current neighbour
			if (num_cells > best_num):
				best_cell = neighbour
				best_set = current_set