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
			printf("%d\t",grid[i][j]);
		}
		printf("\n");
	}
}

int find_path_length (int rows, int cols, int start_i, int start_j, int mask[rows][cols],int neighbours[rows][cols],int roads[rows][cols]) {
	
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
	
	int cur;
	while(queue_start < queue_end){
		GridIndex cell = queue[queue_start];
		queue_start++;
		i = cell.i;
		j = cell.j;
		
		if(neighbours[i][j]==1) {
			
			int x,y,prev_idx;
			x=i;
			y=j;
			
			//printf("%d %d\n",x,y);
			roads[x][y] = 1;
			prev_idx = prev[x][y];
			
			while (prev_idx >= 0) {
				x = prev_idx / cols;
				y = prev_idx % cols;
				
				//printf("%d %d\n",x,y);
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
	int count = 0;
	int visited[rows][cols];
	for(i=0;i<rows;i++)
		for(j=0;j<cols;j++)
			visited[i][j]=0;

	
	GridIndex queue[rows*cols];
	GridIndex first_cell = {start_i, start_j};
	int q_start,q_end = 0;
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
	int q_start,q_end = 0;
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

int compute_num_coverable( int rows, int cols, int start_i, int start_j, int radius, int covered[rows][cols], int mask[rows][cols] ){
	
	int totalcells = rows*cols;
	GridIndex queue[rows*cols];
	int queue_start = 0;
	int queue_end = 0;
	
	int dist[rows][cols];
	int i,j;
	for (i = 0; i < rows; i++)
		for (j = 0; j < cols; j++)
			dist[i][j] = -1;
	
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
	int i,j,x,y;
	int limit = 2*radius+1;
	
	int dist[rows][cols];
	for (i=0;i<rows;i++)
		for (j=0;j<cols;j++)
			dist[i][j]=-1;
	dist[start_i][start_j] = 0;
	
	GridIndex queue[rows*cols];
	GridIndex first_cell = {start_i, start_j};
	int q_start,q_end = 0;
	queue[0] = first_cell;
	q_end++;
	
	
	/*
	printf("\nqueue: \n");
	for (i = 0; i < q_end; i++)
		printf("%d %d\n",queue[i].i,queue[i].j);
	
	printf("\n covered: \n");
	for (i=0;i<rows;i++){
		for (j=0;j<cols;j++){
			printf("%d ",covered[i][j]);
		}
		printf("\n");
	}
	
	printf("\n mask: \n");
	for (i=0;i<rows;i++){
		for (j=0;j<cols;j++){
			printf("%d ",mask[i][j]);
		}
		printf("\n");
	}
	
	printf("\n benefit: \n");
	for (i=0;i<rows;i++){
		for (j=0;j<cols;j++){
			printf("%d ",benefit[i][j]);
		}
		printf("\n");
	}
	
	printf("\n dist: \n");
	for (i=0;i<rows;i++){
		for (j=0;j<cols;j++){
			printf("%d ",dist[i][j]);
		}
		printf("\n");
	}
	*/
	//printf("q_start: %d q_end: %d\n",q_start,q_end);
	
	
	
	while (q_start < q_end) {
		GridIndex cell = queue[q_start];
		q_start++;
		
		
		
		i = cell.i;
		j = cell.j;
		
		if (mask[i][j] == 0)
			continue;
		if (dist[i][j] >= limit)
			continue;
		
		/*
		printf("%d %d\n",i,j);
		for (x=0;x<rows;x++){
			for (y=0;y<cols;y++){
				printf("%02d ",dist[x][y]);
			}
			printf("\n");
		}*/
		
		
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
	int q_start,q_end = 0;
	
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
