#include "communication.h"
#include "fast_math.h"

#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <stdio.h>

static FILE *pipe;

void init_protocol(char *path) {
	char *pipe_path = strcat(path, "/hokuyo_pipe");
	mkfifo(pipe_path, 0666);
	pipe = fopen(pipe_path, "w+");
}

// !t;x1:y1;x2:y2;\n
void pushResults(struct coord *coords, int nbr, long timestamp) {
	int i=0;
	fprintf(pipe, "!%ld;", timestamp);
	for(i=0; i<nbr; i++) {
		fprintf(pipe, "%d:%d;", coords[i].x, coords[i].y);
	}
	fprintf(pipe, "\n");
}
