#include "lidar.h"
#include "global.h"
#include "robot.h"
#include "communication.h"
#include "compat.h"

#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>

#ifdef SDL
#include "gui.h"
#endif

void frame();

static int use_protocol = 0;
static struct lidar l1;
#ifdef SDL
static struct color l1Color;
#endif

long startTime, lastTime = 0;
static struct coord robots[MAX_ROBOTS];

void exit_handler() {
	printf("\n%sClosing lidar(s), please wait...\n", PREFIX);
	closeLidar(&l1);
	printf("%sExitting\n", PREFIX);
	kill(getppid(), SIGUSR1); //Erreur envoyee au pere
}

static void catch_SIGINT(int signal){
	exit(EXIT_FAILURE);
}

int main(int argc, char **argv){
	atexit(exit_handler);
	
	if(argc <= 1 || ( strcmp(argv[1], "red") != 0 && strcmp(argv[1], "yellow") ) ){
		fprintf(stderr, "usage: hokuyo {red|yellow} [path_pipe]\n");
		exit(EXIT_FAILURE);
	}

	if (signal(SIGINT, catch_SIGINT) == SIG_ERR) {
        fputs("An error occurred while setting a signal handler for SIGINT.\n", stderr);
		exit(EXIT_FAILURE);
    }

	struct coord posl1;
	posl1.y = -25;
	if( strcmp(argv[1], "red") == 0 ){
		posl1.x = -25;	
	}else{
		posl1.x = TAILLE_TABLE_X+25;
	}

	char *path = 0;
	if (argc == 3) {
		path = argv[2];
		use_protocol = 1;
	}

	//l1 = initLidarAndCalibrate( hokuyo_urg, "/dev/ttyACM0", posl1, PI/2, 0, PI/2);
	l1 = initLidar( hokuyo_urg, "/dev/ttyACM0", posl1, 0, 0, PI/2);


	#ifdef SDL
	l1Color = newColor(255, 0, 0);
	initSDL();
	#endif

	if (use_protocol) {
		init_protocol(path);
	}

	startTime = timeMillis();
	printf("%sRunning ! ...\n", PREFIX);
	while(1){
		frame();
	}
	exit(EXIT_SUCCESS);
}

void frame(){
	long timestamp;
	getPoints(&l1);
	timestamp = timeMillis() - startTime;
	//printf("%sDuration : %lims\n", PREFIX, timestamp-lastTime);
	if(lastTime != 0 && timestamp-lastTime > HOKUYO_WATCHDOG){
		printf("%s WatchDog exceeded: %li > %li\n", PREFIX, timestamp-lastTime, (long int)HOKUYO_WATCHDOG);
		restartLidar(&l1);
	}
	//printf("nPoints:%i\n", l1.fm.n);
	int nRobots = getRobots(l1.points, l1.fm.n, robots);
	#ifdef SDL
	blitMap();
	blitLidar(l1.pos, l1Color);
	blitRobots(robots, nRobots);
	blitPoints(l1.points, l1.fm.n, l1Color);
	waitScreen();
	#endif
	if (use_protocol){
		pushResults(robots, nRobots, timestamp);
	}
	else{
		printf("%s%li;%i", PREFIX, timestamp, nRobots);
		for(int i=0; i<nRobots; i++){
			printf(";%i:%i", robots[i].x, robots[i].y);
		}
		printf("\n");
	}
	lastTime = timestamp;
}

