#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/wait.h>

#include "com.h"

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

static char pipe_hok[255], pipe_cam[255];

void exit_handler() {
	static int done = 0;
	if (!done) {
		char cmd[255] = "rm ";
		system(strcat(cmd, pipe_cam));
		strcpy(cmd, "rm ");
		system(strcat(cmd, pipe_hok));
		printf("Deleted pipes\n");
		done = 1;
	}
	exit(EXIT_FAILURE);
}

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
		char exec[100];
		strcpy(exec, path);
		strcat(exec, "/hokuyo/hokuyo");
		strcpy(pipe_hok, path);
		strcat(pipe_hok, "/config/raspi/pipe_hokuyo");

		printf("%d - Initilizing fifo for hokuyo\n", getpid());
		//Ouvrir fifo
		mkfifo(pipe_hok, 0666);

		printf("%d - Hokuyo starting...\n", getpid());
		execl(exec, "hokuyo", color, path, (char *)NULL);
	} else {
		printf("%d - Spawned hokuyo, pid %d\n", getpid(), pid_hokuyo);
		//CAMERAS CONFIG
		
		//exec path
		char exec[] = "/usr/bin/python3";

		//path script python
		char file[100], pipe[100]; 
		strcpy(pipe_cam, path);
		strcat(pipe_cam, "/config/raspi/pipe_cameras");
		strcpy(file, path);
		strcat(file, "/raspi_exec/visio_raspi.py");

		pid_cameras = fork();
		if (pid_cameras == 0) {
			//Cameras
			printf("%d - Initializing fifo for cameras\n", getpid());
			mkfifo(pipe_cam, 0666);
			printf("%d - Cameras starting...\n", getpid());
			execl(exec, "python3", file, path, color, (char *)NULL);
		} else {
			signal(SIGINT, exit_handler);
			printf("%d - Spawned cameras, pid %d\n", getpid(), pid_cameras);
			//Suite du main
			sleep(1);
			
			printf("[MAIN]  Starting main program\n");
			com_loop(pipe_cam, pipe_hok);

			printf("[MAIN]  Waiting for children to end\n");
			waitpid(pid_cameras, NULL, 0);
			waitpid(pid_hokuyo, NULL, 0);
			exit_handler();
		}
	}
	return 0;
}

