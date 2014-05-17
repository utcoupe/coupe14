#include "lidar.h"
#include "global.h"
#include "robot.h"
#include "communication.h"
#include "compat.h"

#include <sys/types.h>
#include <urg_ctrl.h>
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
static struct lidar l1, l2;
#ifdef SDL
static struct color l1Color, l2Color;
#endif

long startTime, lastTime = 0;
static struct coord robots1[MAX_ROBOTS], robots2[MAX_ROBOTS];

void exit_handler() {
	printf("\n%sClosing lidar(s), please wait...\n", PREFIX);
	if (l1.lidarObject != 0)
		urg_disconnect(l1.lidarObject);
	if (l2.lidarObject != 0)
		urg_disconnect(l2.lidarObject);
	printf("%sExitting\n", PREFIX);
	//kill(getppid(), SIGUSR1); //Erreur envoyee au pere
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

	struct coord posl1, posl2;
	float angle1, angle2, a1min, a2min, a1max, a2max;

	posl1.y = HOK1_Y;
	if( strcmp(argv[1], "red") == 0 ){
		a1min = HOK1_AMIN;
		a1max = HOK1_AMAX;
		angle1 = HOK1_A;
		posl1.x = HOK1_X;	
	}else{
		angle1 = PI - HOK1_A;
		a1min = PI - HOK1_AMIN;
		a1max = PI - HOK1_AMAX;
		posl1.x = TAILLE_TABLE_X-HOK1_X;
	}

	posl2.y = HOK2_Y;
	if( strcmp(argv[1], "red") == 0 ){
		angle2 = HOK2_A;
		a2min = HOK2_AMIN;
		a2max = HOK2_AMAX;
		posl2.x = HOK2_X;
	}else{
		angle2 = PI - HOK2_A;
		a2min = PI - HOK2_AMIN;
		a2max = PI - HOK2_AMAX;
		posl2.x = TAILLE_TABLE_X - HOK2_X;	
	}

	char *path = 0;
	if (argc == 3) {
		path = argv[2];
		use_protocol = 1;
	}

	l1 = initLidar("/dev/ttyACM0", posl1, angle1, a1min, a1max);
	//l1 = initLidarAndCalibrate("/dev/ttyACM0", posl1, angle1, a1min, a1max);
	l2 = initLidar("/dev/ttyACM1", posl2, angle2, a2min, a2max);
	//l2 = initLidarAndCalibrate("/dev/ttyACM1", posl2, angle2, a2min, a2max);


	#ifdef SDL
	l1Color = newColor(255, 0, 0);
	l2Color = newColor(0, 0, 255);
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
	getPoints(&l2);
	timestamp = timeMillis() - startTime;
	printf("%sDuration : %lims\n", PREFIX, timestamp-lastTime);
	int nRobots1 = getRobots(l1.points, l1.fm.n, robots1);
	int nRobots2 = getRobots(l2.points, l2.fm.n, robots2);
	#ifdef SDL
	blitMap();
	blitLidar(l1.pos, l1Color);
	blitLidar(l2.pos, l2Color);
	blitRobots(robots1, nRobots1);
	blitRobots(robots2, nRobots2);
	blitPoints(l1.points, l1.fm.n, l1Color);
	blitPoints(l2.points, l2.fm.n, l2Color);
	waitScreen();
	#endif
	if (use_protocol){
		//pushResults(robots1, nRobots1, timestamp);
	}
	else{
		printf("%sHOK1 - %li;%i", PREFIX, timestamp, nRobots1);
		for(int i=0; i<nRobots1; i++){
			printf(";%i:%i", robots1[i].x, robots1[i].y);
		}
		printf("\n");
		printf("%sHOK2 - %li;%i", PREFIX, timestamp, nRobots2);
		for(int i=0; i<nRobots2; i++){
			printf(";%i:%i", robots2[i].x, robots2[i].y);
		}
		printf("\n");
	}
	lastTime = timestamp;
}

