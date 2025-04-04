#include <stdio.h>
#include <stdlib.h>

//Compile this with: gcc -O3 -o code/bfs.so -fPIC -shared code/bfs.c

typedef struct{
	int i,j;
} GridIndex;

void print_array(int rows, int cols, int grid[rows][cols]) {
	int i,j;
	for(i=0;i<rows;i++){
		for(j=0;j<cols;j++){
			printf("%d ",grid[i][j]);
		}
		printf("\n");
	}
}

int get_nearest_road_index (int rows, int cols, int start_i, int start_j, int mask[rows][cols],int roads[rows][cols], int index[2]) {
	
	int i,j;
	
	int dist[rows][cols];
	for (i = 0; i < rows; i++){
		for (j = 0; j < cols; j++){
			dist[i][j] = -1;
		}
	}
	
	GridIndex queue[rows*cols];
	int queue_start = 0;
	int queue_end = 0;
	
	GridIndex first_cell = {start_i, start_j};
	queue[0] = first_cell;
	queue_end++;
	dist[start_i][start_j] = 0;
	
	while(queue_start < queue_end){
		GridIndex cell = queue[queue_start];
		queue_start++;
		i = cell.i;
		j = cell.j;
		
		if(roads[i][j]==1) {
			
			index[0] = i;
			index[1] = j;
			return -22;
			
		}
	
		if (!mask[i][j]) //If mask = 0, the cell is invalid
			continue;
		
		if (i+1 < rows){
			if (mask[i+1][j] == 1) {
				if (dist[i+1][j]==-1) {
					GridIndex next_cell = {i+1,j};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i+1][j] = dist[i][j] + 1;
				}
			}
		}
		if (i-1 >= 0){
			if (mask[i-1][j] == 1) {
				if (dist[i-1][j]==-1) {
					GridIndex next_cell = {i-1,j};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i-1][j] = dist[i][j] + 1;
				}
			}
		}
		if (j+1 < cols){
			if (mask[i][j+1] == 1) {
				if (dist[i][j+1]==-1) {
					GridIndex next_cell = {i,j+1};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i][j+1] = dist[i][j] + 1;
				}
			}
		}
		if (j-1 >= 0){
			if (mask[i][j-1] == 1) {
				if (dist[i][j-1]==-1) {
					GridIndex next_cell = {i,j-1};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i][j-1] = dist[i][j] + 1;
				}
			}
		}
	}
	
	return -9999;
}

int find_path (int rows, int cols, int start_i, int start_j, int mask[rows][cols],int neighbours[rows][cols],int roads[rows][cols]) {
	
	int i,j;
	
	
	int dist[rows][cols];
	int prev[rows][cols];
	for (i = 0; i < rows; i++){
		for (j = 0; j < cols; j++){
			dist[i][j] = -1;
			prev[i][j] = -1;
		}
	}
	
	GridIndex queue[rows*cols];
	int queue_start = 0;
	int queue_end = 0;
	
	GridIndex first_cell = {start_i, start_j};
	queue[0] = first_cell;
	queue_end++;
	dist[start_i][start_j] = 0;
	
	while(queue_start < queue_end){
		GridIndex cell = queue[queue_start];
		queue_start++;
		i = cell.i;
		j = cell.j;
		
		if(neighbours[i][j]==1) {
			
			int x,y,prev_idx;
			x=i;
			y=j;
			roads[x][y] = 1;
			prev_idx = prev[x][y];
			
			while (prev_idx >= 0) {
				x = prev_idx / cols;
				y = prev_idx % cols;
				
				roads[x][y] = 1;
				prev_idx = prev[x][y];
			}
			
			return -22;
		}
		
		
		if (!mask[i][j]) //If mask = 0, the cell is invalid
			continue;
		
		if (i+1 < rows){
			if (mask[i+1][j] == 1) {
				if (dist[i+1][j]==-1) {
					GridIndex next_cell = {i+1,j};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i+1][j] = dist[i][j] + 1;
					prev[i+1][j] = i*cols+j;
				}
			}
		}
		if (i-1 >= 0){
			if (mask[i-1][j] == 1) {
				if (dist[i-1][j]==-1) {
					GridIndex next_cell = {i-1,j};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i-1][j] = dist[i][j] + 1;
					prev[i-1][j] = i*cols+j;
				}
			}
		}
		if (j+1 < cols){
			if (mask[i][j+1] == 1) {
				if (dist[i][j+1]==-1) {
					GridIndex next_cell = {i,j+1};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i][j+1] = dist[i][j] + 1;
					prev[i][j+1] = i*cols+j;
				}
			}
		}
		if (j-1 >= 0){
			if (mask[i][j-1] == 1) {
				if (dist[i][j-1]==-1) {
					GridIndex next_cell = {i,j-1};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i][j-1] = dist[i][j] + 1;
					prev[i][j-1] = i*cols+j;
				}
			}
		}
	}
	
	return -9999;
}

int inaccessible_bfs (int rows, int cols, int start_i, int start_j, int grid[rows][cols], int mask[rows][cols]) {
	int i,j;
	int visited[rows][cols];
	for(i=0;i<rows;i++)
		for(j=0;j<cols;j++)
			visited[i][j]=0;

	
	GridIndex queue[rows*cols];
	GridIndex first_cell = {start_i, start_j};
	int q_start = 0;
	int q_end = 0;
	queue[0] = first_cell;
	q_end++;
	
	while (q_start < q_end) {
		GridIndex cell = queue[q_start];
		q_start++;
		
		i = cell.i;
		j = cell.j;
		
		
		if (grid[i][j]==1)
			continue;
		
		if (i+1 < rows) {
			if (visited[i+1][j] == 0) {
				if (grid[i+1][j] == 0) {
					GridIndex next_cell = {i+1,j};
					queue[q_end] = next_cell;
					q_end++;
					visited[i+1][j]=1;
				}
			}
		}
		
		if (i-1 >= 0) {
			if (visited[i-1][j] == 0) {
				if (grid[i-1][j] == 0) {
					GridIndex next_cell = {i-1,j};
					queue[q_end] = next_cell;
					q_end++;
					visited[i-1][j] = 1;
				}
			}
		}
		
		if (j+1 < cols) {
			if (visited[i][j+1] == 0) {
				if (grid[i][j+1] == 0) {
					GridIndex next_cell = {i,j+1};
					queue[q_end] = next_cell;
					q_end++;
					visited[i][j+1]=1;
				}
			}
		}
		
		if (j-1 >= 0) {
			if (visited[i][j-1] == 0) {
				if (grid[i][j-1] == 0) {
					GridIndex next_cell = {i,j-1};
					queue[q_end] = next_cell;
					q_end++;
					visited[i][j-1]=1;
				}
			}
		}
		
	}
	
	for(i=0;i<rows;i++){
		for(j=0;j<cols;j++){
			if(visited[i][j]==0){
				mask[i][j]=0;
			}
		}
	}
	
	return -1;
}

int covered_bfs (int rows, int cols, int start_i, int start_j, int radius, int covered[rows][cols], int mask[rows][cols]) {
	int i,j;
	int count = 0;
	
	int dist[rows][cols];
	for (i=0;i<rows;i++)
		for (j=0;j<cols;j++)
			dist[i][j]=-1;
	dist[start_i][start_j] = 0;
	
	GridIndex queue[rows*cols];
	GridIndex first_cell = {start_i, start_j};
	int q_start = 0;
	int q_end = 0;
	queue[0] = first_cell;
	q_end++;
	
	while (q_start < q_end) {
		GridIndex cell = queue[q_start];
		q_start++;
		
		i = cell.i;
		j = cell.j;
		
		if (mask[i][j] == 0)
			continue;
		if (dist[i][j] >= radius)
			continue;
		
		
		if (i+1 < rows){
			if (dist[i+1][j] < 0){
				if (mask[i+1][j] == 1) {
					GridIndex next_cell = {i+1,j};
					queue[q_end] = next_cell;
					q_end++;
					dist[i+1][j] = dist[i][j] + 1;
					if (covered[i+1][j] == 0) {
						covered[i+1][j] = 1;
						count++;
					}
				}
			}
		}
		
		if (i-1 >= 0){
			if (dist[i-1][j] < 0){
				if (mask[i-1][j] == 1) {
					GridIndex next_cell = {i-1,j};
					queue[q_end] = next_cell;
					q_end++;
					dist[i-1][j] = dist[i][j] + 1;
					if (covered[i-1][j] ==0) {
						covered[i-1][j] = 1;
						count++;
					}
				}
			}
		}
		
		if (j+1 < cols){
			if (dist[i][j+1] < 0){
				if (mask[i][j+1] == 1) {
					GridIndex next_cell = {i,j+1};
					queue[q_end] = next_cell;
					q_end++;
					dist[i][j+1] = dist[i][j] + 1;
					if (covered[i][j+1] ==0) {
						covered[i][j+1] = 1;
						count++;
					}
				}
			}
		}
		
		if (j-1 >= 0){
			if (dist[i][j-1] < 0){
				if (mask[i][j-1] == 1) {
					GridIndex next_cell = {i,j-1};
					queue[q_end] = next_cell;
					q_end++;
					dist[i][j-1] = dist[i][j] + 1;
					if (covered[i][j-1] ==0) {
						covered[i][j-1] = 1;
						count++;
					}
				}
			}
		}
		
	}
	
	return count;
}

int covered_bfs_list (int rows, int cols, int radius, int covered[rows][cols], int mask[rows][cols], GridIndex list[rows*cols]) {
	int i,j,x,y;
	int count = 0;
	
	int dist[rows][cols];
	for (i=0;i<rows;i++)
		for (j=0;j<cols;j++)
			dist[i][j]=-1;
	
	GridIndex queue[rows*cols];
	int q_start = 0;
	int q_end = 0;
	
	for (i = 0; i < rows*cols; i++) {
		if (list[i].i == -1)
			break;
		x = list[i].i;
		y = list[i].j;
		dist[x][y] = 0;
		queue[q_end].i = x;
		queue[q_end].j = y;
		q_end++;
		covered[x][y] = 1;
	}
	
	
	while (q_start < q_end) {
		GridIndex cell = queue[q_start];
		q_start++;
		
		i = cell.i;
		j = cell.j;
		
		if (mask[i][j] == 0)
			continue;
		if (dist[i][j] >= radius)
			continue;
		
		
		if (i+1 < rows){
			if (dist[i+1][j] < 0){
				if (mask[i+1][j] == 1) {
					GridIndex next_cell = {i+1,j};
					queue[q_end] = next_cell;
					q_end++;
					dist[i+1][j] = dist[i][j] + 1;
					if (covered[i+1][j] == 0) {
						covered[i+1][j] = 1;
						count++;
					}
				}
			}
		}
		
		if (i-1 >= 0){
			if (dist[i-1][j] < 0){
				if (mask[i-1][j] == 1) {
					GridIndex next_cell = {i-1,j};
					queue[q_end] = next_cell;
					q_end++;
					dist[i-1][j] = dist[i][j] + 1;
					if (covered[i-1][j] ==0) {
						covered[i-1][j] = 1;
						count++;
					}
				}
			}
		}
		
		if (j+1 < cols){
			if (dist[i][j+1] < 0){
				if (mask[i][j+1] == 1) {
					GridIndex next_cell = {i,j+1};
					queue[q_end] = next_cell;
					q_end++;
					dist[i][j+1] = dist[i][j] + 1;
					if (covered[i][j+1] ==0) {
						covered[i][j+1] = 1;
						count++;
					}
				}
			}
		}
		
		if (j-1 >= 0){
			if (dist[i][j-1] < 0){
				if (mask[i][j-1] == 1) {
					GridIndex next_cell = {i,j-1};
					queue[q_end] = next_cell;
					q_end++;
					dist[i][j-1] = dist[i][j] + 1;
					if (covered[i][j-1] ==0) {
						covered[i][j-1] = 1;
						count++;
					}
				}
			}
		}
		
	}
	
	return count;
}

int compute_num_coverable( int rows, int cols, int start_i, int start_j, int radius, int covered[rows][cols], int mask[rows][cols] ){
	
	int i,j;
	GridIndex queue[rows*cols];
	int queue_start = 0;
	int queue_end = 0;
	
	int dist[rows][cols];	

	for (i = 0; i < rows; i++){
		for (j = 0; j < cols; j++){
			dist[i][j] = -1;
		}
	}
	
	GridIndex first_cell = {start_i, start_j};
	queue[0] = first_cell;
	queue_end++;
	dist[start_i][start_j] = 0;
	
	int total_found = 0;
	
	while(queue_start < queue_end){
		GridIndex cell = queue[queue_start];
		queue_start++;
		
		i = cell.i;
		j = cell.j;
		if (!mask[i][j]) //If mask = 0, the cell is invalid
			continue;
		if (dist[i][j] > radius)
			continue;
	
		if (!covered[i][j])
			total_found++;
		
		//Test each neighbour
		if (i+1 < rows){
			if (dist[i+1][j] < 0){
				if (mask[i+1][j] == 1) {
					GridIndex next_cell = {i+1,j};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i+1][j] = dist[i][j] + 1;
				}
				
			}
		}
		
		if (i-1 >= 0){
			if (dist[i-1][j] < 0){
				if (mask[i-1][j] == 1) {
					GridIndex next_cell = {i-1,j};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i-1][j] = dist[i][j] + 1;
				}
			}
		}
		
		if (j+1 < cols){
			if (dist[i][j+1] < 0){
				if (mask[i][j+1] == 1) {
					GridIndex next_cell = {i,j+1};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i][j+1] = dist[i][j] + 1;
				}
			}
		}
		
		if (j-1 >= 0){
			if (dist[i][j-1] < 0){
				if (mask[i][j-1] == 1) {
					GridIndex next_cell = {i,j-1};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i][j-1] = dist[i][j] + 1;
				}
			}
		}
		
		
	}
	
	return total_found;
	
	
}

int limited_bfs(int rows, int cols, int start_i, int start_j, int radius, int covered[rows][cols], int mask[rows][cols], int benefit[rows][cols]) {
	int i,j;
	int limit = 2*radius+1;
	
	int dist[rows][cols];
	for (i=0;i<rows;i++)
		for (j=0;j<cols;j++)
			dist[i][j]=-1;
	dist[start_i][start_j] = 0;
	
	GridIndex queue[rows*cols];
	GridIndex first_cell = {start_i, start_j};
	int q_start = 0;
	int q_end = 0;
	queue[0] = first_cell;
	q_end++;
	
	while (q_start < q_end) {
		GridIndex cell = queue[q_start];
		q_start++;
		
		i = cell.i;
		j = cell.j;
		
		if (mask[i][j] == 0)
			continue;
		if (dist[i][j] >= limit)
			continue;
		
		
		if (i+1 < rows){
			if (dist[i+1][j] < 0){
				if (mask[i+1][j] == 1) {
					GridIndex next_cell = {i+1,j};
					queue[q_end] = next_cell;
					q_end++;
					dist[i+1][j] = dist[i][j] + 1;
					benefit[i+1][j] = compute_num_coverable(rows, cols, i+1, j, radius, covered, mask);
				}
			}
		}
		
		if (i-1 >= 0){
			if (dist[i-1][j] < 0){
				if (mask[i-1][j] == 1) {
					GridIndex next_cell = {i-1,j};
					queue[q_end] = next_cell;
					q_end++;
					dist[i-1][j] = dist[i][j] + 1;
					benefit[i-1][j] = compute_num_coverable(rows, cols, i-1, j, radius, covered, mask);
				}
			}
		}
		
		if (j+1 < cols){
			if (dist[i][j+1] < 0){
				if (mask[i][j+1] == 1) {
					GridIndex next_cell = {i,j+1};
					queue[q_end] = next_cell;
					q_end++;
					dist[i][j+1] = dist[i][j] + 1;
					benefit[i][j+1] = compute_num_coverable(rows, cols, i, j+1, radius, covered, mask);
				}
			}
		}
		
		if (j-1 >= 0){
			if (dist[i][j-1] < 0){
				if (mask[i][j-1] == 1) {
					GridIndex next_cell = {i,j-1};
					queue[q_end] = next_cell;
					q_end++;
					dist[i][j-1] = dist[i][j] + 1;
					benefit[i][j-1] = compute_num_coverable(rows, cols, i, j-1, radius, covered, mask);
				}
			}
		}
		
	}
	
	return -1;
}

int limited_bfs_list(int rows, int cols, int radius, int covered[rows][cols], int mask[rows][cols], int benefit[rows][cols], GridIndex list[rows*cols]) {
	int i,j,x,y;
	int limit = 2*radius+1;
	
	int dist[rows][cols];
	for (i=0;i<rows;i++)
		for (j=0;j<cols;j++)
			dist[i][j]=-1;
	
	
	GridIndex queue[rows*cols];
	int q_start = 0;
	int q_end = 0;
	
	for (i = 0; i < rows*cols; i++) {
		if (list[i].i == -1)
			break;
		x = list[i].i;
		y = list[i].j;
		dist[x][y] = 0;
		queue[q_end].i = x;
		queue[q_end].j = y;
		q_end++;
		benefit[x][y] = 0;
	}
	
	while (q_start < q_end) {
		GridIndex cell = queue[q_start];
		q_start++;
		
		i = cell.i;
		j = cell.j;
		
		if (mask[i][j] == 0)
			continue;
		if (dist[i][j] >= limit)
			continue;
		
		if (i+1 < rows){
			if (dist[i+1][j] < 0){
				if (mask[i+1][j] == 1) {
					GridIndex next_cell = {i+1,j};
					queue[q_end] = next_cell;
					q_end++;
					dist[i+1][j] = dist[i][j] + 1;
					benefit[i+1][j] = compute_num_coverable(rows, cols, i+1, j, radius, covered, mask);
				}
			}
		}
		
		if (i-1 >= 0){
			if (dist[i-1][j] < 0){
				if (mask[i-1][j] == 1) {
					GridIndex next_cell = {i-1,j};
					queue[q_end] = next_cell;
					q_end++;
					dist[i-1][j] = dist[i][j] + 1;
					benefit[i-1][j] = compute_num_coverable(rows, cols, i-1, j, radius, covered, mask);
				}
			}
		}
		
		if (j+1 < cols){
			if (dist[i][j+1] < 0){
				if (mask[i][j+1] == 1) {
					GridIndex next_cell = {i,j+1};
					queue[q_end] = next_cell;
					q_end++;
					dist[i][j+1] = dist[i][j] + 1;
					benefit[i][j+1] = compute_num_coverable(rows, cols, i, j+1, radius, covered, mask);
				}
			}
		}
		
		if (j-1 >= 0){
			if (dist[i][j-1] < 0){
				if (mask[i][j-1] == 1) {
					GridIndex next_cell = {i,j-1};
					queue[q_end] = next_cell;
					q_end++;
					dist[i][j-1] = dist[i][j] + 1;
					benefit[i][j-1] = compute_num_coverable(rows, cols, i, j-1, radius, covered, mask);
				}
			}
		}
		
	}
	
	return -1;
}

int full_bfs( int rows, int cols, int mask[rows][cols], int roads[rows][cols], int dist[rows][cols] ){
	
	GridIndex queue[rows*cols];
	int q_start = 0;
	int q_end = 0;
	
	int i,j;
	for (i = 0; i < rows; i++) {
		for (j = 0; j < cols; j++) {
			if (roads[i][j] == 1) {
				dist[i][j] = 0;
				queue[q_end].i = i;
				queue[q_end].j = j;
				q_end++;
			}
		}
	}
	
	while (q_start<q_end) {
		GridIndex cell = queue[q_start];
		q_start++;
		i = cell.i;
		j = cell.j;
		if (mask[i][j] == 0)
			continue;

		if (i+1 < rows){
			if (dist[i+1][j] < 0){
				if (mask[i+1][j] == 1) {
					GridIndex next_cell = {i+1,j};
					queue[q_end] = next_cell;
					q_end++;
					dist[i+1][j] = dist[i][j] + 1;
				}
			}
		}
		
		if (i-1 >= 0){
			if (dist[i-1][j] < 0){
				if (mask[i-1][j] == 1) {
					GridIndex next_cell = {i-1,j};
					queue[q_end] = next_cell;
					q_end++;
					dist[i-1][j] = dist[i][j] + 1;
				}
			}
		}
		
		if (j+1 < cols){
			if (dist[i][j+1] < 0){
				if (mask[i][j+1] == 1) {
					GridIndex next_cell = {i,j+1};
					queue[q_end] = next_cell;
					q_end++;
					dist[i][j+1] = dist[i][j] + 1;
				}
			}
		}
		
		if (j-1 >= 0){
			if (dist[i][j-1] < 0){
				if (mask[i][j-1] == 1) {
					GridIndex next_cell = {i,j-1};
					queue[q_end] = next_cell;
					q_end++;
					dist[i][j-1] = dist[i][j] + 1;
				}
			}
		}
		
	}
	return -1;
	
}

int find_path_benefit (int rows, int cols, int start_i, int start_j, int mask[rows][cols],int neighbours[rows][cols],int roads[rows][cols],int benefit[rows][cols], int radius, int covered[rows][cols]) {
	
	int i,j;
	
	
	int dist[rows][cols];
	int prev[rows][cols];
	for (i = 0; i < rows; i++){
		for (j = 0; j < cols; j++){
			dist[i][j] = -1;
			prev[i][j] = -1;
		}
	}
	
	GridIndex queue[rows*cols];
	int queue_start = 0;
	int queue_end = 0;
	
	GridIndex first_cell = {start_i, start_j};
	queue[0] = first_cell;
	queue_end++;
	dist[start_i][start_j] = 0;
	
	while(queue_start < queue_end){
		GridIndex cell = queue[queue_start];
		queue_start++;
		
		i = cell.i;
		j = cell.j;
		
		if(neighbours[i][j]==1) {
			GridIndex list[rows*cols];
			
			int xx;
			for (xx = 0; xx < rows*cols; xx++){
				list[xx].i=-1;
				list[xx].j=-1;
			}
			
			int list_end = 0;
			
			int x,y,prev_idx;
			x=i;
			y=j;
						
			roads[x][y] = 1;
			GridIndex addition = {x,y};
			list[list_end++] = addition;
			prev_idx = prev[x][y];
			
			while (prev_idx >= 0) {
				x = prev_idx / cols;
				y = prev_idx % cols;
				
				roads[x][y] = 1;
				GridIndex addition1 = {x,y};
				list[list_end++] = addition1;
				prev_idx = prev[x][y];
			}
			
			covered_bfs_list (rows, cols, radius, covered, mask, list);
			limited_bfs_list(rows, cols, radius, covered, mask, benefit, list);
			
			return -22;
		}
		
		
		if (!mask[i][j]) //If mask = 0, the cell is invalid
			continue;
		
		if (i+1 < rows){
			if (mask[i+1][j] == 1) {
				if (dist[i+1][j]==-1) {
					GridIndex next_cell = {i+1,j};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i+1][j] = dist[i][j] + 1;
					prev[i+1][j] = i*cols+j;
				}
			}
		}
		if (i-1 >= 0){
			if (mask[i-1][j] == 1) {
				if (dist[i-1][j]==-1) {
					GridIndex next_cell = {i-1,j};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i-1][j] = dist[i][j] + 1;
					prev[i-1][j] = i*cols+j;
				}
			}
		}
		if (j+1 < cols){
			if (mask[i][j+1] == 1) {
				if (dist[i][j+1]==-1) {
					GridIndex next_cell = {i,j+1};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i][j+1] = dist[i][j] + 1;
					prev[i][j+1] = i*cols+j;
				}
			}
		}
		if (j-1 >= 0){
			if (mask[i][j-1] == 1) {
				if (dist[i][j-1]==-1) {
					GridIndex next_cell = {i,j-1};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i][j-1] = dist[i][j] + 1;
					prev[i][j-1] = i*cols+j;
				}
			}
		}
	}
	
	return -9999;
}

int bfs_along_roads (int rows, int cols, int mask[rows][cols], int input[rows][cols], int roads[rows][cols], int dist[rows][cols]) {
	
	int i,j;
	GridIndex queue[rows*cols];
	int q_start = 0;
	int q_end = 0;
	
	//print_array(rows,cols,dist);
	
	for (i = 0; i < rows; i++) {
		for (j = 0; j < cols; j++) {
			if (input[i][j] == 1) {
				dist[i][j] = 0;
				queue[q_end].i = i;
				queue[q_end].j = j;
				q_end++;
			}
		}
	}
	
	while (q_start<q_end) {
		GridIndex cell = queue[q_start];
		q_start++;
		i = cell.i;
		j = cell.j;
		if (mask[i][j] == 0)
			continue;

		if (i+1 < rows){
			if (dist[i+1][j] < 0){
				if (mask[i+1][j] == 1) {
					if (roads[i+1][j]) {
						GridIndex next_cell = {i+1,j};
						queue[q_end] = next_cell;
						q_end++;
						dist[i+1][j] = dist[i][j] + 1;
					}
				}
			}
		}
		
		if (i-1 >= 0){
			if (dist[i-1][j] < 0){
				if (mask[i-1][j] == 1) {
					if (roads[i-1][j]) {
						GridIndex next_cell = {i-1,j};
						queue[q_end] = next_cell;
						q_end++;
						dist[i-1][j] = dist[i][j] + 1;
					}
				}
			}
		}
		
		if (j+1 < cols){
			if (dist[i][j+1] < 0){
				if (mask[i][j+1] == 1) {
					if (roads[i][j+1]) {
						GridIndex next_cell = {i,j+1};
						queue[q_end] = next_cell;
						q_end++;
						dist[i][j+1] = dist[i][j] + 1;
					}
				}
			}
		}
		
		if (j-1 >= 0){
			if (dist[i][j-1] < 0){
				if (mask[i][j-1] == 1) {
					if (roads[i][j-1]) {
						GridIndex next_cell = {i,j-1};
						queue[q_end] = next_cell;
						q_end++;
						dist[i][j-1] = dist[i][j] + 1;
					}
				}
			}
		}
		
	}
	return -1;
	
}