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
static pid_t pid_hokuyo = 0, pid_cameras = 0;

void exit_handler() {
	static int done = 0;
	if (!done) {
		done = 1;
		if (pid_cameras != 0) {
			kill(pid_cameras, SIGINT);
		}
		if (pid_hokuyo != 0) {
			kill(pid_hokuyo, SIGINT);
		}
		printf("[MAIN]  Waiting for children to end\n");
		waitpid(pid_cameras, NULL, 0);
		waitpid(pid_hokuyo, NULL, 0);
		char cmd[255] = "rm ";
		system(strcat(cmd, pipe_cam));
		strcpy(cmd, "rm ");
		system(strcat(cmd, pipe_hok));
		printf("[MAIN]  Deleted pipes\n");
	}
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

	//Path hokuyo
	strcpy(pipe_hok, path);
	strcat(pipe_hok, "/config/raspi/pipe_hokuyo");

	printf("%d - Initializing fifo for cameras\n", getpid());
	mkfifo(pipe_hok, 0666);

	//Path cam
	char pipe[100]; 
	strcpy(pipe_cam, path);
	strcat(pipe_cam, "/config/raspi/pipe_cameras");

	printf("%d - Initializing fifo for hokuyo\n", getpid());
	//Ouvrir fifo
	mkfifo(pipe_cam, 0666);

	pid_hokuyo = fork();
	if (pid_hokuyo == 0) {
		usleep(500000); //Le temps de créer les subprocess
		//Programme hokuyo
		char exec[100];
		strcpy(exec, path);
		strcat(exec, "/hokuyo/hokuyo");

		printf("%d - Hokuyo starting...\n", getpid());
		execl(exec, "hokuyo", color, path, (char *)NULL);
	} else {
		printf("%d - Spawned hokuyo, pid %d\n", getpid(), pid_hokuyo);

		pid_cameras = fork();
		if (pid_cameras == 0) {
			usleep(500000); //Le temps de créer les subprocess
			//Cameras
			//path python
			char exec[] = "/usr/bin/python3", file[255];
			strcpy(file, path);
			strcat(file, "/raspi_exec/visio_raspi.py");
			printf("%d - Cameras starting...\n", getpid());
			execl(exec, "python3", file, path, color, (char *)NULL);
		} else {
			signal(SIGUSR1, exit_handler);
			signal(SIGINT, exit_handler);
			atexit(exit_handler);
			printf("%d - Spawned cameras, pid %d\n", getpid(), pid_cameras);
			//Suite du main
			printf("[MAIN]  Waiting for initialization\n");
			sleep(5);
			
			printf("[MAIN]  Starting main program\n");
			com_loop(pipe_cam, pipe_hok);
		}
	}
	return 0;
}

