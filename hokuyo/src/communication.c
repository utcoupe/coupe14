#include "communication.h"
#include "fast_math.h"

#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <stdio.h>

static FILE *pipe = 0;

void init_protocol(char *path) {
	char pipe_path[255];
	strcpy(pipe_path, path);
	strcat(pipe_path, "/config/raspi/pipe_hokuyo");
	printf("%sInitialisation du protcole, fifo : %s\n", PREFIX, pipe_path);
	pipe = fopen(pipe_path, "w+");
	if (pipe == 0) {
		printf("Failed to open fifo at %s\n", pipe_path);
		exit(EXIT_FAILURE);
	} else {
		printf("%sFifo opened\n", PREFIX);
	}
}

// !t;x1:y1;x2:y2;\n
void pushResults(struct coord *coords, int nbr, long timestamp) {
	int i=0;
	fprintf(pipe, "%ld %d", timestamp, nbr);
	for(i=0; i<nbr; i++) {
		fprintf(pipe, " %d %d", coords[i].x, coords[i].y);
	}
	fprintf(pipe, "\n");
	fflush(pipe);
}
