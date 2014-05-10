#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char **argv) {
	if (argc < 2) {
		printf("Specify path to config : ./raspi path\n");
		exit(EXIT_FAILURE);
	}
	char *path;
	path = argv[1];
	pid_t pid_hokuyo, pid_cam_centre, pid_cam_coin;
	pid_hokuyo = fork();
	if (pid_hokuyo == 0) {
		//Programme hokuyo
	} else {
		printf("Spawned hokuyo, pid %d\n", pid_hokuyo);
		pid_cam_centre = fork();
		if (pid_cam_centre == 0) {
			//Cam centre
		} else {
			printf("Spawned cam_centre, pid %d\n", pid_cam_centre);
			pid_cam_coin = fork();
			if (pid_cam_coin == 0) {
				//Cam coin
			} else {
				printf("Spawned cam_coin, pid %d\n", pid_cam_coin);
				//Suite du main
			}
		}
	}
	return 0;
}

