#include <stdio.h>
#include <stdlib.h>

//Compile this with: gcc -O3 -o compute_num_coverable.so -fPIC -shared compute_num_coverable.c

typedef struct{
	int i,j;
} GridIndex;

int compute_num_coverable( int rows, int cols, int start_i, int start_j, int radius, int covered[rows][cols], int mask[rows][cols] ){
	
	//printf("a  \n");
	//int dist[rows][cols];	
	int** dist;
	dist = (int**) malloc(rows*sizeof(int*));
	for (int i = 0; i < rows; i++)
	   dist[i] = (int*) malloc(cols*sizeof(int));
	//printf("b  \n");
	int i,j;
	for (i = 0; i < rows; i++)
		for (j = 0; j < cols; j++)
			dist[i][j] = -1;
	//printf("c  \n");
	
	GridIndex *queue = malloc(rows*cols * sizeof(GridIndex));
	//printf("d  \n");
	for (i=0;i<rows*cols;i++) {
		GridIndex* a = &queue[i];
		a = malloc(sizeof(GridIndex));
	}
	//printf("e  \n");

	/*
	printf("Covered\n");
	
	for (i = 0; i < rows; i++){
		for (j = 0; j < cols; j++)
			printf("%d ",covered[i][j]);
		printf("\n");
	}
	printf("Mask\n");
	
	for (i = 0; i < rows; i++){
		for (j = 0; j < cols; j++)
			printf("%d ",mask[i][j]);
		printf("\n");
	}
	*/
	
	int total_found = 0;
	int queue_start = 0;
	int queue_end = 0;
	GridIndex first_cell = {start_i, start_j};
	queue[0] = first_cell;
	queue_end++;
	dist[start_i][start_j] = 0;
	printf("1  \n");
	while(queue_start < queue_end){
		GridIndex cell = queue[queue_start];
		queue_start++;
		printf("2  \n");
		i = cell.i;
		j = cell.j;
		if (!mask[i][j]) //If mask = 0, the cell is invalid
			continue;
		if (dist[i][j] > radius)
			continue;
		printf("3  \n");
		if (!covered[i][j])
			total_found++;
		printf("4  \n");
		//Test each neighbour
		if (i+1 < rows){
			if (dist[i+1][j] < 0){
				if (mask[i+1][j] == 1) {
					printf("5  \n");
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
					printf("6  \n");
					GridIndex next_cell = {i-1,j};
					queue[queue_end] = next_cell;
					queue_end++;
					dist[i-1][j] = dist[i][j] + 1;
				}
			}
		}
		if (j+1 < rows){
			if (dist[i][j+1] < 0){
				if (mask[i][j+1] == 1) {
					printf("7  \n");
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
					printf("8  \n");
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