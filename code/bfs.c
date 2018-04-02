#include <stdio.h>
#include <stdlib.h>

//Compile this with: gcc -O3 -o code/bfs.so -fPIC -shared code/bfs.c

typedef struct{
	int i,j;
} GridIndex;

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