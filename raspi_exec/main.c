#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>


#define VISIO_CENTRE_PORT "/dev/video0"
#define VISIO_COIN_PORT "/dev/video1"

int main(int argc, char **argv) {
	if (argc < 3) {
		printf("Specify path to coupe14 : ./raspi path color\n");
		exit(EXIT_FAILURE);
	}
	const char *path, *color;
	path = argv[1];
	color = argv[2];
	pid_t pid_hokuyo, pid_cameras;
	pid_hokuyo = fork();
	if (pid_hokuyo == 0) {
		//Programme hokuyo
		char exec[100], pipe[100]; 
		strcpy(exec, path);
		strcat(exec, "/hokuyo/hokuyo");
		strcpy(pipe, path);
		strcat(pipe, "/config/raspi/pipe_hokuyo");

		execl(exec, color, pipe, (char *)NULL);
	} else {
		printf("Spawned hokuyo, pid %d\n", pid_hokuyo);
		//CAMERAS CONFIG
		
		//exec path
		char exec[100];
		strcpy(exec, path);
		strcat(exec, "/supervisio/visio");

		//config path couleur
		char config[100]; 
		strcpy(config, path);
		strcat(config, "/config/visio/");
		if (strcmp(color, "red")) {
			strcat(config, "visio_tourelle_red/");
		} else if (strcmp(color, "yellow")) {
			strcat(config, "visio_tourelle_yellow/");
		} else {
			printf("Couleur incorrecte\n");
			kill(pid_hokuyo, 9);
			exit(EXIT_FAILURE);
		}

		//config path position
		char config_centre[100];
		strcpy(config_centre, config);
		strcat(config_centre, "centre/");

		pid_cameras = fork();
		if (pid_cameras == 0) {
			//Cameras

		} else {
			printf("Spawned cameras, pid %d\n", pid_cameras);
			//Suite du main
		}
	}
	return 0;
}

