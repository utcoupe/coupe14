#include "com.h"
#include <stdio.h>

void com_loop(const char* cam_pipe, const char* hok_pipe) {
	FILE *cam = 0, *hok = 0;
	printf("[MAIN]  Opening pipe : %s\n", cam_pipe);
	cam = fopen(cam_pipe, "r");
	if (cam < 0) {
		printf("[MAIN]  Failed to open camera pipe\n");
	} else {
		printf("[MAIN]  Pipe opened with cameras\n");
	}

	hok = fopen(hok_pipe, "r");
	if (hok < 0) {
		printf("[MAIN]  Failed to open hokuyo pipe\n");
	} else {
		printf("[MAIN]  Pipe opened with hokuyo\n");
	}
	while (1) {
	}
	fclose(cam);
}
