#include "communication.h"
#include "fast_math.h"

#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <string.h>
#include <stdio.h>

static FILE *pipe = 0;

void init_protocol(char *path) {
	pipe = fopen(path, "w+");
	if (pipe == 0) {
		printf("Failed to open pipe at %s\n", path);
		exit(EXIT_FAILURE);
	}
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
