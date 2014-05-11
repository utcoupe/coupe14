#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>

/*************************************************************
 *                                                           *
 *            Programme père du raspberry pi                 *
 *                                                           *
 *                          protocole                        *
 *                              |                            *
 *                              |                            *
 *                            raspi                          *
 *                            /    \                         *
 *                      hokuyo     visio_raspi               *
 *                                /            \             *
 *                        cam_centre           cam_coin      *
 *                                                           *
 *                                                           *
 ************************************************************/

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
	if (!(strcmp(color, "red") == 0 || strcmp(color, "yellow") == 0)) {
		printf("Couleur incorrecte : red/yellow\n");
		exit(EXIT_FAILURE);
	}
	pid_t pid_hokuyo, pid_cameras;
	pid_hokuyo = fork();
	if (pid_hokuyo == 0) {
		//Programme hokuyo
		char exec[100], pipe[100]; 
		strcpy(exec, path);
		strcat(exec, "/hokuyo/hokuyo");
		strcpy(pipe, path);
		strcat(pipe, "/config/raspi/pipe_hokuyo");

		printf("%d - Initilizing fifo for hokuyo\n", getpid());
		//Ouvrir fifo
		mkfifo(pipe, 0666);

		printf("%d - Hokuyo starting...\n", getpid());
		execl(exec, color, pipe, (char *)NULL);
	} else {
		printf("%d - Spawned hokuyo, pid %d\n", getpid(), pid_hokuyo);
		//CAMERAS CONFIG
		
		//exec path
		char exec[] = "python3";

		//path script python
		char file[100], pipe[100]; 
		strcpy(pipe, path);
		strcat(pipe, "/config/raspi/pipe_cameras");
		strcpy(file, path);
		strcat(file, "/raspi_exec/visio_raspi.py");

		pid_cameras = fork();
		if (pid_cameras == 0) {
			//Cameras
			printf("%d - Initilizing fifo for cameras\n", getpid());
			mkfifo(pipe, 0666);
			printf("%d - Cameras starting...\n", getpid());
			execl(exec, file, pipe, color, (char *)NULL);

		} else {
			printf("%d - Spawned cameras, pid %d\n", getpid(), pid_cameras);
			//Suite du main
		}
	}
	return 0;
}

