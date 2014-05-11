#include "com.h"
#include <stdlib.h>
#include <stdio.h>

void com_loop(const char* cam_pipe, const char* hok_pipe) {
	FILE *cam = 0, *hok = 0;
	printf("[MAIN]  Opening pipe : %s\n", cam_pipe);
	cam = fopen(cam_pipe, "r");
	if (cam == 0) {
		printf("[MAIN]  Failed to open camera pipe\n");
		exit(EXIT_FAILURE);
	} else {
		printf("[MAIN]  Pipe opened with cameras\n");
	}

	printf("[MAIN]  Opening pipe : %s\n", hok_pipe);
	hok = fopen(hok_pipe, "r");
	if (hok == 0) {
		printf("[MAIN]  Failed to open hokuyo pipe\n");
		exit(EXIT_FAILURE);
	} else {
		printf("[MAIN]  Pipe opened with hokuyo\n");
	}
	while (1) {
		char buffer[255];
		fscanf(cam, "%s\n", buffer);
		printf("[MAIN-CAM]  %s\n", buffer);
		/*fscanf(hok, "%s\n", buffer);
		printf("[MAIN-HOK]  %s\n", buffer);*/
	}
	fclose(cam);
}
